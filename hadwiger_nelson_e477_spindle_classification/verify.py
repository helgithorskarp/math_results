"""Check the E477 separating basis and every marked-pair spindle placement.

No SAT search or producer contact formula is imported. Geometry uses generic
arithmetic in Q(sqrt(3),sqrt(11),sqrt(247)) from the parent certificate checker.
"""
from pathlib import Path
from itertools import combinations,product
from hashlib import sha256
import json,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'hadwiger_nelson_overlapping_forcing_seed'
sys.path.insert(0,str(PARENT))
import radicals as r

def require(ok,message):
    if not ok:raise ValueError(message)

def digest(x):
    return sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def word_check(word,n,edges,deleted=None):
    require(type(word) is str and len(word)==n and all(c in '0123' for c in word),'Malformed colouring')
    require(all(word[i]!=word[j] for i,j in edges if deleted not in (i,j)),'Monochromatic unit edge')

def partition(words,n,edges):
    require(type(words) is list and words,'No separating basis')
    for word in words:word_check(word,n,edges)
    buckets={}
    for i in range(n):buckets.setdefault(tuple(w[i] for w in words),[]).append(i)
    return sorted(b for b in buckets.values() if len(b)>1)

def mandatory(certificate,n,edges):
    require(type(certificate) is list,'Bad deletion certificate')
    deleted=[z['deleted'] for z in certificate]
    require(all(type(v) is int and 2<=v<n for v in deleted),'Bad deletion index')
    require(deleted==sorted(set(deleted)) and len(deleted)==253,'Bad deletion census')
    for z in certificate:
        word_check(z['colouring'],n,edges,z['deleted'])
        require(z['colouring'][:2]=='01','Deletion fails to separate terminals')
    return len(deleted)+2

def transform(points,a,b,reflect,sign):
    """Coordinates are scaled by 36*128. First copy centred at vertex a.

    Translate second vertex b to zero, turn its marked vector toward the
    first copy's marked vector, optionally reflect in the vertical axis,
    and rotate by sign*acos(119/128).
    """
    require(a in (0,1) and b in (0,1) and type(reflect) is bool and sign in (-1,1),'Bad frame')
    left=[r.pscale(r.psub(p,points[a]),128) for p in points]
    second=[r.pscale(r.psub(p,points[b]),1 if a==b else -1) for p in points]
    if reflect:second=[(r.neg(x),y) for x,y in second]
    rot=(r.scalar(119),(0,0,0,0,3*sign,0,0,0))
    return left,[r.cmul(rot,p) for p in second]

def check_contacts(points,a,b,reflect,sign):
    left,right=transform(points,a,b,reflect,sign)
    require(len(set(left))==len(left) and len(set(right))==len(right),'Noninjective map')
    require(set(left)&set(right)=={(r.ZERO,r.ZERO)},'Unexpected overlap')
    unit=r.scalar((36*128)**2)
    contact=[[i,j] for i,p in enumerate(left) for j,q in enumerate(right)
             if i!=a and j!=b and r.distance(p,q)==unit]
    require(contact==[[1-a,1-b]],'Unexpected contact census')
    return {'first_endpoint':a,'second_endpoint':b,'reflection':reflect,'sign':sign,
            'overlap':1,'cross_edges':contact,'vertices':len(left)+len(right)-1}

def main():
    source=json.loads((PARENT/'certificate.json').read_text())['equal']
    rows=source['points'];n=len(rows)
    require(n==477 and source['denominator']==1,'Wrong parent graph')
    require(all(len(p)==4 and all(type(v) is int for v in p) for p in rows),'Bad coordinates')
    require(rows[:2]==[[0,0,0,0],[0,0,96,0]],'Wrong terminals')
    points=[r.point(p) for p in rows]
    require(len(set(points))==n,'Repeated point')
    edges=[[i,j] for i,j in combinations(range(n),2) if r.distance(points[i],points[j])==r.scalar(1296)]
    require(digest(rows)=='9286b1fbe0875a15bb0be814986a066ee8b0c9544586b189320ade2c8d622d76','Parent points changed')
    require(digest(edges)=='93ca87d5d1596761646178b9512bb368ffda201e2f8c048ad116066243112d97','Parent edges changed')
    words=json.loads((ROOT/'separating_basis.json').read_text())
    require(partition(words,n,edges)==[[0,1]],'Another unseparated pair remains')
    lower=mandatory(json.loads((PARENT/'mandatory_vertices.json').read_text()),n,edges)
    frames=[]
    for a,b,reflect,sign in product((0,1),(0,1),(False,True),(-1,1)):
        frames.append(check_contacts(points,a,b,reflect,sign))
        print('checked',a,b,reflect,sign,file=sys.stderr,flush=True)
    out={'vertices':n,'unit_edges':len(edges),'separating_words':len(words),
         'separating_basis_sha256':digest(words),'only_unseparated_pair':[0,1],
         'checked_placements':len(frames),'placement_sha256':digest(frames),
         'each_full_spindle_vertices':953,'each_full_spindle_unit_edges':2*len(edges)+1,
         'mandatory_vertices_per_forcing_half':lower,
         'minimum_nonfour_order_lower_bound':2*lower-1,
         'every_subgraph_through_508_four_colourable':True}
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
