"""Exact literal/layer identity controls, not finite all-order coverage."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from deficit_full_dual import dual_profile,scalar_square,derivative
from deficit_functional import parameters,phi,optimizer,require,rational_profile

ROOT=HERE
from affine import direct
from model import choose


def layer_energies(n,B,u,ell):
    N=2**n-n-1;s=2**(n-1)-n;h=N-s
    upper=h*sum(comb(n,a)*u[a]**2 for a in u)-sum(
        comb(n,a)*u[a]*B[a][b]*choose(n-a,b)*u[b] for a in u for b in u)
    lower=s*sum(comb(n,a)*ell[a]**2 for a in ell)-sum(comb(n,a)*ell[a] for a in ell)**2+sum(
        comb(n,a)*ell[a]*B[a][b]*choose(n-a,b)*ell[b] for a in ell for b in ell)
    return upper,lower


def layer_identity(n,k):
    construction={24:6,32:8,40:11}[n]
    p=ROOT/f'fixtures/n{n}.json'
    raw=p.read_bytes();d=json.loads(raw);B=direct(n,[Q(v) for v in d['free_values']])
    # A fixed exact multiplier is a proof witness, not a numerical decision.
    lam={24:Q(967,8),32:Q(218,1),40:Q(2745,8)}[n]
    q=dual_profile(n,k,lam)
    N,s,h,r,c=parameters(n,k);bulk=range(k+1,n-k)
    by={v['a']:v for v in q['profiles']}
    u={a:Q(a) if a<=k else Q(s*(n-a),h) if a>=n-k else by[a]['v']+by[a]['t']
       for a in range(1,n-1)}
    ell={a:Q(0 if a<=k else 2 if a>=n-k else 1) for a in u}
    upper,lower=layer_energies(n,B,u,ell)
    z={a:Q(s)-B[a][n-a] for a in bulk}
    term=sum(comb(n,a)*(by[a]['w']-lam)*z[a] for a in bulk)
    proper=sum(comb(n,a)*choose(n-a,b)*(lam-by[a]['f']*by[b]['f'])*B[a][b]
               for a in bulk for b in bulk if a+b<n)
    require(upper+lam*lower==q['bound']+term+proper,'Complete original upper/lower layer identity')
    require(upper>=0 and lower>=0,'Two direct original energies of credited capped seed')
    mass=sum(comb(n,a)*choose(n-a,b)*max(Q(0),B[a][b]) for a in bulk for b in bulk if a+b<n)/(2*h)
    weighted=proper/(2*h*lam)
    require(weighted>=-q['bound']/(2*h*lam),'Original signed weighted mass bound')
    if q['bound']<0:
        require(q['positive_original_mass_floor'] is not None and
                mass>=q['positive_original_mass_floor'],'Positive original mass, max-weight conversion')
    return {'n':n,'k':k,'credited_construction_cutoff':construction,'seed_sha256':hashlib.sha256(raw).hexdigest(),
            'lambda':str(lam),'upper_energy':str(upper),'lower_energy':str(lower),
            'bound':str(q['bound']),'deficit_term':str(term),'proper_term':str(proper),
            'positive_original_mass':str(mass),'signed_weighted_original_mass':str(weighted),
            'exact_mass_floor':str(q['positive_original_mass_floor'])}


def literal_identity():
    n=7;k=2;N,s,h,r,c=parameters(n,k);full=(1<<n)-1
    F=[A for A in range(1,1<<n) if A.bit_count()<=n-2]
    pos={A:i for i,A in enumerate(F)};sizes=[A.bit_count() for A in F];m=len(F)
    B=[[Q(0)]*m for _ in F]
    for i,A in enumerate(F):
        for j in range(i+1,m):
            D=F[j]
            if A&D:continue
            a,b=sizes[i],sizes[j]
            if a==b==1:value=Q(s-(2**(n-2)-2))
            elif min(a,b)==1:value=Q(1)
            elif A|D==full:value=Q(s-1)
            else:value=Q(0)
            B[i][j]=B[j][i]=value
    # Credited ordinary8106 z1 control plus an explicitly new signed
    # affine trade. Each side has zero sum and every point-star sum0.
    u_side={1:Q(1),3:Q(-1),5:Q(-1),7:Q(1)}
    v_side={24:Q(1),56:Q(-1),88:Q(-1),120:Q(1)}
    require(sum(u_side.values())==sum(v_side.values())==0,'Trade side row kernels')
    for side in (u_side,v_side):
        require(all(sum(value for A,value in side.items() if A>>bit&1)==0 for bit in range(n)),
                'Every trade side point-star kernel')
    for A,x in u_side.items():
        for D,y in v_side.items():
            require(not(A&D),'Trade support')
            i,j=pos[A],pos[D];B[i][j]+=x*y/3;B[j][i]+=x*y/3
    C=[[Q(s*int(i==j)-1)+B[i][j] for j in range(m)] for i in range(m)]
    require(all(sum(C[i][j]*sizes[j] for j in range(m))==0 for i in range(m)),
            'Every literal cardinality kernel row')
    stars=0
    for bit in range(n):
        ids=[j for j,A in enumerate(F) if A>>bit&1]
        require(all(sum(C[i][j] for j in ids)==0 for i in range(m)),
                'Every original individual point-star kernel row')
        stars+=m
    require(all(not B[i][j] or not(F[i]&F[j]) for i in range(m) for j in range(m)),
            'All original nonempty supported positions')
    lam=Q(5)
    profile=dual_profile(n,k,lam);by={q['a']:q for q in profile['profiles']}
    bulk=[i for i,a in enumerate(sizes) if k<a<n-k]
    pairs=[(i,j) for i in bulk for j in bulk if i<j and not(F[i]&F[j]) and F[i]|F[j]!=full]
    z={i:Q(s)-B[i][pos[full^F[i]]] for i in bulk}
    require(len(set(z.values()))>1,'Deficits vary on actual vertices')
    ell=[Q(0 if a<=k else 2 if a>=n-k else 1) for a in sizes]
    u=[Q(a) if a<=k else Q(s*(n-a),h) if a>=n-k else by[a]['v']+by[a]['t'] for a in sizes]
    def energy_upper(table):
        return h*sum(x*x for x in u)-sum(u[i]*table[i][j]*u[j] for i in range(m) for j in range(m))
    def energy_lower(table):
        return s*sum(x*x for x in ell)-sum(ell)**2+sum(ell[i]*table[i][j]*ell[j] for i in range(m) for j in range(m))
    def rhs(table):
        term=sum((by[sizes[i]]['w']-lam)*(Q(s)-table[i][pos[full^F[i]]]) for i in bulk)
        proper=2*sum((lam-by[sizes[i]]['f']*by[sizes[j]]['f'])*table[i][j] for i,j in pairs)
        return profile['bound']+term+proper,term,proper
    upper=energy_upper(B);lower=energy_lower(B);right,term,proper=rhs(B)
    require(upper+lam*lower==right and proper!=0,'Complete literal noninvariant original identity')
    require(lower==4*s-4-sum(z.values())+2*sum(B[i][j] for i,j in pairs),
            'Every original lower budget and proper orientation')
    require(upper+lam*lower!=profile['bound']+term+proper/2,'Wrong unordered factor rejected')
    rows=[sum(row) for row in C]
    L=[[Q(1)+sum(rows)]+[Q(1)-x for x in rows]]
    L+=[[Q(1)-rows[i]]+[Q(1)+x for x in row] for i,row in enumerate(C)]
    require(len(L)==N and all(sum(row)==N for row in L),'Every full original row and actual empty lift')
    require(L[0][0]>N,'Affine trade control is explicitly uncapped')
    for i,A in enumerate(F):
        for j,D in enumerate(F):
            require((L[i+1][j+1]-s*int(i==j))/h==B[i][j]/h,
                    'Every actual nonempty original M entry')
            require(not(A&D) or L[i+1][j+1]==s*int(i==j),'Every forbidden full original position')
    damaged=[row[:] for row in B]
    i,j=pos[7],pos[56];damaged[i][j]+=Q(1);damaged[j][i]+=Q(1)
    Cd=[[Q(s*int(i==j)-1)+damaged[i][j] for j in range(m)] for i in range(m)]
    Ca=[sum(Cd[i][j]*sizes[j] for j in range(m)) for i in range(m)]
    defect=sum((sizes[i]-2*u[i])*Ca[i] for i in range(m))
    wrong,_,_=rhs(damaged)
    require(defect!=0 and energy_upper(damaged)+lam*energy_lower(damaged)==wrong+defect,
            'Complete exposed nonkernel defect')
    require(energy_upper(damaged)+lam*energy_lower(damaged)!=wrong,'Damaged kernel rejection')
    return {'n':n,'k':k,'literal_original_vertices':N,'complete_original_positions':N*N,
            'individual_point_star_rows':stars,'noninvariant':True,'nonuniform_deficits':True,
            'signed_trade_ordered_positions':32,'control_is_uncapped_affine_not_H_certificate':True,
            'empty_loop':str(L[0][0]),'lambda':str(lam),'upper_energy':str(upper),
            'lower_energy':str(lower),'bound':str(profile['bound']),
            'deficit_term':str(term),'proper_term':str(proper),'damaged_kernel_defect':str(defect)}


def scalar_controls():
    count=0
    for n,k,lam in ((6,2,Q(3)),(7,2,Q(5)),(8,2,Q(7)),(8,3,Q(7)),
                    (15,3,Q(334125807,8388608)),(24,5,Q(967,8)),
                    (40,10,Q(2745,8)),(65,19,Q(16408463651,16777216)),
                    (121,40,Q(58933170357,16777216))):
        q=dual_profile(n,k,lam)
        N,s,h,r,c=parameters(n,k)
        for p in q['profiles']:
            a=p['a'];lo=p['lo'];hi=p['hi']
            if hi:
                require(derivative(n,a,lo)>lam>=derivative(n,a,hi),'Exact quartic branch selection')
                for z in (Q(0),Q(1,3),Q(2),Q(2*s-2)):
                    left,right=scalar_square(n,a,z,lam,p['v'],p['t'])
                    require(left==right and right>=0,'Both scalar squares and coefficient sign')
                    count+=1
            else:
                require(lam>=a*(n-a) and p['v']==p['t']==0,'Inactive root boundary')
                count+=1
        x=Q(n,2)-Q(k+1)
        # A fixed exact derivative sample establishes strict concavity
        # convention; the all-order derivative proof is written.
        require(all(derivative(n,a,Q(0))>derivative(n,a,Q(1))>derivative(n,a,Q(2))
                    for a in range(k+1,n-k)),'Every sampled layer derivative strictly decreases')
    return count


def free_lower_controls():
    n=6;k=2;N,s,h,r,c=parameters(n,k);full=(1<<n)-1
    F=[A for A in range(1,1<<n) if k<A.bit_count()<=n-2]
    pos={A:i for i,A in enumerate(F)};bulk=[i for i,A in enumerate(F) if A.bit_count()<n-k]
    high=[i for i,A in enumerate(F) if A.bit_count()>=n-k]
    G=len(bulk);K=len(high);records=[]
    require(G==20 and K==15,'Complete free original vertex census')
    for label,value in (('strict',Q(1)),('zero_odd',Q(0)),('rank_one_boundary',Q(4*s,G+2)),
                        ('negative_even',Q(2*s-2)),('noninvariant',None)):
        z={i:Q(1)+Q(min(F[i],full^F[i])%3,5) if value is None else value for i in bulk}
        C=[[Q(s*int(i==j)-1)+(Q(s)-z[i] if i in z and F[i]^F[j]==full else 0)
            for j in range(len(F))] for i in range(len(F))]
        p=Q(K,s)+sum(1/(2*s-z[i]) for i in bulk)
        Gamma=sum(z[i]/(2*s-z[i]) for i in bulk)
        require(p==1-Q(1,s)+Gamma/(2*s),'Complete original rank-one curvature identity')
        root=[Q(1,s) if i in high else 1/(2*s-z[i]) for i in range(len(F))]
        def energy(u):return sum(u[i]*C[i][j]*u[j] for i in range(len(F)) for j in range(len(F)))
        root_energy=energy(root)
        require(root_energy==p*(1-p),'Sharp complete original rank-one direction')
        u=[Q((A%11)-4,7) for A in F];alpha=sum(u)/p
        shifted=[u[i]-alpha*root[i] for i in range(len(F))]
        squares=s*sum(shifted[i]**2 for i in high)
        for i in bulk:
            j=pos[full^F[i]];v=(shifted[i]+shifted[j])/2;t=(shifted[i]-shifted[j])/2
            squares+=(2*s-z[i])*v*v+z[i]*t*t
        require(energy(u)==squares+alpha*alpha*p*(1-p),'Every even/odd/high principal square')
        if label=='strict':require(Gamma<2 and root_energy>0,'Strict free lower')
        if label=='zero_odd':require(Gamma<2 and all(z[i]==0 for i in bulk),'Odd boundary retained')
        if label=='rank_one_boundary':require(Gamma==2 and root_energy==0,'Rank-one boundary retained')
        if label=='negative_even':require(Gamma>2 and root_energy<0,'Explicit negative lower direction')
        records.append({'label':label,'free_original_vertices':len(F),'Gamma':str(Gamma),
                        'root_energy':str(root_energy),'arbitrary_energy':str(energy(u)),'squares':str(squares),
                        'control_is_not_H':True})
    return records


def exclusions():
    records=[]
    for n,k,lam in ((15,3,Q(334125807,8388608)),(65,19,Q(16408463651,16777216)),
                    (121,40,Q(58933170357,16777216))):
        N,s,h,r,c=parameters(n,k);mu=Q((2*n-5)**2,16)
        prior=c+mu*(4*s-4)+r*sum(comb(n,a)*max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n))**2
                               for a in range(k+1,n-k))
        q=dual_profile(n,k,lam)
        require(prior>=0 and q['bound']<0 and q['positive_original_mass_floor']>0,
                'Exact original support exclusion beyond fixed credited eta')
        records.append({'n':n,'k':k,'lambda':str(lam),'credited_fixed_eta':str(prior),
                        'new_safe_bound':str(q['bound']),
                        'positive_original_mass_floor':str(q['positive_original_mass_floor']),
                        'proper_weight_maximum':str(q['maxrho']),
                        'scope':'Excludes S_k for all original real capped H; comparison is only with the fixed credited profile'})
    return records


def schedules():
    records=[]
    for n,k,lam in ((24,6,Q(967,8)),(32,8,Q(218)),(40,11,Q(2745,8)),
                    (48,14,Q(8704273577,16777216)),(64,19,Q(7944054891,8388608)),
                    (96,31,Q(36698256319,16777216))):
        q=dual_profile(n,k,lam);N,s,h,r,c=parameters(n,k)
        G=sum(comb(n,a) for a in range(k+1,n-k));delta=Q(1,4*n*n)
        target=Q(4*s-4)*(1-delta);factor=(target-delta*G)/q['hi_mass']
        by={p['a']:delta+factor*p['hi'] for p in q['profiles']}
        require(factor>0 and all(0<z<2*s-2 for z in by.values()),'All strict actual complementary deficits')
        mass=sum(comb(n,a)*z for a,z in by.items())
        E=c+sum(comb(n,a)*phi(n,a,z) for a,z in by.items())
        require(mass==target<4*s-4 and E>0,'Strict complete budget and complete cap compression')
        curvature=sum(comb(n,a)*z/(2*s-z) for a,z in by.items())
        require(curvature<2,'Complete original bulk/high principal lower is positive definite')
        records.append({'n':n,'k':k,'lambda':str(lam),'delta_floor':str(delta),
                        'theta':str(factor),'energy':str(E),'lower_budget_slack':str(Q(4*s-4)-mass),
                        'free_lower_curvature_slack':str(Q(2)-curvature),
                        'profile_sha256':hashlib.sha256(json.dumps({str(a):str(z) for a,z in by.items()},
                                                      sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                        'is_H':False})
    return records


def sharp_scalar_frontiers(schedule_records):
    values=[]
    by={(p['n'],p['k']):p for p in schedule_records}
    for n,k,lam in ((24,6,Q(967,8)),(32,8,Q(218)),(40,11,Q(2745,8)),
                    (48,14,Q(8704273577,16777216)),(64,19,Q(7944054891,8388608)),
                    (96,31,Q(36698256319,16777216))):
        lower=dual_profile(n,k-1,lam)
        require(lower['bound']<0 and Q(by[n,k]['energy'])>0 and
                Q(by[n,k]['free_lower_curvature_slack'])>0,
                'Sharp finite scalar frontier: negative previous dual and strict original compressions')
        values.append({'n':n,'first_positive_relaxed_cutoff':k,'lower_cutoff':k-1,
                       'lambda':str(lam),'negative_lower_bound':str(lower['bound']),
                       'strict_profile_sha256':by[n,k]['profile_sha256'],
                       'scope':'Exact deficit relaxation including complete free lower; not an actual H support classification'})
    return values


def compression_controls():
    from compression_check import layer_control,literal_control,scalar_controls
    return {'credited_layers':[layer_control(n,k) for n,k in ((24,6),(32,8),(40,11))],
            'noninvariant_original_cardinality_kernel_only':literal_control(),
            'scalar_controls':scalar_controls()}


def main():
    start=time.monotonic()
    strict_schedules=schedules()
    record={'agent':'six-downset-2','role':'researcher','ordinary_proof_unformalized':True,
            'independent_review_pending':True,
            'scope':'Exact finite original identities and dual witnesses; written proof supplies all-order coverage',
            'literal':literal_identity(),
            'credited_complete_layer_controls':[layer_identity(n,k) for n,k in ((24,5),(24,6),(32,7),(32,8),(40,10),(40,11))],
            'scalar_controls':scalar_controls(),'free_lower_controls':free_lower_controls(),
            'fixed_profile_comparisons':exclusions(),
            'strict_partial_schedules':strict_schedules,
            'sharp_scalar_frontiers':sharp_scalar_frontiers(strict_schedules),
            'complete_cap_compression_controls':compression_controls()}
    text=json.dumps(record,sort_keys=True,indent=2)+'\n'
    import argparse
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--output',type=Path)
    group.add_argument('--check',type=Path)
    args=parser.parse_args()
    if args.output:
        args.output.write_text(text)
    else:
        fixture=args.check or HERE/'expected.json'
        require(fixture.read_bytes()==text.encode(), 'Entire typed mathematical fixture mismatch')
    print(json.dumps({'ok':True,'bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest(),
                      'scalar_controls':record['scalar_controls'],'seconds':time.monotonic()-start}))


if __name__=='__main__':main()
