## Statistical analysis 

from collections import Counter
from typing import List, Tuple, Dict

def message_stats(turns: List[Tuple[str, str]]) -> Dict[str, int]:
    """Given parsed turns, returns counts:
      - total_messages
      - user_messages
      - ai_messages"""
    counts = Counter(s for s, _ in turns)
    total = sum(counts.values())
    return {
        "total_messages": total,
        "user_messages": counts.get("User", 0),
        "ai_messages": counts.get("AI", 0),
    }
