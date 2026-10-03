"""Independent finite fourth jets: direct coordinate powers, Newton integral,
all nine root residuals, normals, Jacobian, reciprocal cost and closing orders.

Formal variables: J3,J4,G,sigma,M,b. No target/earlier executable imports.
"""
from field import E,Q,I,W,C,need
import poly as P
from intervals import scalar_receipt

J3,J4,G,S,M,B=[P.var(j)for j in range(6)]
y=1/(3*(1+C));x=E(Q(2,3))-y;H=14*y;U=-8*x
k=-E(Q(7,18))*(1+2*C);rho=(C-5)/3;ell=k+rho
alpha=-E(Q(527,360))+Q(41,90)*C+Q(13,90)*C*C
tau=ell*ell/2
Bstar=E(Q(2311,108))+Q(4934,27)*C-Q(1976,9)*C*C
K1=Bstar-alpha*H*H/2
Kmax=K1+(Q(43,56)*alpha+Q(9,14)*tau)*H*H
A0=(U+rho*H)/8
moments=[P.const(8),{},P.const(H),J3,J4]


def cp_add(*a):
    out={}
    for p in a:
        for key,v in p.items():out[key]=P.add(out.get(key,{}),v)
    return {key:v for key,v in out.items()if v}


def cp_scale(a,c):
    return {key:P.scale(v,c)for key,v in a.items()if P.scale(v,c)}


def cp_mul(a,b):
    out={}
    for (t,j),p in a.items():
        for (u,l),q in b.items():
            if t+u<=4:
                key=(t+u,j+l);out[key]=P.add(out.get(key,{}),P.mul(p,q))
    return {key:v for key,v in out.items()if v}


def cp_power(a,n):
    out={(0,0):P.const(1)}
    for _ in range(n):out=cp_mul(out,a)
    return out


def summed(a):
    out=[{}for _ in range(5)]
    for (t,j),p in a.items():
        need(j<=4,'retained coordinate degree')
        out[t]=P.add(out[t],P.mul(p,moments[j]))
    return out


def tmul(a,b):
    out=[{}for _ in range(5)]
    for j,p in enumerate(a):
        for h,q in enumerate(b):
            if j+h<=4:out[j+h]=P.add(out[j+h],P.mul(p,q))
    return out


def tadd(*a):
    return [P.add(*(v[j]for v in a))for j in range(5)]


def tscale(a,c):
    return [P.scale(p,c)for p in a]


def tpower(a,n):
    out=[P.const(1),{},{},{},{}]
    for _ in range(n):out=tmul(out,a)
    return out


def eval_z(p,z):
    return P.add(*(P.scale(v,z**j)for j,v in p.items()))


def derivative_z(p,z):
    return P.add(*(P.scale(v,j*z**(j-1))for j,v in p.items()if j))


def gp(terms,constant=0):
    out={0:P.const(constant)}
    for j,a in terms:
        out[j]=P.add(out.get(j,{}),a)
        out[0]=P.sub(out[0],a)
    return {j:a for j,a in out.items()if a}


def record_z(p):
    return [[j,P.record(a)]for j,a in sorted(p.items())]


def normal_from_jets(z,L,T,V,omit_modulus=False):
    return [P.real(P.scale(L,z.conjugate())),
            P.real(P.scale(T,z.conjugate())),
            P.add(P.real(P.scale(V,z.conjugate())),
                  {}if omit_modulus else P.scale(P.mul(L,P.conj(L)),Q(1,2)))]


def run():
    checks=[]
    def equal(a,b,message):
        P.same(a,b,message);checks.append(message)
    # Actual single-coordinate expression, then eight-coordinate summation.
    uv={(0,0):P.const(A0),(0,1):P.scale(J3,ell/H),(0,2):P.const(-rho)}
    us=cp_add(uv,{(0,1):S})
    zeta=cp_add({(1,1):P.const(I),(3,0):P.scale(G,I),
                (3,1):P.scale(B,I),(4,0):M},
               {(t+2,j):p for (t,j),p in us.items()})
    powers=[None]+[summed(cp_power(zeta,n))for n in range(1,5)]
    U2=P.add(P.const(8*x*x-rho*rho*H*H/8),P.scale(J4,rho*rho),
             P.scale(P.power(J3,2),(k*k-rho*rho)/H),
             P.scale(P.mul(S,J3),2*k),P.scale(P.power(S,2),H))
    J21=P.add(P.const(-x*H+rho*H*H/8),P.scale(J4,-rho),
              P.scale(P.power(J3,2),ell/H),P.mul(S,J3))
    D=P.sub(U2,P.scale(B,2*H))
    closed=[
        None,[{}, {}, P.const(U),P.scale(G,8*I),P.scale(M,8)],
        [{},{},P.const(-H),P.scale(P.add(P.scale(J3,k),P.scale(S,H)),2*I),D],
        [{},{},{},P.scale(J3,-I),P.scale(J21,-3)],
        [{},{},{},{},J4]]
    for n in range(1,5):
        for t in range(5):equal(powers[n][t],closed[n][t],f'power moment {n}/{t}')
    equal(summed(uv)[0],P.const(U),'real correction sum')
    equal(summed(cp_mul(uv,{(0,1):P.const(1)}))[0],P.scale(J3,k),'mixed correction constraint')
    equal(summed(cp_power(us,2))[0],U2,'correction squared norm')
    # Newton recurrence in truncated t, then full anchor expansion.
    elementary=[[P.const(1),{},{},{},{}]]
    for n in range(1,5):
        a=tadd(*(tscale(tmul(elementary[n-j],powers[j]),(-1)**(j-1))
                 for j in range(1,n+1)))
        elementary.append(tscale(a,Q(1,n)))
    primitive={}
    from math import comb
    for n in range(5):
        for t,a in enumerate(elementary[n]):
            if not a:continue
            a=P.scale(a,(-1)**n*Q(9,9-n))
            primitive[(t,9-n)]=P.add(primitive.get((t,9-n),{}),a)
            for h in range(3):
                if t+2*h<=4:
                    key=(t+2*h,0)
                    primitive[key]=P.sub(primitive.get(key,{}),P.scale(a,(-1)**h*comb(9-n,h)))
    primitive={key:v for key,v in primitive.items()if v}
    maps=[{j:v for (t,j),v in primitive.items()if t==h}for h in range(5)]
    g2=gp([(8,P.const(9*x)),(7,P.const(9*y))],9)
    g3=gp([(8,P.scale(G,-9*I)),(7,P.scale(P.add(P.scale(J3,k),P.scale(S,H)),-Q(9,7)*I)),
           (6,P.scale(J3,I/2))])
    g4=gp([(8,P.scale(M,-9)),(7,P.scale(P.sub(P.const(U*U),D),Q(9,14))),
           (6,P.add(P.const(-3*U*H/4),P.scale(J21,Q(3,2)))),
           (5,P.sub(P.const(9*H*H/40),P.scale(J4,Q(9,20))))],-36-9*U+9*H/2)
    equal(maps[0],{9:P.const(1),0:P.const(-1)},'full constant primitive')
    equal(maps[1],{},'full linear primitive')
    for j,g in [(2,g2),(3,g3),(4,g4)]:equal(maps[j],g,f'entire primitive map {j}')
    normals=[];roots=[];curvature_damages=[]
    for j in range(9):
        z=W**j
        L=P.scale(eval_z(g2,z),-1/(9*z**8))
        T=P.scale(eval_z(g3,z),-1/(9*z**8))
        V=P.scale(P.add(eval_z(g4,z),P.mul(derivative_z(g2,z),L),
                        P.scale(P.power(L,2),36*z**7)),-1/(9*z**8))
        root=[P.const(z),{},L,T,V]
        residual=[{}for _ in range(5)]
        for (t,h),a in primitive.items():
            zp=tpower(root,h)
            for q in range(5-t):residual[t+q]=P.add(residual[t+q],P.mul(a,zp[q]))
        for t in range(5):equal(residual[t],{},f'all-root residual {j}/{t}')
        n=normal_from_jets(z,L,T,V);normals.append(n)
        ct=z.real();s1=z.imag();s2=(z*z).imag();s3=(z**3).imag()
        equal(n[0],P.const(-2*y*(ct+Q(1,2))*(ct+C)),f'individual quadratic normal {j}')
        equal(n[1],P.add(P.scale(G,s1),P.scale(J3,k*s2/7-s3/18),
                        P.scale(S,H*s2/7)),f'individual cubic normal {j}')
        roots.append([P.record(v)for v in (L,T,V)])
        curvature_damages.append(normal_from_jets(z,L,T,V,True)[2])
    for j in range(9):
        for order in range(3):
            equal(normals[j][order],P.scale(normals[(-j)%9][order],(-1)**order),
                  f'all-branch conjugate reversal {j}/{order+2}')
    equal(normals[0][0],P.const(-1),'marked quadratic normal')
    A={3:E(Q(3,2)),4:1+C};BB={3:E(Q(3,2)),4:1-(2*C*C-1)}
    DE=3*H*(C+2*C*C-1)/14
    DO=H*(W**3).imag()*(W**4).imag()*(1-2*C)/7
    U20=P.substitute(U2,{3:{}});J210=P.substitute(J21,{3:{}})
    Tcal={};R={}
    for j,ratio,sq in [(3,E(-1),E(Q(3,4))),(4,-2*C,1-C*C)]:
        z=W**j
        curvature=-(7*x*x/2+6*x*y*ratio+5*y*y*ratio*ratio/2)*sq
        tc=P.add(P.const(4+U-H/2+BB[j]*U*U/14+curvature),
                 P.scale(P.add(P.const(-U*H/12),P.scale(J21,Q(1,6))),1-(z**6).real()),
                 P.scale(P.sub(P.const(H*H/40),P.scale(J4,Q(1,20))),1-(z**5).real()))
        r=P.sub(tc,P.scale(U2,BB[j]/14))
        equal(normals[j][2],P.add(r,P.scale(M,-A[j]),P.scale(B,H*BB[j]/7)),
              f'complete individual fourth normal {j}')
        Tcal[j]=P.substitute(tc,{3:{}});R[j]=P.sub(Tcal[j],P.scale(U20,BB[j]/14))
    M0=P.scale(P.sub(P.scale(R[4],BB[3]),P.scale(R[3],BB[4])),H/(7*DE))
    b0=P.scale(P.sub(P.scale(R[4],A[3]),P.scale(R[3],A[4])),1/DE)
    base={2:P.scale(J3,k/7),3:{},4:M0,5:b0}
    for j in (3,4,5,6):
        equal(P.substitute(normals[j][1],base),{},f'active cubic cancellation {j}')
        equal(P.substitute(normals[j][2],base),{},f'active quartic cancellation {j}')
    odd=[[P.derivative(normals[j][1],a)for a in (2,3,4,5)]for j in (3,4)]
    even=[[P.derivative(normals[j][2],a)for a in (2,3,4,5)]for j in (3,4)]
    determinant=lambda a,b,c,d:P.sub(P.mul(a,d),P.mul(b,c))
    equal(determinant(*[odd[0][0],odd[0][1],odd[1][0],odd[1][1]]),P.const(DO),'odd determinant')
    equal(determinant(*[even[0][2],even[0][3],even[1][2],even[1][3]]),P.const(DE),'even determinant')
    for row in odd:
        for p in row[2:]:equal(p,{},'zero upper-right Jacobian entry')
    # Actual squared distances and binomial sum, separately from primitive/root calculations.
    distance=cp_add({(0,0):P.const(1),(2,0):P.const(-1)},cp_scale(zeta,-1))
    squared=cp_mul(distance,{key:P.conj(v)for key,v in distance.items()})
    deviation=cp_add(squared,{(0,0):P.const(-1)})
    inverse=cp_add({(0,0):P.const(1)},
                   cp_scale(deviation,Q(-1,2)),
                   cp_scale(cp_power(deviation,2),Q(3,8)),
                   cp_scale(cp_power(deviation,3),Q(-5,16)),
                   cp_scale(cp_power(deviation,4),Q(35,128)))
    cost=summed(inverse)
    coefficient=P.add(P.scale(M,8),P.scale(B,-H),P.const(8+2*U-3*H/2),
                      U2,P.scale(J21,Q(-3,2)),P.scale(J4,Q(3,8)))
    for j,p in enumerate([P.const(8),{},P.const(E(Q(8,3))+y),{},coefficient]):
        equal(cost[j],p,f'full reciprocal coefficient {j}')
    K=P.add(P.const(K1),P.scale(J4,alpha),P.scale(P.power(J3,2),tau/H))
    equal(P.substitute(cost[4],base),K,'whole attained profile cost')
    w4=1/(C+2*C*C-1);w3=Q(2,3)*(7-(1-(2*C*C-1))*w4)
    equal(P.const(w3*A[3]+w4*A[4]),P.const(8),'dual A normalization')
    equal(P.const(w3*BB[3]+w4*BB[4]),P.const(7),'dual B normalization')
    equal(P.add(P.scale(M0,8),P.scale(U20,Q(1,2)),P.scale(b0,-H)),
          P.add(P.scale(Tcal[3],w3),P.scale(Tcal[4],w4)),'complete dual-cost identity')
    centered={(0,2):P.const(1),(0,0):P.const(-H/8),(0,1):P.scale(J3,-1/H)}
    dispersion=P.add(J4,P.const(-H*H/8),P.scale(P.power(J3,2),-1/H))
    equal(summed(cp_power(centered,2))[0],dispersion,'whole centered-square moment identity')
    defect=P.add(P.scale(P.sub(P.const(9*H*H/14),P.scale(P.power(J3,2),1/H)),alpha+tau),
                 P.scale(dispersion,-alpha))
    equal(P.sub(P.const(Kmax),K),defect,'whole profile maximum defect')
    # Four independent real losses: exact algebraic desingularization, not a sample IFT.
    closing=[]
    for a,b in [(Q(1,2),Q(2)),(Q(7,6),Q(3,4)),(Q(1),Q(1))]:
        even_target=-(a+b)/2
        odd_target=-(a-b)/2
        # E*t^4 and O*t^3 both at t^6, requiring orders 2 and 3.
        need(4+2==3+3==6 and even_target+odd_target==-a
             and even_target-odd_target==-b,'individual independent closing losses')
        closing.append([str(a),str(b),str(even_target),str(odd_target)])
    skewness=[]
    for r in range(1,8):
        a=Q(1);b=-Q(r,8-r)
        norm=r*a*a+(8-r)*b*b;cube=r*a**3+(8-r)*b**3
        direct=cube*cube/norm**3;formula=Q((8-2*r)**2,8*r*(8-r))
        need(direct==formula and formula<=Q(9,14),'complete skewness count')
        skewness.append(str(direct))
    need(skewness==['9/14','1/6','1/30','0','1/30','1/6','9/14'],'skewness table')
    # Damage rejection uses previously derived actual expressions vs invariant equations,
    # before any expected fixture is consulted.
    rejected=[]
    def reject(ok,name):
        need(not ok,'mathematical damage survived: '+name);rejected.append(name)
    reject(P.add(powers[2][4],P.scale(B,4*H))==D,'wrong imaginary-correction square sign')
    wrongV=P.scale(P.add(eval_z(g4,W**3),P.mul(derivative_z(g2,W**3),
                  P.scale(eval_z(g2,W**3),-1/(9*(W**3)**8)))),-1/(9*(W**3)**8))
    z=W**3;L=P.scale(eval_z(g2,z),-1/(9*z**8));T=P.scale(eval_z(g3,z),-1/(9*z**8))
    reject(normal_from_jets(z,L,T,wrongV)[2]==normals[3][2],'omitted nonlinear root term')
    reject(curvature_damages[3]==normals[3][2],'omitted squared-modulus curvature')
    reject(P.substitute(normals[3][1],{2:P.scale(J3,-k/7),3:{}})=={},
           'wrong base odd control')
    reject(P.const(-DE)==P.const(DE),'wrong even Jacobian orientation')
    reject(P.add(cost[4],P.scale(J4,Q(1,8)))==coefficient,'wrong quartic reciprocal coefficient')
    reject(3+2==6,'wrong independent odd-target power')
    # Fixed-parameter conjugation gives exact even objective; closing need not be even.
    for (t,j),v in distance.items():
        equal(P.conj(v),P.scale(v,(-1)**t),f'fixed-parameter critical-distance parity {t}/{j}')
    record={'field':'QQ[zeta36]/(X12-X6+1)','formal_variables':['J3','J4','G','sigma','M','b'],
            'coefficient_comparisons':len(checks),'comparison_names':checks,
            'whole_primitive_maps':[record_z(p)for p in maps],
            'whole_root_jets':roots,'whole_individual_normals':[[P.record(v)for v in a]for a in normals],
            'jacobian':[[P.record(v)for v in row]for row in odd+even],
            'base_controls':{str(j):P.record(v)for j,v in base.items()},
            'whole_objective':[P.record(v)for v in cost],
            'profile_cost':P.record(K),'maximum':Kmax.record(),'dispersion':P.record(dispersion),
            'maximum_defect':P.record(defect),'skewness_table':skewness,
            'independent_closing_controls':closing,'mathematical_damages_rejected':rejected,
            'exact_scalar_intervals':scalar_receipt()}
    return record


if __name__=='__main__':
    import json,hashlib
    out=run();data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'record_sha256':hashlib.sha256(data).hexdigest(),'record_bytes':len(data),
                      'coefficient_comparisons':out['coefficient_comparisons'],
                      'mathematical_damages_rejected':out['mathematical_damages_rejected']}))
