from nlp.matching import find_best_segment_match, classify_coverage


def generate_gap_report(clauses, policy_segments):
    """
    Generate structured gap analysis report.
    """

    report = []

    for clause in clauses:
        match = find_best_segment_match(clause, policy_segments)
        coverage = classify_coverage(match["best_score"])

        report.append({
            "clause_id": clause["clause_id"],
            "title": clause["title"],
            "nist_function": clause["nist_function"],
            "nist_category": clause["nist_category"],
            "severity": clause["severity"],
            "coverage": coverage,
            "match_score": round(match["best_score"], 2),
            "matched_segment_id": match["best_segment_id"],
            "matched_segment_text": match["best_segment_text"]
        })

    return report
