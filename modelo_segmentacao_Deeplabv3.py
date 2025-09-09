#!/usr/bin/env python3
"""
Modelo de segmentação otimizado em DeepLabV3
Versão simplificada e eficiente para processamento de imagens front.png e left.png
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
import logging
import time
import json

from segmentacao_imagens_Deeplabv3 import SegmentacaoDeepLabV3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModeloSegmentacaoDeepLabV3:
    """
    Classe otimizada para segmentação de imagens usando DeepLabV3.
    
    Métodos disponíveis:
    - 'rgb': DeepLabV3 original em RGB
    - 'grayscale_adaptive': Conversão inteligente para grayscale
    - 'grayscale_always': Sempre em grayscale (mais rápido)
    """
    
    def __init__(self, dataframe: pd.DataFrame,
                 confidence_threshold: float = 0.5,
                 min_area: int = 100,
                 target_size: Optional[Tuple[int, int]] = None,
                 metodo_deeplabv3: str = 'auto',
                 device: str = 'auto'):
        """
        Inicializa o modelo de segmentação DeepLabV3
        """
        self.dataframe = dataframe.copy()
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.target_size = target_size
        self.device = device
        
        # Configurar caminhos
        self.project_root = Path(__file__).parent.parent
        self.pasta_imagens = self.project_root / "INOVIA_IMAGENS"
        
        if not self.pasta_imagens.exists():
            raise FileNotFoundError(f"Pasta de imagens não encontrada: {self.pasta_imagens}")
        
        # Verificar PyTorch
        self._verificar_pytorch()
        
        # Configurar método
        self.metodo_deeplabv3 = self._determinar_metodo(metodo_deeplabv3)
        
        # Inicializar segmentador
        self._inicializar_segmentador()
        
        # Validar DataFrame
        if self.dataframe.empty or 'id' not in self.dataframe.columns:
            raise ValueError("DataFrame deve conter coluna 'id' não vazia")
        
        self.resultados = []
        self.estatisticas_globais = {}
        
        logger.info(f"Modelo DeepLabV3 inicializado: {len(self.dataframe)} registros, método '{self.metodo_deeplabv3}'")
    
    def _verificar_pytorch(self):
        """Verifica disponibilidade do PyTorch"""
        try:
            import torch
            import torchvision
            logger.info(f"PyTorch {torch.__version__} disponível")
            if torch.cuda.is_available():
                logger.info(f"CUDA disponível: {torch.cuda.get_device_name(0)}")
        except ImportError as e:
            raise RuntimeError(f"PyTorch não disponível: {e}")
    
    def _determinar_metodo(self, metodo: str) -> str:
        """Determina o método DeepLabV3 a ser usado"""
        if metodo != 'auto':
            return metodo.lower()
        
        # Lógica simplificada: baseada no tamanho do dataset
        num_registros = len(self.dataframe)
        
        try:
            import torch
            tem_cuda = torch.cuda.is_available()
            
            if tem_cuda and num_registros < 100:
                return 'rgb'
            elif num_registros < 50:
                return 'grayscale_adaptive'
            else:
                return 'grayscale_always'
        except:
            return 'grayscale_adaptive'
    
    def _inicializar_segmentador(self):
        """Inicializa o segmentador baseado no método escolhido"""
        config = {
            'confidence_threshold': self.confidence_threshold,
            'min_area': self.min_area,
            'target_size': self.target_size,
            'device': self.device
        }
        
        if self.metodo_deeplabv3 == 'rgb':
            config.update({'use_grayscale': False, 'grayscale_mode': 'auto'})
        elif self.metodo_deeplabv3 == 'grayscale_adaptive':
            config.update({'use_grayscale': True, 'grayscale_mode': 'adaptive'})
        else:  # grayscale_always
            config.update({'use_grayscale': True, 'grayscale_mode': 'always'})
        
        self.segmentador = SegmentacaoDeepLabV3(**config)
        logger.info(f"Segmentador {self.metodo_deeplabv3} inicializado")
    
    def _verificar_pasta_imagem(self, variavel: str) -> Tuple[bool, Dict[str, Path]]:
        """Verifica arquivos de imagem na pasta da variável"""
        pasta_variavel = self.pasta_imagens / variavel
        
        if not pasta_variavel.exists():
            return False, {}
        
        arquivos = {}
        for nome_arquivo in ["front.png", "left.png"]:
            caminho = pasta_variavel / nome_arquivo
            if caminho.exists():
                tipo = nome_arquivo.split('.')[0]
                arquivos[tipo] = caminho
        
        return len(arquivos) > 0, arquivos
    
    def _processar_imagem(self, caminho_imagem: Path, tipo_imagem: str, variavel: str) -> Dict:
        """Processa uma única imagem"""
        inicio_tempo = time.time()
        
        try:
            resultado_segmentacao = self.segmentador.processar_imagem(str(caminho_imagem))
            tempo_processamento = time.time() - inicio_tempo
            
            if resultado_segmentacao is not None:
                imagem_original, mascara_final = resultado_segmentacao
                estatisticas_mascara = self._calcular_estatisticas_mascara(mascara_final)
                
                return {
                    'variavel': variavel,
                    'tipo_imagem': tipo_imagem,
                    'caminho': str(caminho_imagem),
                    'sucesso': True,
                    'tempo_processamento': tempo_processamento,
                    'resultado_segmentacao': {
                        'imagem_original': imagem_original,
                        'mascara_final': mascara_final
                    },
                    'estatisticas_mascara': estatisticas_mascara,
                    'erro': None
                }
            else:
                return self._criar_resultado_erro(variavel, tipo_imagem, caminho_imagem, 
                                                 tempo_processamento, 'Falha na segmentação')
                
        except Exception as e:
            tempo_processamento = time.time() - inicio_tempo
            return self._criar_resultado_erro(variavel, tipo_imagem, caminho_imagem, 
                                             tempo_processamento, str(e))
    
    def _criar_resultado_erro(self, variavel: str, tipo_imagem: str, caminho: Path, 
                             tempo: float, erro: str) -> Dict:
        """Cria estrutura padronizada de resultado com erro"""
        return {
            'variavel': variavel,
            'tipo_imagem': tipo_imagem,
            'caminho': str(caminho),
            'sucesso': False,
            'tempo_processamento': tempo,
            'resultado_segmentacao': None,
            'estatisticas_mascara': {},
            'erro': erro
        }
    
    def _calcular_estatisticas_mascara(self, mascara: np.ndarray) -> Dict:
        """Calcula estatísticas básicas da máscara"""
        try:
            if mascara is None:
                return {}
            
            # Garantir que seja binária
            if len(mascara.shape) == 3:
                mascara_bin = np.any(mascara > 0, axis=2)
            else:
                mascara_bin = mascara > 0
            
            total_pixels = mascara_bin.size
            pixels_segmentados = np.sum(mascara_bin)
            percentual_segmentado = (pixels_segmentados / total_pixels) * 100
            
            return {
                'total_pixels': int(total_pixels),
                'pixels_segmentados': int(pixels_segmentados),
                'percentual_segmentado': round(percentual_segmentado, 2)
            }
                
        except Exception as e:
            logger.warning(f"Erro ao calcular estatísticas da máscara: {e}")
            return {}
    
    def processar_variavel(self, variavel: str) -> Dict:
        """Processa todas as imagens de uma variável"""
        inicio_tempo = time.time()
        
        # Verificar arquivos
        pasta_valida, arquivos = self._verificar_pasta_imagem(variavel)
        
        if not pasta_valida:
            return {
                'variavel': variavel,
                'sucesso': False,
                'tempo_processamento': time.time() - inicio_tempo,
                'erro': 'Pasta inválida ou arquivos faltando',
                'resultados_imagens': [],
                'total_imagens': 0,
                'imagens_sucesso': 0
            }
        
        # Processar cada imagem
        resultados_imagens = []
        for tipo_imagem, caminho_arquivo in arquivos.items():
            resultado_imagem = self._processar_imagem(caminho_arquivo, tipo_imagem, variavel)
            resultados_imagens.append(resultado_imagem)
        
        # Calcular resumo
        sucessos = [r['sucesso'] for r in resultados_imagens]
        
        return {
            'variavel': variavel,
            'sucesso': any(sucessos),
            'tempo_processamento': time.time() - inicio_tempo,
            'erro': None if any(sucessos) else 'Nenhuma imagem processada com sucesso',
            'resultados_imagens': resultados_imagens,
            'total_imagens': len(resultados_imagens),
            'imagens_sucesso': sum(sucessos)
        }
    
    def processar_dataset(self, limite_registros: Optional[int] = None,
                         exibir_progresso: bool = True) -> Dict:
        """Processa todo o dataset"""
        logger.info("Iniciando processamento do dataset")
        inicio_tempo_total = time.time()
        
        # Preparar lista de variáveis
        variaveis = self.dataframe['id'].astype(str).tolist()
        
        if limite_registros is not None:
            variaveis = variaveis[:limite_registros]
        
        # Processar cada variável
        self.resultados = []
        total_variaveis = len(variaveis)
        
        for i, variavel in enumerate(variaveis, 1):
            if exibir_progresso:
                logger.info(f"[{i:3d}/{total_variaveis}] Processando: {variavel}")
            
            resultado_variavel = self.processar_variavel(variavel)
            self.resultados.append(resultado_variavel)
        
        # Calcular estatísticas globais
        tempo_total = time.time() - inicio_tempo_total
        self.estatisticas_globais = self._calcular_estatisticas_globais(tempo_total)
        
        # Log resumo
        stats = self.estatisticas_globais
        logger.info(f"Processamento concluído em {stats['tempo_total']:.1f}s:")
        logger.info(f"  Variáveis: {stats['variaveis_sucesso']}/{stats['total_variaveis']} ({stats['taxa_sucesso_variaveis']:.1f}%)")
        logger.info(f"  Imagens: {stats['imagens_sucesso']}/{stats['total_imagens']} ({stats['taxa_sucesso_imagens']:.1f}%)")
        
        return {
            'metodo': f'deeplabv3_{self.metodo_deeplabv3}',
            'configuracao': {
                'metodo_deeplabv3': self.metodo_deeplabv3,
                'confidence_threshold': self.confidence_threshold,
                'min_area': self.min_area,
                'target_size': self.target_size
            },
            'estatisticas_globais': self.estatisticas_globais,
            'resultados_detalhados': self.resultados
        }
    
    def _calcular_estatisticas_globais(self, tempo_total: float) -> Dict:
        """Calcula estatísticas globais do processamento"""
        if not self.resultados:
            return {}
        
        total_variaveis = len(self.resultados)
        variaveis_sucesso = sum(1 for r in self.resultados if r['sucesso'])
        total_imagens = sum(r['total_imagens'] for r in self.resultados)
        imagens_sucesso = sum(r['imagens_sucesso'] for r in self.resultados)
        
        return {
            'tempo_total': tempo_total,
            'total_variaveis': total_variaveis,
            'variaveis_sucesso': variaveis_sucesso,
            'total_imagens': total_imagens,
            'imagens_sucesso': imagens_sucesso,
            'taxa_sucesso_variaveis': (variaveis_sucesso / total_variaveis) * 100 if total_variaveis > 0 else 0,
            'taxa_sucesso_imagens': (imagens_sucesso / total_imagens) * 100 if total_imagens > 0 else 0
        }
    
    def salvar_resultados(self, caminho_saida: Optional[str] = None) -> str:
        """Salva os resultados em arquivo JSON"""
        if not self.resultados:
            logger.warning("Nenhum resultado para salvar")
            return ""
        
        if caminho_saida is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            caminho_saida = self.project_root / f"resultados_deeplabv3_{timestamp}.json"
        
        try:
            dados_exportacao = {
                'metodo': f'deeplabv3_{self.metodo_deeplabv3}',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'configuracao': {
                    'metodo_deeplabv3': self.metodo_deeplabv3,
                    'confidence_threshold': self.confidence_threshold,
                    'min_area': self.min_area,
                    'target_size': self.target_size
                },
                'estatisticas_globais': self.estatisticas_globais,
                'resultados': []
            }
            
            # Processar resultados (excluindo dados das imagens/máscaras para economia de espaço)
            for resultado in self.resultados:
                resultado_serializado = resultado.copy()
                
                for img_result in resultado_serializado.get('resultados_imagens', []):
                    if 'resultado_segmentacao' in img_result and img_result['resultado_segmentacao']:
                        img_result['resultado_segmentacao'] = {
                            'sucesso': True,
                            'metodo': self.metodo_deeplabv3
                        }
                
                dados_exportacao['resultados'].append(resultado_serializado)
            
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(dados_exportacao, f, indent=2, ensure_ascii=False)
            
            tamanho_arquivo = os.path.getsize(caminho_saida) / (1024 * 1024)  # MB
            logger.info(f"Resultados salvos: {caminho_saida} ({tamanho_arquivo:.1f} MB)")
            
            return str(caminho_saida)
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
            return ""
    
    def gerar_relatorio_resumo(self) -> str:
        """Gera relatório resumido do processamento"""
        if not self.resultados or not self.estatisticas_globais:
            return "Nenhum resultado disponível para relatório."
        
        stats = self.estatisticas_globais
        
        relatorio = f"""
═══════════════════════════════════════════════════════════════════
                    RELATÓRIO DE SEGMENTAÇÃO DEEPLABV3                     
═══════════════════════════════════════════════════════════════════
CONFIGURAÇÃO:
• Método: {self.metodo_deeplabv3}
• Threshold de confiança: {self.confidence_threshold}
• Área mínima: {self.min_area} pixels

RESULTADOS:
• Total de variáveis: {stats['total_variaveis']:,}
• Variáveis processadas: {stats['variaveis_sucesso']:,} ({stats['taxa_sucesso_variaveis']:.1f}%)
• Total de imagens: {stats['total_imagens']:,}
• Imagens processadas: {stats['imagens_sucesso']:,} ({stats['taxa_sucesso_imagens']:.1f}%)

PERFORMANCE:
• Tempo total: {stats['tempo_total']:.1f} segundos ({stats['tempo_total']/60:.1f} minutos)
═══════════════════════════════════════════════════════════════════
        """
        
        return relatorio.strip()


# Exemplo de uso simplificado
if __name__ == "__main__":
    try:
        import pandas as pd
        
        # Criar DataFrame de exemplo
        dados_exemplo = pd.DataFrame({
            'id': ['001', '002', '003']
        })
        
        # Inicializar modelo
        modelo = ModeloSegmentacaoDeepLabV3(
            dataframe=dados_exemplo,
            metodo_deeplabv3='auto',
            confidence_threshold=0.5,
            min_area=100
        )
        
        # Processar dataset
        resultados = modelo.processar_dataset(limite_registros=3)
        
        # Gerar relatório
        print(modelo.gerar_relatorio_resumo())
        
        # Salvar resultados
        arquivo_salvo = modelo.salvar_resultados()
        if arquivo_salvo:
            print(f"\nResultados salvos em: {arquivo_salvo}")
        
    except Exception as e:
        print(f"Erro no exemplo: {e}")
