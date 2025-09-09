#!/usr/bin/env python3
"""
PROJETO INOVIA - Sistema de Segmentação de Imagens
Versão 0.2.2 - Arquitetura Modular Refatorada

Este é o módulo principal que coordena todo o fluxo de execução do projeto,
desde a importação dos dados até o processamento final com os modelos de segmentação.
"""

import sys
from pathlib import Path

# Importar módulos do projeto
from importa_dados import ImportadorDados
from escolher_modelo import (
    inicializar_modelo, 
    processar_com_modelo, 
    exibir_resultados, 
    salvar_resultados_modelo
)


def exibir_cabecalho() -> None:
    """
    Exibe o cabeçalho do projeto
    """
    print("="*60)
    print("🚀 PROJETO INOVIA - Sistema de Segmentação de Imagens")
    print("="*60)
    print("📋 Versão 0.2.2 - Arquitetura Modular Refatorada")
    print("🎯 Processamento inteligente de imagens médicas")
    print("📊 Múltiplos métodos de segmentação disponíveis")
    print("="*60)
    print("⚡ Iniciando processamento...")


def validar_dados() -> ImportadorDados:
    """
    Valida e carrega os dados necessários para o processamento
    
    Returns:
        ImportadorDados: Objeto com os dados válidos carregados
    """
    print("\n📂 Verificando e configurando dados...")
    
    # Verificar e configurar dados usando o módulo importa_dados
    data_frame_valido = ImportadorDados()
    dados_ok = data_frame_valido.imprimir_relatorio()
    
    if not dados_ok:
        print("\n❌ ERRO: Dados necessários não encontrados.")
        print("🔧 Verifique os caminhos e tente novamente.")
        sys.exit(1)
    
    return data_frame_valido


def estruturar_dados(data_frame_valido: ImportadorDados) -> ImportadorDados:
    """
    Estrutura os dados por gênero e posição
    
    Args:
        data_frame_valido (ImportadorDados): Objeto com dados carregados
        
    Returns:
        ImportadorDados: Objeto com dados estruturados
    """
    print("\n🗂️ Estruturando dados por gênero e posição...")
    data_frame_valido.filtrar_dados_por_genero_posicao()
    
    # Verificar se há dados válidos para processar
    if not data_frame_valido.lista_possibilidades or all(df.empty for df in data_frame_valido.lista_possibilidades):
        print("\n⚠️ AVISO: Nenhum dado válido encontrado após estruturação.")
        print("🛑 Processo finalizado sem processamento de imagens.")
        sys.exit(0)
    
    return data_frame_valido


def selecionar_dataset(data_frame_valido: ImportadorDados):
    """
    Seleciona o dataset para processamento
    
    Args:
        data_frame_valido (ImportadorDados): Objeto com dados estruturados
        
    Returns:
        pd.DataFrame: Dataset selecionado para processamento
    """
    print("\n📊 Selecionando dataset para processamento...")
    
    # Para este exemplo, processar apenas o primeiro dataset válido
    dataset = data_frame_valido.lista_possibilidades[0]
    
    print(f"✅ Dataset selecionado: {len(dataset)} registros disponíveis")
    return dataset


def main():
    """
    Função principal que coordena a execução do projeto
    """
    # Exibir cabeçalho
    exibir_cabecalho()
    
    # Validar e carregar dados
    data_frame_valido = validar_dados()
    
    # Estruturar dados
    data_frame_valido = estruturar_dados(data_frame_valido)
    
    # Selecionar dataset
    dataset = selecionar_dataset(data_frame_valido)
    
    # Inicializar modelo baseado na escolha do usuário
    modelo_seg, tipo_modelo = inicializar_modelo(dataset)
    
    # Processar dataset com o modelo escolhido
    resultado_geral = processar_com_modelo(
        modelo=modelo_seg,
        tipo_modelo=tipo_modelo,
        limite_registros=3
    )
    
    # Exibir resultados
    exibir_resultados(resultado_geral, tipo_modelo)
    
    # Salvar resultados se processamento foi bem-sucedido
    if resultado_geral:
        # Extrair estatísticas baseado no modelo utilizado
        if tipo_modelo == 'parametrizacao':
            stats = resultado_geral.get('estatisticas_globais', {})
        else:
            stats = resultado_geral
            
        salvar_resultados_modelo(modelo_seg, stats)
    
    # Finalização
    print("\n" + "="*60)
    print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("📋 Projeto INOVIA - Versão 0.2.2")
    print("📖 Para mais informações, consulte o CHANGELOG.md")
    print("🚀 Obrigado por usar o Sistema de Segmentação INOVIA!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Operação cancelada pelo usuário.")
        print("👋 Até a próxima!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        print("🔧 Verifique os logs e tente novamente.")
        sys.exit(1)
