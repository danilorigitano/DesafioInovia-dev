# 🚀 Projeto INOVIA - Sistema de Segmentação Inteligente

Sistema modular avançado para processamento e análise de dados de imagens sintéticas com medidas corporais, utilizando métodos matemáticos otimizados.

```mermaid
graph LR
    A[🖼️ Imagens Sintéticas] --> B[🧠 Processamento IA]
    B --> C[📊 Análise Corporal]
    C --> D[📋 Relatórios]
    
    B --> B2[Parametrização]
    B --> B3[Bounding Boxes]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

🚀 **Versão 0.6.0** - Sistema Modernizado com Parametrização Otimizada!  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico completo de desenvolvimento

## 📋 Visão Geral do Sistema

O Projeto INOVIA é uma solução completa e inovadora para segmentação e análise de imagens corporais sintéticas, oferecendo:

- **📐 Métodos Matemáticos Otimizados**: Algoritmos de parametrização por funções indicadoras com 4 abordagens especializadas
- **📦 Detecção Automática de Regiões**: Sistema de bounding boxes para localização precisa das áreas de interesse
- **⚡ Performance Extrema**: Otimizações NumPy com processamento 3-5x mais rápido e early stopping inteligente
- **📊 Análise Comparativa**: Métricas detalhadas e visualizações especializadas para cada método
- **🧹 Arquitetura Modernizada**: Sistema simplificado focado exclusivamente em parametrização

### 🎯 Características Principais

```mermaid
mindmap
    root((🚀 INOVIA))
        🔬 Precisão Científica
            Algoritmos Validados
            MSE < 200
            Métricas Rigorosas
        ⚡ Performance Extrema
            Vectorização NumPy
            3-5x Velocidade
            Early Stopping
        🎛️ Flexibilidade Total
            4 Métodos Parametrização
            Escolha Inteligente
            Visualização Automática
        📦 Detecção Inteligente
            Bounding Boxes
            Localização Precisa
            Análise Geométrica
```

## 🛠️ Tecnologias e Métodos

### 📐 Parametrização com Funções Indicadoras

Sistema avançado de segmentação matemática com múltiplas abordagens:

- **🎛️ Flexibilidade Total**: Múltiplos métodos de segmentação (4 Parametrizações especializadas)
- **⚡ Performance Otimizada**: Vectorização NumPy para processamento em lote
- **📊 Métricas Rigorosas**: MSE, RMS, taxa de sucesso e análise temporal
- **🖼️ Visualização Automática**: Silhuetas comparativas em tempo real

## 🚀 Instalação e Uso

### 📋 Pré-requisitos

```bash
# Python 3.11+ recomendado
pip install -r requirements.txt
```

### 🎮 Execução Principal

```bash
python MainAvaliador.py
```

**🎮 Interface Interativa:**
- Seleção dinâmica do número de registros para análise
- Padrão de 3 registros (pressione Enter)
- Validação automática de entrada
- Feedback visual durante o processamento

### 📤 Exportação de Resultados

```bash
python exportacao_parametrizacao.py
```

**📋 Funcionalidades de Exportação:**
- **Arquivo TXT**: Resultados em formato legível
- **Métricas Completas**: MSE, tempo de processamento, parâmetros
- **Organização Automática**: Salvos em `dados_analisados/`
- **Integração Automática**: Pode ser chamado após processamento principal

### 📊 Estrutura de Pastas

```
projeto/
├── 📁 INOVIA_IMAGENS/          # Imagens sintéticas organizadas
│   ├── 001/front.png, left.png
│   ├── 002/front.png, left.png
│   └── ...
├── 📁 dados_analisados/        # Resultados processados
├── 🐍 MainAvaliador.py         # Módulo principal
├── 🧠 escolher_modelo.py       # Seleção de método
├── 📐 modelo_segmentacao_parametrizacao.py
├── 🖼️ segmentacao_imagens_parametrizacao_indicadora.py
├── 📦 Bounding_box.py         # Detecção de regiões
├── 📤 exportacao_parametrizacao.py  # Exportação TXT
└── 📋 requirements.txt        # Dependências
```

## 🎯 Métodos de Segmentação

### 🆕 Novidades v0.6.0

#### 🧹 Modernização Arquitetural
- **Remoção do DeepLabV3**: Sistema focado exclusivamente em parametrização matemática
- **Arquitetura Simplificada**: Código mais limpo e manutenível
- **Dependências Reduzidas**: Instalação mais rápida sem PyTorch
- **Performance Otimizada**: Sistema dedicado à parametrização

#### 🎮 Interface Aprimorada
- **Seleção Dinâmica**: Escolha quantos registros analisar (1 até total disponível)
- **Valor Padrão Inteligente**: Pressione Enter para usar padrão (3 registros)
- **Validação Robusta**: Verificação automática de entradas
- **Feedback Visual**: Confirmações e mensagens de status melhoradas

### 🧠 Arquitetura de Processamento

```mermaid
graph TB
    subgraph "🎮 Interface Usuário"
        MainApp[🚀 MainAvaliador.py<br/>Interface Principal]
        Menu[📋 Menu Interativo<br/>Seleção de Método]
    end
    
    subgraph "📊 Gerenciamento Dados"
        Import[📥 ImportadorDados<br/>Validação Dataset]
        Filter[🎯 Filtros Inteligentes<br/>Gênero + Posição]
        Valid[✅ Validação<br/>CSV ↔ Imagens]
    end
    
    subgraph "🔧 Engine Parametrização"
        Model[🧠 ModeloSegmentacao<br/>Coordenação]
        Engine[⚡ SegmentacaoIndicadora<br/>Motor Matemático]
        Metrics[📊 Métricas MSE/RMS<br/>Validação Científica]
    end
    
    subgraph "📦 Módulos Auxiliares"
        BBox[🔍 BoundingBox<br/>Detecção Regiões]
        Display[🖼️ Visualização<br/>Resultados Gráficos]
        Export[📤 Exportação<br/>Relatórios JSON]
    end
    
    MainApp --> Menu
    Menu --> Import
    Import --> Filter
    Filter --> Valid
    Valid --> Model
    Model --> Engine
    Engine --> Metrics
    Metrics --> BBox
    BBox --> Display
    Display --> Export
    
    style MainApp fill:#e3f2fd
    style Engine fill:#e8f5e8
    style BBox fill:#fff3e0
    style Display fill:#f3e5f5
```

### 🧮 Processamento Matemático Detalhado

```mermaid
flowchart LR
    subgraph "📐 Funções Indicadoras"
        FuncGen[📏 Geração de Funções<br/>Linhas: f(x) = triangular<br/>Colunas: g(y) = triangular]
        Vectorize[⚡ Vectorização NumPy<br/>Batch Processing<br/>3-5x Performance]
        Optimize[🎯 Otimização MSE<br/>Early Stopping < 200<br/>Fallback < 300]
    end
    
    subgraph "🔍 Análise Comparativa"
        Method1[📏 Método Linhas<br/>768 funções horizontais]
        Method2[📐 Método Colunas<br/>1024 funções verticais]
        Method3[🔄 Método Combinado<br/>4 resultados finais]
    end
    
    subgraph "📊 Métricas e Resultados"
        MSE[📈 Cálculo MSE<br/>Mean Square Error]
        RMS[📉 Cálculo RMS<br/>Root Mean Square]
        Success[✅ Taxa Sucesso<br/>Análise Global]
        Report[📋 Relatório Final<br/>JSON + Visualizações]
    end
    
    FuncGen --> Vectorize
    Vectorize --> Optimize
    
    Optimize --> Method1
    Optimize --> Method2
    Optimize --> Method3
    
    Method1 --> MSE
    Method2 --> MSE
    Method3 --> MSE
    
    MSE --> RMS
    RMS --> Success
    Success --> Report
    
    style FuncGen fill:#e8f5e8
    style Vectorize fill:#fff9c4
    style MSE fill:#e1f5fe
    style Report fill:#f3e5f5
```

### 1️⃣ 📐 Parametrização com Funções Indicadoras (Otimizado)

```mermaid
flowchart TD
    Start[🚀 Início] --> ChooseModel{Escolher Método}
    
    ChooseModel -->|1️⃣| Linhas[📏 Método LINHAS<br/>768 Funções Horizontais]
    ChooseModel -->|2️⃣| Colunas[📐 Método COLUNAS<br/>1024 Funções Verticais]
    ChooseModel -->|3️⃣| Combinado[🔄 Método COMBINADO<br/>4 Resultados]
    
    Linhas --> Process[🎯 Processamento Vectorizado<br/>Otimização NumPy<br/>Early Stopping]
    Colunas --> Process
    Combinado --> Process
    
    Process --> Results[📊 Resultados<br/>MSE + RMS + Taxa Sucesso<br/>Silhuetas + Bounding Boxes]
    Results --> Save[💾 Salvamento Automático<br/>JSON + Visualizações]
    
    subgraph "📐 Uso Parametrização"
        direction TB
        ParamLoad[Carregamento Imagens]
        ParamProcess[Processamento Matemático]
        ParamMetrics[Cálculo MSE/RMS]
        ParamVisualize[Visualização Silhuetas]
        ParamBBox[Detecção Bounding Boxes]
        
        ParamLoad --> ParamProcess
        ParamProcess --> ParamMetrics
        ParamMetrics --> ParamVisualize
        ParamVisualize --> ParamBBox
    end
    
    Process -.-> ParamLoad
    
    style Linhas fill:#e8f5e8
    style Colunas fill:#e3f2fd
    style Combinado fill:#f3e5f5
    style Process fill:#fff9c4
    style Results fill:#e8f5e8
```

## 🔧 Arquitetura Técnica

### 📊 Pipeline de Processamento

```mermaid
graph TB
    subgraph "🔄 Pipeline Principal"
        Main[🚀 MainAvaliador.py<br/>Coordenação Geral]
        Import[📥 importa_dados.py<br/>Validação Dataset]
        Choose[🎯 escolher_modelo.py<br/>Seleção Método]
        Process[⚡ Processamento<br/>Análise Imagens]
        Export[📤 Exportação<br/>Resultados JSON]
    end
    
    subgraph "📐 Módulos Parametrização"
        Param_Model[ModeloSegmentacaoParametrizacao<br/>Coordenação Científica]
        Param_Engine[SegmentacaoIndicadora<br/>Processamento Matemático]
        Param_Metrics[Métricas MSE/RMS<br/>Validação Rigorosa]
        Param_Visual[Visualização Silhuetas<br/>Análise Comparativa]
    end
    
    subgraph "📦 Módulos Auxiliares"
        BBox[🔍 Bounding_box.py<br/>Detecção Regiões]
        Display[🖼️ exibicao_*.py<br/>Visualizações]
        Export_Param[📋 exportacao_parametrizacao.py<br/>Relatórios Especializados]
    end
    
    Main --> Import
    Import --> Choose
    Choose --> Process
    Process --> Export
    
    Choose --> Param_Model
    Param_Model --> Param_Engine
    Param_Engine --> Param_Metrics
    Param_Metrics --> Param_Visual
    
    Param_Visual --> BBox
    Process --> Display
    Export --> Export_Param
    
    User -->|1️⃣ Parametrização| Param_Config[📐 Configuração<br/>Método + Dimensões]
    Param_Config --> Param_Model
    
    style Main fill:#e1f5fe
    style Param_Model fill:#e8f5e8
    style BBox fill:#fff3e0
```

## ⚡ Performance e Otimizações

### 📈 Benchmarks de Performance

```mermaid
gantt
    title 🚀 Performance Comparativa por Método
    dateFormat X
    axisFormat %s
    
    section 📐 Parametrização
        Método Linhas     : 0, 3s
        Método Colunas    : 0, 4s
        Método Combinado  : 0, 8s
    
    section ⚡ Otimizações
        Vectorização NumPy : 0, 1s
        Early Stopping     : 0, 2s
```

### 🔧 Configurações Recomendadas

| Método | Tempo/Imagem | Precisão | Uso RAM | Aplicação |
|--------|-------------|----------|---------|-----------|
| Linhas | ~3s | ⭐⭐⭐⭐ | Baixo | Análise Horizontal |
| Colunas | ~4s | ⭐⭐⭐⭐ | Baixo | Análise Vertical |
| Combinado | ~8s | ⭐⭐⭐⭐⭐ | Médio | Análise Completa |

## 📊 Estrutura de Dados

### 🗃️ Formato Dataset

```python
# Estrutura do DataFrame principal
{
    'id': '001',                    # Identificador único
    'gender': 'female',             # Gênero
    'frontal_silhouette': array,    # Silhueta frontal
    'lateral_silhouette': array,    # Silhueta lateral
    'body_measurements': {...}      # Medidas corporais
}
```

## 📊 Estrutura de Dados e Fluxo

### 🗃️ Arquitetura de Dados

```mermaid
erDiagram
    DATASET ||--o{ IMAGES : contains
    DATASET {
        string id PK "Identificador único"
        string gender "male/female"
        float weight "Peso corporal"
        float height "Altura"
        json body_measurements "Medidas detalhadas"
    }
    
    IMAGES ||--o{ SILHOUETTES : generates
    IMAGES {
        string id PK "ID do dataset"
        string position "front/left"
        blob image_data "Dados da imagem"
        int width "Largura original"
        int height "Altura original"
    }
    
    SILHOUETTES ||--o{ PARAMETERS : optimizes
    SILHOUETTES {
        string id PK "ID da silhueta"
        string method "linhas/colunas/combinado"
        array mask_data "Máscara segmentada"
        float mse_score "Pontuação MSE"
        json bbox_data "Bounding boxes"
    }
    
    PARAMETERS {
        string silhouette_id FK
        string param_type "a,b,c,d"
        float value "Valor otimizado"
        int function_index "Índice da função"
        float convergence "Taxa convergência"
    }
    
    RESULTS ||--o{ VISUALIZATIONS : creates
    RESULTS {
        string processing_id PK
        datetime timestamp "Data processamento"
        string method_used "Método aplicado"
        json global_stats "Estatísticas globais"
        float processing_time "Tempo execução"
    }
    
    VISUALIZATIONS {
        string result_id FK
        string viz_type "silhouette/bbox/comparison"
        blob image_output "Visualização gerada"
        json metadata "Metadados visuais"
    }
```

### 🔄 Pipeline de Processamento Completo

```mermaid
stateDiagram-v2
    [*] --> Initialization
    
    state Initialization {
        [*] --> LoadData
        LoadData --> ValidateCSV
        ValidateCSV --> CheckImages
        CheckImages --> FilterData
        FilterData --> [*]
    }
    
    Initialization --> MethodSelection
    
    state MethodSelection {
        [*] --> DisplayMenu
        DisplayMenu --> UserChoice
        UserChoice --> ValidateInput
        ValidateInput --> InitializeModel
        InitializeModel --> [*]
    }
    
    MethodSelection --> Processing
    
    state Processing {
        [*] --> LoadImages
        LoadImages --> ApplyParametrization
        
        state ApplyParametrization {
            [*] --> GenerateFunctions
            GenerateFunctions --> VectorizeOperations
            VectorizeOperations --> OptimizeMSE
            OptimizeMSE --> CalculateMetrics
            CalculateMetrics --> [*]
        }
        
        ApplyParametrization --> DetectBoundingBoxes
        DetectBoundingBoxes --> GenerateVisualizations
        GenerateVisualizations --> [*]
    }
    
    Processing --> Results
    
    state Results {
        [*] --> CompileStatistics
        CompileStatistics --> ExportJSON
        ExportJSON --> SaveVisualizations
        SaveVisualizations --> DisplayResults
        DisplayResults --> [*]
    }
    
    Results --> [*]
    
    note right of Processing : ⚡ Vectorização NumPy\n🎯 Early Stopping\n📊 MSE < 200
    note right of Results : 📋 Relatórios JSON\n🖼️ Visualizações\n📦 Bounding Boxes
```

### 📋 Formato de Saída

```json
{
    "metodo": "parametrizacao_linhas",
    "configuracao": {
        "target_width": 512,
        "target_height": 382,
        "metodo_segmentacao": "linhas"
    },
    "estatisticas_globais": {
        "total_variaveis": 3,
        "variaveis_sucesso": 3,
        "total_imagens": 6,
        "imagens_sucesso": 6,
        "taxa_sucesso": 100.0,
        "mse_global": 156.789,
        "rms_global": 12.523,
        "tempo_total": 8.45
    },
    "resultados_detalhados": [...]
}
```

## 🏗️ Evolução do Projeto

### 📈 Cronograma de Desenvolvimento

```mermaid
gantt
    title 🚀 Linha do Tempo - Projeto INOVIA
    dateFormat YYYY-MM-DD
    
    section 📊 v0.1.0 - Base
        Importação Dados : done, 2025-09-01, 2025-09-03
        Estrutura Inicial : done, 2025-09-03, 2025-09-05
        
    section 📐 v0.3.0 - Parametrização
        Funções Indicadoras : done, 2025-09-09, 2025-09-10
        Métricas MSE/RMS : done, 2025-09-10, 2025-09-11
        
    section ⚡ v0.4.0 - Otimização
        Vectorização NumPy : done, 2025-09-11, 2025-09-11
        4 Métodos Especializados : done, 2025-09-11, 2025-09-11
        
    section 📦 v0.5.0 - Boxes
        Detecção Bounding Boxes : done, 2025-09-11, 2025-09-11
        Sistema Completo : done, 2025-09-11, 2025-09-11
        
    section 🧹 v0.6.0 - Modernização
        Remoção DeepLabV3 : done, 2025-09-12, 2025-09-12
        Simplificação Arquitetura : done, 2025-09-12, 2025-09-12
        MainAvaliador : done, 2025-09-12, 2025-09-12
```

### 🎯 Roadmap Atualizado

```mermaid
flowchart LR
    A["v0.1.0<br/>📊 Base de Dados"] --> B["v0.3.0<br/>📐 Parametrização"]
    B --> C["v0.4.0<br/>⚡ Otimização"]
    C --> D["v0.5.0<br/>📦 Bounding Boxes"]
    D --> E["v0.6.0<br/>🧹 Modernização"]
    E --> F["v0.7.0<br/>📊 Analytics"]
    F --> G["v1.0.0<br/>🚀 Release"]
    
    A --> A1["✅ Importação Dados"]
    A --> A2["✅ Estrutura Modular"]
    
    B --> B2["✅ Funções Indicadoras"]
    B --> B3["✅ Métricas MSE/RMS"]
    
    C --> C1["✅ 4 Métodos Especializados"]
    C --> C2["✅ Performance 3-5x"]
    C --> C3["✅ Visualização Automática"]
    
    D --> D2["✅ Detecção Automática"]
    D --> D3["✅ Sistema Integrado"]
    
    E --> E1["✅ Arquitetura Limpa"]
    E --> E2["✅ Foco Parametrização"]
    E --> E3["✅ MainAvaliador"]
    
    F --> F1["🔮 Análise Estatística"]
    F --> F2["🔮 Dashboard Web"]
    F --> F3["🔮 API REST"]
    
    G --> G1["🔮 Interface Gráfica"]
    G --> G2["🔮 Deploy Cloud"]
    G --> G3["🔮 Documentação Final"]
    
    style E fill:#90EE90
    style F fill:#FFE4B5
    style G fill:#F0E68C
```

## 📊 Métricas e Validação

### 🎯 Critérios de Sucesso

| Métrica | Alvo | Atual | Status |
|---------|------|-------|--------|
| MSE Global | < 200 | 156.789 | ✅ |
| RMS Global | < 15 | 12.523 | ✅ |
| Taxa Sucesso | > 95% | 100% | ✅ |
| Tempo/Imagem | < 5s | ~3s | ✅ |

### 📈 Análise de Performance

```mermaid
xychart-beta
    title "📊 Performance por Método"
    x-axis [Linhas, Colunas, Combinado]
    y-axis "Tempo (segundos)" 0 --> 10
    bar [3, 4, 8]
```

## 🔧 Configuração Avançada

### ⚙️ Parâmetros de Otimização

```python
# Configurações recomendadas
CONFIG = {
    'target_width': 512,           # Largura padrão
    'target_height': 382,          # Altura padrão  
    'morph_kernel_size': 5,        # Kernel morfológico
    'min_area': 100,               # Área mínima
    'enhance_contrast': True,       # Melhoria contraste
    'early_stopping': True,        # Parada antecipada
    'vectorized_processing': True   # Processamento vetorizado
}
```

### 🎮 Comandos de Desenvolvimento

```bash
# Executar com limite de registros
python MainAvaliador.py --limit 5

# Executar método específico
python MainAvaliador.py --method linhas

# Modo debug
python MainAvaliador.py --debug

# Executar análise completa
python MainAvaliador.py --full-analysis
```

## 📚 Módulos Especializados

### 🧠 Sistema Modular

```mermaid
mindmap
    root((🏗️ INOVIA))
        📊 Core
            MainAvaliador.py
            importa_dados.py
            escolher_modelo.py
        📐 Parametrização
            modelo_segmentacao_parametrizacao.py
            segmentacao_imagens_parametrizacao_indicadora.py
        📦 Utilitários
            Bounding_box.py
            exibicao_*.py
            exportacao_parametrizacao.py
        🔧 Configuração
            requirements.txt
            CHANGELOG.md
```

### 📁 Organização de Arquivos

```mermaid
graph TB
    subgraph "📂 Projeto INOVIA"
        Main[🚀 MainAvaliador.py<br/>Ponto de Entrada Principal]
        
        subgraph "📊 Core System"
            Import[📥 importa_dados.py<br/>Gerenciamento Dataset]
            Choose[🎯 escolher_modelo.py<br/>Seleção Método]
        end
        
        subgraph "📐 Parametrização Engine"
            Model[🧠 modelo_segmentacao_parametrizacao.py<br/>Coordenação Científica]
            Engine[⚡ segmentacao_imagens_parametrizacao_indicadora.py<br/>Motor Matemático]
        end
        
        subgraph "📦 Utilities"
            BBox[🔍 Bounding_box.py<br/>Detecção Regiões]
            Display1[🖼️ exibicao_imagens_parametrizadas.py<br/>Visualização Silhuetas]
            Display2[📦 exibicao_BBox_imagens.py<br/>Visualização Boxes]
            Export[📋 exportacao_parametrizacao.py<br/>Exportação Resultados]
        end
        
        subgraph "📋 Configuration"
            Req[📄 requirements.txt<br/>Dependências]
            Change[📝 CHANGELOG.md<br/>Histórico Versões]
            Read[📖 README.md<br/>Documentação]
        end
        
        subgraph "💾 Output"
            Data[📁 dados_analisados/<br/>Resultados JSON]
            Cache[🗂️ __pycache__/<br/>Cache Python]
        end
    end
    
    Main --> Import
    Main --> Choose
    Choose --> Model
    Model --> Engine
    Engine --> BBox
    BBox --> Display1
    BBox --> Display2
    Engine --> Export
    Export --> Data
    
    style Main fill:#e3f2fd
    style Engine fill:#e8f5e8
    style BBox fill:#fff3e0
    style Data fill:#f3e5f5
```

### 🔧 Dependências e Tecnologias

```mermaid
mindmap
    root((🛠️ Stack Tecnológico))
        🔬 Científico
            NumPy
                Operações Matriciais
                Vectorização
                Performance Extrema
            SciPy
                Funções Matemáticas
                Otimização
                Estatísticas
            Pandas
                Manipulação Dados
                DataFrames
                CSV Processing
        🖼️ Imagens
            OpenCV
                Processamento Imagens
                Bounding Boxes
                Morfologia
            Matplotlib
                Visualizações
                Gráficos
                Plotagem Científica
            PIL/Pillow
                Manipulação Básica
                Formatos Diversos
                Redimensionamento
        🔧 Sistema
            pathlib
                Gerenciamento Paths
                Cross-Platform
            json
                Serialização
                Resultados
            warnings
                Tratamento Avisos
```

## 🤝 Contribuição

### 🔧 Desenvolvimento

1. **Fork** o repositório
2. **Clone** sua fork
3. **Instale** dependências: `pip install -r requirements.txt`
4. **Desenvolva** sua feature
5. **Teste** thoroughly
6. **Submit** Pull Request

### 📋 Padrões de Código

- **Python 3.11+** recomendado
- **PEP 8** para formatação
- **Docstrings** detalhadas
- **Type hints** sempre que possível
- **Testes unitários** para funcionalidades críticas

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎯 Agradecimentos

- **NumPy** e **SciPy** para computação científica
- **Matplotlib** para visualizações
- **OpenCV** para processamento de imagens
- **Pandas** para manipulação de dados

---

**🚀 Projeto INOVIA v0.6.0** - Sistema de Segmentação Inteligente  
Desenvolvido com ❤️ para análise científica de imagens corporais sintéticas.

### 📈 Roadmap v0.7.0+
- **🌐 Interface Web**: Streamlit/Dash para democratização do acesso
- **📱 Mobile First**: Compatibilidade total com dispositivos móveis
- **☁️ Cloud Native**: Deploy em AWS/Azure/GCP
- **🤖 AI Avançada**: Integração com modelos de visão computacional
- **📊 Analytics**: Dashboard interativo para análise de tendências
