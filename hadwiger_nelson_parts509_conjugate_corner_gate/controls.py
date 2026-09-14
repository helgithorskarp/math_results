#!/usr/bin/env python3
"""Algebra, projection, and deliberate-corruption controls for verify.py."""
import copy,itertools,json
import verify as v

def main():
    gm,den,P,V,U,E,words=v.load()
    # Check the field automorphism on every pair of basis elements.
    def sigma(a):return tuple(c*(-1 if i&2 else 1) for i,c in enumerate(a))
    basis=[tuple(int(i==j) for i in range(8)) for j in range(8)]
    for a,b in itertools.product(basis,repeat=2):
        v.need(sigma(gm.field_multiply(a,b))==gm.field_multiply(sigma(a),sigma(b)),
               'sigma multiplicativity')
    # All positive clauses on a small universe, including fixed selected S
    # and fixed omitted Q, against literal set intersections.
    S=set(range(5));B={0,1,2};C={5,6,7};universe=list(range(10));tests=0
    for mask in range(1,1<<10):
        D={i for i in universe if mask>>i&1}
        for rr in itertools.combinations(sorted(B),2):
            R=set(rr)
            for q in C:
                A={q};X=(S-R)|A
                rhs=bool((D&S)-B) or not (D&S)<=R or bool(D&C&A)
                v.need(bool(D&X)==rhs,'small exact projection');tests+=1
    data=json.loads((v.HERE/'certificate.json').read_text());row=data['rows'][0]
    rejects=0
    def reject(fn):
        nonlocal rejects
        try:fn()
        except ValueError:rejects+=1
        else:raise ValueError('bad certificate accepted')
    bad=copy.deepcopy(row);bad['D'].append(bad['D'][0])
    reject(lambda:v.check_word(bad,U,E,words))
    bad=copy.deepcopy(row);bad['c']=bad['c'][:-1]
    reject(lambda:v.check_word(bad,U,E,words))
    bad=copy.deepcopy(row);bad['p']=20
    reject(lambda:v.check_word(bad,U,E,words))
    bad=copy.deepcopy(row);pos={u:i for i,u in enumerate(U)}
    for a,b in E:
        if a in pos and b in pos and bad['c'][pos[a]]!='.' and bad['c'][pos[b]]!='.':
            c=list(bad['c']);c[pos[a]]=c[pos[b]];bad['c']=''.join(c);break
    reject(lambda:v.check_word(bad,U,E,words))
    unary=[r for r in data['rows'] if len(set(r['D'])&set(data['C']))==1]
    reject(lambda:v.explain(data['B'],data['C'],U[:135],unary))
    print(json.dumps({'status':'CONTROLS_PASS','basis_product_cases':64,
                      'projection_cases':tests,'corruptions_rejected':rejects},indent=2,sort_keys=True))

if __name__=='__main__':main()
