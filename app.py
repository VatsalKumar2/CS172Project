import os
import lucene
import sys

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, Sort, SortField

from flask import request, Flask, render_template
from search_algo import SearchAlgorithm

lucene.initVM(vmargs=["-Djava.awt.headless=true"])

app = Flask(__name__)

index_dir = sys.argv[1]
search = SearchAlgorithm(index_dir)

@app.route('/', methods= ['POST', 'GET'])
def home(): 
    return render_template('input.html')

@app.route('/output', methods=['POST', 'GET'])
def output():
    if request.method == 'GET': 
        return f"Nothing"
    if request.method == 'POST':
        form_data = request.form
        query = form_data['query']
        lucene.getVMEnv().attachCurrentThread()
        docs = search.search(str(query), 10)
        
        return render_template('output.html', lucene_output = docs)


if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8080, debug=True)
