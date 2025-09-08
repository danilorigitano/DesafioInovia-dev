#!/usr/bin/env python3
"""
Módulo para importação e verificação de dados do projeto INOVIA
Este módulo gerencia a localização e verificação dos dados necessários
"""

from pathlib import Path
import pandas as pd
import os

class ImportadorDados:
    """
    Classe responsável por importar e verificar a existência dos dados do projeto
    """
    
    def __init__(self):
        """
        Inicializa o importador com os caminhos dos dados
        """
        self.project_root = Path(__file__).parent.parent
        self.dados_female = self.project_root / "INOVIA_IMAGENS_female"
        self.dados_male = self.project_root / "INOVIA_IMAGENS_male"
        self.dados_csv = self.project_root / "medidas_dados_sinteticos.csv"
    
    def verificar_dados(self):
        """
        Verifica se todos os diretórios e arquivos de dados existem
        
        Returns:
            dict: Dicionário com o status de cada fonte de dados
        """
        print(f"Verificando dados em: {self.project_root}")
        
        status = {
            'female_dir': self.dados_female.exists(),
            'male_dir': self.dados_male.exists(),
            'csv_file': self.dados_csv.exists(),
            'todos_encontrados': True
        }
        
        # Verificar diretório feminino
        if not status['female_dir']:
            print(f"⚠️  Diretório não encontrado: {self.dados_female}")
            status['todos_encontrados'] = False
        else:
            print(f"✅ Encontrado: {self.dados_female}")
        
        # Verificar diretório masculino
        if not status['male_dir']:
            print(f"⚠️  Diretório não encontrado: {self.dados_male}")
            status['todos_encontrados'] = False
        else:
            print(f"✅ Encontrado: {self.dados_male}")
        
        # Verificar arquivo CSV
        if not status['csv_file']:
            print(f"⚠️  Arquivo não encontrado: {self.dados_csv}")
            status['todos_encontrados'] = False
        else:
            print(f"✅ Encontrado: {self.dados_csv}")
        
        return status
    
    def carregar_dados_csv(self):
        """
        Carrega os dados do arquivo CSV
        
        Returns:
            pandas.DataFrame ou None: DataFrame com os dados ou None se erro
        """
        if not self.dados_csv.exists():
            print(f"❌ Erro: Arquivo CSV não encontrado: {self.dados_csv}")
            return None
        
        try:
            df = pd.read_csv(self.dados_csv)
            print(f"✅ CSV carregado com sucesso: {len(df)} registros")
            return df
        except Exception as e:
            print(f"❌ Erro ao carregar CSV: {e}")
            return None
    
    def listar_imagens_pasta(self, pasta_path):
        """
        Lista todas as subpastas de imagens em um diretório
        
        Args:
            pasta_path (Path): Caminho para o diretório
            
        Returns:
            list: Lista de subpastas encontradas
        """
        if not pasta_path.exists():
            print(f"❌ Diretório não encontrado: {pasta_path}")
            return []
        
        subpastas = [item for item in pasta_path.iterdir() if item.is_dir()]
        print(f"📁 Encontradas {len(subpastas)} subpastas em {pasta_path.name}")
        return subpastas
    
    def obter_estatisticas_dados(self):
        """
        Obtém estatísticas gerais dos dados disponíveis
        
        Returns:
            dict: Dicionário com estatísticas dos dados
        """
        stats = {
            'total_pastas_female': 0,
            'total_pastas_male': 0,
            'csv_registros': 0,
            'dados_completos': False
        }
        
        # Contar pastas femininas
        if self.dados_female.exists():
            pastas_female = self.listar_imagens_pasta(self.dados_female)
            stats['total_pastas_female'] = len(pastas_female)
        
        # Contar pastas masculinas
        if self.dados_male.exists():
            pastas_male = self.listar_imagens_pasta(self.dados_male)
            stats['total_pastas_male'] = len(pastas_male)
        
        # Contar registros CSV
        df = self.carregar_dados_csv()
        if df is not None:
            stats['csv_registros'] = len(df)
        
        # Verificar se todos os dados estão completos
        status = self.verificar_dados()
        stats['dados_completos'] = status['todos_encontrados']
        
        return stats
    
    def imprimir_relatorio(self):
        """
        Imprime um relatório completo dos dados disponíveis
        """
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE DADOS - PROJETO INOVIA")
        print("="*50)
        
        # Verificar existência dos dados
        status = self.verificar_dados()
        
        # Obter estatísticas
        stats = self.obter_estatisticas_dados()
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   • Pastas femininas: {stats['total_pastas_female']}")
        print(f"   • Pastas masculinas: {stats['total_pastas_male']}")
        print(f"   • Registros CSV: {stats['csv_registros']}")
        print(f"   • Dados completos: {'✅ Sim' if stats['dados_completos'] else '❌ Não'}")
        
        print(f"\n📍 CAMINHOS:")
        print(f"   • Projeto: {self.project_root}")
        print(f"   • Feminino: {self.dados_female}")
        print(f"   • Masculino: {self.dados_male}")
        print(f"   • CSV: {self.dados_csv}")
        
        print("\n" + "="*50)
        
        if stats['dados_completos']:
            print("✅ Projeto configurado e pronto para desenvolvimento!")
        else:
            print("⚠️  Alguns dados estão faltando. Verifique os caminhos.")
        
        return status

def verificar_e_configurar_dados():
    """
    Função de conveniência para verificar e configurar os dados
    
    Returns:
        ImportadorDados: Instância do importador configurada
    """
    importador = ImportadorDados()
    importador.imprimir_relatorio()
    return importador

if __name__ == "__main__":
    # Teste do módulo
    verificar_e_configurar_dados()
