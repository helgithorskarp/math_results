"""Independent closed antiderivative, formal roots and complete normal maps."""
from math import comb
import json
from cyclo36 import E,A,Q,need,I,W,C,INV1C,INVCPLUS,M,B,constant,add,scale,multiply,power,conjugate,encode

def run():
    c=C;d=2*c*c-1;y=INV1C/3;x=E(Q(2,3))-y;lam=12*(1+c);li=INV1C/12
    k=-7*(1+2*c)/18;g=48*k;m2=-x*lam
    ms=[A(),A(),A(m2),A(I*g),M]
    low=add(ms,[A(),A(-I),A(-6*k),A(-I)*B,A()])
    high=add(ms,[A(),A(7*I),A(42*k),A(7*I)*B,A()])
    delta=add(high,scale(low,-1));anchor=[A(1),A(),A(-lam),A(),A()]
    # H(z)=(z-low)^9-(9/8)delta(z-low)^8; p=H(z)-H(a).
    poly=[]
    neg=scale(low,-1)
    for j in range(10):
        term=scale(power(neg,9-j),comb(9,j))
        if j<=8:term=add(term,scale(multiply(delta,power(neg,8-j)),-Q(9,8)*comb(8,j)))
        poly.append(term)
    aa=add(anchor,neg);H=add(power(aa,9),scale(multiply(delta,power(aa,8)),-Q(9,8)));poly[0]=add(poly[0],scale(H,-1))
    need(poly[9]==constant(1),'monic nine')
    need(all(poly[j][1]==0 for j in range(10)),'full absent first jet')
    need([v[0]for v in poly]==[A(-1)]+[A()for _ in range(8)]+[A(1)],'all zero-parameter polynomial coefficients')
    def evalcol(order,w):return sum((poly[j][order]*(w**j)for j in range(10)),A())
    def derivative(order,w):return sum((poly[j][order]*j*(w**(j-1))for j in range(1,10)),A())
    # Recurrence follows from p_0'=9 w^8 and p_0''/2=36 w^7.
    roots=[];normals=[]
    mstar=-(512+1684*c+1328*c*c)/9;bstar=(86-261*c-172*c*c)/18
    for label in range(9):
        w=W**label;dinv=w/9
        L=-evalcol(2,w)*dinv;U=-evalcol(3,w)*dinv
        V=-(evalcol(4,w)+derivative(2,w)*L+36*(w**7)*L*L)*dinv
        jet=[A(w),A(),L,U,V];roots.append(jet)
        norm=scale(add(multiply(jet,conjugate(jet)),constant(-1)),Q(1,2));normals.append(norm)
        need(L==A(lam*(-w/3-x-y*(w**8))),'every canonical second original jet')
        need(norm[0]==0 and norm[1]==0,'normal constant/linear')
        costheta=(w+w**8)/2
        need(norm[2]==A(-2*lam*y*(costheta+Q(1,2))*(costheta+c)),'every full second normal')
        if label in [3,4,5,6]:need(norm[2]==0 and norm[3]==0 and norm[4].evaluate(mstar,bstar)==-1,'every individually active normal closed')
        if label in [3,6]:need(U==A(-3*I*g*w),'nonzero cube tangency')
    need(roots[0]==anchor,'marked branch exact through full four jet')
    # Inverse square root of each actual distance, computed by the whole series.
    f=constant(0)
    for zeta,multiplicity in [(high,1),(low,7)]:
        diff=add(anchor,scale(zeta,-1));D=multiply(diff,conjugate(diff));need(D[0]==1,'distance tends to one')
        v=add(D,constant(-1));inv=constant(1)
        for n in range(1,5):inv=add(inv,scale(power(v,n),Q((-1)**n*comb(2*n,n),4**n)))
        f=add(f,scale(inv,multiplicity))
    need(f[0]==8 and f[1]==0 and f[3]==0,'objective parity through four')
    need(f[2]==A(lam*(E(Q(8,3))+y)),'entire objective leading coefficient')
    K=f[4]*(li*li);wanted=(19935+47482*c-62948*c*c)/972
    need(K.evaluate(mstar,bstar)==wanted,'target closed second objective coefficient')
    need(K.p.get((1,0))==8*li*li and K.p.get((0,1))==-56*li*li,'whole objective parameter columns')
    # Complete affine repair cone and its dual exact infimum.
    w4=INVCPLUS;w3=E(Q(2,3))*(7-(1-d)*w4)
    r3=normals[3][4];r4=normals[4][4]
    need(r3==A(-(431+320*c+320*c*c)/3)-Q(3,2)*M+12*B,'full normal three affine row')
    need(r4==A(-(1636+2842*c+1980*c*c)/9)-(1+c)*M+8*(1-d)*B,'full normal four affine row')
    Kinf=K+(w3*r3+w4*r4)*(li*li)
    need(set(Kinf.p)<={(0,0)},'complete positive-slack dual objective identity')
    shiftm=-(1+2*d)*w4/3;shiftb=(2*c-1)*w4/24
    mzero=mstar+shiftm;bzero=bstar+shiftb
    need(r3.evaluate(mzero,bzero)==0 and r4.evaluate(mzero,bzero)==0,'unique zero-normal intersection')
    need(K.evaluate(mzero,bzero)==Kinf.evaluate(0,0),'sharp repair-cone infimum')
    determinant=12*(c+d)
    return dict(status='COMPLETE_INDEPENDENT_CYCLOTOMIC36_JETS',field='QQ[T]/(T^12-T^6+1),T=exp(pi*i/18)',basis_degrees=list(range(12)),parameter_monomials=[[0,0],[1,0],[0,1]],polynomial_z_degrees=list(range(10)),s_degrees=list(range(5)),whole_polynomial=[encode(v)for v in poly],critical_mean=encode(ms),critical_large=encode(high),critical_small=encode(low),anchor=encode(anchor),all_nine_roots=[encode(v)for v in roots],all_nine_half_normals=[encode(v)for v in normals],whole_first_objective=encode(f),second_objective_affine=K.json(),closing_parameters=[mstar.json(),bstar.json()],closing_second_coefficient=wanted.json(),repair_domain={'normal3_affine':r3.json(),'normal4_affine':r4.json(),'determinant':determinant.json(),'positive_dual_weights':[w3.json(),w4.json()],'infimum_second_objective':Kinf.json(),'zero_normal_parameters':[mzero.json(),bzero.json()],'closed_to_zero_shifts':[shiftm.json(),shiftb.json()]},embedding_c_bracket=['15/16','47/50'],counts={'original_jets':9,'individual_normals':9,'active_normals':4,'primitive_coefficients':10,'jet_orders':5,'field_coordinates':12,'free_real_parameters':2,'critical_multiplicities':[1,7]})
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
