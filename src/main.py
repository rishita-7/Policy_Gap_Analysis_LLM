from src.nlp.preprocessing import segment_policy
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

    print("Loading policy document...")
    policy_text = load_policy_text(policy_path)
    print("Policy text loaded successfully.\n")


    print("Policy Preview:")
    print(policy_text[:300])


if __name__ == "__main__":
    main()
