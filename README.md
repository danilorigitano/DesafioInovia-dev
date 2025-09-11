# 🚀 Projeto INOVIA - Sistema de Segmentação Inteligente

Sistema modular avançado para processamento e análise de dados de imagens sintéticas com medidas corporais, integrando deep learning e métodos matemáticos otimizados.

```mermaid
graph LR
    A[�️ Imagens Sintéticas] --> B[🧠 Processamento IA]
    B --> C[📊 Análise Corporal]
    C --> D[📋 Relatórios]
    
    B --> B1[DeepLabV3]
    B --> B2[Parametrização]
    B --> B3[Bounding Boxes]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

�🚀 **Versão 0.5.0** - Detecção de Bounding Boxes nas Silhuetas!  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico completo de desenvolvimento

## 📋 Visão Geral do Sistema

O Projeto INOVIA é uma solução completa e inovadora para segmentação e análise de imagens corporais sintéticas, oferecendo:

- **🧠 Inteligência Artificial Avançada**: Integração de DeepLabV3 com ResNet101 para segmentação semântica de alta precisão
- **📐 Métodos Matemáticos Otimizados**: Algoritmos de parametrização por funções indicadoras com 4 abordagens especializadas
- **📦 Detecção Automática de Regiões**: Sistema de bounding boxes para localização precisa das áreas de interesse
- **⚡ Performance Extrema**: Otimizações NumPy com processamento 3-5x mais rápido e early stopping inteligente
- **📊 Análise Comparativa**: Métricas detalhadas e visualizações especializadas para cada método

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
            DeepLabV3
            4 Métodos Parametrização
            Escolha Inteligente
        📊 Análise Completa
            Segmentação Multidimensional
            Métodos Combinados
            Relatórios Automáticos
        📦 Bounding Boxes
            Detecção Automática
            Localização Precisa
            Métricas Detalhadas
        🖼️ Visualização Avançada
            Interface Interativa
            Overlays Especializados
            Análise Comparativa
```

- **🔬 Precisão Científica**: Algoritmos validados com métricas rigorosas (MSE < 200)
- **⚡ Performance Extrema**: Otimizações NumPy com processamento 3-5x mais rápido
- **🎛️ Flexibilidade Total**: Múltiplos métodos de segmentação (DeepLabV3 + 4 Parametrizações)
- **📊 Análise Completa**: Segmentação por linhas, colunas e métodos combinados
- **📦 Bounding Boxes**: Detecção automática de retângulos delimitadores nas silhuetas
- **🖼️ Visualização Avançada**: Interface interativa com overlays especializados
- **📈 Métricas Detalhadas**: Relatórios automáticos com estatísticas de qualidade

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos do Sistema

```mermaid
graph TD
    subgraph "💻 Ambiente Base"
        A[🐍 Python 3.8+]
        B[💾 8GB RAM mínimo]
        C[📁 2GB espaço disco]
        D[🖥️ CPU Multi-core]
    end
    
    subgraph "🎮 GPU (Opcional)"
        E[🚀 NVIDIA GPU]
        F[⚡ CUDA 11.0+]
        G[📊 4GB VRAM]
        H[🔧 cuDNN]
    end
    
    subgraph "📚 Dependências Python"
        I[📊 NumPy 1.21+]
        J[🧠 PyTorch 2.0+]
        K[🖼️ OpenCV 4.5+]
        L[📈 Matplotlib 3.5+]
        M[📋 Pandas 1.3+]
    end
    
    A --> I
    B --> J
    C --> K
    D --> L
    E --> F
    F --> G
    G --> H
    
    style A fill:#306998,color:#fff
    style E fill:#76b900,color:#fff
    style I fill:#4dabf7,color:#fff
```

### ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/danilorigitano/DesafioInovia-dev.git
cd DesafioInovia-dev

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
python main.py
```

### 🔧 Configuração Avançada

```mermaid
flowchart LR
    subgraph "📦 Dependências Principais"
        A[🐍 torch>=2.0.0]
        B[🖼️ torchvision>=0.15.0]
        C[📊 numpy>=1.21.0]
        D[🎨 opencv-python>=4.5.0]
        E[📈 matplotlib>=3.5.0]
        F[📋 pandas>=1.3.0]
        G[🔬 scipy>=1.7.0]
        H[🎨 Pillow>=8.3.0]
    end
    
    subgraph "⚙️ Configuração GPU"
        I[🔍 Detectar CUDA]
        J[📥 Instalar PyTorch GPU]
        K[⚡ Configurar cuDNN]
        L[✅ Validar instalação]
    end
    
    A --> I
    B --> J
    I --> J
    J --> K
    K --> L
    
    style A fill:#ee4c2c,color:#fff
    style I fill:#76b900,color:#fff
```

### 📁 Estrutura de Dados Necessária

```mermaid
graph TD
    subgraph "📂 Estrutura Obrigatória"
        A[📁 projeto_raiz/]
        A --> B[📄 medidas_dados_sinteticos.csv]
        A --> C[📁 INOVIA_IMAGENS/]
        
        C --> D[📁 syn_fXXXXXX-X-Pre/]
        C --> E[📁 syn_fXXXXXX-X-Pos/]
        C --> F[📁 syn_mXXXXXX-X-Pre/]
        C --> G[📁 syn_mXXXXXX-X-Pos/]
        
        D --> H[🖼️ front.png]
        D --> I[🖼️ left.png]
        E --> J[🖼️ front.png]
        E --> K[🖼️ left.png]
    end
    
    style A fill:#e3f2fd,stroke:#1976d2
    style B fill:#fff3e0,stroke:#f57c00
    style C fill:#e8f5e8,stroke:#388e3c
```

## 🎯 Guia de Uso Rápido

### 🚀 Execução Principal

```mermaid
graph LR
    A[▶️ Executar main.py] --> B{📊 Dados Válidos?}
    B -->|✅ Sim| C[🎛️ Escolher Método]
    B -->|❌ Não| D[🔧 Configurar Dados]
    C --> E[🖼️ Processar Imagens]
    E --> F[📊 Ver Resultados]
    D --> A
    
    style A fill:#4caf50,color:#fff
    style C fill:#2196f3,color:#fff
    style F fill:#ff9800,color:#fff
```

### 📋 Menu Interativo

```bash
🎯 Sistema INOVIA - Escolha do Método de Segmentação

1️⃣ 🧠 DeepLabV3 + ResNet101 (Alta Precisão)
   ├── ⚡ GPU/CPU automático
   ├── 🎯 Segmentação semântica
   └── 📊 Confidence scores

2️⃣ 📐 Parametrização v0.4.0 (Alta Velocidade)
   ├── 📏 Método por Linhas (768 funções)
   ├── 📐 Método por Colunas (1024 funções)
   ├── 🔗 Método Combinado (fusão inteligente)
   └── 🔄 Separado + União (análise comparativa)

Digite sua escolha [1-2]: _
```

### 🔍 Exemplos de Uso Específicos

```mermaid
graph TD
    subgraph "🧠 Uso DeepLabV3"
        A1[python main.py]
        A1 --> A2[Escolher opção 1]
        A2 --> A3[🔄 Aguardar processamento ~15s]
        A3 --> A4[📊 Visualizar resultados alta precisão]
    end
    
    subgraph "📐 Uso Parametrização Rápida"
        B1[python main.py]
        B1 --> B2[Escolher opção 2]
        B2 --> B3{🎛️ Submenu Método}
        B3 --> B4[📏 Linhas: ~1-2s]
        B3 --> B5[📐 Colunas: ~1-2s]
        B3 --> B6[🔗 Combinado: ~2-3s]
        B3 --> B7[🔄 Separado: ~3-4s]
    end
    
    subgraph "📦 Uso Bounding Boxes"
        C1[python exemplo_bounding_box.py]
        C1 --> C2[🖼️ Selecionar imagem]
        C2 --> C3[🔍 Detectar retângulos]
        C3 --> C4[📊 Visualizar métricas]
    end
    
    style A1,B1,C1 fill:#4caf50,color:#fff
    style A4,B4,B5,B6,B7,C4 fill:#2196f3,color:#fff
```

### 📊 Interpretar Resultados

```mermaid
graph LR
    subgraph "📈 Métricas Principais"
        A[📊 MSE < 200] --> A1[✅ Qualidade Excelente]
        B[🎯 IoU > 0.8] --> B1[✅ Precisão Alta]
        C[⏱️ Tempo < 5s] --> C1[✅ Performance Ótima]
    end
    
    subgraph "🎨 Visualizações"
        D[🔴 Overlay Vermelho] --> D1[📏 Segmentação Linhas]
        E[🟢 Overlay Verde] --> E1[📐 Segmentação Colunas]
        F[🔵 Overlay Azul] --> F1[🔗 Método Combinado]
        G[🟣 Overlay Magenta] --> G1[🔄 Separado + União]
    end
    
    subgraph "📦 Arquivos Gerados"
        H[📄 resultados_*.json] --> H1[📊 Métricas detalhadas]
        I[🖼️ mascara_*.png] --> I1[📱 Imagem processada]
        J[📈 graficos_*.png] --> J1[📊 Análises visuais]
    end
```

## 🎯 Evolução do Desenvolvimento

```mermaid
graph TD
    A["v0.1.0<br/>📊 Base de Dados"] --> B["v0.2.0<br/>🖼️ Segmentação DeepLabV3"]
    B --> C["v0.2.1<br/>🔧 Refatoração"]
    C --> D["v0.2.2<br/>🎛️ Múltiplos Modelos"]
    D --> E["v0.2.3<br/>⚡ Otimizações Avançadas"]
    E --> F["v0.3.0<br/>🔗 Extensão Completa"]
    F --> G["v0.4.0<br/>📊 Segmentação Multidimensional"]
    G --> H["v0.5.0<br/>📦 Bounding Boxes"]
    H --> I["v0.6.0<br/>🧮 Analytics Avançados"]
    
    A --> A1["✅ Validação CSV/Imagens"]
    A --> A2["✅ Estruturação por Gênero"]
    A --> A3["✅ Relatórios Automáticos"]
    
    B --> B1["✅ Modelo DeepLabV3"]
    B --> B2["✅ Processamento GPU/CPU"]
    B --> B3["✅ Visualização Interativa"]
    
    C --> C1["✅ Nomenclatura Clara"]
    C --> C2["✅ Código Limpo"]
    C --> C3["✅ Arquitetura Modular"]
    
    D --> D1["✅ DeepLabV3 + ResNet101"]
    D --> D2["✅ Parametrização Indicadora"]
    D --> D3["✅ Interface de Escolha"]
    
    E --> E1["✅ Vectorização NumPy"]
    E --> E2["✅ Processamento em Batches"]
    E --> E3["✅ Early Stopping MSE"]
    
    F --> F1["✅ Segmentação por Colunas"]
    F --> F2["✅ Segmentação Combinada"]
    F --> F3["✅ Análise Comparativa"]
    
    G --> G1["✅ 768 Funções Horizontais"]
    G --> G2["✅ 1024 Funções Verticais"]
    G --> G3["✅ Segmentação Separada + União"]
    
    H --> H1["🔄 Correlações Automáticas"]
    H --> H2["🔄 Dashboard Interativo"]
    H --> H3["🔄 Métricas Avançadas"]
    
    classDef implemented fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef current fill:#2196F3,stroke:#1976D2,color:#fff
    classDef future fill:#FF9800,stroke:#F57C00,color:#fff
    
    class A,B,C,D,E,F,G,A1,A2,A3,B1,B2,B3,C1,C2,C3,D1,D2,D3,E1,E2,E3,F1,F2,F3,G1,G2,G3 implemented
    class H current
    class H1,H2,H3 future
```

## 🏗️ Arquitetura do Sistema

### 📊 Fluxo Principal de Dados

```mermaid
flowchart TD
    Start([🚀 Início do Sistema<br/>main.py]) --> ValidData[📂 Validar Dados CSV/Imagens<br/>ImportadorDados]
    ValidData --> StructData[🏗️ Estruturar por Gênero/Posição<br/>Masculino/Feminino - Pre/Pos]
    StructData --> DatasetSelect[📊 Selecionar Dataset<br/>Índice específico]
    DatasetSelect --> ChooseModel{🎛️ Escolher Modelo<br/>escolher_modelo.py}
    
    ChooseModel -->|1️⃣| DeepLabV3[🧠 DeepLabV3 + ResNet101<br/>Alta Precisão]
    ChooseModel -->|2️⃣| Parametrizacao[📐 Parametrização v0.4.0<br/>Alta Velocidade]
    
    DeepLabV3 --> DLProcess[🎯 Segmentação Semântica<br/>PyTorch + GPU/CPU<br/>Threshold Adaptativo]
    Parametrizacao --> MethodChoice{🔧 Método Parametrização<br/>4 Opções Especializadas}
    
    MethodChoice -->|1️⃣| LinhasMethod[📏 768 Funções Horizontais<br/>Parâmetros a,b<br/>Segmentação por Linhas]
    MethodChoice -->|2️⃣| ColunasMethod[📐 1024 Funções Verticais<br/>Parâmetros c,d<br/>Segmentação por Colunas]
    MethodChoice -->|3️⃣| CombinedMethod[🔗 Método Combinado<br/>Fusão Inteligente<br/>Linhas + Colunas]
    MethodChoice -->|4️⃣| SeparatedMethod[🔄 Separado + União<br/>Processamento Independente]
    
    LinhasMethod --> VectorProcess[⚡ Vectorização NumPy<br/>Early Stop MSE < 200<br/>Batch Processing]
    ColunasMethod --> VectorProcess
    CombinedMethod --> VectorProcess
    SeparatedMethod --> VectorProcess
    
    DLProcess --> Results[📊 Processamento Completo<br/>Métricas + Visualizações]
    VectorProcess --> Results
    
    Results --> Analysis{📈 Tipo de Análise<br/>Individual/Comparativa/Combinada}
    Analysis -->|Individual| IndividualMetrics[📊 Métricas Individuais<br/>MSE específico por método]
    Analysis -->|Comparativa| ComparativeMetrics[🔄 Análise Comparativa<br/>4 métodos lado a lado]
    Analysis -->|Combinada| CombinedMetrics[🔗 Métricas Combinadas<br/>União + Interseção]
    
    IndividualMetrics --> Visualizations[🖼️ Visualizações Especializadas<br/>Overlays + Histogramas]
    ComparativeMetrics --> Visualizations
    CombinedMetrics --> Visualizations
    
    Visualizations --> SaveJSON[💾 Salvar Resultados JSON<br/>Estatísticas + Parâmetros]
    SaveJSON --> End([✅ Processamento Concluído<br/>Relatório Gerado])
    
    classDef start fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef process fill:#2196F3,stroke:#1976D2,color:#fff
    classDef decision fill:#FF9800,stroke:#F57C00,color:#fff
    classDef model fill:#9C27B0,stroke:#7B1FA2,color:#fff
    classDef analysis fill:#795548,stroke:#5D4037,color:#fff
    classDef output fill:#F44336,stroke:#C62828,color:#fff
    classDef finalization fill:#607D8B,stroke:#455A64,color:#fff
    
    class Start,End start
    class ValidData,StructData,DatasetSelect,Results,Visualizations,SaveJSON process
    class ChooseModel,MethodChoice,Analysis decision
    class DeepLabV3,Parametrizacao,LinhasMethod,ColunasMethod,CombinedMethod,SeparatedMethod,DLProcess,VectorProcess model
    class IndividualMetrics,ComparativeMetrics,CombinedMetrics analysis
```

### 🎛️ Sistema de Escolha de Modelos Expandido

```mermaid
graph TB
    subgraph "🎯 Interface de Seleção"
        Menu[📋 Menu Interativo<br/>escolher_modelo.py]
        User{👤 Escolha do Usuário<br/>1-2 + Submenu}
        Menu --> User
    end
    
    subgraph "🧠 Pipeline DeepLabV3"
        DL_Config[🔧 Configuração Automática<br/>GPU/CPU Detection]
        DL_Model[ModeloSegmentacaoDeepLabV3<br/>ResNet101 Backbone]
        DL_Engine[SegmentacaoDeepLabV3<br/>Threshold Adaptativo]
        DL_Features[🎯 PyTorch + ResNet101<br/>📊 Alta Precisão<br/>⚙️ GPU/CPU Adaptativo<br/>🎨 Visualização Avançada]
        
        DL_Config --> DL_Model
        DL_Model --> DL_Engine
        DL_Engine --> DL_Features
    end
    
    subgraph "📐 Pipeline Parametrização v0.4.0"
        Param_Config[🔧 Configuração Otimizada<br/>Resolução 1024x768]
        Param_Model[ModeloSegmentacaoParametrizacao<br/>Múltiplos Métodos]
        Param_Engine[SegmentacaoParametrizacaoIndicadora<br/>Early Stopping MSE]
        Param_Choice{🎛️ Método Específico<br/>4 Opções Expandidas}
        
        Param_Config --> Param_Model
        Param_Model --> Param_Engine
        Param_Engine --> Param_Choice
        
        Param_Choice -->|1️⃣| Linhas_Features[📏 768 Funções Horizontais<br/>⚡ Vectorização NumPy<br/>🎯 Early Stopping MSE < 200<br/>📊 Parâmetros a,b otimizados]
        Param_Choice -->|2️⃣| Colunas_Features[📐 1024 Funções Verticais<br/>🔬 Parâmetros c,d<br/>📊 Análise Perpendicular<br/>⚡ Processamento Vectorizado]
        Param_Choice -->|3️⃣| Combined_Features[🔗 Método Híbrido<br/>🎨 Múltiplas Fusões<br/>📈 Análise Comparativa<br/>🔄 União + Interseção]
        Param_Choice -->|4️⃣| Separated_Features[🔄 Separado + União<br/>📊 Processamento Independente<br/>🎯 Análise Individual<br/>📈 Métricas Comparativas]
    end
    
    User -->|1️⃣ DeepLabV3| DL_Config
    User -->|2️⃣ Parametrização| Param_Config
    
    DL_Features --> Results[📊 Resultados Unificados<br/>JSON + Visualizações]
    Linhas_Features --> Results
    Colunas_Features --> Results
    Combined_Features --> Results
    Separated_Features --> Results
    
    classDef interface fill:#E1F5FE,stroke:#0277BD
    classDef deeplab fill:#E8F5E8,stroke:#388E3C
    classDef param fill:#FFF3E0,stroke:#F57C00
    classDef methods fill:#F3E5F5,stroke:#7B1FA2
    classDef output fill:#FFEBEE,stroke:#C62828
    classDef advanced fill:#E0F2F1,stroke:#00695C
    
    class Menu,User interface
    class DL_Config,DL_Model,DL_Engine,DL_Features deeplab
    class Param_Config,Param_Model,Param_Engine,Param_Choice param
    class Linhas_Features,Colunas_Features,Combined_Features methods
    class Separated_Features advanced
    class Results output
```

### 📊 Arquitetura de Dados e Performance

```mermaid
graph TD
    subgraph "📊 Estrutura de Dados"
        CSV[📄 Arquivo CSV<br/>Dados Corporais]
        Images[🖼️ Pastas de Imagens<br/>syn_[m/f]XXXXXX-X-[Pre/Pos]]
        
        CSV --> Validation{🔍 Validação<br/>CSV ↔ Imagens}
        Images --> Validation
        
        Validation --> Structure[🏗️ Estruturação<br/>Por Gênero/Posição]
        Structure --> Dataset[📦 Dataset Válido<br/>Registros Correspondentes]
    end
    
    subgraph "⚡ Performance v0.4.0"
        Input[🔢 Entrada: 1024x768]
        
        Input --> DeepLabTime[🧠 DeepLabV3<br/>~15s por imagem<br/>Alta Precisão]
        Input --> ParamTime[📐 Parametrização<br/>~1-2s por método<br/>Alta Velocidade]
        
        DeepLabTime --> DeepLabResult[📊 Resultado DL<br/>Confidence + IoU]
        ParamTime --> ParamResult[📊 Resultado Param<br/>MSE < 200]
        
        ParamResult --> Methods{🎛️ Múltiplos Métodos}
        Methods --> M1[📏 Linhas: ~1-2s]
        Methods --> M2[📐 Colunas: ~1-2s]
        Methods --> M3[🔗 Combinado: ~2-3s]
        Methods --> M4[🔄 Separado: ~3-4s]
    end
    
    subgraph "🎯 Otimizações Técnicas"
        Vector[⚡ Vectorização NumPy<br/>3-5x Velocidade]
        Batch[📦 Processamento Batches<br/>50 funções simultâneas]
        Early[🎯 Early Stopping<br/>MSE < 200 automático]
        Memory[💾 Gestão Memória<br/>Otimizada para grandes datasets]
        
        Vector --> Batch
        Batch --> Early
        Early --> Memory
    end
    
    Dataset --> Input
    DeepLabResult --> Analytics[📈 Analytics Unificados]
    M1 --> Analytics
    M2 --> Analytics
    M3 --> Analytics
    M4 --> Analytics
    Memory --> Analytics
    
    classDef data fill:#E3F2FD,stroke:#1976D2
    classDef performance fill:#F3E5F5,stroke:#7B1FA2
    classDef optimization fill:#E8F5E8,stroke:#388E3C
    classDef result fill:#FFF3E0,stroke:#F57C00
    
    class CSV,Images,Validation,Structure,Dataset data
    class Input,DeepLabTime,ParamTime,Methods,M1,M2,M3,M4 performance
    class Vector,Batch,Early,Memory optimization
    class DeepLabResult,ParamResult,Analytics result
```

## 🔄 Fluxo de Desenvolvimento e Roadmap

```mermaid
timeline
    title 🚀 Linha do Tempo do Projeto INOVIA
    
    section v0.1.0 - Fundação
        2025-09-08 : 📊 Base de Dados
                  : ✅ Validação CSV/Imagens
                  : ✅ Estruturação por Gênero
                  : ✅ Relatórios Automáticos
    
    section v0.2.0 - Segmentação
        2025-09-08 : 🖼️ Segmentação DeepLabV3
                  : ✅ Modelo ResNet50
                  : ✅ Processamento GPU/CPU
                  : ✅ Visualização Interativa
    
    section v0.2.1 - Refatoração
        2025-09-09 : 🔧 Refatoração Inteligente
                  : ✅ Nomenclatura Clara
                  : ✅ Código Limpo
                  : ✅ Arquitetura Modular
    
    section v0.2.2 - Múltiplos Modelos
        2025-09-09 : 🎛️ Sistema de Escolha
                  : ✅ DeepLabV3 + ResNet101
                  : ✅ Parametrização Indicadora
                  : ✅ Interface de Escolha
    
    section v0.2.3 - Otimizações
        2025-09-09 : ⚡ Performance Extrema
                  : ✅ Vectorização NumPy
                  : ✅ Early Stopping MSE
                  : ✅ Processamento Batches
    
    section v0.4.0 - Multidimensional
        2025-09-10 : 🌟 Segmentação 4 Métodos
                  : ✅ 768 Funções Horizontais
                  : ✅ 1024 Funções Verticais
                  : ✅ Método Combinado
                  : ✅ Separado + União
    
    section v0.5.0 - Analytics
        Futuro    : 🧮 Analytics Avançados
                  : 🔄 Correlações Automáticas
                  : 📊 Dashboard Interativo
                  : 📈 Métricas Avançadas
    
    section v0.6.0 - Interface Web
        Futuro    : 🌐 Interface Gráfica
                  : 🖥️ Streamlit/Dash
                  : 👥 Multi-usuário
                  : 📱 Responsivo
```

### 💾 Arquitetura de Arquivos do Projeto

```mermaid
graph TD
    subgraph "📂 Estrutura Principal"
        Main[📄 main.py<br/>Coordenador Principal]
        Import[📄 importa_dados.py<br/>Gerenciamento Dados]
        Choose[📄 escolher_modelo.py<br/>Seleção de Modelos]
        
        Main --> Import
        Main --> Choose
    end
    
    subgraph "🧠 Módulos DeepLabV3"
        ModelDL[📄 modelo_segmentacao_Deeplabv3.py<br/>Wrapper do Modelo]
        SegmentDL[📄 segmentacao_imagens_Deeplabv3.py<br/>Engine de Processamento]
        
        Choose --> ModelDL
        ModelDL --> SegmentDL
    end
    
    subgraph "📐 Módulos Parametrização"
        ModelParam[📄 modelo_segmentacao_parametrizacao.py<br/>Wrapper Parametrização]
        SegmentParam[📄 segmentacao_imagens_parametrizacao_indicadora.py<br/>Engine 4 Métodos]
        
        Choose --> ModelParam
        ModelParam --> SegmentParam
    end
    
    subgraph "🎨 Módulos Visualização"
        Display[📄 exibicao_imagens_parametrizadas.py<br/>Visualizações Especializadas]
        
        SegmentParam --> Display
        SegmentDL --> Display
    end
    
    subgraph "📦 Módulos Bounding Box"
        BBox[📄 Bounding_box.py<br/>Detecção de Retângulos]
        DisplayBBox[📄 exibicao_BBox_imagens.py<br/>Visualização BBoxes]
        ExemploBBox[📄 exemplo_bounding_box.py<br/>Demonstração Completa]
        
        SegmentParam --> BBox
        BBox --> DisplayBBox
        BBox --> ExemploBBox
        DisplayBBox --> ExemploBBox
    end
    
    subgraph "📊 Configuração e Dados"
        Requirements[📄 requirements.txt<br/>Dependências Python]
        README[📄 README.md<br/>Documentação]
        CHANGELOG[📄 CHANGELOG.md<br/>Histórico Versões]
        Cache[📂 __pycache__/<br/>Python Bytecode]
        
        Main -.-> Requirements
        README -.-> CHANGELOG
    end
    
    classDef main fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef deeplab fill:#2196F3,stroke:#1976D2,color:#fff
    classDef param fill:#FF9800,stroke:#F57C00,color:#fff
    classDef visual fill:#9C27B0,stroke:#7B1FA2,color:#fff
    classDef bbox fill:#E91E63,stroke:#C2185B,color:#fff
    
    class BBox,DisplayBBox,ExemploBBox bbox
    classDef config fill:#607D8B,stroke:#455A64,color:#fff
    
    class Main,Import,Choose main
    class ModelDL,SegmentDL deeplab
    class ModelParam,SegmentParam param
    class Display visual
    class Requirements,README,CHANGELOG,Cache config
```

### 🔍 Comparação de Métodos de Segmentação

```mermaid
graph LR
    subgraph "🧠 DeepLabV3 Method"
        DL_Input[🖼️ Input Image<br/>Original Resolution]
        DL_Process[🔥 PyTorch Processing<br/>ResNet101 Backbone]
        DL_Output[🎯 Semantic Mask<br/>High Precision]
        
        DL_Input --> DL_Process
        DL_Process --> DL_Output
        
        DL_Metrics[📊 Metrics:<br/>• IoU Score<br/>• Confidence<br/>• Processing Time: ~15s<br/>• GPU Recommended]
        DL_Output --> DL_Metrics
    end
    
    subgraph "📐 Parametrization Methods"
        P_Input[🖼️ Input Image<br/>1024x768]
        
        P_Input --> P1[📏 Lines Method<br/>768 Horizontal Functions<br/>Parameters a,b]
        P_Input --> P2[📐 Columns Method<br/>1024 Vertical Functions<br/>Parameters c,d]
        P_Input --> P3[🔗 Combined Method<br/>Smart Fusion<br/>Lines + Columns]
        P_Input --> P4[🔄 Separated + Union<br/>Independent Processing<br/>Individual Analysis]
        
        P1 --> P1_Out[📊 Output Lines<br/>MSE < 200<br/>~1-2s]
        P2 --> P2_Out[📊 Output Columns<br/>MSE < 200<br/>~1-2s]
        P3 --> P3_Out[📊 Combined Output<br/>Weighted MSE<br/>~2-3s]
        P4 --> P4_Out[📊 Union Output<br/>Comparative Analysis<br/>~3-4s]
        
        P1_Out --> P_Analysis[🎨 Comparative Analysis<br/>4 Methods Side by Side]
        P2_Out --> P_Analysis
        P3_Out --> P_Analysis
        P4_Out --> P_Analysis
    end
    
    subgraph "⚖️ Method Comparison"
        Compare[🔄 Performance vs Precision<br/>DeepLabV3 vs Parametrization]
        
        Compare --> Precision[🎯 Precision:<br/>DeepLabV3: ⭐⭐⭐⭐⭐<br/>Parametrization: ⭐⭐⭐⭐]
        Compare --> Speed[⚡ Speed:<br/>DeepLabV3: ⭐⭐<br/>Parametrization: ⭐⭐⭐⭐⭐]
        Compare --> Resources[💻 Resources:<br/>DeepLabV3: GPU + 4GB VRAM<br/>Parametrization: CPU + 2GB RAM]
    end
    
    DL_Metrics --> Compare
    P_Analysis --> Compare
    
    classDef deeplab fill:#1976D2,stroke:#0D47A1,color:#fff
    classDef param fill:#388E3C,stroke:#1B5E20,color:#fff
    classDef comparison fill:#F57C00,stroke:#E65100,color:#fff
    classDef metrics fill:#7B1FA2,stroke:#4A148C,color:#fff
    classDef output fill:#D32F2F,stroke:#B71C1C,color:#fff
    
    class DL_Input,DL_Process,DL_Output deeplab
    class P_Input,P1,P2,P3,P4 param
    class Compare,Precision,Speed,Resources comparison
    class DL_Metrics,P1_Out,P2_Out,P3_Out,P4_Out,P_Analysis metrics
```
```
### 🔧 Diagrama de Tecnologias e Dependências

```mermaid
graph LR
    subgraph "🐍 Python Ecosystem"
        Python[🐍 Python 3.8+<br/>Core Language]
        NumPy[🔢 NumPy<br/>Vectorização]
        Pandas[📊 Pandas<br/>Manipulação Dados]
        Matplotlib[📈 Matplotlib<br/>Visualizações]
        
        Python --> NumPy
        Python --> Pandas
        Python --> Matplotlib
    end
    
    subgraph "🧠 Deep Learning Stack"
        PyTorch[� PyTorch 2.0+<br/>Neural Networks]
        TorchVision[�️ TorchVision<br/>Computer Vision]
        CUDA[⚡ CUDA<br/>GPU Acceleration]
        
        PyTorch --> TorchVision
        PyTorch --> CUDA
    end
    
    subgraph "🖼️ Image Processing"
        OpenCV[📷 OpenCV<br/>Image Operations]
        PIL[🎨 Pillow<br/>Image I/O]
        Scipy[🔬 SciPy<br/>Scientific Computing]
        
        OpenCV --> PIL
        PIL --> Scipy
    end
    
    subgraph "🎯 Models & Algorithms"
        DeepLabV3[🧠 DeepLabV3<br/>Semantic Segmentation]
        ResNet101[�️ ResNet101<br/>Backbone CNN]
        IndicatorFunc[📐 Funções Indicadoras<br/>Parametrização Matemática]
        
        DeepLabV3 --> ResNet101
        IndicatorFunc --> NumPy
    end
    
    NumPy --> IndicatorFunc
    PyTorch --> DeepLabV3
    OpenCV --> DeepLabV3
    Scipy --> IndicatorFunc
    
    classDef python fill:#306998,stroke:#FFD43B,color:#fff
    classDef dl fill:#EE4C2C,stroke:#FF6B35,color:#fff
    classDef image fill:#5C85D6,stroke:#2C5AA0,color:#fff
    classDef model fill:#FF6B35,stroke:#D74315,color:#fff
    
    class Python,NumPy,Pandas,Matplotlib python
    class PyTorch,TorchVision,CUDA dl
    class OpenCV,PIL,Scipy image
    class DeepLabV3,ResNet101,IndicatorFunc model
```
        
        Param_Config --> Param_Model
        Param_Model --> Param_Engine
        Param_Engine --> Param_Features
    end
    
    User -->|1️⃣ DeepLabV3| DL_Config
    User -->|2️⃣ Parametrização| Param_Config
    
    DL_Features --> Results[📊 Resultados Unificados]
    Param_Features --> Results
    
    classDef interface fill:#E1F5FE,stroke:#0277BD
    classDef deeplab fill:#E8F5E8,stroke:#388E3C
    classDef param fill:#FFF3E0,stroke:#F57C00
    classDef output fill:#F3E5F5,stroke:#7B1FA2
    
    class Menu,User interface
    class DL_Config,DL_Model,DL_Engine,DL_Features deeplab
    class Param_Config,Param_Model,Param_Engine,Param_Features param
    class Results output
```

### ⚡ Otimizações de Performance v0.4.0

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant M as 🎯 main.py
    participant E as 🎛️ escolher_modelo.py
    participant P as 📐 Parametrização
    participant V as ⚡ Vectorização
    participant A as 📊 Análise
    
    U->>M: python main.py
    M->>M: 📋 Exibir cabeçalho v0.4.0
    M->>M: 📂 Validar dados
    M->>E: 🎛️ Inicializar modelo
    
    E->>U: 🎯 Menu de seleção
    U->>E: 2️⃣ Parametrização
    E->>U: 🔧 Submenu método
    U->>E: Escolha específica
    E->>P: 🔧 Criar modelo otimizado
    
    M->>P: ⚡ Processar dataset
    
    alt Método por Linhas
        P->>P: 📏 Redimensionar 1024x768
        P->>V: 🧮 Gerar 768 funções horizontais
        V->>V: ⚡ Processamento matricial a,b
        V->>P: 📊 MSE vectorizado < 200
    else Método por Colunas  
        P->>P: 📐 Redimensionar 1024x768
        P->>V: 🧮 Gerar 1024 funções verticais
        V->>V: ⚡ Processamento matricial c,d
        V->>P: 📊 MSE vectorizado < 200
    else Método Combinado
        P->>P: 🔗 Processar ambos os métodos
        P->>V: 🧮 Funções horizontais + verticais
        V->>V: ⚡ Fusão inteligente
        V->>P: 📊 MSE combinado
    end
    
    P->>A: � Análise comparativa
    A->>A: �🔄 Métricas individuais/combinadas
    A->>M: 📊 Resultados + métricas
    M->>M: 🖼️ Visualizar resultados especializados
    M->>U: ✅ Processamento concluído
```

### 🎯 Arquitetura de Segmentação Multidimensional v0.4.0

```mermaid
graph TB
    subgraph "📊 Entrada de Dados"
        A1["📄 medidas_dados_sinteticos.csv"]
        A2["📂 INOVIA_IMAGENS/"]
        A2 --> A21["syn_fXXXXXX-X-Pre/front.png"]
        A2 --> A22["syn_fXXXXXX-X-Pre/left.png"]
        A2 --> A23["syn_fXXXXXX-X-Pos/front.png"]
        A2 --> A24["syn_fXXXXXX-X-Pos/left.png"]
    end
    
    subgraph "🔧 Processamento"
        B1["main.py<br/>🎯 Coordenador"]
        B2["importa_dados.py<br/>� Validação"]
        B3["escolher_modelo.py<br/>🎛️ Seleção"]
        
        B1 --> B2
        B2 --> B3
    end
    
    subgraph "🧠 Modelo DeepLabV3"
        C1["ModeloSegmentacaoDeepLabV3"]
        C2["SegmentacaoDeepLabV3"]
        C3["🎯 PyTorch + ResNet101"]
        
        C1 --> C2
        C2 --> C3
    end
    
    subgraph "📐 Modelo Parametrização v0.4.0"
        D1["ModeloSegmentacaoParametrizacao"]
        D2["SegmentacaoParametrizacaoIndicadora"]
        D3{🎛️ Método Específico}
        
        D1 --> D2
        D2 --> D3
        
        D3 -->|1️⃣| D4["� 768 Funções Horizontais<br/>segmentar()"]
        D3 -->|2️⃣| D5["📐 1024 Funções Verticais<br/>segmentar_por_colunas()"]
        D3 -->|3️⃣| D6["🔗 Método Combinado<br/>segmentar_combinado()"]
        D3 -->|4️⃣| D7["🔄 Separado + União<br/>segmentar_separado_e_unido()"]
    end
    
    subgraph "📊 Análise Avançada"
        E1["📈 Métricas Individuais"]
        E2["🔄 Análise Comparativa"]
        E3["🔗 Métricas Combinadas"]
        E4["📊 Estatísticas MSE"]
    end
    
    subgraph "� Saída"
        F1["📊 Relatórios JSON"]
        F2["�🖼️ Máscaras Processadas"]
        F3["🎨 Visualizações Especializadas"]
        F4["📈 Gráficos Comparativos"]
    end
    
    A1 --> B2
    A2 --> B2
    B3 --> C1
    B3 --> D1
    
    C3 --> E1
    D4 --> E1
    D5 --> E1
    D6 --> E3
    D7 --> E2
    
    E1 --> F1
    E2 --> F2
    E3 --> F3
    E1 --> F4
    E2 --> F4
    E3 --> F4
    
    classDef input fill:#e3f2fd,stroke:#1976d2
    classDef processing fill:#f3e5f5,stroke:#7b1fa2
    classDef models fill:#e8f5e8,stroke:#388e3c
    classDef methods fill:#fff3e0,stroke:#f57c00
    classDef analysis fill:#fce4ec,stroke:#c2185b
    classDef output fill:#e0f2f1,stroke:#00695c
    
    class A1,A2,A21,A22,A23,A24 input
    class B1,B2,B3 processing
    class C1,C2,C3,D1,D2,D3 models
    class D4,D5,D6,D7 methods
    class E1,E2,E3,E4 analysis
    class F1,F2,F3,F4 output
```

### ⚡ v0.4.0 - Segmentação Multidimensional (ATUAL)
O sistema agora oferece **análise completa em múltiplas dimensões** com métodos especializados!

**🚀 Novos Recursos:**
- **📏 Segmentação por Linhas**: 768 funções indicadoras horizontais com parâmetros a,b
- **📐 Segmentação por Colunas**: 1024 funções indicadoras verticais com parâmetros c,d  
- **🔗 Segmentação Combinada**: Fusão inteligente de linhas + colunas
- **� Análise Separada + União**: Processamento independente e união conforme especificado
- **📊 Análise Comparativa**: Comparação automática entre todos os métodos
- **🎨 Visualizações Especializadas**: Overlays coloridos por método

**🏗️ Arquitetura de Métodos Expandida:**

```mermaid
graph TB
    A["main.py"] --> B["escolher_modelo.py"]
    B --> C["🧠 DeepLabV3"]
    B --> D["📐 Parametrização v0.4.0"]
    
    C --> C1["ModeloSegmentacaoDeepLabV3"]
    C --> C2["segmentacao_imagens_Deeplabv3.py"]
    C --> C3["🎯 Alta Precisão"]
    
    D --> D1["ModeloSegmentacaoParametrizacao"]
    D --> D2["SegmentacaoParametrizacaoIndicadora"]
    D --> D3{🎛️ Método Específico}
    
    D3 --> D4["📏 segmentar()<br/>768 Funções Horizontais"]
    D3 --> D5["📐 segmentar_por_colunas()<br/>1024 Funções Verticais"]
    D3 --> D6["🔗 segmentar_combinado()<br/>Híbrido Inteligente"]
    D3 --> D7["🔄 segmentar_separado_e_unido()<br/>Processamento Independente"]
    
    D4 --> E["📊 Resultados"]
    D5 --> E
    D6 --> E
    D7 --> E
    C3 --> E
    
    classDef main fill:#2196F3,stroke:#1976D2,color:#fff
    classDef models fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef engines fill:#FF9800,stroke:#F57C00,color:#fff
    classDef methods fill:#9C27B0,stroke:#7B1FA2,color:#fff
    classDef results fill:#F44336,stroke:#C62828,color:#fff
    
    class A,B main
    class C,D,C1,D1 models
    class C2,C3,D2,D3 engines
    class D4,D5,D6,D7 methods
    class E results
```
    
    C --> C1["ModeloSegmentacaoDeepLabV3"]
    C --> C2["segmentacao_imagens_Deeplabv3.py"]
    C --> C3["🎯 Alta Precisão"]
    
    D --> D1["ModeloSegmentacaoParametrizacao"]
    D --> D2["SegmentacaoParametrizacaoIndicadora"]
    D --> D3["⚡ Vectorização NumPy"]
    D --> D4["🔬 MSE < 200 Early Stop"]
    D --> D5["📊 Processamento em Batches"]
    
    C3 --> E["📊 Resultados"]
    D3 --> E
    D4 --> E
    D5 --> E
    
    classDef main fill:#2196F3,stroke:#1976D2,color:#fff
    classDef models fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef engines fill:#FF9800,stroke:#F57C00,color:#fff
    classDef optimizations fill:#9C27B0,stroke:#7B1FA2,color:#fff
    
    class A,B main
    class C,D,C1,D1 models
    class C2,C3,D2,E engines
    class D3,D4,D5 optimizations
```

### 📊 Comparação Detalhada de Métodos v0.4.0

```mermaid
graph TB
    subgraph "🧠 DeepLabV3 + ResNet101"
        DL1[🎯 Precisão Máxima<br/>⭐⭐⭐⭐⭐]
        DL2[⏱️ ~15s por imagem<br/>🐌 Mais lento]
        DL3[🖥️ GPU recomendada<br/>💻 CPU suportado]
        DL4[🔬 Deep Learning<br/>🤖 PyTorch]
        
        DL1 --> DL2 --> DL3 --> DL4
    end
    
    subgraph "� Parametrização Linhas v0.4.0"
        L1[⚡ Velocidade Alta<br/>⭐⭐⭐⭐⭐]
        L2[⏱️ ~1-2s por imagem<br/>🚀 Ultra rápido]
        L3[💻 CPU suficiente<br/>⚡ Otimizado]
        L4[🧮 768 Funções Horizontais<br/>📊 NumPy Vectorizado]
        
        L1 --> L2 --> L3 --> L4
    end
    
    subgraph "📐 Parametrização Colunas v0.4.0"
        C1[⚡ Velocidade Alta<br/>⭐⭐⭐⭐⭐]
        C2[⏱️ ~1-2s por imagem<br/>🚀 Ultra rápido]
        C3[💻 CPU suficiente<br/>⚡ Otimizado]
        C4[🧮 1024 Funções Verticais<br/>📊 NumPy Vectorizado]
        
        C1 --> C2 --> C3 --> C4
    end
    
    subgraph "🔗 Parametrização Combinada v0.4.0"
        H1[🎯 Precisão + Velocidade<br/>⭐⭐⭐⭐⭐]
        H2[⏱️ ~3-4s por imagem<br/>🔄 Balanceado]
        H3[💻 CPU suficiente<br/>⚡ Otimizado]
        H4[🧮 Linhas + Colunas<br/>🔗 Fusão Inteligente]
        
        H1 --> H2 --> H3 --> H4
    end
    
    subgraph "🎯 Critérios de Escolha"
        Choice1[🔬 Precisão Crítica → DeepLabV3]
        Choice2[⚡ Processamento Horizontal → Linhas]
        Choice3[📐 Análise Vertical → Colunas]
        Choice4[🔗 Máxima Cobertura → Combinado]
        Choice5[🎛️ Análise Completa → Todos disponíveis]
    end
    
    DL4 --> Choice1
    L4 --> Choice2
    C4 --> Choice3
    H4 --> Choice4
    Choice1 --> Choice5
    Choice2 --> Choice5
    Choice3 --> Choice5
    Choice4 --> Choice5
    
    classDef deeplab fill:#E8F5E8,stroke:#388E3C
    classDef linhas fill:#E3F2FD,stroke:#1976D2
    classDef colunas fill:#FFF3E0,stroke:#F57C00
    classDef combinado fill:#F3E5F5,stroke:#7B1FA2
    classDef choice fill:#FFEBEE,stroke:#C62828
    
    class DL1,DL2,DL3,DL4 deeplab
    class L1,L2,L3,L4 linhas
    class C1,C2,C3,C4 colunas
    class H1,H2,H3,H4 combinado
    class Choice1,Choice2,Choice3,Choice4,Choice5 choice
```

**⚖️ Comparação Expandida de Métodos:**

| Aspecto | 🧠 DeepLabV3 | 📏 Linhas v0.4.0 | 📐 Colunas v0.4.0 | 🔗 Combinado v0.4.0 |
|---------|-------------|------------------|-------------------|-------------------|
| **Precisão** | ⭐⭐⭐⭐⭐ Máxima | ⭐⭐⭐⭐ Alta | ⭐⭐⭐⭐ Alta | ⭐⭐⭐⭐⭐ Máxima |
| **Velocidade** | ⭐⭐ ~15s/imagem | ⭐⭐⭐⭐⭐ ~1-2s | ⭐⭐⭐⭐⭐ ~1-2s | ⭐⭐⭐⭐ ~3-4s |
| **Recursos** | GPU recomendada | CPU suficiente | CPU suficiente | CPU suficiente |
| **Método** | Deep Learning | 768 Funções a,b | 1024 Funções c,d | Fusão Inteligente |
| **Otimizações** | ResNet101 pré-treinado | NumPy + Early Stop | NumPy + Early Stop | Múltiplas fusões |
| **Uso Ideal** | Precisão crítica | Análise horizontal | Análise vertical | Cobertura máxima |
| **Análise** | Semântica | Horizontal | Vertical | Multidimensional |

### ⚡ v0.4.0 - Segmentação Multidimensional
**🌟 Revolução na análise de imagens com métodos especializados:**
- **📏 Segmentação por Linhas**: 768 funções indicadoras horizontais (parâmetros a,b)
- **📐 Segmentação por Colunas**: 1024 funções indicadoras verticais (parâmetros c,d)
- **🔗 Segmentação Combinada**: Fusão inteligente de ambos os métodos
- **🔄 Análise Separada + União**: Processamento independente conforme especificado
- **📊 Análise Comparativa**: Comparação automática entre todos os métodos
- **🎨 Visualizações Especializadas**: Overlays coloridos por método

### ⚡ v0.2.3 - Otimizações Avançadas de Performance
**🚀 Revolucionárias melhorias de velocidade mantidas em v0.4.0:**
- **⚡ Vectorização NumPy**: Processamento 3-5x mais rápido com operações matriciais
- **🧠 Processamento em Batches**: 50 funções indicadoras processadas simultaneamente
- **🎯 Early Stopping Inteligente**: MSE < 200 para parada automática
- **🔬 Otimização MSE Rigorosa**: Métrica única para máxima precisão
- **📊 Análise Vectorizada**: Estatísticas calculadas com NumPy puro

### 🎛️ v0.2.2 - Sistema de Múltiplos Modelos
**🛠️ Arquitetura expandida com escolha de métodos:**
- **🎯 Interface de escolha**: Menu interativo para seleção de método
- **🧠 DeepLabV3**: Máxima precisão com deep learning
- **📐 Parametrização**: Máxima velocidade com funções indicadoras
- **📊 Comparação automática**: Métricas de performance para cada método

### 🔧 v0.2.1 - Refatoração e Otimização
**�️ Melhorias Arquiteturais:**
- **� Renomeação**: `SegmentacaoPessoa` → `SegmentacaoDeepLabV3`
- **�️ Organização**: Eliminação de arquivos duplicados

- **� Modularidade**: Estrutura mais clara e manutenível
### �️ v0.2.0 - Sistema de Segmentação de Imagens
**🚀 Implementação do DeepLabV3:**
- **🎯 Detecção automática** de pessoas em imagens
- **🔧 Pipeline otimizada** com pré/pós-processamento
- **👁️ Visualização interativa** de resultados

### 📊 v0.1.0 - Base de Dados Sólida
**🏗️ Fundação do projeto:**
- **✅ Validação automática** de correspondência CSV ↔ Imagens
- **⚖️ Categorização inteligente** por gênero e posição
- **📋 Relatórios detalhados** com estatísticas em tempo real

## ⚡ Quick Start

```powershell
# 1. Ativar ambiente e instalar dependências
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Executar sistema com interface de escolha
python main.py
```

**🎯 Interface de Escolha Expandida:**
```
🎯 SELEÇÃO DE MODELO DE SEGMENTAÇÃO
================================================================
1️⃣  DeepLabV3 + ResNet101
   • Modelo pré-treinado de deep learning
   • Alta precisão na segmentação de pessoas
   • Processamento mais lento

2️⃣  Parametrização com Funções Indicadoras (v0.4.0)
   • Método matemático com vectorização NumPy
   • Processamento ultrarrápido (~1-2s por imagem)
   • Early stopping inteligente (MSE < 200)
   • NOVOS MÉTODOS v0.4.0:
     - 📏 Segmentação por LINHAS (768 funções horizontais)
     - 📐 Segmentação por COLUNAS (1024 funções verticais)  
     - 🔗 Segmentação COMBINADA (linhas + colunas)
     - 🔄 Segmentação SEPARADA + UNIÃO (processamento independente)
   • NOVO: Análise comparativa automática entre métodos

Escolha uma opção (1-2) ou Enter para padrão (2):

🎯 MÉTODO DE PARAMETRIZAÇÃO
================================================================
Escolha o tipo de função indicadora:

1️⃣  Segmentação por LINHAS (clássico)
   • 768 funções indicadoras horizontais
   • Método original otimizado

2️⃣  Segmentação por COLUNAS (novo)
   • 1024 funções indicadoras verticais
   • Análise perpendicular às linhas

3️⃣  Segmentação COMBINADA (avançado)
   • União inteligente de linhas + colunas
   • Máxima cobertura e precisão

4️⃣  Análise SEPARADA + UNIÃO (completo)
   • Processamento independente de cada método
   • União final dos resultados

Escolha uma opção (1-4) ou Enter para padrão (1):
```

## 🏗️ Arquitetura Completa v0.4.0

```mermaid
graph TB
    subgraph "📁 Entrada de Dados"
        A1["📄 medidas_dados_sinteticos.csv"]
        A2["📂 INOVIA_IMAGENS/"]
        A2 --> A21["syn_fXXXXXX-X-Pre/front.png"]
        A2 --> A22["syn_fXXXXXX-X-Pre/left.png"]
        A2 --> A23["syn_fXXXXXX-X-Pos/front.png"]
        A2 --> A24["syn_fXXXXXX-X-Pos/left.png"]
    end
    
    subgraph "🔧 Processamento"
        B1["main.py<br/>🎯 Coordenador"]
        B2["importa_dados.py<br/>📊 Validação"]
        B3["escolher_modelo.py<br/>🎛️ Seleção"]
        
        B1 --> B2
        B2 --> B3
    end
    
    subgraph "🧠 Modelo DeepLabV3"
        C1["ModeloSegmentacaoDeepLabV3"]
        C2["SegmentacaoDeepLabV3"]
        C3["🎯 PyTorch + ResNet101"]
        
        C1 --> C2
        C2 --> C3
    end
    
    subgraph "📐 Modelo Parametrização v0.4.0"
        D1["ModeloSegmentacaoParametrizacao"]
        D2["SegmentacaoParametrizacaoIndicadora"]
        D3{🎛️ Método Específico}
        
        D1 --> D2
        D2 --> D3
        
        D3 -->|1️⃣| D4["� 768 Funções Horizontais"]
        D3 -->|2️⃣| D5["📐 1024 Funções Verticais"]
        D3 -->|3️⃣| D6["🔗 Método Combinado"]
        D3 -->|4️⃣| D7["🔄 Separado + União"]
    end
    
    subgraph "📊 Análise e Métricas"
        E1["📈 MSE Individual por Método"]
        E2["🔄 Análise Comparativa"]
        E3["🔗 Métricas Combinadas"]
        E4["📊 Estatísticas Globais"]
    end
    
    subgraph "📤 Saída"
        F1["📊 Relatórios JSON"]
        F2["🖼️ Máscaras Processadas"]
        F3["🎨 Visualizações Especializadas"]
        F4["� Gráficos Comparativos"]
    end
    
    A1 --> B2
    A2 --> B2
    B3 --> C1
    B3 --> D1
    C1 --> E1
    D4 --> E1
    D5 --> E1
    D6 --> E3
    D7 --> E2
    C2 --> F2
    E1 --> F1
    E2 --> F3
    E3 --> F4
    E4 --> F1
    
    classDef input fill:#e3f2fd,stroke:#1976d2
    classDef processing fill:#f3e5f5,stroke:#7b1fa2
    classDef models fill:#e8f5e8,stroke:#388e3c
    classDef methods fill:#fff3e0,stroke:#f57c00
    classDef analysis fill:#fce4ec,stroke:#c2185b
    classDef output fill:#e0f2f1,stroke:#00695c
    
    class A1,A2,A21,A22,A23,A24 input
    class B1,B2,B3 processing
    class C1,C2,C3,D1,D2,D3 models
    class D4,D5,D6,D7 methods
    class E1,E2,E3,E4 analysis
    class F1,F2,F3,F4 output
```
    C3 --> E3
    D3 --> E3
    C1 --> E4
    D1 --> E4
    
    classDef input fill:#e3f2fd,stroke:#1976d2
    classDef processing fill:#f3e5f5,stroke:#7b1fa2
    classDef models fill:#e8f5e8,stroke:#388e3c
    classDef output fill:#fff3e0,stroke:#f57c00
    
    class A1,A2,A21,A22,A23,A24 input
    class B1,B2,B3 processing
    class C1,C2,C3,D1,D2,D3 models
    class E1,E2,E3,E4 output
```

## 🎯 Funcionalidades Atuais

### 📊 Módulo de Dados
| Componente | Status | Descrição |
|------------|--------|-----------|
| `ImportadorDados` | ✅ | Verificação e carregamento automático |
| `verificar_dados()` | ✅ | Validação de arquivos e caminhos |
| `carregar_dados_csv()` | ✅ | Leitura segura com tratamento de erros |
| `filtrar_por_genero_posicao()` | ✅ | Categorização inteligente |
| `imprimir_relatorio()` | ✅ | Estatísticas visuais em tempo real |

### 🎛️ Sistema de Escolha de Modelos
| Componente | Status | Descrição |
|------------|--------|-----------|
| `escolher_modelo.py` | ✅ | Interface de seleção interativa |
| `inicializar_modelo()` | ✅ | Configuração automática do modelo |
| `processar_com_modelo()` | ✅ | Execução com modelo escolhido |
| `exibir_resultados()` | ✅ | Relatórios personalizados por método |

### 🧠 Módulo DeepLabV3
| Componente | Status | Descrição |
|------------|--------|-----------|
| `ModeloSegmentacaoDeepLabV3` | ✅ | Coordenador DeepLabV3 |
| `SegmentacaoDeepLabV3` | ✅ | Engine de processamento |
| `processar_dataset()` | ✅ | Pipeline completa automatizada |
| `segmentar_pessoa()` | ✅ | Segmentação semântica de alta precisão |
| `melhorar_contraste()` | ✅ | Pré-processamento CLAHE + sharpening |
| `pos_processar_mascara()` | ✅ | Filtros morfológicos avançados |

### 📐 Módulo Parametrização v0.4.0
| Componente | Status | Descrição |
|------------|--------|-----------|
| `ModeloSegmentacaoParametrizacao` | ✅ | Coordenador Parametrização |
| `SegmentacaoParametrizacaoIndicadora` | ✅ | Engine matemático otimizado |
| `segmentar()` | ✅ | 768 funções indicadoras horizontais |
| `segmentar_por_colunas()` | ✅ | 1024 funções indicadoras verticais |
| `segmentar_combinado()` | ✅ | Método híbrido linhas + colunas |
| `segmentar_separado_e_unido()` | ✅ | Processamento independente + união |
| `comparar_metodos()` | ✅ | Análise comparativa automática |
| `_otimizar_parametros_linha()` | ✅ | Otimização MSE rigorosa (a,b) |
| `_otimizar_parametros_coluna()` | ✅ | Otimização MSE rigorosa (c,d) |
| `visualizar_amostra_resultados()` | ✅ | Visualização automática especializada |

## 📊 Dados Suportados

### 🖼️ Estrutura de Imagens
```
📁 INOVIA_IMAGENS/
├── syn_fXXXXXX-X-Pre/    # 👩👨 Pre-procedimento  
│   ├── front.png         # 🖼️ Imagem frontal
│   └── left.png          # 🖼️ Imagem lateral
└── syn_fXXXXXX-X-Pos/    # 👩👨 Pós-procedimento
    ├── front.png         # 🖼️ Imagem frontal
    └── left.png          # 🖼️ Imagem lateral
```

**Processamento Automatizado:**
- **Detecção**: Identifica automaticamente categorias masculinas/femininas
- **Validação**: Verifica correspondência entre CSV e pastas
- **Segmentação**: Processa front.png + left.png para cada ID
- **Métricas**: Calcula estatísticas de qualidade por imagem e globais

### 📈 Dados CSV
- **Arquivo**: `medidas_dados_sinteticos.csv`
- **Integração**: Correspondência automática ID ↔ Pasta
- **Validação**: Verificação de consistência em tempo real
- **Categorização**: Separação por gênero e posição (Pre/Pos)

## ⚙️ Configuração Avançada

### 📦 Dependências Completas
```text
# Base de dados e visualização
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
Pillow>=10.0.0

# Deep Learning (DeepLabV3)
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0

# Processamento matemático (Parametrização)
scipy>=1.11.0
scikit-learn>=1.3.0
pydensecrf>=1.0.2

# Suporte adicional
pathlib2>=2.3.0
warnings
```

### 🎛️ Parâmetros Configuráveis

**DeepLabV3:**
```python
ModeloSegmentacaoDeepLabV3(
    confidence_threshold=0.5,     # Threshold de detecção
    min_area=100,                 # Área mínima (pixels)
    target_size=(512, 512),       # Redimensionamento
    metodo_deeplabv3='auto'       # 'rgb', 'grayscale_adaptive', 'grayscale_always'
)
```

**Parametrização v0.4.0:**
```python
ModeloSegmentacaoParametrizacao(
    target_width=1024,            # Largura da imagem (colunas)
    target_height=768,            # Altura da imagem (linhas)
    morph_kernel_size=3,          # Tamanho kernel morfológico
    min_area=50,                  # Filtro de ruído
    enhance_contrast=True,        # Melhoria de contraste
    metodo_segmentacao='linhas'   # 'linhas', 'colunas', 'combinado'
)

# Novos métodos disponíveis v0.4.0:
segmentador.segmentar()                    # 768 funções horizontais
segmentador.segmentar_por_colunas()        # 1024 funções verticais  
segmentador.segmentar_combinado()          # Método híbrido
segmentador.segmentar_separado_e_unido()   # Processamento independente
segmentador.comparar_metodos()             # Análise comparativa
```

### ⚡ Otimizações v0.4.0 - Performance Mantida + Métodos Expandidos

#### 🧮 Vectorização NumPy (Mantida)
```python
# ✅ IMPLEMENTADO: Processamento em batches vectorizado
def _gerar_multiplas_funcoes_vectorizadas(self, largura, inicios, fins, valor_max):
    """Gera múltiplas funções indicadoras simultaneamente com NumPy"""
    n_funcoes = len(inicios)
    funcoes = np.zeros((n_funcoes, largura), dtype=np.float32)
    # Processamento matricial 3-5x mais rápido

def _calcular_mse_vectorizado(self, pixels, funcoes_batch):
    """Calcula MSE para múltiplas funções usando broadcasting"""
    diff = funcoes_batch - pixels[np.newaxis, :]
    return np.mean(diff ** 2, axis=1)  # MSE vectorizado
```

#### 🎯 Early Stopping Inteligente (Aprimorado)
```python
# ✅ IMPLEMENTADO: Parada automática para parâmetros ótimos
if melhor_mse_lote < 200:  # Excelente qualidade
    return melhores_params  # Para imediatamente

if melhor_mse_lote < 300:  # Boa qualidade no fallback
    break  # Sai do loop de busca
```

#### 📊 Métricas de Performance v0.4.0
| Métrica | v0.2.3 | v0.4.0 | Melhoria |
|---------|--------|--------|----------|
| **Tempo/método** | ~1-2s | ~1-2s | **Mantido** |
| **Métodos** | 1 (linhas) | 4 métodos | **4x expandido** |
| **Funções** | 382 | 768/1024 | **2-3x mais funções** |
| **Análise** | Individual | Individual + Comparativa | **Análise expandida** |
| **Dimensões** | 512x382 | 1024x768 | **2x resolução** |
| **Early Stop** | MSE < 200 | MSE < 200 | **Mantido** |

## 🛣️ Próximos Passos

```mermaid
gantt
    title Roadmap INOVIA 2025
    dateFormat  YYYY-MM-DD
    section Concluído
    Base de Dados       :done, base, 2025-09-08, 1d
    Segmentação DeepLabV3 :done, deep, 2025-09-08, 1d
    Refatoração         :done, refact, 2025-09-09, 1d
    Múltiplos Modelos   :done, multi, 2025-09-09, 1d
    Otimizações Performance :done, optim, 2025-09-09, 1d
    Extensão Completa   :done, ext, 2025-09-10, 1d
    Segmentação Multidimensional :done, multidim, 2025-09-10, 1d
    
    section Em Desenvolvimento  
    Analytics Avançados :active, analytics, 2025-09-10, 5d
    
    section Planejado
    Interface Gráfica   :ui, after analytics, 7d
    Correlações Auto    :corr, after analytics, 5d
    Dashboard Interativo :dash, after ui, 5d
    Testes Automatizados :test, after dash, 3d
    Deploy Produção     :deploy, after test, 5d
```

### 🔮 Visão de Estados do Projeto

```mermaid
stateDiagram-v2
    state "📊 Fundação" as Foundation {
        [*] --> DataValidation
        DataValidation --> CSVProcessing
        CSVProcessing --> ImageMatching
        ImageMatching --> ReportGeneration
        ReportGeneration --> [*]
    }
    
    state "🖼️ Segmentação" as Segmentation {
        [*] --> DeepLabV3Implementation
        DeepLabV3Implementation --> PyTorchIntegration
        PyTorchIntegration --> VisualizationTools
        VisualizationTools --> [*]
    }
    
    state "🎛️ Múltiplos Modelos" as MultiModel {
        [*] --> ModelSelection
        ModelSelection --> DeepLabV3Pipeline
        ModelSelection --> ParametrizationPipeline
        DeepLabV3Pipeline --> UnifiedResults
        ParametrizationPipeline --> UnifiedResults
        UnifiedResults --> [*]
    }
    
    state "⚡ Otimizações v0.2.3" as Optimizations {
        [*] --> VectorizationNumPy
        VectorizationNumPy --> BatchProcessing
        BatchProcessing --> EarlyStopping
        EarlyStopping --> PerformanceGains
        PerformanceGains --> [*]
    }
    
    state "🔮 Futuro" as Future {
        [*] --> Analytics
        Analytics --> Correlations
        Correlations --> WebInterface
        WebInterface --> CloudDeploy
        CloudDeploy --> [*]
    }
    
    state "🌟 Multidimensional v0.4.0" as Multidimensional {
        [*] --> LinhasSegmentation
        LinhasSegmentation --> ColunasSegmentation
        ColunasSegmentation --> CombinedSegmentation
        CombinedSegmentation --> SeparatedUnion
        SeparatedUnion --> ComparativeAnalysis
        ComparativeAnalysis --> [*]
    }
    
    [*] --> Foundation
    Foundation --> Segmentation
    Segmentation --> MultiModel
    MultiModel --> Optimizations
    Optimizations --> Multidimensional
    Multidimensional --> Future
    Future --> [*]
```

### 🎯 v0.5.0 - Analytics Avançados (Próximo)
- **🧮 Correlações automáticas**: Relacionar medidas corporais ↔ silhuetas processadas
- **📈 Insights estatísticos**: Padrões e tendências nos dados com MSE rigoroso
- **🔍 Análise comparativa**: Before/After e Male/Female usando vectorização
- **📊 Métricas avançadas**: Precisão, recall, F1-score com processamento otimizado
- **🔄 Dashboard de análise**: Interface para explorar correlações entre métodos

### 🎛️ v0.6.0 - Interface Gráfica
- **🖥️ Dashboard Streamlit**: Interface web interativa
- **📊 Visualizações dinâmicas**: Gráficos e plots em tempo real
- **🎯 Configuração visual**: Ajustes de parâmetros via interface
- **📤 Exportação facilitada**: Download de resultados em múltiplos formatos
- **🔄 Comparação visual**: Interface para análise lado a lado

### 🚀 v0.7.0 - Deploy e Produção
- **🐳 Containerização Docker**: Deploy simplificado
- **☁️ Cloud deployment**: Suporte Azure/AWS
- **🔧 CI/CD pipeline**: Automação de build e deploy
- **📚 Documentação completa**: Guias de uso e API
- **🔧 Testes automatizados**: Coverage completo do sistema

## 📈 Status Atual

🚀 **Versão 0.4.0** - Segmentação Multidimensional com Análise Comparativa!

## 🆕 Novidades da v0.4.0

### 🎯 Métodos de Segmentação Expandidos
A versão 0.4.0 consolida e expande os métodos de segmentação com funções indicadoras:

#### 📏 **1. Segmentação por LINHAS (Aprimorada)**
- **768 funções indicadoras** - uma para cada linha da imagem 1024x768
- Parâmetros otimizados: **pontos a e b** (pixel_inicio, pixel_fim)
- Análise horizontal completa da imagem
- Resolução duplicada comparada à v0.2.3 (512x382 → 1024x768)

#### 📐 **2. Segmentação por COLUNAS (Consolidada)**
- **1024 funções indicadoras** - uma para cada coluna da imagem 1024x768
- Parâmetros otimizados: **pontos c e d** (pixel_inicio, pixel_fim)
- Análise vertical completa da imagem
- Implementação análoga às linhas com otimizações específicas

#### 🔗 **3. Segmentação COMBINADA (Refinada)**
Combina os resultados de linhas e colunas usando métodos inteligentes:
- **Interseção**: Pixels ativos em ambas as máscaras (mais conservador)
- **União**: Pixels ativos em qualquer máscara (mais abrangente)  
- **Média Ponderada**: Combinação inteligente com pesos ajustáveis

#### 🔄 **4. Segmentação SEPARADA + UNIÃO (NOVO!)**
Processamento independente conforme especificado:
- Executa segmentação por linhas e colunas separadamente
- Realiza união final dos resultados
- Mantém estatísticas individuais de cada método
- Oferece análise comparativa detalhada

### 🔬 Funcionalidades Avançadas

#### 📊 **Análise Comparativa Automática**
```python
# Novo método para comparar todos os métodos
resultado = segmentador.comparar_metodos("imagem.jpg")
```
- Executa os 3 métodos automaticamente
- Gera relatório comparativo de MSE
- Análise de pixels segmentados por método
- Visualização lado a lado

#### 🎨 **Visualizações Especializadas**
- **Visualização por linhas**: Overlay vermelho
- **Visualização por colunas**: Overlay verde  
- **Visualização combinada**: Overlay azul + comparativo
- **Análise de convergência**: Distribuição de parâmetros c e d

#### 📈 **Métricas Expandidas**
- MSE individual para linhas e colunas
- MSE combinado ponderado
- Estatísticas de convergência por dimensão
- Análise de distribuição de parâmetros

### 🚀 Como Usar as Novas Funcionalidades v0.5.0

#### 📦 Detecção de Bounding Boxes

```python
from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora
from Bounding_box import BoundingBoxDetector
from exibicao_BBox_imagens import ExibicaoBBoxImagens

# 1. Realizar segmentação com união de silhuetas
segmentador = SegmentacaoParametrizacaoIndicadora()
resultado = segmentador.segmentar_separado_e_unido("imagem.jpg")

# 2. Detectar bounding boxes nas silhuetas
detector = BoundingBoxDetector(area_minima=100, metodo_deteccao='contornos')
bbox_resultado = detector.processar_resultado_segmentacao(resultado)

# 3. Visualizar todas as bounding boxes
visualizador = ExibicaoBBoxImagens()
visualizador.visualizar_todas_bboxes(bbox_resultado)

# 4. Foco na união das silhuetas
visualizador.visualizar_sobreposicao(bbox_resultado, tipo_silhueta='uniao')

# 5. Análise comparativa das bounding boxes
visualizador.visualizar_comparativo_bboxes(bbox_resultado)
```

#### 📊 Segmentação Multidimensional v0.4.0

```python
from segmentacao_imagens_parametrizacao_indicadora import SegmentacaoParametrizacaoIndicadora

# Inicializar segmentador com configurações v0.4.0
segmentador = SegmentacaoParametrizacaoIndicadora(
    target_width=1024,
    target_height=768,
    enhance_contrast=True
)

# 1. Segmentação clássica por linhas (768 funções)
resultado_linhas = segmentador.segmentar("imagem.jpg")

# 2. Segmentação por colunas (1024 funções)
resultado_colunas = segmentador.segmentar_por_colunas("imagem.jpg")

# 3. Segmentação combinada (híbrida)
resultado_combinado = segmentador.segmentar_combinado("imagem.jpg", 
                                                    metodo_fusao="uniao")

# 4. NOVO v0.4.0: Análise separada + união
resultado_separado = segmentador.segmentar_separado_e_unido("imagem.jpg")

# 5. NOVO v0.4.0: Análise comparativa completa
comparacao = segmentador.comparar_metodos("imagem.jpg")

# 6. Análise de convergência expandida
analise_linhas = segmentador.analisar_convergencia_parametros(resultado_linhas, 'linhas')
analise_colunas = segmentador.analisar_convergencia_parametros(resultado_colunas, 'colunas')
```

### 🏆 Marcos Alcançados v0.5.0
- ✅ **Base de dados robusta** e validação automática
- ✅ **Quatro métodos de segmentação** com escolha interativa
- ✅ **Segmentação multidimensional** com funções horizontais e verticais
- ✅ **Segmentação separada + união** conforme especificação
- ✅ **Detecção de bounding boxes** automática nas silhuetas
- ✅ **Análise comparativa automática** entre todos os métodos
- ✅ **Visualização avançada** com sobreposições e métricas
- ✅ **Pipeline completa** dados → processamento → detecção → visualização
- ✅ **Qualidade enterprise** com logging e tratamento de erros
- ✅ **Métricas expandidas** com MSE individual/combinado/comparativo + bounding boxes
- ✅ **Vectorização NumPy mantida** com processamento 3-5x mais rápido
- ✅ **Early stopping MSE** para otimização inteligente em todos os métodos
- ✅ **Resolução aprimorada** de 512x382 para 1024x768
- 🔄 **Próximo**: Analytics avançados e correlações automáticas

### 📂 Arquivos Principais v0.5.0

#### 🔬 Segmentação e Análise
- 📄 **[segmentacao_imagens_parametrizacao_indicadora.py](segmentacao_imagens_parametrizacao_indicadora.py)** - Módulo principal com 4 métodos
- 📄 **[exibicao_imagens_parametrizadas.py](exibicao_imagens_parametrizadas.py)** - Visualização especializada das segmentações

#### 📦 Bounding Boxes (NOVO v0.5.0)
- 📄 **[Bounding_box.py](Bounding_box.py)** - Detecção automática de retângulos delimitadores
- 📄 **[exibicao_BBox_imagens.py](exibicao_BBox_imagens.py)** - Visualização avançada das bounding boxes
- 📄 **[exemplo_bounding_box.py](exemplo_bounding_box.py)** - Demonstração completa do sistema

#### 🧠 Deep Learning
- 📄 **[modelo_segmentacao_Deeplabv3.py](modelo_segmentacao_Deeplabv3.py)** - Wrapper do modelo DeepLabV3
- 📄 **[segmentacao_imagens_Deeplabv3.py](segmentacao_imagens_Deeplabv3.py)** - Engine de processamento

#### 🎛️ Sistema de Controle
- 📄 **[main.py](main.py)** - Coordenador principal do sistema
- 📄 **[escolher_modelo.py](escolher_modelo.py)** - Interface de seleção de métodos
- 📄 **[importa_dados.py](importa_dados.py)** - Gerenciamento de dados de entrada

### 🎯 Tecnologias Utilizadas

```mermaid
graph TD
    subgraph "🐍 Core Python"
        A[Python 3.8+]
        B[NumPy 1.21+]
        C[Pandas 1.3+]
        D[SciPy 1.7+]
    end
    
    subgraph "🧠 Deep Learning"
        E[PyTorch 2.0+]
        F[TorchVision]
        G[CUDA Support]
    end
    
    subgraph "🖼️ Computer Vision"
        H[OpenCV 4.5+]
        I[Pillow 8.3+]
        J[Matplotlib 3.5+]
    end
    
    A --> B
    B --> C
    C --> D
    E --> F
    F --> G
    H --> I
    I --> J
    
    style A fill:#306998,color:#fff
    style E fill:#ee4c2c,color:#fff
    style H fill:#5c85d6,color:#fff
```

## 🔮 Roadmap Futuro e Desenvolvimento

### 🚀 Próximas Versões Planejadas

```mermaid
gantt
    title 📋 Roadmap de Desenvolvimento INOVIA
    dateFormat  YYYY-MM-DD
    section v0.6.0 - Analytics
    Correlações Automáticas        :2025-09-12, 3d
    Dashboard Interativo           :2025-09-15, 4d
    Métricas Avançadas            :2025-09-19, 3d
    
    section v0.7.0 - Interface Web
    Streamlit/Dash Integration    :2025-09-22, 5d
    Interface Responsiva          :2025-09-27, 4d
    Multi-usuário                 :2025-10-01, 3d
    
    section v0.8.0 - IA Avançada
    Novos Modelos Deep Learning   :2025-10-04, 6d
    Auto-tuning Parâmetros        :2025-10-10, 4d
    Transfer Learning             :2025-10-14, 5d
    
    section v1.0.0 - Release
    Documentação Completa         :2025-10-19, 4d
    Testes Automáticos           :2025-10-23, 3d
    Deploy Production             :2025-10-26, 2d
```

### 🤝 Como Contribuir

```mermaid
graph TD
    A[🤔 Interesse em Contribuir] --> B{🎯 Tipo de Contribuição}
    
    B -->|� Bug Reports| C[📝 Criar Issue]
    B -->|✨ Features| D[💡 Propor Enhancement]
    B -->|📖 Documentação| E[📚 Melhorar Docs]
    B -->|🧪 Testes| F[🔍 Adicionar Tests]
    
    C --> G[� Fork Repository]
    D --> G
    E --> G
    F --> G
    
    G --> H[🌿 Criar Branch]
    H --> I[💻 Implementar Mudanças]
    I --> J[✅ Testar Localmente]
    J --> K[📤 Pull Request]
    K --> L[👥 Code Review]
    L --> M[� Merge Approved]
    
    style A fill:#4caf50,color:#fff
    style B fill:#ff9800,color:#fff
    style M fill:#2196f3,color:#fff
```

### � Suporte e Comunidade

```mermaid
graph LR
    A[❓ Precisa de Ajuda?] --> B{🔍 Tipo de Problema}
    
    B -->|📖 Documentação| C[📚 Consultar README]
    B -->|🐛 Bug Report| D[🎫 Abrir Issue]
    B -->|💡 Feature Request| E[💭 Propor Enhancement]
    B -->|❓ Dúvida Geral| F[💬 Discussions]
    
    style A fill:#ff9800,color:#fff
    style C fill:#4caf50,color:#fff
    style D fill:#f44336,color:#fff
    style E fill:#2196f3,color:#fff
    style F fill:#9c27b0,color:#fff
```

---

## 📄 Licença e Créditos

### 🙏 Agradecimentos Especiais

- **🧠 PyTorch Team**: Framework de deep learning excepcional
- **📊 NumPy Community**: Base sólida para computação científica  
- **🖼️ OpenCV Contributors**: Ferramentas robustas de visão computacional
- **🎯 INOVIA**: Oportunidade de desenvolver solução inovadora
- **👥 Open Source Community**: Inspiração e conhecimento compartilhado

---

<div align="center">

### � Projeto INOVIA - Segmentação Inteligente de Imagens

**Desenvolvido com ❤️ para análise avançada de medidas corporais sintéticas**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![NumPy](https://img.shields.io/badge/NumPy-1.21+-orange?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org)

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

📋 [CHANGELOG.md](CHANGELOG.md) | 🐛 [Issues](../../issues) | 🤝 [Contributing](../../pulls) | 📧 [Contato](mailto:danilo.rigitano@inovia.com)

</div>
