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


def main():
    clauses_path = os.path.join(
        "data", "nist_csf", "policy_clauses.json"
    )

    print("Loading policy clauses...")
    clauses = load_policy_clauses(clauses_path)

    print(f"Loaded {len(clauses)} policy clauses.")
    print("Sample clause:")
    print(clauses[0])


if __name__ == "__main__":
    main()
