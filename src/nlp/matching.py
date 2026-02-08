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
