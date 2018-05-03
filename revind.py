import os
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
import prep

#ripped straight from stackoverflow, 0 shame, 
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')    
    #this is supposed to filter out script, but does no such thing.
    for script in soup.find_all('script', src=False):
        script.decompose()    # rip it out
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    strout = u" ".join(t.strip() for t in visible_texts)
    strout = re.sub(r'<[^>]*?>', '', strout)
    return strout

class r_index:
        def __init__(self, dom):
               self.d = {}
               self.domain = dom
               self.rind = {}
               self.construct()
               self.finalize()

        def construct(self):
            if not os.path.exists(self.domain):
                print('domain folder not found')
            else:
                for file in os.listdir(self.domain):
                    self.scan_doc(file)
                    
        def scan_doc(self, doc):
                body = open(self.domain+'/'+doc, 'r').read()
                text = text_from_html(body)
                words = prep.prep(text)
                for w in words:
                        if w not in self.d.keys():
                                self.d[w] = {}
                        if doc not in self.d[w].keys():
                                self.d[w][doc] = 1
                        else:
                                self.d[w][doc] += 1
                                
        def finalize(self): #does the math, then stores the index as a .pkl file
            
            with open('dicts/'+ self.domain + '.pkl', 'wb') as f:
                pickle.dump(self.d, f, pickle.HIGHEST_PROTOCOL)

        def toString(self):
            out = 'WORDS:\n'
            for word in self.d.keys():
                out += '{0}\n'.format(word)
                for doc in self.d[word]:
                    out += '\tdoc: {0} count: {1}\n'.format(doc, self.d[word][doc])
            return out
