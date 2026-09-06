"""Definition-level certificate checker, independent of encoding and solver."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def parse(data,n):
    need(type(data) is dict and set(data)=={'n','red_edges'},'graph schema')
    need(type(data['n']) is int and data['n']==n,'graph order')
    es=data['red_edges'];need(type(es) is list,'edge list')
    for e in es:
        need(type(e) is list and len(e)==2 and all(type(v) is int for v in e),'edge schema')
        need(0<=e[0]<e[1]<n,'edge range/order')
    red={tuple(e) for e in es}
    need(es==[list(e) for e in sorted(red)],'canonical unique edges')
    return red

def bit_rows(vertices,edges):
    rows={v:0 for v in vertices}
    for u,v in edges:rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def bit_cliques(rows,candidates,k,prefix=0):
    if k==0:
        yield prefix;return
    while candidates.bit_count()>=k:
        bit=candidates&-candidates;candidates-=bit
        yield from bit_cliques(rows,candidates&rows[bit.bit_length()-1],k-1,prefix|bit)

def compare(vertices,edges,k):
    # Literal subset membership and recursive common-neighborhood intersection.
    direct=sorted(sum(1<<v for v in s) for s in it.combinations(vertices,k)
                  if all(e in edges for e in it.combinations(s,2)))
    packed=sorted(bit_cliques(bit_rows(vertices,edges),sum(1<<v for v in vertices),k))
    need(direct==packed,'complete clique-list comparison')
    return direct

def subedges(vertices,edges):
    vs=set(vertices);return {e for e in edges if set(e)<=vs}

def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def audit(H,G,density,full=True):
    h=parse(H,20);r=parse(G,43)
    need(len(h)==density and density in (92,93),'H density')
    need(subedges(range(20),r)==h,'fixed H')
    hb=set(it.combinations(range(20),2))-h
    need(sum(1<<i for i,e in enumerate(it.combinations(range(2,10),2)) if e in hb)==5388912,'W mask')
    hn=[{v for v in range(20) if tuple(sorted((v,u))) in h} for u in range(20)]
    need(hn[0]=={10,11,12,13,18,19} and hn[1]=={14,15,16,17,18,19},'H marked stars')
    vertices=list(range(43));allpairs=set(it.combinations(vertices,2));b=allpairs-r
    rn=[{v for v in vertices if tuple(sorted((v,u))) in r} for u in vertices]
    bn=[set(vertices)-{u}-rn[u] for u in vertices]
    degrees=[len(x) for x in rn]
    need(degrees==[20 if u in (0,1,38) else 21 for u in vertices],'target degree sequence')
    need(degrees==[row.bit_count() for row in bit_rows(vertices,r).values()],'degree crosscheck')
    need(rn[38]==set(range(20)),'central star')
    X=set(range(20,29));Y=set(range(29,38));Z=set(range(39,43))
    need(rn[0]==hn[0]|Y|Z|{38} and rn[1]==hn[1]|X|Z|{38},'marked global stars')
    need(len(r)==450,'whole red edge total')
    # A faster mode only supports malformed-certificate controls, not a report.
    def cliques(vs,es,k):
        vs=sorted(vs)
        return compare(vs,es,k) if full else sorted(bit_cliques(bit_rows(vs,es),sum(1<<v for v in vs),k))
    need(not cliques(range(20),h,4) and not cliques(range(20),hb,5),'H Ramsey conditions')
    Q=[];pieces=[];details={}
    partial=set(it.combinations(range(20),2))|{(u,38) for u in range(38)}
    for a in (0,1):
        q=sorted(bn[a]);expected=(set(range(20))-{a}-hn[a])|(X if a==0 else Y)
        need(set(q)==expected and len(q)==22,'actual blue neighborhood')
        qr=subedges(q,r);qb=subedges(q,b)
        need(len(qr)==124 and len(qb)==107,'Q density')
        need(not cliques(q,qr,5) and not cliques(q,qb,4),'Q Ramsey conditions')
        details[str(a)]={'red_K4':cliques(q,qr,4),'blue_K3':cliques(q,qb,3)}
        pieces.append(dict(anchor=a,global_labels=q,red_edges=len(qr),blue_edges=len(qb),
                           red_K4s=len(details[str(a)]['red_K4']),blue_K3s=len(details[str(a)]['blue_K3'])))
        Q.append(q);partial|=set(it.combinations(q,2))
        partial|={tuple(sorted((a,v))) for v in (X if a==0 else Y)}
    need(len(partial)==552,'partial union size')
    pr=r&partial;pb=b&partial
    need(not cliques(range(39),pr,5) and not cliques(range(39),pb,5),'partial fixed K5')
    W=[]
    for w in range(2,10):
        x=len(rn[w]&X);y=len(rn[w]&Y);z=len(rn[w]&Z)
        need(len(hn[w])+x+y+z+1==21,'W degree decomposition')
        need(z==20-len(hn[w])-x-y and 0<=z<=4,'W residual interface')
        W.append(dict(vertex=w,H_degree=len(hn[w]),X_red=x,Y_red=y,Z_red=z,
                      fixed_partial_red_degree=21-z,Z_red_neighbors=sorted(rn[w]&Z)))
    if not full:return {'status':'FAST_CONTROL_ONLY'}
    profiles=[]
    for v in (0,1,38):
        p=len(subedges(rn[v],r));t=len(subedges(bn[v],b))
        profiles.append(dict(vertex=v,degree=degrees[v],red_neighborhood_red_edges=p,
                             blue_neighborhood_blue_edges=t))
    need([(x['red_neighborhood_red_edges'],x['blue_neighborhood_blue_edges']) for x in profiles]==
         [(93,107),(93,107),(density,199-density)],'exceptional cap identities')
    K={color:cliques(vertices,es,5) for color,es in (('red',r),('blue',b))}
    need(K['red'] or K['blue'],'potential target found: stop for full independent certification')
    byroots={color:{str(v):sum(bool(mask&(1<<v)) for mask in masks) for v in (0,1,38)} for color,masks in K.items()}
    need(byroots['red']['38']==0 and byroots['blue']['0']==byroots['blue']['1']==0,'cone constraints')
    # Exact partition by memberships in the three exceptional roots, not disjoint degrees.
    root_masks={color:[sum(sum(bool(mask&(1<<v))<<i for i,v in enumerate((0,1,38)))==j for mask in masks)
                       for j in range(8)] for color,masks in K.items()}
    return dict(status='JOINT_LOCAL_NEIGHBORHOODS_AND_FULL_DEGREES_REALIZED_NOT_RAMSEY43',
                H_density=density,n=43,red_edges=len(r),blue_edges=len(b),degrees=degrees,
                pieces=pieces,exceptional_profiles=profiles,W_rows=W,
                partial_order=39,partial_colored_pairs=len(partial),partial_red_edges=len(pr),
                partial_blue_edges=len(pb),partial_monochromatic_K5=0,
                completed_pairs=903-len(partial),local_clique_lists_sha256=digest(details),
                monochromatic_K5_counts={c:len(s) for c,s in K.items()},
                monochromatic_K5_by_exceptional_root=byroots,
                monochromatic_K5_root_membership_mask_counts=root_masks,
                monochromatic_K5_lists_sha256=digest(K),
                first_K5={c:[v for v in vertices if masks[0]&(1<<v)] if masks else None for c,masks in K.items()},
                scope='one displayed complete graph at the indicated fixed H; no full Ramsey or family-exclusion claim')

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--work',type=Path);p.add_argument('--report',type=Path,required=True)
    p.add_argument('--density',type=int,nargs='+',choices=(92,93),default=[92])
    a=p.parse_args();results={}
    for d in a.density:
        hpath=a.directory/f'H{d}.json';gpath=a.work/str(d)/'graph.json' if a.work else a.directory/f'G{d}.json'
        result=audit(json.loads(hpath.read_text()),json.loads(gpath.read_text()),d)
        result.update(H_sha256=hashlib.sha256(hpath.read_bytes()).hexdigest(),graph_sha256=hashlib.sha256(gpath.read_bytes()).hexdigest())
        results[str(d)]=result
    with a.report.open('x') as f:json.dump(results,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({d:{k:v[k] for k in ('status','monochromatic_K5_counts','W_rows')} for d,v in results.items()}),flush=True)

if __name__=='__main__':main()
