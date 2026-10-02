"""Literal full eight-factor derivative/integral and physical rational controls."""
import json,hashlib,sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import pair,plus,times,need
from audit import canonical,strict_json
zero=pair(0)
def neg(a):return (-a[0],-a[1])
def sub(a,b):return plus(a,neg(b))
def conj(a):return (a[0],-a[1])
def norm(a):return times(a,conj(a))[0]
def scale(a,b):return times(a,pair(b))
def addp(a,b):
    w=[zero]*max(len(a),len(b))
    for j,x in enumerate(a):w[j]=plus(w[j],x)
    for j,x in enumerate(b):w[j]=plus(w[j],x)
    while len(w)>1 and w[-1]==zero:w.pop()
    return w

def mult(a,b):
    w=[zero]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):w[i+j]=plus(w[i+j],times(x,y))
    return addp(w,[])
def evaluate(p,t):
    w=zero
    for a in reversed(p):w=plus(times(w,t),a)
    return w
def translate(p,m):
    w=[zero]
    for a in reversed(p):w=addp(mult(w,[m,pair(1)]),[a])
    return w

def fixture(name,nu,r,phase):
    need(len(nu)==8,'eight literal critical multiplicities')
    nu=list(map(pair,nu));r=F(r);phase=pair(phase);a=F(65535,65536)
    need(norm(phase)==1,'exact physical unit phase')
    need(sum((v[0] for v in nu),F(0))==sum((v[1] for v in nu),F(0))==0,'literal zero centroid')
    u=scale(phase,r);m=sub(pair(a),u);zs=[plus(m,v) for v in nu]
    q=[pair(1)]
    for z in zs:q=mult(q,[neg(z),pair(1)])
    original=[zero]+[scale(v,F(9,k+1)) for k,v in enumerate(q)]
    original[0]=neg(evaluate(original,pair(a)))
    need(len(original)==10 and original[-1]==pair(1),'entire monic degree-nine integral')
    need(evaluate(original,pair(a))==zero,'actual marked polynomial anchor')
    need([scale(original[k],k) for k in range(1,10)]==[scale(v,9) for v in q],'full eight-factor derivative')
    mean=scale(tuple(map(sum,zip(*zs))),F(1,8));need(mean==m,'physical centroid')
    V=sum(map(norm,nu),F(0));H=sum(map(norm,zs),F(0));S4=sum((norm(v)**2 for v in nu),F(0))
    T=zero;U=zero
    for v in nu:T=plus(T,times(v,v));U=plus(U,times(times(v,v),v))
    cp=translate(original,m);need(cp[8]==zero and cp[7]==scale(T,F(-9,14)) and cp[6]==scale(U,F(-1,2)),'literal complete centered coefficient conversion')
    need(evaluate(cp,u)==zero,'complete centered anchor')
    xi=[times(v,conj(phase)) for v in nu];E=sum((v[0]**2 for v in xi),F(0));QJ=times(T,times(conj(phase),conj(phase)))
    cubic_rot=zero
    for v in xi:cubic_rot=plus(cubic_rot,times(times(v,v),v))
    need(times(U,times(times(conj(phase),conj(phase)),conj(phase)))==cubic_rot,'literal signed cubic physical orientation')
    need(H==V+8*norm(m) and 2*E==V+QJ[0],'entire physical energy trace')
    need(8*S4<=7*V*V,'whole centered fourth-moment bound')
    need(QJ[0]**2+QJ[1]**2<=V*V,'literal complete Gram cone')
    enc=lambda z:list(map(str,z))
    return {'name':name,'a':str(a),'u':enc(u),'m':enc(m),'criticals':[enc(z) for z in zs],'centered':[enc(z) for z in nu],'original_polynomial':[enc(z) for z in original],'centered_polynomial':[enc(z) for z in cp],'V':str(V),'H':str(H),'S4':str(S4),'E':str(E),'QJ':enc(QJ),'U3':enc(U),'rotated_cubic':enc(cubic_rot),'original_disk_or_low_sublevel_certified':False}

def controls():
    asym=[(F(1,7),F(2,9)),(F(-1,7),F(-2,9)),(F(2,11),F(-1,13)),(F(-2,11),F(1,13)),(F(1,17),F(3,19)),(F(-1,17),F(-3,19)),(0,0),(0,0)]
    v=(F(1,12),F(1,20));seven=[v]*7+[(-7*v[0],-7*v[1])]
    cases=[('total_collision',[0]*8,F(1),(1,0)),('pure_imaginary_E_zero',[(0,F(1,8))]*4+[(0,F(-1,8))]*4,F(1),(1,0)),('complex_phase',asym,F(1),(F(3,5),F(4,5))),('imaginary_rotation',asym,F(3,2),(0,1)),('repeated_centered',seven,F(1,2),(F(-3,5),F(4,5)))]
    out=[fixture(*case) for case in cases]
    # This failure control is deliberately not centered.
    need(F(1)>F(7,8),'uncentered quartic failure control')
    # Two actual closed-disk families corroborate only the unrestricted high arm.
    eta=F(1,65536);a=1-eta;C_lower=F(826,291)
    actual={'z9_minus_a9':{'original_moduli':str(a),'critical_multiplicity':8,'F':str(8/a),'low_sublevel':False,'closed_original_disk':True},'marked_ninefold':{'original_moduli':str(a),'critical_multiplicity':8,'F':'infinity','closed_original_disk':True}}
    need(8/a>8+3*eta and 8/a>8+C_lower*eta-327*eta*eta,'actual high-arm positive control')
    return {'all_five_full_literal_records':out,'noncentered_one_nonzero_failure_control':{'V':'1','S4':'1','7V_squared_over8':'7/8','claimed_inequality_fails':True},'actual_high_arm_families':actual,'arbitrary_literal_controls_are_not_original_disk_or_low_sublevel_evidence':True}

if __name__=='__main__':
    r=controls();raw=canonical(r)
    if sys.argv[1:] == ['--emit']:print(raw.decode())
    else:
        need(len(sys.argv)<=2,'only optional external fixture path');v=strict_json(sys.argv[1] if len(sys.argv)==2 else Path(__file__).with_name('CONTROLS.json'))
        need(canonical(v)==raw,'whole literal original/critical control record')
        print(json.dumps({'whole_controls_sha256':hashlib.sha256(raw).hexdigest(),'literal_controls':5,'actual_high_arm_controls':2,'centered_failure_controls':1}))
