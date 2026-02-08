import re

MIN_SEGMENT_LENGTH = 25  # characters


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison:
    - lowercase
    - remove punctuation
    - collapse whitespace
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def segment_policy(text: str):
    """
    Split policy text into sentence-level segments.
    """
    raw_segments = re.split(r"[.!?]\s+", text)
    segments = []

    for idx, segment in enumerate(raw_segments):
        segment = segment.strip()

        if len(segment) < MIN_SEGMENT_LENGTH:
            continue

        segments.append({
            "id": idx,
            "text": segment,
            "normalized": normalize_text(segment)
        })

    return segments
