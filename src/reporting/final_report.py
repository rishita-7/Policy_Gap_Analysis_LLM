def generate_compliance_report(analysis_results):
    """
    Aggregate gap analysis results into a final compliance report.
    """

    report = {
        "summary": {},
        "statistics": {},
        "findings": [],
        "roadmap": []
    }

    total = len(analysis_results)
    covered = sum(1 for r in analysis_results if r["coverage"] == "Covered")
    partial = sum(1 for r in analysis_results if r["coverage"] == "Partial")
    missing = sum(1 for r in analysis_results if r["coverage"] == "Missing")

    report["statistics"] = {
        "total_clauses": total,
        "covered": covered,
        "partial": partial,
        "missing": missing,
        "coverage_percentage": round((covered / total) * 100, 2) if total else 0
    }

    report["summary"] = {
        "overall_posture": determine_posture(covered, partial, missing),
        "key_risks": missing
    }

    for result in analysis_results:
        report["findings"].append({
            "clause_id": result["clause_id"],
            "coverage": result["coverage"],
            "severity": result["severity"],
            "matched_text": result.get("matched_text", []),
            "suggestion": result["suggestion"]
        })

        if result["coverage"] != "Covered":
            report["roadmap"].append({
                "clause_id": result["clause_id"],
                "priority": result["priority"],
                "action": result["suggestion"]
            })

    return report


def determine_posture(covered, partial, missing):
    if missing > covered:
        return "High Risk"
    if missing == 0 and partial <= covered:
        return "Low Risk"
    return "Moderate Risk"
