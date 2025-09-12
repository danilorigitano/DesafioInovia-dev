import csv
import re
from pathlib import Path

def extract_values_from_file(file_path):
    """Extrai os valores de vetorlinha ou vetorcoluna ignorando comentários."""
    values = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                values.append(line)
    return values

def extract_id_from_filename(filename):
    """Extrai o ID do nome do arquivo, ex: syn_f000000-0-Pre."""
    match = re.match(r'(syn_f\d{6}-\d-Pre)', filename)
    return match.group(1) if match else filename

def process_silhueta_files():
    current_dir = Path(__file__).parent
    patterns = {
        'front_vetorlinha': '*--front--vetorlinha.txt',
        'front_vetorcoluna': '*--front--vetorcoluna.txt',
        'left_vetorlinha': '*--left--vetorlinha.txt',
        'left_vetorcoluna': '*--left--vetorcoluna.txt',
    }
    output_files = {
        'front_vetorlinha': 'DadosMedidosCSV--front--vetorlinha--silhueta.csv',
        'front_vetorcoluna': 'DadosMedidosCSV--front--vetorcoluna--silhueta.csv',
        'left_vetorlinha': 'DadosMedidosCSV--left--vetorlinha--silhueta.csv',
        'left_vetorcoluna': 'DadosMedidosCSV--left--vetorcoluna--silhueta.csv',
    }

    for key in patterns:
        files = list(current_dir.glob(patterns[key]))
        print(f"Encontrados {len(files)} arquivos para {key}")
        all_data = []
        max_len = 0
        for file_path in files:
            values = extract_values_from_file(file_path)
            file_id = extract_id_from_filename(file_path.name)
            max_len = max(max_len, len(values))
            all_data.append([file_id] + values)
        # Ordena por ID
        all_data.sort(key=lambda x: x[0])
        # Cabeçalho
        header = ['Id'] + [str(i+1) for i in range(max_len)]
        # Escreve CSV
        with open(current_dir / output_files[key], 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for row in all_data:
                row_filled = row + [''] * (max_len - len(row))
                writer.writerow(row_filled)
        print(f"Arquivo gerado: {output_files[key]} com {len(all_data)} registros")

if __name__ == "__main__":
    process_silhueta_files()
