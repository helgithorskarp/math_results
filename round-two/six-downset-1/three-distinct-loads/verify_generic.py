"""Second-algorithm generic bordered identity audit over19 variables.

Only ordinary sparse integer dictionaries and schoolbook products are
used, independently of the rational/Kronecker determinant engine. Full
6-by-6 determinants use all720 permutations; factorized reconstruction
uses leading adjugate and nine second-compound terms. This is a same-author
exact polynomial audit, not peer review or proof-assistant formalization.
"""
from itertools import permutations,combinations
from pathlib import Path
import argparse,json,resource,signal,time
DIM=19;ZERO=(0,)*DIM;LIMIT=30000
def require(p,message):
    if not p:raise ValueError(message)
def alarm(a,b):raise TimeoutError('generic border audit60s guard')
signal.signal(signal.SIGALRM,alarm)
class P:
    def __init__(self,a=0):
        self.a={k:v for k,v in a.items() if v} if isinstance(a,dict) else ({ZERO:a} if a else {})
        require(len(self.a)<=LIMIT,'unchanged generic polynomial term guard')
    def __add__(self,b):
        if not isinstance(b,P):b=P(b)
        out=dict(self.a)
        for k,v in b.a.items():out[k]=out.get(k,0)+v
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.a.items()})
    def __sub__(self,b):return self+-b
    def __mul__(self,b):
        if not isinstance(b,P):b=P(b)
        out={}
        for i,v in self.a.items():
            for j,w in b.a.items():
                k=tuple(i[z]+j[z] for z in range(DIM));out[k]=out.get(k,0)+v*w
        return P(out)
    __rmul__=__mul__
def var(i):return P({tuple(int(i==j) for j in range(DIM)):1})
def determinant(A):
    out=P()
    for perm in permutations(range(len(A))):
        z=P((-1)**sum(perm[i]>perm[j] for i in range(len(A)) for j in range(i+1,len(A))))
        for i,j in enumerate(perm):z=z*A[i][j]
        out=out+z
    return out
def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),P()) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def check():
    started=time.monotonic();signal.alarm(60)
    A=[[P() for j in range(4)] for i in range(4)];index=0
    for i in range(4):
        for j in range(i,4):A[i][j]=A[j][i]=var(index);index+=1
    X=[[var(10+2*i+j) for j in range(2)] for i in range(3)]+[[P(),P()]]
    E=[[var(16),var(17)],[var(17),var(18)]]
    M=[A[i]+X[i] for i in range(4)]+[[*row,*E[i]] for i,row in enumerate(tr(X))]
    d4=determinant(A)
    C=[[(-1)**(i+j)*determinant([[A[a][b] for b in range(4) if b!=i] for a in range(4) if a!=j]) for j in range(4)] for i in range(4)]
    product=mm(A,C)
    for i in range(4):
        for j in range(4):require(not (product[i][j]-int(i==j)*d4).a,'generic adjugate polynomial identity')
    Y=mm(mm(tr(X),C),X);pairs=list(combinations(range(3),2))
    plucker={I:X[I[0]][0]*X[I[1]][1]-X[I[0]][1]*X[I[1]][0] for I in pairs};compound=P()
    for I in pairs:
        for J in pairs:compound=compound+(-1)**(sum(I)+sum(J))*plucker[I]*plucker[J]*determinant([[A[a][b] for b in range(4) if b not in I] for a in range(4) if a not in J])
    fifth=d4*E[0][0]-Y[0][0]
    sixth=d4*determinant(E)-E[1][1]*Y[0][0]-E[0][0]*Y[1][1]+2*E[0][1]*Y[0][1]+compound
    literal5=determinant([row[:5] for row in M[:5]]);literal6=determinant(M)
    require(not (fifth-literal5).a,'generic fifth border identity over19 variables')
    require(not (sixth-literal6).a,'generic sixth border identity over19 variables')
    require(not (compound*d4-determinant(Y)).a,'generic second-compound Jacobi identity over19 variables')
    require(bool((sixth-4*E[0][1]*Y[0][1]-literal6).a),'wrong cross-term sign damage not detected')
    signal.alarm(0)
    result={'agent':'six-downset-1','role':'researcher','status':'same-author second-algorithm generic polynomial audit; not independent review','coefficient_ring':'ZZ[a_00,a_01,a_02,a_03,a_11,a_12,a_13,a_22,a_23,a_33,x_00,x_01,x_10,x_11,x_20,x_21,e_00,e_01,e_11]','X_last_row_identically_zero':True,'generic_adjugate_identities':16,'generic_fifth_border_identity':True,'generic_sixth_border_identity':True,'generic_second_compound_Jacobi_identity':True,'full_fifth_determinant_permutations':120,'full_sixth_determinant_permutations':720,'nonzero_second_compound_terms':9,'fifth_polynomial_terms':len(literal5.a),'sixth_polynomial_terms':len(literal6.a),'schoolbook_integer_polynomial_arithmetic_only':True,'wrong_cross_term_sign_rejected':True,'per_polynomial_term_guard':LIMIT,'stage_seconds_guard':60,'elapsed_seconds':time.monotonic()-started,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path);args=parser.parse_args();result=check()
    if args.expected:
        expected=json.loads(args.expected.read_text())['generic']
        stable=lambda out:{k:v for k,v in out.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
        require(stable(result)==stable(expected),'frozen generic border identity mismatch')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
