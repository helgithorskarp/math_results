"""Independent original-root Sturm and rational spectral-mass controls."""
from fractions import Fraction as Q
from integers import original,add,mul,scale,constant,shift

def trim(p):
    p=p[:]
    while p and not p[-1]:p.pop()
    return p
def zd(p):return trim([i*p[i]for i in range(1,len(p))])
def zr(p,q):
    p=trim(p)
    while len(p)>=len(q):
        c=p[-1]/q[-1];s=len(p)-len(q)
        for i,v in enumerate(q):p[i+s]-=c*v
        p=trim(p)
    return p
def sturm(p):
    seq=[trim(p),zd(p)]
    while seq[-1]:
        r=[-v for v in zr(seq[-2],seq[-1])]
        if not r:break
        seq.append(r)
    def variations(pos):
        signs=[(1 if a[-1]>0 else -1)*(-1 if not pos and (len(a)-1)%2 else 1)for a in seq]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variations(False)-variations(True),len(seq[-1])-1
def value(p,x):return sum(Q(v)*x[0]**i*x[1]**j*x[2]**k for (i,j,k),v in p.items())
def matrix_value(B,x):return [[value(p,x)for p in row]for row in B]
def determinant(B):
    B=[r[:]for r in B];out=Q(1)
    for k in range(len(B)):
        if not B[k][k]:
            j=next((j for j in range(k+1,len(B))if B[j][k]),None)
            if j is None:return Q(0)
            B[k],B[j]=B[j],B[k];out=-out
        p=B[k][k];out*=p
        for i in range(k+1,len(B)):
            c=B[i][k]/p
            for j in range(k+1,len(B)):B[i][j]-=c*B[k][j]
    return out
def inverse(B):
    n=len(B);B=[row[:]+[Q(i==j)for j in range(n)]for i,row in enumerate(B)]
    for k in range(n):
        if not B[k][k]:raise ValueError('literal full Hermite inverse pivot')
        p=B[k][k];B[k]=[v/p for v in B[k]]
        for i in range(n):
            if i!=k:
                c=B[i][k];B[i]=[v-c*w for v,w in zip(B[i],B[k])]
    return [row[n:]for row in B]
def positive(B):
    B=[row[:]for row in B];piv=[]
    for k in range(len(B)):
        p=B[k][k]
        if p<=0:raise ValueError('all original literal spectral positive pivots')
        piv.append(str(p))
        for i in range(k+1,len(B)):
            for j in range(i,len(B)):
                B[i][j]-=B[i][k]*B[k][j]/p;B[j][i]=B[i][j]
    return piv

def controls(B,R,Delta,N,P):
    H,r,f,Qp=original();a={(1,0,0):1};D={(0,1,0):1};u={(0,0,1):1}
    powers=[constant(1)]
    for i in range(1,9):powers.append(mul(powers[-1],scale(a,-1)))
    def at_minus_a(p):
        out={}
        for i,c in enumerate(p):out=add(out,mul(c,powers[i]))
        return out
    first=[scale(Qp[i],i)for i in range(1,7)];second=[scale(Qp[i],i*(i-1))for i in range(2,7)]
    curvature=add(add(scale(mul(a,a),-192),scale(mul(mul(a,a),mul(a,a)),768)),add(constant(12),scale(D,-32)))
    if at_minus_a(Qp)!=scale(u,256)or at_minus_a(first)or at_minus_a(second)!=curvature:raise ValueError('all original -a identities')
    moments=[constant(8)]
    for k in range(1,6):
        v=scale(f[8-k],Q(-k,64))
        for j in range(1,k):v=add(v,scale(mul(f[8-j],moments[k-j]),Q(-1,64)))
        moments.append(v)
    if moments[1:]!=[{},constant(1),{},add(constant(Q(1,8)),D),{}]:raise ValueError('all original moment constraints')
    fixtures=[('central-negative-s',(Q(1,3),Q(1,100),Q(1,10**9))),
              ('central-positive-s',(Q(2,5),Q(31,1000),Q(1,10**11)))]
    out=[]
    for name,x in fixtures:
        qq=[value(v,x)/64 for v in Qp];hh=[value(v,x)/64 for v in H]
        count,gcd=sturm(qq);hc,hg=sturm(hh)
        if (count,gcd,hc,hg)!=(6,0,6,0):raise ValueError('actual six simple real originals and all active criticals')
        A=x[0]**2;s=A-Q(1,8);d=x[1]/4-6*s*s
        if not(d>0 and x[2]>0 and x[2]<A*d):raise ValueError('literal original central license')
        Qat=sum(v*x[0]**i for i,v in enumerate(qq))
        if not Qat<0:raise ValueError('literal repeated-original separation')
        bb=matrix_value(B,x);rr=matrix_value(R,x);piv=positive(bb);pivr=positive(rr)
        inv=inverse(bb);action=[[sum(inv[i][k]*rr[k][j]for k in range(6))for j in range(6)]for i in range(6)]
        trace=sum(action[i][i]for i in range(6));eta=sum(action[i][j]*action[j][i]for i in range(6)for j in range(6))
        delta=determinant(bb);nval=value({(2*i,j,k):c for (i,j,k),c in N.items()},x)
        dpval=value({(2*i,j,k):c for (i,j,k),c in Delta.items()},x)
        pval=value({(2*i,j,k):c for (i,j,k),c in P.items()},x)
        if trace!=1 or delta!=dpval or nval!=delta*(1-eta)/2 or pval!=47*x[1]*delta-4*nval:raise ValueError('all original full-mass determinant and inverse identities')
        C=(1-eta)/x[1]
        if not C<Q(47,2):raise ValueError('actual central angular value')
        out.append({'name':name,'a_D_u':[str(v)for v in x],'all_original_simple_roots':6,'active_simple_roots':6,'original_double':str(x[0]),'inactive_full_mass':'0','all_B0_pivots':piv,'all_B1_pivots':pivr,'whole_inverse_trace':str(trace),'whole_inverse_trace_square':str(eta),'whole_C':str(C),'all_original_mass_and_polynomial_positions_paid':True})
    boundary=(Q(1,3),Q(1,216),Q(1,10**9));count,gcd=sturm([value(v,boundary)/64 for v in Qp])
    if count==6:raise ValueError('false original equality-boundary reality license')
    # Entire polynomial identities of the coupled gap inequality, not samples.
    y={(1,0,0):1};k={(0,1,0):1};one=constant(1)
    g=add(add(one,scale(y,-1)),scale(k,-1));k2=mul(k,k)
    v=add(y,k2);total=add(add(one,scale(k,-1)),k2)
    diff=add(v,scale(g,-1))
    if add(mul(total,total),scale(mul(v,g),-4))!=mul(diff,diff):raise ValueError('whole first coupled gap identity')
    rhs=mul(mul(k,add(one,scale(k,-1))),add(add(constant(2),scale(k,-1)),k2))
    if add(one,scale(mul(total,total),-1))!=rhs:raise ValueError('whole second coupled gap identity')
    if not(Q(1,133)**2<Q(1,729*24) and Q(159,6916)>Q(1,133) and Q(159,6916)<Q(1,26) and 24*Q(1,26)**2==Q(6,169) and Q(5,141)<Q(6,169)<Q(1,25)<Q(1,24)):raise ValueError('all whole closed box coverage and cap licenses')
    # Exact positivity margins used in the new whole-central quantitative bound.
    bmin=Q(7885466452528416,815730721)
    c=81*bmin/(2**79*133**8);collar=Q(47,2)-Q(237004387,10097379)
    if c<=Q(1,2**106)or collar<=Q(1,2**106)or Q(1,36)<=Q(1,2**106):raise ValueError('new quantitative central margin')
    if Q(47,2)-Q(5,6)/Q(6,169)!=Q(1,36)or Q(6,169)>=Q(1,25):raise ValueError('whole central upper-band license')
    return {'original_moment_identities':[sorted((list(e),str(v))for e,v in p.items())for p in moments],
      'minus_a_value_derivative_curvature':True,'literal_actual_profiles':out,
      'whole_coupled_gap_identities':True,'whole_closed_box_and_cap_licenses':True,
      'equality_boundary_original_root_count':count,'new_central_deficit_constant':str(c),
      'constant_minus_two_negative_106':str(c-Q(1,2**106)),
      'small_collar_gap':str(collar),'high_D_gap_at_six_over169':'1/36',
      'new_whole_central_claim':'C < 47/2 - 2^-106*(1-24*(A-1/8)^2/D)^2',
      'high_C_outer_band':'1/625 < D <= 5/141; d<0,u<0,24*(A-1/8)^2>D'}
