from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup


# defines search for document GUI

def search(query):
    index_path = 'C:/Users/Cole Schnell/Desktop/Summer/Learn/project-2/CPS_meeting_index'
    myindex = open_dir(index_path)

    qp = QueryParser("text", schema=myindex.schema)
    q = qp.parse(u"{0}".format(query))

    with myindex.searcher() as s:
        results = s.search(q, limit=None)
        for result in results:
            dict = {
                "source" : result['source'],
                "path" : result['path'],
                "url" : result['url'],
                "date" : result['date'],
                "type" : result['type']
            }
            with open(result['path'], 'r', encoding="utf-8") as f:
                highlight = result.highlights("text", text=f.read())
            removetags = BeautifulSoup(highlight, 'lxml').text
            dict['highlight'] = removetags
            yield dict