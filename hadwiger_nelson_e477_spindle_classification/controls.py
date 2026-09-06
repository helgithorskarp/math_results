"""Colour-certificate mutations, frame controls and producer cross-check."""
import json,copy,random
from itertools import product
from verify import ROOT,PARENT,r,require,word_check,partition,mandatory,transform
import sys
sys.path.insert(0,str(PARENT))
from graph import crossunit

def main():
    rejected=0
    def reject(fn):
        nonlocal rejected
        try:fn()
        except ValueError:rejected+=1
        else:raise RuntimeError('Malformed control accepted')
    for bad in ('0','004','0x1',[0,1,2]):reject(lambda bad=bad:word_check(bad,3,[[0,1],[1,2]]))
    reject(lambda:word_check('001',3,[[0,1],[1,2]]))
    word_check('001',3,[[0,1],[1,2]],deleted=0)
    require(partition(['010','012'],3,[[0,1],[1,2]])==[],'Small partition')
    require(partition(['010'],3,[[0,1],[1,2]])==[[0,2]],'Small equal block')
    source=json.loads((PARENT/'certificate.json').read_text())['equal'];rows=source['points']
    ps=[r.point(p) for p in rows]
    for args in ((2,0,False,1),(0,2,False,1),(0,0,0,1),(0,0,False,0)):
        reject(lambda args=args:transform(ps,*args))
    cert=json.loads((PARENT/'mandatory_vertices.json').read_text())
    # These fail structural guards before any edge scan.
    for field,value in (('deleted',0),('deleted',True),('deleted',477),('colouring','0')):
        bad=copy.deepcopy(cert);bad[0][field]=value
        reject(lambda bad=bad:mandatory(bad,477,[]))
    bad=copy.deepcopy(cert);bad[1]['deleted']=bad[0]['deleted']
    reject(lambda:mandatory(bad,477,[]))
    # Definition-level bit-indexed arithmetic vs the producer's independent
    # coefficient condition, including every intended contact plus random pairs.
    rng=random.Random(20260906);compared=0
    for a,b,reflect,sign in product((0,1),(0,1),(False,True),(-1,1)):
        left,right=transform(ps,a,b,reflect,sign)
        A=[[u-v for u,v in zip(p,rows[a])] for p in rows]
        B=[[(1 if a==b else -1)*(u-v) for u,v in zip(p,rows[b])] for p in rows]
        if reflect:B=[[-aa,-bb,c,d] for aa,bb,c,d in B]
        pairs=[(1-a,1-b)]+[(rng.randrange(477),rng.randrange(477)) for _ in range(100)]
        for i,j in pairs:
            exact=r.distance(left[i],right[j])==r.scalar((36*128)**2)
            require(exact==crossunit(A[i],B[j]),'Cross formula disagreement');compared+=1
        # Check arbitrary physical distances within each isometric copy.
        for i,j in pairs[:10]:
            d=r.scale(r.distance(ps[i],ps[j]),128**2)
            require(r.distance(left[i],left[j])==d and r.distance(right[i],right[j])==d,'Nonisometric frame')
    print(json.dumps({'malformed_rejected':rejected,'cross_formula_agreements':compared,
                      'distance_preservation_checks':320,'small_partitions':2},sort_keys=True))
if __name__=='__main__':main()
