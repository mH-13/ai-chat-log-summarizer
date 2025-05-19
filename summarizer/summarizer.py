#Generates a human-readable summary string from the stats and keyword lists.
# This function is called in the main script after parsing the chat and extracting keywords. 


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
    
    #Demo rule-based “nature” (we can expand as needed)
    if "code" in top_keys:
        lines.append("- Nature: Questions about code.")
    elif "chatgpt" in top_keys:
        lines.append("- Nature: Questions about ChatGPT.")
    elif "gpt" in top_keys:
        lines.append("- Nature: Questions about GPT.")
    elif "ai" in top_keys:
        lines.append("- Nature: Questions about AI.")
    elif "llm" in top_keys:
        lines.append("- Nature: Questions about LLMs.")
    elif "openai" in top_keys:
        lines.append("- Nature: Questions about OpenAI.")
    elif "model" in top_keys:
        lines.append("- Nature: Questions about models.")
    elif "data" in top_keys:
        lines.append("- Nature: Questions about data.")
    elif "python" in top_keys or "python3" in top_keys:
        lines.append("- Nature: Questions about Python usage.")
    return "\n".join(lines)
