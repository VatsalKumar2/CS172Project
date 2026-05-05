import json
from pathlib import Path

FILE = Path("data/bluesky_posts.jsonl")

REQUIRED_FIELDS = [
    "uri",
    "cid",
    "author_handle",
    "text",
    "created_at"
]


def main():
    count = 0
    invalid_json = 0
    missing_fields = 0
    empty_text = 0
    duplicates = 0

    seen_uris = set()

    with FILE.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                obj = json.loads(line)
                count += 1
            except json.JSONDecodeError:
                print(f"Invalid JSON on line {line_number}")
                invalid_json += 1
                continue

            # Check required fields
            for field in REQUIRED_FIELDS:
                if field not in obj or obj[field] is None:
                    missing_fields += 1
                    break

            # Check empty text
            if not obj.get("text"):
                empty_text += 1

            # Check duplicates
            uri = obj.get("uri")
            if uri in seen_uris:
                duplicates += 1
            else:
                seen_uris.add(uri)

    print("\n--- Verification Summary ---")
    print(f"Total JSON lines: {count}")
    print(f"Invalid JSON lines: {invalid_json}")
    print(f"Entries with missing fields: {missing_fields}")
    print(f"Empty text posts: {empty_text}")
    print(f"Duplicate posts: {duplicates}")


if __name__ == "__main__":
    main()