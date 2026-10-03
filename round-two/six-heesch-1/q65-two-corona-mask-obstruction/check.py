"""Independent physical-square/pair/adjugate reader for fixed-mask implication.

Does not import the producer or any solver. Rebuild clauses directly and replay
the short RUP refutation. Covers only the explicitly supplied finite envelope
and fixed physical motions; not an unrestricted non-tiling theorem.
"""
from collections import Counter
import hashlib
from itertools import combinations,product
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
import lower,rup

def require(ok,msg):
    if not ok:raise ValueError(msg)

def square(point,m,t):
    x,y=point;a,b,c,d=m
    vertices=[(a*(x+i)+b*(y+j)+t[0],c*(x+i)+d*(y+j)+t[1]) for i,j in product((0,1),repeat=2)]
    return min(v[0] for v in vertices),min(v[1] for v in vertices)

def frames(data,depth):
    source=list(map(tuple,data['cells']));images={}
    for swap in (False,True):
        for sx,sy in product((-1,1),repeat=2):
            m=(0,sx,sy,0) if swap else (sx,0,0,sy)
            fp=[square(p,m,(0,0)) for p in source];lo=(min(x for x,y in fp),min(y for x,y in fp))
            images[tuple(sorted((x-lo[0],y-lo[1]) for x,y in fp))]=(m,lo)
    require(len(images)==8,'literal source has unexpected symmetry')
    ordered=sorted(images);out=[]
    for level,poses in enumerate(data['levels'][:depth+1]):
        for o,x,y in poses:
            m,lo=images[ordered[o]];out.append((level,m,(x-lo[0],y-lo[1])))
    require(out[0]==(0,(1,0,0,1),(0,0)),'literal root is not identity')
    return out

def formula(data,certificate,depth,margin):
    source=set(map(tuple,data['cells']))
    # A direct finite box-distance definition, unlike producer dilation.
    ax=min(x for x,y in source)-margin;bx=max(x for x,y in source)+margin
    ay=min(y for x,y in source)-margin;by=max(y for x,y in source)+margin
    universe=sorted((x,y) for x in range(ax,bx+1) for y in range(ay,by+1)
        if any(max(abs(x-u),abs(y-v))<=margin for u,v in source))
    nv=len(universe)+520;clauses=set();fs=frames(data,depth)
    footprints=[{square(p,m,t):i+1 for i,p in enumerate(universe)} for level,m,t in fs]
    def add(c):
        c=tuple(sorted(set(c)))
        if any(-z in c for z in c):return
        clauses.add(c)
    # Direct unordered whole-copy pairs, no producer owner-map computation.
    for left,right in combinations(footprints,2):
        for point,v in left.items():
            if point in right:add([-v,-right[point]])
    for k in range(depth):
        for j,(level,m,t) in enumerate(fs):
            if level>k:continue
            for (x,y),v in footprints[j].items():
                for dx,dy in product((-1,0,1),repeat=2):
                    point=(x+dx,y+dy)
                    options=[fp[point] for l,fp in zip((f[0] for f in fs),footprints) if l<=k+1 and point in fp]
                    add([-v,*options])
    base=sorted(clauses)
    periods=certificate['periods'];require(periods==[[22,6],[-6,22]],'wrong physical lattice')
    (a,b),(c,d)=periods;det=a*d-b*c;require(det==520,'wrong lattice index')
    class_representatives=[(x,y) for y in range(2) for x in range(260)]
    rows=[Counter() for _ in class_representatives]
    for rep in certificate['representatives']:
        m=rep['matrix'];t=rep['translation'];g,h,i,j=m
        require(g*g+h*h==i*i+j*j==1 and g*i+h*j==0,'nonisometric period representative')
        for v,p in enumerate(universe,1):
            x,y=square(p,m,t)
            match=[]
            for k,(u,w) in enumerate(class_representatives):
                dx=x-u;dy=y-w
                if (d*dx-c*dy)%det==0 and (a*dy-b*dx)%det==0:match.append(k)
            require(len(match)==1,'nonunique physical lattice class')
            rows[match[0]][v]+=1
    for k,row in enumerate(rows):
        z=len(universe)+k+1
        for v,n in row.items():
            if n==1:add([-z,-v,*[q for q in row if q!=v]])
    bad=tuple(range(len(universe)+1,nv+1));nonempty=tuple(range(1,len(universe)+1))
    add(bad);add(nonempty)
    result=sorted(clauses)
    dimacs=('p cnf '+str(nv)+' '+str(len(result))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in result)).encode()
    return {'universe':universe,'frames':fs,'base':base,'clauses':result,'variables':nv,'rows':[sorted(row.items()) for row in rows],
        'bad_clause':bad,'nonempty_clause':nonempty,'formula_sha256':hashlib.sha256(dimacs).hexdigest()}

def sat(clauses,chosen):
    return all(any(z in chosen if z>0 else -z not in chosen for z in c) for c in clauses)

def verify():
    data=json.loads((BASE/'input.json').read_text());certificate=json.loads((BASE/'tiling.json').read_text())
    require(data['depth']==2 and data['margin']==1 and len(data['cells'])==65 and list(map(len,data['levels']))==[1,6,12],'literal scaffold declaration differs')
    literal=lower.check(data);f=formula(data,certificate,2,1)
    require((len(f['universe']),f['variables'],len(f['clauses']))==(123,643,2859),'wrong finite formula size')
    require(f['formula_sha256']=='aa183740e680950e521393b4f2111913bbe1f40600cc321ccab18f63c6574dcb','independent formula differs')
    trace=(BASE/'proof.rup').read_text();proof=rup.RupChecker(f['clauses'],f['variables']).verify(trace)
    original={i+1 for i,p in enumerate(f['universe']) if list(p) in data['cells']}
    require(sat(f['base'],original),'original Q65 packing/halos fail')
    require(all(sum(n for v,n in row if v in original)==1 for row in f['rows']),'old source period control fails')
    require(sat([c for c in f['clauses'] if c!=f['bad_clause']],original),'old-source control without failed-period clause fails')
    require(sat([c for c in f['clauses'] if c!=f['nonempty_clause']],set(f['bad_clause'])),'empty-source control without nonempty clause fails')
    counter=json.loads((BASE/'counterexample.json').read_text());fixture=counter['fixture'];positive=lower.check(fixture)
    raw=set(map(tuple,counter['raw_cells']));lo=min(x for x,y in raw),min(y for x,y in raw)
    require(sorted((x-lo[0],y-lo[1]) for x,y in raw)==list(map(tuple,fixture['cells'])),'counter source-origin binding differs')
    require(raw<=set(f['universe']) and len(raw)==64,'counter outside declared finite envelope')
    shapes=lower.images(fixture['cells']);claimed=[]
    for lev in fixture['levels']:
        claimed.append([{(x+tx,y+ty) for x,y in shapes[o]} for o,tx,ty in lev])
    expected=[]
    for level in (0,1):
        expected.append([{tuple(square(p,m,t)[j]-lo[j] for j in range(2)) for p in raw} for k,m,t in f['frames'] if k==level])
    require(claimed==expected,'counter frozen physical first placements differ')
    one=formula(data,certificate,1,1);selected={i+1 for i,p in enumerate(one['universe']) if p in raw}
    bad_rows=[k for k,row in enumerate(one['rows']) if sum(n for v,n in row if v in selected)!=1]
    selected|={len(one['universe'])+k+1 for k in bad_rows}
    require(bad_rows and sat(one['clauses'],selected),'disc-first counter does not break the fixed period')
    rejected=[]
    def reject(name,fn):
        try:fn()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged proof accepted: '+name)
    reject('missing nonempty-source obligation',lambda:rup.RupChecker([c for c in f['clauses'] if c!=f['nonempty_clause']],f['variables']).verify(trace))
    reject('missing failed-period obligation',lambda:rup.RupChecker([c for c in f['clauses'] if c!=f['bad_clause']],f['variables']).verify(trace))
    reject('missing final empty clause',lambda:rup.RupChecker(f['clauses'],f['variables']).verify('\n'.join(trace.splitlines()[:-1])+'\n'))
    reject('only first-prefix packing and halos',lambda:rup.RupChecker(one['clauses'],one['variables']).verify(trace))
    broken=json.loads(json.dumps(fixture));broken['levels'][1].pop()
    reject('missing first-corona whole copy',lambda:lower.check(broken))
    return {'agent':'six-heesch-1','role':'researcher','mask_family_periodicity_implication_checked':True,
        'source_sites':123,'variables':643,'clauses':2859,'formula_sha256':f['formula_sha256'],
        'fixed_copy_count':19,'required_halo_stages':2,'rup':proof,'proof_bytes':len(trace.encode()),
        'proof_sha256':hashlib.sha256(trace.encode()).hexdigest(),'original_disc_control':literal,
        'empty_mask_missing_nonempty_control':True,'original_tiling_control':True,
        'first_only_countercontrol':{'area':64,'normalization_shift':list(lo),'specified_period_bad_rows':len(bad_rows),'disc_lower':positive},
        'damaged_cases_rejected':rejected,'finite_target':'Open. This finite source-envelope and frozen-motion family only yields plane tilers.'}

def main():
    result=verify();require(result==json.loads((BASE/'expected.json').read_text()),'expected proof evidence differs')
    manifest=json.loads((BASE/'manifest.json').read_text())
    require(sorted(manifest)==sorted(p.name for p in BASE.iterdir() if p.is_file() and p.name!='manifest.json'),'manifest file coverage differs')
    for name,digest in manifest.items():require(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,'manifest mismatch: '+name)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
