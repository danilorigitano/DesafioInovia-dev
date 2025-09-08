# Projeto INOVIA 🚀

Sistema modular para processamento e análise de dados de imagens sintéticas com medida🚀 **Versão 0.1.0** - Base sólida estabelecida  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico detalhado com fluxo Mermaidcorporais.

## 📋 Primeiros Passos do Desenvolvimento

O projeto começou focando na **validação e estruturação robusta dos dados** como base sólida para futuras funcionalidades.

**Por que essa estratégia?**
- ✅ Detectar problemas de dados **antes** de desenvolver features complexas
- 🔄 Garantir **integridade** entre CSV e pastas de imagens  
- 📊 Ter **visibilidade** do que temos disponível para trabalhar
- 🧩 Criar **base modular** para crescimento organizado

### 🏗️ O que foi Implementado

**Motor Central: Classe `ImportadorDados`**
```python
# Funcionalidades principais desenvolvidas:
1. 🔍 Verificação automática de paths e arquivos
2. 📄 Carregamento seguro de CSV com tratamento de erros  
3. 🎯 Filtragem inteligente (só dados com pasta correspondente)
4. ⚖️ Categorização por gênero/posição: syn_[f/m]XXXXX-X-[Pre/Pos]
5. 📊 Relatórios visuais com estatísticas em tempo real
```

**Estrutura de Dados Detectada:**
```
📁 INOVIA_IMAGENS/
├── syn_fXXXXXX-X-Pre/    # 👩 Female Pre-procedimento  
├── syn_fXXXXXX-X-Pos/    # 👩 Female Pós-procedimento
├── syn_mXXXXXX-X-Pre/    # 👨 Male Pre-procedimento
└── syn_mXXXXXX-X-Pos/    # 👨 Male Pós-procedimento

📄 medidas_dados_sinteticos.csv # Medidas corporais correspondentes
```

### ⚡ Quick Start

```powershell
# Ativar ambiente e executar verificação completa
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  
python main.py
```

**🎯 Resultado:** Relatório detalhado mostrando quantos dados temos, quais categorias, e se tudo está consistente.

### 🏗️ Arquitetura do Projeto

```
githubinovia/                    # 📁 Código principal
├── main.py                     # 🎯 Coordenador principal
├── importa_dados.py            # 📊 Gerenciamento de dados
├── requirements.txt            # 📦 Dependências
├── CHANGELOG.md               # 📝 Histórico com mermaid
└── README.md                  # 📖 Documentação

Dados (pasta pai):               # 💾 Datasets
├── INOVIA_IMAGENS/             # �️ Todas as imagens sintéticas
│   ├── [subpastas female]      # 👩 Categorias femininas
│   ├── [subpastas male]        # 👨 Categorias masculinas
│   └── [outras categorias]     # 📂 Outros tipos
└── medidas_dados_sinteticos.csv # 📈 Medidas corporais
```

## ⚙️ Configuração Rápida

### 1. Ativar ambiente virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 3. Executar verificação
```powershell
python main.py
```

## 🎯 Funcionalidades Atuais

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `ImportadorDados` | ✅ | Verificação e carregamento automático de dados |
| `verificar_dados()` | ✅ | Validação de existência de arquivos/pastas |
| `carregar_dados_csv()` | ✅ | Leitura segura de dados CSV |
| `obter_estatisticas()` | ✅ | Contagem e métricas dos datasets |
| `imprimir_relatorio()` | ✅ | Relatório visual completo |

## 📊 Dados Suportados

- **Pasta INOVIA_IMAGENS**: Todas as imagens organizadas por subpastas
  - Detecção automática de categorias femininas/masculinas
  - Suporte a estruturas flexíveis de organização
- **CSV de Medidas**: Dados sintéticos estruturados com medidas corporais

## 🛣️ Próximos Passos

1. **Processamento de Imagens** - Algoritmos de análise visual
2. **Análise de Dados** - Correlações entre medidas
3. **Interface Gráfica** - Dashboard interativo
4. **Testes Automatizados** - Validação contínua

## 📈 Status Atual

� **Versão 0.1.0** - Base sólida estabelecida  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico detalhado com fluxo mermaid