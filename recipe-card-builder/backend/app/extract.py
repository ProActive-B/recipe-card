import re
from typing import Dict, List

import spacy

nlp = spacy.load("en_core_web_sm")


def parse_transcript(text: str) -> Dict[str, str]:
    """Very naive rule-based extraction of recipe info."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = lines[0] if lines else "Recipe"
    ingredients: List[str] = []
    steps: List[str] = []
    current = None
    for line in lines[1:]:
        lower = line.lower()
        if "ingredient" in lower:
            current = "ing"
            continue
        if any(word in lower for word in ["step", "instruction"]):
            current = "step"
            continue
        if current == "ing":
            ingredients.append(line)
        elif current == "step":
            steps.append(line)
    servings_match = re.search(r"(serves|servings?):?\s*(\d+)", text, re.I)
    cook_match = re.search(r"(cook time|cooking time):?\s*([\w\s]+)", text, re.I)
    return {
        "title": title,
        "ingredients": str(ingredients),
        "steps": str(steps),
        "servings": servings_match.group(2) if servings_match else None,
        "cook_time": cook_match.group(2) if cook_match else None,
    }
