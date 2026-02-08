
def keyword_overlap_score(clause_keywords, segment_text):
    """
    Calculate keyword overlap score between a clause and a policy segment.
    Score = matched keywords / total clause keywords
    """

    if not clause_keywords:
        return 0.0

    segment_text = segment_text.lower()
    matched = 0

    for kw in clause_keywords:
        if kw.lower() in segment_text:
            matched += 1

    return matched / len(clause_keywords)


def find_best_segment_match(clause, policy_segments):
    """
    Find the policy segment that best matches a given clause.
    Returns the best matching segment and its score.
    """

    best_score = 0.0
    best_segment = None

    for segment in policy_segments:
        score = keyword_overlap_score(
            clause["normalized_keywords"],
            segment["text"]
        )

        if score > best_score:
            best_score = score
            best_segment = segment

    return {
        "best_score": best_score,
        "best_segment_id": best_segment["id"] if best_segment else None,
        "best_segment_text": best_segment["text"] if best_segment else None
    }

