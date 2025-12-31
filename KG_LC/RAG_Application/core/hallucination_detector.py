"""Hallucination detection and prevention module."""

import re
from typing import Dict, Any, List, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class HallucinationDetector:
    """Detect and prevent hallucinations in RAG responses."""

    def __init__(self, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize hallucination detector.

        Args:
            openai_api_key: OpenAI API key
            model_name: Model to use for detection
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=openai_api_key,
            max_tokens=500
        )

    def detect_hallucinations(
        self,
        answer: str,
        source_documents: List,
        question: str = None
    ) -> Dict[str, Any]:
        """
        Detect potential hallucinations in an answer.

        Args:
            answer: The generated answer
            source_documents: List of source documents used
            question: Original question (optional)

        Returns:
            Dictionary with hallucination detection results
        """
        combined_context = self._combine_documents(source_documents)

        detections = {
            "unsupported_claims": self._find_unsupported_claims(answer, combined_context),
            "contradictions": self._find_contradictions(answer, combined_context),
            "fabricated_facts": self._detect_fabricated_facts(answer, combined_context),
            "exaggerations": self._detect_exaggerations(answer, combined_context),
            "citation_issues": self._check_citation_coverage(answer, source_documents),
            "confidence_score": self._calculate_confidence(answer, combined_context)
        }

        # Overall hallucination risk
        total_issues = sum(len(v) for k, v in detections.items() if k != "confidence_score" and isinstance(v, list))
        hallucination_risk = min(1.0, total_issues * 0.15)

        detections["overall_hallucination_risk"] = hallucination_risk
        detections["is_hallucination_likely"] = hallucination_risk > 0.5

        return detections

    def _combine_documents(self, source_documents: List) -> str:
        """Combine all source documents into a single context string."""
        if not source_documents:
            return ""

        context_parts = []
        for doc in source_documents:
            if hasattr(doc, 'page_content'):
                context_parts.append(doc.page_content)
            elif isinstance(doc, dict) and 'page_content' in doc:
                context_parts.append(doc['page_content'])

        return "\n\n---\n\n".join(context_parts)

    def _find_unsupported_claims(self, answer: str, context: str) -> List[str]:
        """
        Find claims in the answer that are not supported by context.

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            List of unsupported claims
        """
        unsupported = []
        context_lower = context.lower()

        # Split answer into sentences
        sentences = re.split(r'[.!?]+', answer)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 10:
                continue

            # Check if key phrases from sentence appear in context
            key_phrases = self._extract_key_phrases(sentence)

            # If no key phrases match context, it's potentially unsupported
            phrase_found = False
            for phrase in key_phrases:
                if phrase.lower() in context_lower:
                    phrase_found = True
                    break

            if key_phrases and not phrase_found:
                unsupported.append(sentence)

        return unsupported[:5]  # Return top 5 to avoid clutter

    def _find_contradictions(self, answer: str, context: str) -> List[Tuple[str, str]]:
        """
        Find contradictions between answer and context.

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            List of (contradiction_in_answer, source_in_context) tuples
        """
        contradictions = []

        # Look for common contradiction patterns
        contradiction_patterns = [
            (r"(\w+) is not (\w+)", r"\1 is \2"),  # "X is not Y" vs "X is Y"
            (r"(\w+) doesn't (\w+)", r"\1 \2"),    # "X doesn't Y" vs "X Y"
            (r"(\w+) never (\w+)", r"\1 \2"),      # "X never Y" vs "X Y"
        ]

        answer_lower = answer.lower()
        context_lower = context.lower()

        for neg_pattern, pos_pattern in contradiction_patterns:
            neg_matches = re.findall(neg_pattern, answer_lower)
            for match in neg_matches:
                if isinstance(match, tuple):
                    search_str = f"{match[0]} {match[1]}".strip()
                else:
                    search_str = str(match)

                if search_str in context_lower:
                    contradictions.append((
                        f"Answer says 'not {search_str}'",
                        f"Context mentions '{search_str}'"
                    ))

        return contradictions[:5]

    def _detect_fabricated_facts(self, answer: str, context: str) -> List[str]:
        """
        Detect potentially fabricated facts (specific claims with no support).

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            List of potentially fabricated claims
        """
        fabricated = []

        # Look for specific facts (numbers, dates, proper nouns) not in context
        specific_facts = re.findall(r'\b(?:\d{4}|\d{1,2}[/-]\d{1,2}|\b[A-Z][a-z]+\s+[A-Z][a-z]+\b)', answer)

        for fact in specific_facts:
            if fact not in context:
                fabricated.append(f"Specific fact '{fact}' not found in source context")

        return fabricated[:5]

    def _detect_exaggerations(self, answer: str, context: str) -> List[str]:
        """
        Detect potential exaggerations or overstated claims.

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            List of potentially exaggerated claims
        """
        exaggerations = []

        # Superlative indicators
        superlatives = [
            'always', 'never', 'all', 'none', 'completely',
            'absolutely', 'totally', 'entirely', 'definitely'
        ]

        for superlative in superlatives:
            if superlative in answer.lower():
                # Check if corresponding claim is in context
                # If a superlative claim isn't strongly supported, flag it
                idx = answer.lower().find(superlative)
                if idx != -1:
                    # Get surrounding context
                    start = max(0, idx - 50)
                    end = min(len(answer), idx + 100)
                    claim = answer[start:end].strip()

                    # If the exact claim isn't in source, it might be exaggerated
                    if claim not in context:
                        exaggerations.append(f"Potential exaggeration: '{claim}'")

        return exaggerations[:3]

    def _check_citation_coverage(self, answer: str, source_documents: List) -> List[str]:
        """
        Check if claims in answer are backed by proper citations.

        Args:
            answer: Generated answer
            source_documents: Source documents

        Returns:
            List of citation issues
        """
        issues = []

        # Check if answer mentions sources/documents
        has_citations = bool(re.search(r'according to|source|document|based on|from the', answer.lower()))

        if not has_citations and len(answer) > 200:
            issues.append("Long answer without explicit source citations")

        return issues

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text."""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}

        words = text.split()
        key_phrases = []

        for i, word in enumerate(words):
            if word.lower() not in stop_words and len(word) > 3:
                # Try to get 2-3 word phrases
                phrase = ' '.join(words[i:min(i+3, len(words))])
                if phrase not in key_phrases:
                    key_phrases.append(phrase)

        return key_phrases[:3]  # Return top 3

    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Calculate confidence score (0-1) based on hallucination indicators.

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            Confidence score (0 = high hallucination risk, 1 = low risk)
        """
        confidence = 1.0

        # Reduce confidence if answer is very different from context
        answer_words = set(w.lower() for w in answer.split() if len(w) > 3)
        context_words = set(w.lower() for w in context.split() if len(w) > 3)

        if answer_words:
            overlap = len(answer_words & context_words) / len(answer_words)
            confidence -= (1 - overlap) * 0.3

        # Reduce confidence for hedging language (indicates uncertainty)
        hedges = ['maybe', 'perhaps', 'seems', 'appears', 'might', 'could']
        hedge_count = sum(1 for h in hedges if h in answer.lower())
        confidence -= min(0.2, hedge_count * 0.05)

        return max(0.0, confidence)

    def generate_hallucination_report(self, detections: Dict[str, Any]) -> str:
        """
        Generate a human-readable report of hallucination detections.

        Args:
            detections: Detection results from detect_hallucinations

        Returns:
            Formatted report string
        """
        report = []
        report.append("=== Hallucination Detection Report ===\n")

        report.append(f"Overall Hallucination Risk: {detections['overall_hallucination_risk']:.1%}")
        report.append(f"Status: {'⚠️ HIGH RISK' if detections['is_hallucination_likely'] else '✓ LOW RISK'}\n")

        if detections['unsupported_claims']:
            report.append("Unsupported Claims Found:")
            for claim in detections['unsupported_claims']:
                report.append(f"  - {claim}")
            report.append("")

        if detections['contradictions']:
            report.append("Potential Contradictions:")
            for answer_part, context_part in detections['contradictions']:
                report.append(f"  - {answer_part} | {context_part}")
            report.append("")

        if detections['fabricated_facts']:
            report.append("Potentially Fabricated Facts:")
            for fact in detections['fabricated_facts']:
                report.append(f"  - {fact}")
            report.append("")

        if detections['exaggerations']:
            report.append("Potential Exaggerations:")
            for exag in detections['exaggerations']:
                report.append(f"  - {exag}")
            report.append("")

        if detections['citation_issues']:
            report.append("Citation Issues:")
            for issue in detections['citation_issues']:
                report.append(f"  - {issue}")
            report.append("")

        report.append(f"Confidence Score: {detections['confidence_score']:.1%}")

        return "\n".join(report)
