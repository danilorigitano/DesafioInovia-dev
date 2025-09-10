"""
Detecção de Bounding Box em Silhuetas - v1.0.0
==============================================

RESPONSABILIDADE: Detectar retângulos delimitadores (bounding boxes) ao redor das silhuetas
da união obtidas da segmentação parametrizada com funções indicadoras.

FUNCIONALIDADES:
===============
✓ Detecção de bounding box na silhueta de união
✓ Múltiplas estratégias de detecção (contornos, coordenadas extremas)
✓ Filtragem de bounding boxes por área mínima
✓ Cálculo de métricas das bounding boxes
✓ Suporte para múltiplas bounding boxes em uma imagem

COMPATIBILIDADE:
===============
- Funciona com resultados de segmentacao_imagens_parametrizacao_indicadora.py
- Suporta máscaras binárias de união de silhuetas
- Integração com sistema de exibição existente

EXEMPLO DE USO:
==============
```python
from Bounding_box import BoundingBoxDetector
from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora

# Obter silhuetas
segmentador = SegmentacaoParametrizacaoIndicadora()
resultado = segmentador.segmentar_separado_e_unido('imagem.jpg')

# Detectar bounding boxes
detector = BoundingBoxDetector()
bbox_resultado = detector.detectar_bounding_boxes(resultado['mascara_uniao_final'])
```
"""

import cv2
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import logging
logger = logging.getLogger(__name__)


class BoundingBoxDetector:
    """
    Classe para detecção de bounding boxes em silhuetas de união.
    
    Esta classe implementa diferentes estratégias para detectar retângulos
    delimitadores ao redor das silhuetas obtidas da união de segmentações
    por linhas e colunas.
    
    MÉTODOS PRINCIPAIS:
    ==================
    - detectar_bounding_boxes(): Método principal de detecção
    - detectar_por_contornos(): Detecção usando contornos OpenCV
    - detectar_por_coordenadas_extremas(): Detecção por coordenadas min/max
    - filtrar_por_area(): Filtra bounding boxes pequenas
    - calcular_metricas(): Calcula estatísticas das bounding boxes
    """
    
    def __init__(self, area_minima=100, metodo_deteccao='contornos'):
        """
        Inicializa o detector de bounding boxes.
        
        Args:
            area_minima (int): Área mínima em pixels para considerar uma bounding box válida
            metodo_deteccao (str): Método de detecção ('contornos' ou 'coordenadas_extremas')
        """
        self.area_minima = area_minima
        self.metodo_deteccao = metodo_deteccao
        
        print("🎯 BoundingBoxDetector v1.0.0 inicializado")
        print(f"   - Área mínima: {area_minima} pixels")
        print(f"   - Método: {metodo_deteccao}")
    
    
    def detectar_bounding_boxes(self, mascara_silhueta, imagem_original=None):
        """
        Detecta bounding boxes na silhueta de união.
        
        Args:
            mascara_silhueta (numpy.ndarray): Máscara binária da silhueta de união
            imagem_original (numpy.ndarray, optional): Imagem original para contexto
            
        Returns:
            dict: Resultado da detecção com bounding boxes e métricas
        """
        try:
            print("\n" + "=" * 50)
            print("🔍 DETECÇÃO DE BOUNDING BOXES")
            print("=" * 50)
            
            # Validação da entrada
            if mascara_silhueta is None:
                raise ValueError("Máscara da silhueta não pode ser None")
            
            # Garantir que a máscara é binária
            if mascara_silhueta.dtype != np.uint8:
                mascara_binaria = (mascara_silhueta > 0).astype(np.uint8) * 255
            else:
                mascara_binaria = mascara_silhueta.copy()
            
            print(f"📐 Máscara de entrada: {mascara_binaria.shape}")
            print(f"📊 Pixels da silhueta: {np.sum(mascara_binaria > 0)}")
            
            # Detectar bounding boxes conforme método escolhido
            if self.metodo_deteccao == 'contornos':
                bounding_boxes = self._detectar_por_contornos(mascara_binaria)
            elif self.metodo_deteccao == 'coordenadas_extremas':
                bounding_boxes = self._detectar_por_coordenadas_extremas(mascara_binaria)
            else:
                # Usar ambos os métodos e combinar
                bbox_contornos = self._detectar_por_contornos(mascara_binaria)
                bbox_coordenadas = self._detectar_por_coordenadas_extremas(mascara_binaria)
                bounding_boxes = bbox_contornos + bbox_coordenadas
            
            # Filtrar por área mínima
            bounding_boxes_filtradas = self._filtrar_por_area(bounding_boxes)
            
            # Calcular métricas
            metricas = self._calcular_metricas(bounding_boxes_filtradas, mascara_binaria.shape)
            
            # Criar máscara com bounding boxes desenhadas
            mascara_com_bbox = self._desenhar_bounding_boxes(mascara_binaria, bounding_boxes_filtradas)
            
            print(f"\n📦 RESULTADOS:")
            print(f"   - Bounding boxes detectadas: {len(bounding_boxes)}")
            print(f"   - Bounding boxes válidas (área >= {self.area_minima}): {len(bounding_boxes_filtradas)}")
            print(f"   - Cobertura total: {metricas['cobertura_percentual']:.1f}%")
            
            return {
                'bounding_boxes': bounding_boxes_filtradas,
                'bounding_boxes_brutas': bounding_boxes,
                'mascara_original': mascara_binaria,
                'mascara_com_bboxes': mascara_com_bbox,
                'metricas': metricas,
                'imagem_original': imagem_original,
                'metodo_deteccao': self.metodo_deteccao,
                'area_minima': self.area_minima,
                'sucesso': True
            }
            
        except Exception as e:
            print(f"❌ Erro durante detecção de bounding boxes: {e}")
            return {'sucesso': False, 'erro': str(e)}
    
    
    def _detectar_por_contornos(self, mascara_binaria):
        """
        Detecta bounding boxes usando contornos do OpenCV.
        
        Args:
            mascara_binaria (numpy.ndarray): Máscara binária
            
        Returns:
            list: Lista de bounding boxes [(x, y, w, h), ...]
        """
        print("🔍 Detectando por contornos...")
        
        # Encontrar contornos
        contornos, _ = cv2.findContours(mascara_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        bounding_boxes = []
        for contorno in contornos:
            # Calcular bounding box do contorno
            x, y, w, h = cv2.boundingRect(contorno)
            bounding_boxes.append((x, y, w, h))
        
        print(f"   - Contornos encontrados: {len(contornos)}")
        print(f"   - Bounding boxes extraídas: {len(bounding_boxes)}")
        
        return bounding_boxes
    
    
    def _detectar_por_coordenadas_extremas(self, mascara_binaria):
        """
        Detecta uma única bounding box usando coordenadas extremas.
        
        Args:
            mascara_binaria (numpy.ndarray): Máscara binária
            
        Returns:
            list: Lista com uma bounding box [(x, y, w, h)]
        """
        print("🔍 Detectando por coordenadas extremas...")
        
        # Encontrar coordenadas dos pixels não-zero
        coords = np.column_stack(np.where(mascara_binaria > 0))
        
        if len(coords) == 0:
            print("   - Nenhum pixel encontrado na máscara")
            return []
        
        # Coordenadas extremas (formato OpenCV: y, x)
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        
        # Converter para formato bounding box (x, y, w, h)
        x, y = x_min, y_min
        w = x_max - x_min + 1
        h = y_max - y_min + 1
        
        print(f"   - Coordenadas extremas: ({x}, {y}) -> ({x+w}, {y+h})")
        print(f"   - Dimensões: {w} x {h}")
        
        return [(x, y, w, h)]
    
    
    def _filtrar_por_area(self, bounding_boxes):
        """
        Filtra bounding boxes por área mínima.
        
        Args:
            bounding_boxes (list): Lista de bounding boxes
            
        Returns:
            list: Lista filtrada de bounding boxes
        """
        filtradas = []
        
        for bbox in bounding_boxes:
            x, y, w, h = bbox
            area = w * h
            
            if area >= self.area_minima:
                filtradas.append(bbox)
            else:
                print(f"   - Filtrada bbox pequena: área {area} < {self.area_minima}")
        
        return filtradas
    
    
    def _calcular_metricas(self, bounding_boxes, shape_imagem):
        """
        Calcula métricas das bounding boxes.
        
        Args:
            bounding_boxes (list): Lista de bounding boxes
            shape_imagem (tuple): Dimensões da imagem (height, width)
            
        Returns:
            dict: Métricas calculadas
        """
        altura_imagem, largura_imagem = shape_imagem
        area_total_imagem = altura_imagem * largura_imagem
        
        if not bounding_boxes:
            return {
                'numero_bboxes': 0,
                'area_total_bboxes': 0,
                'area_media_bbox': 0,
                'cobertura_percentual': 0.0,
                'maior_bbox': None,
                'menor_bbox': None
            }
        
        # Calcular áreas
        areas = [w * h for x, y, w, h in bounding_boxes]
        area_total_bboxes = sum(areas)
        area_media = np.mean(areas)
        cobertura_percentual = (area_total_bboxes / area_total_imagem) * 100
        
        # Encontrar maior e menor
        idx_maior = np.argmax(areas)
        idx_menor = np.argmin(areas)
        maior_bbox = bounding_boxes[idx_maior]
        menor_bbox = bounding_boxes[idx_menor]
        
        return {
            'numero_bboxes': len(bounding_boxes),
            'area_total_bboxes': area_total_bboxes,
            'area_media_bbox': area_media,
            'cobertura_percentual': cobertura_percentual,
            'maior_bbox': maior_bbox,
            'menor_bbox': menor_bbox,
            'areas_individuais': areas
        }
    
    
    def _desenhar_bounding_boxes(self, mascara_binaria, bounding_boxes):
        """
        Desenha bounding boxes na máscara.
        
        Args:
            mascara_binaria (numpy.ndarray): Máscara original
            bounding_boxes (list): Lista de bounding boxes
            
        Returns:
            numpy.ndarray: Máscara com bounding boxes desenhadas
        """
        # Criar imagem colorida para desenhar
        if len(mascara_binaria.shape) == 2:
            mascara_com_bbox = cv2.cvtColor(mascara_binaria, cv2.COLOR_GRAY2RGB)
        else:
            mascara_com_bbox = mascara_binaria.copy()
        
        # Desenhar cada bounding box
        for i, (x, y, w, h) in enumerate(bounding_boxes):
            # Cor diferente para cada bbox (vermelho, verde, azul, etc.)
            cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            cor = cores[i % len(cores)]
            
            # Desenhar retângulo
            cv2.rectangle(mascara_com_bbox, (x, y), (x + w, y + h), cor, 2)
            
            # Adicionar texto com número da bbox
            cv2.putText(mascara_com_bbox, f'#{i+1}', (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 1)
        
        return mascara_com_bbox


    def processar_resultado_segmentacao(self, resultado_segmentacao):
        """
        Processa resultado completo da segmentação para detectar bounding boxes.
        
        Args:
            resultado_segmentacao (dict): Resultado do método segmentar_separado_e_unido()
            
        Returns:
            dict: Resultado com bounding boxes detectadas em todas as silhuetas
        """
        try:
            print("\n" + "=" * 60)
            print("🎯 PROCESSAMENTO COMPLETO - BOUNDING BOXES EM TODAS AS SILHUETAS")
            print("=" * 60)
            
            # Verificar se o resultado é válido
            if not resultado_segmentacao.get('sucesso', False):
                raise ValueError("Resultado de segmentação inválido")
            
            resultados_bbox = {}
            
            # Lista de máscaras para processar
            mascaras_para_processar = [
                ('linhas', resultado_segmentacao.get('mascara_linhas_final')),
                ('colunas', resultado_segmentacao.get('mascara_colunas_final')),
                ('uniao', resultado_segmentacao.get('mascara_uniao_final')),
                ('intersecao', resultado_segmentacao.get('mascara_intersecao_final'))
            ]
            
            # Processar cada máscara
            for nome, mascara in mascaras_para_processar:
                if mascara is not None:
                    print(f"\n🔍 Processando silhueta: {nome.upper()}")
                    bbox_resultado = self.detectar_bounding_boxes(
                        mascara, 
                        resultado_segmentacao.get('imagem_redimensionada')
                    )
                    resultados_bbox[nome] = bbox_resultado
                else:
                    print(f"⚠️  Silhueta {nome} não encontrada")
                    resultados_bbox[nome] = {'sucesso': False, 'erro': 'Máscara não encontrada'}
            
            # Compilar resultado final
            resultado_final = {
                'resultado_segmentacao_original': resultado_segmentacao,
                'bounding_boxes_por_silhueta': resultados_bbox,
                'metodo_deteccao': self.metodo_deteccao,
                'area_minima': self.area_minima,
                'sucesso': True
            }
            
            # Estatísticas resumidas
            print(f"\n📊 RESUMO DAS BOUNDING BOXES:")
            for nome, bbox_resultado in resultados_bbox.items():
                if bbox_resultado.get('sucesso', False):
                    num_bboxes = len(bbox_resultado.get('bounding_boxes', []))
                    cobertura = bbox_resultado.get('metricas', {}).get('cobertura_percentual', 0)
                    print(f"   - {nome.capitalize()}: {num_bboxes} bboxes, cobertura {cobertura:.1f}%")
                else:
                    print(f"   - {nome.capitalize()}: FALHOU")
            
            return resultado_final
            
        except Exception as e:
            print(f"❌ Erro no processamento completo: {e}")
            return {'sucesso': False, 'erro': str(e)}
