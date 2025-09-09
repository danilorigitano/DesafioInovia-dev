#!/usr/bin/env python3
"""
Módulo responsável pela escolha e inicialização dos modelos de segmentação
Este módulo centraliza a lógica de seleção entre diferentes métodos de segmentação
"""

import sys
from typing import Tuple, Union
import pandas as pd

# Importar os modelos de segmentação
from modelo_segmentacao_Deeplabv3 import ModeloSegmentacaoDeepLabV3
from modelo_segmentacao_parametrizacao import ModeloSegmentacaoParametrizacao


def exibir_menu_modelos() -> None:
    """
    Exibe o menu de opções de modelos de segmentação
    """
    print("\n" + "="*60)
    print("🎯 SELEÇÃO DE MODELO DE SEGMENTAÇÃO")
    print("="*60)
    print("Escolha o método de segmentação que deseja utilizar:")
    print()
    print("1️⃣  DeepLabV3 + ResNet101")
    print("   • Modelo pré-treinado de deep learning")
    print("   • Alta precisão na segmentação de pessoas")
    print("   • Processamento mais lento")
    print()
    print("2️⃣  Parametrização com Funções Indicadoras")
    print("   • Método matemático otimizado")
    print("   • Processamento rápido e eficiente")
    print("   • Visualização automática de silhuetas")
    print("   • Métricas detalhadas (MAE, R²)")
    print()
    print("="*60)


def obter_escolha_usuario() -> str:
    """
    Obtém a escolha do usuário e valida a entrada
    
    Returns:
        str: 'deeplabv3' ou 'parametrizacao'
    """
    while True:
        try:
            exibir_menu_modelos()
            escolha = input("Escolha uma opção (1-2) ou Enter para padrão (2): ").strip()
            
            if escolha == "" or escolha == "2":
                print("✅ Modelo selecionado: Parametrização com Funções Indicadoras")
                return "parametrizacao"
            elif escolha == "1":
                print("✅ Modelo selecionado: DeepLabV3 + ResNet101")
                return "deeplabv3"
            else:
                print("❌ Opção inválida. Digite 1 ou 2, ou pressione Enter para padrão.")
                
        except KeyboardInterrupt:
            print("\n\n⛔ Operação cancelada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("Tente novamente.")


def criar_modelo_deeplabv3(dataset: pd.DataFrame) -> ModeloSegmentacaoDeepLabV3:
    """
    Cria e configura o modelo DeepLabV3
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        
    Returns:
        ModeloSegmentacaoDeepLabV3: Modelo configurado
    """
    print("🔧 Configurando modelo DeepLabV3...")
    
    modelo = ModeloSegmentacaoDeepLabV3(
        dataset,
        confidence_threshold=0.5,
        min_area=100,
        target_size=(512, 512),
        enhance_contrast=True,
        metodo_deeplabv3='auto'  # auto, rgb, grayscale_adaptive, grayscale_always
    )
    
    print("✅ Modelo DeepLabV3 especializado inicializado.")
    return modelo


def criar_modelo_parametrizacao(dataset: pd.DataFrame) -> ModeloSegmentacaoParametrizacao:
    """
    Cria e configura o modelo de Parametrização
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        
    Returns:
        ModeloSegmentacaoParametrizacao: Modelo configurado
    """
    print("🔧 Configurando modelo de Parametrização...")
    
    modelo = ModeloSegmentacaoParametrizacao(
        dataset,
        target_width=512,
        target_height=382,
        morph_kernel_size=5,
        min_area=100,
        enhance_contrast=True
    )
    
    print("✅ Modelo Parametrização especializado inicializado.")
    return modelo


def inicializar_modelo(dataset: pd.DataFrame) -> Tuple[Union[ModeloSegmentacaoDeepLabV3, ModeloSegmentacaoParametrizacao], str]:
    """
    Função principal que coordena a escolha e inicialização do modelo
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        
    Returns:
        Tuple: (modelo_inicializado, tipo_modelo)
    """
    print("\n🚀 Iniciando seleção de modelo de segmentação...")
    
    # Obter escolha do usuário
    tipo_modelo = obter_escolha_usuario()
    
    print(f"\n🔄 Inicializando modelo de segmentação ({tipo_modelo})...")
    
    # Criar modelo baseado na escolha
    if tipo_modelo == 'deeplabv3':
        modelo = criar_modelo_deeplabv3(dataset)
    elif tipo_modelo == 'parametrizacao':
        modelo = criar_modelo_parametrizacao(dataset)
    else:
        raise ValueError(f"Tipo de modelo não reconhecido: {tipo_modelo}")
    
    return modelo, tipo_modelo


def processar_com_modelo(modelo: Union[ModeloSegmentacaoDeepLabV3, ModeloSegmentacaoParametrizacao], 
                        tipo_modelo: str, 
                        limite_registros: int = 3) -> dict:
    """
    Processa o dataset usando o modelo escolhido
    
    Args:
        modelo: Modelo de segmentação inicializado
        tipo_modelo (str): Tipo do modelo ('deeplabv3' ou 'parametrizacao')
        limite_registros (int): Número de registros a processar
        
    Returns:
        dict: Resultado do processamento
    """
    print(f"\n⚡ Iniciando processamento com {tipo_modelo.upper()}...")
    print(f"📊 Processando {limite_registros} registros...")
    
    # Processar dataset com configurações específicas para cada modelo
    if tipo_modelo == 'parametrizacao':
        resultado_geral = modelo.processar_dataset(
            limite_registros=limite_registros, 
            exibir_progresso=True
        )
        
        # Exibir silhuetas automaticamente para o método de parametrização
        print("\n🖼️ Exibindo silhuetas dos resultados processados...")
        try:
            modelo.visualizar_amostra_resultados(
                num_amostras=min(3, limite_registros),
                tipo_visualizacao='completo'
            )
            print("✅ Silhuetas exibidas com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível exibir silhuetas: {e}")
            
    elif tipo_modelo == 'deeplabv3':
        resultado_geral = modelo.processar_dataset(
            limite_registros=limite_registros, 
            exibir_progresso=True
        )
    
    return resultado_geral


def exibir_resultados(resultado_geral: dict, tipo_modelo: str) -> None:
    """
    Exibe as estatísticas do resultado do processamento
    
    Args:
        resultado_geral (dict): Resultado do processamento
        tipo_modelo (str): Tipo do modelo utilizado
    """
    if not resultado_geral:
        print("❌ Nenhum resultado para exibir.")
        return
        
    print(f"\n" + "="*50)
    print("📊 RESULTADOS DO PROCESSAMENTO")
    print("="*50)
    print(f"🎯 Modelo utilizado: {tipo_modelo.upper()}")
    
    # Extrair estatísticas baseado no modelo utilizado
    if tipo_modelo == 'parametrizacao':
        stats = resultado_geral.get('estatisticas_globais', {})
    else:
        stats = resultado_geral
    
    # Verificar se as estatísticas estão disponíveis
    if stats:
        print(f"📁 Variáveis processadas: {stats['variaveis_sucesso']}/{stats['total_variaveis']}")
        print(f"🖼️ Imagens processadas: {stats['imagens_sucesso']}/{stats['total_imagens']}")
        print(f"✅ Taxa de sucesso: {stats['taxa_sucesso_imagens']:.1f}%")
        
        # Exibir métricas específicas do modelo de parametrização
        if tipo_modelo == 'parametrizacao' and 'mae_global' in stats:
            print(f"📈 MAE Global: {stats['mae_global']:.3f}")
            print(f"📈 R² Global: {stats['r2_global']:.3f}")
            print(f"⏱️ Tempo total: {stats.get('tempo_total', 0):.1f}s")
    else:
        print("⚠️ Estatísticas não disponíveis")
    
    print("="*50)


def salvar_resultados_modelo(modelo: Union[ModeloSegmentacaoDeepLabV3, ModeloSegmentacaoParametrizacao], 
                           stats: dict) -> None:
    """
    Salva os resultados do processamento
    
    Args:
        modelo: Modelo de segmentação utilizado
        stats (dict): Estatísticas do processamento
    """
    variaveis_sucesso = stats.get('variaveis_sucesso', 0) if stats else 0
    
    if variaveis_sucesso > 0:
        try:
            print("\n💾 Salvando resultados...")
            caminho_resultados = modelo.salvar_resultados()
            print(f"✅ Resultados salvos em: {caminho_resultados}")
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível salvar resultados: {e}")
    else:
        print("⚠️ Nenhum resultado válido para salvar.")


if __name__ == "__main__":
    print("⚠️ Este módulo deve ser importado, não executado diretamente.")
    print("Execute o arquivo main.py para utilizar o sistema.")
