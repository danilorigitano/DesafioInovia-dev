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
    print("   • Métricas detalhadas (MSE, RMS)")
    print()
    print("="*60)


def obter_escolha_usuario() -> Tuple[str, str]:
    """
    Obtém a escolha do usuário e valida a entrada
    
    Returns:
        Tuple[str, str]: (tipo_modelo, metodo_segmentacao)
    """
    while True:
        try:
            exibir_menu_modelos()
            escolha = input("Escolha uma opção (1-2) ou Enter para padrão (2): ").strip()
            
            if escolha == "" or escolha == "2":
                print("✅ Modelo selecionado: Parametrização com Funções Indicadoras")
                metodo_segmentacao = obter_metodo_parametrizacao()
                return "parametrizacao", metodo_segmentacao
            elif escolha == "1":
                print("✅ Modelo selecionado: DeepLabV3 + ResNet101")
                return "deeplabv3", "deeplabv3"
            else:
                print("❌ Opção inválida. Digite 1 ou 2, ou pressione Enter para padrão.")
                
        except KeyboardInterrupt:
            print("\n\n⛔ Operação cancelada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("Tente novamente.")


def obter_metodo_parametrizacao() -> str:
    """
    Obtém o método específico de parametrização (linhas, colunas ou combinado)
    
    Returns:
        str: 'linhas', 'colunas' ou 'combinado'
    """
    while True:
        try:
            print("\n" + "="*60)
            print("🎯 MÉTODO DE PARAMETRIZAÇÃO")
            print("="*60)
            print("Escolha o tipo de função indicadora:")
            print()
            print("1️⃣  Segmentação por LINHAS (clássico)")
            print("   • 768 funções indicadoras horizontais")
            print("   • Método original otimizado")
            print()
            print("2️⃣  Segmentação por COLUNAS (novo)")
            print("   • 1024 funções indicadoras verticais")
            print("   • Análise perpendicular às linhas")
            print()
            print("3️⃣  Segmentação COMBINADA (4 resultados)")
            print("   • Mostra 4 silhuetas: somente linhas, somente colunas,")
            print("   • união (linha ∪ coluna) e intersecção (linha ∩ coluna)")
            print("   • Análise completa e comparativa")
            print("   • Processamento um pouco mais longo")
            print()
            print("="*60)
            
            escolha = input("Escolha uma opção (1-3) ou Enter para padrão (1): ").strip()
            
            if escolha == "" or escolha == "1":
                print("✅ Método selecionado: Segmentação por LINHAS")
                return "linhas"
            elif escolha == "2":
                print("✅ Método selecionado: Segmentação por COLUNAS")
                return "colunas"
            elif escolha == "3":
                print("✅ Método selecionado: Segmentação COMBINADA (4 resultados)")
                return "combinado"
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 3, ou pressione Enter para padrão.")
                
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


def criar_modelo_parametrizacao(dataset: pd.DataFrame, metodo_segmentacao: str = "linhas") -> ModeloSegmentacaoParametrizacao:
    """
    Cria e configura o modelo de Parametrização
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        metodo_segmentacao (str): Método de segmentação ('linhas', 'colunas', 'combinado')
        
    Returns:
        ModeloSegmentacaoParametrizacao: Modelo configurado
    """
    print("🔧 Configurando modelo de Parametrização...")
    
    # Ajustar dimensões baseado no método escolhido
    if metodo_segmentacao == "colunas" or metodo_segmentacao == "combinado":
        # Para colunas, usar dimensões maiores para melhor precisão
        target_width = 1024
        target_height = 768
    else:
        # Para linhas (método original)
        target_width = 512
        target_height = 382
    
    modelo = ModeloSegmentacaoParametrizacao(
        dataset,
        target_width=target_width,
        target_height=target_height,
        morph_kernel_size=5,
        min_area=100,
        enhance_contrast=True,
        metodo_segmentacao=metodo_segmentacao  # Adicionar o método
    )
    
    print(f"✅ Modelo Parametrização especializado inicializado ({metodo_segmentacao}).")
    return modelo


def inicializar_modelo(dataset: pd.DataFrame) -> Tuple[Union[ModeloSegmentacaoDeepLabV3, ModeloSegmentacaoParametrizacao], str, str]:
    """
    Função principal que coordena a escolha e inicialização do modelo
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        
    Returns:
        Tuple: (modelo_inicializado, tipo_modelo, metodo_segmentacao)
    """
    print("\n🚀 Iniciando seleção de modelo de segmentação...")
    
    # Obter escolha do usuário
    tipo_modelo, metodo_segmentacao = obter_escolha_usuario()
    
    print(f"\n🔄 Inicializando modelo de segmentação ({tipo_modelo})...")
    
    # Criar modelo baseado na escolha
    if tipo_modelo == 'deeplabv3':
        modelo = criar_modelo_deeplabv3(dataset)
    elif tipo_modelo == 'parametrizacao':
        modelo = criar_modelo_parametrizacao(dataset, metodo_segmentacao)
    else:
        raise ValueError(f"Tipo de modelo não reconhecido: {tipo_modelo}")
    
    return modelo, tipo_modelo, metodo_segmentacao


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


def exibir_resultados(resultado_geral: dict, tipo_modelo: str, metodo_segmentacao: str = None) -> None:
    """
    Exibe as estatísticas do resultado do processamento
    
    Args:
        resultado_geral (dict): Resultado do processamento
        tipo_modelo (str): Tipo do modelo utilizado
        metodo_segmentacao (str): Método de segmentação usado (se aplicável)
    """
    if not resultado_geral:
        print("❌ Nenhum resultado para exibir.")
        return
        
    print(f"\n" + "="*50)
    print("📊 RESULTADOS DO PROCESSAMENTO")
    print("="*50)
    
    if metodo_segmentacao and tipo_modelo == 'parametrizacao':
        print(f"🎯 Modelo utilizado: {tipo_modelo.upper()} ({metodo_segmentacao.upper()})")
    else:
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
        if tipo_modelo == 'parametrizacao':
            if 'mse_global' in stats:
                print(f"📈 MSE Global: {stats['mse_global']:.3f}")
            if 'rms_global' in stats:
                print(f"📈 RMS Global: {stats['rms_global']:.3f}")
            if metodo_segmentacao:
                if metodo_segmentacao == "linhas":
                    print(f"📏 Funções indicadoras horizontais processadas")
                elif metodo_segmentacao == "colunas":
                    print(f"📐 Funções indicadoras verticais processadas")
                elif metodo_segmentacao == "combinado":
                    print(f"🔄 4 resultados de silhuetas: linhas, colunas, união e intersecção")
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
