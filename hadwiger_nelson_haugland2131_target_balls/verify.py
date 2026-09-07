"""Independent graph-distance and positive-colouring verifier; no producer imports."""
import argparse
from collections import Counter,deque
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PERMS=tuple(permutations(range(4)))
N=2131
HALF=1066


def require(ok,message):
    if not ok:raise ValueError(message)


def load():
    plan=json.loads((HERE/'inputs.json').read_text());raw=(HERE.parent/plan['graph_file']).read_bytes()
    require(sha256(raw).hexdigest()==plan['graph_sha256'],'graph input hash')
    edges=[tuple(e) for e in json.loads(raw)['G3_edges']]
    require(len(edges)==12530 and edges==sorted(set(edges)),'edge census')
    require(all(0<=u<v<N for u,v in edges),'edge range')
    digest=sha256(''.join(f'{u} {v}\n' for u,v in edges).encode()).hexdigest()
    require(digest==plan['strict_edge_sha256'],'strict source edge hash')
    require(plan['limit']==508 and plan['vertices']==N and plan['edges']==len(edges),'problem parameters')
    adj=[[] for _ in range(N)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    return edges,adj


def check_halves(edges,word_text):
    left={(u,v) for u,v in edges if v<HALF}
    image=lambda v:0 if v==0 else v+1065
    right={tuple(sorted((image(u),image(v)))) for u,v in left}
    bridges={(303,1368),(435,1500)}
    require(len(left)==len(right)==6264 and not left&right,'half edge counts')
    require(left|right|bridges==set(edges),'complete two-bridge decomposition')
    lines=word_text.splitlines();require(len(lines)==16,'half word count')
    require(all(len(w)==HALF and set(w)<=set('0123') for w in lines),'half word format')
    words=[list(map(int,w)) for w in lines]
    require(len({tuple(w) for w in words})==16,'distinct half words')
    for word in words:
        require(word[0]==0,'common-vertex colour normalization')
        require(all(word[u]!=word[v] for u,v in left),'proper full-half colouring')
    return words,left


def enumerate_family(adj):
    # Full BFS from every vertex, independent of the producer's truncated layers.
    all_sets=set();maxima=[];radii=[];orders=[];admissible_count=0
    for root in range(N):
        distance=[-1]*N;distance[root]=0;queue=deque([root])
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                if distance[v]<0:distance[v]=distance[u]+1;queue.append(v)
        require(all(d>=0 for d in distance),'connected host')
        layers=[0]*(max(distance)+1)
        for v,d in enumerate(distance):layers[d]|=1<<v
        mask=0;last=0;radius=-1
        for r,layer in enumerate(layers):
            mask|=layer
            if mask.bit_count()>508:break
            last=mask;radius=r;all_sets.add(mask);admissible_count+=1
        require(radius>=0,'admissible radius exists')
        maxima.append(last);radii.append(radius);orders.append(last.bit_count())
    return maxima,radii,orders,all_sets,admissible_count


def swap_components(vertices,word,colour,half_adj):
    result={v:word[v] for v in vertices}
    if colour==0:return result
    remaining={v for v in vertices if word[v] in (0,colour)}
    while remaining:
        root=min(remaining);component={root};queue=deque([root]);remaining.remove(root)
        while queue:
            u=queue.popleft()
            for v in half_adj[u]:
                if v in remaining:remaining.remove(v);component.add(v);queue.append(v)
        if 0 not in component:
            for v in component:result[v]=colour-result[v]
    return result


def colour_recipe(row,mask,words,half_adj):
    require(len(row)==7 and all(type(x)==int for x in row),'recipe format')
    root,r,wl,cl,wr,cr,pi=row
    require(0<=wl<16 and 0<=wr<16 and 0<=cl<4 and 0<=cr<4 and 0<=pi<24,'recipe range')
    support={v for v in range(N) if mask>>v&1}
    ls={v for v in support if v<HALF}
    rs={0 if v==0 else v-1065 for v in support if v==0 or v>=HALF}
    left=swap_components(ls,words[wl],cl,half_adj)
    right=swap_components(rs,words[wr],cr,half_adj)
    perm=PERMS[pi]
    if 0 in support:require(left[0]==perm[right[0]],'shared vertex agrees')
    colour=dict(left)
    for v,c in right.items():colour[0 if v==0 else v+1065]=perm[c]
    require(set(colour)==support and all(0<=c<4 for c in colour.values()),'complete proper palette')
    return colour


def check_recipes(cert,edges,words,half_edges,maxima,radii):
    require(cert['version']==1 and cert['limit']==508,'certificate version and target')
    half_adj=[[] for _ in range(HALF)]
    for u,v in half_edges:half_adj[u].append(v);half_adj[v].append(u)
    masks=[];centres=set();edge_checks=0;word_hash=sha256();sizes=[];recipe_radii=Counter()
    for row in cert['recipes']:
        require(len(row)==7 and all(type(x)==int for x in row),'recipe format')
        root,r=row[:2];require(0<=root<N and root not in centres,'unique recipe centre');centres.add(root)
        require(r==radii[root],'maximal admissible radius')
        mask=maxima[root];require(mask.bit_count()<=508,'target size');masks.append(mask);sizes.append(mask.bit_count());recipe_radii[r]+=1
        colour=colour_recipe(row,mask,words,half_adj)
        for u,v in edges:
            if u in colour and v in colour:
                require(colour[u]!=colour[v],'monochromatic induced edge');edge_checks+=1
        word_hash.update((str(root)+':'+','.join(f'{v}={colour[v]}' for v in sorted(colour))+'\n').encode())
    require(len(set(masks))==len(masks),'distinct certified balls')
    # Antichain + coverage proves that these are exactly the maximal sets.
    for i,a in enumerate(masks):
        for b in masks[i+1:]:require(a&b!=a and a&b!=b,'maximal-ball antichain')
    covering=[]
    for root,mask in enumerate(maxima):
        match=next((i for i,b in enumerate(masks) if mask&b==mask),None)
        require(match is not None,'uncovered centre');covering.append(match)
    return {'maximal_balls':len(masks),'maximal_ball_min_order':min(sizes),'maximal_ball_max_order':max(sizes),
            'maximal_ball_radius_histogram':dict(sorted(recipe_radii.items())),
            'induced_edge_checks':edge_checks,'decoded_colourings_sha256':word_hash.hexdigest(),
            'covering_map_sha256':sha256((json.dumps(covering,separators=(',',':'))+'\n').encode()).hexdigest()}


def verify(cert,word_text):
    edges,adj=load();words,half_edges=check_halves(edges,word_text)
    maxima,radii,orders,all_sets,admissible=enumerate_family(adj)
    result=check_recipes(cert,edges,words,half_edges,maxima,radii)
    result.update(verified=True,host_vertices=N,host_edges=len(edges),target=508,centres=N,
                  admissible_centre_radius_pairs=admissible,distinct_admissible_balls=len(all_sets),
                  distinct_maximal_radius_balls=len(set(maxima)),
                  maximal_admissible_radius_histogram=dict(sorted(Counter(radii).items())),
                  checked_full_half_words=len(words),full_half_edge_checks=len(words)*len(half_edges),
                  all_target_balls_four_colourable=True,all_subgraphs_of_target_balls_four_colourable=True,
                  arbitrary_target_subgraphs_classified=False,record_improvement=False,solver_required=False)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args()
    raw=args.certificate.read_bytes();text=(HERE/'half_colourings.txt').read_text();result=verify(json.loads(raw),text)
    result.update(certificate_bytes=len(raw),certificate_sha256=sha256(raw).hexdigest(),half_colourings_sha256=sha256(text.encode()).hexdigest())
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
