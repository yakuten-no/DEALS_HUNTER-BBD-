"""
Deterministic deal assessment.

No AI here by design (D-003 in project-memory/DECISIONS.md): every signal
in a DealAssessment is computed from stored data using plain arithmetic and
comparisons, and every claim can be traced back to the observations/offers
that produced it. See assessment.py for the actual logic.
"""

from app.deal_engine.assessment import DealAssessment, DealSignals, assess_deal

__all__ = ["DealAssessment", "DealSignals", "assess_deal"]
