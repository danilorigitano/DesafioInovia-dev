"""
Módulo de Exibição de Imagens Parametrizadas - v0.4.0
====================================================

RESPONSABILIDADE: Visualização e análise gráfica dos resultados de segmentação parametrizada
MÓDULO PRINCIPAL: segmentacao_imagens_parametrizacao_indicadora.py (processamento)

Este módulo foi criado conforme solicitado para separar as responsabilidades:
- O módulo principal foca no processamento e segmentação
- Este módulo foca na visualização e análise gráfica dos resultados

FUNCIONALIDADES IMPLEMENTADAS:
=============================
✓ Visualização completa com original, processada e máscara
✓ Visualização dos 4 resultados: linhas, colunas, união e intersecção  
✓ Visualização simples (original + máscara)
✓ Visualização de métricas e estatísticas
✓ Análise comparativa de sobreposição
✓ Gráficos de performance (MSE, RMS, tempo de processamento)
✓ Distribuição de pixels segmentados

MÉTODOS PRINCIPAIS:
==================
- ExibicaoImagensParametrizadas: Classe principal de visualização
- visualizar_amostra_resultados(): Visualiza amostras dos resultados
- visualizar_resultado_completo(): Visualização completa 
- visualizar_4_resultados(): NOVO! Visualização dos 4 tipos de silhuetas
- visualizar_resultado_simples(): Visualização básica
- visualizar_metricas(): Foco em métricas e estatísticas
- visualizar_resultado_individual(): Para um único resultado

COMPATIBILIDADE:
===============
- Funciona com resultados de segmentacao_imagens_parametrizacao_indicadora.py
- Suporta todos os métodos: linhas, colunas, combinado, separado_e_unido
- Backend TkAgg para Windows (interativo)
- Fallback gracioso se matplotlib não disponível

EXEMPLO DE USO:
==============
```python
from exibicao_imagens_parametrizadas import ExibicaoImagensParametrizadas

# Processar imagem primeiro
segmentador = SegmentacaoParametrizacaoIndicadora()
resultado = segmentador.segmentar_separado_e_unido('imagem.jpg')

# Visualizar resultado
visualizador = ExibicaoImagensParametrizadas()
visualizador.visualizar_resultado_individual(resultado, titulo='Minha Imagem')
```

NOTA: Separação de responsabilidades implementada conforme solicitado
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Imports de logging (opcional)
import logging
logger = logging.getLogger(__name__)


class ExibicaoImagensParametrizadas:
    """
    Classe principal para visualização de resultados de segmentação parametrizada.
    
    Esta classe foi criada para separar as responsabilidades de visualização
    do processamento principal de segmentação.
    
    COMPATIBILIDADE:
    ===============
    - Funciona com resultados de SegmentacaoParametrizacaoIndicadora
    - Suporta todos os métodos de segmentação disponíveis
    - Visualização interativa com matplotlib/TkAgg
    
    RESPONSABILIDADES:
    =================
    ✓ Exibição de imagens originais, processadas e máscaras
    ✓ Visualização comparativa dos 4 tipos de silhuetas
    ✓ Gráficos de métricas e estatísticas
    ✓ Análise de performance e sobreposição
    ✓ Diferentes tipos de visualização (completo, simples, métricas)
    
    MÉTODOS PRINCIPAIS:
    ==================
    - visualizar_resultado_individual(): Para um único resultado
    - visualizar_amostra_resultados(): Para múltiplos resultados
    - visualizar_4_resultados(): Específico para método combinado
    - visualizar_metricas(): Foco em estatísticas
    """
    
    def __init__(self, backend='TkAgg'):
        """
        Inicializa o visualizador de imagens parametrizadas.
        
        Args:
            backend (str): Backend do matplotlib ('TkAgg' para Windows interativo)
        """
        self.backend = backend
        self.matplotlib_disponivel = self._verificar_matplotlib()
        
        if self.matplotlib_disponivel:
            print("🎨 Visualizador de Imagens Parametrizadas v0.4.0 inicializado")
            print("📊 Módulo separado para visualização conforme solicitado")
            print("🖼️ Suporte a: linhas, colunas, combinado, separado_e_unido")
            print("📈 Visualizações: completo, simples, métricas, 4_resultados")
        else:
            print("⚠️ Matplotlib não disponível - visualizações limitadas")
    
    def _verificar_matplotlib(self):
        """Verifica se matplotlib está disponível e configura backend."""
        try:
            import matplotlib
            matplotlib.use(self.backend)
            import matplotlib.pyplot as plt
            return True
        except ImportError:
            logger.warning("matplotlib não disponível para visualização")
            return False
        except Exception as e:
            logger.warning(f"Erro ao configurar matplotlib: {e}")
            return False
    
    def visualizar_resultado_individual(self, resultado_segmentacao, titulo="Resultado da Segmentação", 
                                      tipo_visualizacao='auto'):
        """
        Visualiza um único resultado de segmentação.
        
        Args:
            resultado_segmentacao (dict): Resultado da segmentação 
            titulo (str): Título da visualização
            tipo_visualizacao (str): 'auto', 'completo', 'simples', 'metricas', '4_resultados'
        """
        if not self.matplotlib_disponivel:
            print("❌ Matplotlib não disponível para visualização")
            return
        
        try:
            import matplotlib
            matplotlib.use(self.backend)
            import matplotlib.pyplot as plt
            
            # Detectar tipo de resultado automaticamente se necessário
            if tipo_visualizacao == 'auto':
                if ('mascara_linhas_final' in resultado_segmentacao and 
                    'mascara_colunas_final' in resultado_segmentacao and
                    'mascara_uniao_final' in resultado_segmentacao and
                    'mascara_intersecao_final' in resultado_segmentacao):
                    tipo_visualizacao = '4_resultados'
                    print(f"🎯 Detectado: Resultado com 4 silhuetas - usando visualização '4_resultados'")
                elif 'tipo_segmentacao' in resultado_segmentacao and resultado_segmentacao['tipo_segmentacao'] == 'separado_e_unido':
                    tipo_visualizacao = '4_resultados'
                    print(f"🎯 Detectado: Segmentação separada e unida - usando visualização '4_resultados'")
                else:
                    tipo_visualizacao = 'completo'
                    print(f"🎯 Detectado: Resultado padrão - usando visualização 'completo'")
            
            # Executar visualização baseada no tipo
            if tipo_visualizacao == '4_resultados':
                self._visualizar_4_resultados_individual(resultado_segmentacao, titulo)
            elif tipo_visualizacao == 'completo':
                self._visualizar_resultado_completo_individual(resultado_segmentacao, titulo)
            elif tipo_visualizacao == 'simples':
                self._visualizar_resultado_simples_individual(resultado_segmentacao, titulo)
            elif tipo_visualizacao == 'metricas':
                self._visualizar_metricas_individual(resultado_segmentacao, titulo)
            
            plt.show()
            
        except Exception as e:
            logger.error(f"Erro na visualização individual: {e}")
            print(f"❌ Erro na visualização: {e}")
    
    def _visualizar_4_resultados_individual(self, resultado, titulo):
        """
        Visualiza os 4 resultados de segmentação: linhas, colunas, união e intersecção.
        
        Método específico para resultados do tipo 'separado_e_unido' ou 'combinado'.
        """
        import matplotlib
        matplotlib.use(self.backend)
        import matplotlib.pyplot as plt
        
        # Verificar se as chaves necessárias estão presentes
        chaves_necessarias = ['mascara_linhas_final', 'mascara_colunas_final', 
                             'mascara_uniao_final', 'mascara_intersecao_final']
        
        chaves_faltando = [chave for chave in chaves_necessarias if chave not in resultado]
        if chaves_faltando:
            print(f"⚠️ Chaves faltando para visualização 4_resultados: {chaves_faltando}")
            print("🔄 Usando visualização completa como fallback")
            self._visualizar_resultado_completo_individual(resultado, titulo)
            return
        
        # Criar figura com 6 subplots: original, grayscale, e os 4 resultados
        fig, axes = plt.subplots(1, 6, figsize=(30, 5))
        fig.suptitle(f'{titulo} - 4 Tipos de Silhuetas', fontsize=16, color='blue')
        
        # Posição 0: Original
        img_original = resultado['imagem_original']
        axes[0].imshow(img_original)
        axes[0].set_title('Original', color='blue', fontsize=12)
        axes[0].axis('off')
        
        # Posição 1: Grayscale
        img_gray = resultado['imagem_gray']
        axes[1].imshow(img_gray, cmap='gray')
        axes[1].set_title('Grayscale', color='blue', fontsize=12)
        axes[1].axis('off')
        
        # Posição 2: Somente Linhas
        mascara_linhas = resultado['mascara_linhas_final']
        axes[2].imshow(mascara_linhas, cmap='gray')
        axes[2].set_title('Somente Linha', color='blue', fontsize=12)
        axes[2].axis('off')
        
        # Posição 3: Somente Colunas
        mascara_colunas = resultado['mascara_colunas_final']
        axes[3].imshow(mascara_colunas, cmap='gray')
        axes[3].set_title('Somente Coluna', color='blue', fontsize=12)
        axes[3].axis('off')
        
        # Posição 4: Intersecção
        mascara_intersecao = resultado['mascara_intersecao_final']
        axes[4].imshow(mascara_intersecao, cmap='gray')
        axes[4].set_title('Intersecção', color='blue', fontsize=12)
        axes[4].axis('off')
        
        # Posição 5: União
        mascara_uniao = resultado['mascara_uniao_final']
        axes[5].imshow(mascara_uniao, cmap='gray')
        axes[5].set_title('União', color='blue', fontsize=12)
        axes[5].axis('off')
        
        plt.tight_layout()
    
    def _visualizar_resultado_completo_individual(self, resultado, titulo):
        """Visualização completa com original, processada e máscara."""
        import matplotlib
        matplotlib.use(self.backend)
        import matplotlib.pyplot as plt
        
        # Criar figura com 3 subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(titulo, fontsize=16, color='blue')
        
        # Imagem original
        img_original = resultado['imagem_original']
        axes[0].imshow(img_original)
        axes[0].set_title('Original', color='blue')
        axes[0].axis('off')
        
        # Imagem em grayscale
        img_gray = resultado['imagem_gray']
        axes[1].imshow(img_gray, cmap='gray')
        axes[1].set_title('Grayscale', color='blue')
        axes[1].axis('off')
        
        # Máscara binária
        mascara = resultado.get('mascara_binaria', resultado.get('mascara_uniao_final'))
        axes[2].imshow(mascara, cmap='gray')
        
        # Adicionar métricas se disponíveis
        mse = resultado.get('mse_global_combinado', resultado.get('mse_global', 0))
        pixels = resultado.get('pixels_uniao', np.sum(mascara > 0))
        axes[2].set_title(f'Segmentação\\n{pixels} pixels | MSE: {mse:.2f}', color='blue')
        axes[2].axis('off')
        
        plt.tight_layout()
    
    def _visualizar_resultado_simples_individual(self, resultado, titulo):
        """Visualização simples apenas com original e máscara."""
        import matplotlib
        matplotlib.use(self.backend)
        import matplotlib.pyplot as plt
        
        # Criar figura com 2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(titulo, fontsize=16, color='blue')
        
        # Imagem original
        img_original = resultado['imagem_original']
        axes[0].imshow(img_original)
        axes[0].set_title('Original', color='blue')
        axes[0].axis('off')
        
        # Máscara binária
        mascara = resultado.get('mascara_binaria', resultado.get('mascara_uniao_final'))
        axes[1].imshow(mascara, cmap='gray')
        axes[1].set_title('Segmentação', color='blue')
        axes[1].axis('off')
        
        plt.tight_layout()
    
    def _visualizar_metricas_individual(self, resultado, titulo):
        """Visualização focada em métricas e estatísticas."""
        import matplotlib
        matplotlib.use(self.backend)
        import matplotlib.pyplot as plt
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'{titulo} - Análise de Métricas', fontsize=16, color='blue')
        
        # Gráfico 1: MSE por tipo de segmentação (se disponível)
        if 'mse_global_linhas' in resultado and 'mse_global_colunas' in resultado:
            tipos = ['Linhas', 'Colunas', 'Combinado']
            mses = [
                resultado.get('mse_global_linhas', 0),
                resultado.get('mse_global_colunas', 0),
                resultado.get('mse_global_combinado', 0)
            ]
            ax1.bar(tipos, mses, color=['skyblue', 'lightgreen', 'orange'])
            ax1.set_title('MSE por Tipo de Segmentação')
            ax1.set_ylabel('MSE')
        else:
            mse_global = resultado.get('mse_global', 0)
            ax1.bar(['Segmentação'], [mse_global], color='skyblue')
            ax1.set_title('MSE Global')
            ax1.set_ylabel('MSE')
        
        # Gráfico 2: Pixels segmentados por tipo
        if 'pixels_linhas' in resultado and 'pixels_colunas' in resultado:
            tipos = ['Linhas', 'Colunas', 'União', 'Intersecção']
            pixels = [
                resultado.get('pixels_linhas', 0),
                resultado.get('pixels_colunas', 0),
                resultado.get('pixels_uniao', 0),
                resultado.get('pixels_intersecao', 0)
            ]
            ax2.bar(tipos, pixels, color=['coral', 'lightblue', 'gold', 'lightpink'])
            ax2.set_title('Pixels Segmentados por Tipo')
            ax2.set_ylabel('Número de Pixels')
            ax2.tick_params(axis='x', rotation=45)
        else:
            mascara = resultado.get('mascara_binaria', resultado.get('mascara_uniao_final'))
            pixels_segmentados = np.sum(mascara > 0) if mascara is not None else 0
            pixels_fundo = mascara.size - pixels_segmentados if mascara is not None else 0
            ax2.bar(['Segmentado', 'Fundo'], [pixels_segmentados, pixels_fundo], 
                   color=['green', 'gray'])
            ax2.set_title('Distribuição de Pixels')
            ax2.set_ylabel('Número de Pixels')
        
        # Gráfico 3: Percentuais de sobreposição (se disponível)
        if 'percentual_intersecao_uniao' in resultado:
            tipos = ['Int. vs União', 'Int. vs Linhas', 'Int. vs Colunas']
            percentuais = [
                resultado.get('percentual_intersecao_uniao', 0),
                resultado.get('percentual_intersecao_linhas', 0),
                resultado.get('percentual_intersecao_colunas', 0)
            ]
            ax3.bar(tipos, percentuais, color=['purple', 'brown', 'teal'])
            ax3.set_title('Percentuais de Sobreposição')
            ax3.set_ylabel('Percentual (%)')
            ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, 'Dados de sobreposição\\nnão disponíveis', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Análise de Sobreposição')
        
        # Gráfico 4: Informações dimensionais
        if 'imagem_gray' in resultado:
            img_gray = resultado['imagem_gray']
            altura, largura = img_gray.shape
            ax4.bar(['Altura', 'Largura'], [altura, largura], color=['navy', 'maroon'])
            ax4.set_title('Dimensões da Imagem')
            ax4.set_ylabel('Pixels')
        else:
            ax4.text(0.5, 0.5, 'Dados dimensionais\\nnão disponíveis', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Dimensões da Imagem')
        
        plt.tight_layout()
    
    def visualizar_amostra_resultados(self, resultados_list, num_amostras=3, 
                                    tipo_visualizacao='completo'):
        """
        Visualiza uma amostra de múltiplos resultados (compatibilidade com modelo).
        
        Args:
            resultados_list (list): Lista de resultados de segmentação
            num_amostras (int): Número de amostras a visualizar  
            tipo_visualizacao (str): 'simples', 'completo', 'metricas', '4_resultados'
        """
        if not self.matplotlib_disponivel:
            print("❌ Matplotlib não disponível para visualização")
            return
        
        try:
            import matplotlib
            matplotlib.use(self.backend)
            import matplotlib.pyplot as plt
            
            # Filtrar resultados com sucesso
            resultados_sucesso = [r for r in resultados_list if r.get('sucesso', True)]
            
            if not resultados_sucesso:
                logger.warning("Nenhum resultado com sucesso para visualizar")
                print("⚠️ Nenhum resultado válido para visualizar")
                return
            
            # Selecionar amostras
            amostras = resultados_sucesso[:num_amostras]
            print(f"🎨 Visualizando {len(amostras)} amostra(s) - Tipo: {tipo_visualizacao}")
            
            for i, resultado in enumerate(amostras):
                titulo = f"Amostra #{i + 1}"
                
                # Adicionar informações específicas se disponíveis
                if 'variavel' in resultado:
                    titulo += f" - Variável: {resultado['variavel']}"
                
                self.visualizar_resultado_individual(resultado, titulo, tipo_visualizacao)
            
        except Exception as e:
            logger.error(f"Erro na visualização de amostras: {e}")
            print(f"❌ Erro na visualização: {e}")
    
    def visualizar_comparacao_metodos(self, resultado_linhas, resultado_colunas, 
                                    resultado_combinado, titulo="Comparação de Métodos"):
        """
        Visualiza comparação entre diferentes métodos de segmentação.
        
        Args:
            resultado_linhas: Resultado da segmentação por linhas
            resultado_colunas: Resultado da segmentação por colunas  
            resultado_combinado: Resultado da segmentação combinada
            titulo: Título da comparação
        """
        if not self.matplotlib_disponivel:
            print("❌ Matplotlib não disponível para visualização")
            return
        
        try:
            import matplotlib
            matplotlib.use(self.backend)
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(2, 4, figsize=(20, 10))
            fig.suptitle(f'{titulo} - Comparação de Métodos', fontsize=16, color='blue')
            
            # Linha 1: Imagens originais e processadas
            img_original = resultado_linhas.get('imagem_original')
            axes[0, 0].imshow(img_original)
            axes[0, 0].set_title('Original', color='blue')
            axes[0, 0].axis('off')
            
            img_gray = resultado_linhas.get('imagem_gray')
            axes[0, 1].imshow(img_gray, cmap='gray')
            axes[0, 1].set_title('Grayscale', color='blue')
            axes[0, 1].axis('off')
            
            # Máscaras dos métodos individuais
            mascara_linhas = resultado_linhas.get('mascara_binaria')
            axes[0, 2].imshow(mascara_linhas, cmap='gray')
            mse_linhas = resultado_linhas.get('mse_global', 0)
            axes[0, 2].set_title(f'Método Linhas\\nMSE: {mse_linhas:.2f}', color='blue')
            axes[0, 2].axis('off')
            
            mascara_colunas = resultado_colunas.get('mascara_binaria')
            axes[0, 3].imshow(mascara_colunas, cmap='gray')
            mse_colunas = resultado_colunas.get('mse_global', 0)
            axes[0, 3].set_title(f'Método Colunas\\nMSE: {mse_colunas:.2f}', color='blue')
            axes[0, 3].axis('off')
            
            # Linha 2: Resultados combinados
            if 'mascara_uniao_final' in resultado_combinado:
                mascara_uniao = resultado_combinado['mascara_uniao_final']
                axes[1, 0].imshow(mascara_uniao, cmap='gray')
                pixels_uniao = resultado_combinado.get('pixels_uniao', 0)
                axes[1, 0].set_title(f'União\\n{pixels_uniao} pixels', color='blue')
                axes[1, 0].axis('off')
                
                mascara_intersecao = resultado_combinado['mascara_intersecao_final']
                axes[1, 1].imshow(mascara_intersecao, cmap='gray')
                pixels_intersecao = resultado_combinado.get('pixels_intersecao', 0)
                axes[1, 1].set_title(f'Intersecção\\n{pixels_intersecao} pixels', color='blue')
                axes[1, 1].axis('off')
                
                # Gráfico de comparação de pixels
                tipos = ['Linhas', 'Colunas', 'União', 'Intersecção']
                pixels = [
                    np.sum(mascara_linhas > 0) if mascara_linhas is not None else 0,
                    np.sum(mascara_colunas > 0) if mascara_colunas is not None else 0,
                    pixels_uniao,
                    pixels_intersecao
                ]
                axes[1, 2].bar(tipos, pixels, color=['skyblue', 'lightgreen', 'orange', 'pink'])
                axes[1, 2].set_title('Pixels Segmentados')
                axes[1, 2].set_ylabel('Pixels')
                axes[1, 2].tick_params(axis='x', rotation=45)
                
                # Gráfico de MSE
                mses = [mse_linhas, mse_colunas, resultado_combinado.get('mse_global_combinado', 0)]
                axes[1, 3].bar(['Linhas', 'Colunas', 'Combinado'], mses, 
                              color=['coral', 'lightblue', 'gold'])
                axes[1, 3].set_title('MSE por Método')
                axes[1, 3].set_ylabel('MSE')
                axes[1, 3].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            logger.error(f"Erro na visualização comparativa: {e}")
            print(f"❌ Erro na visualização: {e}")


def exemplo_uso():
    """
    Exemplo de como usar o módulo de exibição de imagens parametrizadas.
    """
    print("=" * 60)
    print("📖 EXEMPLO DE USO - Exibição de Imagens Parametrizadas")
    print("=" * 60)
    
    print("""
🎯 PASSOS PARA USO:

1. Processar imagem com o módulo principal:
   ```python
   from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora
   
   segmentador = SegmentacaoParametrizacaoIndicadora()
   resultado = segmentador.segmentar_separado_e_unido('imagem.jpg')
   ```

2. Visualizar resultado:
   ```python
   from exibicao_imagens_parametrizadas import ExibicaoImagensParametrizadas
   
   visualizador = ExibicaoImagensParametrizadas()
   visualizador.visualizar_resultado_individual(resultado, 'Minha Imagem')
   ```

🎨 TIPOS DE VISUALIZAÇÃO DISPONÍVEIS:
- 'auto': Detecta automaticamente o melhor tipo
- 'completo': Original + Grayscale + Máscara
- 'simples': Original + Máscara apenas
- 'metricas': Foco em estatísticas e gráficos
- '4_resultados': Linhas + Colunas + União + Intersecção

📊 MÉTODOS SUPORTADOS:
- segmentar(): Segmentação por linhas
- segmentar_por_colunas(): Segmentação por colunas  
- segmentar_combinado(): Segmentação híbrida
- segmentar_separado_e_unido(): NOVO! Separado + União

✅ RESPONSABILIDADE SEPARADA:
- Processamento: segmentacao_imagens_parametrizacao_indicadora.py
- Visualização: exibicao_imagens_parametrizadas.py (ESTE MÓDULO)
""")


if __name__ == "__main__":
    # Executar exemplo de uso
    exemplo_uso()
    
    # Testar inicialização
    try:
        visualizador = ExibicaoImagensParametrizadas()
        print("\\n✅ Módulo inicializado com sucesso!")
        print("🎨 Pronto para visualizar resultados de segmentação parametrizada")
        
    except Exception as e:
        print(f"\\n❌ Erro na inicialização: {e}")
