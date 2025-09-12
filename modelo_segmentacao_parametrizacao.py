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
            logger.error(f"❌ Erro na visualização de bounding boxes: {e}")


    def _exportar_variavel_individual(self, resultado_variavel: Dict) -> None:
        """
        Exporta os dados de uma variável individual imediatamente após processamento.
        
        Args:
            resultado_variavel (Dict): Dados de resultado de uma variável processada
        """
        try:
            # Importar o exportador apenas quando necessário
            from exportacao_parametrizacao import ExportadorParametrizacao
            
            variavel_id = resultado_variavel.get('variavel', '')
            
            # Verificar se a variável foi processada com sucesso
            if not resultado_variavel.get('sucesso', False):
                logger.debug(f"⚠️ Variável {variavel_id} não processada com sucesso - pulando exportação")
                return
            
            # Inicializar exportador
            exportador = ExportadorParametrizacao()
            
            # Exportar dados da variável
            sucesso = exportador.exportar_variavel_completa(resultado_variavel, mostrar_log=False)
            
            if sucesso:
                logger.info(f"✅ Dados de {variavel_id} exportados para TXT")
            else:
                logger.warning(f"⚠️ Falha ao exportar dados de {variavel_id}")
                
        except ImportError:
            logger.debug("⚠️ Módulo de exportação não disponível")
        except Exception as e:
            logger.warning(f"⚠️ Erro na exportação de {resultado_variavel.get('variavel', 'N/A')}: {e}")


# Exemplo de uso
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
                
                # 🎯 NOVA FUNCIONALIDADE: Criar bounding box logo após a execução das silhuetas
                bounding_box_dados = self._processar_bounding_box(resultado_segmentacao, variavel, tipo_imagem)
                
                # 💾 SALVAR IMEDIATAMENTE: Arquivo de bounding box específico para este tipo de foto
                self._salvar_bounding_box_imediato(bounding_box_dados, variavel, tipo_imagem)
                
                return {
                    'variavel': variavel,
                    'tipo_imagem': tipo_imagem,
                    'caminho': str(caminho_imagem),
                    'sucesso': True,
                    'tempo_processamento': tempo_processamento,
                    'resultado_segmentacao': resultado_segmentacao,
                    'bounding_box_dados': bounding_box_dados,  # ✨ Adicionar dados do bounding box
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
    
    def _processar_bounding_box(self, resultado_segmentacao: Dict, variavel: str, tipo_imagem: str) -> Dict:
        """
        Processa bounding box para o resultado da segmentação.
        
        Args:
            resultado_segmentacao (Dict): Resultado da segmentação
            variavel (str): ID da variável
            tipo_imagem (str): Tipo da imagem ('front' ou 'left')
            
        Returns:
            Dict: Dados do bounding box processado
        """
        try:
            logger.debug(f"🎯 Processando bounding box para {variavel} - {tipo_imagem}")
            
            # Importar o detector de bounding box
            from Bounding_box import BoundingBoxDetector
            
            # Inicializar detector
            detector = BoundingBoxDetector(area_minima=100, metodo_deteccao='contornos')
            
            # Determinar qual máscara usar baseado no método de segmentação
            mascara_para_bbox = None
            
            if self.metodo_segmentacao == "combinado":
                # Para método combinado, usar a máscara de união final
                mascara_para_bbox = resultado_segmentacao.get('mascara_uniao_final')
                if mascara_para_bbox is None:
                    # Fallback para máscara binária padrão
                    mascara_para_bbox = resultado_segmentacao.get('mascara_binaria')
            else:
                # Para métodos de linhas ou colunas, usar máscara binária
                mascara_para_bbox = resultado_segmentacao.get('mascara_binaria')
            
            if mascara_para_bbox is None:
                logger.warning(f"Nenhuma máscara disponível para bounding box - {variavel} {tipo_imagem}")
                return {'sucesso': False, 'erro': 'Máscara não encontrada'}
            
            # Detectar bounding boxes
            bbox_resultado = detector.detectar_bounding_boxes(
                mascara_para_bbox, 
                resultado_segmentacao.get('imagem_redimensionada')
            )
            
            if bbox_resultado.get('sucesso', False):
                logger.info(f"✅ Bounding box detectado para {variavel} - {tipo_imagem}: {len(bbox_resultado.get('bounding_boxes', []))} caixas")
                
                # Incluir informações do tipo de imagem
                bbox_resultado['variavel'] = variavel
                bbox_resultado['tipo_imagem'] = tipo_imagem
                
                return bbox_resultado
            else:
                logger.warning(f"❌ Falha na detecção de bounding box para {variavel} - {tipo_imagem}")
                return {'sucesso': False, 'erro': bbox_resultado.get('erro', 'Detecção falhou')}
                
        except Exception as e:
            logger.error(f"Erro no processamento de bounding box para {variavel} - {tipo_imagem}: {e}")
            return {'sucesso': False, 'erro': str(e)}
    
    def _salvar_bounding_box_imediato(self, bounding_box_dados: Dict, variavel: str, tipo_imagem: str) -> bool:
        """
        Salva imediatamente o arquivo de bounding box no formato solicitado.
        
        Args:
            bounding_box_dados (Dict): Dados do bounding box
            variavel (str): ID da variável
            tipo_imagem (str): Tipo da imagem ('front' ou 'left')
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            if not bounding_box_dados.get('sucesso', False):
                logger.debug(f"⚠️ Bounding box sem sucesso para {variavel} - {tipo_imagem}, não salvando arquivo")
                return False
            
            # Manter o ID original sem remover prefixos
            # Isso evita duplicação de arquivos já que syn_f000000-0-Pre e 000000-0-Pre 
            # devem gerar arquivos diferentes
            id_limpo = variavel
            
            # Criar nome do arquivo no formato: id--tipodefoto--boundingbox.txt
            nome_arquivo = f"{id_limpo}--{tipo_imagem}--boundingbox.txt"
            
            # Definir pasta de dados analisados
            pasta_dados = Path(__file__).parent / "dados_analisados"
            pasta_dados.mkdir(exist_ok=True)
            
            caminho_arquivo = pasta_dados / nome_arquivo
            
            # Extrair bounding boxes
            bboxes = bounding_box_dados.get('bounding_boxes', [])
            
            if not bboxes:
                logger.warning(f"⚠️ Nenhuma bounding box para salvar - {variavel} {tipo_imagem}")
                return False
            
            # Salvar arquivo com coordenadas dos 4 pontos
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write(f"# Bounding Box - {nome_arquivo}\n")
                f.write(f"# Variável: {variavel}\n")
                f.write(f"# Tipo de Foto: {tipo_imagem}\n")
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
            
            logger.info(f"✅ Bounding box salvo: {nome_arquivo} ({len(bboxes)} caixas)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar bounding box para {variavel} - {tipo_imagem}: {e}")
            return False
    
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
        
        # 🎨 NOVA FUNCIONALIDADE: Exibir figuras com bounding box imediatamente após processamento
        # DESATIVADO: Comentado para não interromper o processamento - as imagens são exibidas no final
        # if sucesso_geral:
        #     self._exibir_figuras_com_bounding_box(resultado_variavel)
        
        logger.info(f"✓ Variável {variavel}: {resultado_variavel['imagens_sucesso']}/{resultado_variavel['total_imagens']} imagens processadas (MSE: {metricas_resumo['mse_medio']:.3f}, RMS: {metricas_resumo['rms_medio']:.3f})")
        
        return resultado_variavel
    
    def _exibir_figuras_com_bounding_box(self, resultado_variavel: Dict) -> None:
        """
        Exibe figuras com bounding boxes imediatamente após o processamento da variável.
        
        Args:
            resultado_variavel (Dict): Resultado do processamento da variável
        """
        try:
            logger.info(f"🎨 Exibindo figuras com bounding box para {resultado_variavel.get('variavel', 'N/A')}")
            
            # Importar visualizador se disponível
            try:
                from exibicao_BBox_imagens import ExibicaoBBoxImagens
                visualizador = ExibicaoBBoxImagens()
            except ImportError:
                logger.warning("⚠️ Módulo de exibição de bounding box não disponível")
                return
            
            # Processar cada imagem da variável
            for resultado_imagem in resultado_variavel.get('resultados_imagens', []):
                if not resultado_imagem.get('sucesso', False):
                    continue
                
                variavel = resultado_imagem.get('variavel', 'N/A')
                tipo_imagem = resultado_imagem.get('tipo_imagem', 'N/A')
                bounding_box_dados = resultado_imagem.get('bounding_box_dados', {})
                
                if not bounding_box_dados.get('sucesso', False):
                    logger.debug(f"⚠️ Sem bounding box para exibir - {variavel} {tipo_imagem}")
                    continue
                
                # Exibir figura com bounding box
                titulo = f"Bounding Box - {variavel} ({tipo_imagem})"
                logger.info(f"📺 Exibindo: {titulo}")
                
                try:
                    visualizador.visualizar_bbox_individual(bounding_box_dados, titulo)
                    
                    # Pequena pausa para visualização
                    import time
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro na exibição de {titulo}: {e}")
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na exibição geral de figuras com bounding box: {e}")
    
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
            
            # 💾 EXPORTAÇÃO IMEDIATA: Salvar dados da variável processada
            self._exportar_variavel_individual(resultado_variavel)
        
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
    
    def visualizar_amostra_resultados(self, num_amostras: int = 3, tipo_visualizacao: str = 'auto'):
        """
        Visualiza uma amostra dos resultados processados.
        
        NOTA: Visualização agora delegada ao módulo exibicao_imagens_parametrizadas.py
        conforme separação de responsabilidades solicitada.
        
        NOVO: Integração automática com detecção de bounding boxes
        
        Args:
            num_amostras (int): Número de amostras a visualizar
            tipo_visualizacao (str): 'auto', 'simples', 'completo', 'metricas' ou '4_resultados'
        """
        try:
            from exibicao_imagens_parametrizadas import ExibicaoImagensParametrizadas
            
            # Filtrar resultados com sucesso
            resultados_sucesso = [r for r in self.resultados if r['sucesso']]
            
            if not resultados_sucesso:
                logger.warning("Nenhum resultado com sucesso para visualizar")
                print("⚠️ Nenhum resultado com sucesso para visualizar")
                return
            
            # Preparar dados para o visualizador
            resultados_para_visualizar = []
            for resultado in resultados_sucesso[:num_amostras]:
                variavel = resultado['variavel']
                imagens_sucesso = [img for img in resultado['resultados_imagens'] if img['sucesso']]
                
                for img_result in imagens_sucesso:
                    seg_result = img_result['resultado_segmentacao']
                    # Adicionar informações de contexto
                    seg_result['variavel'] = variavel
                    seg_result['tipo_imagem'] = img_result['tipo_imagem']
                    
                    if 'bounding_box_dados' in img_result and img_result['bounding_box_dados'].get('sucesso', False):
                    # Reutilizar dados já processados
                        bbox_dados = img_result['bounding_box_dados']
                        seg_result['bounding_boxes'] = {
                            'mascara_binaria': bbox_dados  # Usar dados já processados
                        }
                        print(f"♻️ Reutilizando bounding boxes: {len(bbox_dados.get('bounding_boxes', []))} caixas")
                    else:
                        print(f"⚠️ Sem bounding boxes disponíveis para {variavel} - {img_result['tipo_imagem']}")
                
                    resultados_para_visualizar.append(seg_result)
            
            # Detectar automaticamente se deve usar visualização de 4 resultados
            if tipo_visualizacao == 'auto' and self.metodo_segmentacao == 'combinado':
                tipo_visualizacao = '4_resultados'
                print(f"🎯 Método combinado detectado - forçando visualização '4_resultados'")
            
            # Usar o módulo de visualização separado
            visualizador = ExibicaoImagensParametrizadas()
            visualizador.visualizar_amostra_resultados(
                resultados_para_visualizar, 
                num_amostras, 
                tipo_visualizacao
            )
            
            # 🎨 NOVA FUNCIONALIDADE: Visualizar bounding boxes se disponíveis
            self._visualizar_bounding_boxes(resultados_para_visualizar)
            
        except ImportError as e:
            logger.warning(f"Módulo de visualização não disponível: {e}")
            print("❌ Módulo exibicao_imagens_parametrizadas não encontrado")
        except Exception as e:
            logger.error(f"Erro na visualização: {e}")
            print(f"❌ Erro na visualização: {e}")
    
    def _processar_bounding_boxes(self, resultado_segmentacao: Dict) -> Dict:
        """
        Processa bounding boxes para um resultado de segmentação.
        
        Args:
            resultado_segmentacao (Dict): Resultado da segmentação
            
        Returns:
            Dict: Resultado com bounding boxes adicionadas
        """
        try:
            from Bounding_box import BoundingBoxDetector
            
            print("📦 Detectando bounding boxes...")
            
            # Inicializar detector de bounding boxes
            detector = BoundingBoxDetector(area_minima=100, metodo_deteccao='contornos')
            
            # Detectar bounding boxes nas máscaras disponíveis
            bounding_boxes_resultado = {}
            
            # Processar máscara binária principal
            if 'mascara_binaria' in resultado_segmentacao:
                bbox_result = detector.detectar_bounding_boxes(
                    resultado_segmentacao['mascara_binaria'],
                    resultado_segmentacao.get('imagem_original')
                )
                if bbox_result.get('sucesso', False):
                    bounding_boxes_resultado['mascara_binaria'] = bbox_result
                    print(f"✅ Bounding boxes detectadas: {len(bbox_result['bounding_boxes'])}")
            
            # Processar máscaras específicas para método combinado
            if 'mascara_uniao_final' in resultado_segmentacao:
                bbox_result = detector.detectar_bounding_boxes(
                    resultado_segmentacao['mascara_uniao_final'],
                    resultado_segmentacao.get('imagem_original')
                )
                if bbox_result.get('sucesso', False):
                    bounding_boxes_resultado['mascara_uniao'] = bbox_result
                    print(f"✅ Bounding boxes união detectadas: {len(bbox_result['bounding_boxes'])}")
            
            if 'mascara_linhas_final' in resultado_segmentacao:
                bbox_result = detector.detectar_bounding_boxes(
                    resultado_segmentacao['mascara_linhas_final'],
                    resultado_segmentacao.get('imagem_original')
                )
                if bbox_result.get('sucesso', False):
                    bounding_boxes_resultado['mascara_linhas'] = bbox_result
                    print(f"✅ Bounding boxes linhas detectadas: {len(bbox_result['bounding_boxes'])}")
            
            if 'mascara_colunas_final' in resultado_segmentacao:
                bbox_result = detector.detectar_bounding_boxes(
                    resultado_segmentacao['mascara_colunas_final'],
                    resultado_segmentacao.get('imagem_original')
                )
                if bbox_result.get('sucesso', False):
                    bounding_boxes_resultado['mascara_colunas'] = bbox_result
                    print(f"✅ Bounding boxes colunas detectadas: {len(bbox_result['bounding_boxes'])}")
            
            # Adicionar bounding boxes ao resultado
            resultado_segmentacao['bounding_boxes'] = bounding_boxes_resultado
            
            return resultado_segmentacao
            
        except ImportError:
            print("⚠️ Módulo Bounding_box não disponível - pulando detecção")
            return resultado_segmentacao
        except Exception as e:
            print(f"⚠️ Erro na detecção de bounding boxes: {e}")
            return resultado_segmentacao
    
    def _visualizar_bounding_boxes(self, resultados_para_visualizar: List[Dict]) -> None:
        """
        Visualiza bounding boxes dos resultados processados.
        
        Args:
            resultados_para_visualizar (List[Dict]): Lista de resultados com bounding boxes
        """
        try:
            from exibicao_BBox_imagens import ExibicaoBBoxImagens
            
            # Filtrar resultados que têm bounding boxes
            resultados_com_bbox = [r for r in resultados_para_visualizar 
                                 if 'bounding_boxes' in r and r['bounding_boxes']]
            
            if not resultados_com_bbox:
                print("ℹ️ Nenhum resultado com bounding boxes para visualizar")
                return
            
            print(f"\n📦 Visualizando bounding boxes para {len(resultados_com_bbox)} resultados...")
            
            # Inicializar visualizador de bounding boxes
            visualizador_bbox = ExibicaoBBoxImagens()
            
            # Visualizar cada resultado
            for i, resultado in enumerate(resultados_com_bbox[:3]):  # Limitar a 3 para não sobrecarregar
                print(f"\n🖼️ Visualizando bounding boxes - {resultado.get('variavel', 'N/A')} {resultado.get('tipo_imagem', 'N/A')}")
                
                # Escolher a melhor máscara para visualização
                bboxes = resultado['bounding_boxes']
                
                if 'mascara_uniao' in bboxes:
                    # Priorizar união se disponível (método combinado)
                    visualizador_bbox.visualizar_bbox_individual(
                        bboxes['mascara_uniao'], 
                        f"União - {resultado.get('variavel', 'N/A')}"
                    )
                elif 'mascara_binaria' in bboxes:
                    # Usar máscara principal
                    visualizador_bbox.visualizar_bbox_individual(
                        bboxes['mascara_binaria'], 
                        f"Segmentação - {resultado.get('variavel', 'N/A')}"
                    )
                
                # Para método combinado, mostrar visualização comparativa
                if self.metodo_segmentacao == 'combinado' and len(bboxes) > 1:
                    try:
                        visualizador_bbox.visualizar_comparativo_bboxes(bboxes)
                    except Exception as e:
                        print(f"⚠️ Erro na visualização comparativa: {e}")
            
            print("✅ Visualização de bounding boxes concluída!")
            
        except ImportError:
            print("⚠️ Módulo exibicao_BBox_imagens não disponível")
        except Exception as e:
            print(f"⚠️ Erro na visualização de bounding boxes: {e}")

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
