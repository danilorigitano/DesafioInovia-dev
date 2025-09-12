#!/usr/bin/env python3
"""
Exportador de Dados de Parametrização - v1.1.0
==============================================

RESPONSABILIDADE: Exportar dados analisados pelo programa de parametrização para arquivos TXT
na pasta dados_analisados.

NOVIDADE v1.1.0: EXPORTAÇÃO IMEDIATA
====================================
✅ Os dados são exportados IMEDIATAMENTE após cada ID ser processado
✅ Não espera o final de todo o processamento
✅ Evita perda de dados se o programa for interrompido
✅ Melhor performance de memória

FUNCIONALIDADES:
===============
✅ Exporta vetores coluna e linha por tipo de foto (front/left)
✅ Exporta dados de bounding boxes calculados
✅ Gera arquivos TXT organizados por ID e tipo
✅ Processa dados de segmentação parametrizada
✅ Integração automática com fluxo principal
✓ Exporta vetores coluna e linha por tipo de foto (front/left)
✓ Exporta dados de bounding boxes calculados
✓ Gera arquivos TXT organizados por ID e tipo
✓ Processa dados de segmentação parametrizada

FORMATO DOS ARQUIVOS:
====================
- {id}--front--vetorcoluna.txt
- {id}--front--vetorlinha.txt  
- {id}--left--vetorcoluna.txt
- {id}--left--vetorlinha.txt
- {id}--boundingbox.txt

EXEMPLO DE USO:
==============
```python
# 1. Execução Standalone (após rodar o programa principal)
python exportacao_parametrizacao.py

# 2. Integração com código Python
from exportacao_parametrizacao import ExportadorParametrizacao

# Após executar o programa principal
exportador = ExportadorParametrizacao()
resultado = exportador.exportar_resultados_processados()

# 3. Especificar pasta personalizada
exportador = ExportadorParametrizacao("caminho/para/dados_analisados")
exportador.exportar_resultados_processados()
```

FLUXO DE TRABALHO:
=================
1. Execute main.py para processar imagens com parametrização
2. Execute exportacao_parametrizacao.py para gerar arquivos TXT
3. Os arquivos TXT estarão em dados_analisados/

INTEGRAÇÃO AUTOMÁTICA:
=====================
Este módulo pode ser chamado automaticamente após o processamento
adicionando no final do main.py:

```python
from exportacao_parametrizacao import ExportadorParametrizacao
exportador = ExportadorParametrizacao()
exportador.exportar_resultados_processados()
```
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExportadorParametrizacao:
    """
    Classe responsável por exportar os dados analisados da parametrização
    para arquivos TXT na pasta dados_analisados.
    """
    
    def __init__(self, pasta_dados_analisados: Optional[str] = None):
        """
        Inicializa o exportador.
        
        Args:
            pasta_dados_analisados (str, optional): Caminho para pasta de dados analisados
        """
        # Determinar pasta de dados analisados
        if pasta_dados_analisados is None:
            self.pasta_dados = Path(__file__).parent / "dados_analisados"
        else:
            self.pasta_dados = Path(pasta_dados_analisados)
        
        # Criar pasta se não existir
        self.pasta_dados.mkdir(exist_ok=True)
        
        # Pasta de trabalho (onde ficam os arquivos JSON de resultados)
        self.pasta_trabalho = Path(__file__).parent
        
        print(f"🗂️ Exportador inicializado")
        print(f"📁 Pasta de dados analisados: {self.pasta_dados}")
    
    
    def encontrar_arquivos_resultados(self) -> List[Path]:
        """
        Encontra arquivos JSON de resultados de parametrização na pasta de trabalho e pasta pai.
        
        Returns:
            List[Path]: Lista de arquivos de resultados encontrados
        """
        arquivos_json = []
        
        # Buscar na pasta atual
        arquivos_atual = list(self.pasta_trabalho.glob("resultados_parametrizacao_*.json"))
        arquivos_json.extend(arquivos_atual)
        
        # Buscar na pasta pai (onde o modelo salva por padrão)
        pasta_pai = self.pasta_trabalho.parent
        arquivos_pai = list(pasta_pai.glob("resultados_parametrizacao_*.json"))
        arquivos_json.extend(arquivos_pai)
        
        if not arquivos_json:
            print("⚠️ Nenhum arquivo de resultados de parametrização encontrado")
            print("💡 Execute primeiro o programa principal para gerar dados")
            print(f"🔍 Procurou em:")
            print(f"   - {self.pasta_trabalho}")
            print(f"   - {pasta_pai}")
        else:
            print(f"📋 Encontrados {len(arquivos_json)} arquivo(s) de resultados")
            for arquivo in arquivos_json:
                print(f"   - {arquivo.name}")
        
        return arquivos_json
    
    
    def carregar_dados_processados(self, arquivo_json: Path) -> Dict:
        """
        Carrega dados processados de um arquivo JSON.
        
        Args:
            arquivo_json (Path): Caminho para arquivo JSON
            
        Returns:
            Dict: Dados carregados do arquivo
        """
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            print(f"✅ Carregado: {arquivo_json.name}")
            return dados
            
        except Exception as e:
            print(f"❌ Erro ao carregar {arquivo_json.name}: {e}")
            return {}
    
    
    def extrair_id_limpo(self, variavel_id: str) -> str:
        """
        Extrai o ID limpo da variável (exemplo: syn_f000002-3-Pre).
        
        Args:
            variavel_id (str): ID da variável
            
        Returns:
            str: ID limpo para usar nos nomes dos arquivos
        """
        # Retorna o ID como está, assumindo que já está no formato correto
        return str(variavel_id).strip()
    
    
    def exportar_vetores_parametrizacao(self, resultado_variavel: Dict, mostrar_log: bool = True) -> bool:
        """
        Exporta os vetores de parametrização (linha e coluna) para arquivos TXT.
        
        Args:
            resultado_variavel (Dict): Dados de resultado de uma variável
            mostrar_log (bool): Se deve mostrar logs detalhados
            
        Returns:
            bool: True se exportou com sucesso
        """
        variavel_id = resultado_variavel.get('variavel', '')
        id_limpo = self.extrair_id_limpo(variavel_id)
        
        if not id_limpo:
            if mostrar_log:
                print(f"⚠️ ID inválido para variável: {variavel_id}")
            return False
        
        sucesso_total = True
        
        # Processar cada resultado de imagem
        for resultado_imagem in resultado_variavel.get('resultados_imagens', []):
            tipo_imagem = resultado_imagem.get('tipo_imagem', '')  # 'front' ou 'left'
            
            if tipo_imagem not in ['front', 'left']:
                continue
            
            resultado_seg = resultado_imagem.get('resultado_segmentacao', {})
            if not resultado_seg or not resultado_seg.get('sucesso', False):
                continue
            
            # Extrair vetores de pixels claros (linhas e colunas)
            vetor_linhas = resultado_seg.get('vetor_pixels_claros', [])
            vetor_colunas = resultado_seg.get('vetor_pixels_claros_colunas', [])
            
            # Verificar se vetor_linhas existe e não está vazio (tratando arrays numpy)
            if vetor_linhas is not None and len(vetor_linhas) > 0:
                nome_arquivo_linhas = f"{id_limpo}--{tipo_imagem}--vetorlinha.txt"
                sucesso_linhas = self._salvar_vetor_txt(vetor_linhas, nome_arquivo_linhas, mostrar_log)
                sucesso_total = sucesso_total and sucesso_linhas
            
            # Verificar se vetor_colunas existe e não está vazio (tratando arrays numpy)
            if vetor_colunas is not None and len(vetor_colunas) > 0:
                nome_arquivo_colunas = f"{id_limpo}--{tipo_imagem}--vetorcoluna.txt"
                sucesso_colunas = self._salvar_vetor_txt(vetor_colunas, nome_arquivo_colunas, mostrar_log)
                sucesso_total = sucesso_total and sucesso_colunas
        
        return sucesso_total
    
    
    def exportar_bounding_box(self, resultado_variavel: Dict, mostrar_log: bool = True) -> bool:
        """
        Exporta dados de bounding box para arquivos TXT separados por tipo de foto.
        NOVO FORMATO: {id}--{tipodefoto}--boundingbox.txt
        
        Args:
            resultado_variavel (Dict): Dados de resultado de uma variável
            mostrar_log (bool): Se deve mostrar logs detalhados
            
        Returns:
            bool: True se exportou com sucesso
        """
        variavel_id = resultado_variavel.get('variavel', '')
        id_limpo = self.extrair_id_limpo(variavel_id)
        
        if not id_limpo:
            if mostrar_log:
                print(f"⚠️ ID inválido para variável: {variavel_id}")
            return False
        
        # ✨ NOVA ABORDAGEM: Exportar separadamente por tipo de foto (front/left)
        sucessos = []
        
        for resultado_imagem in resultado_variavel.get('resultados_imagens', []):
            if not resultado_imagem.get('sucesso', False):
                continue
            
            tipo_imagem = resultado_imagem.get('tipo_imagem', '')
            bounding_box_dados = resultado_imagem.get('bounding_box_dados', {})
            
            if not bounding_box_dados.get('sucesso', False):
                if mostrar_log:
                    print(f"⚠️ Bounding box sem sucesso para {id_limpo} - {tipo_imagem}")
                continue
            
            # Extrair bounding boxes
            bboxes = bounding_box_dados.get('bounding_boxes', [])
            
            if not bboxes:
                if mostrar_log:
                    print(f"⚠️ Nenhuma bounding box encontrada para {id_limpo} - {tipo_imagem}")
                continue
            
            # Criar nome do arquivo no novo formato: id--tipodefoto--boundingbox.txt
            nome_arquivo_bbox = f"{id_limpo}--{tipo_imagem}--boundingbox.txt"
            
            # Salvar arquivo específico
            sucesso = self._salvar_bounding_boxes_txt(bboxes, nome_arquivo_bbox, mostrar_log)
            sucessos.append(sucesso)
            
            if mostrar_log and sucesso:
                print(f"✅ Bounding box exportado: {nome_arquivo_bbox} ({len(bboxes)} caixas)")
        
        # Retornar True se pelo menos uma exportação foi bem-sucedida
        return any(sucessos)
    
    
    def _salvar_vetor_txt(self, vetor_dados: List, nome_arquivo: str, mostrar_log: bool = True) -> bool:
        """
        Salva um vetor de dados em arquivo TXT.
        
        Args:
            vetor_dados (List): Dados do vetor
            nome_arquivo (str): Nome do arquivo
            mostrar_log (bool): Se deve mostrar logs detalhados
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            caminho_arquivo = self.pasta_dados / nome_arquivo
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write(f"# Vetor de dados - {nome_arquivo}\n")
                f.write(f"# Total de elementos: {len(vetor_dados)}\n")
                f.write(f"# Formato: um valor por linha\n")
                f.write("#" + "="*50 + "\n\n")
                
                # Dados do vetor
                for i, valor in enumerate(vetor_dados):
                    f.write(f"{valor}\n")
            
            if mostrar_log:
                print(f"✅ Exportado: {nome_arquivo} ({len(vetor_dados)} elementos)")
            return True
            
        except Exception as e:
            if mostrar_log:
                print(f"❌ Erro ao salvar {nome_arquivo}: {e}")
            return False
    
    
    def _salvar_bounding_boxes_txt(self, bboxes: List, nome_arquivo: str, mostrar_log: bool = True) -> bool:
        """
        Salva dados de bounding boxes em arquivo TXT com as coordenadas dos 4 cantos.
        
        Args:
            bboxes (List): Lista de bounding boxes
            nome_arquivo (str): Nome do arquivo
            mostrar_log (bool): Se deve mostrar logs detalhados
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            caminho_arquivo = self.pasta_dados / nome_arquivo
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write(f"# Bounding Boxes - {nome_arquivo}\n")
                f.write(f"# Total de bounding boxes: {len(bboxes)}\n")
                f.write(f"# Formato: x\ty (coordenadas dos 4 cantos do retângulo)\n")
                f.write(f"# Para cada bbox: canto_superior_esquerdo, superior_direito, inferior_direito, inferior_esquerdo\n")
                f.write("#" + "="*70 + "\n\n")
                
                # Dados das bounding boxes - converter para coordenadas dos 4 cantos
                for i, bbox in enumerate(bboxes):
                    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                        x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
                        
                        # Calcular as 4 coordenadas dos cantos do retângulo
                        # Canto superior esquerdo
                        x1, y1 = x, y
                        # Canto superior direito  
                        x2, y2 = x + w, y
                        # Canto inferior direito
                        x3, y3 = x + w, y + h
                        # Canto inferior esquerdo
                        x4, y4 = x, y + h
                        
                        # Escrever as 4 coordenadas dos cantos (formato x \t y)
                        f.write(f"# Bounding Box {i+1}\n")
                        f.write(f"{x1}\t{y1}\n")  # Superior esquerdo
                        f.write(f"{x2}\t{y2}\n")  # Superior direito
                        f.write(f"{x3}\t{y3}\n")  # Inferior direito
                        f.write(f"{x4}\t{y4}\n")  # Inferior esquerdo
                        f.write("\n")  # Linha em branco entre bounding boxes
                    else:
                        if mostrar_log:
                            print(f"⚠️ Bounding box inválida ignorada: {bbox}")
            
            if mostrar_log:
                print(f"✅ Exportado: {nome_arquivo} ({len(bboxes)} bounding boxes)")
            return True
            
        except Exception as e:
            if mostrar_log:
                print(f"❌ Erro ao salvar {nome_arquivo}: {e}")
            return False
    
    
    def exportar_variavel_completa(self, resultado_variavel: Dict, mostrar_log: bool = True) -> bool:
        """
        Exporta todos os dados de uma variável (vetores + bounding box).
        
        Args:
            resultado_variavel (Dict): Dados de resultado de uma variável
            mostrar_log (bool): Se deve mostrar logs detalhados
            
        Returns:
            bool: True se exportou com sucesso
        """
        variavel_id = resultado_variavel.get('variavel', '')
        
        if mostrar_log:
            print(f"\n📦 Exportando dados da variável: {variavel_id}")
        
        # Verificar se a variável foi processada com sucesso
        if not resultado_variavel.get('sucesso', False):
            if mostrar_log:
                print(f"⚠️ Variável {variavel_id} não foi processada com sucesso - pulando exportação")
            return False
        
        # Exportar vetores de parametrização
        sucesso_vetores = self.exportar_vetores_parametrizacao(resultado_variavel, mostrar_log)
        
        # Exportar bounding boxes
        sucesso_bbox = self.exportar_bounding_box(resultado_variavel, mostrar_log)
        
        sucesso_total = sucesso_vetores or sucesso_bbox  # Pelo menos um deve ter sucesso
        
        if mostrar_log:
            if sucesso_total:
                print(f"✅ Variável {variavel_id} exportada com sucesso")
            else:
                print(f"❌ Falha ao exportar variável {variavel_id}")
        
        return sucesso_total
    
    
    def exportar_resultados_processados(self) -> Dict:
        """
        Exporta todos os resultados processados encontrados.
        
        Returns:
            Dict: Estatísticas da exportação
        """
        print("\n" + "="*60)
        print("🚀 INICIANDO EXPORTAÇÃO DE DADOS PARAMETRIZADOS")
        print("="*60)
        
        # Encontrar arquivos de resultados
        arquivos_resultados = self.encontrar_arquivos_resultados()
        
        if not arquivos_resultados:
            return {
                'sucesso': False,
                'erro': 'Nenhum arquivo de resultados encontrado',
                'variaveis_processadas': 0,
                'variaveis_exportadas': 0
            }
        
        # Estatísticas
        total_variaveis = 0
        variaveis_exportadas = 0
        arquivos_gerados = 0
        
        # Processar cada arquivo de resultados
        for arquivo_json in arquivos_resultados:
            print(f"\n📄 Processando: {arquivo_json.name}")
            
            dados = self.carregar_dados_processados(arquivo_json)
            if not dados:
                continue
            
            # Processar cada variável nos resultados
            resultados = dados.get('resultados', [])
            total_variaveis += len(resultados)
            
            for resultado_variavel in resultados:
                if self.exportar_variavel_completa(resultado_variavel, mostrar_log=True):
                    variaveis_exportadas += 1
        
        # Contar arquivos gerados
        arquivos_txt = list(self.pasta_dados.glob("*.txt"))
        arquivos_gerados = len(arquivos_txt)
        
        # Estatísticas finais
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DA EXPORTAÇÃO")
        print("="*60)
        print(f"📁 Arquivos JSON processados: {len(arquivos_resultados)}")
        print(f"🔢 Variáveis encontradas: {total_variaveis}")
        print(f"✅ Variáveis exportadas: {variaveis_exportadas}")
        print(f"📄 Arquivos TXT gerados: {arquivos_gerados}")
        print(f"📂 Pasta de destino: {self.pasta_dados}")
        
        if arquivos_txt:
            print(f"\n📋 Arquivos gerados:")
            for arquivo in sorted(arquivos_txt):
                tamanho = arquivo.stat().st_size
                print(f"   - {arquivo.name} ({tamanho} bytes)")
        
        return {
            'sucesso': variaveis_exportadas > 0,
            'arquivos_json_processados': len(arquivos_resultados),
            'variaveis_processadas': total_variaveis,
            'variaveis_exportadas': variaveis_exportadas,
            'arquivos_gerados': arquivos_gerados,
            'pasta_destino': str(self.pasta_dados)
        }


def main():
    """
    Função principal para execução standalone do exportador.
    """
    print("🚀 Exportador de Dados de Parametrização")
    print("="*50)
    
    try:
        exportador = ExportadorParametrizacao()
        resultado = exportador.exportar_resultados_processados()
        
        if resultado['sucesso']:
            print(f"\n🎉 Exportação concluída com sucesso!")
            print(f"📊 {resultado['variaveis_exportadas']}/{resultado['variaveis_processadas']} variáveis exportadas")
        else:
            print(f"\n❌ Exportação falhou: {resultado.get('erro', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"\n❌ Erro durante exportação: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
