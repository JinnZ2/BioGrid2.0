from collections import defaultdict
from typing import Dict, List


class ContraGraph:
    """Tracks claim polarities and detects mutual exclusion violations."""

    def __init__(self):
        self.prop_polarities = defaultdict(set)

    def ingest(self, claims: List[Dict]):
        for c in claims:
            prop = c["text"].strip().lower()
            self.prop_polarities[prop].add(c["polarity"])

    def contradictions(self):
        return [p for p, s in self.prop_polarities.items()
                if "assert" in s and "deny" in s]
