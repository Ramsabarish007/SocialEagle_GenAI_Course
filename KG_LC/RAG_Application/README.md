# RAG Document Assistant

A production-ready Retrieval-Augmented Generation (RAG) application with advanced quality guardrails, hallucination detection, and fallback strategies.

## 🌟 Features

### Core RAG Capabilities
- **Multi-format Document Support**: PDF, DOCX, TXT, Excel files
- **Intelligent Chunking**: Recursive text splitting with configurable chunk size and overlap
- **Vector Embeddings**: OpenAI embeddings with FAISS vector store
- **Fast Retrieval**: Efficient similarity search over indexed documents

### Quality Assurance
- **Answer Quality Assessment**: Evaluates completeness, specificity, relevance, and confidence
- **Hallucination Detection**: Identifies unsupported claims, contradictions, and fabricated facts
- **Confidence Scoring**: Measures answer reliability (0-1 scale)
- **Quality-based Fallback**: Automatically applies fallback strategies for low-quality answers

### Smart Fallback Strategies
1. **Increased Context**: Retrieves more chunks for comprehensive coverage
2. **Strict Matching**: Uses similarity thresholds to reduce hallucination risk
3. **Query Expansion**: Expands queries with related terms and synonyms
4. **Multi-strategy**: Combines multiple retrieval approaches

### Model Support
- **GPT-4 Turbo**: Most powerful, best for complex queries
- **GPT-4**: Powerful reasoning capabilities
- **GPT-3.5 Turbo**: Fast and cost-effective

### Session Management
- Save and load conversation sessions
- Document upload tracking
- Conversation history with quality scores
- Export sessions to JSON or Markdown

## 📋 Requirements

- Python 3.9+
- OpenAI API key
- FAISS (automatically installed)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd RAG_Application

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your OpenAI API key
# Set OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

### 3. Run the Application

```bash
# Start Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Usage Guide

### Upload Documents

1. Use the **Upload Documents** section to select files
2. Supported formats: PDF, DOCX, TXT, XLSX, CSV
3. Click **Load & Index Documents** to process

### Ask Questions

1. Enter your question in the text area
2. Click **Get Answer** to retrieve results
3. View:
   - Generated answer
   - Quality assessment metrics
   - Hallucination detection report
   - Source documents used

### Manage Sessions

1. Create new sessions or load existing ones
2. Automatically tracks all conversations
3. Export sessions as reports

### Configure Models

- Select different LLM models from the sidebar
- Models update automatically without reindexing

## 🔧 Configuration Options

Edit `.env` to customize:

```env
# Model Selection
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Quality Thresholds
QUALITY_THRESHOLD=0.6
HALLUCINATION_THRESHOLD=0.5

# Enable/Disable Features
CHECK_HALLUCINATION=true
ENABLE_FALLBACK=true
```

## 🛡️ Quality Guardrails

### Quality Assessment Metrics

**Completeness (30% weight)**: Does the answer fully address the question?
- Short answers (<30 words): Low completeness
- Longer, detailed answers: High completeness

**Specificity (25% weight)**: Does the answer contain specific details?
- Checks for: numbers, quotes, technical terms, varied sentence structure
- Higher specificity = more credible answers

**Relevance (25% weight)**: How relevant is the answer to the question?
- Word overlap analysis between question and answer
- Semantic relevance assessment

**Confidence (20% weight)**: How confident is the model?
- Detects hedging language (maybe, perhaps, seems, etc.)
- Reduces score for excessive uncertainty

### Hallucination Detection

Checks for:
1. **Unsupported Claims**: Assertions not backed by source documents
2. **Contradictions**: Conflicting statements within the answer or with sources
3. **Fabricated Facts**: Specific claims (dates, numbers, proper nouns) not in sources
4. **Exaggerations**: Overstated or superlative claims not well-supported
5. **Citation Issues**: Lack of proper source attribution

## 📊 Project Structure

```
RAG_Application/
├── app.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment configuration template
├── README.md                        # This file
├── core/
│   ├── __init__.py
│   ├── document_loader.py          # Multi-format document loading
│   ├── rag_pipeline.py             # Enhanced RAG system
│   ├── quality_assessor.py         # Answer quality evaluation
│   └── hallucination_detector.py   # Hallucination detection
├── utils/
│   ├── __init__.py
│   ├── fallback_handler.py         # Fallback strategies
│   ├── session_manager.py          # Session management
│   └── logger.py                   # Logging utilities
├── config/
│   └── config.py                   # Configuration management
├── indexes/                         # FAISS vector indexes (auto-created)
├── sessions/                        # Session data (auto-created)
├── logs/                           # Application logs (auto-created)
└── exports/                        # Exported reports (auto-created)
```

## 🔄 Workflow

```
1. Upload Documents
   ↓
2. Document Loading & Chunking
   ↓
3. Embedding Generation
   ↓
4. FAISS Index Building
   ↓
5. Query Processing
   ├→ Retrieve relevant chunks
   ├→ Generate answer
   └→ Quality Assessment & Hallucination Detection
   ↓
6. Quality Check
   ├→ If Quality ≥ 0.6: Return answer
   └→ If Quality < 0.6: Apply Fallback
   ↓
7. Display Results
```

## 🤖 Answer Quality Example

**Good Answer**:
- Quality: 0.82 (Good)
- Completeness: 90% (addresses all aspects)
- Specificity: 85% (includes numbers, examples)
- Relevance: 95% (directly answers question)
- Confidence: 80% (expresses certainty)
- Hallucination Risk: 5% (low)

**Poor Answer**:
- Quality: 0.45 (Poor)
- Completeness: 40% (incomplete coverage)
- Specificity: 30% (vague)
- Relevance: 60% (partially relevant)
- Confidence: 50% (hedged)
- Hallucination Risk: 45% (high)

## 🔐 Security Notes

- API keys are stored in `.env` file (not version controlled)
- Sessions are stored locally
- No data is sent to external services except OpenAI
- Logs contain minimal sensitive information

## 🐛 Troubleshooting

### "Invalid API Key"
- Check `.env` file has correct `OPENAI_API_KEY`

### "FAISS Index Error"
- Run: `pip install --upgrade faiss-cpu`
- Or use GPU version: `pip install faiss-gpu`

### "Document Loading Failed"
- Ensure file format is supported
- Check file is not corrupted
- Try with a smaller document first

### "Slow Query Processing"
- Reduce CHUNK_SIZE in `.env`
- Use GPT-3.5-turbo for faster responses
- Disable hallucination checks for speed

## 📈 Performance Tips

1. **Chunk Optimization**: 
   - Smaller chunks (500-750): Better for precise retrieval
   - Larger chunks (1500-2000): Better for context

2. **Model Selection**:
   - GPT-3.5-turbo: Fast, cost-effective
   - GPT-4: Accurate, slower

3. **Quality Thresholds**:
   - Lower threshold (0.5): More answers, some lower quality
   - Higher threshold (0.7): Fewer answers, higher quality

4. **Fallback Strategy**:
   - Disable if speed is critical
   - Enable for accuracy

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional document formats (HTML, Markdown)
- More sophisticated chunking strategies
- Additional LLM providers (Anthropic, Cohere, etc.)
- Advanced visualization of document relationships
- Multi-language support

## 📞 Support

For issues or questions:
1. Check README.md and documentation
2. Review error messages in logs/
3. Verify .env configuration
4. Test with sample documents

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Version**: 1.0.0  
**Last Updated**: December 2024
