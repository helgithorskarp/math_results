"""Literal seven-BLUE-page witnesses after the ordinary C/C reduction."""
from itertools import combinations, permutations, product
from functools import lru_cache
import hashlib, json
import literal as L
import reference as R
from reduction import core, QMASKS, QS, canonical

def verify(require,n,spine,pages):
    i,j=spine
    require(i!=j and j not in n[i] and i not in n[j],'terminal spine must be BLUE')
    require(len(pages)==7 and len(set(pages))==7,'seven distinct original BLUE pages')
    require(all(z not in spine and z not in n[i] and z not in n[j] for z in pages),
            'each actual original vertex is BLUE to both spine endpoints')

def run(require,guard,digest):
    roles=[w for k in range(3,7) for w in QMASKS[k]]
    require(len(roles)==42,'all initially free rank3..6 Ti Q rows')
    U22=set(range(22));full=(1<<22)-1
    models=[];witness_hash=hashlib.sha256();count=0;damages=[]
    @lru_cache(maxsize=None)
    def ranked_model(rename,k1,k2):
        return core(require,qend=(2,2,2,k1,k2),rename=rename)
    for rename in permutations(range(3)):
        n,d,q,c,b=core(require,rename=rename)
        t0,t1,t2=(13+rename[t] for t in range(3))
        pages=[0,1,t0,5,6,7,8]
        require(sorted((set(range(16))-n[t1]-{t1})&(set(range(16))-n[t2]-{t2}))==sorted(pages),
                'entire seven mandatory BLUE pages in original16')
        models.append([list(rename),[t1,t2],pages])
        for f,g in product(roles,repeat=2):
            actual,ad,aq,ac,ab=ranked_model(rename,f.bit_count(),g.bit_count())
            nn=[set(s) for s in actual];bb=list(ab)
            nn[t1].update(QS[f]);nn[t2].update(QS[g])
            bb[t1]|=f<<16;bb[t2]|=g<<16
            require(len(nn[t1])==ad[t1] and len(nn[t2])==ad[t2],
                    'actual original22 terminal endpoint degrees, not default ranks')
            verify(require,nn,(t1,t2),pages)
            blue=sorted((U22-nn[t1]-{t1})&(U22-nn[t2]-{t2}))
            bitblue=[z for z in range(22) if ((full&~(bb[t1]|(1<<t1)))&(full&~(bb[t2]|(1<<t2))))>>z&1]
            require(blue==bitblue and len(blue)==7+6-(f|g).bit_count(),
                    'whole actual22 terminal BLUE page list in both representations')
            witness_hash.update(canonical([rename,f,g,pages,blue]))
            count+=1
        guard()
        f,g=7,56
        positive=[set(s) for s in n]
        positive[t1].update(QS[f]);positive[t2].update(QS[g])
        verify(require,positive,(t1,t2),pages)
        for name in ('drop-page','duplicate-page','red-page','spine-page','red-spine','damaged-blue-incidence'):
            nn=[set(s) for s in positive];ps=list(pages)
            if name=='drop-page':ps.pop()
            elif name=='duplicate-page':ps[-1]=ps[0]
            elif name=='red-page':ps[-1]=2
            elif name=='spine-page':ps[-1]=t1
            elif name=='red-spine':nn[t1].add(t2);nn[t2].add(t1)
            elif name=='damaged-blue-incidence':nn[t1].add(ps[-1])
            try:verify(require,nn,(t1,t2),ps)
            except ValueError:damages.append([list(rename),name])
            else:raise ValueError('damaged original BLUE witness accepted: '+name)
    require(count==10584 and len(damages)==36,'all stated terminal roles and semantic damages')
    guard()
    return {'agent':'six-books-1','role':'researcher','complete':True,
            'six_original_T_label_models':models,'all_literal_bit_terminal_Q_roles':[count,witness_hash.hexdigest()],
            'mandatory_BLUE_pages':7,'terminal_semantic_damages_rejected':damages,
            'Ti_row_input_is_derived_C_C':True,'Q_Q_or_SX_Q_completion_assumed':False,
            'ordinary_bridge_unformalized':True,'independent_review_pending':True}
