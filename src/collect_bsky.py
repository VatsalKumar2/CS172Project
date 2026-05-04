import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from atproto import Client


load_dotenv()

HANDLE = os.getenv("BSKY_HANDLE")
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

QUERY = "climate change"
MAX_POSTS = 300
OUTPUT_FILE = Path("data/bluesky_posts.jsonl")


def post_to_dict(post):
    record = post.record

    return {
        "platform": "bluesky",
        "uri": post.uri,
        "cid": post.cid,
        "author_handle": post.author.handle,
        "author_display_name": post.author.display_name,
        "text": getattr(record, "text", ""),
        "created_at": getattr(record, "created_at", None),
        "like_count": post.like_count,
        "reply_count": post.reply_count,
        "repost_count": post.repost_count,
        "quote_count": post.quote_count,
        "indexed_at": post.indexed_at,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    if not HANDLE or not APP_PASSWORD:
        raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD in .env file.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    client = Client()
    client.login(HANDLE, APP_PASSWORD)

    collected = 0
    cursor = None
    seen_uris = set()

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        while collected < MAX_POSTS:
            response = client.app.bsky.feed.search_posts(
                {
                    "q": QUERY,
                    "limit": min(100, MAX_POSTS - collected),
                    "cursor": cursor,
                }
            )

            posts = response.posts

            if not posts:
                break

            for post in posts:
                if post.uri in seen_uris:
                    continue

                seen_uris.add(post.uri)
                f.write(json.dumps(post_to_dict(post), ensure_ascii=False) + "\n")
                collected += 1

            print(f"Collected {collected} posts")

            cursor = response.cursor
            if not cursor:
                break

            time.sleep(1)

    print(f"Done. Saved {collected} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()