from nlp.preprocessing import segment_policy
from nlp.clause_preprocessing import preprocess_clauses

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
    
    clauses = preprocess_clauses(clauses)
    print("=== BENCHMARK CLAUSES (Phase 4.2 Validation) ===\n")
    for clause in clauses:
        print(f"[{clause['id']}] {clause['requirement_text']}")
        print(f"  Normalized Requirement: {clause['normalized_requirement']}")
        print(f"  Normalized Keywords: {clause['normalized_keywords']}\n")
        

    print("Loading policy document...")
    policy_text = load_policy_text(policy_path)
    print("Policy text loaded successfully.\n")


    print("Policy Preview:")
    print(policy_text[:300])

    policy_segments = segment_policy(policy_text)

    print("\n=== POLICY SEGMENTS (Phase 4.1 Validation) ===\n")
    for seg in policy_segments:
        print(f"[{seg['id']}] {seg['text']}")



if __name__ == "__main__":
    main()
