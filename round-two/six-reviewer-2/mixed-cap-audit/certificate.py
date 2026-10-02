"""Independent complete polynomial signs by scalar determinant interpolation."""
import argparse,json,signal
from fractions import Fraction as F
from pathlib import Path
from frame import model,evaluate
from rational import R,positive_certificate,determinant,reconstruct,ev,mul,add
from linear import need,canonical,digest,psd

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60s symbolic phase guard')));signal.alarm(60)
    p=argparse.ArgumentParser();p.add_argument('--expected');a=p.parse_args();M=model();rows=[]
    for name,A in M['blocks']:rows.append(positive_certificate(A,name))
    scalar=[]
    for q in [4,5,7,8,16,32,1024,1000000,2**100]:
        G=evaluate(M['gram'],q);FF=evaluate(M['frame'],q);BB=evaluate(M['cap'],q)
        need(psd(G)['rank']==10 and psd(BB)['rank']==10,'entire ten-dimensional scalar forms')
        scalar.append({'q':q,'gram_sha256':digest(G),'full_frame_sha256':digest(FF),'cap_sha256':digest(BB)})
    # Determinant/interpolation controls compared to literal permutation sums.
    from itertools import permutations
    cases=0
    for n in [1,2,3]:
        for seed in range(5):
            A=[[tuple((seed+1)*(i+1)-j+k for k in range(1+(i+j)%3))for j in range(n)]for i in range(n)]
            wanted=(F(0),)
            for perm in permutations(range(n)):
                inversions=sum(perm[i]>perm[j]for i in range(n)for j in range(i+1,n))
                term=(F((-1)**inversions),)
                for i,j in enumerate(perm):term=mul(term,A[i][j])
                wanted=add(wanted,term)
            got,_,_=reconstruct(A);need(tuple(map(F,got))==wanted,'literal permutation determinant polynomial');cases+=1
    rejections=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,ZeroDivisionError):rejections.append(name);return
        raise ValueError('damage accepted '+name)
    reject('negative-constant',lambda:positive_certificate([[R(-1)]],'bad'))
    reject('negative-tail-coefficient',lambda:positive_certificate([[R((1,-1))]],'bad'))
    reject('zero-constant',lambda:positive_certificate([[R((0,1))]],'bad'))
    reject('asymmetric-original',lambda:positive_certificate([[R(2),R(1)],[R(0),R(2)]],'bad'))
    reject('indefinite-positive-diagonal',lambda:positive_certificate([[R(1),R(2)],[R(2),R(1)]],'bad'))
    reject('invalid-denominator-exponent',lambda:R((1,),(-1,0,0,0,0)))
    reject('unknown-divisor',lambda:R(1)/R((1,1)))
    reject('zero-divisor',lambda:R(1)/R(0))
    need((R((4,1))/R((4,1)))==1,'exact positive-factor cancellation')
    need(R((4,1),(1,0,0,0,0))==1,'synthetic division with zero remainder')
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer',
         'method':'original rational vectors; positive linear-factor clearing; degree-bounded scalar Gaussian/Newton reconstruction',
         'certificates':rows,'scalar_controls':scalar,'literal_permutation_polynomial_controls':cases,'rejections':rejections,
         'total_minors':sum(len(r['leading_minors'])for r in rows),
         'total_coefficients':sum(v['coefficient_count']for r in rows for v in r['leading_minors']),
         'total_identity_evaluations':sum(v['identity_evaluations']for r in rows for v in r['leading_minors'])}
    if a.expected:need(canonical(out)==json.loads(Path(a.expected).read_text()),'complete frozen symbolic record')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)

if __name__=='__main__':main()
