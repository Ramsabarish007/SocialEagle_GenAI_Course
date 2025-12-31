# Project File Structure & Descriptions

## 📁 Root Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application - entry point |
| `examples.py` | Usage examples for developers |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Environment configuration template |
| `setup.bat` | Windows setup script |
| `setup.sh` | macOS/Linux setup script |

## 📚 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Complete feature overview and usage guide |
| `QUICKSTART.md` | 5-minute setup and first-run guide |
| `ARCHITECTURE.md` | Technical design and implementation details |
| `FEATURES.md` | Feature explanations and configuration guide |
| `API_REFERENCE.md` | Code API documentation with examples |
| `PROJECT_SUMMARY.md` | Project overview and achievements |
| `FILE_STRUCTURE.md` | This file - file organization guide |

## 🔧 Core Modules (`core/`)

### `__init__.py`
- Package initialization
- Exports: DocumentLoader, EnhancedRAG, QualityAssessor, HallucinationDetector

### `document_loader.py` (300+ lines)
**Handles multi-format document loading and processing**
- Classes:
  - `DocumentLoader`: Main document loading class
- Features:
  - PDF support (PyPDF2)
  - DOCX support (python-docx)
  - Text file support
  - Excel/CSV support (pandas)
  - Recursive character splitting
  - Document metadata preservation
  - Batch file loading
  - File statistics

### `rag_pipeline.py` (280+ lines)
**Enhanced RAG system with multi-model support**
- Classes:
  - `EnhancedRAG`: Main RAG class
- Features:
  - FAISS vector store integration
  - Multi-model support (GPT-3.5, GPT-4, GPT-4-turbo)
  - Dynamic model switching
  - Similarity search
  - Index persistence
  - Source document retrieval
  - Configurable prompting

### `quality_assessor.py` (350+ lines)
**Answer quality evaluation system**
- Classes:
  - `QualityAssessor`: Quality evaluation class
- Features:
  - Completeness assessment
  - Specificity evaluation
  - Relevance scoring
  - Confidence measurement
  - Hallucination risk detection
  - Quality-to-level conversion
  - Recommendations generation
  - Batch assessment

### `hallucination_detector.py` (400+ lines)
**Hallucination detection and prevention**
- Classes:
  - `HallucinationDetector`: Hallucination detection class
- Features:
  - Unsupported claims detection
  - Contradiction identification
  - Fabricated facts detection
  - Exaggeration detection
  - Citation coverage checking
  - Confidence scoring
  - Detailed reporting
  - Multi-method detection

## 🛠️ Utility Modules (`utils/`)

### `__init__.py`
- Package initialization
- Exports: FallbackHandler, SessionManager, setup_logger

### `fallback_handler.py` (350+ lines)
**Fallback strategies for low-quality answers**
- Classes:
  - `FallbackHandler`: Fallback strategy handler
- Methods:
  - `apply_fallback()`: Determines and applies strategy
  - `_apply_increase_context()`: Retrieve more chunks
  - `_apply_strict_matching()`: Use confidence threshold
  - `_apply_query_expansion()`: Expand query variants
  - `_apply_multi_strategy()`: Combine strategies
  - `combine_fallback_result()`: Merge results

### `session_manager.py` (400+ lines)
**Session and conversation management**
- Classes:
  - `SessionManager`: Session management class
- Features:
  - Session creation and loading
  - Document tracking
  - Conversation history
  - Quality score averaging
  - Session export (JSON/Markdown)
  - Session listing and deletion
  - Summary generation

### `logger.py` (30 lines)
**Logging configuration**
- Functions:
  - `setup_logger()`: Configure logger with file and console handlers

## ⚙️ Configuration (`config/`)

### `__init__.py`
- Package initialization
- Exports: Config

### `config.py` (100+ lines)
**Configuration management**
- Classes:
  - `Config`: Central configuration class
- Features:
  - Environment variable reading
  - Default values
  - Validation method
  - Type-safe access
  - Configurable thresholds and weights

## 📂 Auto-Created Directories

| Directory | Purpose |
|-----------|---------|
| `data/` | User uploaded documents (optional) |
| `indexes/` | FAISS vector indexes |
| `sessions/` | Session data files (JSON) |
| `logs/` | Application logs |
| `exports/` | Exported session reports |

## 📊 File Statistics

### Lines of Code
- **Core modules**: ~1,330 lines
- **Utils modules**: ~780 lines  
- **Configuration**: ~100 lines
- **Streamlit app**: ~600 lines
- **Documentation**: ~3,000 lines
- **Total**: ~5,810 lines

### File Count
- **Python files**: 11
- **Documentation**: 7
- **Configuration**: 2
- **Scripts**: 2
- **Total tracked files**: 22+

## 🔄 Module Dependencies

```
app.py (Streamlit)
├── core.document_loader
├── core.rag_pipeline
├── core.quality_assessor
├── core.hallucination_detector
├── utils.fallback_handler
├── utils.session_manager
├── utils.logger
└── config.config

core.document_loader
└── langchain_text_splitters

core.rag_pipeline
├── langchain_openai
├── langchain_community
└── langchain.prompts

core.quality_assessor
└── langchain_openai

core.hallucination_detector
└── langchain_openai

utils.fallback_handler
└── core.rag_pipeline

utils.session_manager
└── (standard library only)

utils.logger
└── (standard library only)

config.config
└── (standard library only)
```

## 📝 Documentation Hierarchy

```
README.md (Start here)
├── QUICKSTART.md (5-minute setup)
├── ARCHITECTURE.md (Technical details)
├── FEATURES.md (Feature explanations)
├── API_REFERENCE.md (Code examples)
└── PROJECT_SUMMARY.md (Overview)

examples.py (Code examples)
FILE_STRUCTURE.md (This file)
```

## 🚀 Getting Started File Order

1. **README.md** - Understand what this is
2. **QUICKSTART.md** - Get it running in 5 minutes
3. **app.py** - Run `streamlit run app.py`
4. Upload documents → Ask questions
5. **FEATURES.md** - Understand quality metrics
6. **API_REFERENCE.md** - Use in your code
7. **ARCHITECTURE.md** - Deep technical dive

## 💾 Important Locations

### Configuration
- `.env` (after setup) - API keys and settings

### Data
- `indexes/` - Searchable document index
- `sessions/` - Conversation history
- `logs/` - Application logs
- `exports/` - Generated reports

### Code Entry Points
- `app.py` - Streamlit UI
- `examples.py` - Command-line examples
- `core/rag_pipeline.py` - RAG API
- `utils/session_manager.py` - Session API

## 📦 Dependencies by Purpose

### Core RAG
- langchain (0.3.13)
- langchain-openai (0.2.14)
- openai (1.58.1)
- faiss-cpu (1.9.0.post1)

### Document Processing
- PyPDF2 (4.0.1)
- python-docx (0.8.11)
- openpyxl (3.11.0)
- pandas (2.2.3)

### Interface
- streamlit (1.39.0)
- streamlit-option-menu (0.4.1)

### Utilities
- python-dotenv (1.0.1)
- pydantic (2.10.5)
- rich (13.9.4)

---

**Total Package Size**: ~150-200MB (including dependencies)  
**Python Version**: 3.9+  
**Last Updated**: December 2024
