# Changelog

Histórico de desenvolvimento do Projeto INOVIA.

## Fluxo de Desenvolvimento

```mermaid
graph TD
    A[Início do Projeto] --> B[Setup Inicial]
    B --> C[Estrutura de Dados]
    C --> D[Módulo de Importação]
    D --> E[Sistema de Verificação]
    E --> F[Relatórios de Status]
    F --> G[Próximas Funcionalidades]
    
    B --> B1[Ambiente Virtual]
    B --> B2[Requirements.txt]
    B --> B3[Estrutura de Pastas]
    
    C --> C1[Imagens Female]
    C --> C2[Imagens Male]
    C --> C3[Dados CSV]
    
    D --> D1[ImportadorDados Class]
    D --> D2[Verificação de Caminhos]
    D --> D3[Carregamento CSV]
    
    E --> E1[Status dos Dados]
    E --> E2[Contagem de Arquivos]
    E --> E3[Validação Completa]
    
    F --> F1[Relatório Detalhado]
    F --> F2[Estatísticas]
    F --> F3[Status Visual]
    
    style A fill:#e1f5fe
    style G fill:#fff3e0
    style F fill:#e8f5e8
```

## Versões

### [0.1.0] - 2025-09-08 - Setup Inicial ✨

#### Adicionado
- **Estrutura base do projeto** com `main.py` como ponto de entrada
- **Módulo `importa_dados.py`** para gerenciamento de dados
- **Classe `ImportadorDados`** com funcionalidades completas:
  - Verificação automática de diretórios e arquivos
  - Carregamento e validação de dados CSV
  - Listagem de subpastas de imagens
  - Geração de estatísticas dos dados
  - Relatórios detalhados com status visual
- **Sistema de paths dinâmicos** usando pathlib
- **Configuração do ambiente** com requirements.txt
- **Documentação inicial** com README.md

#### Funcionalidades Implementadas
- ✅ Verificação automática de dados female/male
- ✅ Validação de arquivo CSV com medidas sintéticas
- ✅ Contagem de pastas e registros
- ✅ Relatórios coloridos com emojis
- ✅ Sistema modular e extensível

#### Estrutura de Dados Suportada
```
INOVIA_IMAGENS_female/    # Imagens sintéticas femininas
INOVIA_IMAGENS_male/      # Imagens sintéticas masculinas
medidas_dados_sinteticos.csv  # Dados de medidas
```

#### Próximos Passos
- [ ] Processamento de imagens
- [ ] Análise de dados sintéticos
- [ ] Algoritmos de medição
- [ ] Interface de usuário
- [ ] Testes automatizados

---

**Legenda:**
- ✨ Nova funcionalidade
- 🐛 Correção de bug
- 📝 Documentação
- 🔧 Manutenção
