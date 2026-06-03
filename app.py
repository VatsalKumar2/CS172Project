import os
import lucene

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, Sort, SortField

from flask import Flask, request, jsonify

app = Flask(__name__)

INDEX_DIR = os.environ.get("INDEX_DIR", "./bsky_index")
SORT_FIELDS = ("like_count", "reply_count", "repost_count", "quote_count", "created_at")

lucene.initVM(vmargs=['-Djava.awt.headless=true'])


@app.route("/search", methods=["GET"])
def search():
    lucene.getVMEnv().attachCurrentThread()

    query_str = request.args.get("q", "").strip()
    if not query_str:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    top_n   = int(request.args.get("top_n", 10))
    author  = request.args.get("author")
    sort_by = request.args.get("sort")

    if author:
        query_str = f'{query_str} AND author_handle:"{author}"'

    store    = SimpleFSDirectory(Paths.get(INDEX_DIR))
    reader   = DirectoryReader.open(store)
    searcher = IndexSearcher(reader)

    # Use QueryParser with default field "text"
    # Users can still search other fields explicitly e.g. author_handle:alice
    analyzer = StandardAnalyzer()
    parser   = QueryParser("text", analyzer)
    query    = parser.parse(query_str)

    if sort_by in SORT_FIELDS:
        hits = searcher.search(query, top_n, Sort(SortField(sort_by, SortField.Type.STRING, True)))
    else:
        hits = searcher.search(query, top_n)

    results = []
    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        results.append({
            "score":               hit.score,
            "uri":                 doc.get("uri"),
            "author_handle":       doc.get("author_handle"),
            "author_display_name": doc.get("author_display_name"),
            "text":                doc.get("text"),
            "created_at":          doc.get("created_at"),
            "like_count":          doc.get("like_count"),
            "reply_count":         doc.get("reply_count"),
            "repost_count":        doc.get("repost_count"),
            "quote_count":         doc.get("quote_count"),
        })

    reader.close()
    return jsonify({"total": len(results), "results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)