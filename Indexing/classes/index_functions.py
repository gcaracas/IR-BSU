from collections import Counter
import math

class index_functions:
    def __init__(self):
        pass

    # Create a Term_Frequecy(Term_document)
    # applying weight based on frequency.
    def tf_td(self, doc_tokens=''):
        tf = Counter(doc_tokens)
        return tf

    def idf(self, N='', df=''):
        return math.log((N/df),10)

    def tf_tid(self, doc_tokens='', N=''):
        tf = self.tf_td(doc_tokens=doc_tokens)
        ret=dict()
        for t in list(tf.keys()):
            ret[t]=tf[t]*self.idf(N=N, df=tf[t])
        return ret

    def score_doc(self, doc='', query='', N=''):
        tokens=doc.split()
        tf_tid=self.tf_tid(doc_tokens=tokens,
                           N=N)
        #score=0
        #for t in query.split():
        #    if t in tokens:
        #        score=score+tf_tid[t]
        #return score
        return tf_tid
