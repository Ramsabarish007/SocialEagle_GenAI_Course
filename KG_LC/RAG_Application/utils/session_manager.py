"""Session and state management."""

import json
import os
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class SessionManager:
    """Manage RAG session state and history."""

    def __init__(self, session_dir: str = "sessions"):
        """
        Initialize session manager.

        Args:
            session_dir: Directory to store session files
        """
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.current_session = None
        self.session_data = {
            "created_at": None,
            "updated_at": None,
            "documents_loaded": [],
            "conversations": [],
            "model_used": None
        }

    def create_session(self, session_name: str = None) -> str:
        """
        Create a new session.

        Args:
            session_name: Optional session name

        Returns:
            Session ID
        """
        if session_name is None:
            session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session_id = session_name
        self.current_session = session_id

        self.session_data = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "documents_loaded": [],
            "conversations": [],
            "model_used": None
        }

        return session_id

    def load_session(self, session_id: str) -> bool:
        """
        Load an existing session.

        Args:
            session_id: Session ID to load

        Returns:
            True if successful, False otherwise
        """
        session_file = self.session_dir / f"{session_id}.json"

        if not session_file.exists():
            return False

        try:
            with open(session_file, 'r') as f:
                self.session_data = json.load(f)
            self.current_session = session_id
            return True
        except Exception:
            return False

    def save_session(self) -> bool:
        """
        Save current session to disk.

        Returns:
            True if successful, False otherwise
        """
        if not self.current_session:
            return False

        try:
            self.session_data["updated_at"] = datetime.now().isoformat()
            session_file = self.session_dir / f"{self.current_session}.json"

            with open(session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2, default=str)

            return True
        except Exception:
            return False

    def add_document(self, doc_name: str, doc_path: str, num_chunks: int):
        """
        Add loaded document to session.

        Args:
            doc_name: Document name
            doc_path: Path to document
            num_chunks: Number of chunks created
        """
        doc_info = {
            "name": doc_name,
            "path": doc_path,
            "chunks": num_chunks,
            "loaded_at": datetime.now().isoformat()
        }
        self.session_data["documents_loaded"].append(doc_info)

    def add_conversation(self, question: str, answer: str, model: str, quality_score: float = None):
        """
        Add conversation to session history.

        Args:
            question: User question
            answer: RAG answer
            model: Model used
            quality_score: Quality assessment score
        """
        conversation = {
            "question": question,
            "answer": answer,
            "model": model,
            "quality_score": quality_score,
            "timestamp": datetime.now().isoformat()
        }
        self.session_data["conversations"].append(conversation)
        self.session_data["model_used"] = model

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.session_data.get("conversations", [])

    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary."""
        conversations = self.session_data.get("conversations", [])

        return {
            "session_id": self.current_session,
            "created_at": self.session_data.get("created_at"),
            "updated_at": self.session_data.get("updated_at"),
            "num_documents": len(self.session_data.get("documents_loaded", [])),
            "documents": self.session_data.get("documents_loaded", []),
            "num_conversations": len(conversations),
            "model_used": self.session_data.get("model_used"),
            "average_quality_score": self._calculate_avg_quality() if conversations else None
        }

    def _calculate_avg_quality(self) -> float:
        """Calculate average quality score from conversations."""
        conversations = self.session_data.get("conversations", [])
        scores = [c.get("quality_score") for c in conversations if c.get("quality_score") is not None]

        if scores:
            return sum(scores) / len(scores)
        return None

    def list_sessions(self) -> List[str]:
        """List all available sessions."""
        sessions = []
        for file in self.session_dir.glob("*.json"):
            sessions.append(file.stem)
        return sorted(sessions)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session ID to delete

        Returns:
            True if successful
        """
        try:
            session_file = self.session_dir / f"{session_id}.json"
            session_file.unlink()
            if self.current_session == session_id:
                self.current_session = None
            return True
        except Exception:
            return False

    def export_session(self, session_id: str, export_path: str, format: str = "json") -> bool:
        """
        Export session to file.

        Args:
            session_id: Session to export
            export_path: Path to export to
            format: Export format (json or md)

        Returns:
            True if successful
        """
        try:
            if self.current_session != session_id:
                if not self.load_session(session_id):
                    return False

            if format == "json":
                with open(export_path, 'w') as f:
                    json.dump(self.session_data, f, indent=2, default=str)

            elif format == "md":
                with open(export_path, 'w') as f:
                    f.write(f"# Session Report: {session_id}\n\n")
                    summary = self.get_session_summary()

                    f.write(f"**Created:** {summary['created_at']}\n")
                    f.write(f"**Updated:** {summary['updated_at']}\n")
                    f.write(f"**Model:** {summary['model_used']}\n")
                    f.write(f"**Quality Score:** {summary['average_quality_score']:.2f}\n\n")

                    f.write("## Documents Loaded\n")
                    for doc in summary['documents']:
                        f.write(f"- {doc['name']} ({doc['chunks']} chunks)\n")

                    f.write("\n## Conversations\n")
                    for i, conv in enumerate(self.session_data['conversations'], 1):
                        f.write(f"\n### Q{i}: {conv['question']}\n")
                        f.write(f"**A:** {conv['answer']}\n")
                        if conv.get('quality_score'):
                            f.write(f"*Quality: {conv['quality_score']:.2f}*\n")

            return True
        except Exception:
            return False
