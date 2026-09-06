"""Exact local-piece and shared-degree obstruction checker; no solver imports."""
import argparse
import copy
import hashlib
import itertools as it
import json
from pathlib import Path


def need(ok,text):
    if not ok:raise ValueError(text)


def parse(g,n):
    need(type(g) is dict and set(g)=={'n','red_edges'},'schema')
    need(type(g['n']) is int and g['n']==n,'order')
    es=g['red_edges'];need(type(es) is list,'edges')
    for e in es:
        need(type(e) is list and len(e)==2 and all(type(x) is int for x in e),'pair schema')
        need(0<=e[0]<e[1]<n,'pair range/order')
    red={tuple(e) for e in es}
    need(es==[list(e) for e in sorted(red)],'canonical unique edges')
    return red


def rows_for(n,edges):
    rows=[0]*n
    for u,v in edges:rows[u]|=1<<v;rows[v]|=1<<u
    return rows


def bit_cliques(rows,candidates,k,prefix=0):
    if not k:
        yield prefix;return
    while candidates.bit_count()>=k:
        low=candidates&-candidates;candidates^=low
        yield from bit_cliques(rows,candidates&rows[low.bit_length()-1],k-1,prefix|low)


def literal_cliques(n,edges,k):
    return sorted(sum(1<<v for v in q) for q in it.combinations(range(n),k)
                  if all(e in edges for e in it.combinations(q,2)))


def compare_cliques(n,edges,k):
    direct=literal_cliques(n,edges,k)
    packed=sorted(bit_cliques(rows_for(n,edges),(1<<n)-1,k))
    need(direct==packed,'clique-list comparison')
    return direct


def audit(H,Q0,Q1,density):
    h=parse(H,20);need(len(h)==density and density in (92,93),'H density')
    hblue=set(it.combinations(range(20),2))-h
    need(sum(1<<b for b,e in enumerate(it.combinations(range(2,10),2)) if e in hblue)==5388912,'W mask')
    N=[{w for w in range(20) if tuple(sorted((v,w))) in h} for v in range(20)]
    need(N[0]=={10,11,12,13,18,19} and N[1]=={14,15,16,17,18,19},'H marked neighborhoods')
    need(not compare_cliques(20,h,4) and not compare_cliques(20,hblue,5),'H Ramsey conditions')
    fixed={e:e in h for e in it.combinations(range(20),2)}
    # Literal union: H0..19, X20..28, Y29..37, central root38.
    def insert(u,v,color):
        e=tuple(sorted((u,v)))
        need(u!=v and (e not in fixed or fixed[e]==color),'overlap consistency')
        fixed[e]=color
    pieces=[];contributions=[];all_details=[]
    for anchor,g in enumerate((Q0,Q1)):
        q=parse(g,22);need(len(q)==124,'Q red density')
        qb=set(it.combinations(range(22),2))-q
        core=[v for v in range(20) if v!=anchor and v not in N[anchor]]
        need(len(core)==13,'core size')
        need(all(((u,v) in q)==(tuple(sorted((core[u],core[v]))) in h)
                 for u,v in it.combinations(range(13),2)),'Q fixed core')
        other=core.index(1-anchor)
        need(all(tuple(sorted((other,v))) in q for v in range(13,22)),'Q marked links')
        need(not compare_cliques(22,q,5) and not compare_cliques(22,qb,4),'Q Ramsey conditions')
        details={'red_K4_masks':compare_cliques(22,q,4),
                 'blue_triangle_masks':compare_cliques(22,qb,3)}
        all_details.append(details)
        # The blue cone is also checked literally and by bit recursion.
        cone_red=q;cone_blue=qb|{(v,22) for v in range(22)}
        need(not compare_cliques(23,cone_red,5) and not compare_cliques(23,cone_blue,5),'Q blue cone')
        group=list(range(20+9*anchor,29+9*anchor))
        mapping=core+group
        for u,v in it.combinations(range(22),2):insert(mapping[u],mapping[v],(u,v) in q)
        for v in group:insert(anchor,v,False)
        counts={v:sum(tuple(sorted((core.index(v),w))) in q for w in range(13,22)) for v in core}
        contributions.append(counts)
        pieces.append(dict(anchor=anchor,core_H_labels=core,Q_degrees=[r.bit_count() for r in rows_for(22,q)],
                           Q_red_edges=124,Q_blue_edges=107,other_mark_Q_degree=sum(other in e for e in q),
                           red_K5=0,blue_K4=0,cone_monochromatic_K5=0,
                           red_K4s=len(details['red_K4_masks']),blue_triangles=len(details['blue_triangle_masks']),
                           clique_lists_sha256=hashlib.sha256(json.dumps(details,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
        need(pieces[-1]['other_mark_Q_degree']==13,'other mark degree')
    for v in range(38):insert(v,38,v<20)
    need(len(fixed)==552,'fixed-pair union size')
    reds={e for e,c in fixed.items() if c};blues={e for e,c in fixed.items() if not c}
    # A missing pair is neither red nor blue: no invented completion.
    need(not compare_cliques(39,reds,5) and not compare_cliques(39,blues,5),'fixed monochromatic K5')
    degrees=[sum(v in e for e in reds) for v in range(39)]
    need(degrees==[row.bit_count() for row in rows_for(39,reds)],'literal/bit degree comparison')
    W=[];overloads=[]
    for v in range(2,10):
        x,y=contributions[0][v],contributions[1][v]
        need(all(tuple(sorted((v,w))) in fixed for w in range(39) if v!=w),'W star not fully colored')
        need(degrees[v]==1+len(N[v])+x+y,'two degree calculations')
        residual=21-degrees[v]
        row=dict(H_vertex=v,H_degree=len(N[v]),X_red=x,Y_red=y,
                 fixed_red_degree=degrees[v],required_from_future_RR4=residual)
        W.append(row)
        if residual<0 or residual>4:
            neighbors=sorted(w for w in range(39) if tuple(sorted((v,w))) in reds)
            overloads.append(dict(vertex=v,known_red_neighbors=neighbors,known_red_degree=len(neighbors),
                                  target_degree=21,required_from_future_RR4=residual))
    need(overloads,'no degree obstruction')
    need(all(r['known_red_degree']>21 for r in overloads),'expected overload witness')
    expected={92:[(3,23)],93:[(2,22),(6,23)]}[density]
    need([(r['vertex'],r['known_red_degree']) for r in overloads]==expected,'recorded obstruction')
    return dict(status='LOCAL_PIECES_PASS_BUT_THEIR_LITERAL_UNION_FAILS_TARGET_DEGREES',H_density=density,
                pieces=pieces,partial_order=39,fixed_pairs=552,uncolored_pairs=189,
                fixed_red_edges=len(reds),fixed_blue_edges=len(blues),fixed_monochromatic_K5=0,
                W_degree_rows=W,overloads=overloads,
                scope='chosen H and both chosen Q embeddings only; any new-vertex relabeling within X/Y preserves the degree obstruction; no whole-H or Ramsey43 exclusion'),all_details


def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--work',type=Path);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();results={}
    for d in (92,93):
        H=json.loads((a.directory/f'H{d}.json').read_text())
        Q=[json.loads(((a.work/f'{d}-{j}'/'graph.json') if a.work else (a.directory/f'Q{d}_{j}.json')).read_text()) for j in (0,1)]
        results[d]=audit(H,*Q,d)[0]
    with a.report.open('x') as f:json.dump(results,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(results),flush=True)


if __name__=='__main__':main()
