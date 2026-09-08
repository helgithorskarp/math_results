#!/usr/bin/env python3
"""Check ten literal pairs; no theorem, producer, catalog or extractor imports."""
import hashlib,itertools,json,re,sys
from pathlib import Path

def verify(g,c):
    if g.get('n')!=43 or type(g.get('n')) is not int:raise ValueError('order')
    s=g.get('red_hex')
    if not isinstance(s,str) or re.fullmatch('[0-9a-f]{226}',s) is None or int(s,16)>>903:raise ValueError('word')
    q=c.get('vertices');color=c.get('color')
    if not isinstance(q,list) or len(q)!=5 or len(set(q))!=5 or any(type(x)is not int or x<0 or x>=43 for x in q):raise ValueError('vertices')
    if type(color)is not int or color not in (0,1):raise ValueError('color')
    if c.get('graph_word_sha256')!=hashlib.sha256(s.encode('ascii')).hexdigest():raise ValueError('graph binding')
    word=int(s,16)
    for u,v in itertools.combinations(sorted(q),2):
        index=u*(85-u)//2+v-u-1
        if (word>>index)&1!=color:raise ValueError('literal pair')
    return {'status':'VERIFIED_LITERAL_MONOCHROMATIC_FIVE','pairs':10}
if __name__=='__main__':print(json.dumps(verify(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text())),indent=2))
