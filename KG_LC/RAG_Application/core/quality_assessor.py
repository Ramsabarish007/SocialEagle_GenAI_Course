"""Answer quality assessment module."""

import re
from typing import Dict, Any, Tuple
from langchain_openai import ChatOpenAI


class QualityAssessor:
    """Assess the quality of RAG answers based on completeness, specificity, and recency."""

    def __init__(self, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize quality assessor.

        Args:
            openai_api_key: OpenAI API key
            model_name: Model to use for assessment
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=openai_api_key,
            max_tokens=500
        )

    def assess_answer(self, question: str, answer: str, context: str) -> Dict[str, Any]:
        """
        Assess the quality of an answer.

        Args:
            question: Original question
            answer: Generated answer
            context: Context used to generate answer

        Returns:
            Dictionary with quality metrics and score
        """
        metrics = {
            "completeness": self._assess_completeness(question, answer),
            "specificity": self._assess_specificity(answer),
            "relevance": self._assess_relevance(question, answer),
            "confidence": self._assess_confidence(answer),
            "hallucination_risk": self._detect_hallucination_risk(answer, context)
        }

        # Calculate overall quality score (0-1)
        overall_score = (
            metrics["completeness"] * 0.3 +
            metrics["specificity"] * 0.25 +
            metrics["relevance"] * 0.25 +
            metrics["confidence"] * 0.2 -
            (metrics["hallucination_risk"] * 0.5)
        )
        overall_score = max(0, min(1, overall_score))  # Clamp to 0-1

        return {
            "metrics": metrics,
            "overall_score": overall_score,
            "quality_level": self._score_to_level(overall_score),
            "needs_fallback": overall_score < 0.6,
            "recommendations": self._get_recommendations(metrics)
        }

    def _assess_completeness(self, question: str, answer: str) -> float:
        """
        Assess answer completeness.

        Checks if the answer adequately addresses the question.
        """
        # Check answer length
        word_count = len(answer.split())
        if word_count < 30:
            return 0.3  # Too short, likely incomplete

        # Check for common incomplete indicators
        incomplete_indicators = [
            "i don't know",
            "i'm not sure",
            "insufficient information",
            "not provided",
            "unclear"
        ]

        answer_lower = answer.lower()
        has_incomplete_indicators = any(indicator in answer_lower for indicator in incomplete_indicators)

        if has_incomplete_indicators:
            return 0.4
        elif word_count > 100:
            return 0.9
        elif word_count > 60:
            return 0.8
        else:
            return 0.6

    def _assess_specificity(self, answer: str) -> float:
        """
        Assess answer specificity.

        Checks for specific details, numbers, and concrete examples.
        """
        specificity_score = 0.5

        # Check for numbers
        if re.search(r'\d+', answer):
            specificity_score += 0.15

        # Check for quotes or citations
        if '"' in answer or "'" in answer:
            specificity_score += 0.15

        # Check for technical terms (more than 4 capital letters in sequence)
        if re.search(r'[A-Z]{4,}', answer):
            specificity_score += 0.1

        # Check sentence structure variety
        sentences = re.split(r'[.!?]+', answer)
        if len(sentences) > 5:
            specificity_score += 0.15

        return min(1.0, specificity_score)

    def _assess_relevance(self, question: str, answer: str) -> float:
        """
        Assess answer relevance to the question.

        Checks if answer addresses the key aspects of the question.
        """
        question_words = set(word.lower() for word in question.split() if len(word) > 3)
        answer_words = set(word.lower() for word in answer.split() if len(word) > 3)

        if not question_words:
            return 0.5

        # Calculate word overlap
        overlap = len(question_words & answer_words) / len(question_words)

        return min(1.0, 0.3 + (overlap * 0.7))

    def _assess_confidence(self, answer: str) -> float:
        """
        Assess the confidence level expressed in the answer.

        Higher score for confident answers without excessive hedging.
        """
        hedging_words = [
            "maybe", "perhaps", "possibly", "might",
            "could be", "appears to be", "seems",
            "arguably", "probably"
        ]

        answer_lower = answer.lower()
        hedge_count = sum(1 for word in hedging_words if word in answer_lower)

        word_count = len(answer.split())
        hedge_ratio = hedge_count / max(1, word_count / 50)  # Normalize by answer length

        confidence = 1.0 - min(0.5, hedge_ratio * 0.1)
        return max(0.3, confidence)

    def _detect_hallucination_risk(self, answer: str, context: str) -> float:
        """
        Detect risk of hallucination in the answer.

        Returns score 0-1 where 1 means high hallucination risk.
        """
        # Check if answer contains content not in context
        answer_sentences = re.split(r'[.!?]+', answer)
        context_words = set(context.lower().split())

        hallucination_risk = 0.0

        for sentence in answer_sentences:
            if not sentence.strip():
                continue

            sentence_words = set(sentence.lower().split())
            # Calculate how many content words are not in context
            content_words = [w for w in sentence_words if len(w) > 3]

            if content_words:
                not_in_context = sum(
                    1 for word in content_words
                    if word not in context_words and
                    not any(word in cw for cw in context_words)  # Check partial matches
                )
                ratio = not_in_context / len(content_words)

                if ratio > 0.5:  # More than half of content words not in context
                    hallucination_risk += 0.1

        # Check for self-contradiction
        sentences = re.split(r'[.!?]+', answer)
        for i, sent1 in enumerate(sentences):
            for sent2 in sentences[i+1:]:
                if "not" in sent1.lower() and sent1.lower().replace("not", "") in sent2.lower():
                    hallucination_risk += 0.15

        return min(1.0, hallucination_risk)

    def _score_to_level(self, score: float) -> str:
        """Convert quality score to human-readable level."""
        if score >= 0.85:
            return "Excellent"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        elif score >= 0.4:
            return "Poor"
        else:
            return "Very Poor"

    def _get_recommendations(self, metrics: Dict[str, float]) -> list:
        """Get recommendations for improving answer quality."""
        recommendations = []

        if metrics["completeness"] < 0.6:
            recommendations.append("Answer appears incomplete - consider asking a more specific follow-up question")

        if metrics["specificity"] < 0.5:
            recommendations.append("Answer lacks specific details - request concrete examples or data")

        if metrics["confidence"] < 0.5:
            recommendations.append("Answer expresses low confidence - try rephrasing the question")

        if metrics["hallucination_risk"] > 0.5:
            recommendations.append("High risk of hallucination detected - verify with original documents")

        return recommendations

    def assess_batch(self, questions: list, answers: list, contexts: list) -> Dict[str, Any]:
        """
        Assess multiple Q&A pairs at once.

        Args:
            questions: List of questions
            answers: List of answers
            contexts: List of contexts

        Returns:
            Summary statistics
        """
        assessments = []
        for q, a, c in zip(questions, answers, contexts):
            assessments.append(self.assess_answer(q, a, c))

        overall_scores = [a["overall_score"] for a in assessments]

        return {
            "total_assessments": len(assessments),
            "average_score": sum(overall_scores) / len(overall_scores) if overall_scores else 0,
            "min_score": min(overall_scores) if overall_scores else 0,
            "max_score": max(overall_scores) if overall_scores else 1,
            "assessments": assessments
        }
