"""Exhaustive small-graph ball controls and certificate corruption checks."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import generate
import verify

HERE=Path(__file__).resolve().parent

def small_graphs():
    graphs=cases=0
    for n in range(1,6):
        possible=list(combinations(range(n),2))
        for mask in range(1<<len(possible)):
            adj=[set() for _ in range(n)];dist=[[0 if i==j else n+1 for j in range(n)] for i in range(n)]
            for i,(u,v) in enumerate(possible):
                if mask>>i&1:adj[u].add(v);adj[v].add(u);dist[u][v]=dist[v][u]=1
            for k in range(n):
                for i in range(n):
                    for j in range(n):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
            for limit in range(1,n+1):
                all_sets={sum(1<<v for v in range(n) if dist[u][v]<=r) for u in range(n) for r in range(n)}
                valid={b for b in all_sets if b.bit_count()<=limit}
                expected={a for a in valid if not any(a!=b and a&b==a for b in valid)}
                _,actual=generate.maximal_balls(adj,limit)
                verify.require(set(actual)==expected,'small-graph maximal ball family');cases+=1
            graphs+=1
    return graphs,cases


def main():
    graphs,cases=small_graphs();edges,adj=verify.load();word_text=(HERE/'half_colourings.txt').read_text();words,half_edges=verify.check_halves(edges,word_text)
    maxima,radii,orders,all_sets,count=verify.enumerate_family(adj);cert=json.loads((HERE/'certificate.json').read_text());rejected=[]
    def bad(name,operation):
        try:operation()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise ValueError('accepted malformed input: '+name)
    def mutated(name,mutation):
        data=deepcopy(cert);mutation(data)
        bad(name,lambda:verify.check_recipes(data,edges,words,half_edges,maxima,radii))
    bad('missing half word',lambda:verify.check_halves(edges,'\n'.join(word_text.splitlines()[:-1])+'\n'))
    bad('invalid colour symbol',lambda:verify.check_halves(edges,'x'+word_text[1:]))
    text=list(word_text);u,v=min(e for e in half_edges if e[0]!=0);text[u]=text[v]
    bad('monochromatic half edge',lambda:verify.check_halves(edges,''.join(text)))
    bad('missing strict host edge',lambda:verify.check_halves(edges[:-1],word_text))
    mutated('wrong target',lambda c:c.update(limit=507))
    mutated('wrong version',lambda c:c.update(version=2))
    mutated('missing maximal ball',lambda c:c['recipes'].pop())
    mutated('duplicate centre',lambda c:c['recipes'].append(c['recipes'][0]))
    mutated('incorrect radius',lambda c:c['recipes'][0].__setitem__(1,c['recipes'][0][1]+1))
    mutated('centre out of range',lambda c:c['recipes'][0].__setitem__(0,2131))
    mutated('word index out of range',lambda c:c['recipes'][0].__setitem__(2,16))
    mutated('swap colour out of range',lambda c:c['recipes'][0].__setitem__(3,4))
    index=next(i for i,row in enumerate(cert['recipes']) if maxima[row[0]]&1)
    wrong_perm=next(i for i,perm in enumerate(verify.PERMS) if perm[0]!=0)
    mutated('shared vertex disagreement',lambda c:c['recipes'][index].__setitem__(6,wrong_perm))
    print(json.dumps({'all_checks_passed':True,'simple_graphs':graphs,'graph_and_limit_cases':cases,
                      'malformed_inputs_rejected':len(rejected),'rejections':rejected},indent=2,sort_keys=True))

if __name__=='__main__':main()
