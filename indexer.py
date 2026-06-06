import logging
import sys
import json
import os

logging.disable(sys.maxsize)

import lucene

from java.nio.file import Paths

from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import (
    IndexWriter,
    IndexWriterConfig,
    IndexOptions
)

# Initialize Lucene VM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])


if len(sys.argv) != 3:
    print("Usage: python3 indexer.py <input_jsonl> <index_dir>")
    sys.exit(1)

input_file = sys.argv[1]
index_dir = sys.argv[2]


# -----------------------------
# Configure field types
# -----------------------------

metaType = FieldType()
metaType.setStored(True)
metaType.setTokenized(False)

contentType = FieldType()
contentType.setStored(True)
contentType.setTokenized(True)
contentType.setIndexOptions(
    IndexOptions.DOCS_AND_FREQS_AND_POSITIONS
)

metaType.freeze()
contentType.freeze()

# -----------------------------
# Create index directory
# -----------------------------

index_dir = sys.argv[2]

if not os.path.exists(index_dir):
    os.mkdir(index_dir)

store = SimpleFSDirectory(Paths.get(index_dir))

analyzer = StandardAnalyzer()

config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

writer = IndexWriter(store, config)

# -----------------------------
# Parse JSONL and build index
# -----------------------------
doc_count = 0

with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        try:
            post = json.loads(line)

            doc = Document()

            author_handle = (
                post.get("author_handle") or ""
            )

            author_display_name = (
                post.get("author_display_name") or ""
            )

            text = (
                post.get("text") or ""
            )

            created_at = (
                post.get("created_at") or ""
            )

            uri = (
                post.get("uri") or ""
            )

            like_count = str(
                post.get("like_count") or 0
            )

            reply_count = str(
                post.get("reply_count") or 0
            )

            repost_count = str(
                post.get("repost_count") or 0
            )

            quote_count = str(
                post.get("quote_count") or 0
            )

            # Extract webpage titles from links
            links = post.get("links") or []

            link_titles = []

            for link in links:

                title = link.get("title")

                if title:
                    link_titles.append(title)

            link_text = " ".join(link_titles)

            # Add searchable fields

            doc.add(
                Field(
                    "author_handle",
                    author_handle,
                    contentType
                )
            )

            doc.add(
                Field(
                    "author_display_name",
                    author_display_name,
                    contentType
                )
            )

            doc.add(
                Field(
                    "text",
                    text,
                    contentType
                )
            )

            doc.add(
                Field(
                    "link_title",
                    link_text,
                    contentType
                )
            )

            # Add metadata fields

            doc.add(
                Field(
                    "created_at",
                    created_at,
                    metaType
                )
            )

            doc.add(
                Field(
                    "uri",
                    uri,
                    metaType
                )
            )

            doc.add(
                    Field(
                        "like_count",
                        like_count,
                        metaType
                    )
            )

            doc.add(
                    Field(
                        "reply_count",
                        reply_count,
                        metaType
                    )
            )

            doc.add(
                    Field(
                        "repost_count",
                        repost_count,
                        metaType
                    )
            )

            doc.add(
                    Field(
                       "quote_count",
                       quote_count,
                       metaType
                    )
            )

            writer.addDocument(doc)

            doc_count += 1

        except Exception as e:
            print("Error parsing document:", e)

writer.close()

print(f"Indexed {doc_count} documents.")
print(f"Index written to: {index_dir}")
