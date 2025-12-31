# Architecture & Implementation Details

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit User Interface                      │
│  (Document Upload, Model Selection, Q&A, Session Management)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐      ┌──────────┐    ┌──────────────┐
   │Document │      │RAG Core  │    │Quality & Safe │
   │ Loader  │      │ System   │    │ty Guardrails  │
   └────┬────┘      └────┬─────┘    └──────┬───────┘
        │                │                  │
        └────────────────┼──────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
┌─────────────┐     ┌──────────────┐   ┌────────────┐
│  Document   │     │  FAISS Index │   │ OpenAI API │
│  Processing │     │  (Local)     │   │ (Remote)   │
└─────────────┘     └──────────────┘   └────────────┘
```

## Component Details

### 1. Document Loader (`core/document_loader.py`)

**Supported Formats:**
- PDF: Uses PyPDF2 for text extraction
- DOCX: Uses python-docx for paragraph extraction
- TXT: Direct text reading
- Excel (XLSX, CSV): Uses pandas for data conversion

**Process:**
```
Raw Document
    ↓
Text Extraction (format-specific)
    ↓
Recursive Character Splitting (configurable overlap)
    ↓
Document Objects with Metadata
    ↓
OpenAI Embeddings
    ↓
FAISS Vector Store
```

### 2. Enhanced RAG Pipeline (`core/rag_pipeline.py`)

**Key Features:**
- Multi-model support (GPT-4, GPT-3.5-turbo)
- Dynamic model switching
- Similarity search with configurable k parameter
- Index persistence (save/load)

**Retrieval Process:**
```
Question
    ↓
OpenAI Embedding
    ↓
Similarity Search (FAISS)
    ↓
Top-K Documents Retrieved
    ↓
Prompt Template Construction
    ↓
LLM Generation
    ↓
Answer + Source Documents
```

### 3. Quality Assessment (`core/quality_assessor.py`)

**Scoring Metrics:**

| Metric | Weight | Measures |
|--------|--------|----------|
| Completeness | 30% | Adequacy in addressing question |
| Specificity | 25% | Concrete details, examples, numbers |
| Relevance | 25% | Direct connection to question |
| Confidence | 20% | Certainty (inverse of hedging) |

**Quality Thresholds:**
- Score ≥ 0.85: Excellent
- Score ≥ 0.70: Good
- Score ≥ 0.60: Fair
- Score ≥ 0.40: Poor
- Score < 0.40: Very Poor

### 4. Hallucination Detector (`core/hallucination_detector.py`)

**Detection Methods:**

1. **Unsupported Claims Detection**
   - Extracts key phrases from sentences
   - Checks if phrases appear in source context
   - Flags sentences with no supporting evidence

2. **Contradiction Detection**
   - Identifies negation patterns
   - Compares with source content
   - Flags conflicting statements

3. **Fabricated Facts Detection**
   - Identifies specific facts (dates, numbers, names)
   - Checks if facts appear in context
   - High confidence in anomalies

4. **Exaggeration Detection**
   - Identifies superlatives (always, never, all, etc.)
   - Assesses if claims are well-supported
   - Flags overstated assertions

5. **Citation Coverage**
   - Checks for explicit source mentions
   - Flags long answers without citations

### 5. Fallback Handler (`utils/fallback_handler.py`)

**Fallback Strategies:**

**Strategy 1: Increase Context**
- Retrieves 8 chunks instead of 4
- Best for: Incomplete answers

**Strategy 2: Strict Matching**
- Applies similarity score threshold (< 0.5)
- Only uses high-confidence matches
- Best for: High hallucination risk

**Strategy 3: Query Expansion**
- Generates 3-4 query variants
- Searches with expanded queries
- Deduplicates results
- Best for: Low specificity

**Strategy 4: Multi-Strategy**
- Combines multiple approaches
- Gets best coverage
- Best for: General improvement

## Data Flow

### Document Upload & Indexing

```
1. User uploads file(s)
   ↓
2. File saved to temp directory
   ↓
3. DocumentLoader identifies file type
   ↓
4. Format-specific extractor processes content
   ↓
5. RecursiveCharacterTextSplitter chunks text
   ↓
6. OpenAI Embeddings generates vectors
   ↓
7. FAISS builds index from vectors
   ↓
8. Index saved to disk
   ↓
9. Session updated with document info
```

### Question Answering Flow

```
1. User enters question
   ↓
2. Question embedded using OpenAI
   ↓
3. FAISS retrieves top-K similar chunks
   ↓
4. LLM generates answer from context
   ↓
5. Quality Assessor evaluates answer
   ├─→ Completeness check
   ├─→ Specificity check
   ├─→ Relevance check
   └─→ Confidence check
   ↓
6. HallucinationDetector scans answer
   ├─→ Unsupported claims
   ├─→ Contradictions
   ├─→ Fabricated facts
   └─→ Exaggerations
   ↓
7. If quality < threshold:
   ├─→ FallbackHandler activates
   ├─→ Re-retrieves with strategy
   └─→ Regenerates answer
   ↓
8. Results displayed with metrics
```

## Performance Characteristics

### Indexing
- PDF (10MB): ~30 seconds
- DOCX (5MB): ~15 seconds
- TXT (2MB): ~5 seconds
- Index size: ~100MB per 1M tokens

### Query Processing
- Retrieval: 0.2-0.5s (FAISS)
- LLM generation: 1-5s (depends on model)
- Quality assessment: 0.5-1s
- Hallucination detection: 0.3-0.8s
- **Total: 2-8 seconds per query**

### Token Usage (Approx.)
- Embedding: 0.02¢ per 1K tokens
- GPT-3.5-turbo: 0.5¢-1.5¢ per query
- GPT-4-turbo: 1¢-3¢ per query

## Configuration Impact

### Chunk Size
- Smaller (500): Better precision, more chunks
- Larger (1500+): Better context, fewer chunks
- Recommended: 1000

### Chunk Overlap
- No overlap: Faster, less context
- 200 overlap: Balanced
- 500+ overlap: Better continuity, slower
- Recommended: 200

### Retrieval K
- k=4: Fast, may miss context
- k=8: Balanced (used in fallback)
- k=12+: Comprehensive but slower
- Recommended: 4 (standard), 8 (fallback)

### Temperature
- 0.0: Deterministic, consistent
- 0.3: Slightly creative, maintains consistency
- 0.7+: Creative, may hallucinate more
- Current: 0.3 (optimal for RAG)

## Security Considerations

1. **API Key Security**
   - Stored in .env (not version controlled)
   - Never logged or exposed
   - Recommend API key rotation

2. **Data Privacy**
   - Documents processed locally
   - Only embeddings sent to OpenAI
   - Sessions stored locally
   - No external data sharing

3. **Output Safety**
   - Hallucination detection prevents false claims
   - Quality assessment filters low-quality answers
   - Confidence scoring indicates reliability

## Scalability Notes

### Current Limitations
- Single-machine FAISS index
- In-memory document processing
- Sequential query processing

### Future Improvements
- Distributed index (Milvus, Weaviate)
- Batch processing
- Caching layer
- Multi-worker architecture

---

For more details, see individual module docstrings.
