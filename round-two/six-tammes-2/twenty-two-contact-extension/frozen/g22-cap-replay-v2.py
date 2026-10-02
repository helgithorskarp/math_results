"""Literal replay of chosen G22 witnesses; no search or float selector.

Actual author: six-tammes-2, researcher. This shares the pinned model and
integer interval kernel and is not an independent review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter
import argparse,hashlib,importlib.util,json,signal,time

HERE=Path(__file__).resolve().parent
MODEL_HASH='d74b0f38daa9b5d29e82fac7603856f47d4a743590c15a7f12199a4fbaca95e1'
PUBLIC_HASH='0d1a9608e97f6810a2154176cc242988ad3113bb7de2e88b44696cc05cd536cc'
def require(ok,text):
    if not ok:raise ValueError(text)
model_file=HERE/'g22-cap-model-v2.py'
require(hashlib.sha256(model_file.read_bytes()).hexdigest()==MODEL_HASH,'frozen model hash')
public_model=HERE.parent/'round-two/six-tammes-2/twenty-two-contact-strip/model.py'
require(hashlib.sha256(public_model.read_bytes()).hexdigest()==PUBLIC_HASH,'committed9193 model hash')
spec=importlib.util.spec_from_file_location('literal_g22_cap_model',model_file)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
EXPECTED_CONTACTS={(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),
 (2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(8,13),
 (9,10),(9,11),(10,12)}
require(c.CONTACTS==EXPECTED_CONTACTS,'literal22 contacts; deleted pairs are inequalities')

def core_adjugate(triple,model):
    require(triple[-1]!=13,'core Gram witness on three core planes')
    labels=[c.LABELS[j] for j in triple]
    a=c.gram_product(model,labels[0],labels[1])
    b=c.gram_product(model,labels[0],labels[2])
    d=c.gram_product(model,labels[1],labels[2])
    determinant=1+2*a*b*d-a*a-b*b-d*d
    q=[(1-d)*(1+d-a-b),(1-b)*(1+b-a-d),(1-a)*(1+a-b-d)]
    return labels,q,determinant

def row_index(j,triple):
    require(type(j)is int and 0<=j<14 and j not in triple,'valid nonactive inequality row')

def verify_bounded(model):
    P,t,rows=(model[k] for k in ('P','t','rows'))
    w=c.refined_solve([[P[i][j] for i in c.QUAD[:3]] for j in range(3)],[-v for v in P[c.QUAD[3]]])
    require(all(x.v.l>0 for x in w),'strict positive spanning weights')
    for triple in combinations(c.QUAD,3):
        x=c.refined_solve([rows[i] for i in triple],[t]*3)
        require(all(max(abs(v.v.l),abs(v.v.h))<c.OUTER_BOUND*c.S for v in x),'strict outer coordinate bound10')

def verify_record(record,base,geometry,bounded):
    require(type(record)is list and len(record)>=2,'literal witness record')
    index,kind=record[:2]
    require(type(index)is int and 0<=index<364,'active triple index')
    triple=c.TRIPLES[index];t=base['t']
    if kind=='K':
        require(record==[c.CRITICAL,'K'],'exact critical147 import')
        return
    if kind in ('T','R'):
        labels,q,determinant=core_adjugate(triple,base)
        if kind=='T':
            require(len(record)==2,'core norm instruction arity')
            require((t**2*sum(q)-determinant).v.h<0,'core Gram norm below1')
        else:
            require(len(record)==3,'core residual instruction arity')
            j=record[2];row_index(j,triple);require(j<13,'core Gram residual targets a core row')
            residual=sum(qi*c.gram_product(base,c.LABELS[j],label) for qi,label in zip(q,labels))-determinant
            require(residual.v.l>0,'core Gram positive residual')
        return
    require(geometry is not None,'cut/Cramer witness has whole-box geometry')
    A,rhs=(geometry[k] for k in ('A','rhs'))
    if kind=='F':
        require(len(record)==2 and triple[-1]!=13,'core Gram cut residual instruction')
        labels,q,determinant=core_adjugate(triple,base)
        residual=t*sum(qi*c.normal_product(geometry,label) for qi,label in zip(q,labels))-c.RHO*geometry['length']*determinant
        require(residual.v.l>0,'core Gram cut inequality strictly violated')
        return
    if kind=='G':
        require(len(record)==2 and triple[-1]==13,'cut Gram norm instruction')
        a,b=(c.LABELS[j] for j in triple[:2]);P,n=(geometry[k] for k in ('P','n'))
        s=c.gram_product(geometry,a,b)
        delta=1-s*s;require(delta.v.l>0,'cut Gram positive delta')
        def product(j):return c.normal_product(geometry,j)
        na,nb=product(a),product(b)
        perpendicular=geometry['nn']-(na*na+nb*nb-2*s*na*nb)/delta
        require(perpendicular.v.l>0,'cut Gram positive perpendicular norm')
        height=c.RHO*geometry['length']-t*(na+nb)/(1+s)
        norm=2*t*t/(1+s)+height*height/perpendicular
        require(norm.v.h<c.S,'cut Gram norm below1')
        return
    C,D=c.cm([A[j] for j in triple],[rhs[j] for j in triple])
    ds=c.sign(D.v)
    if kind=='C':
        require(len(record)==3 and bounded,'coordinate witness with boundedness premise')
        j=record[2];require(type(j)is int and 0<=j<3,'coordinate index')
        v=C[j].v
        require(c.sign(v)!=0 and min(abs(v.l),abs(v.h))>c.OUTER_BOUND*max(abs(D.v.l),abs(D.v.h)),
                'Cramer coordinate lies outside bound10 for every nonzero determinant')
    elif kind=='N':
        require(len(record)==2 and ds!=0,'direct norm with nonsingular whole-box matrix')
        x=[v/D for v in C]
        require(c.m.dot(x,x,t).v.h<c.S,'direct norm below1')
    elif kind=='H':
        require(len(record)==4,'homogeneous instruction arity')
        wp,wn=record[2:]
        require(ds<0 or wp is not None,'positive determinant regime is covered')
        require(ds>0 or wn is not None,'negative determinant regime is covered')
        # A narrower enclosure can make an old regime unnecessary. Check
        # every present literal anyway; do not weaken a required regime.
        if wp is not None:
            row_index(wp,triple)
            require((c.edot(A[wp],C)-rhs[wp]*D).v.l>0,'positive determinant regime residual')
        if wn is not None:
            row_index(wn,triple)
            require((c.edot(A[wn],C)-rhs[wn]*D).v.h<0,'negative determinant regime residual')
    else:raise ValueError('unknown literal witness opcode')

def shape(plan,complete=False):
    nodes=plan['nodes'];seen=set();open_nodes=[];areas=Counter();maxdepth=0
    def walk(index,incoming,inherited,cell):
        nonlocal maxdepth
        require(type(index)is int and 0<=index<len(nodes) and index not in seen,'reachable distinct node')
        seen.add(index);n=nodes[index]
        require(n['cell']==cell and n['bounded_inherited']==inherited,'literal cell/boundedness inheritance')
        td,ti,zd,zi=cell;maxdepth=max(maxdepth,td+zd)
        require(td+zd<=22,'unchanged depth22 guard')
        proofs=n['proofs'];proved=[row[0] for row in proofs]
        require(len(proved)==len(set(proved)) and set(proved)<=set(incoming),'distinct inherited active triples')
        expected=[j for j in incoming if j not in set(proved)]
        require(n['remaining']==expected,'exact outstanding obligation list')
        require(sum(k in n for k in ('split','prune','complete'))<=1,'exclusive node status')
        if 'split' in n:
            axis=n['split'];require(axis in ('t','z'),'split axis')
            cells=([td+1,2*ti,zd,zi],[td+1,2*ti+1,zd,zi]) if axis=='t' else ([td,ti,zd+1,2*zi],[td,ti,zd+1,2*zi+1])
            require(len(n['children'])==2,'both closed children are present')
            for child,b in zip(n['children'],cells):walk(child,expected,inherited or n['bounded'],b)
        elif 'prune' in n:areas['packing_pruned']+=Q(1,2**(td+zd))
        elif n.get('complete'):
            require(not expected and (inherited or n['bounded']),'all364 triples and boundedness at extension leaf')
            areas['extension']+=Q(1,2**(td+zd))
        else:open_nodes.append(index);areas['unresolved']+=Q(1,2**(td+zd))
    walk(0,list(range(364)),False,[0,0,0,0])
    require(len(seen)==len(nodes),'no unattached nodes')
    require(set(open_nodes)==set(plan['stack']) and len(open_nodes)==len(plan['stack']),'saved frontier equals unresolved leaves')
    require(sum(areas.values())==1,'exact closed rectangle coverage')
    require(not complete or not open_nodes,'complete theorem requires no unresolved cell')
    return dict(node_count=len(nodes),pending_nodes=open_nodes,maximum_depth=maxdepth,
                normalized_rectangle_areas={k:str(v) for k,v in areas.items()})

def replay(plan,complete=False,progress=None):
    out=shape(plan,complete);counts=Counter();bounded_count=0;pruned_count=0;regular_count=0
    started=time.monotonic();last=started
    for index,n in enumerate(plan['nodes']):
        proofs=n['proofs']
        needed=proofs or n['bounded'] or n.get('complete') or 'prune' in n
        if needed:
            P,t,raw=c.m.enclosed(*c.box(*n['cell']));base=dict(P=P,t=t);regular_count+=1
            geo=None
            if n['bounded'] or n.get('complete') or any(row[1] in ('C','G','H','N','F') for row in proofs):
                geo=c.geometry(P,t);geo['products']=base.setdefault('products',{})
            if n['bounded']:verify_bounded(geo);bounded_count+=1
            if 'prune' in n:
                row=n['prune']
                require(type(row)is list and len(row)==3 and row[0]=='pair' and tuple(row[1:]) in c.m.e.PAIRS,'literal packing pair witness')
                require(c.m.pair_gap(P,t,tuple(row[1:])).v.l>0,'packing pair strictly exceeds t')
                pruned_count+=1
            for row in proofs:
                verify_record(row,base,geo,n['bounded_inherited'] or n['bounded']);counts[row[1]]+=1
        if progress is not None and time.monotonic()-last>5:
            progress(dict(status='REPLAY_RUNNING',last_node=index,checked_witnesses=sum(counts.values()),seconds=round(time.monotonic()-started,3)))
            last=time.monotonic()
    margin=2*c.RHO**2-1
    require(margin>Q(593,1000),'exact cap capacity margin')
    out.update(status='CHECKED_COMPLETE_AUTHOR_G22_CAP_COVER' if complete else 'CHECKED_PARTIAL_AUTHOR_WITNESSES_NOT_FULL_THEOREM',
        agent='six-tammes-2',role='researcher',regular_nodes=regular_count,bounded_nodes=bounded_count,
        packing_witnesses=pruned_count,witness_count=sum(counts.values()),witness_counts=dict(counts),
        frozen_model_sha256=MODEL_HASH,public_model_sha256=PUBLIC_HASH,enclosure_version='v2',cap_pair_lower_bound=str(margin),
        imported_critical_lemma='bafkreif3recyji2krueruwtszh6v7gjdnktl64mmmifpla6xhlw5in6ate',
        trust_boundary='same-author literal replay sharing pinned interval kernel and model; no independent review')
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('plan');parser.add_argument('--require-complete',action='store_true')
    parser.add_argument('--receipt',default='scratch/g22-cap-replay-report.json');args=parser.parse_args()
    started=time.monotonic();source=Path(args.plan);plan=json.loads(source.read_text())
    def progress(out):Path('scratch/g22-cap-replay-progress.json').write_text(json.dumps(out,indent=2)+'\n')
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('160-second replay guard; incomplete')))
    signal.alarm(160)
    try:
        out=replay(plan,args.require_complete,progress)
        out['plan_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
        out['seconds']=round(time.monotonic()-started,3)
    except Exception as exc:
        out=dict(status='REPLAY_FAILED_OR_INCOMPLETE',error_type=type(exc).__name__,reason=str(exc),seconds=round(time.monotonic()-started,3))
        Path(args.receipt).write_text(json.dumps(out,indent=2)+'\n');progress(out);raise
    finally:signal.alarm(0)
    Path(args.receipt).write_text(json.dumps(out,indent=2)+'\n');progress(out)
    print(json.dumps(out,indent=2))
