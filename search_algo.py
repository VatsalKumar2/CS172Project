import sys
import math
import lucene

from java.nio.file import Paths

from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.queryparser.classic import QueryParser


class SearchAlgorithm:
    def __init__(self, index_dir):
        lucene.initVM(vmargs=["-Djava.awt.headless=true"])

        self.index_dir = index_dir
        self.analyzer = StandardAnalyzer()

        self.store = SimpleFSDirectory(Paths.get(index_dir))
        self.reader = DirectoryReader.open(self.store)

        self.searcher = IndexSearcher(self.reader)

        self.searcher.setSimilarity(BM25Similarity())

        self.search_fields = [
            "text",
            "link_title",
            "author_handle",
            "author_display_name"
        ]

        self.parser = MultiFieldQueryParser(
            self.search_fields,
            self.analyzer
        )

    def search(self, query_text, top_k=10):
        if query_text is None:
            return []

        elif query_text.strip() == "":
            return []

        else:
            escaped_query = QueryParser.escape(query_text)
            query = self.parser.parse(escaped_query)

            # PyLucene searches the inverted index and returns top-k documents.
            top_docs = self.searcher.search(query, top_k)

            results = []

            for score_doc in top_docs.scoreDocs:
                doc = self.searcher.doc(score_doc.doc)

                relevance_score = float(score_doc.score)

                like_count = self.safe_int(doc.get("like_count"))
                reply_count = self.safe_int(doc.get("reply_count"))
                repost_count = self.safe_int(doc.get("repost_count"))
                quote_count = self.safe_int(doc.get("quote_count"))

                social_score = self.compute_social_score(
                    like_count,
                    reply_count,
                    repost_count,
                    quote_count
                )

                final_score = self.compute_final_score(
                    relevance_score,
                    social_score
                )

                result = {
                    "final_score": final_score,
                    "relevance_score": relevance_score,
                    "social_score": social_score,
                    "author_handle": doc.get("author_handle"),
                    "author_display_name": doc.get("author_display_name"),
                    "text": doc.get("text"),
                    "link_title": doc.get("link_title"),
                    "created_at": doc.get("created_at"),
                    "uri": doc.get("uri"),
                    "like_count": like_count,
                    "reply_count": reply_count,
                    "repost_count": repost_count,
                    "quote_count": quote_count
                }

                results.append(result)

            # Similar to the slides: return documents in decreasing score order.
            results.sort(
                key=lambda result: result["final_score"],
                reverse=True
            )

            return results[:top_k]

    def compute_social_score(
        self,
        like_count,
        reply_count,
        repost_count,
        quote_count
    ):
        # Social score is our social-network version of popularity.
        # It is not PageRank, but it follows the idea that popular results
        # can be ranked higher along with relevance.

        score = 0

        score += like_count
        score += reply_count * 2
        score += repost_count * 3
        score += quote_count * 3

        if score <= 0:
            return 0

        else:
            return math.log(1 + score)

    def compute_final_score(self, relevance_score, social_score):
        # Main score is still BM25 relevance.
        # Social score is only a smaller boost.

        relevance_weight = 0.85
        social_weight = 0.15

        final_score = (
            relevance_weight * relevance_score
            + social_weight * social_score
        )

        return final_score

    def safe_int(self, value):
        try:
            return int(value)

        except Exception:
            return 0


def print_results(results):
    if len(results) == 0:
        print("No results found.")

    else:
        for index, result in enumerate(results, start=1):
            print("\n--------------------------------")
            print(f"Rank: {index}")
            print(f"Final Score: {round(result['final_score'], 4)}")
            print(f"BM25 Relevance Score: {round(result['relevance_score'], 4)}")
            print(f"Social Score: {round(result['social_score'], 4)}")
            print(f"Author: {result['author_handle']}")
            print(f"Created At: {result['created_at']}")
            print(f"Likes: {result['like_count']}")
            print(f"Replies: {result['reply_count']}")
            print(f"Reposts: {result['repost_count']}")
            print(f"Quotes: {result['quote_count']}")
            print(f"URI: {result['uri']}")
            print(f"Link Title: {result['link_title']}")
            print("Text:")
            print(result["text"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 search_algorithm.py <index_dir>")
        sys.exit(1)

    index_dir = sys.argv[1]

    search_engine = SearchAlgorithm(index_dir)

    while True:
        query = input("\nSearch query: ")

        if query.lower() == "exit":
            break

        elif query.lower() == "quit":
            break

        else:
            results = search_engine.search(query, top_k=10)
            print_results(results)