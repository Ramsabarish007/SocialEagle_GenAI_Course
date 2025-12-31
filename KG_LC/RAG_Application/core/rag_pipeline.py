"""Enhanced RAG Pipeline with multi-model support and quality assessment."""

import os
import time
from typing import List, Dict, Any, Tuple
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import json


class EnhancedRAG:
    """Enhanced RAG system with multi-model support and quality assessment."""

    # Available models
    AVAILABLE_MODELS = {
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "description": "Most powerful, best for complex queries",
            "cost": "high"
        },
        "gpt-4": {
            "name": "GPT-4",
            "description": "Powerful, good for complex reasoning",
            "cost": "high"
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "description": "Fast and cost-effective",
            "cost": "low"
        },
    }

    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "gpt-3.5-turbo",
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize Enhanced RAG system.

        Args:
            openai_api_key: OpenAI API key
            model_name: LLM model to use
            embedding_model: Embedding model to use
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=openai_api_key
        )

        # Initialize LLM
        self.llm = self._initialize_llm(model_name)

        self.vectorstore = None
        self.qa_chain = None
        self.documents = []

    def _initialize_llm(self, model_name: str):
        """Initialize LLM with specified model."""
        return ChatOpenAI(
            model=model_name,
            temperature=0.3,  # Slightly higher than 0 to reduce repetition but maintain consistency
            api_key=self.openai_api_key,
            max_tokens=2048
        )

    def switch_model(self, model_name: str) -> None:
        """
        Switch to a different LLM model.

        Args:
            model_name: Name of the model to switch to
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not available. Available: {list(self.AVAILABLE_MODELS.keys())}")

        self.model_name = model_name
        self.llm = self._initialize_llm(model_name)

        # Recreate QA chain with new model
        if self.vectorstore:
            self._create_qa_chain()

    def build_index(self, documents: List[Document]) -> None:
        """
        Build FAISS vector index from documents.

        Args:
            documents: List of LangChain Documents
        """
        if not documents:
            raise ValueError("No documents provided")

        print(f"Building FAISS index with {len(documents)} chunks...")
        start_time = time.time()

        self.documents = documents
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

        build_time = time.time() - start_time
        print(f"FAISS index built in {build_time:.2f} seconds")

        # Create QA chain
        self._create_qa_chain()

    def _create_qa_chain(self) -> None:
        """Create the QA chain with custom prompt."""
        prompt_template = """You are a knowledgeable and helpful AI assistant. Your task is to answer questions accurately and completely based on the provided context.

IMPORTANT INSTRUCTIONS:
1. Only use information from the provided context to answer the question
2. If the answer is not found in the context, clearly state: "I don't have enough information in the provided documents to answer this question."
3. Be specific and cite relevant parts of the context
4. Provide complete answers with all necessary details
5. If uncertain, express your uncertainty clearly
6. Do not invent or assume information not in the context

Context:
{context}

Question: {question}

Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def query(self, question: str, use_fallback: bool = False) -> Dict[str, Any]:
        """
        Query the RAG system.

        Args:
            question: User's question
            use_fallback: Whether to use fallback retrieval if answer quality is low

        Returns:
            Dictionary with answer, source documents, metrics, and quality assessment
        """
        if not self.qa_chain:
            raise ValueError("Index not built. Call build_index() first.")

        print(f"\nQuerying RAG with model: {self.model_name}")
        start_time = time.time()

        # Execute query
        result = self.qa_chain.invoke({"query": question})

        query_time = time.time() - start_time

        # Extract results
        answer = result['result']
        source_docs = result['source_documents']

        # Calculate metrics
        num_tokens = len(answer.split())
        num_chunks = len(source_docs)

        result_dict = {
            "answer": answer,
            "source_documents": source_docs,
            "query_time": query_time,
            "model": self.model_name,
            "metrics": {
                "query_time": query_time,
                "num_source_chunks": num_chunks,
                "answer_tokens": num_tokens,
                "retrieval_method": "vector_similarity"
            }
        }

        return result_dict

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search without generation.

        Args:
            query: Search query
            k: Number of results

        Returns:
            List of similar documents
        """
        if not self.vectorstore:
            raise ValueError("Index not built. Call build_index() first.")

        return self.vectorstore.similarity_search(query, k=k)

    def save_index(self, path: str) -> None:
        """Save FAISS index to disk."""
        if self.vectorstore:
            self.vectorstore.save_local(path)
            print(f"Index saved to {path}")

    def load_index(self, path: str) -> None:
        """Load FAISS index from disk."""
        self.vectorstore = FAISS.load_local(
            path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        self._create_qa_chain()
        print(f"Index loaded from {path}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current RAG system."""
        return {
            "total_documents": len(self.documents),
            "total_characters": sum(len(doc.page_content) for doc in self.documents) if self.documents else 0,
            "current_model": self.model_name,
            "embedding_model": self.embedding_model,
            "available_models": list(self.AVAILABLE_MODELS.keys()),
            "has_index": self.vectorstore is not None
        }
