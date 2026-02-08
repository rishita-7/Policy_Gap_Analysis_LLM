from src.nlp.preprocessing import normalize_text


def preprocess_clauses(clauses):
    """
    Normalize benchmark clause requirement text and keywords
    for later comparison with policy segments.
    """
    processed_clauses = []

    for clause in clauses:
        normalized_requirement = normalize_text(
            clause.get("requirement_text", "")
        )

        normalized_keywords = [
            normalize_text(keyword)
            for keyword in clause.get("keywords", [])
        ]

        processed_clauses.append({
            **clause,
            "normalized_requirement": normalized_requirement,
            "normalized_keywords": normalized_keywords
        })

    return processed_clauses
