"""Complete classical 537-word SAT formulas, with optional colour symmetry."""
import argparse,hashlib
from pathlib import Path
N=537;K=6
TRIPLES=72092
BASE=N*(1+K*(K-1)//2)+TRIPLES*K
AUX=N*(K-1)
RGS_CLAUSES=BASE+2*(K-1)+3*(N-1)*(K-1)+N*(K-1)

def x(v,c):return K*(v-1)+c
def used(v,c):return K*N+(K-1)*(v-1)+c

def write(path,mode):
    assert mode in ('plain','rgs')
    total=BASE+1 if mode=='plain' else RGS_CLAUSES
    variables=K*N if mode=='plain' else K*N+AUX
    count=0;triples=0
    with Path(path).open('w',encoding='ascii',newline='\n') as f:
        f.write(f'p cnf {variables} {total}\n')
        def cl(lits):
            nonlocal count
            f.write(' '.join(map(str,lits))+' 0\n');count+=1
        if mode=='plain':cl([x(1,1)])
        for v in range(1,N+1):
            cl([x(v,c) for c in range(1,K+1)])
            for c in range(1,K+1):
                for d in range(c+1,K+1):cl([-x(v,c),-x(v,d)])
        for z in range(2,N+1):
            for a in range(1,z//2+1):
                b=z-a;triples+=1
                for c in range(1,K+1):
                    cl([-x(v,c) for v in sorted({a,b,z})])
        if mode=='rgs':
            for v in range(1,N+1):
                for c in range(1,K):
                    u=used(v,c)
                    cl([-x(v,c),u])
                    if v==1:cl([-u,x(v,c)])
                    else:
                        prior=used(v-1,c)
                        cl([-prior,u]);cl([-u,prior,x(v,c)])
            for v in range(1,N+1):
                for c in range(2,K+1):
                    if v==1:cl([-x(v,c)])
                    else:cl([-x(v,c),used(v-1,c-1)])
    assert triples==TRIPLES and count==total
    h=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    print('mode',mode,'vars',variables,'clauses',count,'triples',triples,
          'sha256',h,flush=True)
    return {'variables':variables,'clauses':count,'triples':triples,'sha256':h}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cnf',type=Path)
 p.add_argument('--mode',choices=('plain','rgs'),default='rgs')
 a=p.parse_args();write(a.cnf,a.mode)
