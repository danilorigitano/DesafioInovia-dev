import numpy as np
import cv2
from PIL import Image
import warnings
warnings.filterwarnings('ignore')


class SegmentacaoParametrizacaoIndicadora:
    
    def __init__(self, target_width=1024, target_height=768, 
                 morph_kernel_size=3, min_area=50, enhance_contrast=True):
        """Inicializa o segmentador com parametrização indicadora."""
        self.target_width = target_width
        self.target_height = target_height
        self.morph_kernel_size = morph_kernel_size
        self.min_area = min_area
        self.enhance_contrast = enhance_contrast
        
        print(f"🔧 Segmentador v0.6.0 OTIMIZADO inicializado: {self.target_width}x{self.target_height}")
    
    def _redimensionar_imagem(self, imagem):
        """Redimensiona a imagem para as dimensões alvo."""
        return cv2.resize(imagem, (self.target_width, self.target_height), interpolation=cv2.INTER_CUBIC)
    
    def _converter_para_gray(self, imagem):
        """Converte imagem para escala de cinza."""
        if len(imagem.shape) == 3:
            gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        else:
            gray = imagem.copy()
        return np.clip(gray, 0, 255).astype(np.uint8)
    
    def _melhorar_contraste(self, imagem_gray):
        """Aplica melhoria de contraste usando CLAHE."""
        if self.enhance_contrast:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            return clahe.apply(imagem_gray)
        return imagem_gray
    
    def _gerar_funcao_indicadora(self, comprimento, pixel_inicio, pixel_fim, valor_maximo, is_coluna=False):
        """
        Gera função indicadora genérica otimizada para linhas ou colunas.
        """
        # Validação otimizada
        if is_coluna:
            limite = comprimento // 3
            pixel_inicio = np.clip(pixel_inicio, 5, limite + 50)
            pixel_fim = np.clip(pixel_fim, limite - 50, comprimento - 5)
        else:
            meio = comprimento // 2
            pixel_inicio = np.clip(pixel_inicio, 5, meio + 50)
            pixel_fim = np.clip(pixel_fim, meio - 50, comprimento - 5)
        
        # Garantir ordem correta
        if pixel_inicio >= pixel_fim:
            pixel_fim = max(pixel_inicio + 10, comprimento // 2)
            
        valor_maximo = np.clip(valor_maximo, 40, 255)
        
        # Criar função base
        funcao = np.zeros(comprimento, dtype=np.float32)
        funcao[pixel_inicio:pixel_fim+1] = valor_maximo
        
        # Suavização otimizada
        tamanho_transicao = min(5, (pixel_fim - pixel_inicio) // 4)
        if tamanho_transicao > 0:
            # Transição de subida
            inicio_suave = pixel_inicio
            fim_suave = min(pixel_inicio + tamanho_transicao, comprimento)
            if fim_suave > inicio_suave:
                fatores = np.linspace(0, valor_maximo, fim_suave - inicio_suave + 1)[1:]
                funcao[inicio_suave:fim_suave] = fatores[:fim_suave-inicio_suave]
            
            # Transição de descida
            inicio_desc = max(0, pixel_fim - tamanho_transicao + 1)
            if inicio_desc < pixel_fim:
                fatores = np.linspace(valor_maximo, 0, pixel_fim - inicio_desc + 1)[:-1]
                funcao[inicio_desc:pixel_fim] = fatores[:pixel_fim-inicio_desc]
        
        return np.clip(funcao, 0, 255)
    
    def _gerar_multiplas_funcoes_otimizada(self, comprimento, pontos_inicio, pontos_fim, valor_maximo, is_coluna=False):
        """Geração vetorizada de múltiplas funções indicadoras."""
        n_funcoes = len(pontos_inicio)
        funcoes = np.zeros((n_funcoes, comprimento), dtype=np.float32)
        
        pontos_inicio = np.asarray(pontos_inicio)
        pontos_fim = np.asarray(pontos_fim)
        
        # Validação vetorizada
        if is_coluna:
            limite = comprimento // 3
            pontos_inicio = np.clip(pontos_inicio, 5, limite + 50)
            pontos_fim = np.clip(pontos_fim, limite - 50, comprimento - 5)
        else:
            meio = comprimento // 2
            pontos_inicio = np.clip(pontos_inicio, 5, meio + 50)
            pontos_fim = np.clip(pontos_fim, meio - 50, comprimento - 5)
        
        # Correção de ordem
        mask_invalido = pontos_inicio >= pontos_fim
        pontos_fim[mask_invalido] = np.maximum(pontos_inicio[mask_invalido] + 10, comprimento // 2)
        
        # Preenchimento eficiente
        for i in range(n_funcoes):
            funcoes[i, pontos_inicio[i]:pontos_fim[i]+1] = valor_maximo
        
        # Suavização vetorizada
        tamanhos_transicao = np.minimum(5, (pontos_fim - pontos_inicio) // 4)
        mask_suavizacao = tamanhos_transicao > 0
        
        for i in np.where(mask_suavizacao)[0]:
            tamanho = tamanhos_transicao[i]
            inicio, fim = pontos_inicio[i], pontos_fim[i]
            
            # Subida
            if tamanho > 0 and inicio + tamanho <= comprimento:
                fatores = np.linspace(0, valor_maximo, tamanho + 1)[1:]
                end_pos = min(inicio + len(fatores), comprimento)
                funcoes[i, inicio:end_pos] = fatores[:end_pos-inicio]
            
            # Descida
            if fim - tamanho >= 0:
                fatores = np.linspace(valor_maximo, 0, tamanho + 1)[:-1]
                start_pos = max(0, fim - len(fatores) + 1)
                end_pos = min(fim + 1, comprimento)
                funcoes[i, start_pos:end_pos] = fatores[:end_pos-start_pos]
        
        return np.clip(funcoes, 0, 255)
    
    def _calcular_mse_vectorizado(self, pixels, funcoes_batch):
        """Cálculo vectorizado de MSE para múltiplas funções."""
        diff = funcoes_batch - pixels[np.newaxis, :]
        return np.mean(diff ** 2, axis=1)
    
    def _calcular_metricas(self, pixels, idx):
        """Calcula métricas básicas para pixels."""
        return {
            'idx': idx,
            'media': np.mean(pixels),
            'desvio_padrao': np.std(pixels),
            'contraste': np.max(pixels) - np.min(pixels),
            'min_val': np.min(pixels),
            'max_val': np.max(pixels)
        }
    
    def _otimizar_parametros(self, pixels, idx, is_coluna=False):
        """Otimização vetorizada de parâmetros."""
        comprimento = len(pixels)
        step = 1
        valor_max = 200 if is_coluna else 100
        
        if is_coluna:
            regiao = 0.05
            ponto_inicial = round(comprimento * regiao)
            ponto_final = round(comprimento * (1 - regiao))
            limite_max = round(comprimento * 0.32 + 1)
            limite_min = round(comprimento * 0.32 - 1)
        else:
            regiao = 0.16
            ponto_inicial = round(comprimento * regiao)
            ponto_final = round(comprimento * (1 - regiao))
            limite_max = round(comprimento * 0.5 + 3)
            limite_min = round(comprimento * 0.5 - 3)
        
        # Otimização do primeiro ponto
        range_a = np.arange(ponto_inicial, limite_max + 1, step)
        if len(range_a) > 0:
            pontos_b_fixos = np.full(len(range_a), ponto_final)
            funcoes_a = self._gerar_multiplas_funcoes_otimizada(
                comprimento, range_a, pontos_b_fixos, valor_max, is_coluna
            )
            mse_valores_a = self._calcular_mse_vectorizado(pixels, funcoes_a)
            melhor_idx_a = np.argmin(mse_valores_a)
            melhor_mse_a = mse_valores_a[melhor_idx_a]
            melhor_ponto_a = range_a[melhor_idx_a]
            
            # Early stopping ou otimização do segundo ponto
            if melhor_mse_a < 200:
                mse_final = melhor_mse_a
                melhor_ponto_b = ponto_final
            else:
                range_b = np.arange(ponto_final, limite_min - 1, -step)
                range_b = range_b[range_b > melhor_ponto_a]
                
                if len(range_b) > 0:
                    pontos_a_fixos = np.full(len(range_b), melhor_ponto_a)
                    funcoes_b = self._gerar_multiplas_funcoes_otimizada(
                        comprimento, pontos_a_fixos, range_b, valor_max, is_coluna
                    )
                    mse_valores_b = self._calcular_mse_vectorizado(pixels, funcoes_b)
                    melhor_idx_b = np.argmin(mse_valores_b)
                    mse_final = mse_valores_b[melhor_idx_b]
                    melhor_ponto_b = range_b[melhor_idx_b]
                else:
                    mse_final = melhor_mse_a
                    melhor_ponto_b = ponto_final
        else:
            melhor_ponto_a = ponto_inicial
            melhor_ponto_b = ponto_final
            funcao_inicial = self._gerar_funcao_indicadora(
                comprimento, ponto_inicial, ponto_final, valor_max, is_coluna
            )
            mse_final = self._calcular_mse_vectorizado(pixels, funcao_inicial[np.newaxis, :])[0]
        
        return {
            'pixel_inicio': melhor_ponto_a,
            'pixel_fim': melhor_ponto_b,
            'valor_maximo': valor_max,
            'mse': mse_final,
            'score': mse_final / (255.0 * 255.0)
        }
    
    def _aplicar_parametrizacao(self, imagem_gray, por_colunas=False):
        """Aplica parametrização unificada para linhas ou colunas."""
        altura, largura = imagem_gray.shape
        dimensao = largura if por_colunas else altura
        
        tipo = "colunas" if por_colunas else "linhas"
        print(f"Aplicando {dimensao} funções indicadoras de {tipo}...")
        
        # Pré-alocação
        mascara_final = np.zeros_like(imagem_gray, dtype=np.uint8)
        parametros_todos = [None] * dimensao
        metricas_todos = [None] * dimensao
        vetor_pixels_claros = np.zeros(dimensao, dtype=np.int32)
        
        # Processamento
        for i in range(dimensao):
            if i % (200 if por_colunas else 150) == 0:
                print(f"Processando {tipo[:-1]} {i}/{dimensao} ({100*i/dimensao:.0f}%)")
            
            # Extrair pixels
            pixels = imagem_gray[:, i] if por_colunas else imagem_gray[i, :]
            pixels = pixels.astype(np.float32)
            
            # Calcular métricas e otimizar
            metricas = self._calcular_metricas(pixels, i)
            params = self._otimizar_parametros(pixels, i, por_colunas)
            
            # Calcular pixels claros
            largura_silhueta = params['pixel_fim'] - params['pixel_inicio']
            vetor_pixels_claros[i] = largura_silhueta
            
            # Gerar função otimizada
            funcao_otimizada = self._gerar_funcao_indicadora(
                len(pixels), params['pixel_inicio'], params['pixel_fim'], 
                params['valor_maximo'], por_colunas
            )
            
            # Aplicar threshold
            mse_normalizado = min(1.0, params['mse'] / 1000.0)
            qualidade_ajuste = 1.0 - mse_normalizado
            threshold = np.clip(0.5 + (qualidade_ajuste - 0.5) * 0.2, 0.3, 0.7)
            
            valor_threshold = threshold * np.max(funcao_otimizada)
            mascara = (funcao_otimizada > valor_threshold).astype(np.uint8) * 255
            
            # Suavização simples
            if np.sum(mascara) > 0:
                kernel = np.ones(3) / 3
                mascara_suave = np.convolve(mascara.astype(float), kernel, mode='same')
                mascara = (mascara_suave > 127).astype(np.uint8) * 255
            
            # Armazenar resultados
            if por_colunas:
                mascara_final[:, i] = mascara
            else:
                mascara_final[i, :] = mascara
            
            params.update({
                'threshold_usado': threshold,
                'qualidade_ajuste': qualidade_ajuste
            })
            
            parametros_todos[i] = params
            metricas_todos[i] = metricas
        
        # Estatísticas finais
        mses = np.array([p['mse'] for p in parametros_todos])
        qualidades = np.array([p['qualidade_ajuste'] for p in parametros_todos])
        
        print(f"Parametrização de {tipo} concluída!")
        print(f"MSE global: {np.mean(mses):.2f}")
        print(f"Qualidade global: {np.mean(qualidades):.3f}")
        
        # Estatísticas de pixels claros
        print(f"Dimensão da silhueta - Min: {np.min(vetor_pixels_claros)}, "
              f"Max: {np.max(vetor_pixels_claros)}, Média: {np.mean(vetor_pixels_claros):.1f}")
        
        return mascara_final, parametros_todos, metricas_todos, vetor_pixels_claros
    
    def _combinar_mascaras_linhas_colunas(self, mascara_linhas, mascara_colunas, metodo='intersecao'):
        """Combina máscaras de linhas e colunas."""
        if metodo == 'uniao':
            mascara_combinada = np.logical_or(mascara_linhas > 0, mascara_colunas > 0).astype(np.uint8) * 255
        else:  # intersecao
            mascara_combinada = np.logical_and(mascara_linhas > 0, mascara_colunas > 0).astype(np.uint8) * 255
        
        return mascara_combinada
    
    def _pos_processar(self, mascara):
        """Aplica pós-processamento morfológico otimizado."""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                         (self.morph_kernel_size, self.morph_kernel_size))
        
        # Operações morfológicas combinadas
        mascara_limpa = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        mascara_limpa = cv2.morphologyEx(mascara_limpa, cv2.MORPH_CLOSE, kernel)
        
        # Análise de componentes simplificada
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mascara_limpa)
        
        mascara_final = np.zeros_like(mascara_limpa)
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= self.min_area:
                mascara_final[labels == i] = 255
        
        return mascara_final
    
    def segmentar(self, imagem_path):
        """Segmentação usando funções indicadoras de linhas."""
        try:
            # Carregamento e pré-processamento
            if isinstance(imagem_path, str):
                imagem = cv2.imread(imagem_path)
                if imagem is None:
                    raise ValueError(f"Não foi possível carregar a imagem: {imagem_path}")
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            else:
                imagem = imagem_path
            
            print("Iniciando segmentação por linhas...")
            
            imagem_redimensionada = self._redimensionar_imagem(imagem)
            imagem_gray = self._converter_para_gray(imagem_redimensionada)
            imagem_gray = self._melhorar_contraste(imagem_gray)
            
            # Aplicar parametrização
            mascara_bruta, parametros_linhas, metricas_linhas, vetor_pixels_claros = \
                self._aplicar_parametrizacao(imagem_gray, por_colunas=False)
            
            mascara_final = self._pos_processar(mascara_bruta)
            
            mse_global = np.mean([p['mse'] for p in parametros_linhas])
            
            return {
                'imagem_original': imagem,
                'imagem_redimensionada': imagem_redimensionada,
                'imagem_gray': imagem_gray,
                'mascara_binaria': mascara_final,
                'mascara_bruta': mascara_bruta,
                'parametros_linhas': parametros_linhas,
                'metricas_linhas': metricas_linhas,
                'mse_global': mse_global,
                'vetor_pixels_claros': vetor_pixels_claros,
                'largura_media_silhueta': np.mean(vetor_pixels_claros),
                'largura_min_silhueta': np.min(vetor_pixels_claros),
                'largura_max_silhueta': np.max(vetor_pixels_claros),
                'sucesso': True
            }
            
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}

    def segmentar_por_colunas(self, imagem_path):
        """Segmentação usando funções indicadoras de colunas."""
        try:
            # Carregamento e pré-processamento
            if isinstance(imagem_path, str):
                imagem = cv2.imread(imagem_path)
                if imagem is None:
                    raise ValueError(f"Não foi possível carregar a imagem: {imagem_path}")
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            else:
                imagem = imagem_path
            
            print("Iniciando segmentação por colunas...")
            
            imagem_redimensionada = self._redimensionar_imagem(imagem)
            imagem_gray = self._converter_para_gray(imagem_redimensionada)
            imagem_gray = self._melhorar_contraste(imagem_gray)
            
            # Aplicar parametrização
            mascara_bruta, parametros_colunas, metricas_colunas, vetor_pixels_claros_colunas = \
                self._aplicar_parametrizacao(imagem_gray, por_colunas=True)
            
            mascara_final = self._pos_processar(mascara_bruta)
            
            mse_global = np.mean([p['mse'] for p in parametros_colunas])
            
            return {
                'imagem_original': imagem,
                'imagem_redimensionada': imagem_redimensionada,
                'imagem_gray': imagem_gray,
                'mascara_binaria': mascara_final,
                'mascara_bruta': mascara_bruta,
                'parametros_colunas': parametros_colunas,
                'metricas_colunas': metricas_colunas,
                'vetor_pixels_claros_colunas': vetor_pixels_claros_colunas,
                'mse_global': mse_global,
                'sucesso': True
            }
            
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}

    def segmentar_separado_e_unido(self, imagem_path):
        """Segmentação por linhas e colunas separadamente e depois combinação."""
        try:
            # Carregamento e pré-processamento
            if isinstance(imagem_path, str):
                imagem = cv2.imread(imagem_path)
                if imagem is None:
                    raise ValueError(f"Não foi possível carregar a imagem: {imagem_path}")
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            else:
                imagem = imagem_path
            
            print("Iniciando segmentação separada e união...")
            
            imagem_redimensionada = self._redimensionar_imagem(imagem)
            imagem_gray = self._converter_para_gray(imagem_redimensionada)
            imagem_gray = self._melhorar_contraste(imagem_gray)
            
            # Processamento por linhas
            print("\n=== SEGMENTAÇÃO POR LINHAS ===")
            mascara_linhas, parametros_linhas, metricas_linhas, vetor_pixels_claros = \
                self._aplicar_parametrizacao(imagem_gray, por_colunas=False)
            mascara_linhas_final = self._pos_processar(mascara_linhas)
            
            # Processamento por colunas
            print("\n=== SEGMENTAÇÃO POR COLUNAS ===")
            mascara_colunas, parametros_colunas, metricas_colunas, vetor_pixels_claros_colunas = \
                self._aplicar_parametrizacao(imagem_gray, por_colunas=True)
            mascara_colunas_final = self._pos_processar(mascara_colunas)
            
            # Combinações
            print("\n=== COMBINANDO RESULTADOS ===")
            mascara_uniao = self._combinar_mascaras_linhas_colunas(
                mascara_linhas_final, mascara_colunas_final, 'uniao'
            )
            mascara_uniao_final = self._pos_processar(mascara_uniao)
            
            mascara_intersecao = self._combinar_mascaras_linhas_colunas(
                mascara_linhas_final, mascara_colunas_final, 'intersecao'
            )
            mascara_intersecao_final = self._pos_processar(mascara_intersecao)
            
            # Métricas finais
            mse_global_linhas = np.mean([p['mse'] for p in parametros_linhas])
            mse_global_colunas = np.mean([p['mse'] for p in parametros_colunas])
            mse_global_combinado = (mse_global_linhas + mse_global_colunas) / 2
            
            pixels_linhas = np.sum(mascara_linhas_final > 0)
            pixels_colunas = np.sum(mascara_colunas_final > 0)
            pixels_uniao = np.sum(mascara_uniao_final > 0)
            pixels_intersecao = np.sum(mascara_intersecao_final > 0)
            
            print(f"\nResultados:")
            print(f"Linhas: {pixels_linhas} pixels | MSE: {mse_global_linhas:.2f}")
            print(f"Colunas: {pixels_colunas} pixels | MSE: {mse_global_colunas:.2f}")
            print(f"União: {pixels_uniao} pixels")
            print(f"Intersecção: {pixels_intersecao} pixels")
            
            return {
                'imagem_original': imagem,
                'imagem_redimensionada': imagem_redimensionada,
                'imagem_gray': imagem_gray,
                
                # Resultados separados
                'mascara_linhas_bruta': mascara_linhas,
                'mascara_linhas_final': mascara_linhas_final,
                'mascara_colunas_bruta': mascara_colunas,
                'mascara_colunas_final': mascara_colunas_final,
                
                # Combinações
                'mascara_uniao_bruta': mascara_uniao,
                'mascara_uniao_final': mascara_uniao_final,
                'mascara_intersecao_bruta': mascara_intersecao,
                'mascara_intersecao_final': mascara_intersecao_final,
                'mascara_binaria': mascara_uniao_final,
                
                # Parâmetros e métricas
                'parametros_linhas': parametros_linhas,
                'parametros_colunas': parametros_colunas,
                'metricas_linhas': metricas_linhas,
                'metricas_colunas': metricas_colunas,
                
                # Vetores de pixels claros
                'vetor_pixels_claros': vetor_pixels_claros,
                'vetor_pixels_claros_colunas': vetor_pixels_claros_colunas,
                'largura_media_silhueta': np.mean(vetor_pixels_claros),
                'largura_min_silhueta': np.min(vetor_pixels_claros),
                'largura_max_silhueta': np.max(vetor_pixels_claros),
                'altura_media_silhueta': np.mean(vetor_pixels_claros_colunas),
                'altura_min_silhueta': np.min(vetor_pixels_claros_colunas),
                'altura_max_silhueta': np.max(vetor_pixels_claros_colunas),
                
                # MSE e estatísticas
                'mse_global_linhas': mse_global_linhas,
                'mse_global_colunas': mse_global_colunas,
                'mse_global_combinado': mse_global_combinado,
                'pixels_linhas': pixels_linhas,
                'pixels_colunas': pixels_colunas,
                'pixels_uniao': pixels_uniao,
                'pixels_intersecao': pixels_intersecao,
                'percentual_intersecao_uniao': (pixels_intersecao / pixels_uniao * 100) if pixels_uniao > 0 else 0,
                'percentual_intersecao_linhas': (pixels_intersecao / pixels_linhas * 100) if pixels_linhas > 0 else 0,
                'percentual_intersecao_colunas': (pixels_intersecao / pixels_colunas * 100) if pixels_colunas > 0 else 0,
                
                # Metadata
                'metodo_combinacao': 'separado_e_uniao',
                'tipo_segmentacao': 'separado_e_unido',
                'sucesso': True
            }
            
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}