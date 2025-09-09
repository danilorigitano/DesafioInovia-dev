#!/usr/bin/env python3
"""
Modelo de segmentação para processamento de imagens do projeto INOVIA
Este módulo coordena o processamento de segmentação das imagens front.png e left.png
para cada ID presente nos dados estruturados.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

from segmentacao_imagens_Deeplabv3 import SegmentacaoDeepLabV3

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModeloSegmentacao:
    """
    Classe responsável por coordenar o processamento de segmentação de imagens
    para cada ID presente nos dados estruturados.
    """
    
    def __init__(self, dataframe: pd.DataFrame, 
                 confidence_threshold: float = 0.5,
                 min_area: int = 100,
                 target_size: Optional[Tuple[int, int]] = None):
        """
        Inicializa o modelo de segmentação
        
        Args:
            dataframe (pd.DataFrame): DataFrame com os dados estruturados contendo a coluna 'id'
            confidence_threshold (float): Threshold de confiança para segmentação
            min_area (int): Área mínima para filtrar ruídos
            target_size (Tuple[int, int], optional): Tamanho alvo para redimensionamento (width, height)
        """
        self.dataframe = dataframe.copy()
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.target_size = target_size
        
        # Definir caminhos base
        self.project_root = Path(__file__).parent.parent
        self.pasta_imagens = self.project_root / "INOVIA_IMAGENS"
        
        # Verificar se a pasta de imagens existe
        if not self.pasta_imagens.exists():
            raise FileNotFoundError(f"Pasta de imagens não encontrada: {self.pasta_imagens}")
        
        # Inicializar modelo de segmentação
        logger.info("Inicializando modelo de segmentação...")
        self.segmentador = SegmentacaoDeepLabV3(
            confidence_threshold=confidence_threshold,
            min_area=min_area,
            target_size=target_size
        )
        
        # Verificar estrutura do DataFrame
        self._validar_dataframe()
        
        # Resultados do processamento
        self.resultados = []
        
        logger.info(f"Modelo inicializado com {len(self.dataframe)} registros para processar")
    
    def _validar_dataframe(self):
        """
        Valida se o DataFrame contém a estrutura necessária
        """
        if self.dataframe.empty:
            raise ValueError("DataFrame está vazio")
        
        if 'id' not in self.dataframe.columns:
            raise ValueError(f"Coluna 'id' não encontrada. Colunas disponíveis: {list(self.dataframe.columns)}")
        
        logger.info(f"DataFrame validado: {len(self.dataframe)} registros com coluna 'id'")
    
    def _verificar_pasta_imagem(self, variavel: str) -> Tuple[bool, Dict[str, Path]]:
        """
        Verifica se a pasta da variável existe e contém os arquivos necessários
        
        Args:
            variavel (str): Nome da pasta (ID do registro)
            
        Returns:
            Tuple[bool, Dict[str, Path]]: (True se válida, dicionário com caminhos dos arquivos)
        """
        pasta_variavel = self.pasta_imagens / variavel
        
        if not pasta_variavel.exists():
            logger.warning(f"Pasta não encontrada: {pasta_variavel}")
            return False, {}
        
        # Verificar arquivos obrigatórios
        arquivo_front = pasta_variavel / "front.png"
        arquivo_left = pasta_variavel / "left.png"
        
        arquivos = {}
        arquivos_faltando = []
        
        if arquivo_front.exists():
            arquivos['front'] = arquivo_front
        else:
            arquivos_faltando.append('front.png')
        
        if arquivo_left.exists():
            arquivos['left'] = arquivo_left
        else:
            arquivos_faltando.append('left.png')
        
        if arquivos_faltando:
            logger.warning(f"Arquivos faltando na pasta {variavel}: {arquivos_faltando}")
            return False, arquivos
        
        logger.debug(f"Pasta {variavel} validada com sucesso")
        return True, arquivos
    
    def _processar_imagem(self, caminho_imagem: Path, tipo_imagem: str, variavel: str) -> Dict:
        """
        Processa uma única imagem usando o segmentador
        
        Args:
            caminho_imagem (Path): Caminho para a imagem
            tipo_imagem (str): Tipo da imagem ('front' ou 'left')
            variavel (str): ID da variável/pasta
            
        Returns:
            Dict: Resultado do processamento
        """
        try:
            logger.debug(f"Processando {tipo_imagem} para {variavel}: {caminho_imagem}")
            
            # Processar segmentação
            resultado = self.segmentador.processar_imagem(str(caminho_imagem))
            
            if resultado is None:
                logger.error(f"Falha na segmentação de {tipo_imagem} para {variavel}")
                return {
                    'variavel': variavel,
                    'tipo_imagem': tipo_imagem,
                    'caminho': str(caminho_imagem),
                    'sucesso': False,
                    'erro': 'Falha na segmentação',
                    'mascara': None,
                    'imagem_original': None,
                    'estatisticas': None
                }
            
            # Extrair dados do resultado
            imagem_original, mascara_binaria = resultado
            
            return {
                'variavel': variavel,
                'tipo_imagem': tipo_imagem,
                'caminho': str(caminho_imagem),
                'sucesso': True,
                'erro': None,
                'mascara': mascara_binaria,
                'imagem_original': imagem_original,
                'estatisticas': None
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar {tipo_imagem} para {variavel}: {str(e)}")
            return {
                'variavel': variavel,
                'tipo_imagem': tipo_imagem,
                'caminho': str(caminho_imagem),
                'sucesso': False,
                'erro': str(e),
                'mascara': None,
                'imagem_original': None,
                'estatisticas': None
            }
    
    def processar_variavel(self, variavel: str) -> Dict:
        """
        Processa todas as imagens de uma variável específica
        
        Args:
            variavel (str): ID da variável a ser processada
            
        Returns:
            Dict: Resultado do processamento da variável
        """
        logger.info(f"Processando variável: {variavel}")
        
        # Verificar se a pasta existe e contém os arquivos necessários
        pasta_valida, arquivos = self._verificar_pasta_imagem(variavel)
        
        if not pasta_valida:
            return {
                'variavel': variavel,
                'sucesso': False,
                'erro': 'Pasta inválida ou arquivos faltando',
                'resultados_imagens': []
            }
        
        resultados_imagens = []
        
        # Processar cada tipo de imagem
        for tipo_imagem, caminho_arquivo in arquivos.items():
            resultado_imagem = self._processar_imagem(caminho_arquivo, tipo_imagem, variavel)
            resultados_imagens.append(resultado_imagem)
        
        # Verificar se pelo menos uma imagem foi processada com sucesso
        sucessos = [r['sucesso'] for r in resultados_imagens]
        sucesso_geral = any(sucessos)
        
        resultado_variavel = {
            'variavel': variavel,
            'sucesso': sucesso_geral,
            'erro': None if sucesso_geral else 'Nenhuma imagem processada com sucesso',
            'resultados_imagens': resultados_imagens,
            'total_imagens': len(resultados_imagens),
            'imagens_sucesso': sum(sucessos),
            'imagens_falha': len(sucessos) - sum(sucessos)
        }
        
        logger.info(f"Variável {variavel} processada: {resultado_variavel['imagens_sucesso']}/{resultado_variavel['total_imagens']} imagens com sucesso")
        
        return resultado_variavel
    
    def processar_dataset(self, limite_registros: Optional[int] = None, 
                         exibir_silhuetas: bool = False) -> Dict:
        """
        Processa todo o dataset, processando cada variável (ID)
        
        Args:
            limite_registros (int, optional): Limitar o número de registros processados
            exibir_silhuetas (bool): Se deve exibir as silhuetas processadas
            
        Returns:
            Dict: Resultado geral do processamento
        """
        logger.info("Iniciando processamento do dataset")
        
        # Preparar lista de variáveis para processar
        variaveis = self.dataframe['id'].astype(str).tolist()
        
        if limite_registros is not None:
            variaveis = variaveis[:limite_registros]
            logger.info(f"Limitando processamento a {limite_registros} registros")
        
        # Processar cada variável
        self.resultados = []
        total_variaveis = len(variaveis)
        
        for i, variavel in enumerate(variaveis, 1):
            logger.info(f"Processando {i}/{total_variaveis}: {variavel}")
            
            resultado_variavel = self.processar_variavel(variavel)
            self.resultados.append(resultado_variavel)
            
            # Exibir silhuetas se solicitado
            if exibir_silhuetas and resultado_variavel['sucesso']:
                self._exibir_silhuetas(resultado_variavel)
        
        # Calcular estatísticas gerais
        variaveis_sucesso = sum(1 for r in self.resultados if r['sucesso'])
        total_imagens_processadas = sum(r['total_imagens'] for r in self.resultados)
        total_imagens_sucesso = sum(r['imagens_sucesso'] for r in self.resultados)
        
        resultado_geral = {
            'total_variaveis': total_variaveis,
            'variaveis_sucesso': variaveis_sucesso,
            'variaveis_falha': total_variaveis - variaveis_sucesso,
            'total_imagens': total_imagens_processadas,
            'imagens_sucesso': total_imagens_sucesso,
            'imagens_falha': total_imagens_processadas - total_imagens_sucesso,
            'taxa_sucesso_variaveis': (variaveis_sucesso / total_variaveis) * 100 if total_variaveis > 0 else 0,
            'taxa_sucesso_imagens': (total_imagens_sucesso / total_imagens_processadas) * 100 if total_imagens_processadas > 0 else 0,
            'resultados_detalhados': self.resultados
        }
        
        logger.info(f"Processamento concluído: {variaveis_sucesso}/{total_variaveis} variáveis processadas com sucesso")
        logger.info(f"Imagens processadas: {total_imagens_sucesso}/{total_imagens_processadas} com sucesso")
        
        return resultado_geral
    
    def _exibir_silhuetas(self, resultado_variavel: Dict):
        """
        Exibe as silhuetas processadas para uma variável
        
        Args:
            resultado_variavel (Dict): Resultado do processamento da variável
        """
        try:
            import matplotlib.pyplot as plt
            
            variavel = resultado_variavel['variavel']
            resultados_imagens = resultado_variavel['resultados_imagens']
            
            # Filtrar apenas imagens processadas com sucesso
            imagens_sucesso = [r for r in resultados_imagens if r['sucesso']]
            
            if not imagens_sucesso:
                return
            
            fig, axes = plt.subplots(len(imagens_sucesso), 2, figsize=(10, 5 * len(imagens_sucesso)))
            
            if len(imagens_sucesso) == 1:
                axes = axes.reshape(1, -1)
            
            for i, resultado_img in enumerate(imagens_sucesso):
                # Imagem original
                axes[i, 0].imshow(resultado_img['imagem_original'])
                axes[i, 0].set_title(f"{variavel} - {resultado_img['tipo_imagem']} (Original)")
                axes[i, 0].axis('off')
                
                # Máscara/Silhueta
                axes[i, 1].imshow(resultado_img['mascara'], cmap='gray')
                axes[i, 1].set_title(f"{variavel} - {resultado_img['tipo_imagem']} (Silhueta)")
                axes[i, 1].axis('off')
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            logger.warning("matplotlib não disponível para exibição de silhuetas")
        except Exception as e:
            logger.error(f"Erro ao exibir silhuetas para {variavel}: {str(e)}")
    
    def salvar_resultados(self, caminho_saida: Optional[str] = None) -> str:
        """
        Salva os resultados do processamento em arquivo
        
        Args:
            caminho_saida (str, optional): Caminho para salvar os resultados
            
        Returns:
            str: Caminho do arquivo salvo
        """
        if not self.resultados:
            logger.warning("Nenhum resultado para salvar")
            return ""
        
        if caminho_saida is None:
            caminho_saida = self.project_root / "resultados_segmentacao.json"
        
        try:
            import json
            
            # Preparar dados para serialização (remover arrays numpy)
            resultados_serializaveis = []
            
            for resultado in self.resultados:
                resultado_copy = resultado.copy()
                
                # Processar resultados de imagens
                for resultado_img in resultado_copy['resultados_imagens']:
                    # Remover dados não serializáveis
                    resultado_img.pop('mascara', None)
                    resultado_img.pop('imagem_original', None)
                
                resultados_serializaveis.append(resultado_copy)
            
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(resultados_serializaveis, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Resultados salvos em: {caminho_saida}")
            return str(caminho_saida)
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {str(e)}")
            return ""
    
    def obter_estatisticas_resumo(self) -> Dict:
        """
        Obtém estatísticas resumidas do processamento
        
        Returns:
            Dict: Estatísticas resumidas (simplificado - estatísticas de máscara removidas)
        """
        if not self.resultados:
            return {}
        
        # Coletar apenas estatísticas básicas de processamento
        total_imagens_processadas = 0
        total_imagens_sucesso = 0
        
        for resultado in self.resultados:
            if resultado['sucesso']:
                for resultado_img in resultado['resultados_imagens']:
                    total_imagens_processadas += 1
                    if resultado_img['sucesso']:
                        total_imagens_sucesso += 1
        
        return {
            'total_imagens_processadas': total_imagens_processadas,
            'total_imagens_sucesso': total_imagens_sucesso,
            'taxa_sucesso': (total_imagens_sucesso / total_imagens_processadas * 100) if total_imagens_processadas > 0 else 0
        }
