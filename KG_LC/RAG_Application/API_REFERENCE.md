# API Reference

## Core Classes

### DocumentLoader

Load and process multi-format documents.

```python
from core.document_loader import DocumentLoader

loader = DocumentLoader(
    chunk_size=1000,
    chunk_overlap=200
)

# Load single file
documents = loader.load_file("document.pdf", file_type="pdf")

# Load directory
documents = loader.load_directory("./documents", file_types=["pdf", "docx"])

# Get statistics
stats = loader.get_file_stats(documents)
print(f"Total documents: {stats['total_documents']}")
```

**Methods:**
- `load_file(path, file_type)` - Load single file
- `load_directory(path, file_types)` - Load all files in directory
- `get_file_stats(documents)` - Get document statistics

---

### EnhancedRAG

Main RAG system for document retrieval and answer generation.

```python
from core.rag_pipeline import EnhancedRAG

# Initialize
rag = EnhancedRAG(
    openai_api_key="<YOUR_OPENAI_API_KEY>",
    model_name="gpt-3.5-turbo",
    embedding_model="text-embedding-3-small"
)

# Build index
rag.build_index(documents)

# Query
result = rag.query("Your question here")
print(result['answer'])

# Switch model
rag.switch_model("gpt-4")

# Save/Load index
rag.save_index("./indexes/my_index")
rag.load_index("./indexes/my_index")
```

**Methods:**
- `build_index(documents)` - Create vector index
- `query(question)` - Get answer
- `switch_model(model_name)` - Change LLM model
- `similarity_search(query, k)` - Retrieve documents
- `save_index(path)` - Persist index
- `load_index(path)` - Load index
- `get_statistics()` - System statistics

**Available Models:**
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`

---

### QualityAssessor

Evaluate answer quality on multiple dimensions.

```python
from core.quality_assessor import QualityAssessor

assessor = QualityAssessor(openai_api_key="<YOUR_OPENAI_API_KEY>")

# Assess single answer
quality = assessor.assess_answer(
    question="What is X?",
    answer="X is...",
    context="Source material..."
)

print(f"Quality Score: {quality['overall_score']}")
print(f"Level: {quality['quality_level']}")

# Assess batch
batch_results = assessor.assess_batch(
    questions=[...],
    answers=[...],
    contexts=[...]
)
```

**Quality Metrics:**
- `completeness` - Does it answer fully?
- `specificity` - Is it detailed?
- `relevance` - Is it on-topic?
- `confidence` - Is it certain?
- `hallucination_risk` - False information risk

**Scoring:**
- 0.85-1.0: Excellent
- 0.70-0.84: Good
- 0.60-0.69: Fair
- 0.40-0.59: Poor
- <0.40: Very Poor

---

### HallucinationDetector

Detect and report hallucinations in answers.

```python
from core.hallucination_detector import HallucinationDetector

detector = HallucinationDetector(openai_api_key="<YOUR_OPENAI_API_KEY>")

# Detect hallucinations
detections = detector.detect_hallucinations(
    answer="The answer text...",
    source_documents=[doc1, doc2, ...],
    question="Original question"
)

# Check results
if detections['is_hallucination_likely']:
    print("High hallucination risk!")

# Generate report
report = detector.generate_hallucination_report(detections)
print(report)
```

**Detections Include:**
- `unsupported_claims` - Claims not in source
- `contradictions` - Conflicting statements
- `fabricated_facts` - Made-up specific facts
- `exaggerations` - Overstated claims
- `citation_issues` - Missing source attribution
- `overall_hallucination_risk` - 0-1 score
- `is_hallucination_likely` - Boolean

---

### FallbackHandler

Apply fallback strategies for low-quality answers.

```python
from utils.fallback_handler import FallbackHandler

handler = FallbackHandler(rag_system)

# Apply fallback
fallback = handler.apply_fallback(
    question="Your question",
    quality_assessment=quality_result,
    source_documents=source_docs
)

# Combine with original
combined = handler.combine_fallback_result(
    original_result=rag_result,
    fallback_result=fallback
)

print(f"Strategy: {fallback['strategy']}")
print(f"Improvement: {fallback['improvement']}")
```

**Strategies:**
- `increase_context` - Retrieve more chunks
- `strict_matching` - Use confidence threshold
- `query_expansion` - Expand query variants
- `multi_strategy` - Combine approaches

---

### SessionManager

Manage sessions and conversation history.

```python
from utils.session_manager import SessionManager

manager = SessionManager(session_dir="sessions")

# Create session
session_id = manager.create_session("my_session")

# Add document
manager.add_document("file.pdf", "path/file.pdf", 50)

# Add conversation
manager.add_conversation(
    question="What is X?",
    answer="X is...",
    model="gpt-3.5-turbo",
    quality_score=0.85
)

# Save
manager.save_session()

# Get summary
summary = manager.get_session_summary()

# Export
manager.export_session(session_id, "report.md", format="md")

# List sessions
sessions = manager.list_sessions()
```

**Methods:**
- `create_session(name)` - Create new session
- `load_session(session_id)` - Load existing
- `save_session()` - Persist to disk
- `add_document()` - Track loaded document
- `add_conversation()` - Log Q&A pair
- `export_session()` - Generate report
- `list_sessions()` - List all sessions
- `delete_session()` - Remove session

---

## Configuration

### Environment Variables

```env
# OpenAI Settings
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Quality Assessment
QUALITY_THRESHOLD=0.6
COMPLETENESS_WEIGHT=0.3
SPECIFICITY_WEIGHT=0.25
RELEVANCE_WEIGHT=0.25
CONFIDENCE_WEIGHT=0.2

# Hallucination Detection
HALLUCINATION_THRESHOLD=0.5
CHECK_HALLUCINATION=true

# Fallback
ENABLE_FALLBACK=true

# Paths
INDEX_PERSIST_DIR=indexes
SESSION_DIR=sessions
LOG_DIR=logs
EXPORT_DIR=exports
```

### Programmatic Configuration

```python
from config.config import Config

# Validate configuration
Config.validate()

# Access settings
print(Config.OPENAI_MODEL)
print(Config.CHUNK_SIZE)
print(Config.QUALITY_THRESHOLD)
```

---

## Return Value Examples

### Query Result

```python
{
    "answer": "The answer text...",
    "source_documents": [Document(...), ...],
    "query_time": 2.34,
    "model": "gpt-3.5-turbo",
    "metrics": {
        "query_time": 2.34,
        "num_source_chunks": 4,
        "answer_tokens": 150,
        "retrieval_method": "vector_similarity"
    }
}
```

### Quality Assessment Result

```python
{
    "metrics": {
        "completeness": 0.85,
        "specificity": 0.80,
        "relevance": 0.90,
        "confidence": 0.75,
        "hallucination_risk": 0.15
    },
    "overall_score": 0.82,
    "quality_level": "Good",
    "needs_fallback": False,
    "recommendations": [
        "Consider providing more specific examples"
    ]
}
```

### Hallucination Detection Result

```python
{
    "unsupported_claims": [...],
    "contradictions": [...],
    "fabricated_facts": [...],
    "exaggerations": [...],
    "citation_issues": [...],
    "confidence_score": 0.85,
    "overall_hallucination_risk": 0.20,
    "is_hallucination_likely": False
}
```

---

## Error Handling

```python
try:
    documents = loader.load_file("file.pdf")
    rag.build_index(documents)
    result = rag.query("question")
except FileNotFoundError:
    print("Document not found")
except ImportError:
    print("Required library not installed")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

For more examples, see `examples.py`
