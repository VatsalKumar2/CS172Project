from dotenv import load_dotenv
from atproto import Client
import os

load_dotenv()

HANDLE       = os.getenv("BSKY_HANDLE")
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

COMMENT_KEYWORDS = [
    # general internship
    "internship", "intern", "co-op", "coop", "new grad",
    "entry level", "hiring", "offer", "referral", "apply",
    "application", "interview", "resume", "salary", "stipend",
    "remote", "hybrid", "onsite", "position", "role",

    # computer science
    "software", "software engineer", "SWE", "developer",
    "frontend", "backend", "fullstack", "full stack",
    "data science", "data scientist", "data engineer",
    "machine learning", "ML", "AI", "artificial intelligence",
    "deep learning", "NLP", "computer vision",
    "algorithms", "data structures", "leetcode", "coding",
    "python", "java", "javascript", "typescript", "c++", "rust",
    "react", "node", "django", "flask",
    "cloud", "AWS", "Azure", "GCP", "devops", "docker",
    "kubernetes", "CI/CD", "git", "github",
    "database", "SQL", "NoSQL", "mongodb", "postgresql",
    "cybersecurity", "security", "network", "systems",
    "operating systems", "distributed systems",
    "mobile", "iOS", "android", "swift", "kotlin",
    "api", "REST", "microservices",

    # computer engineering
    "computer engineering", "hardware", "embedded",
    "embedded systems", "firmware", "FPGA", "VHDL", "verilog",
    "circuit", "microcontroller", "arduino", "raspberry pi",
    "signal processing", "DSP", "VLSI", "semiconductor",
    "PCB", "schematic", "RTL", "ASIC",
    "computer architecture", "processor", "GPU", "CPU",
    "IoT", "internet of things", "robotics", "automation",
    "control systems", "electronics",

    # companies and jobs
    "Google", "Meta", "Apple", "Microsoft", "Amazon",
    "Netflix", "Nvidia", "OpenAI", "Qualcomm", "Intel",
    "Tesla", "SpaceX", "LinkedIn", "Uber", "Airbnb",
    "FAANG", "big tech", "startup", "company", "team",
    "project", "research", "lab",
]


def get_comments(client, post_uri):
    try:
        response = client.app.bsky.feed.get_post_thread({"uri": post_uri})
        thread   = response.thread
        comments = []

        def flatten_replies_tree(node):
            if not hasattr(node, "replies") or not node.replies:
                return
            for reply in node.replies:
                if not hasattr(reply, "post"):
                    continue
                reply_text = getattr(reply.post.record, "text", "")
                if not reply_text:
                    continue
                if not any(kw in reply_text.lower() for kw in COMMENT_KEYWORDS):
                    continue
                comments.append({
                    "author": reply.post.author.handle,
                    "body":   reply_text,
                    "likes":  reply.post.like_count,
                })
                flatten_replies_tree(reply)

        flatten_replies_tree(thread)
        return comments

    except Exception as e:
        print(f"Could not fetch comments: {e}")
        return []


client = Client()
client.login(HANDLE, APP_PASSWORD)

response = client.app.bsky.feed.search_posts({"q": "internship", "limit": 20})

for post in response.posts:
    if not post.reply_count or post.reply_count == 0:
        continue

    comments = get_comments(client, post.uri)

    if not comments:
        continue

    print(f"\nPost: {post.record.text[:80]}")
    print(f"Reply count: {post.reply_count}")
    print(f"Comments fetched: {len(comments)}")
    for c in comments[:3]:
        print(f"  → {c['author']}: {c['body'][:60]}")