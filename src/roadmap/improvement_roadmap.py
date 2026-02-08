def determine_priority(severity, coverage):
    if coverage == "Covered":
        return "No Action"

    if severity == "High" and coverage == "Missing":
        return "Immediate"
    if severity == "High" and coverage == "Partial":
        return "Short-Term"
    if severity == "Medium" and coverage == "Missing":
        return "Short-Term"
    if severity == "Medium" and coverage == "Partial":
        return "Long-Term"

    return "Long-Term"


def generate_improvement_roadmap(gap_report):
    """
    Generate a prioritized improvement roadmap from gap report.
    """

    roadmap = []

    for item in gap_report:
        priority = determine_priority(
            item["severity"],
            item["coverage"]
        )

        roadmap.append({
            "clause_id": item["clause_id"],
            "title": item["title"],
            "nist_function": item["nist_function"],
            "severity": item["severity"],
            "coverage": item["coverage"],
            "priority": priority
        })

    return roadmap
