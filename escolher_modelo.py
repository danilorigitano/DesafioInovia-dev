#!/usr/bin/env python3
"""
Módulo responsável pela escolha e inicialização dos modelos de segmentação
Este módulo centraliza a lógica de seleção entre diferentes métodos de segmentação
"""

import sys
from typing import Tuple, Union
import pandas as pd

# Importar os modelos de segmentação
from modelo_segmentacao_parametrizacao import ModeloSegmentacaoParametrizacao


def exibir_menu_modelos() -> None:
    """
    Exibe o menu de opções de modelos de segmentação
    """
    print("\nSeleção de Modelo de Segmentação")
    print("1. Parametrização com Funções Indicadoras")
    print("   - Método matemático otimizado")


def obter_escolha_usuario() -> Tuple[str, str]:
    """
    Obtém a escolha do usuário e valida a entrada
    
    Returns:
        Tuple[str, str]: (tipo_modelo, metodo_segmentacao)
    """
    while True:
        try:
            exibir_menu_modelos()
            escolha = input("Escolha uma opção (1) ou Enter para padrão (1): ").strip()
            
            if escolha == "" or escolha == "1":
                print("Modelo selecionado: Parametrização com Funções Indicadoras")
                print("Método selecionado: Segmentação COMBINADA")
                return "parametrizacao", "combinado"
            else:
                print("Opção inválida. Digite 1 ou pressione Enter para padrão.")
                
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            print("Tente novamente.")


def criar_modelo_parametrizacao(dataset: pd.DataFrame, metodo_segmentacao: str = "combinado") -> ModeloSegmentacaoParametrizacao:
    """
    Cria e configura o modelo de Parametrização
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        metodo_segmentacao (str): Método de segmentação (sempre 'combinado')
        
    Returns:
        ModeloSegmentacaoParametrizacao: Modelo configurado
    """
    print("Configurando modelo de Parametrização...")
    
    # Usar dimensões otimizadas para segmentação combinada
    target_width = 1024
    target_height = 768
    
    modelo = ModeloSegmentacaoParametrizacao(
        dataset,
        target_width=target_width,
        target_height=target_height,
        morph_kernel_size=5,
        min_area=100,
        enhance_contrast=True,
        metodo_segmentacao=metodo_segmentacao
    )
    
    print(f"Modelo Parametrização inicializado ({metodo_segmentacao}).")
    return modelo


def inicializar_modelo(dataset: pd.DataFrame) -> Tuple[ModeloSegmentacaoParametrizacao, str, str]:
    """
    Função principal que coordena a escolha e inicialização do modelo
    
    Args:
        dataset (pd.DataFrame): Dataset com os dados estruturados
        
    Returns:
        Tuple: (modelo_inicializado, tipo_modelo, metodo_segmentacao)
    """
    print("\nIniciando seleção de modelo de segmentação...")
    
    # Obter escolha do usuário
    tipo_modelo, metodo_segmentacao = obter_escolha_usuario()
    
    print(f"\nInicializando modelo de segmentação ({tipo_modelo})...")
    
    # Criar modelo baseado na escolha
    if tipo_modelo == 'parametrizacao':
        modelo = criar_modelo_parametrizacao(dataset, metodo_segmentacao)
    else:
        raise ValueError(f"Tipo de modelo não reconhecido: {tipo_modelo}")
    
    return modelo, tipo_modelo, metodo_segmentacao


def processar_com_modelo(modelo: ModeloSegmentacaoParametrizacao, 
                        tipo_modelo: str, 
                        limite_registros: int = 3) -> dict:
    """
    Processa o dataset usando o modelo escolhido
    
    Args:
        modelo: Modelo de segmentação inicializado
        tipo_modelo (str): Tipo do modelo ('parametrizacao')
        limite_registros (int): Número de registros a processar
        
    Returns:
        dict: Resultado do processamento
    """
    print(f"\nIniciando processamento com {tipo_modelo.upper()}...")
    print(f"Processando {limite_registros} registros...")
    
    # Processar dataset
    if tipo_modelo == 'parametrizacao':
        resultado_geral = modelo.processar_dataset(
            limite_registros=limite_registros, 
            exibir_progresso=True
        )
        
        # Exibir silhuetas
        print("\nExibindo silhuetas dos resultados...")
        try:
            modelo.visualizar_amostra_resultados(
                num_amostras=min(3, limite_registros),
                tipo_visualizacao='auto'
            )
            print("Silhuetas exibidas com sucesso!")
        except Exception as e:
            print(f"Aviso: Não foi possível exibir silhuetas: {e}")
    else:
        raise ValueError(f"Tipo de modelo não suportado: {tipo_modelo}")
    
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
        print("Nenhum resultado para exibir.")
        return
        
    print(f"\nResultados do Processamento")
    print("-" * 30)
    
    if metodo_segmentacao and tipo_modelo == 'parametrizacao':
        print(f"Modelo: {tipo_modelo.upper()} ({metodo_segmentacao.upper()})")
    else:
        print(f"Modelo: {tipo_modelo.upper()}")
    
    # Extrair estatísticas
    if tipo_modelo == 'parametrizacao':
        stats = resultado_geral.get('estatisticas_globais', {})
    else:
        stats = resultado_geral
    
    # Exibir estatísticas
    if stats:
        print(f"Variáveis processadas: {stats['variaveis_sucesso']}/{stats['total_variaveis']}")
        print(f"Imagens processadas: {stats['imagens_sucesso']}/{stats['total_imagens']}")
        print(f"Taxa de sucesso: {stats['taxa_sucesso_imagens']:.1f}%")
        
        if tipo_modelo == 'parametrizacao':
            if 'mse_global' in stats:
                print(f"MSE Global: {stats['mse_global']:.3f}")
            if 'rms_global' in stats:
                print(f"RMS Global: {stats['rms_global']:.3f}")
            print(f"Tempo total: {stats.get('tempo_total', 0):.1f}s")
    else:
        print("Estatísticas não disponíveis")
    
    print("-" * 30)


def salvar_resultados_modelo(modelo: ModeloSegmentacaoParametrizacao, 
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
            print("\nSalvando resultados...")
            caminho_resultados = modelo.salvar_resultados()
            print(f"Resultados salvos em: {caminho_resultados}")
        except Exception as e:
            print(f"Aviso: Não foi possível salvar resultados: {e}")
    else:
        print("Nenhum resultado válido para salvar.")


if __name__ == "__main__":
    print("Este módulo deve ser importado, não executado diretamente.")
    print("Execute o arquivo MainAvaliador.py para utilizar o sistema.")
