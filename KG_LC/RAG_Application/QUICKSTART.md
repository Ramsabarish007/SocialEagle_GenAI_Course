# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Configure API Key (1 minute)

1. Open `.env` file in your editor
2. Replace `your_openai_api_key_here` with your actual API key
3. Save the file

Get your API key from: https://platform.openai.com/api-keys

### Step 3: Run the App (30 seconds)

```bash
streamlit run app.py
```

Browser will open automatically at `http://localhost:8501`

## First Run

### 1. Create a Session
- Enter session name in sidebar
- Click "Create Session"

### 2. Upload Documents
- Click "Choose documents"
- Select PDF, DOCX, TXT, or Excel files
- Click "Load & Index Documents"

### 3. Ask a Question
- Type your question
- Click "Get Answer"
- Review quality metrics and hallucination detection

## Key Features Explained

### Quality Assessment
Shows if answer is:
- **Excellent** (85-100%): Reliable, complete, specific
- **Good** (70-84%): Mostly reliable
- **Fair** (60-69%): Acceptable with some gaps
- **Poor** (40-59%): Limited reliability
- **Very Poor** (<40%): Not reliable

### Hallucination Risk
- **🟢 LOW RISK** (<50%): Safe to use
- **🔴 HIGH RISK** (>50%): Verify before using

### Fallback Strategies
Automatically applied when answer quality is low:
1. **More Context**: Increases retrieved chunks from 4 to 8
2. **Strict Matching**: Uses similarity threshold
3. **Query Expansion**: Rephrases question

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Invalid API key"
- Check `.env` has correct key
- Can't share or test keys with others

### Slow responses
- Try GPT-3.5-turbo (faster than GPT-4)
- Reduce chunk size in `.env`
- Disable hallucination checks

### Out of memory error
- Reduce CHUNK_SIZE in `.env` (try 500-750)
- Upload fewer documents at once
- Use GPT-3.5-turbo

## Configuration Tips

**For Accuracy:**
```env
OPENAI_MODEL=gpt-4-turbo
QUALITY_THRESHOLD=0.7
CHECK_HALLUCINATION=true
ENABLE_FALLBACK=true
```

**For Speed:**
```env
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=750
CHECK_HALLUCINATION=false
ENABLE_FALLBACK=false
```

**For Balance:**
```env
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=1000
QUALITY_THRESHOLD=0.6
CHECK_HALLUCINATION=true
ENABLE_FALLBACK=true
```

## Example Questions

**Completeness & Specificity:**
- "List all features mentioned in the documentation"
- "What are the steps to configure the system?"
- "How do X and Y interact?"

**Quality Results:**
- "Explain X in detail" (usually good results)
- "What is X?" (vague, may need follow-up)
- "Compare X with Y" (requires specificity)

## Next Steps

- Read full README.md for advanced features
- Explore different models and settings
- Export sessions for record-keeping
- Try different document types

## Common Questions

**Q: Do I need internet?**
A: Yes, for OpenAI API calls. Document processing is local.

**Q: Can I use free OpenAI API?**
A: No, you need a paid account with credits.

**Q: How much does it cost?**
A: Depends on document size and model. Usually $0.01-$0.50 per query.

**Q: Are my documents sent to OpenAI?**
A: Only text chunks are sent for embedding and answering. Full documents stay local.

**Q: Can I use other LLM providers?**
A: Not in current version, but planned for future updates.

---

**Need help?** Check README.md for detailed documentation.
