"""Fallback handler for low-quality answers."""

from typing import Dict, Any, List
from langchain.docstore.document import Document


class FallbackHandler:
    """Handle fallback retrieval when primary answer quality is low."""

    def __init__(self, rag_system):
        """
        Initialize fallback handler.

        Args:
            rag_system: Reference to the RAG system
        """
        self.rag_system = rag_system

    def apply_fallback(
        self,
        question: str,
        quality_assessment: Dict[str, Any],
        source_documents: List[Document]
    ) -> Dict[str, Any]:
        """
        Apply fallback strategy when answer quality is low.

        Strategies:
        1. Re-retrieve with more context chunks
        2. Use different embedding similarity metrics
        3. Expand the query with related terms
        4. Use document structure to find better answers

        Args:
            question: Original question
            quality_assessment: Quality assessment results
            source_documents: Original source documents

        Returns:
            Dictionary with fallback attempt results
        """
        fallback_results = {
            "strategy": None,
            "new_answer": None,
            "new_documents": None,
            "improvement": None
        }

        # Determine fallback strategy based on quality issues
        metrics = quality_assessment.get("metrics", {})

        if metrics.get("completeness", 1) < 0.5:
            # Try retrieval with more context chunks
            fallback_results["strategy"] = "increase_context"
            fallback_results = self._apply_increase_context(question, fallback_results)

        elif metrics.get("hallucination_risk", 0) > 0.5:
            # Try re-retrieval with stricter matching
            fallback_results["strategy"] = "strict_matching"
            fallback_results = self._apply_strict_matching(question, fallback_results)

        elif metrics.get("specificity", 1) < 0.5:
            # Try query expansion
            fallback_results["strategy"] = "query_expansion"
            fallback_results = self._apply_query_expansion(question, fallback_results)

        else:
            # Try multiple retrievals and combine
            fallback_results["strategy"] = "multi_strategy"
            fallback_results = self._apply_multi_strategy(question, fallback_results)

        return fallback_results

    def _apply_increase_context(
        self,
        question: str,
        fallback_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Increase context by retrieving more chunks.

        Args:
            question: Question to answer
            fallback_results: Results dictionary to update

        Returns:
            Updated results with fallback attempt
        """
        try:
            # Retrieve more documents (increase k parameter)
            more_docs = self.rag_system.vectorstore.similarity_search(question, k=8)

            if more_docs:
                fallback_results["new_documents"] = more_docs
                fallback_results["improvement"] = "Retrieved 8 chunks instead of 4 for better context"
            else:
                fallback_results["improvement"] = "Failed to retrieve additional documents"

        except Exception as e:
            fallback_results["improvement"] = f"Error in fallback: {str(e)}"

        return fallback_results

    def _apply_strict_matching(
        self,
        question: str,
        fallback_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply strict matching to reduce hallucination risk.

        Args:
            question: Question to answer
            fallback_results: Results dictionary to update

        Returns:
            Updated results with fallback attempt
        """
        try:
            # Retrieve with strict threshold
            docs = self.rag_system.vectorstore.similarity_search_with_score(question, k=4)

            # Filter for high similarity only (score < 0.5)
            high_similarity_docs = [doc for doc, score in docs if score < 0.5]

            if high_similarity_docs:
                fallback_results["new_documents"] = high_similarity_docs
                fallback_results["improvement"] = f"Applied strict similarity threshold, kept {len(high_similarity_docs)} high-confidence chunks"
            else:
                fallback_results["improvement"] = "No documents met strict similarity threshold"

        except Exception as e:
            fallback_results["improvement"] = f"Error in fallback: {str(e)}"

        return fallback_results

    def _apply_query_expansion(
        self,
        question: str,
        fallback_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Expand query with related terms.

        Args:
            question: Question to answer
            fallback_results: Results dictionary to update

        Returns:
            Updated results with fallback attempt
        """
        try:
            # Expand question with common synonyms
            expanded_queries = self._generate_expanded_queries(question)

            all_docs = []
            doc_ids = set()

            for expanded_q in expanded_queries:
                docs = self.rag_system.vectorstore.similarity_search(expanded_q, k=3)
                for doc in docs:
                    doc_id = id(doc.page_content)
                    if doc_id not in doc_ids:
                        all_docs.append(doc)
                        doc_ids.add(doc_id)

            fallback_results["new_documents"] = all_docs
            fallback_results["improvement"] = f"Expanded query to {len(expanded_queries)} variants, found {len(all_docs)} documents"

        except Exception as e:
            fallback_results["improvement"] = f"Error in fallback: {str(e)}"

        return fallback_results

    def _apply_multi_strategy(
        self,
        question: str,
        fallback_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply multiple strategies and combine results.

        Args:
            question: Question to answer
            fallback_results: Results dictionary to update

        Returns:
            Updated results with fallback attempt
        """
        try:
            # Combine results from different retrieval strategies
            standard_docs = self.rag_system.vectorstore.similarity_search(question, k=4)

            expanded = self._generate_expanded_queries(question)
            expanded_docs = []
            for q in expanded[:2]:
                expanded_docs.extend(self.rag_system.vectorstore.similarity_search(q, k=2))

            # Combine and deduplicate
            all_docs = standard_docs + expanded_docs
            unique_docs = []
            seen = set()

            for doc in all_docs:
                doc_id = hash(doc.page_content)
                if doc_id not in seen:
                    unique_docs.append(doc)
                    seen.add(doc_id)

            fallback_results["new_documents"] = unique_docs
            fallback_results["improvement"] = f"Applied multi-strategy retrieval, combined {len(unique_docs)} unique documents"

        except Exception as e:
            fallback_results["improvement"] = f"Error in fallback: {str(e)}"

        return fallback_results

    def _generate_expanded_queries(self, question: str) -> List[str]:
        """
        Generate expanded queries with related terms.

        Args:
            question: Original question

        Returns:
            List of expanded queries
        """
        expanded = [question]

        # Common expansions
        replacements = {
            "how": ["explain", "describe", "what is"],
            "why": ["explain reasons for", "what causes"],
            "what": ["define", "explain", "describe"],
            "which": ["what", "list"],
            "when": ["time of", "date of"],
        }

        for orig, alts in replacements.items():
            if question.lower().startswith(orig):
                for alt in alts:
                    expanded_q = question.lower().replace(orig, alt, 1)
                    expanded.append(expanded_q)
                break

        return expanded[:4]  # Return up to 4 queries

    def combine_fallback_result(
        self,
        original_result: Dict[str, Any],
        fallback_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Combine original and fallback results.

        Args:
            original_result: Original query result
            fallback_result: Fallback retrieval result

        Returns:
            Combined result dictionary
        """
        combined = original_result.copy()

        if fallback_result.get("new_documents"):
            # Add fallback flag and information
            combined["fallback_applied"] = True
            combined["fallback_strategy"] = fallback_result["strategy"]
            combined["fallback_improvement"] = fallback_result["improvement"]
            combined["additional_context_documents"] = fallback_result["new_documents"]
        else:
            combined["fallback_applied"] = False
            combined["fallback_strategy"] = fallback_result["strategy"]
            combined["fallback_improvement"] = fallback_result["improvement"]

        return combined
