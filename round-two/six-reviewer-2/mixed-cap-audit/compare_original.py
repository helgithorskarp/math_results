"""Late fixture adapter; imports only sealed reviewer engines, never author code.

The author record is external comparison data, not a proof-generation input.
Positive row clearing differs by explicit positive integer multipliers.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,prod
import argparse,hashlib,json,signal
from frame import model,evaluate
from physical import original,raw_core,lift
from rational import clear_rows,reconstruct,ROOTS
from linear import need,psd,canonical

def matrix_hash(A):
    return hashlib.sha256(json.dumps([[str(x)for x in r]for r in A],separators=(',',':')).encode()).hexdigest()
def polynomial_hash(p):
    denominator=lcm(*(v.denominator for v in p))
    record={'den':denominator,'terms':[[[i],str(int(v*denominator))]for i,v in enumerate(p)if v]}
    return hashlib.sha256(json.dumps(record,separators=(',',':')).encode()).hexdigest()
def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60s late comparison guard')));signal.alarm(60)
    a=argparse.ArgumentParser();a.add_argument('record');a.add_argument('--expected');args=a.parse_args()
    author=json.loads(Path(args.record).read_text());M=model();polynomials=[]
    labels=['residual-Gram','cap-antisymmetric','cap-symmetric']
    for (name,A),native,label in zip(M['blocks'],author['uniform_certificate']['records'],labels):
        need(native['label']==label,'all polynomial block labels')
        cleared,factors=clear_rows(A)
        for row,declared in zip(factors,native['row_clearing_domains']):
            supplied={int(F(x['factor'][0][1])):x['exponent']for x in declared}
            wanted={c:e for c,e in zip(ROOTS,row['positive_factor_exponents'])if e}
            need(supplied==wanted,'all normalized positive row factor domains')
        for k,expected in enumerate(native['minors'],1):
            p,bound,values=reconstruct([r[:k]for r in cleared[:k]])
            scale=prod(row['positive_integer']for row in factors[:k]);p=[F(v,scale)for v in p]
            made={'order':k,'degree':len(p)-1,'coefficients':len(p),
                  'strictly_positive_coefficients':all(v>0 for v in p),'constant':str(p[0]),
                  'fingerprint':polynomial_hash(p),'independent_identity_points':bound+1}
            need(made==expected,'every native polynomial coefficient fingerprint/math field')
            polynomials.append({'block':label,**made,'reviewer_integer_multiplier':scale})
    fixtures=[];whole_entries=0
    for expected in author['original_fixtures']:
        n=expected['n'];r,S,seed=original(n,M);q=1<<(n-1);N=len(S);s=q+3
        u=1<<n;v=1<<(n+1);b=1<<(n+2);new=[u,v,u|v,b]
        order=list(range(2*q))
        for T,mark in zip(new,[1,1,1,2]):order.extend([T,T|mark])
        permutation=[S.index(T)for T in order]
        reorder=lambda A:[[A[i][j]for j in permutation]for i in permutation]
        core=[[(N-s)*seed[i][j]+s*(i==j)-1 for j in range(1,N)]for i in range(1,N)]
        labels_core=[('old',-1,T)for T in range(1,2*q)]+[('marked',i,T)for i,T in enumerate(new)]+[('private',i,T)for i,T in enumerate(new)]
        raw=raw_core(q,list(range(1,2*q)),labels_core);T=F(r['raw_trace']);epsilon=1/(2*(1+T))
        mixed,_,_=lift([[(1-epsilon)*x+epsilon*y for x,y in zip(row,rr)]for row,rr in zip(core,raw)],s)
        def info(A,lower_rank):
            upper=[[(i==j)-x for j,x in enumerate(row)]for i,row in enumerate(A)]
            return {'N':N,'s':s,'lower_rank':lower_rank,'upper_rank':psd(upper)['rank'],'matrix_sha256':matrix_hash(reorder(A))}
        made={'n':n,'q':q,'seed':info(seed,N-2),'mixed':info(mixed,N-1),
              'changed_Gram_positions':100,'changed_frame_positions':100,
              'untouched_high':r['high_actions'],'untouched_low':r['low_actions'],
              'epsilon':str(epsilon),'raw_trace':str(T)}
        need(made==expected,'every complete native original fixture math field')
        fixtures.append(made);whole_entries+=2*N*N
    scalar=[]
    for x in author['uniform_certificate']['scalar_controls']:
        q=int(x['q']);G=evaluate(M['gram'],q);B=evaluate(M['cap'],q)
        made={'q':str(q),'Gram_positions':100,'frame_positions':100,'Gram_rank':psd(G)['rank'],'gap1_cap_rank':psd(B)['rank']}
        need(made==x,'all native scalar control fields');scalar.append(made)
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer','late_comparison':True,
         'polynomials':polynomials,'original_fixtures':fixtures,'scalar_controls':scalar,
         'whole_matrix_encoded_entries':whole_entries,'whole_matrix_encoded_hashes':8,
         'trust':'All 13 complete coefficient fingerprints/positive row factors and every native fixture field reconstructed by sealed own engines. Whole matrices compared by exact rational entry encoding SHA, not an author full-matrix corpus. Native implementations are never imported.'}
    if args.expected:need(canonical(out)==json.loads(Path(args.expected).read_text()),'complete frozen late comparison record')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)
if __name__=='__main__':main()
