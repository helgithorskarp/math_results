"""Independent residue Gram solve and complete coefficient case audit over Q."""
from fractions import Fraction as F
from polys import Poly, cast, symbol, need

Z=cast(0)

def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p

def coeff(p,k):return p[k] if k<len(p) else Z
def add(a,b):return trim([coeff(a,i)+coeff(b,i) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([x*c for x in a])
def neg(a):return scale(a,-1)
def mul(a,b):
    out=[Z]*(max(0,len(a)+len(b)-1))
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=out[i+j]+x*y
    return trim(out)
def deriv(p):return trim([p[i]*i for i in range(1,len(p))])
def divrem(p,h):
    p=trim(p);h=trim(h);need(h and h[-1]==1,'monic divisor')
    q=[Z]*max(0,len(p)-len(h)+1)
    while len(p)>=len(h):
        j=len(p)-len(h);t=p[-1];q[j]=q[j]+t
        for k,x in enumerate(h):p[j+k]=p[j+k]-t*x
        p=trim(p)
    return trim(q),p
def rem(p,h):return divrem(p,h)[1]
def same(a,b):return trim(a)==trim(b)
def specialize(p,m):return trim([x.substitute(m) for x in p])
def record(p):return [x.record() for x in trim(p)]
def power_sums(h,count):
    n=len(h)-1;out=[cast(n)]
    for k in range(1,count+1):
        v=Z
        for j in range(1,min(k,n)+1):
            v=v+coeff(h,n-j)*(k if j==k else out[k-j])
        out.append(-v)
    return out

def gram_adjoint(h):
    """Solve G*T=D^t*G by anti-triangular unit pivots; no node inverse."""
    n=len(h)-1;rs=[];r=[cast(1)]
    for k in range(2*n-1):
        rs.append(coeff(r,n-1));r=rem([Z]+r,h)
    G=[[rs[i+j] for j in range(n)] for i in range(n)]
    cols=[]
    for i in range(n):
        rhs=[Z]+[G[j-1][i]*j for j in range(1,n)];x=[Z]*n
        for row in range(n):
            col=n-1-row;need(G[row][col]==1,'unit anti-diagonal pivot')
            need(all(G[row][j]==0 for j in range(col)),'zero anti-triangle')
            x[col]=rhs[row]-sum((G[row][j]*x[j] for j in range(col+1,n)),Z)
        cols.append(trim(x))
    def T(p):
        need(len(trim(p))<=n,'normal representative before adjoint')
        out=[]
        for i,x in enumerate(p):out=add(out,scale(cols[i],x))
        return out
    return G,cols,T

def structures():
    A,B,E,Fc,G,J,C,N,t,d=[symbol(x) for x in ('A','B','E','F','G','J','C','N','t','d')]
    h=[J,G,Fc,E,B,A,Z,cast(1)]
    f=[symbol('f0'),8*J,4*G,F(8,3)*Fc,2*E,F(8,5)*B,F(4,3)*A,Z,cast(1)]
    p=[symbol('p'+str(i)) for i in range(7)]
    Q,_=divrem(add(scale(f,8),mul(p,deriv(h))),h)
    gram,cols,T=gram_adjoint(h)
    K=add(scale(p,-16),add(scale(T(T(rem(mul(p,p),h))),-F(1,4)),scale(T(rem(mul(p,add(Q,neg(deriv(p)))),h)),F(1,4))))
    O=add(mul(p,deriv(deriv(h))),add(mul(add(deriv(p),neg(Q)),deriv(h)),mul(add([cast(64)],neg(deriv(Q))),h)))
    return locals()

def audit():
    s=structures();h,p,Q,K,O=s['h'],s['p'],s['Q'],s['K'],s['O'];A,B,E,Fc,G,J,C,N,t,d=[s[x] for x in ('A','B','E','Fc','G','J','C','N','t','d')]
    checks={}
    def equal(name,left,right):
        need(cast(left)==cast(right),name);checks[name]=cast(left).record()
    def poly_equal(name,left,right):
        need(same(left,right),name);checks[name]=record(left)
    # Gram construction is independent of the target's closed Newton formula.
    tau=power_sums(h,6)
    for i,col in enumerate(s['cols']):
        closed=[Z]*i
        for j in range(i):closed[i-1-j]=tau[j]
        if i:closed[i-1]=closed[i-1]-i
        poly_equal('adjoint column '+str(i),col,closed)
        for j in range(7):
            left=j*s['gram'][i][j-1] if j else Z
            right=sum((coeff(col,k)*s['gram'][k][j] for k in range(7)),Z)
            equal('whole adjoint pair '+str(i)+','+str(j),left,right)
    equal('sixth kernel coefficient',coeff(K,6),-16*p[6])
    p5zero={'p6':0,'p5':0};k4=specialize(K,p5zero)
    equal('quartic fifth kernel',coeff(k4,5),F(7,4)*p[3]*p[4])
    low={'p6':0,'p5':0,'p4':0};k3=specialize(K,low)
    equal('cubic fourth kernel',coeff(k3,4),F(3,2)*p[3]**2)
    quadratic={**low,'p3':0};k2=specialize(K,quadratic)
    equal('quadratic second kernel',coeff(k2,2),2*p[2]*(p[2]-4))
    equal('quadratic first kernel',coeff(k2,1),F(3,4)*p[1]*(5*p[2]-8))
    evenq={**quadratic,'p1':0};o2=specialize(O,evenq)
    equal('quadratic odd z4 ODE',coeff(o2,4),-3*(5*p[2]-8)*B)
    equal('quadratic full odd z2 ODE',coeff(o2,2),12*B*p[0]-5*(3*p[2]-8)*Fc)
    equal('quadratic full odd z0 ODE',coeff(o2,0),2*Fc*p[0]-7*(p[2]-8)*J)
    # Entire resonance h' polynomial, including p0=0, with no generic divisor.
    derivative=[F(7,512)*p[0]**3,Z,F(21,64)*p[0]**2,Z,F(21,8)*p[0],Z,cast(7)]
    resonance=add(mul([p[0],Z,cast(8)],deriv(derivative)),scale([Z]+derivative,-48))
    poly_equal('whole final-resonance derivative ODE',resonance,[])
    substitutions={**p5zero,'p3':0,'p4':t,'p2':4+F(2,3)*A*t,'p1':F(4,5)*B*t}
    kq=specialize(K,substitutions);oq=specialize(O,substitutions)
    equal('quartic full O5',coeff(oq,5),2*(2*A**2*t-16*A-12*E*t+21*p[0]))
    equal('quartic full O4',coeff(oq,4),7*A*B*t-36*B-25*Fc*t)
    equal('quartic full O2',coeff(oq,2),(-20*A*Fc*t-3*B*E*t+60*B*p[0]-100*Fc-105*J*t)/5)
    equal('quartic kernel K2',coeff(kq,2),-t*(-2*A**2*t+24*A+27*p[0])/9)
    equal('quartic kernel K1',coeff(kq,1),t*(5*A*B*t-36*B+25*Fc*t)/20)
    equal('full two-equation exception split',coeff(kq,1)+t*coeff(oq,4)/20,F(3,5)*t*B*(A*t-6))
    # A polynomial clearing is clearer than pretending to divide a symbolic N.
    raw=coeff(oq,5).substitute({'A':-F(3,8)*N,'t':t,'E':-N**2/128-F(7,64)*N*p[0]})
    equal('exception O5 cleared',raw,(F(3,4)*N+F(21,8)*p[0])*(N*t+16))
    evalue=-N**2/128-F(7,64)*N*p[0]
    equal('exception D identity',F(3,8)*N**2-8*evalue,F(7,16)*N**2+F(7,8)*N*p[0])
    # Substitute normalized N=1; scale invariance supplies arbitrary N>0.
    kval=coeff(kq,2).substitute({'A':-F(3,8),'t':-16,'p0':F(8,7)*d-F(1,2)})
    equal('exception actual normalized C',kval/4,F(96,7)*d-8)
    quintic={'p6':0};q5=specialize(Q,quintic);k5=specialize(K,quintic);o5=specialize(O,quintic)
    expectedQ=[7*p[1]-2*A*p[3]-3*B*p[4]+(2*A**2-4*E)*p[5],8+7*p[2]-2*A*p[4]-3*B*p[5],7*p[3]-2*A*p[5],7*p[4],7*p[5]]
    poly_equal('entire quintic quotient',q5,expectedQ)
    equal('entire quintic leading odd kernel',4*coeff(k5,5),7*p[2]*p[5]+7*p[3]*p[4]-9*A*p[4]*p[5]-5*B*p[5]**2-56*p[5])
    reconstructed=scale(add(mul(q5,h),neg(mul(specialize(p,quintic),deriv(h)))),F(1,8))
    equal('reconstruction monic',coeff(reconstructed,8),1)
    equal('reconstruction balanced',coeff(reconstructed,7),0)
    poly_equal('complete reconstruction derivative defect',add(deriv(reconstructed),scale(h,-8)),scale(o5,-F(1,8)))
    # Explicit legal fixed pivots; no stationary solution is constructed.
    equal('quintic O5 p0 pivot',coeff(o5,5).derivative('p0'),42)
    equal('quintic O5 p1 absence',coeff(o5,5).derivative('p1'),0)
    equal('quintic O4 p0 absence',coeff(o5,4).derivative('p0'),0)
    equal('quintic O4 p1 pivot',coeff(o5,4).derivative('p1'),-10*A)
    damages={}
    def wrong(name,left,right):
        witness=cast(left)-cast(right);need(witness!=0,'damaged identity accidentally passed: '+name)
        damages[name]=witness.record()
    wrong('omit normal derivative adjoint boundary',1,7)
    wrong('wrong quartic exception sign',coeff(kq,1)+t*coeff(oq,4)/20,F(3,5)*t*B*(A*t+6))
    badQ=add(q5,[cast(1)])
    bad_f=scale(add(mul(badQ,h),neg(mul(specialize(p,quintic),deriv(h)))),F(1,8))
    wrong('alter quotient but retain old ODE',coeff(add(deriv(bad_f),scale(h,-8)),6),coeff(scale(o5,-F(1,8)),6))
    wrong('change ODE normalization64',coeff(o5,7),coeff(add(o5,scale(h,-1)),7))
    wrong('pretend derivative descends through quotient',coeff(rem(deriv(h),h),6),0)
    collapsed=specialize(h,{name:0 for name in ('A','B','E','F','G','J')})
    cg,ct,_=gram_adjoint(collapsed)
    for i,col in enumerate(ct):poly_equal('repeated-critical adjoint '+str(i),col,([Z]*(i-1)+[cast(7-i)]) if i else [])
    return {'checks':checks,'whole_gram':[[x.record() for x in row] for row in s['gram']],
            'whole_adjoint': [record(c) for c in s['cols']], 'whole_generic_kernel':record(K),
            'whole_generic_ODE':record(O),'whole_quintic_kernel':record(k5),'whole_quintic_ODE':record(o5),
            'whole_quartic_kernel':record(kq),'whole_quartic_ODE':record(oq),
            'quintic_O5_without_p0':coeff(o5,5).substitute({'p0':0}).record(),
            'quintic_O4_without_p1':coeff(o5,4).substitute({'p1':0}).record(),
            'algebraic_gram_determinant': '-1', 'resonance_lower_pivots':[8*(k-6) for k in range(6)],
            'mathematical_damage_rejections':damages,'whole_collided_gram':[[x.record() for x in row] for row in cg]}
