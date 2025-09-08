# Projeto INOVIA 🚀

Sistema modular para processamento e análise de dados de imagens sintéticas com medidas corporais.

## 📋 Primeiros Passos do Desenvolvimento

O projeto foi iniciado com foco na **estruturação sólida dos dados** e **verificação automática** do ambiente. As primeiras implementações estabeleceram:

### ✅ Fundação Implementada
- **Módulo de Importação**: Sistema robusto para localizar e validar dados
- **Verificação Automática**: Detecção de pastas de imagens (female/male) e arquivo CSV
- **Relatórios Dinâmicos**: Status visual com estatísticas em tempo real
- **Arquitetura Modular**: Base extensível para futuras funcionalidades

### 🏗️ Estrutura do Projeto

```
githubinovia/                    # 📁 Código principal
├── main.py                     # 🎯 Coordenador principal
├── importa_dados.py            # 📊 Gerenciamento de dados
├── requirements.txt            # 📦 Dependências
├── CHANGELOG.md               # 📝 Histórico com mermaid
└── README.md                  # 📖 Documentação

Dados (pasta pai):               # 💾 Datasets
├── INOVIA_IMAGENS_female/      # 👩 Imagens sintéticas femininas
├── INOVIA_IMAGENS_male/        # 👨 Imagens sintéticas masculinas
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

- **Imagens Femininas**: Subpastas organizadas por categorias
- **Imagens Masculinas**: Subpastas organizadas por categorias  
- **CSV de Medidas**: Dados sintéticos estruturados

## 🛣️ Próximos Passos

1. **Processamento de Imagens** - Algoritmos de análise visual
2. **Análise de Dados** - Correlações entre medidas
3. **Interface Gráfica** - Dashboard interativo
4. **Testes Automatizados** - Validação contínua

## 📈 Status Atual

� **Versão 0.1.0** - Base sólida estabelecida  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico detalhado com fluxo mermaid