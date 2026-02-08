from nlp.preprocessing import segment_policy
from nlp.clause_preprocessing import preprocess_clauses
from nlp.matching import find_best_segment_match, classify_coverage
from reporting.gap_report import generate_gap_report
from remediation.policy_suggestions import generate_policy_suggestions
from roadmap.improvement_roadmap import generate_improvement_roadmap
from reporting.final_report import generate_compliance_report


import json
import os


def load_policy_clauses(filepath):
    """
    Load benchmark policy clauses from a JSON file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Policy clauses file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        clauses = json.load(file)

    return clauses


def load_policy_text(filepath):
    """
    Load organizational policy text from a file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Policy file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    return text


def main():
    clauses_path = os.path.join(
        "data", "nist_csf", "policy_clauses.json"
    )
    policy_path = os.path.join(
        "data", "sample_policies", "sample_policy.txt"
    )

    print("Loading policy clauses...")
    clauses = load_policy_clauses(clauses_path)
    print(f"Loaded {len(clauses)} policy clauses.\n")

    # 🔹 Phase 4.2 – Benchmark Clause Preprocessing
    clauses = preprocess_clauses(clauses)

    print("=== BENCHMARK CLAUSES (Phase 4.2 Validation) ===\n")
    for clause in clauses:
        print(f"[{clause['clause_id']}] {clause['title']}")
        print(f"  Description: {clause['description']}")
        print(f"  Normalized Requirement: {clause['normalized_requirement']}")
        print(f"  Normalized Keywords: {clause['normalized_keywords']}\n")

    print("Loading policy document...")
    policy_text = load_policy_text(policy_path)
    print("Policy text loaded successfully.\n")

    print("Policy Preview:")
    print(policy_text[:300])

    #  Phase 4.1 – Policy Segmentation
    policy_segments = segment_policy(policy_text)

    print("\n=== GAP ANALYSIS (Phase 4.3 Validation) ===\n")

    for clause in clauses:
        match = find_best_segment_match(clause, policy_segments)
        coverage = classify_coverage(match["best_score"])
    
        print(f"[{clause['clause_id']}] {clause['title']}")
        print(f"  Coverage: {coverage}")
        print(f"  Match Score: {match['best_score']:.2f}")
    
        if match["best_segment_id"] is not None:
            print(f"  Best Segment [{match['best_segment_id']}]: {match['best_segment_text']}")
        else:
            print("  Best Segment: None")
    
        print("-" * 60)


    print("\n=== POLICY SEGMENTS (Phase 4.1 Validation) ===\n")
    for seg in policy_segments:
        print(f"[{seg['id']}] {seg['text']}")

    gap_report = generate_gap_report(clauses, policy_segments)

    print("\n=== STRUCTURED GAP REPORT (Phase 5.1 Validation) ===\n")
    for item in gap_report:
        print(item)


    suggestions = generate_policy_suggestions(gap_report)
    
    # Build lookup table by clause_id
    suggestion_map = {
        s["clause_id"]: s["suggestion"]
        for s in suggestions
    }
    
    # Attach suggestion to EVERY clause
    for gap in gap_report:
        gap["suggestion"] = suggestion_map.get(
            gap["clause_id"],
            "No improvement required. Policy is adequately covered."
        )

    
    print("\n=== POLICY IMPROVEMENT SUGGESTIONS (Phase 5.2 Validation) ===\n")
    for g in gap_report:
        print({
            "clause_id": g["clause_id"],
            "suggestion": g["suggestion"]
        })

    roadmap = generate_improvement_roadmap(gap_report)

    # 🔹 Merge priority back into gap_report
    priority_map = {
        r["clause_id"]: r["priority"]
        for r in roadmap
    }
    
    for item in gap_report:
        item["priority"] = priority_map.get(item["clause_id"], "Unassigned")


    print("\n=== IMPROVEMENT ROADMAP (Phase 5.3 Validation) ===\n")
    for r in roadmap:
        print(r)

    print("\n=== DEBUG: gap_report keys ===\n")
    for item in gap_report:
        print(item["clause_id"], item.keys())


    final_report = generate_compliance_report(gap_report)
    print("\n=== FINAL COMPLIANCE REPORT (Phase 5.4 Validation) ===\n")

    print("Summary:")
    print(final_report["summary"])
    
    print("\nStatistics:")
    print(final_report["statistics"])
    
    print("\nPrioritized Roadmap:")
    for item in final_report["roadmap"]:
        print(item)


if __name__ == "__main__":
    main()
