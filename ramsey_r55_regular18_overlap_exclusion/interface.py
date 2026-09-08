#!/usr/bin/env python3
"""Recognize the excluded regular strata and extract a literal monochromatic five."""
import hashlib,itertools,json,re,sys
from pathlib import Path

def read_graph(obj):
    if set(obj)!={'n','red_hex'} or type(obj['n']) is not int or obj['n']!=43:raise ValueError('graph schema')
    s=obj['red_hex']
    if not isinstance(s,str) or not re.fullmatch('[0-9a-f]{226}',s):raise ValueError('graph word')
    word=int(s,16)
    if word>>903:raise ValueError('high padding bit')
    a=[0]*43
    for bit,(i,j) in enumerate(itertools.combinations(range(43),2)):
        if word>>bit&1:a[i]|=1<<j;a[j]|=1<<i
    return a

def extract(obj):
    a=read_graph(obj);degrees=[x.bit_count() for x in a]
    if len(set(degrees))!=1 or degrees[0] not in (18,24):
        return {'status':'OUTSIDE_PROVED_REGULAR_BRANCH','degrees':degrees}
    for color in (1,0):
        masks=a if color else [((1<<43)-1)^a[i]^(1<<i) for i in range(43)]
        def go(prefix,mask):
            if len(prefix)==5:return prefix
            while mask.bit_count()>=5-len(prefix):
                b=mask&-mask;mask-=b
                found=go(prefix+[b.bit_length()-1],mask&masks[b.bit_length()-1])
                if found:return found
            return None
        q=go([],(1<<43)-1)
        if q is not None:
            return {'status':'REJECTED_COMPLETE_REGULAR18_OR24_FAMILY','regular_degree':degrees[0],'color':color,'vertices':q,'graph_word_sha256':hashlib.sha256(obj['red_hex'].encode('ascii')).hexdigest()}
    raise RuntimeError('Excluded-family input without a certificate; theorem or implementation mismatch')

if __name__=='__main__':print(json.dumps(extract(json.loads(Path(sys.argv[1]).read_text())),indent=2))
