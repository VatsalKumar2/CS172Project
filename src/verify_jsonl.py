import json
from pathlib import Path


FILE = Path("data/bluesky_posts.jsonl")


def main():
    count = 0

    with FILE.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                json.loads(line)
                count += 1
            except json.JSONDecodeError as e:
                print(f"Invalid JSON on line {line_number}: {e}")
                return

    print(f"All good. Verified {count} JSON lines.")


if __name__ == "__main__":
    main()