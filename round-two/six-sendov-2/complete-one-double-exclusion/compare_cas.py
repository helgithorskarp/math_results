"""Separate exact SymPy ring/subset determinant proof computation.

Direct substitution on the NEW positive-q0 caps, without native binomial
or native determinant imports. Shared module provides serialization only.
Requires SymPy 1.14.0. All coefficients are QQ, characteristic zero.
"""
from pathlib import Path
from math import comb
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from record_io import emit, require, rows, partitions
import sympy as sp
from sympy.polys.rings import ring


def compute():
    require(sp.__version__ == "1.14.0", "pinned exact CAS version")

    V,h,x=ring("h,x",sp.QQ)
    require(h**4-x*x*(2*h-x)**2==(h-x)**2*(h*h+x*(2*h-x)),
            "whole original height numerator inequality")
    A0=h;B0=sp.QQ(1,4)-h
    require(A0*B0-sp.QQ(1,100)==(A0-sp.QQ(1,20))*(sp.QQ(1,5)-A0),
            "whole strict AB factor identity")
    require((A0+3*B0)*(A0+4*B0/3)-(A0-B0)**2==B0*(19*A0/3+3*B0),
            "whole positive J0 lower-bound identity")
    M, a, D, u, z = ring("a,D,u,z", sp.QQ)
    A, E = a*a, sp.QQ(3, 64)-D/8
    q = z**4+(2*A-sp.QQ(1, 2))*z*z+3*A*A-A+2*E
    Q = (z+a)**2*q+4*u
    f = (z-a)**2*Q
    H = f.diff(z).exquo(8*(z-a))
    require(f == (z*z-A)**2*q+4*u*(z-a)**2, "entire original factorization")
    require(H == z*(z+a)*(z**4+(A-sp.QQ(3, 8))*z*z+A*A-3*A/8+E)+u,
            "entire derivative quotient")
    T4 = Q.diff(z).exquo(2*(z+a))
    require(T4 == 3*z**4+2*a*z**3+2*(2*A-sp.QQ(1, 2))*z*z+a*(2*A-sp.QQ(1, 2))*z+3*A*A-A+2*E,
            "whole original critical quartic")
    r = 8*z*H-8*(z-a)*Q
    require(r.degree(z) == 5, "whole residue numerator degree")
    def zc(poly, i):
        return M.from_dict({(*m[:3], 0): c for m, c in poly.items() if m[3] == i})
    require(zc(r, 5) == M.one, "entire leading-one residue numerator")
    fc = [zc(f, 8-i) for i in range(9)]
    moments = [M(8)]
    for n in range(1, 6):
        moments.append(-sum((fc[i]*moments[n-i] for i in range(1, n)), M.zero)-n*fc[n])
    require(moments[1] == moments[3] == moments[5] == M.zero, "all original odd moments")
    require(moments[2] == M.one and moments[4] == sp.QQ(1, 8)+D, "whole original norm and excess")
    R, aa, DD, uu = ring("a,D,u", sp.QQ)
    def scalar(poly):
        require(all(m[3] == 0 for m in poly), "no z in scalar coefficient")
        return R.from_dict({m[:3]: c for m, c in poly.items()})
    tc = [scalar(zc(T4, 4-i))/3 for i in range(5)]
    tp = [R(4)]
    for n in range(1, 7):
        val = -sum((tc[j]*tp[n-j] for j in range(1, min(n, 4)+1)), R.zero)
        if n <= 4: val -= (n-4)*tc[n]
        tp.append(val)
    tminors = []
    for n in range(1, 5):
        mat = sp.Matrix(n, n, lambda i, j: tp[i+j].as_expr())
        tminors.append(R.from_expr(mat.det(method="domain-ge")))
    require(tminors[0] == 4, "first whole critical Hermite minor")
    hc = [scalar(zc(H, i)) for i in range(7)]
    rc = [scalar(zc(r, i)) for i in range(6)] + [R.zero]
    gc = [(i+1)*hc[i+1] for i in range(6)] + [R.zero]
    def bez(g):
        B = [[R.zero for _ in range(6)] for _ in range(6)]
        for i in range(1, 7):
            for j in range(i):
                v = hc[i]*g[j]-hc[j]*g[i]
                for k2 in range(i-j):
                    B[i-1-k2][j+k2] += v
        require(all(B[i][j] == B[j][i] for i in range(6) for j in range(6)), "whole Bezout symmetry")
        return B
    B0, B1 = bez(gc), bez(rc)
    dp = {0: (R.one, R.zero, R.zero)}
    for row in range(6):
        nxt = {}
        for mask, old in dp.items():
            for j in range(6):
                if (mask >> j) & 1: continue
                sign = -1 if (mask >> (j+1)).bit_count() % 2 else 1
                x, y2 = B0[row][j], B1[row][j]
                values = (sign*old[0]*x, sign*(old[1]*x+old[0]*y2),
                          sign*(old[2]*x+old[1]*y2))
                key = mask | (1 << j)
                previous = nxt.get(key, (R.zero, R.zero, R.zero))
                nxt[key] = tuple(previous[i]+values[i] for i in range(3))
        dp = nxt
    delta, d1, N = dp[63]
    require(d1 == delta, "entire sum-one coefficient")
    S, XA, XD, XU = ring("A,D,u", sp.QQ)
    def even(poly):
        require(all(m[0] % 2 == 0 for m in poly), "complete reflection parity")
        return S.from_dict({(m[0]//2, m[1], m[2]): c for m, c in poly.items()})
    de, en = even(delta), even(N)
    P = 47*XD*de-4*en
    require(de.degree(XU) == en.degree(XU) == 5, "whole u degrees")

    T,h,rn,v=ring("h,r,v",sp.QQ)
    def substitute(poly,axis,lo,hi):
        grouped={}
        for m,c in poly.items():
            n=list(m);i=n[axis];n[axis]=0
            grouped.setdefault(i,T.zero)[tuple(n)]=c
        out=T.zero;aff=lo+(hi-lo)*[h,rn,v][axis]
        for i in range(max(grouped,default=0),-1,-1):out=out*aff+grouped.get(i,T.zero)
        return out
    def transform(poly,degrees,reverse=False):
        d=dict(poly.items())
        for axis,n in enumerate(degrees):
            out={}
            # Direct contribution formula, rather than grouped native lines.
            for m,c in d.items():
                i=m[axis]
                for k in range(i,n+1):
                    q=list(m);q[axis]=k;q=tuple(q)
                    factor=(comb(n,k)*comb(k,i)*(-1)**(k-i) if reverse else
                            sp.QQ(comb(k,i),comb(n,i)))
                    out[q]=out.get(q,sp.QQ.zero)+c*factor
            d={m:c for m,c in out.items()if c}
        return T.from_dict(d)
    quartic=T.zero
    for (ia,id0,iu,iz),c in T4.items():
        require(iu==0,"original critical quartic independent of shift")
        quartic+=c*h**ia*sp.QQ(5,141)**id0*(-rn)**iz
    require([quartic.degree(g)for g in [h,rn,v]]==[4,4,0],
            "whole negative critical quartic rectangle degree")
    leaves=[]
    for spec in partitions():
        box=quartic
        for axis,(lo,hi)in enumerate(spec["bounds"]):
            box=substitute(box,axis,sp.QQ(lo.numerator,lo.denominator),sp.QQ(hi.numerator,hi.denominator))
        deg=[4,4,0];ctrl=transform(box,deg)
        require(transform(ctrl,deg,True)==box,"whole quartic reverse tensor identity")
        leaves.append({"label":spec["label"],"kind":"quartic","bounds":
                       [[str(lo),str(hi)]for lo,hi in spec["bounds"]],
                       "degrees":deg,"box":rows(box),"controls":rows(ctrl)})
    parents=[]
    for side,sign,kappa,hi in [("positive",1,9,sp.QQ(17,250)),("negative",-1,16,sp.QQ(71,1000))]:
        A2=sp.QQ(1,8)+sign*h;B2=sp.QQ(1,4)-A2
        J=(B2*(19*A2/3+3*B2)if side=="positive"else 4*A2*(A2+B2/3+sp.QQ(4,35))-4*h*h)
        require(J==(sp.QQ(7,48)-3*h/4-10*h*h/3 if side=="positive"else
                    sp.QQ(59,420)-51*h/35-4*h*h/3),"whole rational J identity")
        den=kappa*A2*J;dn=kappa*A2*(8*h*h*J-4*h**4*rn)
        un=-h**4*(J+4*h*h*rn)*v
        require(max(m[1]+m[2]for m in P)==8,"whole joint D-u denominator degree")
        cleared=T.zero
        for(i,j,k),c in P.items():cleared+=c*A2**i*dn**j*un**k*den**(8-j-k)
        require(min(m[0]for m in cleared)==10,"entire h common factor")
        reduced=cleared.exquo(h**10)
        require(cleared==h**10*reduced,"entire positive-q0 factor identity")
        parents.append({"label":side,"kappa":kappa,"denominator_power":8,"h_removed":10,
                        "A":rows(A2),"J":rows(J),"cleared":rows(cleared),"reduced":rows(reduced)})
        lo=sp.QQ(1,72);box=substitute(reduced,0,lo,hi)
        deg=[box.degree(g)for g in [h,rn,v]]
        require(deg==[31,8,5],"whole positive-q0 cap tensor degrees")
        ctrl=transform(box,deg)
        require(transform(ctrl,deg,True)==box,"whole cap reverse tensor identity")
        leaves.append({"label":side,"kind":"cap","bounds":[[str(lo),str(hi)],["0","1"],["0","1"]],
                       "degrees":deg,"box":rows(box),"controls":rows(ctrl)})
    model = {"f": rows(f), "Q": rows(Q), "H": rows(H), "r": rows(r),
             "T4": rows(T4), "T4_moments": [rows({(*m, 0): c for m, c in p.items()}) for p in tp],
             "T4_Hermite_leading_minors": [rows(even(p)) for p in tminors],
             "moments": [rows(p) for p in moments],
             "B0": [[rows(p) for p in line] for line in B0],
             "B1": [[rows(p) for p in line] for line in B1]}

    return {"domain":"QQ[a,D,u,z]; QQ[A,D,u]; QQ[h,r,v]; characteristic zero",
            "model":model,"Delta":rows(de),"N":rows(en),"P":rows(P),
            "scalar_margins":scalar_margins(),"negative_quartic":rows(quartic),
            "parents":parents,"leaves":leaves}


def scalar_margins():
    q={}
    q["positive_A_ge_21_100"] = 2*(sp.QQ(21,100)-sp.QQ(1,8))**2-sp.QQ(5,564)-sp.QQ(1,1875)-sp.QQ(4,1125)
    q["positive_A_ge_1_5"] = 8*sp.QQ(3,40)**2-4*sp.QQ(17,200)**4/sp.QQ(104,1875)-sp.QQ(5,141)
    q["positive_D_monotonic"] = 1-sp.QQ(240,17)*sp.QQ(3,40)**2
    q["positive_h_ge_17_250"] = 8*sp.QQ(17,250)**2-sp.QQ(960,17)*sp.QQ(17,250)**4-sp.QQ(5,141)
    q["h_low_enclosure"] = sp.QQ(1,5000)-sp.QQ(1,72)**2
    q["positive_J_box"] = sp.QQ(7,48)-sp.QQ(3,4)*sp.QQ(17,250)-sp.QQ(10,3)*sp.QQ(17,250)**2
    for name,lo,hi in [("low",sp.QQ(1,25),sp.QQ(9,200)),("high",sp.QQ(9,200),sp.QQ(1,20))]:
        hhi,hlo = sp.QQ(1,8)-lo,sp.QQ(1,8)-hi
        ell = lo+(sp.QQ(1,4)-lo)/3+sp.QQ(18,175)
        J=ell*ell-4*hhi*hhi
        q["negative_J_"+name]=J
        q["negative_eJ_minus_h4_"+name]=(2*hlo*hlo-sp.QQ(5,564))*J-hhi**4
    q["sqrt_AB_low"]=sp.QQ(1,25)*sp.QQ(21,100)-sp.QQ(9,100)**2
    q["twice_inverse_sqrt3"]=sp.QQ(7,4)**2-3
    q["sqrt_AB_high_positive_factor"]=sp.QQ(1,5)-sp.QQ(1,8)
    q["negative_J_min"]=sp.QQ(59,420)-sp.QQ(51,35)*sp.QQ(3,40)-sp.QQ(4,3)*sp.QQ(3,40)**2
    q["negative_D_monotonic"]=1-sp.QQ(8400,199)*sp.QQ(3,40)**2
    q["negative_h_ge_71_1000"]=8*sp.QQ(71,1000)**2-sp.QQ(33600,199)*sp.QQ(71,1000)**4-sp.QQ(5,141)
    require(all(c>0 for c in q.values()), "all original-strip endpoint margins")
    return {k:str(c)for k,c in q.items()}



if __name__ == "__main__": emit(compute())
