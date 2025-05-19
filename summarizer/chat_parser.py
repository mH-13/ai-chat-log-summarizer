## Core parsing logic

import re
from typing import List, Tuple

def parse_chat(path: str) -> List[Tuple[str, str]]:
    #Reads a chat.txt file and returns a list of (speaker, message).

    pattern = re.compile(r'^(User|AI):\s*(.+)$')
    turns: List[Tuple[str, str]] = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                speaker, text = m.groups()
                turns.append((speaker, text))
    return turns
