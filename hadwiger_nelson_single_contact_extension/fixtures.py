"""Exact geometric and algorithm controls; finite fixtures are not placement coverage."""
import argparse,json,time
from itertools import combinations,product
from pathlib import Path
from colour import colour,graph

def need(x,msg):
    if not x:raise ValueError(msg)

# Coordinates are integer four-tuples in 1,sqrt3,sqrt7,sqrt21, divided by 2.
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))
def times(x,y):
    z=[0]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            z[i^j]+=a*b*(3 if i&j&1 else 1)*(7 if i&j&2 else 1)
    return tuple(z)
def pplus(x,y):return plus(x[0],y[0]),plus(x[1],y[1])
def distance4(p,q):return plus(times(minus(p[0],q[0]),minus(p[0],q[0])),times(minus(p[1],q[1]),minus(p[1],q[1])))
ZERO=(0,0,0,0)

def run():
    q=[(ZERO,ZERO),((2,0,0,0),ZERO),((1,0,0,0),(0,1,0,0))]
    t=[(ZERO,ZERO),((0,0,2,0),ZERO),((0,0,1,0),(0,0,0,1))]
    ps=[pplus(a,b) for a in q for b in t];sets=[list(range(3*i,3*i+3)) for i in range(3)]
    cases=[('prism',ps,sets),('coincident_terminal_sets',t,[[0,1,2]]*3)]
    geometry_pairs=terminal_pairs=choices=colour_runs=0;results=[]
    for name,points,terminals in cases:
        need(len(set(points))==len(points),'duplicate labelled fixture point')
        edges=[]
        for i,j in combinations(range(len(points)),2):
            geometry_pairs+=1
            if distance4(points[i],points[j])==(4,0,0,0):edges.append((i,j))
        for tri in terminals:
            for i,j in combinations(tri,2):
                need(distance4(points[i],points[j])==(28,0,0,0),'not equilateral sqrt7');terminal_pairs+=1
        max_degree=0;cubic_orders=set()
        for selected in product(*(list(combinations(tri,2)) for tri in terminals)):
            choices+=1;aux=sorted(set(edges)|{tuple(sorted(e)) for e in selected});adj=graph(len(points),aux)
            for v in range(len(points)):
                multiplicity=sum(v in tri for tri in terminals)
                unit_degree=sum(v in e for e in edges)
                need(unit_degree<=3-multiplicity,'separation bound failed')
                need(len(adj[v])<=3,'auxiliary degree failed');max_degree=max(max_degree,len(adj[v]))
            seen=set()
            for seed in range(len(points)):
                if seed in seen:continue
                component={seed};todo=[seed]
                for u in todo:
                    for v in adj[u]-component:component.add(v);todo.append(v)
                seen|=component
                if all(len(adj[v])==3 for v in component):cubic_orders.add(len(component))
            for f in [[0]*len(points),[1]*len(points),[i%4 for i in range(len(points))],[(i*i+2*i+1)%4 for i in range(len(points))]]:
                cs=colour(len(points),aux,f);colour_runs+=1
                need(all(cs[i]!=cs[j] for i,j in edges),'fixture unit edge failed')
                need(all(len({cs[i] for i in tri})>1 for tri in terminals),'monochromatic terminals')
        results.append({'fixture':name,'points':len(points),'unit_edges':len(edges),'maximum_auxiliary_degree':max_degree,'cubic_component_orders':sorted(cubic_orders)})
    need(results[0]['unit_edges']==9 and results[0]['cubic_component_orders']==[6],'prism fixture missing')
    greedy_cases=[(4,[(0,1),(1,2),(2,3)]),(5,[(i,(i+1)%5) for i in range(5)]),
                  (4,[e for e in combinations(range(4),2) if e!=(2,3)]),(2,[])]
    greedy_profiles=0
    for n,edges in greedy_cases:
        for f in product(range(4),repeat=n):colour(n,edges,f);greedy_profiles+=1
    reject=[(4,list(combinations(range(4),2)),[0]*4),(5,[(0,i) for i in range(1,5)],[0]*5),
            (1,[],[4]),(8,[(i,j) for i,j in combinations(range(8),2) if (i^j) in (1,2,4)],[0]*8)]
    for n,edges,f in reject:
        try:colour(n,edges,f)
        except ValueError:pass
        else:raise ValueError('invalid theorem premise accepted')
    return {'fixtures':results,'exact_fixture_pair_norms':geometry_pairs,'terminal_distance_checks':terminal_pairs,
            'selected_pair_cases':choices,'geometric_list_runs':colour_runs,'noncubic_list_profiles':greedy_profiles,
            'invalid_input_rejections':len(reject),'status':'PASS'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();start=time.monotonic();r=run()
    Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({**r,'seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':main()
