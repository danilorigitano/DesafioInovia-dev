import csv
import numpy as np
from pathlib import Path

# Optional pandas import for nicer DataFrame display; fallback to csv reader if unavailable
try:
    import pandas as pd
except Exception:
    pd = None

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

def integrate_dados_relevantes_with_medidas(medidas_csv_name='medidas_dados_sinteticos.csv',
                                           relevantes_csv_name='DadosRelevantes.csv',
                                           output_csv_name='DadosRelevantesIntegrados.csv'):
    """
    Integra o arquivo `DadosRelevantes.csv` com `medidas_dados_sinteticos.csv`
    buscando as colunas extras (height,chest_circ,waist_circ,hip_circ,thigh_circ,
    knee_circ,calf_circ,abd_circ,neck_circ,biceps_circ,split) pelo campo `id`.

    Retorna o DataFrame `Integrado` (pandas) e grava o CSV `DadosRelevantesIntegrados.csv`
    na mesma pasta do módulo.
    """
    current_dir = Path(__file__).parent

    medidas_path = current_dir.parent / medidas_csv_name
    relevantes_path = current_dir / relevantes_csv_name
    output_path = current_dir / output_csv_name

    if pd is None:
        raise ImportError('pandas é necessário para esta função. Instale pandas e tente novamente.')

    if not medidas_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {medidas_path}")
    if not relevantes_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {relevantes_path}")

    # Lê os CSVs com pandas
    medidas_df = pd.read_csv(medidas_path, encoding='utf-8')
    relevantes_df = pd.read_csv(relevantes_path, encoding='utf-8')

    # Detecta automaticamente o nome da coluna de ID (p.ex. 'id' ou 'Id') e normaliza para 'id'
    def _find_id_col(df):
        for c in df.columns:
            if str(c).strip().lower() == 'id':
                return c
        # fallback: considera a primeira coluna como ID
        return df.columns[0]

    medidas_id_col = _find_id_col(medidas_df)
    relevantes_id_col = _find_id_col(relevantes_df)

    medidas_df[medidas_id_col] = medidas_df[medidas_id_col].astype(str).str.strip()
    relevantes_df[relevantes_id_col] = relevantes_df[relevantes_id_col].astype(str).str.strip()

    # Renomeia para 'id' para unificar as operações de merge
    if medidas_id_col != 'id':
        medidas_df = medidas_df.rename(columns={medidas_id_col: 'id'})
    if relevantes_id_col != 'id':
        relevantes_df = relevantes_df.rename(columns={relevantes_id_col: 'id'})

    # Seleciona somente as colunas de medidas extras esperadas (se existirem)
    expected_cols = ['height','chest_circ','waist_circ','hip_circ','thigh_circ',
                     'knee_circ','calf_circ','abd_circ','neck_circ','biceps_circ','split']
    present_cols = [c for c in expected_cols if c in medidas_df.columns]

    if len(present_cols) == 0:
        raise ValueError(f"Nenhuma das colunas esperadas encontradas em {medidas_path}: {expected_cols}")

    # Filtra medidas_df apenas para ids que aparecem em relevantes_df, usando intersection/is in
    ids_medidas = pd.Index(medidas_df['id'].unique())
    ids_relevantes = pd.Index(relevantes_df['id'].unique())
    common_ids = ids_medidas.intersection(ids_relevantes)

    if common_ids.empty:
        print('[WARN] Nenhuma correspondência de IDs encontrada entre os arquivos.')

    medidas_filtradas = medidas_df[medidas_df['id'].isin(common_ids)].copy()

    # Faz merge (left) dos dados relevantes com as medidas (mantendo a ordem de relevantes_df)
    integrado_df = relevantes_df.merge(medidas_filtradas[['id'] + present_cols], on='id', how='left')

    # Salva arquivo integrado
    try:
        integrado_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"[SAVED] Arquivo integrado salvo em: {output_path}")
    except Exception as e:
        print(f"[ERROR] Falha salvando arquivo integrado: {e}")

    # Disponibiliza o DataFrame como variável global para uso interativo
    globals()['Integrado'] = integrado_df
    return integrado_df

if __name__ == "__main__":
    # Por padrão exibe apenas o DataFrame de `DadosRelevantes.csv` quando executado diretamente.
    def show_dados_relevantes():
        current_dir = Path(__file__).parent
        csv_file = current_dir / 'DadosRelevantes.csv'
        if not csv_file.exists():
            print(f"[ERROR] Arquivo não encontrado: {csv_file}")
            raise SystemExit(1)

        if pd is not None:
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
                print(df)
                return df
            except Exception as e:
                print(f"[WARN] Falha lendo com pandas: {e} - tentando csv.reader")

        # Fallback: leitura simples com csv.reader
        data = read_csv(csv_file)
        for row in data:
            print(','.join(map(str, row)))
        return data

    show_dados_relevantes()
    # Tenta integrar com medidas (arquivo medidas_dados_sinteticos.csv está na pasta parent)
    try:
        integrated = integrate_dados_relevantes_with_medidas()
        if integrated is not None:
            print('\n[Integrado] Resultado da integração:')
            print(integrated.head(20))
    except Exception as e:
        print(f"[WARN] Integração não realizada: {e}")