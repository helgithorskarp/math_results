"""Reject malformed literal positive colouring certificates."""
import json
import model as m

def main():
    cert=json.loads((m.HERE/'certificate.json').read_text())
    edges,adj=m.load();row=cert['records'][0]
    vs=m.support(row['seed'],row['orientation'],adj);ie=m.induced(vs,edges)
    good=row['four_word'];m.check_word(vs,ie,good,4)
    u,v=ie[0];bad=list(good);bad[vs.index(v)]=bad[vs.index(u)]
    tests=[good[:-1],good+'0','4'+good[1:],''.join(bad)]
    rejected=0
    for word in tests:
        try:m.check_word(vs,ie,word,4)
        except ValueError:rejected+=1
        else:raise ValueError('accepted malformed word')
    m.require(rejected==4,'all controls rejected')
    print(json.dumps({'invalid_words_rejected':rejected,'solver_used':False},sort_keys=True))

if __name__=='__main__':main()
