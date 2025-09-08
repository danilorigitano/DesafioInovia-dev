# Changelog

Histórico de desenvolvimento do Projeto INOVIA.

## Fluxo de Desenvolvimento

```mermaid
graph LR
    A["🚀 Início"] --> B["⚙️ Setup"]
    B --> C["📊 Dados"]
    C --> D["🔍 Validação"]
    D --> E["📋 Relatórios"]
    E --> F["🔮 Próximo"]
    
    B --> B1["🐍 Virtual Env"]
    B --> B2["📦 Dependencies"]
    
    C --> C1["👩 Female"]
    C --> C2["👨 Male"]
    C --> C3["📈 CSV"]
    
    D --> D1["✅ Verificar"]
    D --> D2["🎯 Filtrar"]
    D --> D3["⚖️ Categorizar"]
    
    E --> E1["📊 Stats"]
    E --> E2["🎨 Visual"]
    
    F --> F1["🖼️ Imagens"]
    F --> F2["🧮 Analytics"]
    
    classDef done fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef next fill:#FF9800,stroke:#F57C00,color:#fff
    
    class A,B,C,D,E,B1,B2,C1,C2,C3,D1,D2,D3,E1,E2 done
    class F,F1,F2 next
```

## Versões

### [0.1.0] - 2025-09-08 - Base Sólida ✨

#### 🔥 Implementado
- **🎯 Arquitetura modular** com `main.py` como coordenador
- **📊 Sistema ImportadorDados** para gerenciamento inteligente
- **🔍 Validação automática** de dados CSV ↔ Pastas de imagens
- **⚖️ Categorização inteligente** por gênero e posição (Pre/Pos)
- **📋 Relatórios visuais** com estatísticas em tempo real

#### 🏗️ Funcionalidades Core
```python
ImportadorDados():
├── verificar_dados()          # ✅ Paths e arquivos
├── carregar_dados_csv()       # 📄 Leitura segura
├── filtrar_dados_validos()    # 🎯 Correspondência
├── filtrar_por_genero_posicao() # ⚖️ Categorias
└── imprimir_relatorio()       # 📊 Status visual
```

#### 📊 Estrutura Suportada
```
syn_fXXXXXX-X-Pre/    # 👩 Female Pre
syn_fXXXXXX-X-Pos/    # 👩 Female Pos  
syn_mXXXXXX-X-Pre/    # 👨 Male Pre
syn_mXXXXXX-X-Pos/    # 👨 Male Pos
```

#### 🔮 Roadmap
- 🖼️ **v0.2** - Processamento de imagens
- 🧮 **v0.3** - Analytics e correlações  
- 🎛️ **v0.4** - Interface gráfica
