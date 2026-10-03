"""Independently counted ambient full-S_q cap, exact deletion constraint.

11 constant fibre values and the full6 standard sector are constructed
from the defining original table. The deleted bcx values are zero;
variance of its surviving constant fibre is kq/(q-k) times mean^2.
"""
from pathlib import Path
import json
import original_field as O
q,k,Z,I=O.q,O.k,O.ZERO,O.ONE
TAB=O.table()

def c(x,r): return O.choose(x,r)

def gram(standard):
    groups=[(0,),(0,),(1,),(2,4),(3,5),(6,)] if standard else [(0,),(0,),(1,),(2,4),(3,5),(6,),(7,),(1,),(2,4),(3,5),(6,)]
    sizes=[1,2,1,1,1,1] if standard else [1,2,0,0,0,0,0,1,1,1,1]
    norm=[len(g)*(2*(q-2) if r==2 else 2) if standard else len(g)*c(q,r) for g,r in zip(groups,sizes)]
    N=(q*q+13*q+16)/2-k;s=3*q+4
    U=[];D=[]
    for i,(g,r) in enumerate(zip(groups,sizes)):
        ur=[];dr=[]
        for j,(h,t) in enumerate(zip(groups,sizes)):
            dis=sum(not(a&b) for a in g for b in h)
            val=(N-s)*norm[i] if i==j else Z;dv=Z
            if dis:
                b0,b1=TAB[tuple(sorted(((g[0].bit_count(),r),(h[0].bit_count(),t))))]
                fac=(-2*(q-2)*(q-3) if r==t==2 else -2 if r==t==1 else -2*(q-2)) if standard else c(q,r)*c(q-r,t)
                val-=dis*fac*b0;dv=dis*fac*b1
            ur.append(val);dr.append(dv)
        U.append(ur);D.append(dr)
    return U,D,norm

def main():
    Us,Ds,ns=gram(True)
    Su,Vs=O.short(Us,[5],masses=ns)
    nu=Su[0][0]/2;Es=O.energy(Ds,Vs)[0][0]/2
    print('full standard cap short and Delta',flush=True)
    Ut,Dt,nt=gram(False)
    H4,V4=O.short(Ut,[2,4,3,10],masses=nt)
    print('full trivial cap original solve7 complete',flush=True)
    rr=q-k; coef=H4[3][3]+k*q/rr*nu
    beta=[-H4[3][i]/coef for i in range(3)]
    M=[[H4[i][j]+H4[i][3]*beta[j] for j in range(3)] for i in range(3)]
    V=[[V4[j][i]+V4[j][3]*beta[i] for i in range(3)] for j in range(11)]
    E=O.energy(Dt,V)
    Dc=[[E[i][j]+k*q/rr*beta[i]*beta[j]*Es for j in range(3)] for i in range(3)]
    O.require(all(M[i][j]==M[j][i] and Dc[i][j]==Dc[j][i] for i in range(3) for j in range(3)),'all cap field entries symmetric')
    O.require(all(Dc[i][1]==Dc[i][2] for i in range(3)) and all(Dc[1][j]==Dc[2][j] for j in range(3)), 'complete cap derivative null direction')
    O.write('cap-sectors',dict(M=M,Delta=Dc,V=V,beta=beta,standard_minimizer=Vs,standard_nu=nu,standard_Delta=Es,H4=H4))
    print('complete independent cap fields saved',flush=True)

if __name__=='__main__':main()
