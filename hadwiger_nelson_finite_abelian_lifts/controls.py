#!/usr/bin/env python3
"""Fault injection and an independent small-group rhombus-matrix audit."""
import copy
import itertools
import json
from pathlib import Path
from verify import require,verify


def group_types(n,minimum=2):
    if n==1:yield ()
    for d in range(minimum,n+1):
        if n%d:continue
        for tail in group_types(n//d,d):
            if not tail or tail[0]%d==0:yield (d,)+tail


def small_groups():
    cases=admissible=obstructed=0;types=[]
    for n in range(2,13):
        for moduli in group_types(n):
            types.append(list(moduli))
            elements=list(itertools.product(*[range(m) for m in moduli]));zero=elements[0]
            add=lambda a,b:tuple((x+y)%m for x,y,m in zip(a,b,moduli))
            neg=lambda a:tuple(-x%m for x,m in zip(a,moduli))
            reps=[x for x in elements[1:] if x<=neg(x)]
            def span(gens):
                seen={zero};stack=[zero]
                while stack:
                    a=stack.pop()
                    for b in gens:
                        c=add(a,b)
                        if c not in seen:seen.add(c);stack.append(c)
                return seen
            for mask in range(1<<len(reps)):
                selected=[x for i,x in enumerate(reps) if mask>>i&1]
                independent=all(span([s]).intersection(span([t for t in selected if t!=s]))=={zero} for s in selected)
                S=set(selected)|{neg(s) for s in selected}
                # All graph four-cycles, without using the mixed-generator rule.
                adj=[{j for j,b in enumerate(elements) if add(b,neg(a)) in S} for a in elements]
                basis={};P=101
                def reduce(row):
                    for pivot,b in sorted(basis.items()):
                        c=row[pivot]
                        if c:row=[(x-c*y)%P for x,y in zip(row,b)]
                    return row
                for u,v in itertools.combinations(range(n),2):
                    for a,b in itertools.combinations(sorted(adj[u]&adj[v]),2):
                        row=[0]*n;row[u]+=1;row[v]+=1;row[a]-=1;row[b]-=1
                        row=reduce(row)
                        if any(row):
                            pivot=next(i for i,x in enumerate(row) if x)
                            c=pow(row[pivot],-1,P);basis[pivot]=[x*c%P for x in row]
                collision=False
                for u,v in itertools.combinations(range(n),2):
                    row=[0]*n;row[u]=1;row[v]=-1
                    if not any(reduce(row)):collision=True;break
                require(collision != independent,'small-group theorem/matrix mismatch')
                cases+=1;admissible+=independent;obstructed+=collision
    return {'group_types':types,'cayley_presentations':cases,'direct_cyclic_products':admissible,
            'forced_collision_presentations':obstructed,'matrix_prime':101}


def faults(directory):
    cert=json.loads((directory/'certificate.json').read_text())
    proof=(directory/'q11_four_unsat.drat').read_text()
    word=json.loads((directory/'q11_five_colouring.json').read_text())
    rejected=[]
    def reject(name,mutate):
        c,p,w=copy.deepcopy(cert),proof,word.copy()
        c,p,w=mutate(c,p,w)
        try:verify(directory,c,p,w)
        except ValueError as e:rejected.append({'fault':name,'reason':str(e)});return
        raise ValueError('fault accepted: '+name)
    def change(name,edit):
        def mutation(c,p,w):edit(c);return c,p,w
        reject(name,mutation)
    change('boolean version',lambda c:c.update(version=True))
    change('missing case',lambda c:c['cases'].pop())
    change('duplicate case',lambda c:c['cases'].__setitem__(1,c['cases'][0]))
    change('wrong parameter',lambda c:c['cases'][0].update(q=True))
    change('reducible modulus',lambda c:c['cases'][0].update(modulus=[0,0,1]))
    change('missing generator',lambda c:c['cases'][0]['generators'].pop())
    change('wrong edge count',lambda c:c['cases'][0].update(edges=5))
    change('invalid transverse generator',lambda c:c['cases'][0]['redundancy']['terms'][0].__setitem__(0,1))
    change('invalid coefficient',lambda c:c['cases'][0]['redundancy']['terms'][0].__setitem__(1,True))
    change('false relation',lambda c:c['cases'][0]['redundancy']['terms'].pop())
    change('missing obstruction',lambda c:c['cases'][-1].update(redundancy=None))
    change('wrong exceptional case',lambda c:c['cases'][1].update(redundancy={}))
    reject('monochromatic witness',lambda c,p,w:(c,p,[0]*121))
    reject('boolean colour',lambda c,p,w:(c,p,[True]+w[1:]))
    reject('short witness',lambda c,p,w:(c,p,w[:-1]))
    reject('missing proof end',lambda c,p,w:(c,'\n'.join(p.splitlines()[:-1])+'\n',w))
    reject('unsupported empty clause',lambda c,p,w:(c,'0\n',w))
    reject('false initial clause',lambda c,p,w:(c,'-1 0\n'+p,w))
    reject('out of range literal',lambda c,p,w:(c,'485 0\n'+p,w))
    return rejected


def main():
    directory=Path(__file__).resolve().parent
    print(json.dumps({'small_group_audit':small_groups(),'rejected_faults':faults(directory)},sort_keys=True))


if __name__=='__main__':main()
