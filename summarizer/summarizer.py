from typing import List, Tuple, Dict, Union

def generate_summary(
    stats: Dict[str, int],
    keywords: List[Tuple[str, Union[int, float]]]
) -> str:
    """Returns a multi-line summary of the chat:
      - Total messages
      - Breakdown User vs AI
      - Top keywords
      - Simple nature line if relevant"""
    top_keys = [kw for kw, _ in keywords]
    lines = [
        "=== Conversation Summary ===",
        f"- Total messages: {stats['total_messages']} "
        f"({stats['user_messages']} User, {stats['ai_messages']} AI)",
        f"- Top keywords: {', '.join(top_keys)}",
    ]
    # Example rule-based “nature” (you can expand this)
    if "python" in top_keys:
        lines.append("- Nature: Questions about Python usage.")
    return "\n".join(lines)
