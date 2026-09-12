"""Standalone literal endpoint verification; no producer, solver or canonicalizer import.

Verifies the final physical partition and destination, not the intermediate history.
"""
from pathlib import Path
from itertools import combinations
import hashlib,json,re
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def matrix(g):
    require(g['n']==43 and isinstance(g['red_hex'],str) and re.fullmatch('[0-9a-f]{226}',g['red_hex']) is not None,'graph framing')
    bits=int(g['red_hex'],16);require(bits<2**903,'padding');a=[[0]*43 for _ in range(43)]
    for i,(u,v) in enumerate(combinations(range(43),2)):a[u][v]=a[v][u]=(bits>>i)&1
    return a

def homogeneous(a,V,k,c):
    return next((S for S in combinations(V,k) if all(a[u][v]==c for u,v in combinations(S,2))),None)

def verify(source,packet,data):
    a=matrix(source);out=packet['packing'];dest=packet['destination'];red,blue,C=out['red'],out['blue'],out['core']
    require(sorted(sum(red+blue,[])+C)==list(range(43)),'partition')
    q,r=len(red)+len(blue),len(red)
    require(7<=q<=10 and 5<=r<=q,'macro shape')
    for blocks,c in ((red,1),(blue,0)):
        for B in blocks:require(len(B)==4 and homogeneous(a,B,4,c) is not None,'monochromatic block')
    require(homogeneous(a,sum(blue,[])+C,4,1) is None,'red maximality')
    require(homogeneous(a,C,4,0) is None,'blue maximality')
    for blocks,c in ((red,1),(blue,0)):
        for B in blocks:
            for v in C:
                for w in B:
                    if a[v][w]!=c and all(a[v][u]==c for u in B if u!=w):
                        old_edges=sum(a[u][z] for u,z in combinations(C,2))
                        new_edges=sum(a[u][z] for u,z in combinations([u for u in C if u!=v]+[w],2))
                        require(new_edges<=old_edges,'improving exchange')
    # All two-core-edge augmentations, checked as literal replacement K4s.
    for B in red:
        for four in combinations(C,4):
            u=four[0]
            for v in four[1:]:
                e=[u,v];f=[x for x in four if x not in e]
                for S in combinations(B,2):
                    T=[x for x in B if x not in S]
                    require(not (homogeneous(a,list(S)+e,4,1) is not None and homogeneous(a,T+f,4,1) is not None),'augmentation')
    p=dest['new_to_old'];require(sorted(p)==list(range(43)),'permutation')
    aa=matrix(dest['graph'])
    require(all(aa[u][v]==a[p[u]][p[v]] for u,v in combinations(range(43),2)),'903 physical edge identities')
    require(set(p[4*q:])==set(C),'transported core')
    require([set(p[4*i:4*i+4]) for i in range(r)]==[set(B) for B in red] or
            set(map(frozenset,[p[4*i:4*i+4] for i in range(r)]))==set(map(frozenset,red)),'red block transport')
    require(set(map(frozenset,[p[4*i:4*i+4] for i in range(r,q)]))==set(map(frozenset,blue)),'blue block transport')
    match=re.fullmatch(r'bo1-q(\d+)-r(\d+)-c(\d{6})',dest['task']);require(match is not None,'task syntax')
    tq,tr,index=map(int,match.groups());require((q,r)==(tq,tr),'task stratum')
    pins=json.loads((HERE.parent/'ramsey_r55_maximal_residual_domains/INPUTS.json').read_text())
    pin=next(x for x in pins if x['order']==len(C));raw=(Path(data)/pin['file']).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==pin['sha256'],'catalogue pin')
    rows=raw.splitlines();require(0<=index<len(rows)==pin['count'],'core index')
    bits=''.join(format(x-63,'06b') for x in rows[index][1:])
    require(all(aa[4*q+u][4*q+v]==int(bit) for bit,(v,u) in zip(bits,((v,u) for v in range(len(C)) for u in range(v)))),'catalogue all edges')
    words=[]
    for b in range(1,q):
        signatures=[sum(aa[i][4*b+j]<<i for i in range(4)) for j in range(4)]
        require(signatures==sorted(signatures,reverse=True),'root column order')
        words.append(sum(aa[i][4*b+j]<<(4*i+j) for i in range(4) for j in range(4)))
    require(words[:r-1]==sorted(words[:r-1],reverse=True) and words[r-1:]==sorted(words[r-1:],reverse=True),'whole block order')
    bad=dest['physical_five_in_input_labels']
    if bad is not None:
        V=bad['vertices'];require(len(V)==5 and len(set(V))==5 and all(0<=v<43 for v in V),'five-set')
        require(bad['color'] in (0,1) and homogeneous(a,V,5,bad['color']) is not None,'physical monochromatic five')
        require(dest['status']=='MONOCHROMATIC_FIVE','rejection status')
    else:
        for b,c in combinations(range(q),2):
            V=list(range(4*b,4*b+4))+list(range(4*c,4*c+4))
            require(all(homogeneous(aa,V,5,color) is None for color in (0,1)),'pair palette')
        for b in range(q):
            for v in range(4*q,43):
                V=list(range(4*b,4*b+4))+[v]
                require(all(homogeneous(aa,V,5,color) is None for color in (0,1)),'star palette')
        require(dest['status']=='ORDERED_CARRIER_NO_RAMSEY_VERDICT','admission status')
    return dict(status='LITERAL_NORMAL_FORM_DESTINATION_VERIFIED',task=dest['task'],new_original_task_verdict=False)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('source');p.add_argument('packet');a=p.parse_args()
    print(json.dumps(verify(json.loads(Path(a.source).read_text()),json.loads(Path(a.packet).read_text()),a.data),sort_keys=True))
