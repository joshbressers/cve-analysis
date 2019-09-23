#!/usr/bin/env python

import sys
from elasticsearch import Elasticsearch
import requests
from queue import Queue
import threading

# Setup some queues
global total_size
global url_q
global count_q
url_q = Queue()
url_q.maxsize = 1000
count_q = Queue()
q_threads = 8

class Reference:
    "CVE References class"

    def __init__(self, my_url, my_id):

        self.url = my_url
        self.id = my_id
        self.status = 0

    def get_id(self):
        return self.id

    def get_url(self):
        return self.url

    def get_status(self):
        return self.status

    def check_url(self):
        "Get the return code for a URL"

        try:
            r = requests.head(self.url, timeout=10)
            self.status = r.status_code
        except requests.ConnectionError:
            pass
        except requests.exceptions.InvalidSchema:
            pass
        except requests.exceptions.ReadTimeout:
            pass

def update_status(the_q):
    "Pull data from the status_queue and update it"

    while True:
        the_data = the_q.get()
        the_data.check_url()
        the_path = the_data.get_url()
        the_id = the_data.get_id()

        status = the_data.get_status()

        #es.update(index="cve-references", id=the_id, doc_type='ref',
        #            body={"doc": {"status_code": status}})
        the_q.task_done()
        count_q.put(1)
        print("%d/%d" % (count_q.qsize(), total_size))


# Set up some threads
for i in range(q_threads):
    worker = threading.Thread(
        target=update_status,
        args=(url_q,),
        name='worker-{}'.format(i),
    )
    worker.setDaemon(True)
    worker.start()

# Setup all the ES connections and run our first query
es = Elasticsearch(['http://elastic:changeme@localhost:9200'])
res = es.search(index="cve-index", scroll='5m',
                size=10, body={"_source": ["references.reference_data.url"],"query": {"match_all": {}}})

sid = res['_scroll_id']
scroll_size = res['hits']['total']['value']
total_size = res['hits']['total']['value']

current = 0

while(scroll_size > 0):

    for hit in res['hits']['hits']:

        # Not all CVE IDs have references
        if 'references' in hit['_source']:
            for url in hit['_source']['references']['reference_data']:
                the_path = url['url']
                the_id = hit['_id']
                the_ref = Reference(the_path, the_id)
                url_q.put(the_ref)

    res = es.scroll(scroll_id = sid, scroll = '5m')
    # Update the scroll ID
    sid = res['_scroll_id']
    scroll_size = len(res['hits']['hits'])



