# Feature Documentation

## Quality Assessment Features

### What is Quality Assessment?

Quality Assessment evaluates how well the RAG system answered your question. It scores answers on multiple dimensions and provides recommendations for improvement.

### Quality Metrics Explained

#### 1. Completeness (30% weight)
**Measures:** Does the answer fully address your question?

| Score | Interpretation | Examples |
|-------|---|---|
| 90-100% | Comprehensive | "The system has 5 main components: A, B, C, D, E. Each works by..." |
| 70-89% | Good coverage | "The main features include: X, Y, and Z..." |
| 50-69% | Partial | "It does X and Y" (missing important details) |
| 30-49% | Incomplete | "Yes, it has features" (very vague) |
| <30% | Very incomplete | "I'm not sure" (non-answer) |

**What affects it:**
- Answer length
- Depth of explanation
- Whether it addresses all parts of question

#### 2. Specificity (25% weight)
**Measures:** How concrete and detailed is the answer?

| Score | Indicators |
|-------|---|
| High | Contains numbers, dates, code examples, quotes, technical terms |
| Medium | Has some details but lacks examples |
| Low | Vague or generic language |

**Examples:**
- ✅ Specific: "The API supports 5 endpoints: GET, POST, PUT, DELETE, PATCH"
- ❌ Non-specific: "The API supports multiple endpoints"

#### 3. Relevance (25% weight)
**Measures:** How directly does the answer address the question?

| Score | Meaning |
|-------|---|
| 95%+ | Answer is perfectly on-topic |
| 80-94% | Answer is mostly relevant |
| 60-79% | Some relevant content mixed with off-topic |
| <60% | Mostly off-topic |

#### 4. Confidence (20% weight)
**Measures:** How certain does the answer sound?

**Hedging words that reduce confidence:**
- "maybe", "perhaps", "possibly", "might"
- "could be", "appears to be", "seems"
- "arguably", "probably", "potentially"

**High confidence examples:**
- ✅ "The authentication service manages user login"
- ❌ "The authentication service might manage user login"

### Quality Score Interpretation

| Score | Level | Recommendation |
|-------|-------|---|
| 85-100 | 🟢 Excellent | Trust and use the answer |
| 70-84 | 🟢 Good | Good answer, verify if needed |
| 60-69 | 🟡 Fair | Acceptable but may need clarification |
| 40-59 | 🔴 Poor | Don't fully trust, ask follow-up |
| <40 | 🔴 Very Poor | Not reliable, rephrase question |

## Hallucination Detection Features

### What is a Hallucination?

A hallucination occurs when the AI generates plausible-sounding but false information that isn't in the source documents.

### Types of Hallucinations Detected

#### 1. Unsupported Claims
Claims that don't appear in source documents.

**Example:**
- Document: "The system was released in 2023"
- Hallucination: "The system won 3 major awards" (not mentioned)

#### 2. Contradictions
Statements that conflict with source documents.

**Example:**
- Document: "Authentication is optional"
- Hallucination: "Authentication is required" (contradicts)

#### 3. Fabricated Facts
Specific claims (dates, numbers, names) invented by the model.

**Example:**
- Hallucination: "Released on March 15, 2024" (if not in source)
- Real: "Released in March 2024" (from source)

#### 4. Exaggerations
Overstated claims with superlatives beyond what source supports.

**Example:**
- Document: "The system is faster than alternative X"
- Hallucination: "The system is THE FASTEST available" (overstated)

#### 5. Citation Issues
Long answers without mentioning sources.

**Example:**
- ❌ Long answer with no "according to..." or source mention
- ✅ "According to the documentation..." or "As mentioned in..."

### Hallucination Risk Score

| Risk | Level | Action |
|------|-------|--------|
| 0-20% | 🟢 Very Low | Safe to use |
| 20-40% | 🟢 Low | Generally safe |
| 40-60% | 🟡 Medium | Verify important claims |
| 60-80% | 🔴 High | Don't fully trust |
| 80%+ | 🔴 Critical | Major hallucination risk |

## Fallback Strategies

### When Do Fallbacks Activate?

Fallbacks automatically activate when answer quality < 0.6 (60%).

### Strategy 1: Increase Context

**When used:** Answer seems incomplete

**How it works:**
- Retrieves 8 document chunks instead of 4
- Provides more source material
- Regenerates answer with fuller context

**Best for:**
- Questions requiring comprehensive answers
- Complex topics needing detailed explanation

### Strategy 2: Strict Matching

**When used:** High hallucination risk detected

**How it works:**
- Only uses high-confidence retrieved chunks
- Filters out borderline matches
- More conservative retrieval

**Best for:**
- Factual accuracy critical
- Questions about specific details

### Strategy 3: Query Expansion

**When used:** Low specificity detected

**How it works:**
- Rephrases question in 3-4 ways
- Searches for each variant
- Combines diverse results

**Best for:**
- Questions that can be asked multiple ways
- Specific concepts or definitions

### Strategy 4: Multi-Strategy

**When used:** General quality improvement needed

**How it works:**
- Combines all above strategies
- Gets maximum coverage
- Deduplicates results

**Best for:**
- Highly important queries
- When accuracy is paramount

## Document Format Support

### PDF Files
- Text extraction from any PDF
- Preserves page structure
- Supports scanned PDFs with OCR capability

### DOCX Files
- Extracts all paragraphs
- Maintains formatting structure
- Handles tables and lists

### Text Files
- Plain .txt files
- Any encoding (automatically detected)
- No preprocessing needed

### Excel Files
- .xlsx and .xls formats
- CSV files
- Converts tables to readable format
- Includes column headers

## Session Management

### What are Sessions?

Sessions track:
- Documents you uploaded
- All questions and answers
- Quality scores for each answer
- Model used for each query
- Timestamps

### Why Use Sessions?

1. **Record Keeping:** Keep history of your research
2. **Comparison:** See quality trends
3. **Export:** Generate reports
4. **Reuse:** Load previous work

### Session Features

- **Create New:** Start fresh session
- **Load Existing:** Resume previous work
- **Export:** Generate markdown reports
- **View History:** See all conversations
- **Quality Metrics:** Average score over session

## Model Selection

### GPT-3.5 Turbo
| Feature | Rating |
|---|---|
| Speed | ⚡⚡⚡ Fast |
| Quality | ⭐⭐⭐⭐ Good |
| Cost | 💰 Low |
| Best for | Fast responses, cost-effective |

### GPT-4
| Feature | Rating |
|---|---|
| Speed | ⚡⚡ Medium |
| Quality | ⭐⭐⭐⭐⭐ Excellent |
| Cost | 💰💰 High |
| Best for | Complex reasoning, accuracy |

### GPT-4 Turbo
| Feature | Rating |
|---|---|
| Speed | ⚡⚡ Medium |
| Quality | ⭐⭐⭐⭐⭐ Excellent |
| Cost | 💰💰 High |
| Best for | Best overall, largest context |

## Configuration Guide

### For Accuracy
```env
OPENAI_MODEL=gpt-4-turbo
QUALITY_THRESHOLD=0.7
CHECK_HALLUCINATION=true
ENABLE_FALLBACK=true
CHUNK_SIZE=1000
```

### For Speed
```env
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=750
CHECK_HALLUCINATION=false
ENABLE_FALLBACK=false
```

### For Balance (Recommended)
```env
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=1000
QUALITY_THRESHOLD=0.6
CHECK_HALLUCINATION=true
ENABLE_FALLBACK=true
```

---

For technical details, see ARCHITECTURE.md
