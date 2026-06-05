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
Powershell: python -m venv venv
```

``` macOS
macOS: python3 -m venv venv
```

Activate it:

```powershell
Powershell: .\venv\Scripts\Activate.ps1
```

``` macOS
macOS: source venv/bin/activate
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
Powershell: copy .env.example .env
```

``` macOS
macOS: cp .env.example .env
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
Powershell: python src/collect_bsky.py
```

``` macOS
macOS: python3 src/collect_bsky.py
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
Powershell: python src/verify_jsonl.py
```

```macos
macOS: python3 src/verify_jsonl.py
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
Powershell: dir data
```

```macOS
macOS: ls -lh data
```

The `Length` column shows the file size in bytes.

To see the size in MB:

```powershell
Powershell: (Get-Item data\bluesky_posts.jsonl).Length / 1MB
```

```macOS
macOS: stat -f%z data/bluesky_posts.jsonl
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

## Enabling and Running the Search Algorithm

The search algorithm uses PyLucene to search the Bluesky index created from `bsky_posts.jsonl`. It returns the top 10 results ranked by a combined score using BM25 relevance and a small social engagement boost.

### 1. SSH into the Bolt server
If you're not in the server yet, open the terminal and enter this
```bash
ssh <yourNetID>@bolt.cs.ucr.edu
example: ssh jdoe001@bolt.cs.ucr.edu
```

### 2. Enter the CS172 PyLucene environment

```bash
cs172_login
```

After logging in, you should be inside the CS172 container.

### 3. Go to the project directory inside the container

```bash
cd /home/cs172
```

Check that the required files exist:

```bash
ls
```

You should see:

```bash
bsky_posts.jsonl
indexer.py
search_algo.py
```

### 4. Build the PyLucene index

Run the indexer on the collected Bluesky JSONL file:

```bash
python3 indexer.py bsky_posts.jsonl bsky_index
```

This creates a PyLucene index folder called:

```bash
bsky_index
```

You can confirm it was created with:

```bash
ls bsky_index
```

### 5. Run the search algorithm

After the index is created, run:

```bash
python3 search_algo.py bsky_index
```

The program will prompt:

```bash
Search query:
```

Type a search query, for example:

```bash
software internship
```

or:

```bash
remote SWE intern
```

The algorithm will return the top 10 results ordered by decreasing final score.

### 6. Exit the search program

To stop the search loop, type:

```bash
exit
```

or:

```bash
quit
```

### Search Algorithm Details

The search algorithm searches the following indexed fields:

```bash
text
link_title
author_handle
author_display_name
```

It uses BM25 as the main relevance ranking method. The final ranking score is calculated using:

```bash
final_score = 0.85 * BM25_relevance_score + 0.15 * social_score
```

The social score is based on Bluesky engagement fields:

```bash
like_count
reply_count
repost_count
quote_count
```
### 7. Running the full web application

If flask is not already installed, run this:

```bash
pip install flask
```
Then run the indexer:

```bash
python3 indexer.py bsky_posts.jsonl bsky_index
```

After the indexer has been created, run this:
```bash
python3 app.py ./bsky_index
```
Once this command has been executed, a notification will popup asking if you would like to open the app on a browser.
Click open, but if there are no popup notification, copying and pasting the http link provided in terminal containing your IP address
and the port number 8080 will also work. For example, the terminal will output this:
```bash
Running on http://169.235.31.65:8080
```
Copy and paste http link in a browser to see web app. 
If web app is not working and keeps on loading, campus vpn might be needed in order to help with network connection.
