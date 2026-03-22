"""Persistent claim polarity tracker for multi-turn conversations."""

from collections import defaultdict
from typing import Dict, List


class ContradictionTracker:
    """Accumulates claim polarities and detects conflicts across turns."""

    def __init__(self):
        self.polarities = defaultdict(set)

    def ingest(self, claims: List[Dict]):
        """Add claims to the tracker. Each claim needs 'text' and 'polarity'."""
        for c in claims:
            prop = c["text"].strip().lower()
            self.polarities[prop].add(c["polarity"])

    def conflicts(self) -> List[str]:
        """Return propositions that have been both asserted and denied."""
        return [p for p, s in self.polarities.items()
                if "assert" in s and "deny" in s]

    def conflict_count(self) -> int:
        return len(self.conflicts())

    def clear(self):
        self.polarities.clear()
