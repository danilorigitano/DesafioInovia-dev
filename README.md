# Projeto INOVIA 🚀

Sistema modular para processamento e análise de dados de imagens sintéticas com medidas corporais.

🚀 **Versão 0.2.2** - Sistema de múltiplos modelos de segmentação!  
📋 [Ver CHANGELOG.md](CHANGELOG.md) para histórico detalhado

## 🎯 Evolução do Desenvolvimento

```mermaid
graph TD
    A["v0.1.0<br/>📊 Base de Dados"] --> B["v0.2.0<br/>🖼️ Segmentação DeepLabV3"]
    B --> C["v0.2.1<br/>🔧 Refatoração"]
    C --> D["v0.2.2<br/>🎛️ Múltiplos Modelos"]
    D --> E["v0.3.0<br/>🧮 Analytics"]
    
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
    
    E --> E1["🔄 Correlações Automáticas"]
    E --> E2["🔄 Dashboard Interativo"]
    E --> E3["🔄 Métricas Avançadas"]
    
    classDef implemented fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef current fill:#2196F3,stroke:#1976D2,color:#fff
    classDef future fill:#FF9800,stroke:#F57C00,color:#fff
    
    class A,B,C,D,A1,A2,A3,B1,B2,B3,C1,C2,C3,D1,D2,D3 implemented
    class E current
    class E1,E2,E3 future
```

### 🎛️ v0.2.2 - Sistema de Múltiplos Modelos (ATUAL)
O projeto agora oferece **dois métodos de segmentação** com interface de escolha!

**🚀 Novos Recursos:**
- **🎯 Interface de escolha**: Menu interativo para seleção de método
- **🧠 DeepLabV3**: Máxima precisão com deep learning
- **📐 Parametrização**: Máxima velocidade com funções indicadoras
- **📊 Comparação automática**: Métricas de performance para cada método

**🏗️ Arquitetura de Modelos:**

```mermaid
graph LR
    A["main.py"] --> B["escolher_modelo.py"]
    B --> C["🧠 DeepLabV3"]
    B --> D["📐 Parametrização"]
    
    C --> C1["ModeloSegmentacaoDeepLabV3"]
    C --> C2["segmentacao_imagens_Deeplabv3.py"]
    C --> C3["🎯 Alta Precisão"]
    
    D --> D1["ModeloSegmentacaoParametrizacao"]
    D --> D2["segmentacao_imagens_parametrizacao_indicadora.py"]
    D --> D3["⚡ Alta Velocidade"]
    
    C3 --> E["📊 Resultados"]
    D3 --> E
    
    classDef main fill:#2196F3,stroke:#1976D2,color:#fff
    classDef models fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef engines fill:#FF9800,stroke:#F57C00,color:#fff
    
    class A,B main
    class C,D,C1,D1 models
    class C2,D2,C3,D3,E engines
```

**⚖️ Comparação de Métodos:**

| Aspecto | 🧠 DeepLabV3 | 📐 Parametrização |
|---------|-------------|------------------|
| **Precisão** | ⭐⭐⭐⭐⭐ Máxima | ⭐⭐⭐⭐ Alta |
| **Velocidade** | ⭐⭐ ~15s/imagem | ⭐⭐⭐⭐⭐ ~3s/imagem |
| **Recursos** | GPU recomendada | CPU suficiente |
| **Método** | Deep Learning | Funções Matemáticas |
| **Uso Ideal** | Precisão crítica | Processamento em massa |

### 🔧 v0.2.1 - Refatoração e Otimização
**🛠️ Melhorias Arquiteturais:**
- **🔄 Renomeação**: `SegmentacaoPessoa` → `SegmentacaoDeepLabV3`
- **🗂️ Organização**: Eliminação de arquivos duplicados
- **📦 Modularidade**: Estrutura mais clara e manutenível

### 🖼️ v0.2.0 - Sistema de Segmentação de Imagens
**🚀 Implementação do DeepLabV3:**
- **🤖 Modelo pré-treinado** com backbone ResNet50
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

**🎯 Interface de Escolha:**
```
🎯 SELEÇÃO DE MODELO DE SEGMENTAÇÃO
================================================================
1️⃣  DeepLabV3 + ResNet101
   • Modelo pré-treinado de deep learning
   • Alta precisão na segmentação de pessoas
   • Processamento mais lento

2️⃣  Parametrização com Funções Indicadoras
   • Método matemático otimizado
   • Processamento rápido e eficiente
   • Visualização automática de silhuetas
   • Métricas detalhadas (MAE, R²)

Escolha uma opção (1-2) ou Enter para padrão (2):
```

## 🏗️ Arquitetura Completa

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
        C3["🎯 PyTorch + ResNet50"]
        
        C1 --> C2
        C2 --> C3
    end
    
    subgraph "📐 Modelo Parametrização"
        D1["ModeloSegmentacaoParametrizacao"]
        D2["SegmentacaoParametrizacaoIndicadora"]
        D3["📊 382 Funções Indicadoras"]
        
        D1 --> D2
        D2 --> D3
    end
    
    subgraph "📤 Saída"
        E1["📊 Relatórios JSON"]
        E2["🖼️ Máscaras Processadas"]
        E3["📈 Métricas de Qualidade"]
        E4["👁️ Visualizações"]
    end
    
    A1 --> B2
    A2 --> B2
    B3 --> C1
    B3 --> D1
    C1 --> E1
    D1 --> E1
    C2 --> E2
    D2 --> E2
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

### 📐 Módulo Parametrização
| Componente | Status | Descrição |
|------------|--------|-----------|
| `ModeloSegmentacaoParametrizacao` | ✅ | Coordenador Parametrização |
| `SegmentacaoParametrizacaoIndicadora` | ✅ | Engine matemático otimizado |
| `_aplicar_parametrizacao_linhas()` | ✅ | 382 funções indicadoras |
| `_otimizar_parametros_linha()` | ✅ | Otimização MSE rigorosa |
| `visualizar_amostra_resultados()` | ✅ | Visualização automática |

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

**Parametrização:**
```python
ModeloSegmentacaoParametrizacao(
    target_width=512,             # Largura da imagem
    target_height=382,            # Altura = nº funções indicadoras
    morph_kernel_size=5,          # Tamanho kernel morfológico
    min_area=100,                 # Filtro de ruído
    enhance_contrast=True         # Melhoria de contraste
)
```

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
    
    section Em Desenvolvimento
    Analytics Avançados :active, analytics, 2025-09-10, 5d
    
    section Planejado
    Interface Gráfica   :ui, after analytics, 7d
    Correlações Auto    :corr, after analytics, 5d
    Dashboard Interativo :dash, after ui, 5d
    Testes Automatizados :test, after dash, 3d
    Deploy Produção     :deploy, after test, 5d
```

### 🎯 v0.3.0 - Analytics Avançados (Próximo)
- **🧮 Correlações automáticas**: Relacionar medidas corporais ↔ silhuetas
- **📈 Insights estatísticos**: Padrões e tendências nos dados
- **🔍 Análise comparativa**: Before/After e Male/Female
- **📊 Métricas avançadas**: Precisão, recall, F1-score

### 🎛️ v0.4.0 - Interface Gráfica
- **🖥️ Dashboard Streamlit**: Interface web interativa
- **📊 Visualizações dinâmicas**: Gráficos e plots em tempo real
- **🎯 Configuração visual**: Ajustes de parâmetros via interface
- **📤 Exportação facilitada**: Download de resultados em múltiplos formatos

### 🚀 v0.5.0 - Deploy e Produção
- **🐳 Containerização Docker**: Deploy simplificado
- **☁️ Cloud deployment**: Suporte Azure/AWS
- **🔧 CI/CD pipeline**: Automação de build e deploy
- **📚 Documentação completa**: Guias de uso e API

## 📈 Status Atual

🚀 **Versão 0.2.2** - Sistema de múltiplos modelos de segmentação!

### 🏆 Marcos Alcançados
- ✅ **Base de dados robusta** e validação automática
- ✅ **Dois métodos de segmentação** com escolha interativa
- ✅ **Pipeline completa** dados → processamento → resultados
- ✅ **Qualidade enterprise** com logging e tratamento de erros
- ✅ **Métricas comparativas** entre diferentes métodos
- 🔄 **Próximo**: Analytics avançados e correlações automáticas

### 🎯 Tecnologias Utilizadas
- **🐍 Python 3.11+** - Linguagem principal
- **🤖 PyTorch + Torchvision** - Deep Learning (DeepLabV3)
- **📐 SciPy + NumPy** - Computação matemática (Parametrização)
- **🖼️ OpenCV** - Processamento de imagens
- **📊 Pandas + Matplotlib** - Análise e visualização de dados
- **⚡ CUDA** - Aceleração GPU (opcional para DeepLabV3)

### 🌟 Destaques da v0.2.2
- **🎛️ Interface de escolha** entre métodos de segmentação
- **⚖️ Comparação automática** de performance entre modelos
- **📊 Métricas específicas** para cada método (MSE, IoU, etc.)
- **🎭 Visualização automática** de silhuetas processadas
- **💾 Resultados estruturados** em formato JSON padronizado

---

**🔗 Links Úteis:**
- 📋 [CHANGELOG.md](CHANGELOG.md) - Histórico detalhado de versões
- 🐛 [Issues](../../issues) - Reportar bugs ou sugerir melhorias
- 🤝 [Contributing](../../pulls) - Contribuir com o projeto

**📞 Suporte:**
- 📧 Email: suporte@inovia.com
- 💬 Chat: [Discord INOVIA](https://discord.gg/inovia)
- 📱 WhatsApp: +55 (11) 99999-9999
