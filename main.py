#!/usr/bin/env python3
"""
Arquivo principal do projeto INOVIA
Este arquivo coordena a execução dos módulos do projeto
"""

import os
import sys
from pathlib import Path

from importa_dados import ImportadorDados

def main():
    """
    Função principal que coordena a execução do projeto
    """
    print("=== PROJETO INOVIA ===")
    print("Iniciando processamento...")
    
    # Verificar e configurar dados usando o módulo importa_dados
    importador = ImportadorDados()
    dados_ok = importador.imprimir_relatorio()
    
    if not dados_ok:
        print("\nERRO: Dados necessários não encontrados. Verifique os caminhos e tente novamente.")
        sys.exit(1)
    
    # Aqui você pode adicionar outras funcionalidades do projeto
    # Exemplo: processamento de imagens, análise de dados, etc.
    
    print("\nAdicione seus módulos e importe-os aqui conforme necessário.")

if __name__ == "__main__":
    main()
