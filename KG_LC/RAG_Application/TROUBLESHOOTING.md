# Troubleshooting Guide

## Installation Issues

### Problem: "Python is not installed or not in PATH"
**Solution:**
1. Install Python 3.9+ from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

### Problem: "No module named 'venv'"
**Solution:**
```bash
# Windows
python -m pip install virtualenv
python -m virtualenv venv

# macOS/Linux
python3 -m pip install virtualenv
python3 -m virtualenv venv
```

### Problem: "pip install fails with permission denied"
**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Problem: "Failed to install dependencies"
**Solution:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Try individual packages
pip install langchain
pip install langchain-openai
# ... etc
```

## Configuration Issues

### Problem: "OPENAI_API_KEY is required"
**Solution:**
1. Check `.env` file exists
2. Add line: `OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>`
3. Get key from https://platform.openai.com/api-keys
4. Restart Streamlit app

### Problem: "Invalid API key format"
**Solution:**
- Ensure key length > 20 characters
- No extra spaces or quotes
- Check it's not a test key

### Problem: "Authentication failed - invalid credentials"
**Solution:**
1. Verify API key is correct (copy/paste carefully)
2. Check key hasn't been revoked
3. Verify account has API credits
4. Try generating new key from OpenAI dashboard

### Problem: "Rate limit exceeded"
**Solution:**
- Wait a few minutes before retrying
- Reduce CHUNK_SIZE in .env
- Use GPT-3.5-turbo instead of GPT-4
- Implement caching (future feature)

## Runtime Issues

### Problem: Streamlit doesn't start
**Solution:**
```bash
# Check Streamlit installed
pip show streamlit

# Reinstall if needed
pip install --upgrade streamlit

# Try explicit port
streamlit run app.py --server.port 8501

# Check port isn't in use
# Windows: netstat -ano | findstr 8501
# macOS/Linux: lsof -i :8501
```

### Problem: "No such file or directory: .env"
**Solution:**
```bash
# Create from template
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows

# Edit and add API key
```

### Problem: "FAISS error" or "Segmentation fault"
**Solution:**
```bash
# Try CPU version
pip uninstall faiss-gpu
pip install faiss-cpu

# Or try GPU version if available
pip uninstall faiss-cpu
pip install faiss-gpu
```

### Problem: "Out of memory" error
**Solution:**
1. Reduce CHUNK_SIZE in .env (try 500 or 750)
2. Upload fewer documents at once
3. Increase available RAM
4. Use GPT-3.5-turbo (uses less memory)
5. Disable hallucination checks temporarily

## Document Loading Issues

### Problem: "PDF file not recognized"
**Solution:**
```bash
# Update PyPDF2
pip install --upgrade PyPDF2

# Check PDF is valid
# Try with a different PDF

# Use Acrobat to verify/repair PDF
```

### Problem: "DOCX file loading fails"
**Solution:**
```bash
# Install/update python-docx
pip install --upgrade python-docx

# Verify DOCX file isn't corrupted
# Try opening in Word and resaving
```

### Problem: "Excel file encoding error"
**Solution:**
```bash
# Install openpyxl
pip install --upgrade openpyxl pandas

# Ensure Excel file is .xlsx not .xls
# Try saving as CSV and loading that instead
```

### Problem: "Document has 0 chunks"
**Solution:**
1. Check file isn't empty
2. Reduce CHUNK_SIZE in .env
3. Try with a different document
4. Check file format is correct

## Query/Response Issues

### Problem: "Very slow query responses"
**Solution:**
1. Use GPT-3.5-turbo instead of GPT-4
2. Reduce CHUNK_SIZE (from 1000 to 750)
3. Reduce RETRIEVAL_K (from 4 to 3)
4. Disable hallucination checks temporarily
5. Check internet connection

### Problem: "Vague or incomplete answers"
**Solution:**
1. Rephrase question to be more specific
2. Switch to GPT-4 for better reasoning
3. Enable fallback strategies
4. Increase chunk context
5. Upload more relevant documents

### Problem: "Inconsistent answers on same question"
**Solution:**
1. Increase temperature slightly (already at 0.3)
2. Use GPT-4 for more consistent output
3. Rephrase question consistently
4. Check if documents have contradictions

### Problem: "High hallucination risk detected"
**Solution:**
1. Rephrase to more specific question
2. Switch to stricter model (GPT-4)
3. Disable fallback and try again
4. Add more source documents
5. Ask about specific dates/names less

### Problem: "Quality score always low"
**Solution:**
1. Upload more relevant documents
2. Check question isn't too vague
3. Use GPT-4 for better answers
4. Reduce quality threshold in .env
5. Enable fallback strategies

## Display/Interface Issues

### Problem: "Streamlit not showing results"
**Solution:**
1. Check browser console for errors (F12)
2. Clear browser cache
3. Try different browser
4. Refresh page
5. Check all required fields are filled

### Problem: "Session not saving"
**Solution:**
```bash
# Check permissions on sessions directory
chmod 755 sessions/  # macOS/Linux

# Create sessions directory if missing
mkdir -p sessions

# Check disk space
df -h  # macOS/Linux
```

### Problem: "Quality metrics not showing"
**Solution:**
1. Ensure CHECK_HALLUCINATION=true in .env
2. Wait for quality assessment (takes 0.5-1s)
3. Reload page if stuck
4. Try different document/question

## Performance Issues

### Problem: "Initial document loading slow"
**Solution:**
1. Normal for first load (30s for 10MB)
2. Index is cached, subsequent loads faster
3. Process large documents separately
4. Reduce chunk overlap if too slow

### Problem: "Memory usage high"
**Solution:**
1. Close other applications
2. Reduce chunk size
3. Reduce index size (fewer documents)
4. Use smaller documents
5. Increase swap space

### Problem: "Disk space running out"
**Solution:**
1. Clear old sessions: `rm -r sessions/*`
2. Clear old indexes: `rm -r indexes/*`
3. Clear logs: `rm -r logs/*`
4. Archive large exports

## Logging & Debugging

### Enable Debug Logging
```bash
# Windows
set LOG_LEVEL=DEBUG
streamlit run app.py

# macOS/Linux
LOG_LEVEL=DEBUG streamlit run app.py
```

### Check Logs
```bash
# View recent logs
tail -f logs/app.log  # macOS/Linux
type logs\app.log  # Windows

# Search logs
grep "error" logs/app.log  # macOS/Linux
findstr "error" logs\app.log  # Windows
```

### Test Components Individually
```bash
# Test document loading
python -c "from core.document_loader import DocumentLoader; \
loader = DocumentLoader(); \
docs = loader.load_file('test.txt', 'txt'); \
print(f'Loaded {len(docs)} chunks')"

# Test RAG
python examples.py
```

## Getting Help

### Check Logs First
1. Look in `logs/app.log`
2. Copy relevant error messages
3. Search logs for warnings

### Test in Isolation
```python
# Create test.py
from core.rag_pipeline import EnhancedRAG
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

rag = EnhancedRAG(openai_api_key=api_key)
print("RAG initialized successfully!")
```

### Common Solutions
1. **Restart everything**
   - Close Streamlit
   - Deactivate/reactivate venv
   - Rerun app
   
2. **Clear cache**
   - Delete `indexes/` directory
   - Streamlit will rebuild

3. **Update packages**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Verify setup**
   ```bash
   python -c "import langchain; import streamlit; print('OK')"
   ```

## Reporting Issues

When reporting problems, include:
1. Error message (exact text)
2. Full stack trace from logs
3. What you were trying to do
4. Your configuration (without API key)
5. Python version: `python --version`
6. OS: Windows/macOS/Linux

---

**Still having issues?**
1. Re-read the error message carefully
2. Check README.md for your scenario
3. Try the QUICKSTART.md from scratch
4. Review ARCHITECTURE.md for system design
5. Check examples.py for usage patterns
