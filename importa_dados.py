#!/usr/bin/env python3
"""
Módulo de importação e validação de dados - INOVIA
Gerencia carregamento de CSV e validação de estruturas de imagens
"""

from pathlib import Path
import pandas as pd

class ImportadorDados:
    """Gerencia importação e validação de dados"""
    
    def __init__(self):
        """Inicializa caminhos dos dados"""
        self.project_root = Path(__file__).parent.parent
        self.dados_imagens = self.project_root / "INOVIA_IMAGENS"
        self.dados_csv = self.project_root / "medidas_dados_sinteticos.csv"
    
    def carregar_dados_csv(self):
        """Carrega dados do CSV"""
        try:
            df = pd.read_csv(self.dados_csv)
            print(f"✅ CSV: {len(df)} registros")
            return df
        except FileNotFoundError:
            print(f"❌ CSV não encontrado: {self.dados_csv}")
            return None
        except Exception as e:
            print(f"❌ Erro CSV: {e}")
            return None
    
    def listar_imagens_pasta(self):
        """
        Lista todas as subpastas de imagens no diretório principal
            
        Returns:
            list: Lista de subpastas encontradas
        """
        if not self.dados_imagens.exists():
            print(f"ERRO: Diretório não encontrado: {self.dados_imagens}")
            return []
        
        subpastas = [item for item in self.dados_imagens.iterdir() if item.is_dir()]
        return subpastas
    
    def obter_ids_pastas_existentes(self):
        """
        Obtém os IDs (nomes) das pastas existentes no diretório de imagens
        
        Returns:
            set: Conjunto com os nomes das pastas existentes
        """
        subpastas = self.listar_imagens_pasta()
        ids_pastas = {pasta.name for pasta in subpastas}
        ids_ordenados = sorted(ids_pastas)
        if len(ids_ordenados) > 20:
            print(f"IDs de pastas encontrados (primeiros 20 de {len(ids_ordenados)}): {ids_ordenados[:20]}")
        else:
            print(f"IDs de pastas encontrados: {ids_ordenados}")
        return ids_pastas
    
    def filtrar_dados_csv_validos(self, df=None):
        """
        Filtra os dados do CSV mantendo apenas as linhas cujos IDs possuem pastas correspondentes
        
        Args:
            df (pandas.DataFrame, optional): DataFrame a ser filtrado. Se None, carrega do CSV
            
        Returns:
            tuple: (DataFrame filtrado, lista de IDs válidos)
        """
        # Carregar dados se não fornecidos
        if df is None:
            df = self.carregar_dados_csv()
            if df is None:
                return None, []
        
        # Verificar se a coluna 'id' existe
        if 'id' not in df.columns:
            print(f"ERRO: Coluna 'id' não encontrada no CSV. Colunas disponíveis: {list(df.columns)}")
            return None, []
        
        # Obter IDs das pastas existentes
        ids_pastas_existentes = self.obter_ids_pastas_existentes()
        
        # Converter IDs do CSV para string para comparação consistente
        df_copy = df.copy()
        df_copy['id'] = df_copy['id'].astype(str)
        
        # Identificar IDs correspondentes
        ids_csv = set(df_copy['id'].unique())
        ids_correspondentes = ids_csv.intersection(ids_pastas_existentes)
        
        # Filtrar DataFrame
        df_filtrado = df_copy[df_copy['id'].isin(ids_correspondentes)].copy()
        
        # Relatório de filtragem
        print(f"\n--- RELATÓRIO DE FILTRAGEM ---")
        print(f"Total de registros no CSV: {len(df)}")
        print(f"Total de IDs únicos no CSV: {len(ids_csv)}")
        print(f"Total de pastas de imagens: {len(ids_pastas_existentes)}")
        print(f"IDs correspondentes (com pasta): {len(ids_correspondentes)}")
        print(f"Registros após filtragem: {len(df_filtrado)}")
        
        if ids_correspondentes:
            ids_correspondentes_ordenados = sorted(ids_correspondentes)
            if len(ids_correspondentes_ordenados) > 20:
                print(f"\nIDs correspondentes mantidos (primeiros 20 de {len(ids_correspondentes_ordenados)}): {ids_correspondentes_ordenados[:20]}")
            else:
                print(f"\nIDs correspondentes mantidos: {ids_correspondentes_ordenados}")
        
        return df_filtrado, list(ids_correspondentes)
    
    def obter_dados_validos(self):
        """
        Método conveniente para obter apenas os dados válidos do CSV
        
        Returns:
            pandas.DataFrame ou None: DataFrame filtrado com apenas dados válidos
        """
        dados_filtrados, _ = self.filtrar_dados_csv_validos()
        return dados_filtrados
    
    def _extrair_informacoes_id(self, id_string):
        """
        Extrai informações do ID baseado na nomenclatura: syn_[f/m]XXXXXX-X-[Pos/Pre]
        
        Args:
            id_string (str): String do ID a ser analisada
            
        Returns:
            dict: Dicionário com 'genero' ('female'/'male') e 'posicao' ('Pos'/'Pre'), ou None se inválido
        """
        try:
            # Verificar se começa com "syn_"
            if not id_string.startswith("syn_"):
                return None
            
            # Remover o prefixo "syn_"
            resto = id_string[4:]
            
            # Extrair gênero (primeira letra)
            if len(resto) < 1:
                return None
            
            letra_genero = resto[0].lower()
            if letra_genero == 'f':
                genero = 'female'
            elif letra_genero == 'm':
                genero = 'male'
            else:
                return None
            
            # Encontrar a posição (Pos ou Pre no final)
            if resto.endswith('-Pos'):
                posicao = 'Pos'
            elif resto.endswith('-Pre'):
                posicao = 'Pre'
            else:
                return None
            
            return {
                'genero': genero,
                'posicao': posicao
            }
            
        except Exception:
            return None
    
    def filtrar_dados_por_genero_posicao(self, df=None):
        """
        Filtra os dados válidos separando por gênero e posição e define como atributos da instância
        
        Args:
            df (pandas.DataFrame, optional): DataFrame a ser filtrado. Se None, usa dados válidos
        """
        # Obter dados válidos se não fornecidos
        if df is None:
            df = self.obter_dados_validos()
            if df is None:
                print("ERRO: Não foi possível obter dados válidos")
                return
        
        # Verificar se a coluna 'id' existe
        if 'id' not in df.columns:
            print(f"ERRO: Coluna 'id' não encontrada. Colunas disponíveis: {list(df.columns)}")
            return
        
        # Criar uma cópia do DataFrame para trabalhar
        df_work = df.copy()
        df_work['id'] = df_work['id'].astype(str)
        
        # Extrair informações de gênero e posição usando operações vetorizadas
        # Filtrar apenas IDs que começam com "syn_"
        mask_syn = df_work['id'].str.startswith('syn_')
        df_valid = df_work[mask_syn].copy()
        
        # Extrair gênero (letra após "syn_")
        df_valid['genero_letra'] = df_valid['id'].str[4:5].str.lower()
        df_valid['genero'] = df_valid['genero_letra'].map({'f': 'female', 'm': 'male'})
        
        # Extrair posição (final do ID)
        df_valid['posicao'] = df_valid['id'].str.extract(r'-(Pos|Pre)$')[0]
        
        # Filtrar apenas registros válidos (com gênero e posição reconhecidos)
        mask_valido = (df_valid['genero'].notna()) & (df_valid['posicao'].notna())
        df_final = df_valid[mask_valido].copy()
        
        # Separar por categoria usando query (mais eficiente que múltiplos filtros)
        self.female_pre = df_final.query("genero == 'female' and posicao == 'Pre'").drop(
            columns=['genero_letra', 'genero', 'posicao']).reset_index(drop=True)
        self.female_pos = df_final.query("genero == 'female' and posicao == 'Pos'").drop(
            columns=['genero_letra', 'genero', 'posicao']).reset_index(drop=True)
        self.male_pre = df_final.query("genero == 'male' and posicao == 'Pre'").drop(
            columns=['genero_letra', 'genero', 'posicao']).reset_index(drop=True)
        self.male_pos = df_final.query("genero == 'male' and posicao == 'Pos'").drop(
            columns=['genero_letra', 'genero', 'posicao']).reset_index(drop=True)
        
        # Calcular contadores para relatório
        total_processados = len(df)
        total_syn = len(df_valid)
        total_validos = len(df_final)
        invalidos = total_processados - total_validos
        
        # Imprimir relatório
        print(f"\n--- RELATÓRIO DE FILTRAGEM POR GÊNERO E POSIÇÃO ---")
        print(f"Total de registros processados: {total_processados}")
        print(f"Female Pre: {len(self.female_pre)} registros")
        print(f"Female Pos: {len(self.female_pos)} registros") 
        print(f"Male Pre: {len(self.male_pre)} registros")
        print(f"Male Pos: {len(self.male_pos)} registros")
        print(f"IDs inválidos/não reconhecidos: {invalidos} registros")
    
    @property
    # Uso de decorador para permitir usar importador.lista_possibilidades[i] ao inves de importador.lista_possibilidades()[i]
    def lista_possibilidades(self):
        """
        Lista com os 4 DataFrames: [female_pre, female_pos, male_pre, male_pos]
        """
        if all(hasattr(self, attr) for attr in ['female_pre', 'female_pos', 'male_pre', 'male_pos']):
            return [self.female_pre, self.female_pos, self.male_pre, self.male_pos]
        return []
    
    def obter_estatisticas_dados(self):
        """
        Obtém estatísticas gerais dos dados disponíveis, incluindo dados filtrados por categoria
        
        Returns:
            dict: Dicionário com estatísticas dos dados
        """
        # Contar subpastas de imagens
        subpastas = self.listar_imagens_pasta()
        
        # Contar registros CSV
        df = self.carregar_dados_csv()
        csv_registros = len(df) if df is not None else 0
        
        # Verificar completude dos dados
        dados_completos = self.dados_imagens.exists() and self.dados_csv.exists()
        
        # Obter dados filtrados se possível
        dados_filtrados = None
        ids_correspondentes = []
        dados_por_categoria = None
        
        if df is not None and dados_completos:
            try:
                dados_filtrados, ids_correspondentes = self.filtrar_dados_csv_validos(df)
                if dados_filtrados is not None:
                    self.filtrar_dados_por_genero_posicao(dados_filtrados)
                    dados_por_categoria = {
                        'female_pre': self.female_pre if hasattr(self, 'female_pre') else pd.DataFrame(),
                        'female_pos': self.female_pos if hasattr(self, 'female_pos') else pd.DataFrame(),
                        'male_pre': self.male_pre if hasattr(self, 'male_pre') else pd.DataFrame(),
                        'male_pos': self.male_pos if hasattr(self, 'male_pos') else pd.DataFrame()
                    }
            except Exception as e:
                print(f"AVISO: Erro ao filtrar dados: {e}")
        
        # Estatísticas por categoria
        stats_categoria = {}
        if dados_por_categoria:
            for nome, dataset in dados_por_categoria.items():
                stats_categoria[nome] = len(dataset)
        
        return {
            'total_subpastas': len(subpastas),
            'csv_registros': csv_registros,
            'csv_registros_correspondentes': len(dados_filtrados) if dados_filtrados is not None else 0,
            'ids_correspondentes': len(ids_correspondentes),
            'dados_completos': dados_completos,
            'subpastas': subpastas,
            'dados_filtrados': dados_filtrados,
            'dados_por_categoria': dados_por_categoria,
            'stats_categoria': stats_categoria
        }
    
    def imprimir_relatorio(self):
        """
        Imprime um relatório completo dos dados disponíveis
        """
        print("\n" + "="*50)
        print("RELATÓRIO DE DADOS - PROJETO INOVIA")
        print("="*50)
        
        print(f"Verificando dados em: {self.project_root}")
        
        # Obter estatísticas (já inclui todas as verificações)
        stats = self.obter_estatisticas_dados()
        
        # Verificar existência e reportar
        if self.dados_imagens.exists():
            print(f"OK: Encontrado: {self.dados_imagens}")
        else:
            print(f"AVISO: Diretório não encontrado: {self.dados_imagens}")
            
        if self.dados_csv.exists():
            print(f"OK: Encontrado: {self.dados_csv}")
        else:
            print(f"AVISO: Arquivo não encontrado: {self.dados_csv}")
        
        print(f"\nESTATÍSTICAS:")
        print(f"   • Total de subpastas: {stats['total_subpastas']}")
        print(f"   • Registros CSV totais: {stats['csv_registros']}")
        print(f"   • Registros CSV correspondentes: {stats['csv_registros_correspondentes']}")
        print(f"   • IDs correspondentes (com pasta): {stats['ids_correspondentes']}")
        
        # Mostrar estatísticas por categoria se disponíveis
        if stats.get('stats_categoria'):
            print(f"\nESTATÍSTICAS POR CATEGORIA:")
            for categoria, quantidade in stats['stats_categoria'].items():
                print(f"   • {categoria}: {quantidade} registros")
        
        print(f"\nESTRUTURA DE IMAGENS:")
        if stats['subpastas']:
            nomes_subpastas = [p.name for p in stats['subpastas']]
            if len(nomes_subpastas) > 5:
                print(f"   • Subpastas encontradas (primeiras 5 de {len(nomes_subpastas)}): {nomes_subpastas[:5]}")
            else:
                print(f"   • Subpastas encontradas: {nomes_subpastas}")
        else:
            print(f"   • Nenhuma subpasta encontrada")
        
        print(f"\nCAMINHOS:")
        print(f"   • Projeto: {self.project_root}")
        print(f"   • Imagens: {self.dados_imagens}")
        print(f"   • CSV: {self.dados_csv}")
        
        print("\n" + "="*50)
        
        if stats['dados_completos']:
            print("OK: Projeto configurado e pronto para desenvolvimento!")
        else:
            print("AVISO: Alguns dados estão faltando. Verifique os caminhos.")
        
        return stats['dados_completos']

if __name__ == "__main__":
    importador = ImportadorDados()
    importador.imprimir_relatorio()
