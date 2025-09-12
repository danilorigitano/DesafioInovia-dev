#!/usr/bin/env python3
"""
PROJETO INOVIA - Sistema de Segmentação de Imagens
Versão 0.6.0 

Módulo principal
"""

import sys
from pathlib import Path
import pandas as pd

# Importar módulos do projeto
from importa_dados import ImportadorDados
from escolher_modelo import (
    inicializar_modelo, 
    processar_com_modelo, 
    exibir_resultados, 
    salvar_resultados_modelo
)


def exibir_cabecalho() -> None:
    """Exibe cabeçalho do sistema"""
    print("="*50)
    print("INOVIA - Segmentação de Imagens v0.6.0")

    print("="*50)


def validar_dados() -> ImportadorDados:
    """Carrega e valida dados de entrada"""
    print("📂 Carregando dados...")
    
    data_frame_valido = ImportadorDados()
    dados_ok = data_frame_valido.imprimir_relatorio()
    
    if not dados_ok:
        print("ERRO: Dados não encontrados")
        sys.exit(1)
    
    return data_frame_valido


def estruturar_dados(data_frame_valido: ImportadorDados) -> ImportadorDados:
    """Estrutura dados por gênero e posição"""
    print("🗂️ Estruturando dados...")
    data_frame_valido.filtrar_dados_por_genero_posicao()
    
    if not data_frame_valido.lista_possibilidades or all(df.empty for df in data_frame_valido.lista_possibilidades):
        print("⚠️ Nenhum dado válido encontrado")
        sys.exit(0)
    
    return data_frame_valido


def selecionar_dataset(data_frame_valido: ImportadorDados, indice: int) -> 'pd.DataFrame':
    """Seleciona dataset para processamento"""
    print("Selecionando dataset...")
    
    dataset = data_frame_valido.lista_possibilidades[indice]
    print(f"Dataset: {len(dataset)} registros")
    return dataset


def obter_numero_ids_para_analisar(total_registros: int) -> int:
    """
    Permite ao usuário escolher quantos IDs serão analisados
    
    Args:
        total_registros (int): Número total de registros disponíveis
        
    Returns:
        int: Número de registros escolhidos pelo usuário
    """
    print(f"\n📊 Total de registros disponíveis: {total_registros}")
    print("="*50)
    
    while True:
        try:
            resposta = input(f"Quantos IDs você deseja analisar? (1-{total_registros}) ou Enter para padrão (3): ").strip()
            
            # Se usuário pressionar Enter, usar padrão de 3
            if resposta == "":
                numero_escolhido = min(3, total_registros)
                print(f"✅ Usando padrão: {numero_escolhido} registros")
                return numero_escolhido
            
            # Converter entrada para inteiro
            numero_escolhido = int(resposta)
            
            # Validar range
            if numero_escolhido < 1:
                print("❌ Erro: O número deve ser pelo menos 1")
                continue
            elif numero_escolhido > total_registros:
                print(f"❌ Erro: O número não pode ser maior que {total_registros}")
                continue
            else:
                print(f"✅ Selecionado: {numero_escolhido} registros para análise")
                return numero_escolhido
                
        except ValueError:
            print("❌ Erro: Digite um número válido")
        except KeyboardInterrupt:
            print("\n⚠️ Operação cancelada pelo usuário")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("Tente novamente.")


def main():
    """Função principal - coordena execução"""
    exibir_cabecalho()
    
    # Pipeline de processamento
    data_frame_valido = validar_dados()
    data_frame_valido = estruturar_dados(data_frame_valido)
    dataset = selecionar_dataset(data_frame_valido, 0)
    
    # Permitir usuário escolher quantos IDs analisar
    total_registros = len(dataset)
    numero_ids_analisar = obter_numero_ids_para_analisar(total_registros)
    
    # Processamento com modelo escolhido
    modelo_seg, tipo_modelo, metodo_segmentacao = inicializar_modelo(dataset)
    resultado_geral = processar_com_modelo(
        modelo=modelo_seg,
        tipo_modelo=tipo_modelo,
        limite_registros=numero_ids_analisar
    )
    
    # Resultados
    exibir_resultados(resultado_geral, tipo_modelo, metodo_segmentacao)
    
    if resultado_geral:
        if tipo_modelo == 'parametrizacao':
            stats = resultado_geral.get('estatisticas_globais', {})
        else:
            stats = resultado_geral
        salvar_resultados_modelo(modelo_seg, stats)
    
    # Finalização
    print("\n" + "="*50)
    print("🎉 PROCESSAMENTO CONCLUÍDO")
    print(f"📊 Total de IDs analisados: {numero_ids_analisar}")
    print("📋 INOVIA v0.5.0 | Consulte CHANGELOG.md")
    print("="*50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\nERRO: {e}")
        sys.exit(1)
