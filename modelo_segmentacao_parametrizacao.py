#!/usr/bin/env python3
"""
Modelo de segmentação especializado em Parametrização com Funções Indicadoras
Este módulo coordena o processamento de segmentação das imagens front.png e left.png
usando exclusivamente o método de Parametrização com Funções Indicadoras.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
import time

from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModeloSegmentacaoParametrizacao:
    """
    Classe responsável por coordenar o processamento de segmentação de imagens
    usando exclusivamente o método de Parametrização com Funções Indicadoras.
    
    Características:
    - Método otimizado para velocidade e eficiência
    - 382 funções indicadoras (uma por linha)
    - Redimensionamento para 512x382 pixels
    - Pós-processamento morfológico avançado
    - Métricas de qualidade (MSE e RMS)
    """
    
    def __init__(self, dataframe: pd.DataFrame,
                 target_width: int = 512,
                 target_height: int = 382,
                 morph_kernel_size: int = 5,
                 min_area: int = 10,
                 enhance_contrast: bool = True,
                 num_workers: int = 1,
                 metodo_segmentacao: str = "linhas"):
        """
        Inicializa o modelo de segmentação por parametrização
        
        Args:
            dataframe (pd.DataFrame): DataFrame com os dados estruturados contendo a coluna 'id'
            target_width (int): Largura alvo para redimensionamento (padrão: 512)
            target_height (int): Altura alvo para redimensionamento (padrão: 382)
            morph_kernel_size (int): Tamanho do kernel para operações morfológicas
            min_area (int): Área mínima para filtrar ruídos (pixels)
            enhance_contrast (bool): Se deve aplicar melhoria de contraste
            num_workers (int): Número de workers para processamento paralelo (futuro)
            metodo_segmentacao (str): Método de segmentação ('linhas', 'colunas', 'combinado')
        """
        self.dataframe = dataframe.copy()
        self.target_width = target_width
        self.target_height = target_height
        self.morph_kernel_size = morph_kernel_size
        self.min_area = min_area
        self.enhance_contrast = enhance_contrast
        self.num_workers = num_workers
        self.metodo_segmentacao = metodo_segmentacao
        
        # Definir caminhos base
        self.project_root = Path(__file__).parent.parent
        self.pasta_imagens = self.project_root / "INOVIA_IMAGENS"
        
        # Verificar se a pasta de imagens existe
        if not self.pasta_imagens.exists():
            raise FileNotFoundError(f"Pasta de imagens não encontrada: {self.pasta_imagens}")
        
        # Inicializar segmentador de parametrização
        self._inicializar_segmentador()
        
        # Verificar estrutura do DataFrame
        self._validar_dataframe()
        
        # Resultados do processamento
        self.resultados = []
        self.estatisticas_globais = {}
        
        logger.info(f"Modelo de Parametrização inicializado:")
        logger.info(f"  • {len(self.dataframe)} registros para processar")
        logger.info(f"  • Dimensões alvo: {self.target_width}x{self.target_height}")
        logger.info(f"  • Método: {self.metodo_segmentacao.upper()}")
        if self.metodo_segmentacao == "linhas":
            logger.info(f"  • {self.target_height} funções indicadoras horizontais")
        elif self.metodo_segmentacao == "colunas":
            logger.info(f"  • {self.target_width} funções indicadoras verticais")
        else:  # combinado
            logger.info(f"  • {self.target_height} funções horizontais + {self.target_width} verticais")
        logger.info(f"  • Kernel morfológico: {self.morph_kernel_size}x{self.morph_kernel_size}")
        logger.info(f"  • Contraste aprimorado: {'✓' if self.enhance_contrast else '✗'}")
    
    def _inicializar_segmentador(self):
        """
        Inicializa o segmentador de parametrização com configurações otimizadas
        """
        logger.info("Inicializando segmentador de Parametrização com Funções Indicadoras...")
        
        try:
            self.segmentador = SegmentacaoParametrizacaoIndicadora(
                target_width=self.target_width,
                target_height=self.target_height,
                morph_kernel_size=self.morph_kernel_size,
                min_area=self.min_area,
                enhance_contrast=self.enhance_contrast
            )
            logger.info("✓ Segmentador inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"✗ Erro ao inicializar segmentador: {e}")
            raise RuntimeError(f"Falha na inicialização do segmentador: {e}")
    
    def _validar_dataframe(self):
        """
        Valida se o DataFrame contém a estrutura necessária
        """
        if self.dataframe.empty:
            raise ValueError("DataFrame está vazio")
        
        if 'id' not in self.dataframe.columns:
            raise ValueError(f"Coluna 'id' não encontrada. Colunas disponíveis: {list(self.dataframe.columns)}")
        
        logger.info(f"✓ DataFrame validado: {len(self.dataframe)} registros com coluna 'id'")
    
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
        
        logger.debug(f"✓ Pasta {variavel} validada")
        return True, arquivos
    
    def _processar_imagem(self, caminho_imagem: Path, tipo_imagem: str, variavel: str) -> Dict:
        """
        Processa uma única imagem usando parametrização com funções indicadoras
        
        Args:
            caminho_imagem (Path): Caminho para a imagem
            tipo_imagem (str): Tipo da imagem ('front' ou 'left')
            variavel (str): ID da variável/pasta
            
        Returns:
            Dict: Resultado do processamento
        """
        inicio_tempo = time.time()
        
        try:
            logger.debug(f"Processando {tipo_imagem} para {variavel}: {caminho_imagem}")
            
            # Processar com Parametrização Indicadora baseado no método escolhido
            if self.metodo_segmentacao == "linhas":
                resultado_segmentacao = self.segmentador.segmentar(str(caminho_imagem))
            elif self.metodo_segmentacao == "colunas":
                resultado_segmentacao = self.segmentador.segmentar_por_colunas(str(caminho_imagem))
            elif self.metodo_segmentacao == "combinado":
                resultado_segmentacao = self.segmentador.segmentar_separado_e_unido(str(caminho_imagem))
            else:
                raise ValueError(f"Método de segmentação inválido: {self.metodo_segmentacao}")
            
            tempo_processamento = time.time() - inicio_tempo
            
            if resultado_segmentacao.get('sucesso', False):
                # Extrair métricas de qualidade
                mse_global = resultado_segmentacao.get('mse_global', 0)
                rms_global = np.sqrt(mse_global) if mse_global > 0 else 0
                
                # Calcular estatísticas da máscara
                mascara_binaria = resultado_segmentacao.get('mascara_binaria')
                estatisticas_mascara = self._calcular_estatisticas_mascara(mascara_binaria) if mascara_binaria is not None else {}
                
                return {
                    'variavel': variavel,
                    'tipo_imagem': tipo_imagem,
                    'caminho': str(caminho_imagem),
                    'sucesso': True,
                    'tempo_processamento': tempo_processamento,
                    'resultado_segmentacao': resultado_segmentacao,
                    'metricas_qualidade': {
                        'mse_global': mse_global,
                        'rms_global': rms_global,
                        'num_funcoes_indicadoras': self.target_height
                    },
                    'estatisticas_mascara': estatisticas_mascara,
                    'erro': None
                }
            else:
                erro_msg = resultado_segmentacao.get('erro', 'Falha na segmentação por parametrização')
                logger.error(f"Falha na segmentação de {tipo_imagem} para {variavel}: {erro_msg}")
                
                return {
                    'variavel': variavel,
                    'tipo_imagem': tipo_imagem,
                    'caminho': str(caminho_imagem),
                    'sucesso': False,
                    'tempo_processamento': tempo_processamento,
                    'resultado_segmentacao': None,
                    'metricas_qualidade': {},
                    'estatisticas_mascara': {},
                    'erro': erro_msg
                }
                
        except Exception as e:
            tempo_processamento = time.time() - inicio_tempo
            logger.error(f"Erro ao processar {tipo_imagem} para {variavel}: {e}")
            
            return {
                'variavel': variavel,
                'tipo_imagem': tipo_imagem,
                'caminho': str(caminho_imagem),
                'sucesso': False,
                'tempo_processamento': tempo_processamento,
                'resultado_segmentacao': None,
                'metricas_qualidade': {},
                'estatisticas_mascara': {},
                'erro': str(e)
            }
    
    def _calcular_estatisticas_mascara(self, mascara_binaria: np.ndarray) -> Dict:
        """
        Calcula estatísticas detalhadas da máscara binária
        
        Args:
            mascara_binaria (np.ndarray): Máscara binária resultante
            
        Returns:
            Dict: Estatísticas da máscara
        """
        try:
            if mascara_binaria is None:
                return {}
            
            # Converter para booleano se necessário
            if mascara_binaria.dtype != bool:
                mascara_bool = mascara_binaria > 0
            else:
                mascara_bool = mascara_binaria
            
            total_pixels = mascara_binaria.size
            pixels_segmentados = np.sum(mascara_bool)
            pixels_fundo = total_pixels - pixels_segmentados
            
            # Calcular percentual de segmentação
            percentual_segmentado = (pixels_segmentados / total_pixels) * 100
            
            # Encontrar componentes conectados para análise de fragmentação
            try:
                import cv2
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                    mascara_binaria.astype(np.uint8), connectivity=8
                )
                
                # Excluir o fundo (label 0)
                componentes_validos = num_labels - 1
                areas_componentes = stats[1:, cv2.CC_STAT_AREA] if componentes_validos > 0 else []
                
                estatisticas = {
                    'total_pixels': int(total_pixels),
                    'pixels_segmentados': int(pixels_segmentados),
                    'pixels_fundo': int(pixels_fundo),
                    'percentual_segmentado': round(percentual_segmentado, 2),
                    'num_componentes': int(componentes_validos),
                    'area_maior_componente': int(np.max(areas_componentes)) if len(areas_componentes) > 0 else 0,
                    'area_media_componentes': round(float(np.mean(areas_componentes)), 2) if len(areas_componentes) > 0 else 0,
                    'fragmentacao': componentes_validos > 1
                }
                
            except ImportError:
                # Fallback se opencv não estiver disponível
                estatisticas = {
                    'total_pixels': int(total_pixels),
                    'pixels_segmentados': int(pixels_segmentados),
                    'pixels_fundo': int(pixels_fundo),
                    'percentual_segmentado': round(percentual_segmentado, 2),
                    'num_componentes': 'N/A',
                    'area_maior_componente': 'N/A',
                    'area_media_componentes': 'N/A',
                    'fragmentacao': 'N/A'
                }
            
            return estatisticas
            
        except Exception as e:
            logger.warning(f"Erro ao calcular estatísticas da máscara: {e}")
            return {}
    
    def processar_variavel(self, variavel: str) -> Dict:
        """
        Processa todas as imagens de uma variável específica
        
        Args:
            variavel (str): ID da variável a ser processada
            
        Returns:
            Dict: Resultado do processamento da variável
        """
        logger.info(f"Processando variável: {variavel}")
        inicio_tempo = time.time()
        
        # Verificar se a pasta existe e contém os arquivos necessários
        pasta_valida, arquivos = self._verificar_pasta_imagem(variavel)
        
        if not pasta_valida:
            return {
                'variavel': variavel,
                'sucesso': False,
                'tempo_processamento': time.time() - inicio_tempo,
                'erro': 'Pasta inválida ou arquivos faltando',
                'resultados_imagens': [],
                'metricas_resumo': {}
            }
        
        resultados_imagens = []
        
        # Processar cada tipo de imagem
        for tipo_imagem, caminho_arquivo in arquivos.items():
            resultado_imagem = self._processar_imagem(caminho_arquivo, tipo_imagem, variavel)
            resultados_imagens.append(resultado_imagem)
        
        # Calcular métricas de resumo
        sucessos = [r['sucesso'] for r in resultados_imagens]
        sucesso_geral = any(sucessos)
        
        # Agregar métricas de qualidade
        mses = [r['metricas_qualidade'].get('mse_global', 0) for r in resultados_imagens if r['sucesso']]
        rmss = [r['metricas_qualidade'].get('rms_global', 0) for r in resultados_imagens if r['sucesso']]
        tempos = [r['tempo_processamento'] for r in resultados_imagens]
        
        metricas_resumo = {
            'mse_medio': round(np.mean(mses), 3) if mses else 0,
            'rms_medio': round(np.mean(rmss), 3) if rmss else 0,
            'tempo_total': round(sum(tempos), 3),
            'tempo_medio_por_imagem': round(np.mean(tempos), 3) if tempos else 0
        }
        
        tempo_total = time.time() - inicio_tempo
        
        resultado_variavel = {
            'variavel': variavel,
            'sucesso': sucesso_geral,
            'tempo_processamento': tempo_total,
            'erro': None if sucesso_geral else 'Nenhuma imagem processada com sucesso',
            'resultados_imagens': resultados_imagens,
            'total_imagens': len(resultados_imagens),
            'imagens_sucesso': sum(sucessos),
            'imagens_falha': len(sucessos) - sum(sucessos),
            'metricas_resumo': metricas_resumo
        }
        
        logger.info(f"✓ Variável {variavel}: {resultado_variavel['imagens_sucesso']}/{resultado_variavel['total_imagens']} imagens processadas (MSE: {metricas_resumo['mse_medio']:.3f}, RMS: {metricas_resumo['rms_medio']:.3f})")
        
        return resultado_variavel
    
    def processar_dataset(self, limite_registros: Optional[int] = None,
                         exibir_progresso: bool = True) -> Dict:
        """
        Processa todo o dataset usando parametrização com funções indicadoras
        
        Args:
            limite_registros (int, optional): Limitar o número de registros processados
            exibir_progresso (bool): Se deve exibir progresso detalhado
            
        Returns:
            Dict: Resultado geral do processamento
        """
        logger.info("🚀 Iniciando processamento do dataset com Parametrização")
        inicio_tempo_total = time.time()
        
        # Preparar lista de variáveis para processar
        variaveis = self.dataframe['id'].astype(str).tolist()
        
        if limite_registros is not None:
            variaveis = variaveis[:limite_registros]
            logger.info(f"📊 Limitando processamento a {limite_registros} registros")
        
        # Processar cada variável
        self.resultados = []
        total_variaveis = len(variaveis)
        
        logger.info(f"📁 Processando {total_variaveis} variáveis...")
        
        for i, variavel in enumerate(variaveis, 1):
            if exibir_progresso:
                logger.info(f"🔄 [{i:3d}/{total_variaveis}] Processando: {variavel}")
            
            resultado_variavel = self.processar_variavel(variavel)
            self.resultados.append(resultado_variavel)
        
        # Calcular estatísticas globais
        tempo_total = time.time() - inicio_tempo_total
        self.estatisticas_globais = self._calcular_estatisticas_globais(tempo_total)
        
        # Log de resumo final
        stats = self.estatisticas_globais
        logger.info(f"🎯 Processamento concluído em {stats['tempo_total']:.1f}s:")
        logger.info(f"   • Variáveis: {stats['variaveis_sucesso']}/{stats['total_variaveis']} ({stats['taxa_sucesso_variaveis']:.1f}%)")
        logger.info(f"   • Imagens: {stats['imagens_sucesso']}/{stats['total_imagens']} ({stats['taxa_sucesso_imagens']:.1f}%)")
        logger.info(f"   • Qualidade: MSE {stats['mse_global']:.3f}, RMS {stats['rms_global']:.3f}")
        
        return {
            'metodo': 'parametrizacao_indicadora',
            'configuracao': {
                'target_size': f"{self.target_width}x{self.target_height}",
                'num_funcoes_indicadoras': self.target_height,
                'kernel_morfologico': self.morph_kernel_size,
                'contraste_aprimorado': self.enhance_contrast
            },
            'estatisticas_globais': self.estatisticas_globais,
            'resultados_detalhados': self.resultados
        }
    
    def _calcular_estatisticas_globais(self, tempo_total: float) -> Dict:
        """
        Calcula estatísticas globais do processamento
        """
        if not self.resultados:
            return {}
        
        # Estatísticas básicas
        total_variaveis = len(self.resultados)
        variaveis_sucesso = sum(1 for r in self.resultados if r.get('sucesso', False))
        total_imagens = sum(r.get('total_imagens', 0) for r in self.resultados)
        imagens_sucesso = sum(r.get('imagens_sucesso', 0) for r in self.resultados)
        
        # Métricas de tempo
        tempos_variaveis = [r.get('tempo_processamento', 0) for r in self.resultados]
        
        # Métricas de qualidade (apenas de sucessos)
        mses_globais = []
        rmss_globais = []
        
        for resultado in self.resultados:
            if resultado.get('sucesso', False):
                metricas_resumo = resultado.get('metricas_resumo', {})
                mse = metricas_resumo.get('mse_medio', 0)
                rms = metricas_resumo.get('rms_medio', 0)
                if mse > 0:  # Filtrar valores inválidos
                    mses_globais.append(mse)
                if rms > 0:
                    rmss_globais.append(rms)
        
        mse_global = np.mean(mses_globais) if mses_globais else 0
        rms_global = np.mean(rmss_globais) if rmss_globais else 0
        
        return {
            'tempo_total': tempo_total,
            'total_variaveis': total_variaveis,
            'variaveis_sucesso': variaveis_sucesso,
            'variaveis_falha': total_variaveis - variaveis_sucesso,
            'total_imagens': total_imagens,
            'imagens_sucesso': imagens_sucesso,
            'imagens_falha': total_imagens - imagens_sucesso,
            'taxa_sucesso_variaveis': (variaveis_sucesso / total_variaveis) * 100 if total_variaveis > 0 else 0,
            'taxa_sucesso_imagens': (imagens_sucesso / total_imagens) * 100 if total_imagens > 0 else 0,
            'mse_global': mse_global,
            'rms_global': rms_global,
            'throughput_variaveis_por_minuto': (total_variaveis / (tempo_total / 60)) if tempo_total > 0 else 0,
            'throughput_imagens_por_minuto': (total_imagens / (tempo_total / 60)) if tempo_total > 0 else 0
        }
    
    def salvar_resultados(self, caminho_saida: Optional[str] = None,
                         incluir_mascaras: bool = False,
                         incluir_metricas_detalhadas: bool = True) -> str:
        """
        Salva os resultados do processamento em arquivo
        
        Args:
            caminho_saida (str, optional): Caminho para salvar os resultados
            incluir_mascaras (bool): Se deve incluir as máscaras binárias (aumenta muito o tamanho)
            incluir_metricas_detalhadas (bool): Se deve incluir métricas detalhadas por linha
            
        Returns:
            str: Caminho do arquivo salvo
        """
        if not self.resultados:
            logger.warning("⚠️  Nenhum resultado para salvar")
            return ""
        
        if caminho_saida is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            caminho_saida = self.project_root / f"resultados_parametrizacao_{timestamp}.json"
        
        try:
            import json
            
            # Custom JSON encoder para tipos numpy
            class NumpyEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    elif isinstance(obj, np.floating):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    return super(NumpyEncoder, self).default(obj)
            
            # Preparar dados para serialização
            dados_exportacao = {
                'metodo': 'parametrizacao_indicadora',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'configuracao': {
                    'target_width': self.target_width,
                    'target_height': self.target_height,
                    'num_funcoes_indicadoras': self.target_height,
                    'morph_kernel_size': self.morph_kernel_size,
                    'min_area': self.min_area,
                    'enhance_contrast': self.enhance_contrast
                },
                'estatisticas_globais': self.estatisticas_globais,
                'resultados': []
            }
            
            # Processar resultados para serialização
            for resultado in self.resultados:
                resultado_serializado = resultado.copy()
                
                # Processar resultados de imagens
                for img_result in resultado_serializado.get('resultados_imagens', []):
                    if 'resultado_segmentacao' in img_result and img_result['resultado_segmentacao']:
                        seg_result = img_result['resultado_segmentacao']
                        
                        # Dados essenciais sempre incluídos
                        dados_essenciais = {
                            'sucesso': seg_result.get('sucesso', False),
                            'mse_global': seg_result.get('mse_global', 0),
                            'rms_global': seg_result.get('rms_global', 0)
                        }
                        
                        # Incluir métricas detalhadas se solicitado
                        if incluir_metricas_detalhadas:
                            dados_essenciais.update({
                                'metricas_linhas': seg_result.get('metricas_linhas', []),
                                'parametros_linhas': seg_result.get('parametros_linhas', [])
                            })
                        
                        # Incluir máscaras se solicitado (cuidado com o tamanho!)
                        if incluir_mascaras:
                            mascara = seg_result.get('mascara_binaria')
                            if mascara is not None:
                                dados_essenciais['mascara_shape'] = mascara.shape
                                dados_essenciais['mascara_dtype'] = str(mascara.dtype)
                                # Converter para lista para serialização JSON
                                dados_essenciais['mascara_dados'] = mascara.astype(int).tolist()
                        
                        img_result['resultado_segmentacao'] = dados_essenciais
                
                dados_exportacao['resultados'].append(resultado_serializado)
            
            # Salvar arquivo
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(dados_exportacao, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
            
            tamanho_arquivo = os.path.getsize(caminho_saida) / (1024 * 1024)  # MB
            logger.info(f"💾 Resultados salvos: {caminho_saida} ({tamanho_arquivo:.1f} MB)")
            
            return str(caminho_saida)
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")
            return ""
    
    def visualizar_amostra_resultados(self, num_amostras: int = 3,
                                    tipo_visualizacao: str = 'completo'):
        """
        Visualiza uma amostra dos resultados processados
        
        Args:
            num_amostras (int): Número de amostras a visualizar
            tipo_visualizacao (str): 'simples', 'completo' ou 'metricas'
        """
        try:
            import matplotlib
            matplotlib.use('TkAgg')  # Força backend interativo no Windows
            import matplotlib.pyplot as plt
            
            # Filtrar resultados com sucesso
            resultados_sucesso = [r for r in self.resultados if r['sucesso']]
            
            if not resultados_sucesso:
                logger.warning("Nenhum resultado com sucesso para visualizar")
                return
            
            # Selecionar amostras
            amostras = resultados_sucesso[:num_amostras]
            
            for i, resultado in enumerate(amostras):
                variavel = resultado['variavel']
                imagens_sucesso = [img for img in resultado['resultados_imagens'] if img['sucesso']]
                
                if not imagens_sucesso:
                    continue
                
                if tipo_visualizacao == 'completo':
                    self._visualizar_resultado_completo(resultado, i + 1)
                elif tipo_visualizacao == 'simples':
                    self._visualizar_resultado_simples(resultado, i + 1)
                else:  # metricas
                    self._visualizar_metricas(resultado, i + 1)
            
            plt.show()
            
        except ImportError:
            logger.warning("matplotlib não disponível para visualização")
        except Exception as e:
            logger.error(f"Erro na visualização: {e}")
    
    def _visualizar_resultado_completo(self, resultado: Dict, num_fig: int):
        """Visualização completa com original, processada e máscara"""
        import matplotlib
        matplotlib.use('TkAgg')  # Força backend interativo
        import matplotlib.pyplot as plt
        
        variavel = resultado['variavel']
        imagens_sucesso = [img for img in resultado['resultados_imagens'] if img['sucesso']]
        
        # Verificar se é método combinado (4 resultados)
        if self.metodo_segmentacao == "combinado" and imagens_sucesso:
            primeiro_resultado = imagens_sucesso[0]['resultado_segmentacao']
            if 'mascara_linhas_final' in primeiro_resultado:
                self._visualizar_4_resultados(resultado, num_fig)
                return
        
        # Visualização padrão para outros métodos
        fig, axes = plt.subplots(len(imagens_sucesso), 3, figsize=(15, 5 * len(imagens_sucesso)))
        fig.suptitle(f'Resultado #{num_fig} - Variável: {variavel}', fontsize=16)
        
        if len(imagens_sucesso) == 1:
            axes = axes.reshape(1, -1)
        
        for i, img_result in enumerate(imagens_sucesso):
            seg_result = img_result['resultado_segmentacao']
            tipo_img = img_result['tipo_imagem']
            
            # Imagem original
            img_original = seg_result['imagem_original']
            axes[i, 0].imshow(img_original)
            axes[i, 0].set_title(f'{tipo_img.capitalize()} - Original', color='blue')
            axes[i, 0].axis('off')
            
            # Imagem em grayscale
            img_gray = seg_result['imagem_gray']
            axes[i, 1].imshow(img_gray, cmap='gray')
            axes[i, 1].set_title(f'{tipo_img.capitalize()} - Grayscale', color='blue')
            axes[i, 1].axis('off')
            
            # Máscara binária
            mascara = seg_result['mascara_binaria']
            axes[i, 2].imshow(mascara, cmap='gray')
            mse = seg_result.get('mse_global', 0)
            rms = seg_result.get('rms_global', 0)
            axes[i, 2].set_title(f'{tipo_img.capitalize()} - Máscara (MSE: {mse:.3f}, RMS: {rms:.3f})', color='blue')
            axes[i, 2].axis('off')
        
        plt.tight_layout()
    
    def _visualizar_4_resultados(self, resultado: Dict, num_fig: int):
        """Visualização dos 4 resultados: linhas, colunas, união e intersecção"""
        import matplotlib
        matplotlib.use('TkAgg')  # Força backend interativo
        import matplotlib.pyplot as plt
        
        variavel = resultado['variavel']
        imagens_sucesso = [img for img in resultado['resultados_imagens'] if img['sucesso']]
        
        for idx_img, img_result in enumerate(imagens_sucesso):
            seg_result = img_result['resultado_segmentacao']
            tipo_img = img_result['tipo_imagem']
            
            # Criar figura com 6 subplots lado a lado: original, grayscale, e os 4 resultados
            fig, axes = plt.subplots(1, 6, figsize=(30, 5))
            fig.suptitle(f'4 Resultados de Silhuetas - {variavel} - {tipo_img.capitalize()}', fontsize=16, color='blue')
            
            # Posição 0: Original
            img_original = seg_result['imagem_original']
            axes[0].imshow(img_original)
            axes[0].set_title('Original', color='blue')
            axes[0].axis('off')
            
            # Posição 1: Grayscale
            img_gray = seg_result['imagem_gray']
            axes[1].imshow(img_gray, cmap='gray')
            axes[1].set_title('Grayscale', color='blue')
            axes[1].axis('off')
            
            # Posição 2: Somente Linhas
            mascara_linhas = seg_result['mascara_linhas_final']
            pixels_linhas = seg_result.get('pixels_linhas', 0)
            mse_linhas = seg_result.get('mse_global_linhas', 0)
            axes[2].imshow(mascara_linhas, cmap='gray')
            axes[2].set_title(f'1. Somente Linhas\n{pixels_linhas} pixels | MSE: {mse_linhas:.1f}', color='blue')
            axes[2].axis('off')
            
            # Posição 3: Somente Colunas
            mascara_colunas = seg_result['mascara_colunas_final']
            pixels_colunas = seg_result.get('pixels_colunas', 0)
            mse_colunas = seg_result.get('mse_global_colunas', 0)
            axes[3].imshow(mascara_colunas, cmap='gray')
            axes[3].set_title(f'2. Somente Colunas\n{pixels_colunas} pixels | MSE: {mse_colunas:.1f}', color='blue')
            axes[3].axis('off')
            
            # Posição 4: União
            mascara_uniao = seg_result['mascara_uniao_final']
            pixels_uniao = seg_result.get('pixels_uniao', 0)
            mse_combinado = seg_result.get('mse_global_combinado', 0)
            axes[4].imshow(mascara_uniao, cmap='gray')
            axes[4].set_title(f'3. União (L ∪ C)\n{pixels_uniao} pixels | MSE: {mse_combinado:.1f}', color='blue')
            axes[4].axis('off')
            
            # Posição 5: Intersecção
            mascara_intersecao = seg_result['mascara_intersecao_final']
            pixels_intersecao = seg_result.get('pixels_intersecao', 0)
            axes[5].imshow(mascara_intersecao, cmap='gray')
            axes[5].set_title(f'4. Intersecção (L ∩ C)\n{pixels_intersecao} pixels', color='blue')
            axes[5].axis('off')
            
            plt.tight_layout()
            
            # Adicionar informações de sobreposição na figura
            percentual_intersecao_uniao = seg_result.get('percentual_intersecao_uniao', 0)
            percentual_intersecao_linhas = seg_result.get('percentual_intersecao_linhas', 0)
            percentual_intersecao_colunas = seg_result.get('percentual_intersecao_colunas', 0)
            
            fig.text(0.5, 0.02, 
                f'Análise de Sobreposição: Intersecção vs União: {percentual_intersecao_uniao:.1f}% | '
                f'vs Linhas: {percentual_intersecao_linhas:.1f}% | vs Colunas: {percentual_intersecao_colunas:.1f}%', 
                ha='center', fontsize=10, style='italic')
    
    def _visualizar_resultado_simples(self, resultado: Dict, num_fig: int):
        """Visualização simples apenas com original e máscara"""
        import matplotlib.pyplot as plt
        
        variavel = resultado['variavel']
        imagens_sucesso = [img for img in resultado['resultados_imagens'] if img['sucesso']]
        
        fig, axes = plt.subplots(len(imagens_sucesso), 2, figsize=(10, 5 * len(imagens_sucesso)))
        fig.suptitle(f'Resultado #{num_fig} - Variável: {variavel}', fontsize=16)
        
        if len(imagens_sucesso) == 1:
            axes = axes.reshape(1, -1)
        
        for i, img_result in enumerate(imagens_sucesso):
            seg_result = img_result['resultado_segmentacao']
            tipo_img = img_result['tipo_imagem']
            
            # Imagem original
            img_original = seg_result['imagem_original']
            axes[i, 0].imshow(img_original)
            axes[i, 0].set_title(f'{tipo_img.capitalize()} - Original')
            axes[i, 0].axis('off')
            
            # Máscara binária
            mascara = seg_result['mascara_binaria']
            axes[i, 1].imshow(mascara, cmap='gray')
            axes[i, 1].set_title(f'{tipo_img.capitalize()} - Segmentação')
            axes[i, 1].axis('off')
        
        plt.tight_layout()
    
    def _visualizar_metricas(self, resultado: Dict, num_fig: int):
        """Visualização focada em métricas e estatísticas"""
        import matplotlib.pyplot as plt
        
        variavel = resultado['variavel']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Métricas #{num_fig} - Variável: {variavel}', fontsize=16)
        
        # Métricas de qualidade por imagem
        tipos_imagens = []
        mses = []
        rmss = []
        
        for img_result in resultado['resultados_imagens']:
            if img_result['sucesso']:
                tipos_imagens.append(img_result['tipo_imagem'])
                mses.append(img_result['metricas_qualidade']['mse_global'])
                rmss.append(img_result['metricas_qualidade']['rms_global'])
        
        # Gráfico MSE
        ax1.bar(tipos_imagens, mses, color='skyblue')
        ax1.set_title('MSE por Imagem')
        ax1.set_ylabel('MSE')
        
        # Gráfico RMS
        ax2.bar(tipos_imagens, rmss, color='lightgreen')
        ax2.set_title('RMS por Imagem')
        ax2.set_ylabel('RMS')
        
        # Estatísticas de máscara (se disponível)
        if resultado['resultados_imagens']:
            primeiro_resultado = resultado['resultados_imagens'][0]
            if 'estatisticas_mascara' in primeiro_resultado:
                stats_mascara = primeiro_resultado['estatisticas_mascara']
                if stats_mascara:
                    labels = ['Segmentado', 'Fundo']
                    sizes = [stats_mascara.get('pixels_segmentados', 0), 
                            stats_mascara.get('pixels_fundo', 0)]
                    ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                    ax3.set_title('Distribuição de Pixels')
        
        # Tempo de processamento
        tempos = [img_result['tempo_processamento'] for img_result in resultado['resultados_imagens']]
        ax4.bar(range(len(tempos)), tempos, color='orange')
        ax4.set_title('Tempo de Processamento')
        ax4.set_ylabel('Segundos')
        ax4.set_xlabel('Imagem')
        
        plt.tight_layout()

# Exemplo de uso
if __name__ == "__main__":
    # Este é um exemplo de como usar o modelo
    try:
        import pandas as pd
        
        # Criar DataFrame de exemplo (substitua pelos seus dados reais)
        dados_exemplo = pd.DataFrame({
            'id': ['001', '002', '003', '004', '005']
        })
        
        # Inicializar modelo
        modelo = ModeloSegmentacaoParametrizacao(
            dataframe=dados_exemplo,
            enhance_contrast=True,
            min_area=100
        )
        
        # Processar dataset
        resultados = modelo.processar_dataset(limite_registros=3)
        
        # Salvar resultados
        arquivo_salvo = modelo.salvar_resultados()
        if arquivo_salvo:
            print(f"\n📄 Resultados salvos em: {arquivo_salvo}")
        
    except Exception as e:
        print(f"Erro no exemplo: {e}")
