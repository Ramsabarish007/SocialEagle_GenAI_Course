#!/usr/bin/env python3
"""
Example usage of RAG Application components without Streamlit.
Useful for testing and integration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from core.document_loader import DocumentLoader
from core.rag_pipeline import EnhancedRAG
from core.quality_assessor import QualityAssessor
from core.hallucination_detector import HallucinationDetector
from utils.fallback_handler import FallbackHandler
from utils.session_manager import SessionManager


def example_basic_rag():
    """Example: Basic RAG without quality checks."""
    print("=" * 80)
    print("Example 1: Basic RAG Usage")
    print("=" * 80)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        return

    # Initialize RAG
    rag = EnhancedRAG(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo"
    )

    # Load documents
    loader = DocumentLoader()
    documents = loader.load_file("sample.txt", "txt")
    rag.build_index(documents)

    # Query
    result = rag.query("What is the main topic?")
    print(f"\nQuestion: What is the main topic?")
    print(f"Answer: {result['answer']}")
    print(f"Query Time: {result['query_time']:.2f}s")


def example_with_quality():
    """Example: RAG with quality assessment."""
    print("\n" + "=" * 80)
    print("Example 2: RAG with Quality Assessment")
    print("=" * 80)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        return

    # Initialize components
    rag = EnhancedRAG(openai_api_key=api_key)
    assessor = QualityAssessor(openai_api_key=api_key)
    loader = DocumentLoader()

    # Load and index
    documents = loader.load_file("sample.txt", "txt")
    rag.build_index(documents)

    # Query with assessment
    result = rag.query("What features are described?")
    source_text = " ".join([doc.page_content for doc in result['source_documents']])
    quality = assessor.assess_answer(
        "What features are described?",
        result['answer'],
        source_text
    )

    print(f"\nAnswer: {result['answer']}")
    print(f"\nQuality Assessment:")
    print(f"  Overall Score: {quality['overall_score']:.2f}")
    print(f"  Level: {quality['quality_level']}")
    print(f"  Completeness: {quality['metrics']['completeness']:.2f}")
    print(f"  Specificity: {quality['metrics']['specificity']:.2f}")


def example_with_hallucination_detection():
    """Example: RAG with hallucination detection."""
    print("\n" + "=" * 80)
    print("Example 3: RAG with Hallucination Detection")
    print("=" * 80)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        return

    # Initialize components
    rag = EnhancedRAG(openai_api_key=api_key)
    detector = HallucinationDetector(openai_api_key=api_key)
    loader = DocumentLoader()

    # Load and index
    documents = loader.load_file("sample.txt", "txt")
    rag.build_index(documents)

    # Query and detect
    result = rag.query("What are specific details mentioned?")
    detections = detector.detect_hallucinations(
        result['answer'],
        result['source_documents']
    )

    print(f"\nAnswer: {result['answer']}")
    print(f"\nHallucination Detection:")
    print(f"  Risk Level: {detections['overall_hallucination_risk']:.1%}")
    print(f"  Status: {'HIGH RISK' if detections['is_hallucination_likely'] else 'LOW RISK'}")
    print(f"  Unsupported Claims: {len(detections['unsupported_claims'])}")
    print(f"  Fabricated Facts: {len(detections['fabricated_facts'])}")

    if detections['unsupported_claims']:
        print(f"\n  Unsupported Claims:")
        for claim in detections['unsupported_claims'][:3]:
            print(f"    - {claim}")


def example_with_session():
    """Example: Session management."""
    print("\n" + "=" * 80)
    print("Example 4: Session Management")
    print("=" * 80)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        return

    # Create session
    manager = SessionManager()
    session_id = manager.create_session("demo_session")
    print(f"Created session: {session_id}")

    # Add document info
    manager.add_document("sample.txt", "sample.txt", 50)

    # Add conversations
    manager.add_conversation(
        "What is the main topic?",
        "The main topic is...",
        "gpt-3.5-turbo",
        0.85
    )

    # Save
    manager.save_session()

    # Get summary
    summary = manager.get_session_summary()
    print(f"\nSession Summary:")
    print(f"  Documents: {summary['num_documents']}")
    print(f"  Conversations: {summary['num_conversations']}")
    print(f"  Average Quality: {summary['average_quality_score']:.2f}")

    # Export
    manager.export_session(session_id, "exports/demo_report.md", "md")
    print(f"  Exported to: exports/demo_report.md")


def example_model_switching():
    """Example: Switching between models."""
    print("\n" + "=" * 80)
    print("Example 5: Model Switching")
    print("=" * 80)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        return

    # Initialize RAG
    rag = EnhancedRAG(openai_api_key=api_key, model_name="gpt-3.5-turbo")
    loader = DocumentLoader()

    # Load documents
    documents = loader.load_file("sample.txt", "txt")
    rag.build_index(documents)

    question = "What is the summary?"

    # Query with GPT-3.5-turbo
    print(f"\nModel 1: gpt-3.5-turbo")
    result1 = rag.query(question)
    print(f"Answer: {result1['answer'][:100]}...")

    # Switch to GPT-4
    print(f"\nModel 2: gpt-4")
    rag.switch_model("gpt-4")
    result2 = rag.query(question)
    print(f"Answer: {result2['answer'][:100]}...")

    print("\n✓ Successfully switched between models without reindexing")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("RAG Application Examples")
    print("=" * 80)
    print("\nNote: Some examples require sample.txt in the current directory")
    print("Run the Streamlit app for the full interactive experience\n")

    try:
        example_basic_rag()
        example_with_quality()
        example_with_hallucination_detection()
        example_with_session()
        example_model_switching()

        print("\n" + "=" * 80)
        print("All examples completed!")
        print("=" * 80)

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTip: Make sure .env file is configured and sample.txt exists")
