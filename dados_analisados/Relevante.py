import csv
import numpy as np
from pathlib import Path

def read_csv(file_path):
    """Lê um arquivo CSV e retorna os dados como lista de listas."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data):
    """Escreve dados em um arquivo CSV."""
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except PermissionError:
        # Tenta salvar em arquivo alternativo para evitar falha completa
        backup = str(file_path) + '.tmp'
        try:
            with open(backup, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"Aviso: não foi possível escrever em {file_path}. Gravado em {backup} em vez disso.")
        except Exception as e:
            print(f"Erro escrevendo arquivo {file_path} e fallback {backup}: {e}")

def reparametrize_data(data, start_pos, end_pos, new_size=1000):
    """
    Reparametriza os dados entre start_pos e end_pos para uma nova função 
    enumerada entre 1 e new_size.
    """
    if start_pos >= end_pos or start_pos < 0 or end_pos > len(data):
        return []
    
    # Extrai os dados entre as posições especificadas
    relevant_data = data[start_pos:end_pos]
    
    if len(relevant_data) == 0:
        return []
    
    # Converte para numpy array para facilitar interpolação
    try:
        relevant_data = np.array([float(x) if x != '' else 0 for x in relevant_data])
    except ValueError:
        # Se houver valores não numéricos, tenta conversão mais robusta
        processed_data = []
        for x in relevant_data:
            try:
                processed_data.append(float(x) if x != '' else 0)
            except ValueError:
                processed_data.append(0)
        relevant_data = np.array(processed_data)
    
    # Cria nova escala de 1 a new_size
    old_indices = np.linspace(0, len(relevant_data)-1, len(relevant_data))
    new_indices = np.linspace(0, len(relevant_data)-1, new_size)
    
    # Interpola os dados para o novo tamanho
    reparametrized = np.interp(new_indices, old_indices, relevant_data)
    
    return reparametrized.tolist()

def process_parametrization():
    """Processa a parametrização dos dados de silhueta baseado nos bounding boxes."""
    
    current_dir = Path(__file__).parent
    
    # Arquivos de entrada
    bbox_files = {
        'front': 'DadosmedidosCSV--front--boundingbox.csv',
        'left': 'DadosmedidosCSV--left--boundingbox.csv'
    }
    
    silhueta_files = {
        'front_vetorcoluna': 'DadosMedidosCSV--front--vetorcoluna--silhueta.csv',
        'front_vetorlinha': 'DadosMedidosCSV--front--vetorlinha--silhueta.csv',
        'left_vetorcoluna': 'DadosMedidosCSV--left--vetorcoluna--silhueta.csv',
        'left_vetorlinha': 'DadosMedidosCSV--left--vetorlinha--silhueta.csv'
    }
    
    # Arquivos de saída
    output_files = {
        'front_vetorcoluna': 'DadosParametrizados--front--vetorcoluna--silhueta.csv',
        'front_vetorlinha': 'DadosParametrizados--front--vetorlinha--silhueta.csv',
        'left_vetorcoluna': 'DadosParametrizados--left--vetorcoluna--silhueta.csv',
        'left_vetorlinha': 'DadosParametrizados--left--vetorlinha--silhueta.csv'
    }
    
    # Processa front e left separadamente
    for view in ['front', 'left']:
        print(f"\n{'='*60}")
        print(f"Processando view: {view.upper()}")
        print(f"{'='*60}")
        
        # Lê dados do bounding box
        bbox_file = current_dir / bbox_files[view]
        if not bbox_file.exists():
            print(f"[ERROR] Arquivo não encontrado: {bbox_file}")
            continue
            
        bbox_data = read_csv(bbox_file)
        if len(bbox_data) < 2:
            print(f"[ERROR] Arquivo bbox vazio ou sem dados: {bbox_file}")
            continue
            
        bbox_header = bbox_data[0]
        bbox_rows = bbox_data[1:]
        
        print(f"[INFO] Cabeçalho bbox: {bbox_header}")
        
        # Cria dicionário de bounding boxes por ID (normaliza IDs removendo sufixo --front/--left)
        bbox_dict = {}
        invalid_rows = 0
        
        for row in bbox_rows:
            if len(row) >= 5:  # Id, x1, x2, y2, y3
                raw_id = row[0].strip()
                # Normaliza removendo sufixos como '--front' ou '--left' (se presentes)
                base_id = raw_id.split('--')[0].strip()
                try:
                    x1, x2, y2, y3 = int(row[1]), int(row[2]), int(row[3]), int(row[4])
                    bbox_dict[base_id] = {'x1': x1, 'x2': x2, 'y2': y2, 'y3': y3}
                except (ValueError, IndexError):
                    invalid_rows += 1
                    continue
        
        print(f"[OK] BBox carregados para {view}: {len(bbox_dict)} registros válidos")
        if invalid_rows > 0:
            print(f"[WARN] Linhas bbox inválidas ignoradas: {invalid_rows}")
        
        # Processa vetorcoluna
        print(f"\n[STEP] Processando vetorcoluna...")
        vetorcoluna_file = current_dir / silhueta_files[f'{view}_vetorcoluna']
        if vetorcoluna_file.exists():
            silhueta_data = read_csv(vetorcoluna_file)
            if len(silhueta_data) < 2:
                print(f"[ERROR] Arquivo vetorcoluna vazio: {vetorcoluna_file}")
            else:
                header = silhueta_data[0]
                rows = silhueta_data[1:]
                
                parametrized_data = []
                parametrized_data.append(['Id'] + [str(i+1) for i in range(1000)])  # Header com 1000 colunas
                
                processed_count = 0
                error_count = 0
                not_found_count = 0
                
                for row in rows:
                    if len(row) > 1:
                        id_key = row[0].strip()
                        # Usa id base (sem sufixo) para procurar no dicionário
                        if id_key in bbox_dict:
                            x1 = bbox_dict[id_key]['x1']
                            x2 = bbox_dict[id_key]['x2']

                            # Para vetorcoluna, usamos x1 e x2
                            data_values = row[1:]  # Remove ID
                            len_data = len(data_values)

                            # Ajusta (clampa) os índices para o tamanho dos dados disponíveis
                            x1_clamped = max(1, min(x1, len_data))
                            x2_clamped = max(1, min(x2, len_data))

                            if x1_clamped < x2_clamped:
                                reparametrized = reparametrize_data(data_values, x1_clamped-1, x2_clamped-1, 1000)
                                if reparametrized:
                                    parametrized_data.append([id_key] + reparametrized)
                                    processed_count += 1
                                    if processed_count <= 10 or processed_count % 100 == 0:
                                        print(f"  [OK] Processado {id_key}: x1={x1}->{x1_clamped}, x2={x2}->{x2_clamped}, dados originais={len_data}")
                                else:
                                    error_count += 1
                                    if error_count <= 5:
                                        print(f"  [ERROR] Erro reparametrizando {id_key}: intervalo vazio")
                            else:
                                error_count += 1
                                if error_count <= 5:
                                    print(f"  [ERROR] Erro com {id_key}: x1={x1}, x2={x2}, len_data={len_data} (após clamp x1={x1_clamped}, x2={x2_clamped})")
                        else:
                            not_found_count += 1
                            if not_found_count <= 10:
                                print(f"  [WARN] ID não encontrado no bbox: {id_key}")
                
                # Salva arquivo parametrizado
                output_file = current_dir / output_files[f'{view}_vetorcoluna']
                write_csv(output_file, parametrized_data)
                print(f"[SAVED] Arquivo gerado: {output_file}")
                print(f"  [OK] {processed_count} registros processados com sucesso")
                print(f"  [ERROR] {error_count} registros com erro de processamento")
                print(f"  [WARN] {not_found_count} IDs não encontrados no bbox")
                print(f"  [INFO] Total de linhas no arquivo de entrada: {len(rows)}")
        else:
            print(f"[ERROR] Arquivo não encontrado: {vetorcoluna_file}")
        
        # Processa vetorlinha
        print(f"\n[STEP] Processando vetorlinha...")
        vetorlinha_file = current_dir / silhueta_files[f'{view}_vetorlinha']
        if vetorlinha_file.exists():
            silhueta_data = read_csv(vetorlinha_file)
            if len(silhueta_data) < 2:
                print(f"[ERROR] Arquivo vetorlinha vazio: {vetorlinha_file}")
            else:
                header = silhueta_data[0]
                rows = silhueta_data[1:]
                
                parametrized_data = []
                parametrized_data.append(['Id'] + [str(i+1) for i in range(1000)])  # Header com 1000 colunas
                
                processed_count = 0
                error_count = 0
                not_found_count = 0
                
                for row in rows:
                    if len(row) > 1:
                        id_key = row[0].strip()  # Remove espaços extras
                        if id_key in bbox_dict:
                            y2 = bbox_dict[id_key]['y2']
                            y3 = bbox_dict[id_key]['y3']

                            # Para vetorlinha, usamos y2 e y3
                            data_values = row[1:]  # Remove ID
                            len_data = len(data_values)

                            # Ajusta (clampa) os índices para o tamanho dos dados disponíveis
                            y2_clamped = max(1, min(y2, len_data))
                            y3_clamped = max(1, min(y3, len_data))

                            if y2_clamped < y3_clamped:
                                reparametrized = reparametrize_data(data_values, y2_clamped-1, y3_clamped-1, 1000)  # -1 porque y2,y3 são 1-indexed
                                if reparametrized:
                                    parametrized_data.append([id_key] + reparametrized)
                                    processed_count += 1
                                    if processed_count <= 10 or processed_count % 100 == 0:  # Mostra apenas alguns logs
                                        print(f"  [OK] Processado {id_key}: y2={y2}->{y2_clamped}, y3={y3}->{y3_clamped}, dados originais={len_data}")
                                else:
                                    error_count += 1
                                    if error_count <= 5:
                                        print(f"  [ERROR] Erro reparametrizando {id_key}: intervalo vazio")
                            else:
                                error_count += 1
                                if error_count <= 5:
                                    print(f"  [ERROR] Erro com {id_key}: y2={y2}, y3={y3}, len_data={len_data} (após clamp y2={y2_clamped}, y3={y3_clamped}, intervalo=({y2_clamped}, {y3_clamped}])")
                        else:
                            not_found_count += 1
                            if not_found_count <= 10:
                                print(f"  [WARN] ID não encontrado no bbox: {id_key}")
                
                # Salva arquivo parametrizado
                output_file = current_dir / output_files[f'{view}_vetorlinha']
                write_csv(output_file, parametrized_data)
                print(f"[SAVED] Arquivo gerado: {output_file}")
                print(f"  [OK] {processed_count} registros processados com sucesso")
                print(f"  [ERROR] {error_count} registros com erro de processamento")
                print(f"  [WARN] {not_found_count} IDs não encontrados no bbox")
                print(f"  [INFO] Total de linhas no arquivo de entrada: {len(rows)}")
        else:
            print(f"[ERROR] Arquivo não encontrado: {vetorlinha_file}")
    
    print(f"\n{'='*60}")
    print("[DONE] Processamento concluído!")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_parametrization()