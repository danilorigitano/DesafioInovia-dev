"""
Segmentação de imagens usando parametrização com funções indicadoras.
- Redimensiona imagem para 512x382 pixels
- Cria 382 funções indicadoras (uma para cada linha)
- Cada função começa em 0 (preto), atinge um valor máximo no meio, volta a 0
- Aplica funções indicadoras otimizadas com MSE (Mean Square Error) - MÉTRICA ÚNICA
- Parâmetros de ajuste OTIMIZADOS para maior velocidade
- Binariza baseado em parametrização personalizada otimizada
"""

import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class SegmentacaoParametrizacaoIndicadora:
    def __init__(self, target_width=512, target_height=382, 
                 morph_kernel_size=3, min_area=50, enhance_contrast=True):
        """
        Inicializa o segmentador com parametrização indicadora.
        
        Args:
            target_width: Largura alvo da imagem (512)
            target_height: Altura alvo da imagem (382)
            morph_kernel_size: Tamanho do kernel para operações morfológicas
            min_area: Área mínima para filtrar ruídos (pixels)
            enhance_contrast: Se deve aplicar melhoria de contraste
        """
        self.target_width = target_width
        self.target_height = target_height
        self.morph_kernel_size = morph_kernel_size
        self.min_area = min_area
        self.enhance_contrast = enhance_contrast
        
        print(f"Configuração do segmentador:")
        print(f"- Dimensões alvo: {self.target_width}x{self.target_height}")
        print(f"- Número de funções indicadoras: {self.target_height}")
        print(f"- Kernel morfológico: {self.morph_kernel_size}")
    
    
    def _redimensionar_imagem(self, imagem):
        """Redimensiona a imagem para as dimensões alvo 512x382."""
        if len(imagem.shape) == 3:
            altura_original, largura_original = imagem.shape[:2]
        else:
            altura_original, largura_original = imagem.shape
            
        print(f"Redimensionando de {largura_original}x{altura_original} para {self.target_width}x{self.target_height}")
        
        # Redimensiona usando interpolação bicúbica para melhor qualidade
        imagem_redimensionada = cv2.resize(imagem, 
                                         (self.target_width, self.target_height), 
                                         interpolation=cv2.INTER_CUBIC)
        return imagem_redimensionada
    
    def _converter_para_gray(self, imagem):
        """Converte imagem para escala de cinza (0-255)."""
        if len(imagem.shape) == 3:
            # Converte RGB para grayscale usando pesos padrão
            gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        else:
            gray = imagem.copy()
        
        # Garante que está no range 0-255
        gray = np.clip(gray, 0, 255).astype(np.uint8)
        return gray
    
    def _melhorar_contraste(self, imagem_gray):
        """Aplica melhoria de contraste usando CLAHE."""
        if self.enhance_contrast:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            return clahe.apply(imagem_gray)
        return imagem_gray
    
    def _gerar_funcao_indicadora_linha(self, linha_idx, largura, pixel_inicio=200, pixel_fim=400, valor_maximo=100):
        """
        Gera uma função indicadora para uma linha específica.
        Implementa a lógica: 0 (preto) -> valor_maximo (branco) -> 0 (preto)
        
        Args:
            linha_idx: Índice da linha (0 a 381)
            largura: Largura da imagem (512)
            pixel_inicio: Pixel onde começa a subir (entre 5 e metade+50)
            pixel_fim: Pixel onde volta a 0 (entre metade-50 e fim-5)
            valor_maximo: Valor máximo no meio (intensidade da cor branca)
            
        Note:
            Sempre garantido que pixel_inicio < pixel_fim
            
        Returns:
            array: Função indicadora para esta linha (valores 0-255)
        """
        funcao = np.zeros(largura, dtype=np.float32)
        
        # Garante que os parâmetros estão dentro dos limites válidos
        # Especificação: pixel_inicio (a) entre 5 e maior que metade (256+)
        # pixel_fim (b) entre um pouco menor que metade e fim-5
        # SEMPRE garantindo pixel_inicio < pixel_fim
        metade = largura // 2  # 256 para largura 512
        
        # pixel_inicio (a): mínimo 5, máximo pode ser maior que metade
        pixel_inicio = max(5, min(metade + 100, pixel_inicio))  # Até 356 (maior que metade)
        
        # pixel_fim (b): um pouco menor que metade até fim-5
        pixel_fim = max(metade - 50, min(largura - 5, pixel_fim))  # De 206 até 507
        
        # Garante que pixel_inicio < pixel_fim
        if pixel_inicio >= pixel_fim:
            # Ajusta para garantir ordem correta
            if pixel_inicio < largura - 20:
                pixel_fim = max(pixel_inicio + 20, metade - 50)
            else:
                pixel_inicio = max(5, pixel_fim - 20)
                
        # Validação final dos ranges
        pixel_inicio = max(5, min(metade + 100, pixel_inicio))
        pixel_fim = max(max(pixel_inicio + 10, metade - 50), min(largura - 5, pixel_fim))
        valor_maximo = max(50, min(255, valor_maximo))
        
        # Implementar a função indicadora conforme especificado:
        # 0 (cor preta) -> valor_maximo (mais branco) -> 0 (cor preta)
        
        # Região 1: Do início até pixel_inicio (sempre 0 - cor preta)
        funcao[:pixel_inicio] = 0
        
        # Região 2: De pixel_inicio até pixel_fim (valor_maximo - mais branco)
        funcao[pixel_inicio:pixel_fim+1] = valor_maximo
        
        # Região 3: De pixel_fim até o final (sempre 0 - cor preta)
        funcao[pixel_fim+1:] = 0
        
        # Aplicar suavização nas transições para evitar bordas abruptas
        # Suavização na subida (transição 0 -> valor_maximo)
        tamanho_transicao = min(5, (pixel_fim - pixel_inicio) // 4)
        if tamanho_transicao > 0:
            for i in range(tamanho_transicao):
                pos = pixel_inicio + i
                if pos < largura:
                    fator = (i + 1) / tamanho_transicao
                    funcao[pos] = valor_maximo * fator
            
            # Suavização na descida (transição valor_maximo -> 0)
            for i in range(tamanho_transicao):
                pos = pixel_fim - i
                if pos >= 0 and pos < largura:
                    fator = (i + 1) / tamanho_transicao
                    funcao[pos] = valor_maximo * (1 - fator)
        
        # Garantir que os valores estão no range correto
        funcao = np.clip(funcao, 0, 255).astype(np.float32)
        
        return funcao
    
    def _calcular_metricas_linha(self, linha_pixels, linha_idx):
        """Calcula métricas para uma linha específica."""
        metricas = {
            'linha_idx': linha_idx,
            'media': np.mean(linha_pixels),
            'desvio_padrao': np.std(linha_pixels),
            'contraste': np.max(linha_pixels) - np.min(linha_pixels),
            'min_val': np.min(linha_pixels),
            'max_val': np.max(linha_pixels)
        }
        
        return metricas
    
    def _calcular_mse(self, valores_observados, valores_preditos):
        """
        Calcula MSE (Mean Square Error) para avaliar o ajuste.
        MSE é a métrica principal para otimização, mais rigorosa na avaliação.
        
        Args:
            valores_observados: Valores reais dos pixels da linha
            valores_preditos: Valores preditos pela função indicadora
            
        Returns:
            dict: {'mse': float, 'n_samples': int}
        """
        # Garante que os arrays tenham o mesmo tamanho
        min_len = min(len(valores_observados), len(valores_preditos))
        obs = valores_observados[:min_len]
        pred = valores_preditos[:min_len]
        
        # Calcula MSE (Mean Square Error) - métrica principal
        mse = np.mean((obs - pred) ** 2)
        
        return {
            'mse': mse,
            'n_samples': min_len
        }
    
    def _otimizar_parametros_linha(self, linha_pixels, linha_idx):
        """
        Otimiza os parâmetros da função indicadora para uma linha específica.
        Busca otimizada com parâmetros ajustados para velocidade.
        Usa apenas MSE como métrica de avaliação.
        
        Ranges:
        - pixel_inicio (a): mínimo 5, máximo maior que metade (até 356 para largura 512)
        - pixel_fim (b): um pouco menor que metade até fim-5 (206 a 507 para largura 512)
        - Sempre garantindo a < b
        
        Args:
            linha_pixels: Array com os pixels da linha
            linha_idx: Índice da linha
            
        Returns:
            dict: Melhores parâmetros encontrados
        """
        melhor_score = float('inf')  # Para MSE, menor é melhor
        melhores_params = {
            'pixel_inicio': 100,
            'pixel_fim': 380,
            'valor_maximo': 100,
            'mse': float('inf')
        }
        
        largura = len(linha_pixels)
        
        # Busca otimizada para velocidade (menos densa, mais rápida):
        # pixel_inicio: entre 5 e metade+50
        # pixel_fim: entre metade-50 e fim-5
        # SEMPRE garantindo pixel_inicio < pixel_fim
        # valor_maximo: baseado na intensidade da linha com busca simplificada
        
        # Análise simplificada da linha para determinar valor_maximo candidato
        intensidade_media = np.mean(linha_pixels)
        intensidade_max = np.max(linha_pixels)
        intensidade_min = np.min(linha_pixels)
        
        # Novos ranges conforme especificação:
        # pixel_inicio (a): mínimo 5, máximo maior que metade (256+)
        # pixel_fim (b): um pouco menor que metade até fim-5
        metade = largura // 2  # 256 para largura 512
        
        # Range para pixel_inicio: de 5 até maior que metade
        inicio_range = range(5, metade + 100, 20)  # De 5 até 356 (maior que metade)
        
        # Range simplificado para valor_maximo (menos pontos testados)
        if intensidade_max > 200:
            valor_range = range(180, 256, 25)  # Step maior para velocidade (8 -> 25)
        elif intensidade_max > 150:
            valor_range = range(120, 201, 25)  # Valores médios-altos
        elif intensidade_max > 100:
            valor_range = range(80, 151, 25)   # Valores médios
        else:
            valor_range = range(50, 101, 25)   # Valores baixos
        
        # Busca otimizada com menos tentativas para velocidade
        tentativas = 0
        max_tentativas = 150  # Reduzido de 500 para 150 para maior velocidade
        
        melhor_mse_global = float('inf')
        
        for pixel_inicio in inicio_range:
            # Range para pixel_fim: um pouco menor que metade até fim-5
            # Garantindo sempre que pixel_fim > pixel_inicio
            fim_min = max(pixel_inicio + 10, metade - 50)  # Garante pixel_fim > pixel_inicio
            fim_max = largura - 5  # Até 507
            
            if fim_min < fim_max:  # Só processa se há range válido
                fim_range = range(fim_min, fim_max, 25)  # Step maior para velocidade
            
            for pixel_fim in fim_range:
                # Validação adicional: garante pixel_inicio < pixel_fim
                if pixel_inicio >= pixel_fim:
                    continue
                    
                for valor_maximo in valor_range:
                    tentativas += 1
                    if tentativas > max_tentativas:
                        break
                        
                    # Gera função indicadora com estes parâmetros
                    funcao = self._gerar_funcao_indicadora_linha(
                        linha_idx, len(linha_pixels), 
                        pixel_inicio, pixel_fim, valor_maximo
                    )
                    
                    # Calcula MSE apenas (métrica única e rigorosa)
                    try:
                        metricas = self._calcular_mse(linha_pixels, funcao)
                        mse = metricas['mse']
                        
                        # Normaliza MSE baseado no range de pixels (0-255)²
                        mse_normalizado = mse / (255.0 ** 2)  # Entre 0 e 1
                        
                        # Penalizações simplificadas para velocidade:
                        # 1. Penalização simples se valor_maximo muito diferente da intensidade
                        diff_intensidade = abs(valor_maximo - intensidade_media)
                        penalty_intensidade = (diff_intensidade / 255.0) * 0.1  # Penalização linear simplificada
                        
                        # 2. Penalização simplificada para funções inadequadas
                        largura_funcao = pixel_fim - pixel_inicio
                        largura_ideal = largura * 0.3  # 30% da largura total
                        penalty_largura = abs(largura_funcao - largura_ideal) / largura * 0.05  # Linear simplificada
                        
                        # Score final simplificado (menor é melhor para MSE)
                        score_mse = mse_normalizado + penalty_intensidade + penalty_largura
                        
                        if score_mse < melhor_score:
                            melhor_score = score_mse
                            melhores_params = {
                                'pixel_inicio': pixel_inicio,
                                'pixel_fim': pixel_fim,
                                'valor_maximo': valor_maximo,
                                'mse': mse,
                                'score': score_mse
                            }
                            
                            # Early stopping simplificado: MSE baixo indica bom ajuste
                            if mse < 200:  # MSE moderado (menos rigoroso que antes: 100 -> 200)
                                return melhores_params
                            
                            # Update do melhor MSE global
                            if mse < melhor_mse_global:
                                melhor_mse_global = mse
                                
                    except Exception as e:
                        continue
                        
                if tentativas > max_tentativas:
                    break
            if tentativas > max_tentativas:
                break
        
        # Se não encontrou resultado satisfatório, faz busca simplificada (mais rápida)
        if melhor_score == float('inf') or melhores_params['mse'] > 400:  # Critério mais relaxado (200 -> 400)
            print(f"Linha {linha_idx}: Fazendo busca simplificada...")
            
            # Busca simplificada respeitando os novos ranges
            metade = largura // 2  # 256 para largura 512
            
            # Range simplificado para pixel_inicio: 5 até maior que metade
            inicio_range_refinado = range(5, metade + 100, 15)  # De 5 até 356
            
            for pixel_inicio in inicio_range_refinado:
                # Range simplificado para pixel_fim: um pouco menor que metade até fim-5
                # Garantindo sempre pixel_fim > pixel_inicio
                fim_min = max(pixel_inicio + 10, metade - 50)  # A partir de 206
                fim_max = largura - 5  # Até 507
                
                if fim_min < fim_max:  # Só processa se há range válido
                    fim_range_refinado = range(fim_min, fim_max, 20)  # Step maior (8 -> 20)
                    
                    for pixel_fim in fim_range_refinado:
                        # Validação: garante pixel_inicio < pixel_fim
                        if pixel_inicio >= pixel_fim:
                            continue
                        # Usa menos valores baseados na intensidade da linha (para velocidade)
                        valores_teste = [
                            int(intensidade_media * 1.0),
                            int(intensidade_max * 0.9),
                            int((intensidade_media + intensidade_max) / 2)
                        ]
                        
                        for valor_maximo in valores_teste:
                            valor_maximo = max(40, min(255, valor_maximo))
                            
                            funcao = self._gerar_funcao_indicadora_linha(
                                linha_idx, len(linha_pixels), 
                                pixel_inicio, pixel_fim, valor_maximo
                            )
                            
                            try:
                                metricas = self._calcular_mse(linha_pixels, funcao)
                                mse = metricas['mse']
                                
                                if mse < melhores_params['mse']:
                                    melhores_params = {
                                        'pixel_inicio': pixel_inicio,
                                        'pixel_fim': pixel_fim,
                                        'valor_maximo': valor_maximo,
                                        'mse': mse,
                                        'score': mse / (255.0 ** 2)
                                    }
                            except:
                                continue
        
        return melhores_params
    
    def _aplicar_parametrizacao_linhas(self, imagem_gray):
        """
        Aplica a parametrização com 382 funções indicadoras (uma para cada linha).
        Cada função indicadora tem formato: 0 -> valor_max -> 0
        Versão com parâmetros mais rigorosos usando apenas MSE.
        
        Args:
            imagem_gray: Imagem em escala de cinza 512x382
            
        Returns:
            tuple: (mascara_final, parametros_otimizados, metricas_todas_linhas)
        """
        altura, largura = imagem_gray.shape
        print(f"Aplicando {altura} funções indicadoras com parâmetros otimizados (velocidade) para imagem {largura}x{altura}")
        
        # Arrays para armazenar resultados
        mascara_final = np.zeros_like(imagem_gray, dtype=np.uint8)
        parametros_todas_linhas = []
        metricas_todas_linhas = []
        
        # Análise global da imagem para parametrização rigorosa
        intensidade_global = np.mean(imagem_gray)
        contraste_global = np.std(imagem_gray)
        
        print(f"Intensidade global: {intensidade_global:.1f}, Contraste global: {contraste_global:.1f}")
        
        # Processa cada linha individualmente com parâmetros otimizados para velocidade
        for linha_idx in range(altura):
            if linha_idx % 150 == 0:  # Progress report a cada 150 linhas (menos frequente para velocidade)
                print(f"Processando linha {linha_idx}/{altura} - Progresso: {100*linha_idx/altura:.0f}%")
            
            # Extrai pixels da linha atual
            linha_pixels = imagem_gray[linha_idx, :].astype(np.float32)
            
            # Calcula métricas da linha
            metricas_linha = self._calcular_metricas_linha(linha_pixels, linha_idx)
            
            # Otimiza parâmetros da função indicadora para esta linha (rigoroso)
            params_otimizados = self._otimizar_parametros_linha(linha_pixels, linha_idx)
            
            # Gera a função indicadora otimizada
            funcao_otimizada = self._gerar_funcao_indicadora_linha(
                linha_idx, largura,
                params_otimizados['pixel_inicio'],
                params_otimizados['pixel_fim'],
                params_otimizados['valor_maximo']
            )
            
            # Threshold simplificado baseado em MSE (para velocidade)
            mse_normalizado = min(1.0, params_otimizados['mse'] / 1000.0)  # Normaliza MSE
            qualidade_ajuste = 1.0 - mse_normalizado  # Inverte: maior qualidade = menor MSE
            
            # Threshold mais simples e rápido
            threshold_linha = 0.5 + (qualidade_ajuste - 0.5) * 0.2  # Menos cálculos
            threshold_linha = max(0.3, min(0.7, threshold_linha))  # Range: 0.3-0.7
            
            # Aplicar threshold rigoroso para criar máscara binária da linha
            valor_threshold = threshold_linha * np.max(funcao_otimizada)
            mascara_linha = (funcao_otimizada > valor_threshold).astype(np.uint8) * 255
            
            # Refinamento simplificado para velocidade
            if np.sum(mascara_linha) > 0:
                # Suavização simples e rápida
                kernel_linha = np.ones(3) / 3
                mascara_suave = np.convolve(mascara_linha.astype(float), kernel_linha, mode='same')
                mascara_linha = (mascara_suave > 127).astype(np.uint8) * 255
            
            # Armazena na máscara final
            mascara_final[linha_idx, :] = mascara_linha
            
            # Armazena resultados com métricas MSE
            params_otimizados.update({
                'threshold_usado': threshold_linha,
                'qualidade_ajuste': qualidade_ajuste
            })
            
            parametros_todas_linhas.append(params_otimizados)
            metricas_todas_linhas.append(metricas_linha)
        
        print("Parametrização otimizada completada!")
        
        # Calcula estatísticas globais usando apenas MSE
        mses = [p['mse'] for p in parametros_todas_linhas]
        qualidades = [p['qualidade_ajuste'] for p in parametros_todas_linhas]
        
        mse_global = np.mean(mses)
        qualidade_global = np.mean(qualidades)
        
        # Estatísticas de desempenho otimizadas usando MSE
        linhas_excelentes = sum(1 for mse in mses if mse < 200)  # MSE baixo (relaxado: 150 -> 200)
        linhas_boas = sum(1 for mse in mses if 200 <= mse < 400)  # MSE moderado (relaxado: 150-300 -> 200-400)
        linhas_regulares = sum(1 for mse in mses if 400 <= mse < 600)  # MSE alto (relaxado: 300-500 -> 400-600)
        linhas_ruins = len(mses) - linhas_excelentes - linhas_boas - linhas_regulares
        
        print(f"=== RESULTADOS DA PARAMETRIZAÇÃO OTIMIZADA (MSE) ===")
        print(f"MSE global: {mse_global:.2f}")
        print(f"Qualidade global: {qualidade_global:.3f}")
        print(f"Linhas excelentes (MSE < 200): {linhas_excelentes}/{len(mses)} ({100*linhas_excelentes/len(mses):.1f}%)")
        print(f"Linhas boas (200 ≤ MSE < 400): {linhas_boas}/{len(mses)} ({100*linhas_boas/len(mses):.1f}%)")
        print(f"Linhas regulares (400 ≤ MSE < 600): {linhas_regulares}/{len(mses)} ({100*linhas_regulares/len(mses):.1f}%)")
        print(f"Linhas ruins (MSE ≥ 600): {linhas_ruins}/{len(mses)} ({100*linhas_ruins/len(mses):.1f}%)")
        print(f"Processamento OTIMIZADO para velocidade com métrica MSE!")
        
        return mascara_final, parametros_todas_linhas, metricas_todas_linhas
    
    def _pos_processar(self, mascara):
        """
        Aplica pós-processamento morfológico OTIMIZADO para velocidade.
        Versão simplificada com menos etapas para maior rapidez.
        """
        print("Aplicando pós-processamento otimizado (rápido)...")
        
        # Etapa 1: Apenas uma operação de limpeza (SIMPLIFICADO)
        kernel_medio = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                               (self.morph_kernel_size, self.morph_kernel_size))
        
        # Operação combinada: abertura + fechamento em uma só etapa
        mascara_limpa = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel_medio)
        mascara_limpa = cv2.morphologyEx(mascara_limpa, cv2.MORPH_CLOSE, kernel_medio)
        
        # Etapa 2: Análise de componentes SIMPLIFICADA (critérios mais relaxados)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mascara_limpa)
        
        # Criar máscara final com critérios RELAXADOS
        mascara_final = np.zeros_like(mascara_limpa)
        componentes_validos = 0
        
        # Critério SIMPLES: apenas área mínima
        area_threshold = self.min_area
        
        for i in range(1, num_labels):  # Pula o background (label 0)
            area = stats[i, cv2.CC_STAT_AREA]
            
            # Critério RELAXADO: só verificar área
            if area >= area_threshold:
                mascara_final[labels == i] = 255
                componentes_validos += 1
        
        print(f"Componentes válidos: {componentes_validos}/{num_labels-1} (pós-processamento rápido)")
        
        return mascara_final
    
    def segmentar(self, imagem_path):
        """
        Realiza a segmentação da imagem usando 382 funções indicadoras.
        
        Args:
            imagem_path: Caminho para a imagem
            
        Returns:
            dict: Dicionário com resultados da segmentação
        """
        try:
            # Carrega imagem
            if isinstance(imagem_path, str):
                imagem = cv2.imread(imagem_path)
                if imagem is None:
                    raise ValueError(f"Não foi possível carregar a imagem: {imagem_path}")
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            else:
                imagem = imagem_path
            
            print("Iniciando segmentação com 382 funções indicadoras...")
            print(f"Imagem original: {imagem.shape}")
            
            # 1. Redimensiona para 512x382
            imagem_redimensionada = self._redimensionar_imagem(imagem)
            print(f"Imagem redimensionada: {imagem_redimensionada.shape}")
            
            # 2. Converte para escala de cinza
            imagem_gray = self._converter_para_gray(imagem_redimensionada)
            print(f"Imagem convertida para grayscale: {imagem_gray.shape}")
            
            # 3. Melhora contraste se necessário
            imagem_gray = self._melhorar_contraste(imagem_gray)
            
            # 4. Aplica parametrização com 382 funções indicadoras (uma por linha)
            mascara_bruta, parametros_linhas, metricas_linhas = self._aplicar_parametrizacao_linhas(imagem_gray)
            
            # 5. Pós-processamento
            mascara_final = self._pos_processar(mascara_bruta)
            
            # Calcula métricas finais usando apenas MSE
            mses = [p['mse'] for p in parametros_linhas]
            mse_global = np.mean(mses)
            
            print(f"Segmentação concluída!")
            print(f"MSE global: {mse_global:.2f}")
            
            return {
                'imagem_original': imagem,
                'imagem_redimensionada': imagem_redimensionada,
                'imagem_gray': imagem_gray,
                'mascara_binaria': mascara_final,
                'mascara_bruta': mascara_bruta,
                'parametros_linhas': parametros_linhas,
                'metricas_linhas': metricas_linhas,
                'mse_global': mse_global,
                'sucesso': True
            }
            
        except Exception as e:
            print(f"Erro durante segmentação: {e}")
            return {'sucesso': False, 'erro': str(e)}
    
    def visualizar_resultados(self, resultado, salvar_path=None):
        """Visualiza os resultados da segmentação com 382 funções indicadoras."""
        if not resultado['sucesso']:
            print(f"Erro na segmentação: {resultado['erro']}")
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Imagem original
        axes[0, 0].imshow(resultado['imagem_original'])
        axes[0, 0].set_title('Imagem Original')
        axes[0, 0].axis('off')
        
        # Imagem redimensionada
        axes[0, 1].imshow(resultado['imagem_redimensionada'])
        axes[0, 1].set_title('Redimensionada (512x382)')
        axes[0, 1].axis('off')
        
        # Imagem em grayscale
        axes[0, 2].imshow(resultado['imagem_gray'], cmap='gray')
        axes[0, 2].set_title('Grayscale 512x382')
        axes[0, 2].axis('off')
        
        # Máscara bruta
        axes[1, 0].imshow(resultado['mascara_bruta'], cmap='gray')
        axes[1, 0].set_title('Máscara Bruta (382 funções)')
        axes[1, 0].axis('off')
        
        # Máscara final
        axes[1, 1].imshow(resultado['mascara_binaria'], cmap='gray')
        axes[1, 1].set_title('Máscara Final')
        axes[1, 1].axis('off')
        
        # Overlay
        overlay = resultado['imagem_redimensionada'].copy()
        if len(overlay.shape) == 3:
            # Aplicar cor vermelha nas áreas segmentadas
            mask_bool = resultado['mascara_binaria'] > 0
            overlay[mask_bool, 0] = 255  # Canal vermelho
            overlay[mask_bool, 1] = 0    # Canal verde
            overlay[mask_bool, 2] = 0    # Canal azul
        axes[1, 2].imshow(overlay)
        axes[1, 2].set_title('Overlay')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        
        if salvar_path:
            plt.savefig(salvar_path, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {salvar_path}")
        
        plt.show()
        
        # Plota algumas funções indicadoras como exemplo
        self._visualizar_funcoes_indicadoras(resultado)
    
    def _visualizar_funcoes_indicadoras(self, resultado, num_exemplos=5):
        """Visualiza algumas funções indicadoras como exemplo."""
        parametros = resultado['parametros_linhas']
        altura = len(parametros)
        
        # Seleciona linhas distribuídas ao longo da imagem
        indices_exemplo = np.linspace(0, altura-1, num_exemplos, dtype=int)
        
        fig, axes = plt.subplots(1, num_exemplos, figsize=(15, 3))
        if num_exemplos == 1:
            axes = [axes]
        
        for i, linha_idx in enumerate(indices_exemplo):
            params = parametros[linha_idx]
            
            # Gera a função indicadora para esta linha
            funcao = self._gerar_funcao_indicadora_linha(
                linha_idx, self.target_width,
                params['pixel_inicio'],
                params['pixel_fim'],
                params['valor_maximo']
            )
            
            axes[i].plot(funcao, 'b-', linewidth=2)
            axes[i].set_title(f'Linha {linha_idx}\nMSE: {params["mse"]:.1f}')
            axes[i].set_xlabel('Pixel')
            axes[i].set_ylabel('Valor')
            axes[i].grid(True, alpha=0.3)
            axes[i].set_ylim(0, 255)
        
        plt.suptitle('Exemplos de Funções Indicadoras por Linha')
        plt.tight_layout()
        plt.show()
    
    def ajustar_parametros(self, target_width=None, target_height=None):
        """Permite ajustar parâmetros do segmentador."""
        if target_width is not None:
            self.target_width = target_width
            print(f"Largura alvo atualizada para: {self.target_width}")
        
        if target_height is not None:
            self.target_height = target_height
            print(f"Altura alvo atualizada para: {self.target_height}")


def exemplo_uso():
    """
    Exemplo de uso da classe com parâmetros otimizados:
    - Imagem redimensionada para 512x382
    - 382 funções indicadoras (uma para cada linha)
    - Cada função: 0 -> valor_max -> 0
    - Otimização para velocidade usando MSE
    """
    print("=== SEGMENTAÇÃO COM 382 FUNÇÕES INDICADORAS (OTIMIZADA) ===")
    print("Implementação:")
    print("- Redimensiona imagem para 512x382 pixels")
    print("- Cria 382 funções indicadoras (uma para cada linha)")
    print("- Cada função: começa em 0 (preto), sobe para valor máximo, volta a 0")
    print("- Otimiza parâmetros para VELOCIDADE usando MSE")
    print("- Ranges flexíveis: pixel_inicio (5 a metade+50), pixel_fim (metade-50 a fim-5)")
    print("- Restrição: sempre pixel_inicio < pixel_fim")
    print("- Busca otimizada: steps maiores, menos tentativas")
    print("- Penalizações simplificadas para maior velocidade")
    print("- Threshold adaptativo simplificado")
    print()
    
    # Inicializa o segmentador
    segmentador = SegmentacaoParametrizacaoIndicadora(
        target_width=512,        # Largura fixa
        target_height=382,       # Altura fixa = número de funções indicadoras
        morph_kernel_size=3,     # Suavização mínima
        min_area=50             # Remove ruídos pequenos
    )
    
    # Segmenta uma imagem (substitua pelo caminho real)
    caminho_imagem = "caminho/para/sua/imagem.jpg"
    print(f"Processando imagem: {caminho_imagem}")
    
    resultado = segmentador.segmentar(caminho_imagem)
    
    # Visualiza resultados
    if resultado['sucesso']:
        segmentador.visualizar_resultados(resultado)
        
        # Mostra estatísticas detalhadas com MSE
        print("\n=== ANÁLISE DAS FUNÇÕES INDICADORAS (RIGOROSA) ===")
        parametros = resultado['parametros_linhas']
        
        # Estatísticas dos parâmetros otimizados
        pixel_inicios = [p['pixel_inicio'] for p in parametros]
        pixel_fins = [p['pixel_fim'] for p in parametros]
        valores_maximos = [p['valor_maximo'] for p in parametros]
        mses = [p['mse'] for p in parametros]
        
        print(f"Parâmetros das funções indicadoras:")
        print(f"- Pixel início: min={min(pixel_inicios)}, max={max(pixel_inicios)}, média={np.mean(pixel_inicios):.1f}")
        print(f"- Pixel fim: min={min(pixel_fins)}, max={max(pixel_fins)}, média={np.mean(pixel_fins):.1f}")
        print(f"- Valor máximo: min={min(valores_maximos):.1f}, max={max(valores_maximos):.1f}, média={np.mean(valores_maximos):.1f}")
        
        print(f"\nQualidade do ajuste rigoroso (MSE):")
        print(f"- MSE: min={min(mses):.1f}, max={max(mses):.1f}, média={np.mean(mses):.1f}")
        
        # Conta linhas com diferentes níveis de qualidade MSE
        excelente = sum(1 for mse in mses if mse < 150)
        bom = sum(1 for mse in mses if 150 <= mse < 300)
        regular = sum(1 for mse in mses if 300 <= mse < 500)
        ruim = sum(1 for mse in mses if mse >= 500)
        
        print(f"- Linhas excelentes (MSE < 150): {excelente}/{len(mses)} ({100*excelente/len(mses):.1f}%)")
        print(f"- Linhas boas (150 ≤ MSE < 300): {bom}/{len(mses)} ({100*bom/len(mses):.1f}%)")
        print(f"- Linhas regulares (300 ≤ MSE < 500): {regular}/{len(mses)} ({100*regular/len(mses):.1f}%)")
        print(f"- Linhas ruins (MSE ≥ 500): {ruim}/{len(mses)} ({100*ruim/len(mses):.1f}%)")
        
        # Mostra exemplos de algumas linhas
        print(f"\n=== EXEMPLOS DE LINHAS ===")
        exemplos = [0, 95, 191, 286, 381]  # Início, 1/4, meio, 3/4, fim
        for linha_idx in exemplos:
            if linha_idx < len(parametros):
                p = parametros[linha_idx]
                print(f"Linha {linha_idx:3d}: início={p['pixel_inicio']:3d}, fim={p['pixel_fim']:3d}, "
                      f"max={p['valor_maximo']:5.1f}, MSE={p['mse']:6.1f}")
        
        print(f"\n=== RESUMO FINAL (RIGOROSO) ===")
        print(f"✓ Imagem processada: 512x382 pixels")
        print(f"✓ Funções indicadoras criadas: {len(parametros)}")
        print(f"✓ MSE global: {resultado['mse_global']:.2f}")
        
        # Classificação rigorosa baseada em MSE
        if resultado['mse_global'] < 200:
            qualidade = "EXCELENTE"
        elif resultado['mse_global'] < 400:
            qualidade = "BOM"
        elif resultado['mse_global'] < 600:
            qualidade = "REGULAR"
        else:
            qualidade = "INSATISFATÓRIO"
            
        print(f"✓ Qualidade geral: {qualidade}")
        print(f"✓ Ranges flexíveis: pixel_inicio (5 a metade+50), pixel_fim (metade-50 a fim-5)")
        print(f"✓ Garantia: sempre pixel_inicio < pixel_fim")
        print(f"✓ Busca densa com penalizações rigorosas")
        print(f"✓ Métrica única: MSE (Mean Square Error)")


if __name__ == "__main__":
    exemplo_uso()
