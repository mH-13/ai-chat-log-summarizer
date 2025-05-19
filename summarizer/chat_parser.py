#Core parsing logic
#Loads a .txt chat log and splits it into ordered (speaker, text) entries for further processing.

import re
from typing import List, Tuple

def parse_chat(path: str) -> List[Tuple[str, str]]:

    pattern = re.compile(r'^(User|AI):\s*(.+)$')
    #This regex captures lines starting with "User:" or "AI:";  ^ for start of line; $ for end of line and \s* allows for any whitespace after the colon. (.+) captures the rest of the line as text message. 
    turns: List[Tuple[str, str]] = []
    
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                speaker, text = m.groups()
                turns.append((speaker, text))
    return turns
