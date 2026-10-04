"""Independent all-original sparse q18 primal, derivative, universal dual, and new gates."""
from collections import Counter
from fractions import Fraction as F
import copy,hashlib
from geometry import literal,typ,build,repairs,integer,need,canon,outerlift
from blocks import inspect
DEN=148635648;KDEN=9072;OLD=16384;CENTER=F(1,128);EXTENDED=F(1,64)
ZZ=(0,2,0);WW=(0,0,2);BCW=(6,0,1);ZS=(0,1,0);WS=(0,0,1);ABC=(7,0,0)

def key(a,b):return tuple(sorted((a,b)))


def inputs(cert,comparison):
    need(integer(cert['free_original_entry_denominator'],'new denominator')==DEN,'correct nondyadic denominator')
    keys=[tuple(tuple(integer(x,'orbit integer') for x in t) for t in k) for k in cert['free_original_entry_orbit_keys']]
    need(keys==sorted(set(keys)) and len(keys)==143 and all(len(k)==2 and all(len(t)==3 for t in k) and k[0]<=k[1] for k in keys),'complete orbit key schema')
    values=cert['free_original_entry_numerators'];need(type(values)is list and len(values)==143,'all new values');values=[integer(x,'new coefficient integer') for x in values]
    old= comparison['comparison_free_numerators'];need(type(old)is list and len(old)==143,'all old values');old=[integer(x,'old coefficient integer') for x in old]
    need(integer(comparison['comparison_free_denominator'],'old denominator')==OLD,'historical denominator')
    return keys,dict(zip(keys,old)),values


def recipe(old,tau):
    dz=F(32877,OLD)+tau;dw=F(36259,OLD)+tau;db=F(999,OLD)+tau
    a=(dz-db/4)/36;b=db/36;w=(dw-dz+db/4)/21;p=(F(476335,32768)+41*tau)/81;t=(F(20819,OLD)+tau)/9
    delta={key(ZZ,WW):-a,key(ZZ,BCW):-b,key(WW,WW):-w,key(ZS,WS):p,key(ZS,ABC):-t}
    table={k:F(n,OLD)+delta.get(k,F(0)) for k,n in old.items()};result={}
    for k,v in table.items():
        num=v*DEN;need(num.denominator==1,'entire affine coefficient integral decoder');result[k]=num.numerator
    return result,dict(a=str(a),b=str(b),w=str(w),p=str(p),t=str(t))


def derivative(D):
    proper=D[1:];anchor=proper.index(1);slopes={key(ZZ,WW):F(-1,48),key(ZZ,BCW):F(-1,36),key(WW,WW):F(-1,84),key(ZS,WS):F(41,81),key(ZS,ABC):F(-1,9)}
    K=[[0]*277 for _ in proper];counts=Counter()
    for i,A in enumerate(proper):
        for j,B in enumerate(proper[:i]):
            if A&B or anchor in (i,j):continue
            k=key(typ(A),typ(B));s=slopes.get(k,F(0));v=s*KDEN;need(v.denominator==1,'whole derivative integer');K[i][j]=K[j][i]=v.numerator
            if s:counts[k]+=1
    need([counts[k] for k in slopes]==[1296,324,378,81,9],'whole five-type slope census')
    for i,A in enumerate(proper):
        if not A&1:K[i][anchor]=K[anchor][i]=-sum(K[i][j] for j,B in enumerate(proper) if B&1 and j!=anchor)
    need(all(sum(row[j] for j,B in enumerate(proper) if B&1)==0 for row in K),'every derivative star row')
    need(sum(K[i][anchor]!=0 for i in range(277))==9 and all(K[i][anchor]==1008 for i in range(277) if K[i][anchor]),'every anchored slope')
    r=[sum(row) for row in K];A=[[sum(r) if i==j==0 else -r[(i or j)-1] if not i or not j else K[i-1][j-1] for j in range(278)] for i in range(278)]
    need(all(sum(row)==0 for row in A),'every actual derivative row')
    need(all(not D[i]&D[j] or A[i][j]==0 for i in range(278) for j in range(278)),'all original derivative support')
    f2=F(sum(x*x for row in K for x in row),KDEN*KDEN);need(f2==F(198145,4536) and f2<F(53,8)**2,'whole original proper Frobenius slope budget')
    return K,A,dict(slope_denominator=KDEN,frobenius_squared=str(f2),rational_operator_upper='53/8',whole_proper_derivative_sha256=hashlib.sha256(canon(K)).hexdigest(),whole_actual_lift_derivative_sha256=hashlib.sha256(canon(A)).hexdigest(),original_proper_positions=76729,original_actual_positions=77284,five_nonanchor_counts=[counts[k] for k in slopes],anchor_slots=9)


def dual(D,Co,Mo,damage='none'):
    claimed_slope=40 if damage=='dual' else 41
    proper=D[1:];anchor=proper.index(1);bad={i for i,A in enumerate(proper) if not A&1 and Mo[0][i+1]<0};need(len(bad)==81,'all bad nonstar rows')
    need(Counter(typ(proper[i]) for i in bad)==Counter({ZZ:36,WW:36,BCW:9}),'whole bad type census')
    allbad=[i for i in range(278) if Mo[0][i]<0];need(len(allbad)==82 and D.index(7) in allbad,'abc included only in total negative rows')
    d=-F(sum(Mo[0][i+1] for i in bad),OLD);ell=F(Mo[0][0],OLD);base=(d-ell)/2
    need(d==F(2497887,OLD) and ell==F(2021552,OLD) and base==F(476335,32768),'whole old deficits/loop/dual constant')
    need(2*claimed_slope==len(bad)+1,'universal floor parameter coefficient')
    edges=[];counts=Counter();gens=0;trades=0
    for i,A in enumerate(proper):
        for j,B in enumerate(proper[:i]):
            if A&B or anchor in (i,j):continue
            gens+=1;R={(i,j):1,(j,i):1}
            if (A&1)!=(B&1):
                trades+=1;r=i if not A&1 else j;R[r,anchor]=R[anchor,r]=-1;k=0
            else:need(not A&1 and not B&1,'no star/star free edge');k=int(i in bad)+int(j in bad);edges.append((i,j,k));counts[k]+=1
            lift=outerlift(R);badcoef=sum(lift.get((0,r+1),0) for r in bad);loopcoef=lift.get((0,0),0)
            if A&1 or B&1:need(badcoef==loopcoef==0,'each trade absent from cost/dual')
            else:
                need(badcoef==-k and loopcoef==2,'every actual NN dual coefficient')
                need(badcoef+loopcoef+k==2 and -(badcoef+loopcoef)+(2-k)==0,'each positive/negative formal dual variable coefficient')
    need(gens==29802 and trades==10280 and len(edges)==19522 and counts==Counter({0:7885,1:9009,2:2628}),'whole dual/generator census')
    return bad,edges,dict(old_nonstar_deficit=str(d),old_loop_C_units=str(ell),optimum_intercept=str(base),optimum_slope=41,bad_nonstar_rows=sorted(bad),all_old_negative_actual_empty_rows=allbad,NN_k_census=sorted(counts.items()),all29802_actual_generator_dual_coefficients_checked=True,all19522_positive_negative_symbolic_pairs_checked=True,anchored_cost_zero_columns=trades,entry_slack_sum_upper='2*Delta',NN_sign_cone_l1_distance_upper='2*Delta',claim_is_not_distance_to_feasible_optimal_set=True)


def endpoint(D,C,U,L,M,Co,bad,edges,tau):
    tauD=tau*DEN;need(tauD.denominator==1,'floor integral decoder');tauN=tauD.numerator;allowed=[];zero=[];slacks=[]
    for i,A in enumerate(D):
        for j,B in enumerate(D):
            if A&B:continue
            s=M[i][j]-tauN;need(s>=0,'every original allowed floor at affine endpoint');allowed.append(M[i][j]);slacks.append(s)
            if M[i][j]==0:zero.append([i,j])
    need(len(allowed)==60597,'entire allowed ordered census')
    pos=neg=penalty=0;signs=Counter()
    for i,j,k in edges:
        r=C[i][j]-Co[i][j]*(DEN//OLD);p=max(r,0);n=max(-r,0);pos+=p;neg+=n;penalty+=k*p+(2-k)*n;signs['positive' if r>0 else 'negative' if r<0 else 'zero']+=1
    Bsum=sum(M[0][i+1]-tauN for i in bad);loop=M[0][0]-tauN
    need(Bsum==loop==penalty==0,'all primal dual equality channels')
    need(F(pos,DEN)==F(476335,32768)+41*tau and F(neg,DEN)==F(2497887,OLD)/2+F(81,2)*tau,'whole increasing/decreasing NN masses')
    need(signs==Counter(positive=81,negative=1998,zero=17443),'every NN primal sign')
    need(F(M[0][0],DEN)==tau,'actual empty loop floor')
    if tau==0:need(len(zero)==165,'entire zero-floor endpoint census')
    return dict(tau=str(tau),minimum_allowed_entry=str(F(min(allowed),220*DEN)),minimum_floor_slack_C_units=str(F(min(slacks),DEN)),zero_actual_entries=zero,P=str(F(pos,DEN)),T=str(F(neg,DEN)),loop_C_units=str(F(M[0][0],DEN)),all_entry_positions=77284,allowed_entry_positions=60597,NN_sign_census=dict(signs),whole_original_matrix_sha256={k:hashlib.sha256(canon(v)).hexdigest() for k,v in [('C',C),('U',U),('L',L),('M_numerators',M)]})


def sharp_cycle(D,endpoints,Co,bad,edges,damage):
    proper=D[1:];lookup={A:i for i,A in enumerate(proper)};A=(1<<3)|(1<<4);B=(1<<5)|(1<<6);G=1<<7;H=(1<<12)|(1<<13);ids=[lookup[x] for x in (A,B,G,H)];a,b,g,h=ids
    need(a in bad and b in bad and h in bad and g not in bad,'cycle uses three bad vertices and one good vertex')
    R={(a,g):1,(g,a):1,(b,g):-1,(g,b):-1,(a,h):-1,(h,a):-1,(b,h):1,(h,b):1};lift=outerlift(R)
    need(all(i and j for i,j in lift),'empty entries completely unchanged by cycle')
    need(all(sum(v for (i,j),v in R.items() if i==r)==0 for r in ids),'every cycle row zero')
    x={a:1,b:-1};y={g:1,h:-1};need(all(v==x.get(i,0)*y.get(j,0)+y.get(i,0)*x.get(j,0) for (i,j),v in R.items()) and len(R)==8,'whole rank-two cycle outer-product identity')
    need(sum(v*v for v in x.values())==sum(v*v for v in y.values())==2 and not set(x)&set(y),'exact disjoint vector norms giving operator norm2')
    t=F(1,1024);T=t*DEN;need(T.denominator==1,'cycle integral perturbation');tn=T.numerator
    rows=[]
    for tau,(C,U,L,M) in endpoints.items():
        if tau==CENTER:continue
        for sign in (-1,1):
            Cp=[r[:] for r in C];Up=[r[:] for r in U];Mp=[r[:] for r in M]
            for (i,j),v in R.items():Cp[i][j]+=sign*tn*v;Up[i][j]-=sign*tn*v
            for (i,j),v in lift.items():Mp[i][j]+=sign*tn*v
            need(all(sum(row)==220*DEN for row in Mp),'all cycle original rows')
            need(all(not X&Y or Mp[i][j]==0 for i,X in enumerate(D) for j,Y in enumerate(D)),'whole cycle support')
            tauN=(tau*DEN).numerator;minimum=min(Mp[i][j]-tauN for i,X in enumerate(D) for j,Y in enumerate(D) if not X&Y);need(minimum>=0,'whole cycle allowed entry rectangle corners')
            pos=badpos=goodneg=cross=V=0
            for i,j,k in edges:
                r=Cp[i][j]-Co[i][j]*(DEN//OLD);pos+=max(r,0)
                if k==2:badpos+=max(r,0)
                elif k==0:goodneg+=max(-r,0)
                else:cross+=abs(r)
            gap=F(pos,DEN)-F(476335,32768)-41*tau;V=F(badpos+goodneg+cross,DEN)
            need(badpos==goodneg==0 and gap==t and V==2*t,'sharp actual cost/stability pair')
            if damage=='stability':need(V<=gap,'deliberately false unit stability constant')
            rows.append(dict(tau=str(tau),cycle_parameter=str(sign*t),actual_cost_gap=str(gap),NN_sign_distance=str(V),minimum_entry_slack_C_units=str(F(minimum,DEN))))
    floor=F(11,1024)-2*t;need(floor==F(9,1024)>0,'proper real rectangle spectral floor')
    return dict(original_masks=[A,B,G,H],proper_ids=ids,cycle_entries=[[i,j,v] for (i,j),v in sorted(R.items())],parameter_interval=['-1/1024','1/1024'],exact_operator_norm='2*abs(t)',all_real_tau_interval=['0','1/64'],proper_uniform_floor=str(floor),actual_uniform_spectral_gap=str(floor/220),sharp_distance_constant=2,corner_checks=rows,all_empty_entries_unchanged=True,not_a_feasible_set_distance_claim=True)


def make(cert,comparison,damage='none'):
    cert=copy.deepcopy(cert);comparison=copy.deepcopy(comparison)
    if damage=='float':cert['free_original_entry_numerators'][0]=float(cert['free_original_entry_numerators'][0])
    if damage=='boolean':cert['free_original_entry_numerators'][0]=True
    if damage=='key':cert['free_original_entry_orbit_keys'].pop()
    if damage=='coefficient':cert['free_original_entry_numerators'][0]+=1
    if damage=='triangle':cert['positive_sector_certificates']['TT_lower']['factor_lower_triangle_numerators'].pop()
    if damage=='residual-den':cert['positive_sector_certificates']['TT_lower']['whole_residual_denominator']+=1
    if damage=='scalar':cert['positive_sector_certificates']['WW_upper']['scalar_gram_numerator']+=1
    keys,old,values=inputs(cert,comparison);D,stars=literal();Co,Uo,Lo,Mo=build(D,old,OLD);bad,edges,dual_record=dual(D,Co,Mo,damage)
    endpoints={};rec=[]
    for tau in (F(0),CENTER,EXTENDED):
        table,pars=recipe(old,tau)
        if tau==CENTER:need([table[k] for k in keys]==values,'every fresh coefficient equals explicit primal at certificate center')
        C,U,L,M=build(D,table,DEN)
        if damage=='star' and tau==CENTER:C[0][0]+=1
        if damage=='upper' and tau==CENTER:U[0][0]+=1
        if damage=='empty' and tau==CENTER:M[0][0]+=1
        need(all(sum(row[j] for j,A in enumerate(D[1:]) if A&1)==0 for row in C),'all original lower star equations')
        need(all(U[i][j]==278*DEN*(i==j)-DEN-C[i][j] for i in range(277) for j in range(277)),'whole opposite proper endpoint')
        need(all(sum(row)==220*DEN for row in M),'every original completed row')
        e=endpoint(D,C,U,L,M,Co,bad,edges,tau);e['recipe_constants']=pars;rec.append(e);endpoints[tau]=(C,U,L,M)
    K,KL,slope=derivative(D)
    if damage=='slope':K[0][0]+=1
    C0,U0,L0,M0=endpoints[F(0)];Cc,Uc,Lc,Mc=endpoints[CENTER];C2,U2,L2,M2=endpoints[EXTENDED]
    need(all((Cc[i][j]-C0[i][j])*128*KDEN==(C2[i][j]-Cc[i][j])*128*KDEN==K[i][j]*DEN for i in range(277) for j in range(277)),'every proper endpoint affine difference')
    need(all((Lc[i][j]-L0[i][j])*128*KDEN==(L2[i][j]-Lc[i][j])*128*KDEN==KL[i][j]*DEN for i in range(278) for j in range(278)),'every actual endpoint affine difference')
    psd=inspect(D,Cc,Uc,cert,DEN,damage);B,geometry=repairs(D)
    floor=F(1,16)-F(53,8)*F(1,128);need(floor==F(11,1024)>F(1,128),'whole enlarged real interval physical floor')
    if damage=='range':need(F(1,16)-F(53,8)*F(1,64)>=F(1,128),'deliberately unpaid interval spectral budget')
    cycle=sharp_cycle(D,endpoints,Co,bad,edges,damage)
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',carrier=dict(N=278,proper=277,ground_points=21,s=58,stars=stars),explicit_input_scope='Open author current coefficient/factor/compiled margin and old comparison DATA. Own published frame/literal code openly reused with pins; no author programs/EXPECTED/validators/private input or old PSD premise.',endpoint_records=rec,point_certificates=psd,full_real_affine_face=geometry,universal_dual_and_stability=dual_record,derivative=slope,proved_real_parameter_interval=['0','1/64'],target_parameter_interval_confirmed=['0','1/128'],center_point_proper_floor='1/16',enlarged_uniform_proper_floor='11/1024',enlarged_uniform_actual_gap='1/20480',sharper_exact_gap=str(floor/220),rank_lower=277,rank_upper=277,simple_extreme_eigenvalues=['-29/110','1'],sharp_NN_sign_stability=cycle,strict_positive_infimum='476335/32768',strict_positive_infimum_unattained=True,ordinary_analytic_bridges='UNFORMALIZED all-real star forcing/dual/cone metric/completeness/tensor metric/section/norm/congruence/ranks/convex entry/affine interval/sharp rank-two cycle; no global H/I, maximal interval, optimizer geometry10308 or feasible-optimal-set distance verdict.')
