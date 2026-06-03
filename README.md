# CS172 Project – Bluesky Data Collector

## Overview

This repository contains the Bluesky data collection portion of the CS172 Part A project.

This script uses the Bluesky API instead of Reddit/PRAW to collect social media posts. It searches Bluesky by keyword, handles pagination, removes duplicate posts, and stores the data in JSONL format.

Each line in the output file is one JSON object representing one post.

## Project Structure

```text
CS172Project/
├── src/
│   ├── collect_bsky.py
│   └── verify_jsonl.py
├── data/
│   └── bluesky_posts.jsonl
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Git
- Bluesky account
- Bluesky app password

## Step 1: Clone the Repository

```powershell
git clone https://github.com/VatsalKumar2/CS172Project.git
cd CS172Project
```

## Step 2: Create a Virtual Environment

```powershell
python -m venv venv
```

``` macOS
python3 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

``` macOS
source venv/bin/activate
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:

```powershell
.\venv\Scripts\Activate.ps1
```

## Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

## Step 4: Create a Bluesky Account

Go to:

```text
https://bsky.app
```

Create an account and log in.

## Step 5: Create a Bluesky App Password

In Bluesky:

```text
Settings → Privacy and Security → App Passwords → Add App Password
```

Copy the generated app password.

Do not use your normal Bluesky login password in the code.

## Step 6: Create the `.env` File

Copy the example file:

```powershell
copy .env.example .env
```

``` macOS
cp .env.example .env
```

Open `.env` and fill it in:

```env
BSKY_HANDLE=yourhandle.bsky.social
BSKY_APP_PASSWORD=your-app-password
```

Example:

```env
BSKY_HANDLE=exampleuser.bsky.social
BSKY_APP_PASSWORD=abcd-efgh-ijkl-mnop
```

Do not commit `.env` to GitHub.

## Step 7: Run the Crawler

```powershell
python src/collect_bsky.py
```

``` macOS
python3 src/collect_bsky.py
```

The crawler will:

1. Log into Bluesky.
2. Search posts using the configured keywords.
3. Crawl through paginated results.
4. Remove duplicate posts.
5. Save posts into a JSONL file.

## Step 8: Check the Output

The output file will be created here:

```text
data/bluesky_posts.jsonl
```

Each line is one post in JSON format.

Example structure:

```json
{
  "platform": "bluesky",
  "search_query": "climate change",
  "uri": "at://...",
  "cid": "...",
  "author_handle": "user.bsky.social",
  "author_display_name": "User",
  "text": "Post text here",
  "created_at": "2026-05-04T...",
  "like_count": 10,
  "reply_count": 2,
  "repost_count": 1,
  "quote_count": 0,
  "indexed_at": "...",
  "collected_at": "..."
}
```

## Step 9: Verify the JSONL File

Run:

```powershell
python src/verify_jsonl.py
```

```macos
python3 src/verify_jsonl.py
```

If the file is valid, it should print something like:

```text
--- Verification Summary ---
Total lines: X
Invalid JSON lines: X
Entries with missing fields: X
Empty text posts: X
Duplicate posts: X
```

## Step 10: Check File Size

Run:

```powershell
dir data
```

```macOS
ls -lh data
```

The `Length` column shows the file size in bytes.

To see the size in MB:

```powershell
(Get-Item data\bluesky_posts.jsonl).Length / 1MB
```

```macOS
stat -f%z data/bluesky_posts.jsonl
echo "$(stat -f%z data/bluesky_posts.jsonl) / 1024 / 1024" | bc -l
```

## Configuration

The crawler settings are inside:

```text
src/collect_bsky.py
```

You can change the search keywords:

```python
QUERIES = ["climate change", "global warming", "carbon emissions"]
```

You can change how many posts are collected per keyword:

```python
MAX_POSTS_PER_QUERY = 300
```

Increasing `MAX_POSTS_PER_QUERY` will collect more posts and create a larger dataset.

## Git Notes

These files should be committed:

```text
README.md
requirements.txt
.env.example
.gitignore
src/
```

These files should NOT be committed:

```text
.env
venv/
data/
```

Reasons:

- `.env` contains private credentials.
- `venv/` is machine-specific.
- `data/` contains generated output files.

## Commit and Push Changes

After editing code or README:

```powershell
git status
git add README.md .gitignore requirements.txt .env.example src
git commit -m "Update Bluesky crawler documentation"
git push
```

## Summary

This portion of the project handles:

- Bluesky API setup
- Authentication
- Base post collection
- Pagination
- Duplicate removal
- JSONL file storage
- Data verification

This script provides the base crawler and storage pipeline for the team’s Part A data collection.

## Part B: Pylucene Indexer & Web Interface
The Pylucene Indexer requires these files in the main directory:
```
indexer.py
bsky_posts.jsonl
```

Using the Pylucene Indexer:
- (Recommended) Login to the CS172 Bolt server using your UCR CS login:
  - Pylucene is installed on the UCR Bolt server, so it'll make access quicker than installing on your local machine.
  - Use Ctrl + Shift + P to open the Command Palette
  - Select 'Remote-SSH: Connect to Host'
  - SSH into Bolt Account:
    - ssh netid@bolt.cs.ucr.edu
  - Type in your Bolt Account Password

## In the Bolt Server:
Login into the CS172 container to access Pylucene by typing:
```
cs172_login
```

Check that the required files mentioned above exist in the directory:
```
bsky_posts.jsonl
indexer.py
```

- If they don't then you will need to scp them from your local machine:
  - First, while ssh'd into the Bolt Server, scp the Bluesky Posts data file and Indexer file into bolt server: 
  ```
  netid@bolt $ scp data/bsky_posts.jsonl netid@bolt.cs.ucr.edu:~/

  netid@bolt $ scp indexer.py netid@bolt.cs.ucr.edu:~/
  ```

  - Second, login to the CS172 container, and scp the Bluesky Posts data file and the Indexer file from Bolt server into the CS172 container:
  ```
  netid@bolt $ cs172_login
  cs172@class-060:~ $ scp netid@bolt.cs.ucr.edu:~/data/bsky_posts.jsonl ~/
  cs172@class-060:~ $ scp netid@bolt.cs.ucr.edu:~/indexer.py ~/
  ```

  - Check again that the required files mentioned above exist in the directory:
  ```
  bsky_posts.jsonl
  indexer.py
  ```

## Run the Indexer
Use this command to run the indexer:
```
python3 indexer.py bsky_posts.jsonl bsky_index
```

This is what the expected output should look like:
```
Indexed 10187 documents.
Index written to: bsky_index
```

Verify that all index files are in the bsky_index directory by typing:
```
ls bsky_index
```

The index is now ready for searching with PyLucene.

## Indexed Fields

Searchable fields:
```
author_handle
author_display_name
text
link_title
```

Stored Metadata Fields:
```
created_at
uri
like_count
reply_count
repost_count
quote_count
```

## Using Flask Backend:
After creating the index, run the following command to your terminal:
```
python3 app.py
```
Your terminal should display the following:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://169.235.31.65:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 975-513-288
```
Then create a new terminal and login to the cs172 container again. Finally to find something in the index, run the following command in the new terminal:
```
curl "http://localhost:5000/search?q=topic"
```
You can also search with filters. Here are examples of this
```
Get post with based on amount of likes
curl "http://localhost:5000/search?q=cats&sort=like_count"
Get top results
curl "http://localhost:5000/search?q=cats&top_n=20"
Search by author
curl "http://localhost:5000/search?q=cats&author=sachikoko.bsky.social"
```
