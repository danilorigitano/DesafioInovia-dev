#!/usr/bin/env python3
"""
Arquivo principal do projeto INOVIA
Este arquivo coordena a execução dos módulos do projeto
"""

import os
import sys
from pathlib import Path

from importa_dados import ImportadorDados
from modelo_segmentacao import ModeloSegmentacao

def main():
    """
    Função principal que coordena a execução do projeto
    """
    print("=== PROJETO INOVIA ===")
    print("Iniciando processamento...")
    
    # Verificar e configurar dados usando o módulo importa_dados
    data_frame_valido = ImportadorDados()
    dados_ok = data_frame_valido.imprimir_relatorio()
    
    if not dados_ok:
        print("\nERRO: Dados necessários não encontrados. Verifique os caminhos e tente novamente.")
        sys.exit(1)
    
    # Estruturar dados por gênero e posição para poder usar 
    print("\nEstruturando dados por gênero e posição...")
    data_frame_valido.filtrar_dados_por_genero_posicao()
    
    # Verificar se há dados válidos para processar
    if not data_frame_valido.lista_possibilidades or all(df.empty for df in data_frame_valido.lista_possibilidades):
        print("\nAVISO: Nenhum dado válido encontrado após estruturação.")
        print("Processo finalizado sem processamento de imagens.")
        return
    
    # Inicializar modelo de segmentação
    print("\nInicializando modelo de segmentação...")
    
    # Para teste, processar apenas o primeiro dataset válido
    modelo_seg = ModeloSegmentacao(data_frame_valido.lista_possibilidades[0])

    #for i in range(len(data_frame_valido.lista_possibilidades)):
    #    modelo_seg = ModeloSegmentacao(data_frame_valido.lista_possibilidades[i])
    
    # Aqui você pode escolher qual dataset processar
    # Exemplo: processar todos com limite de registros
    print("\nIniciando processamento de segmentação...")
    
    resultado_geral = modelo_seg.processar_dataset(limite_registros=3, exibir_silhuetas=True)
    
    # Salvar resultados se necessário
    # caminho_resultados = modelo_seg.salvar_resultados()
    
    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
