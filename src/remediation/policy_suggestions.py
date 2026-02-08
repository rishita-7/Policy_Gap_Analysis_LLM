def generate_policy_suggestions(gap_report):
    """
    Generate policy improvement suggestions based on gap report.
    """

    suggestions = []

    for item in gap_report:
        coverage = item["coverage"]

        if coverage == "Missing":
            suggestion = (
                f"Add a policy statement that addresses the following requirement: "
                f"{item['title']}. The policy should clearly define responsibilities, "
                f"processes, and enforcement mechanisms."
            )

        elif coverage == "Partial":
            suggestion = (
                f"Enhance the existing policy section related to {item['title']} by "
                f"providing more detailed guidance, roles, and implementation procedures "
                f"to fully meet the requirement."
            )

        else:  # Covered
            suggestion = "No changes required. Existing policy sufficiently addresses this requirement."

        suggestions.append({
            "clause_id": item["clause_id"],
            "title": item["title"],
            "severity": item["severity"],
            "coverage": coverage,
            "suggestion": suggestion
        })

    return suggestions
