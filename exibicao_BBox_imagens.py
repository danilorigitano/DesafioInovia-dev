"""
Exibição de Bounding Boxes em Imagens - v1.0.0
==============================================

RESPONSABILIDADE: Visualização de bounding boxes detectadas nas silhuetas
de união e outras máscaras obtidas da segmentação parametrizada.

FUNCIONALIDADES:
===============
✓ Visualização de bounding boxes em silhuetas individuais
✓ Comparação visual entre diferentes tipos de silhuetas com suas bounding boxes
✓ Exibição de métricas das bounding boxes
✓ Visualização sobreposta na imagem original
✓ Análise comparativa de cobertura das bounding boxes

COMPATIBILIDADE:
===============
- Funciona com resultados de Bounding_box.py
- Integra com sistema de exibição existente
- Suporte para resultados de segmentacao_imagens_parametrizacao_indicadora.py

EXEMPLO DE USO:
==============
```python
from exibicao_BBox_imagens import ExibicaoBBoxImagens
from Bounding_box import BoundingBoxDetector
from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora

# Processar imagem
segmentador = SegmentacaoParametrizacaoIndicadora()
resultado = segmentador.segmentar_separado_e_unido('imagem.jpg')

# Detectar bounding boxes
detector = BoundingBoxDetector()
bbox_resultado = detector.processar_resultado_segmentacao(resultado)

# Visualizar resultado
visualizador = ExibicaoBBoxImagens()
visualizador.visualizar_todas_bboxes(bbox_resultado)
```
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configurar matplotlib para Windows
import matplotlib
try:
    matplotlib.use('TkAgg')  # Backend interativo para Windows
except:
    pass

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

import logging
logger = logging.getLogger(__name__)


class ExibicaoBBoxImagens:
    """
    Classe para visualização de bounding boxes em silhuetas.
    
    Esta classe implementa diferentes tipos de visualização para mostrar
    as bounding boxes detectadas nas silhuetas de união e outras máscaras
    obtidas da segmentação parametrizada.
    
    MÉTODOS PRINCIPAIS:
    ==================
    - visualizar_todas_bboxes(): Visualização completa de todas as silhuetas
    - visualizar_bbox_individual(): Visualização de uma única silhueta
    - visualizar_comparativo_bboxes(): Comparação entre diferentes silhuetas
    - visualizar_metricas_bboxes(): Foco nas métricas das bounding boxes
    - visualizar_sobreposicao(): Sobreposição das bounding boxes na imagem original
    """
    
    def __init__(self, figsize=(16, 12), dpi=100):
        """
        Inicializa o visualizador de bounding boxes.
        
        Args:
            figsize (tuple): Tamanho da figura matplotlib
            dpi (int): DPI para qualidade da imagem
        """
        self.figsize = figsize
        self.dpi = dpi
        
        # Configurar estilo matplotlib
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        })
        
        print("🎯 ExibicaoBBoxImagens v1.0.0 inicializado")
        print(f"   - Tamanho da figura: {figsize}")
        print(f"   - DPI: {dpi}")
    
    
    def visualizar_todas_bboxes(self, resultado_bbox_completo, titulo="Bounding Boxes em Todas as Silhuetas"):
        """
        Visualiza bounding boxes de todas as silhuetas em uma única figura.
        
        Args:
            resultado_bbox_completo (dict): Resultado do BoundingBoxDetector.processar_resultado_segmentacao()
            titulo (str): Título da visualização
        """
        try:
            print("\n" + "=" * 60)
            print("🖼️  VISUALIZAÇÃO COMPLETA - TODAS AS BOUNDING BOXES")
            print("=" * 60)
            
            # Verificar validade do resultado
            if not resultado_bbox_completo.get('sucesso', False):
                raise ValueError("Resultado de bounding boxes inválido")
            
            bbox_por_silhueta = resultado_bbox_completo.get('bounding_boxes_por_silhueta', {})
            resultado_original = resultado_bbox_completo.get('resultado_segmentacao_original', {})
            
            # Configurar subplot
            fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
            fig.suptitle(titulo, fontsize=16, fontweight='bold')
            
            # Layout: 2x2 grid para as 4 silhuetas
            gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
            
            # Lista de silhuetas para visualizar
            silhuetas = [
                ('linhas', 'Segmentação por Linhas'),
                ('colunas', 'Segmentação por Colunas'), 
                ('uniao', 'União (Linhas ∪ Colunas)'),
                ('intersecao', 'Intersecção (Linhas ∩ Colunas)')
            ]
            
            positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
            
            for i, ((silhueta_nome, silhueta_titulo), pos) in enumerate(zip(silhuetas, positions)):
                ax = fig.add_subplot(gs[pos[0], pos[1]])
                
                # Verificar se a silhueta existe
                bbox_resultado = bbox_por_silhueta.get(silhueta_nome)
                if not bbox_resultado or not bbox_resultado.get('sucesso', False):
                    ax.text(0.5, 0.5, f'Silhueta {silhueta_nome}\nnão disponível', 
                           ha='center', va='center', transform=ax.transAxes,
                           fontsize=12, color='red')
                    ax.set_title(silhueta_titulo, fontweight='bold')
                    ax.axis('off')
                    continue
                
                # Obter dados da bounding box
                mascara_com_bbox = bbox_resultado.get('mascara_com_bboxes')
                bounding_boxes = bbox_resultado.get('bounding_boxes', [])
                metricas = bbox_resultado.get('metricas', {})
                
                if mascara_com_bbox is not None:
                    # Exibir máscara com bounding boxes
                    ax.imshow(mascara_com_bbox)
                    
                    # Título com informações
                    num_bboxes = len(bounding_boxes)
                    cobertura = metricas.get('cobertura_percentual', 0)
                    ax.set_title(f'{silhueta_titulo}\n{num_bboxes} BBoxes, {cobertura:.1f}% cobertura', 
                               fontweight='bold', fontsize=11)
                    
                    # Informações adicionais no canto
                    if num_bboxes > 0:
                        info_text = f"Área total: {metricas.get('area_total_bboxes', 0)} px²"
                        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8),
                               fontsize=8, va='top')
                
                ax.axis('off')
            
            plt.tight_layout()
            plt.show()
            
            # Exibir estatísticas textuais
            self._exibir_estatisticas_resumidas(bbox_por_silhueta)
            
        except Exception as e:
            print(f"❌ Erro na visualização completa: {e}")
    
    
    def visualizar_bbox_individual(self, resultado_bbox, titulo=None, mostrar_original=True):
        """
        Visualiza bounding boxes de uma única silhueta.
        
        Args:
            resultado_bbox (dict): Resultado do BoundingBoxDetector.detectar_bounding_boxes()
            titulo (str): Título customizado
            mostrar_original (bool): Se deve mostrar a máscara original também
        """
        try:
            print("\n🖼️  Visualizando bounding box individual...")
            
            if not resultado_bbox.get('sucesso', False):
                raise ValueError("Resultado de bounding box inválido")
            
            # Dados
            mascara_original = resultado_bbox.get('mascara_original')
            mascara_com_bbox = resultado_bbox.get('mascara_com_bboxes')
            bounding_boxes = resultado_bbox.get('bounding_boxes', [])
            metricas = resultado_bbox.get('metricas', {})
            imagem_original = resultado_bbox.get('imagem_original')
            
            # Configurar layout
            if mostrar_original and imagem_original is not None:
                fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=self.dpi)
                titles = ['Imagem Original', 'Silhueta', 'Silhueta + Bounding Boxes']
                images = [imagem_original, mascara_original, mascara_com_bbox]
            elif mostrar_original:
                fig, axes = plt.subplots(1, 2, figsize=(12, 6), dpi=self.dpi)
                titles = ['Silhueta Original', 'Silhueta + Bounding Boxes']
                images = [mascara_original, mascara_com_bbox]
            else:
                fig, axes = plt.subplots(1, 1, figsize=(8, 6), dpi=self.dpi)
                axes = [axes]  # Transformar em lista para compatibilidade
                titles = ['Silhueta + Bounding Boxes']
                images = [mascara_com_bbox]
            
            # Título principal
            if titulo is None:
                num_bboxes = len(bounding_boxes)
                cobertura = metricas.get('cobertura_percentual', 0)
                titulo = f'Detecção de Bounding Box - {num_bboxes} BBoxes ({cobertura:.1f}% cobertura)'
            
            fig.suptitle(titulo, fontsize=14, fontweight='bold')
            
            # Exibir cada imagem
            for ax, title, image in zip(axes, titles, images):
                if image is not None:
                    ax.imshow(image)
                    ax.set_title(title, fontweight='bold')
                else:
                    ax.text(0.5, 0.5, 'Imagem não disponível', 
                           ha='center', va='center', transform=ax.transAxes)
                ax.axis('off')
            
            # Adicionar informações das bounding boxes
            if len(bounding_boxes) > 0:
                info_text = self._formatar_info_bboxes(bounding_boxes, metricas)
                fig.text(0.02, 0.02, info_text, fontsize=9, 
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8),
                        verticalalignment='bottom')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"❌ Erro na visualização individual: {e}")
    
    
    def visualizar_comparativo_bboxes(self, resultado_bbox_completo, titulo="Comparativo de Bounding Boxes"):
        """
        Visualiza comparação entre diferentes tipos de silhuetas e suas bounding boxes.
        
        Args:
            resultado_bbox_completo (dict): Resultado completo com todas as silhuetas
            titulo (str): Título da visualização
        """
        try:
            print("\n📊 Criando visualização comparativa...")
            
            bbox_por_silhueta = resultado_bbox_completo.get('bounding_boxes_por_silhueta', {})
            
            # Preparar dados para comparação
            dados_comparacao = []
            for nome, bbox_resultado in bbox_por_silhueta.items():
                if bbox_resultado.get('sucesso', False):
                    metricas = bbox_resultado.get('metricas', {})
                    dados_comparacao.append({
                        'nome': nome.capitalize(),
                        'num_bboxes': metricas.get('numero_bboxes', 0),
                        'cobertura': metricas.get('cobertura_percentual', 0),
                        'area_total': metricas.get('area_total_bboxes', 0),
                        'area_media': metricas.get('area_media_bbox', 0)
                    })
            
            if not dados_comparacao:
                print("⚠️  Nenhum dado válido para comparação")
                return
            
            # Criar figura com subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize, dpi=self.dpi)
            fig.suptitle(titulo, fontsize=16, fontweight='bold')
            
            # Dados para gráficos
            nomes = [d['nome'] for d in dados_comparacao]
            num_bboxes = [d['num_bboxes'] for d in dados_comparacao]
            coberturas = [d['cobertura'] for d in dados_comparacao]
            areas_totais = [d['area_total'] for d in dados_comparacao]
            areas_medias = [d['area_media'] for d in dados_comparacao]
            
            # Cores para os gráficos
            cores = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            # Gráfico 1: Número de Bounding Boxes
            bars1 = ax1.bar(nomes, num_bboxes, color=cores)
            ax1.set_title('Número de Bounding Boxes', fontweight='bold')
            ax1.set_ylabel('Quantidade')
            ax1.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, val in zip(bars1, num_bboxes):
                if val > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                            str(val), ha='center', va='bottom', fontweight='bold')
            
            # Gráfico 2: Cobertura Percentual
            bars2 = ax2.bar(nomes, coberturas, color=cores)
            ax2.set_title('Cobertura Percentual', fontweight='bold')
            ax2.set_ylabel('Cobertura (%)')
            ax2.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, val in zip(bars2, coberturas):
                if val > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            # Gráfico 3: Área Total das Bounding Boxes
            bars3 = ax3.bar(nomes, areas_totais, color=cores)
            ax3.set_title('Área Total das Bounding Boxes', fontweight='bold')
            ax3.set_ylabel('Área (pixels²)')
            ax3.tick_params(axis='x', rotation=45)
            
            # Gráfico 4: Área Média das Bounding Boxes
            bars4 = ax4.bar(nomes, areas_medias, color=cores)
            ax4.set_title('Área Média das Bounding Boxes', fontweight='bold')
            ax4.set_ylabel('Área Média (pixels²)')
            ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.show()
            
            # Exibir tabela comparativa
            self._exibir_tabela_comparativa(dados_comparacao)
            
        except Exception as e:
            print(f"❌ Erro na visualização comparativa: {e}")
    
    
    def visualizar_sobreposicao(self, resultado_bbox_completo, tipo_silhueta='uniao', titulo=None):
        """
        Visualiza bounding boxes sobrepostas na imagem original.
        
        Args:
            resultado_bbox_completo (dict): Resultado completo
            tipo_silhueta (str): Tipo de silhueta para sobrepor ('uniao', 'linhas', 'colunas', 'intersecao')
            titulo (str): Título customizado
        """
        try:
            print(f"\n🎨 Criando sobreposição para silhueta: {tipo_silhueta}")
            
            # Obter dados
            bbox_por_silhueta = resultado_bbox_completo.get('bounding_boxes_por_silhueta', {})
            resultado_original = resultado_bbox_completo.get('resultado_segmentacao_original', {})
            
            bbox_resultado = bbox_por_silhueta.get(tipo_silhueta)
            if not bbox_resultado or not bbox_resultado.get('sucesso', False):
                print(f"⚠️  Silhueta {tipo_silhueta} não disponível")
                return
            
            # Obter imagem original
            imagem_original = resultado_original.get('imagem_redimensionada')
            if imagem_original is None:
                imagem_original = resultado_original.get('imagem_original')
            
            if imagem_original is None:
                print("⚠️  Imagem original não disponível")
                return
            
            # Obter bounding boxes
            bounding_boxes = bbox_resultado.get('bounding_boxes', [])
            metricas = bbox_resultado.get('metricas', {})
            
            # Criar figura
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
            
            if titulo is None:
                num_bboxes = len(bounding_boxes)
                titulo = f'Sobreposição na Imagem Original - {tipo_silhueta.capitalize()} ({num_bboxes} BBoxes)'
            
            fig.suptitle(titulo, fontsize=14, fontweight='bold')
            
            # Imagem original
            ax1.imshow(imagem_original)
            ax1.set_title('Imagem Original', fontweight='bold')
            ax1.axis('off')
            
            # Imagem com bounding boxes sobrepostas
            ax2.imshow(imagem_original)
            
            # Desenhar bounding boxes
            cores = ['red', 'lime', 'blue', 'yellow', 'magenta', 'cyan']
            for i, (x, y, w, h) in enumerate(bounding_boxes):
                cor = cores[i % len(cores)]
                
                # Criar retângulo
                rect = patches.Rectangle((x, y), w, h, linewidth=2, 
                                       edgecolor=cor, facecolor='none')
                ax2.add_patch(rect)
                
                # Adicionar label
                ax2.text(x, y-5, f'BBox #{i+1}', color=cor, fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
            
            ax2.set_title(f'Com Bounding Boxes - {tipo_silhueta.capitalize()}', fontweight='bold')
            ax2.axis('off')
            
            # Adicionar informações
            if len(bounding_boxes) > 0:
                info_text = self._formatar_info_bboxes(bounding_boxes, metricas)
                fig.text(0.02, 0.02, info_text, fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8),
                        verticalalignment='bottom')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"❌ Erro na visualização de sobreposição: {e}")
    
    
    def _exibir_estatisticas_resumidas(self, bbox_por_silhueta):
        """Exibe estatísticas resumidas das bounding boxes."""
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS RESUMIDAS DAS BOUNDING BOXES")
        print("=" * 60)
        
        for nome, bbox_resultado in bbox_por_silhueta.items():
            if bbox_resultado.get('sucesso', False):
                bboxes = bbox_resultado.get('bounding_boxes', [])
                metricas = bbox_resultado.get('metricas', {})
                
                print(f"\n🔸 {nome.upper()}:")
                print(f"   - Número de BBoxes: {len(bboxes)}")
                print(f"   - Cobertura: {metricas.get('cobertura_percentual', 0):.1f}%")
                print(f"   - Área total: {metricas.get('area_total_bboxes', 0)} pixels²")
                print(f"   - Área média: {metricas.get('area_media_bbox', 0):.1f} pixels²")
                
                if len(bboxes) > 0:
                    maior_bbox = metricas.get('maior_bbox')
                    menor_bbox = metricas.get('menor_bbox')
                    
                    if maior_bbox:
                        x, y, w, h = maior_bbox
                        print(f"   - Maior BBox: {w}x{h} em ({x}, {y})")
                    
                    if menor_bbox and len(bboxes) > 1:
                        x, y, w, h = menor_bbox
                        print(f"   - Menor BBox: {w}x{h} em ({x}, {y})")
            else:
                print(f"\n🔸 {nome.upper()}: FALHOU - {bbox_resultado.get('erro', 'Erro desconhecido')}")
    
    
    def _formatar_info_bboxes(self, bounding_boxes, metricas):
        """Formata informações das bounding boxes para exibição."""
        info_lines = [
            f"Bounding Boxes Detectadas: {len(bounding_boxes)}",
            f"Cobertura: {metricas.get('cobertura_percentual', 0):.1f}%",
            f"Área Total: {metricas.get('area_total_bboxes', 0)} px²"
        ]
        
        if len(bounding_boxes) > 0:
            info_lines.append(f"Área Média: {metricas.get('area_media_bbox', 0):.1f} px²")
        
        return '\n'.join(info_lines)
    
    
    def _exibir_tabela_comparativa(self, dados_comparacao):
        """Exibe tabela comparativa das métricas."""
        print("\n" + "=" * 80)
        print("📋 TABELA COMPARATIVA DAS BOUNDING BOXES")
        print("=" * 80)
        print(f"{'Silhueta':<15} {'BBoxes':<8} {'Cobertura':<12} {'Área Total':<12} {'Área Média':<12}")
        print("-" * 80)
        
        for dados in dados_comparacao:
            nome = dados['nome'][:14]  # Truncar se muito longo
            print(f"{nome:<15} {dados['num_bboxes']:<8d} {dados['cobertura']:<11.1f}% "
                  f"{dados['area_total']:<12d} {dados['area_media']:<12.1f}")
        
        print("-" * 80)
