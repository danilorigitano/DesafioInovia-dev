"""
DadosRelevantes.py - Extrai dados específicos dos arquivos parametrizados
"""

import pandas as pd
import csv
from pathlib import Path

def read_csv_safe(file_path):
    """Lê um arquivo CSV e retorna os dados como lista de listas."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.reader(file))

def extract_values_at_positions(data, positions_dict):
    """Extrai valores específicos de cada linha nas posições indicadas."""
    if len(data) < 2:
        return []
    
    rows = data[1:]  # Skip header
    extracted_data = []
    
    for row in rows:
        if len(row) < 2:
            continue
            
        row_data = {'Id': row[0]}
        
        for col_name, position in positions_dict.items():
            if position < len(row):
                try:
                    row_data[col_name] = float(row[position]) if row[position] else 0.0
                except ValueError:
                    row_data[col_name] = 0.0
            else:
                row_data[col_name] = 0.0
        
        extracted_data.append(row_data)
    
    return extracted_data

def process_dados_relevantes():
    """Processa arquivos parametrizados e cria DataFrame consolidado."""
    
    current_dir = Path(__file__).parent
    
    # Arquivos e posições
    files_positions = {
        'DadosParametrizados--front--vetorlinha--silhueta.csv': {
            'Pescoço Front Vetor linha': 150,
            'Peito Front Vetor linha': 300,
            'Abdomen Front Vetor linha': 420,
            'Quadril Front Vetor linha': 473,
            'Coxa Front Vetor linha': 543
        },
        'DadosParametrizados--front--vetorcoluna--silhueta.csv': {
            'Biceps Front Vetor Coluna': 338
        },
        'DadosParametrizados--left--vetorlinha--silhueta.csv': {
            'Pescoço Left Vetor linha': 151,
            'Peito Left Vetor linha': 294,
            'Abdomem Left Vetor linha': 405,
            'Quadril Left Vetor linha': 450,
            'Cintura Left Vetor linha': 490,
            'Coxa Left Vetor linha': 577
        }
    }
    
    # Coleta dados por ID
    all_data_by_id = {}
    
    for filename, positions in files_positions.items():
        file_path = current_dir / filename
        
        if not Path(file_path).exists():
            print(f"❌ Arquivo não encontrado: {file_path}")
            return None
        
        data = read_csv_safe(file_path)
        extracted = extract_values_at_positions(data, positions)
        
        for row_data in extracted:
            id_key = row_data['Id']
            if id_key not in all_data_by_id:
                all_data_by_id[id_key] = {'Id': id_key}
            
            for key, value in row_data.items():
                if key != 'Id':
                    all_data_by_id[id_key][key] = value
    
    # Cria DataFrame
    consolidated_data = list(all_data_by_id.values())
    consolidated_data.sort(key=lambda x: x['Id'])
    
    column_order = [
        'Id',
        'Pescoço Front Vetor linha',
        'Peito Front Vetor linha', 
        'Abdomen Front Vetor linha',
        'Quadril Front Vetor linha',
        'Coxa Front Vetor linha',
        'Biceps Front Vetor Coluna',
        'Pescoço Left Vetor linha',
        'Peito Left Vetor linha',
        'Abdomem Left Vetor linha',
        'Quadril Left Vetor linha',
        'Cintura Left Vetor linha',
        'Coxa Left Vetor linha'
    ]
    
    df_data = []
    for row in consolidated_data:
        df_row = {col: row.get(col, 0.0) for col in column_order}
        df_data.append(df_row)
    
    dadosRelevantes = pd.DataFrame(df_data)
    
    # Salva CSV
    output_file = current_dir / 'DadosRelevantes.csv'
    dadosRelevantes.to_csv(output_file, index=False, encoding='utf-8')
    
    return dadosRelevantes

if __name__ == "__main__":
    dadosRelevantes = process_dados_relevantes()
    if dadosRelevantes is not None:
        print(f"DataFrame criado com {len(dadosRelevantes)} registros")
    else:
        print("[ERROR] Não foi possível criar DataFrame: arquivo(s) faltando ou erro na leitura")