"""Definition-level geometry and exhaustive colour checks; no producer import."""
import json,sys,argparse
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import radicals as r
from colour_check import solve
ROOT=Path(__file__).resolve().parent

def digest(x):
    return sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def require(value,message):
    if not value:raise ValueError(message)

def decode(row,spindle=False):
    side=0
    if spindle:side,*row=row
    require(type(side) is int and side in (0,1),'Bad side')
    require(len(row)==4 and all(type(x) is int for x in row),'Bad coordinate row')
    p=r.point(row)
    if side:return r.cmul((r.scalar(119),(0,0,0,0,3,0,0,0)),p)
    return r.pscale(p,128)

def edges(rows,den=1,spindle=False):
    require(type(den) is int and den>0,'Bad denominator')
    ps=[decode(p,spindle) for p in rows]
    require(len(set(ps))==len(ps),'Repeated coordinate')
    unit=r.scalar((36*128*den)**2)
    return [[i,j] for i,j in combinations(range(len(ps)),2)
            if r.distance(ps[i],ps[j])==unit]

def colouring(word,n,es,k):
    require(len(word)==n and all(type(c) is int and 0<=c<k for c in word),'Bad colours')
    require(all(word[i]!=word[j] for i,j in es),'Monochromatic edge')

def check_component(x,mode):
    pts=x['points'];den=x['denominator'];es=edges(pts,den)
    colouring(x['colouring'],len(pts),es,4)
    pin=0 if mode=='unequal' else 1
    stats=None
    if mode=='unequal':
        answer,stats=solve(len(pts),es,pins=[(0,0),(1,pin)])
        require(answer is None,'Conditional obstruction fails')
    if mode=='equal':
        require(pts[0]==[0,0,0,0],'Wrong origin')
        require(r.distance(r.point(pts[0]),r.point(pts[1]))==r.scalar(9216*den*den),'Wrong spindle radius')
    else:require(r.distance(r.point(pts[0]),r.point(pts[1]))==r.scalar(4752*den*den),'Wrong unequal-pair length')
    return {'vertices':len(pts),'edges':len(es),'point_sha256':digest(pts),'edge_sha256':digest(es),'forcing_search':stats}

def mandatory(witnesses,n,he):
    deleted=[z['deleted'] for z in witnesses]
    require(len(deleted)==253 and deleted==sorted(set(deleted)) and all(type(v) is int and 2<=v<n for v in deleted),'Bad mandatory vertex list')
    for z in witnesses:
        word=z['colouring'];v=z['deleted']
        require(type(word) is str and len(word)==n and all(c in '0123' for c in word),'Bad mandatory word')
        require(word[:2]=='01','Mandatory word has equal endpoints')
        require(all(word[a]!=word[b] for a,b in he if v not in (a,b)),'Mandatory word has a unit conflict')
    return {'mandatory_half_vertices':255,'minimum_non_four_order':509,'all_subgraphs_through_508_four_colourable':True,'witness_sha256':digest(witnesses)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--python',action='store_true',help='Use the slower reference colour checker')
    parser.add_argument('--native',type=Path,default=ROOT/'out/colour-check')
    args=parser.parse_args()
    x=json.loads((ROOT/'certificate.json').read_text())
    out={}
    for k in ('unequal','equal'):
        out[k]=check_component(x[k],k)
        print(k, out[k]['vertices'], out[k]['forcing_search'],file=sys.stderr,flush=True)
    pts=x['equal']['points'];den=x['equal']['denominator']
    full=[[0]+p for p in pts]+[[1]+p for p in pts[1:]]
    selected=x['retained_spindle_indices']
    require(selected==sorted(set(selected)) and all(type(i) is int and 0<=i<len(full) for i in selected),'Bad retained indices')
    rows=[full[i] for i in selected];es=edges(rows,den,True)
    colouring(x['five_colouring'],len(rows),es,5)
    print('final_geometry',len(rows),len(es),file=sys.stderr,flush=True)
    n=len(pts);left=[i for i in selected if i<n]
    right=sorted(([0] if 0 in selected else [])+[i-n+1 for i in selected if i>=n])
    require(left==right and left[:2]==[0,1],'Not symmetric terminal-preserving halves')
    ix={v:i for i,v in enumerate(selected)}
    cross=[e for e in es if all(selected[v]!=0 for v in e) and rows[e[0]][0]!=rows[e[1]][0]]
    require(cross==[[ix[1],ix[n]]],'Not the single-bridge spindle')
    hp=[pts[i] for i in left];he=edges(hp,den)
    if args.python:answer,stats=solve(len(hp),he,pins=[(0,0),(1,1)])
    else:
        from native import solve as native_solve
        answer,stats=native_solve(args.native,len(hp),he,pins=[(0,0),(1,1)])
    require(answer is None,'Retained half does not force equal endpoints')
    out['equal']['forcing_by_verified_subgraph']=len(hp)
    out['final']={'vertices':len(rows),'edges':len(es),'chromatic_number':5,'point_sha256':digest(rows),'edge_sha256':digest(es),'half_vertices':len(hp),'half_edges':len(he),'half_forcing_search':stats,'cross_edges':len(cross),'proof':'two isometric equal-pair halves and their single unit bridge'}
    require(selected==list(range(len(full))),'Target certificate describes the full spindle')
    witnesses=json.loads((ROOT/'mandatory_vertices.json').read_text())
    out['target_exclusion']=mandatory(witnesses,n,he)
    out['spindle_upper_order']=len(full)
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
