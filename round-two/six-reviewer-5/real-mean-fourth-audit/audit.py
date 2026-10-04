"""Independent full mean-channel audit. Written target exposed, native excluded.

Own REVIEW10246 Phi36 Fraction/jet framework explicitly reused; new mean
family, compensation, complete coefficient checks and repair stability.
No target fixture, executable, CAS, solver or floating-point input.
"""
import argparse, hashlib, json, sys
from pathlib import Path
from fractions import Fraction as Q
from math import comb
sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import F, R, J, W, I, C, zproduct, zeval, inverse_sqrt
from signs import equal, require, bound, ratio


def constants():
    y=1/(3*(1+C));x=F(Q(2,3))-y;H=14*y;rho=(C-5)/3
    uz=(-8*x+rho*H)/8;up=uz-rho*H/2
    w2=(F(Q(2512,27))+5840*C/9-21392*C*C/27)/8
    gamma=F(Q(13,36))+1253*C/72-50*C*C/3
    m0=-F(Q(17403419,34992))-45702565*C/17496+180635*C*C/54
    b0=-F(Q(1162307,23328))-5484833*C/11664+52426519*C*C/93312
    M0=F(Q(8148040331,629856))+78878749667*C/1259712-51194418673*C*C/629856
    beta0=F(Q(27821775167,17915904))+80418819893*C/8957952-12650091319*C*C/1119744
    m1=56*(C-C*C)/9;b1=F(Q(1,2))+2*C
    M1=-F(Q(51583,972))-175385*C/486+448*C*C
    beta1=F(Q(1771,324))-94039*C/1296+12347*C*C/162
    beta2=2*(1+C)/7
    Bstar=F(Q(2311,108))+4934*C/27-1976*C*C/9
    Tstar=-F(Q(60800959,17496))-307083769*C/17496+10980067*C*C/486
    Gstar=F(Q(183619658945,2519424))+444829186913*C/1259712-288729410449*C*C/629856
    linear=-F(Q(101920,243))-1218245*C/486+251888*C*C/81
    mustar=-3*linear/8
    Gmean=F(Q(340367352475,839808))+808137564635*C/419904-1052841914857*C*C/419904
    return locals()


def family(damage='none', repairs=False, repair_order=4):
    c=constants();mu=R([0,1]);e=J([0,1]);eta=e*e
    # All degree<=10 coefficients have mu-degree<=2. Repairs enter degree8
    # affinely, with no mu-repair/product term before degree12/16. Thus
    # powers3 and4 encode independent repair coordinates injectively.
    dm=R([0,0,0,1]) if repairs else R()
    db=R([0,0,0,0,1]) if repairs else R()
    m=c['m0']+c['m1']*mu;b=c['b0']+c['b1']*mu
    M=c['M0']+c['M1']*mu+(dm if repair_order==4 else 0)
    beta=c['beta0']+c['beta1']*mu+c['beta2']*mu*mu+(db if repair_order==4 else 0)
    if repair_order==3:m=m+dm;b=b+db
    if damage=='third':m=R(c['m0'])
    if damage=='pair-third':b=R(c['b0'])
    if damage=='fourth':M=R(c['M0'])+dm
    if damage=='pair-fourth':beta=R(c['beta0'])+db
    if damage=='M':M=M+1
    if damage=='beta':beta=beta+1
    inward=0 if damage=='inward' else 1
    A=c['uz']*eta+(c['w2']-mu/3)*(eta**2)+m*(eta**3)+M*(eta**4)+inward*(e**9)
    B=c['up']*eta+(c['w2']+mu)*(eta**2)+m*(eta**3)+M*(eta**4)+inward*(e**9)
    if damage=='balance':A=A+mu*(eta**2)
    K=I*(1+c['gamma']*eta+b*(eta**2)+beta*(eta**3))
    D=[J(1)]
    for _ in range(6):D=zproduct(D,[-A,J(1)])
    D=[9*v for v in zproduct(D,[B*B-eta*c['H']/2*K*K,-2*B,J(1)])]
    if damage=='multiplicity':D[8]=J(8)
    p=[J()]+[v/(j+1) for j,v in enumerate(D)]
    anchor=1-eta if damage!='anchor' else 1-2*eta
    p[0]=-zeval(p,anchor)
    return c,mu,e,A,B,K,D,p,dm,db


def packed(a):
    if isinstance(a,F):return [[j,ratio(x)] for j,x in enumerate(a.v) if x]
    if isinstance(a,R):return [[j,packed(x)] for j,x in enumerate(a.v) if x]
    if isinstance(a,J):return [[j,packed(x)] for j,x in enumerate(a.v) if x]
    raise TypeError('exact sparse record')


def core(damage='none', repairs=False):
    c,mu,e,A,B,K,D,p,dm,db=family(damage,repairs);eta=e*e;a=1-eta
    equal(W**12-W**6+1,F(),'Phi36');equal(W**18,F(-1),'physical embedding')
    equal(8*C**3-6*C-1,F(),'physical cubic');equal(I*I,F(-1),'imaginary unit')
    equal(p[9],J(1),'whole monic');equal(zeval(p,a),J(),'whole actual anchor')
    # Genuinely separate all-eight power sums/Newton elementary recurrence.
    ps=[J()]
    for k in range(1,9):
        pair=2*sum((comb(k,m)*(B**(k-m))*((eta*c['H']/2*K*K)**(m//2)) for m in range(0,k+1,2)),J())
        ps.append(6*(A**k)+pair)
    elem=[J(1)]
    for n in range(1,9):elem.append(sum((((-1)**(k-1))*elem[n-k]*ps[k] for k in range(1,n+1)),J())/n)
    for j in range(9):equal(D[j],9*((-1)**(8-j))*elem[8-j],'whole Newton primitive column '+str(j))
    VA=(a-A)*(a-A);VB=(a-B)*(a-B)+eta*c['H']/2*K*K.conjugate()
    obj=(5 if damage=='cost-multiplicity' else 6)*inverse_sqrt(VA)+2*inverse_sqrt(VB)
    G=R(c['Gstar'])+c['linear']*mu+Q(4,3)*mu*mu
    wanted={0:R(8),2:R(F(Q(8,3))+c['y']),4:R(c['Bstar']),6:R(c['Tstar']),8:G+8*dm-c['H']*db,9:R(8)}
    for n in range(10):equal(obj.v[n],wanted.get(n,R()),'whole direct FIRST coefficient '+str(n))
    equal(G,R(c['Gmean'])+Q(4,3)*(mu-c['mustar'])**2,'whole completed square')
    equal(c['Gmean'],c['Gstar']-3*c['linear']**2/16,'whole strict improvement identity')
    equal(6*(A.imag()**3)+2*(B.imag()**3)+3*c['H']*eta*B.imag()*(K.imag()**2),J(),'whole zero cubic imaginary moment')
    d0=C+2*C*C-1;w4=1/d0;w3=Q(2,3)*(7-(2-2*C*C)*w4)
    equal(Q(3,2)*w3+(1+C)*w4,F(8),'positive dual first column')
    equal(Q(3,2)*w3+(2-2*C*C)*w4,F(7),'positive dual pair column')
    q3=-Q(3,2)*dm+c['H']*Q(3,14)*db
    q4=-(1+C)*dm+c['H']/7*(2-2*C*C)*db
    equal(8*dm-c['H']*db,-w3*q3-w4*q4,'whole dual objective elimination')
    # Exact inverse cone and sharp vertices, new mean-gap stability.
    u=R([0,1]);v=R([0,0,1]);pair=(v-Q(2,3)*(1+C)*u)*7/c['H']/d0
    center=Q(2,3)*u+pair*c['H']/7
    equal(Q(3,2)*(center-pair*c['H']/7),u,'inverse first deficit')
    equal((1+C)*center-(2-2*C*C)*pair*c['H']/7,v,'inverse second deficit')
    equal(8*center-c['H']*pair,w3*u+w4*v,'entire cone cost')
    vertices=((2*(C-1)/(16*C-9),-1/(16*C-9)),(F(1),F(1)))
    for M,scaled in vertices:equal(8*M-7*scaled,F(1),'unit-gap simplex vertex')
    va,vb=vertices
    equal(Q(3,2)*(va[0]-va[1]),1/w3,'first vertex first deficit')
    equal((1+C)*va[0]-(2-2*C*C)*va[1],F(),'first vertex second deficit')
    equal(Q(3,2)*(vb[0]-vb[1]),F(),'second vertex first deficit')
    equal((1+C)*vb[0]-(2-2*C*C)*vb[1],1/w4,'second vertex second deficit')
    signs={'H':c['H'],'negative L':-c['linear'],'mu*>8':c['mustar']-8,'16>mu*':16-c['mustar'],
           'negative Gstar':-c['Gstar'],'strict improvement':3*c['linear']**2/16,'negative Gmean':-c['Gmean'],
           'dual w3':w3,'dual w4':w4,'real determinant':2*C-1,'d0':d0,
           'vertex denominator>one':16*C-10,'vertex real lower':1+vertices[0][0],
           'vertex real upper':1-vertices[0][0],'vertex pair lower':1+vertices[0][1],'vertex pair upper':1-vertices[0][1]}
    intervals={}
    for name,value in signs.items():
        lo,hi=bound(value);require(lo>0,'exact physical positive sign '+name);intervals[name]=[ratio(lo),ratio(hi)]
    return dict(route='core-repairs' if repairs else 'core',primitive=[packed(v) for v in p],powers=[packed(v) for v in ps],objective=packed(obj),G=packed(G),dual=[packed(w3),packed(w4)],vertices=[[packed(v) for v in x] for x in vertices],signs=intervals)


def root(label, damage='none', repairs=False):
    c,mu,e,A,B,K,D,p,dm,db=family(damage,repairs);o=W**(4*label)
    # Literal Taylor-column contraction, differs from author's order-by-order
    # recursion; complete composed equation is then checked separately.
    tc=[sum((p[j]*comb(j,m)*(o**(j-m)) for j in range(m,10)),J()) for m in range(6)]
    delta=J()
    for _ in range(6):
        residual=tc[0]+(tc[1]-9*(o**8))*delta
        for m in range(2,6):residual=residual+tc[m]*(delta**m)
        delta=-residual*(o/9)
    z=o+delta;equal(zeval(p,z),J(),'every composed original equation '+str(label))
    equal(z.v[1],R(),'no epsilon first drift')
    equal(z.v[2],R(-o/3-c['x']-c['y']*o.conjugate()),'literal first original drift')
    normal=(z*z.conjugate()-1)/2
    Aj=F(1)-(o+o.conjugate())/2;Bj=F(1)-(o*o+o.conjugate()**2)/2
    leading=-(F(Q(1,3))+c['x']*(1-Aj)+c['y']*(1-Bj))
    equal(normal.v[0],R(),'unit original');equal(normal.v[1],R(),'zero epsilon normal')
    equal(normal.v[2],R(leading),'whole first half-normal')
    for n in (3,5,7):equal(normal.v[n],R(),'whole odd lower original normal')
    if label in (3,4,5,6):
        equal(leading,F(),'each active first normal')
        for n in range(3,8):equal(normal.v[n],R(),'each compensated lower normal '+str(n))
        equal(normal.v[8],-Aj*dm+c['H']/7*Bj*db,'whole active fourth mean/repair normal')
        equal(normal.v[9],R(-Aj),'each target ninth normal')
    else:require(bound(-leading)[0]>0,'each other actual root strictly interior')
    if label==0:equal(z,1-e*e,'entire original anchor branch')
    return dict(route='root-repairs' if repairs else 'root',label=label,root=packed(z),normal=packed(normal),first=packed(leading),columns=[packed(Aj),packed(c['H']/7*Bj)],raw_normal=normal,raw_root=z)


def columns(damage='none'):
    rows=[];c,mu,e,A,B,K,D,p,dm,db=family()
    for q in (3,4):
        *_,changed,dm,db=family(repairs=True,repair_order=q)
        responses=[changed[j].v[2*q]-p[j].v[2*q] for j in range(10)]
        expected=[9*dm-9*c['H']/7*db]+[R()]*6+[9*c['H']/7*db,-9*dm,R()]
        if damage=='column':expected[7]=expected[7]+db
        for j in range(10):equal(responses[j],expected[j],'entire leading actual repair primitive '+str((q,j)))
        normals=[]
        for label in range(9):
            o=W**(4*label);Aj=1-(o+o.conjugate())/2;Bj=1-(o*o+o.conjugate()**2)/2
            response=-sum((responses[j]*(o**j) for j in range(10)),R())*(o/9)
            normal=(response*o.conjugate()).real()
            equal(normal,-Aj*dm+c['H']/7*Bj*db,'both repair columns each original '+str((q,label)))
            normals.append(packed(normal))
        rows.append(dict(order=q,primitive=[packed(v) for v in responses],all_original_normals=normals))
    equal(-Q(3,2)*c['H']/7*(2-2*C*C)+Q(3,2)*(1+C)*c['H']/7,2*C-1,'physical two-row determinant')
    return dict(route='columns',rows=rows)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--route',choices=('core','root','columns'),required=True)
    parser.add_argument('--label',type=int,default=3);parser.add_argument('--repairs',action='store_true')
    parser.add_argument('--damage',default='none');parser.add_argument('--output',required=True);args=parser.parse_args()
    require(type(args.label) is int and 0<=args.label<=8,'valid original label')
    require(args.damage in ('none','third','pair-third','fourth','pair-fourth','M','beta','inward','balance','multiplicity','anchor','cost-multiplicity','column'),'known damage')
    if args.route=='core':out=core(args.damage,args.repairs)
    elif args.route=='root':out=root(args.label,args.damage,args.repairs)
    else:out=columns(args.damage)
    out.pop('raw_normal',None);out.pop('raw_root',None)
    b=json.dumps(out,sort_keys=True,separators=(',',':')).encode();Path(args.output).write_bytes(b+b'\n')
    print(json.dumps(dict(route=out['route'],label=out.get('label'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())))


if __name__=='__main__':main()
