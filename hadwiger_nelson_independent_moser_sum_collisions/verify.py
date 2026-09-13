#!/usr/bin/env python3
"""Solver-free complete replay. All generated bulky objects remain in memory."""
import argparse,hashlib,json,sys
from pathlib import Path
from family import *
from local import f_local
from two_factor import rotations,cases,event_graph,event_phase
from geometry import Geometry,three_points,descend,proper
HERE=Path(__file__).resolve().parent

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def rejected(fn):
    try:fn()
    except ValueError:return
    raise ValueError('negative control accepted')

def run(library,certificate,audit):
    G=Geometry(library);cert=json.loads(Path(certificate).read_text());words=cert['words']
    require(cert['format']=='formal343-v1','certificate version')
    require(all(len(w)==343 and all(c in '0123' for c in w) for w in words),'certificate word syntax')
    M=spindle();me=[(i,j) for i,j in combinations(range(7),2) if norm(sub(M[i],M[j]))==ONE]
    require(not any(all(w[i]!=w[j] for i,j in me) for w in product(range(3),repeat=7)),'source is three-colourable')
    require(any(all(w[i]!=w[j] for i,j in me) for w in product(range(4),repeat=7)),'source lacks four-colouring')
    rejected(lambda:descend('4'*343,list(range(343)),343))
    rejected(lambda:descend('0'*342,list(range(343)),343))
    rejected(lambda:descend('01'+'0'*341,[0]*343,1))
    require(rotations()[1]==30 and len(rotations()[0])==16,'two-factor rotation count')
    data=enumerate_roots();fields=[tuple(map(F,s)) for s in data['fields']]
    require(len(cert['three'])==len(data['roots'])==6528,'three-factor certificate coverage')
    cats=[]
    for s in fields:
        val,unit=f_local(s);cats.append({'valuation':val,'unit_mod8':unit,'Q2_square':val%2==0 and unit==1})
    counts=Counter();sizes=Counter();edge_sizes=Counter();pairs=0;threehash=hashlib.sha256()
    for i,(r,row) in enumerate(zip(data['roots'],cert['three'])):
        if cats[r['field']]['Q2_square']:
            require(row==-1,'local-field certificate tag');counts['local_field']+=1;continue
        require(isinstance(row,int) and 0<=row<len(words),'invalid three-factor row')
        pp,lm=three_points(r);require(len(pp)<343,'missing three-factor collision')
        es=G.graph(pp,fields[r['field']],audit);cc=descend(words[row],lm,len(pp));proper(cc,es)
        rejected(lambda:proper(['0']*len(pp),es))
        counts['explicit']+=1;sizes[len(pp)]+=1;edge_sizes[len(es)]+=1;pairs+=len(pp)*(len(pp)-1)//2
        threehash.update((str(i)+':'+digest(es)+'\n').encode())
        if counts['explicit']%500==0:print('three-factor checked',counts['explicit'],file=sys.stderr,flush=True)
    require(counts=={'local_field':3024,'explicit':3504},'three-factor census')
    two=[];twohash=hashlib.sha256();two_keys=[];two_pairs=0;groups_total=0
    require(len(cert['two'])==16,'two-factor case coverage')
    for k,(u,B,Db,Dm,base,groups,stats) in enumerate(cases()):
        ix={p:i for i,p in enumerate(B)}
        lm=[7*ix[add(a,mul(u,b))]+j for a,b in product(M,repeat=2) for j in range(7)]
        require(len(groups)==len(cert['two'][k]),'two-factor group coverage')
        eh=Counter()
        for gi,((key,g),row) in enumerate(zip(groups,cert['two'][k])):
            require(isinstance(row,int) and 0<=row<len(words),'invalid two-factor row')
            es=event_graph(Db,Dm,base,g);v=event_phase(key,g)
            vm=[ecscale(v,m) for m in M]
            pts=[(add(a,w[0]),w[1]) for a,w in product(B,vm)]
            require(len(set(pts))==len(pts),'outside-E two-factor collision')
            actual=G.graph(pts,g['ss'],audit)
            require(actual==es,'event-polynomial/physical-edge disagreement')
            cc=descend(words[row],lm,len(pts));proper(cc,actual)
            rejected(lambda:proper(['0']*len(pts),actual))
            twohash.update((str(k)+','+str(gi)+':'+digest(actual)+'\n').encode())
            two_keys.append([[str(z) for z in u],[[str(z) for z in p] for p in key]])
            eh[len(es)]+=1;two_pairs+=len(pts)*(len(pts)-1)//2;groups_total+=1
        two.append({'B_vertices':len(B),'sum_vertices':len(B)*7,'groups':len(groups),'filters':stats,'edge_counts':dict(eh)})
        print('two-factor checked',k+1,'/16',file=sys.stderr,flush=True)
    require(groups_total==5064,'two-factor exceptional group total')
    return {'claim':'Every noninjective M+uM+vM is four-chromatic for unit complex u,v',
            'source_vertices':7,'source_edges':len(me),'certificate_words':len(words),'certificate_sha256':hashlib.sha256(Path(certificate).read_bytes()).hexdigest(),
            'three_factor':{'census':data['summary'],'complete_root_inventory_sha256':digest(data),'fields':cats,'checked':dict(counts),'vertex_counts':dict(sizes),'edge_counts':dict(edge_sizes),'audited_unordered_pairs':pairs,'edge_stream_sha256':threehash.hexdigest()},
            'two_factor':{'unit_rotations':30,'conjugation_representatives':16,'groups':groups_total,'physical_roots':2*groups_total,'cases':two,'complete_quadratic_inventory_sha256':digest(two_keys),'audited_unordered_pairs':two_pairs,'edge_stream_sha256':twohash.hexdigest()},
            'negative_controls':{'malformed_words':2,'collision_disagreement':1,'constant_colour_rejections':counts['explicit']+groups_total},'record_improvement':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--library',required=True);p.add_argument('--certificate',default=str(HERE/'certificate.json'));p.add_argument('--skip-real-audit',action='store_true');a=p.parse_args()
    print(json.dumps(run(a.library,a.certificate,not a.skip_real_audit),sort_keys=True,indent=2))
