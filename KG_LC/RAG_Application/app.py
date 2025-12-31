"""Streamlit RAG Application."""

import os
import sys
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.document_loader import DocumentLoader
from core.rag_pipeline import EnhancedRAG
from core.quality_assessor import QualityAssessor
from core.hallucination_detector import HallucinationDetector
from utils.fallback_handler import FallbackHandler
from utils.session_manager import SessionManager
from utils.logger import setup_logger

# Configure logging
logger = setup_logger("RAG_App", "logs/app.log")

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .quality-excellent { color: #00D084; font-weight: bold; }
    .quality-good { color: #0ABF5B; font-weight: bold; }
    .quality-fair { color: #FFA500; font-weight: bold; }
    .quality-poor { color: #FF6B6B; font-weight: bold; }
    .quality-very-poor { color: #C71D1D; font-weight: bold; }
    .hallucination-high { color: #C71D1D; font-weight: bold; }
    .hallucination-low { color: #00D084; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = None
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []


def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key."""
    return api_key and len(api_key) > 20


def setup_rag_system(api_key: str, model: str) -> bool:
    """Set up RAG system with given API key and model."""
    try:
        st.session_state.rag_system = EnhancedRAG(
            openai_api_key=api_key,
            model_name=model
        )
        return True
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {str(e)}")
        logger.error(f"RAG initialization error: {str(e)}")
        return False


def load_documents(uploaded_files: list, api_key: str) -> bool:
    """Load and index uploaded documents."""
    if not uploaded_files or not st.session_state.rag_system:
        return False

    try:
        loader = DocumentLoader()
        all_documents = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name

            try:
                # Load document
                file_type = Path(uploaded_file.name).suffix.lstrip('.').lower()
                documents = loader.load_file(tmp_path, file_type)
                all_documents.extend(documents)

                logger.info(f"Loaded {len(documents)} chunks from {uploaded_file.name}")

                # Add to session
                st.session_state.session_manager.add_document(
                    uploaded_file.name,
                    uploaded_file.name,
                    len(documents)
                )

            finally:
                os.unlink(tmp_path)

            progress_bar.progress((idx + 1) / len(uploaded_files))

        if not all_documents:
            st.error("No valid documents were loaded")
            return False

        # Build RAG index
        status_text.text("Building search index...")
        st.session_state.rag_system.build_index(all_documents)

        # Save session
        st.session_state.session_manager.save_session()

        status_text.text("✓ Documents loaded and indexed successfully!")
        progress_bar.empty()

        logger.info(f"Successfully loaded {len(all_documents)} chunks from {len(uploaded_files)} files")
        return True

    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")
        logger.error(f"Document loading error: {str(e)}")
        return False


def display_quality_assessment(quality_result: dict):
    """Display quality assessment results."""
    metrics = quality_result["metrics"]
    overall_score = quality_result["overall_score"]
    quality_level = quality_result["quality_level"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Quality Level",
            quality_level,
            f"{overall_score:.1%}"
        )

    with col2:
        st.metric(
            "Completeness",
            f"{metrics['completeness']:.1%}"
        )

    with col3:
        st.metric(
            "Specificity",
            f"{metrics['specificity']:.1%}"
        )

    with col4:
        st.metric(
            "Confidence",
            f"{metrics['confidence']:.1%}"
        )

    # Display recommendations if any
    if quality_result["recommendations"]:
        st.warning("⚠️ **Recommendations:**")
        for rec in quality_result["recommendations"]:
            st.write(f"• {rec}")

    if quality_result["needs_fallback"]:
        st.info("ℹ️ This answer may need additional context. Consider asking a follow-up question or rephrase your question.")


def display_hallucination_report(detections: dict):
    """Display hallucination detection report."""
    risk_level = "🔴 HIGH RISK" if detections["is_hallucination_likely"] else "🟢 LOW RISK"

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Hallucination Risk",
            risk_level,
            f"{detections['overall_hallucination_risk']:.1%}"
        )

    with col2:
        st.metric(
            "Confidence Score",
            f"{detections['confidence_score']:.1%}"
        )

    # Show detailed findings
    if detections["unsupported_claims"]:
        st.warning("**Unsupported Claims:**")
        for claim in detections["unsupported_claims"]:
            st.write(f"• {claim}")

    if detections["fabricated_facts"]:
        st.error("**Potentially Fabricated Facts:**")
        for fact in detections["fabricated_facts"]:
            st.write(f"• {fact}")


def display_source_documents(source_docs: list):
    """Display source documents used."""
    st.subheader("📄 Source Documents")

    for i, doc in enumerate(source_docs, 1):
        with st.expander(f"Chunk {i} - {doc.metadata.get('source', 'Unknown')}"):
            st.text(doc.page_content)
            st.caption(f"Source: {doc.metadata.get('source')}")


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")

        # Session Management
        st.subheader("Session Management")
        session_options = ["New Session"] + st.session_state.session_manager.list_sessions()
        selected_session = st.selectbox("Select Session:", session_options)

        if selected_session == "New Session":
            session_name = st.text_input("Session Name:", value="")
            if st.button("Create Session", key="create_session_btn"):
                if session_name:
                    st.session_state.current_session = st.session_state.session_manager.create_session(session_name)
                    st.success(f"Session '{session_name}' created!")
                    st.rerun()
        else:
            if st.button("Load Session"):
                if st.session_state.session_manager.load_session(selected_session):
                    st.session_state.current_session = selected_session
                    st.success(f"Session '{selected_session}' loaded!")
                    st.rerun()

        st.divider()

        # API Configuration
        st.subheader("API Configuration")

        api_key = st.text_input(
            "OpenAI API Key:",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password"
        )

        if not api_key:
            st.warning("⚠️ OpenAI API key is required")
        elif not validate_api_key(api_key):
            st.warning("⚠️ API key format seems invalid")

        st.divider()

        # Model Selection
        st.subheader("Model Selection")

        available_models = list(EnhancedRAG.AVAILABLE_MODELS.keys())
        selected_model = st.selectbox(
            "Select LLM Model:",
            available_models,
            help="Choose which language model to use for generating answers"
        )

        # Display model info
        model_info = EnhancedRAG.AVAILABLE_MODELS[selected_model]
        st.info(f"**{model_info['name']}**\n\n{model_info['description']}\n\nCost: {model_info['cost']}")

        st.divider()

        # Settings
        st.subheader("Settings")

        enable_hallucination_check = st.checkbox(
            "Enable Hallucination Detection",
            value=True,
            help="Check generated answers for potential hallucinations"
        )

        enable_quality_assessment = st.checkbox(
            "Enable Quality Assessment",
            value=True,
            help="Assess completeness, specificity, and confidence of answers"
        )

        enable_fallback = st.checkbox(
            "Enable Fallback Strategies",
            value=True,
            help="Use alternative retrieval methods if answer quality is low"
        )

        chunk_size = st.slider(
            "Chunk Size:",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Size of text chunks for document processing"
        )

        st.divider()

        # Session Info
        if st.session_state.current_session:
            st.subheader("Session Info")
            summary = st.session_state.session_manager.get_session_summary()
            st.write(f"**Session:** {summary['session_id']}")
            st.write(f"**Documents:** {summary['num_documents']}")
            st.write(f"**Conversations:** {summary['num_conversations']}")
            if summary['average_quality_score']:
                st.write(f"**Avg Quality:** {summary['average_quality_score']:.2f}")

    # Main content
    st.title("📚 RAG Document Assistant")
    st.markdown("Upload documents and ask questions about them using advanced RAG with quality guardrails.")

    # Initialize RAG system if API key is provided
    if api_key and validate_api_key(api_key):
        if st.session_state.rag_system is None or st.session_state.rag_system.model_name != selected_model:
            with st.spinner("Initializing RAG system..."):
                if setup_rag_system(api_key, selected_model):
                    st.session_state.documents_loaded = False
                    st.success("✓ RAG system initialized!")

    # Document Upload Section
    st.header("📤 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose documents (PDF, DOCX, TXT, Excel):",
        type=["pdf", "docx", "doc", "txt", "xlsx", "xls", "csv"],
        accept_multiple_files=True,
        help="Upload one or more documents to create your knowledge base"
    )

    if uploaded_files and st.session_state.rag_system:
        if st.button("📥 Load & Index Documents", key="load_docs"):
            if st.session_state.session_manager.current_session is None:
                st.error("Please create or select a session first")
            else:
                st.session_state.documents_loaded = load_documents(uploaded_files, api_key)
                if st.session_state.documents_loaded:
                    st.rerun()

    if st.session_state.documents_loaded:
        st.success("✓ Documents loaded and indexed successfully!")

    # Q&A Section
    if st.session_state.rag_system and st.session_state.documents_loaded:
        st.header("💬 Ask Questions")

        question = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Ask a question about the uploaded documents...",
            help="Be specific for better results"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            ask_button = st.button("🔍 Get Answer", key="ask_button", use_container_width=True)

        with col2:
            if st.button("🗑️ Clear History", key="clear_history", use_container_width=True):
                st.session_state.conversation_history = []
                st.rerun()

        with col3:
            if st.session_state.current_session:
                if st.button("💾 Export Session", key="export_session", use_container_width=True):
                    export_path = f"exports/{st.session_state.current_session}_report.md"
                    st.session_state.session_manager.export_session(
                        st.session_state.current_session,
                        export_path,
                        "md"
                    )
                    st.success(f"Session exported to {export_path}")

        # Process question
        if ask_button and question:
            with st.spinner("Processing your question..."):
                try:
                    # Get answer from RAG
                    result = st.session_state.rag_system.query(question)
                    answer = result["answer"]
                    source_docs = result["source_documents"]

                    # Quality Assessment
                    quality_result = None
                    if enable_quality_assessment:
                        quality_assessor = QualityAssessor(api_key, selected_model)
                        context = " ".join([doc.page_content for doc in source_docs])
                        quality_result = quality_assessor.assess_answer(question, answer, context)

                    # Hallucination Detection
                    hallucination_result = None
                    if enable_hallucination_check:
                        hallucination_detector = HallucinationDetector(api_key, selected_model)
                        hallucination_result = hallucination_detector.detect_hallucinations(
                            answer, source_docs, question
                        )

                    # Apply Fallback if needed
                    if enable_fallback and quality_result and quality_result["needs_fallback"]:
                        fallback_handler = FallbackHandler(st.session_state.rag_system)
                        fallback_result = fallback_handler.apply_fallback(
                            question, quality_result, source_docs
                        )

                        if fallback_result.get("new_documents"):
                            result = fallback_handler.combine_fallback_result(result, fallback_result)
                            st.info(f"ℹ️ Fallback applied: {fallback_result['improvement']}")

                    # Store in history
                    quality_score = quality_result["overall_score"] if quality_result else None
                    st.session_state.session_manager.add_conversation(
                        question, answer, selected_model, quality_score
                    )
                    st.session_state.session_manager.save_session()

                    # Display Answer
                    st.subheader("✨ Answer")
                    st.write(answer)

                    # Display Quality Assessment
                    if quality_result:
                        st.subheader("📊 Quality Assessment")
                        display_quality_assessment(quality_result)

                    # Display Hallucination Detection
                    if hallucination_result:
                        st.subheader("🛡️ Hallucination Detection")
                        display_hallucination_report(hallucination_result)

                    # Display Source Documents
                    display_source_documents(source_docs)

                except Exception as e:
                    st.error(f"Error processing question: {str(e)}")
                    logger.error(f"Question processing error: {str(e)}")

        # Conversation History
        if st.session_state.session_manager.current_session:
            st.subheader("📋 Conversation History")

            history = st.session_state.session_manager.get_conversation_history()

            if history:
                for i, conv in enumerate(history, 1):
                    with st.expander(f"Q{i}: {conv['question'][:50]}..."):
                        st.write(f"**Model:** {conv['model']}")
                        st.write(f"**Question:** {conv['question']}")
                        st.write(f"**Answer:** {conv['answer']}")
                        if conv.get('quality_score'):
                            st.write(f"**Quality Score:** {conv['quality_score']:.2f}")
            else:
                st.info("No conversations yet. Ask a question to get started!")

    elif not st.session_state.rag_system:
        st.warning("⚠️ Please provide a valid OpenAI API key to continue")
    elif not st.session_state.documents_loaded:
        st.info("ℹ️ Please upload and load documents to start asking questions")


if __name__ == "__main__":
    main()
