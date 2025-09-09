"""
Segmentação semântica da pessoa na imagem.
- Usa modelo DeepLabV3 pré-treinado do torchvision.
- Retorna a máscara binária da pessoa (silhueta) e a imagem original.
"""

import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt


class SegmentacaoDeepLabV3:
    def __init__(self, device=None, confidence_threshold=0.5, min_area=100, 
                 morph_kernel_size=5, target_size=None, enhance_contrast=True,
                 contrast_factor=1.5, brightness_factor=1.0, gamma_correction=1.0):
        """
        Inicializa o modelo DeepLabV3 com backbone ResNet50.
        
        Args:
            device: Device para execução ('cuda' ou 'cpu'). Se None, detecta automaticamente.
            confidence_threshold: Threshold de confiança para detecção (0.1 - 0.9)
            min_area: Área mínima para filtrar ruídos (pixels)
            morph_kernel_size: Tamanho do kernel para operações morfológicas
            target_size: Tamanho alvo para redimensionamento (width, height) ou None
            enhance_contrast: Se deve aplicar melhoria de contraste
            contrast_factor: Fator de contraste (1.0 = normal, >1.0 = mais contraste)
            brightness_factor: Fator de brilho (1.0 = normal)
            gamma_correction: Correção gamma (1.0 = normal, <1.0 = mais claro, >1.0 = mais escuro)
        """
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        # Hiperparâmetros ajustáveis
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.morph_kernel_size = morph_kernel_size
        self.target_size = target_size
        self.enhance_contrast = enhance_contrast
        self.contrast_factor = contrast_factor
        self.brightness_factor = brightness_factor
        self.gamma_correction = gamma_correction
        
        print(f"Usando device: {self.device}")
        print(f"Confidence threshold: {self.confidence_threshold}")
        print(f"Área mínima: {self.min_area} pixels")
        print(f"Kernel morfológico: {self.morph_kernel_size}x{self.morph_kernel_size}")
        if self.enhance_contrast:
            print(f"Melhoria de contraste ativada:")
            print(f"  - Fator de contraste: {self.contrast_factor}")
            print(f"  - Fator de brilho: {self.brightness_factor}")
            print(f"  - Correção gamma: {self.gamma_correction}")
        
        # Carrega o modelo DeepLabV3 pré-treinado com backbone ResNet50
        self.model = models.segmentation.deeplabv3_resnet50(pretrained=True)
        self.model.to(self.device)
        self.model.eval()
        
        # Transformações de pré-processamento
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Classe 15 no COCO dataset corresponde à "person"
        self.PERSON_CLASS = 15
    
    def melhorar_contraste(self, imagem):
        """
        Aplica técnicas de melhoria de contraste na imagem.
        
        Args:
            imagem: PIL Image
            
        Returns:
            PIL Image: Imagem com contraste melhorado
        """
        if not self.enhance_contrast:
            return imagem
        
        # Converte para numpy para processamento
        img_array = np.array(imagem, dtype=np.float32)
        
        # 1. Correção Gamma
        if self.gamma_correction != 1.0:
            img_array = img_array / 255.0
            img_array = np.power(img_array, self.gamma_correction)
            img_array = img_array * 255.0
        
        # 2. Ajuste de contraste e brilho
        img_array = img_array * self.contrast_factor + (self.brightness_factor - 1.0) * 128
        
        # 3. Equalização de histograma adaptativa (CLAHE)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        # Aplicar CLAHE em cada canal de cor
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        if len(img_array.shape) == 3:  # Imagem colorida
            lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
            lab[:,:,0] = clahe.apply(lab[:,:,0])
            img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        else:  # Imagem em escala de cinza
            img_array = clahe.apply(img_array)
        
        # 4. Sharpening (afiação) para destacar bordas
        kernel = np.array([[-1,-1,-1], 
                          [-1, 9,-1], 
                          [-1,-1,-1]])
        if len(img_array.shape) == 3:
            sharpened = cv2.filter2D(img_array, -1, kernel)
            img_array = cv2.addWeighted(img_array, 0.7, sharpened, 0.3, 0)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def preprocessar_imagem(self, imagem):
        """
        Pré-processa a imagem para o modelo.
        
        Args:
            imagem: PIL Image ou numpy array
            
        Returns:
            tensor: Tensor pré-processado
            original_size: Tamanho original da imagem
            process_size: Tamanho usado para processamento
        """
        if isinstance(imagem, np.ndarray):
            imagem = Image.fromarray(imagem)
        
        original_size = imagem.size
        
        # Aplica melhoria de contraste antes do redimensionamento
        imagem = self.melhorar_contraste(imagem)
        
        process_size = original_size
        
        # Redimensiona se target_size foi especificado
        if self.target_size is not None:
            imagem = imagem.resize(self.target_size, Image.BILINEAR)
            process_size = self.target_size
        
        # Aplica as transformações
        input_tensor = self.transform(imagem)
        input_batch = input_tensor.unsqueeze(0).to(self.device)
        
        return input_batch, original_size, process_size
    
    def pos_processar_mascara(self, mascara_pessoa):
        """
        Aplica pós-processamento na máscara para melhorar a qualidade.
        
        Args:
            mascara_pessoa: Máscara binária inicial
            
        Returns:
            numpy array: Máscara pós-processada
        """
        # Filtro de abertura para remover ruído pequeno
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                               (self.morph_kernel_size, self.morph_kernel_size))
        mascara_pessoa = cv2.morphologyEx(mascara_pessoa, cv2.MORPH_OPEN, kernel_open)
        
        # Filtro de fechamento para preencher buracos
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                                (self.morph_kernel_size * 2, self.morph_kernel_size * 2))
        mascara_pessoa = cv2.morphologyEx(mascara_pessoa, cv2.MORPH_CLOSE, kernel_close)
        
        # Filtrar componentes conectados por área mínima
        if self.min_area > 0:
            # Encontrar componentes conectados
            num_labels, labels = cv2.connectedComponents(mascara_pessoa)
            
            # Calcular área de cada componente
            for label in range(1, num_labels):  # Ignorar fundo (label 0)
                component_area = np.sum(labels == label)
                if component_area < self.min_area:
                    mascara_pessoa[labels == label] = 0
        
        return mascara_pessoa
    
    def segmentar_pessoa(self, imagem_path):
        """
        Realiza a segmentação semântica para detectar pessoas na imagem.
        
        Args:
            imagem_path: Caminho para a imagem
            
        Returns:
            tuple: (imagem_original, mascara_pessoa)
                - imagem_original: Imagem original como numpy array
                - mascara_pessoa: Máscara binária da pessoa (0 ou 255)
        """
        # Carrega a imagem
        imagem = Image.open(imagem_path).convert('RGB')
        imagem_original = np.array(imagem)
        
        # Pré-processa a imagem
        input_batch, original_size, process_size = self.preprocessar_imagem(imagem)
        
        # Realiza a inferência
        with torch.no_grad():
            output = self.model(input_batch)['out'][0]
        
        # Aplica softmax para obter probabilidades
        output_softmax = torch.softmax(output, dim=0)
        person_confidence = output_softmax[self.PERSON_CLASS]
        
        # Aplica threshold de confiança
        mascara_pessoa = (person_confidence > self.confidence_threshold).cpu().numpy().astype(np.uint8)
        
        # Redimensiona a máscara para o tamanho original
        mascara_pessoa = cv2.resize(mascara_pessoa, original_size, interpolation=cv2.INTER_NEAREST)
        
        # Aplica pós-processamento
        mascara_pessoa = self.pos_processar_mascara(mascara_pessoa)
        
        # Converte para valores 0-255
        mascara_pessoa = mascara_pessoa * 255
        
        return imagem_original, mascara_pessoa
    
    def aplicar_mascara(self, imagem_original, mascara_pessoa, alpha=0.7):
        """
        Aplica a máscara sobre a imagem original para visualização.
        
        Args:
            imagem_original: Imagem original
            mascara_pessoa: Máscara binária da pessoa
            alpha: Transparência da máscara
            
        Returns:
            numpy array: Imagem com máscara aplicada
        """
        # Cria uma versão colorida da máscara
        mascara_colorida = np.zeros_like(imagem_original)
        mascara_colorida[mascara_pessoa > 0] = [0, 255, 0]  # Verde para pessoa
        
        # Aplica a máscara com transparência
        imagem_com_mascara = cv2.addWeighted(imagem_original, 1-alpha, mascara_colorida, alpha, 0)
        
        return imagem_com_mascara
    
    def extrair_silhueta(self, imagem_original, mascara_pessoa):
        """
        Extrai apenas a silhueta da pessoa da imagem original.
        
        Args:
            imagem_original: Imagem original
            mascara_pessoa: Máscara binária da pessoa
            
        Returns:
            numpy array: Imagem apenas com a pessoa (fundo transparente/preto)
        """
        # Cria uma imagem com 4 canais (RGBA)
        silhueta = np.zeros((imagem_original.shape[0], imagem_original.shape[1], 4), dtype=np.uint8)
        
        # Copia os pixels da pessoa
        silhueta[mascara_pessoa > 0] = np.concatenate([
            imagem_original[mascara_pessoa > 0], 
            np.full((np.sum(mascara_pessoa > 0), 1), 255)  # Canal alpha
        ], axis=1)
        
        return silhueta
    
    def visualizar_resultados(self, imagem_original, mascara_pessoa, salvar=False, caminho_saida=None):
        """
        Visualiza os resultados da segmentação.
        
        Args:
            imagem_original: Imagem original
            mascara_pessoa: Máscara binária da pessoa
            salvar: Se deve salvar as imagens
            caminho_saida: Caminho base para salvar as imagens
        """
        fig, axes = plt.subplots(1, 4, figsize=(20, 5))
        
        # Imagem original
        axes[0].imshow(imagem_original)
        axes[0].set_title('Imagem Original')
        axes[0].axis('off')
        
        # Máscara da pessoa
        axes[1].imshow(mascara_pessoa, cmap='gray')
        axes[1].set_title('Máscara da Pessoa')
        axes[1].axis('off')
        
        # Imagem com máscara sobreposta
        imagem_com_mascara = self.aplicar_mascara(imagem_original, mascara_pessoa)
        axes[2].imshow(imagem_com_mascara)
        axes[2].set_title('Imagem com Máscara')
        axes[2].axis('off')
        
        # Silhueta extraída
        silhueta = self.extrair_silhueta(imagem_original, mascara_pessoa)
        axes[3].imshow(silhueta)
        axes[3].set_title('Silhueta Extraída')
        axes[3].axis('off')
        
        plt.tight_layout()
        
        if salvar and caminho_saida:
            plt.savefig(f"{caminho_saida}_resultado_segmentacao.png", dpi=300, bbox_inches='tight')
            
            # Salva as imagens individuais
            cv2.imwrite(f"{caminho_saida}_mascara.png", mascara_pessoa)
            cv2.imwrite(f"{caminho_saida}_com_mascara.png", cv2.cvtColor(imagem_com_mascara, cv2.COLOR_RGB2BGR))
            cv2.imwrite(f"{caminho_saida}_silhueta.png", cv2.cvtColor(silhueta, cv2.COLOR_RGBA2BGRA))
        
        plt.show()
    
    def processar_imagem(self, imagem_path):
        """
        Método simplificado para processar uma imagem e retornar os resultados.
        
        Args:
            imagem_path (str): Caminho para a imagem a ser processada
            
        Returns:
            tuple ou None: (imagem_original, mascara_binaria) se sucesso, None se erro
        """
        try:
            return self.segmentar_pessoa(imagem_path)
        except Exception as e:
            print(f"Erro ao processar imagem {imagem_path}: {str(e)}")
            return None