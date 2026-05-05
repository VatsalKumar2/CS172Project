import os
import json
import time
import requests
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from atproto import Client


load_dotenv()

HANDLE = os.getenv("BSKY_HANDLE")
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

QUERIES = [
    # THIS TARGETS GENERAL INTERNSHIPS
    "software internship",
    "SWE intern",
    "internship offer",
    "summer internship 2026",
    "tech internship",
    "internship hiring",
    "new grad internship",
    "internship referral",

    # THIS TARGETS SPECIFIC ROLES
    "product manager intern",
    "machine learning intern",
    "ML intern",
    "AI internship",
    "backend intern",
    "frontend intern",
    "fullstack intern",
    "devops intern",
    "cybersecurity intern",
    "cloud intern",
    "mobile intern",
    "iOS intern",
    "android intern",
    "embedded systems intern",
    "systems engineer intern",
    "hardware intern",
    "QA intern",
    "data engineer intern",
    "data analyst intern",
    "research intern",
    "UX intern",
    "design intern",

    # #  THIS QUERY TARGETS MOST POPULAR COMPANIES THAT STUDENTS WANT TO INTERN FOR
    # "Google internship",
    # "Meta internship",
    # "Apple internship",
    # "Microsoft internship",
    # "Amazon internship",
    # "Netflix internship",
    # "Nvidia internship",
    # "OpenAI internship",
    # "Spotify internship",
    # "Uber internship",
    # "Airbnb internship",
    # "LinkedIn internship",
    # "Salesforce internship",
    # "Adobe internship",
    # "Intel internship",
    # "Qualcomm internship",
    # "SpaceX internship",
    # "Tesla internship",
    # "Bloomberg internship",

    #  THIS QUERY TARGETS FOR POPULAR INTERNSHIP LOCATIONS
    "internship San Francisco",
    "internship Seattle",
    "internship New York",
    "internship Los Angeles",
    "internship Austin",
    "internship remote",
    "remote internship 2026",
    "hybrid internship",

    #  THIS QUERY TARGETS FOR CURRENTLY ENROLLED STUDENTS
    "CS student internship",
    "computer science internship",
    "engineering internship",
    "STEM internship",
]
MAX_POSTS_PER_QUERY = 1000
OUTPUT_FILE = Path("data/bluesky_posts.jsonl")


def get_comments(client, post_uri:str)->list:
    try:
        response = client.app.bsky.feed.get_post_thread({"uri":post_uri})
        thread = response.thread
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
                comments.append({
                    "author": reply.post.author.handle,  
                    "body":   reply_text,                
                    "likes":  reply.post.like_count,   
                })
                # Here, we apply recursion to go through our nested replies and to flatten the entire comment tree
                flatten_replies_tree(reply)
 
        flatten_replies_tree(thread)
        return comments
 
    except Exception as e:
        print(f"  Could not fetch comments for {post_uri}: {e}")
        return []
    

#def get_link(post):
    #post_links = []

    #post_facets = getattr(post.record, "facets", [])
    #if post_facets is not None:
        #for each in post_facets:
            #features = getattr(each, "features", [])
            #for values in features:
                #if hasattr(values, "uri"):
                    #post_links.append(values.uri)
    
    #return post_links

#def get_title(url):
    #try:
        #page = requests.get(url, timeout=8)
        #html = page.content.decode("utf-8", errors="ignore")
        #soup = BeautifulSoup(html, "lxml")
        #if soup.title and soup.title.string is not None:
            #return soup.title.string
        #return ""
    #except Exception as e:
        #print(e)
        #return None
    
#def crawl_link(urls):
    #with ThreadPoolExecutor(max_workers=5) as exe:
        #return list(exe.map(get_title, urls))

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

    total_collected = 0
    seen_uris = set()

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for query in QUERIES:
            print(f"\nCollecting posts for query: {query}")

            collected_for_query = 0
            cursor = None

            while collected_for_query < MAX_POSTS_PER_QUERY:
                response = client.app.bsky.feed.search_posts(
                    {
                        "q": query,
                        "limit": min(100, MAX_POSTS_PER_QUERY - collected_for_query),
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
                    
                    comments = [] #this is to store all the comments
                    if post.reply_count and post.reply_count > 0 :
                        comments = get_comments(client, post.uri)
                        #time.sleep(0.5) # DONT REMOVE THIS, WITHOUT THIS, IT MIGHT SKIP COMMENTS AND HIT THE RATE LIMIT

                    #links = []
                    #for values in get_link(post):
                        #links.append(values)

                    #if len(links) != 0:
                        #valid_links = []
                        #for urls in links:
                            #if urls and urls.startswith("http"):
                                #valid_links.append(urls)

                        #if valid_links:
                            #page_title = crawl_link(valid_links)
                        #else:
                            #page_title = []

                    data = post_to_dict(post)
                    data["comments"] = comments
                    data["search_query"] = query

                    #if len(links) != 0:
                        #data["links"] = links
                        #if len(page_title) != 0:
                            #data["page_title"] = page_title

                    f.write(json.dumps(data, ensure_ascii=False) + "\n")

                    collected_for_query += 1
                    total_collected += 1

                print(f"Collected {collected_for_query} posts for '{query}'")

                cursor = response.cursor
                if not cursor:
                    break

                time.sleep(1)

    print(f"\nDone. Saved {total_collected} total posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()