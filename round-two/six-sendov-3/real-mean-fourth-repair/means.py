"""Entire balanced real-mean repair calculation; ordinary author evidence.
The same-author10212 finite series engine is openly reused in series.py.
Finite maps do not formalize uniform implicit collars or disk containment.
"""
from pathlib import Path
from hashlib import sha256
import json
import series as s
from arithmetic import F,need,canonical

BASELINE_BYTES=150740
BASELINE_SHA256='d00486db2576f1be9de39483d374b68c4223a8193bf0f7374bd37b3c9d14cccd'
Mstar=s.const(s.fcf(F(8148040331,629856),F(78878749667,1259712),F(-51194418673,629856)))
betastar=s.const(s.fcf(F(27821775167,17915904),F(80418819893,8957952),F(-12650091319,1119744)))
Gstar=s.const(s.fcf(F(183619658945,2519424),F(444829186913,1259712),F(-288729410449,629856)))
mu={1:s.ar.N1}
L=s.const(s.fcf(F(-101920,243),F(-1218245,486),F(251888,81)))
MUstar=s.ns(L,F(-3,8))
IMPROVEMENT=s.ns(s.np(L,2),F(3,16))
Gmean=s.na(Gstar,s.ns(IMPROVEMENT,-1))
def components(m3,beta2,m4,beta3,shift=mu,eta_power=1,inward=0,damage=None):
    e=eta_power
    direction=F(1,3) if damage=='unbalanced_mean' else F(-1,3)
    A={(e,0):s.gf(s.uz),(2*e,0):s.gf(s.na(s.w2,s.ns(shift,direction))),
       (3*e,0):s.gf(m3),(4*e,0):s.gf(m4)}
    B={(e,0):s.gf(s.up),(2*e,0):s.gf(s.na(s.w2,shift)),
       (3*e,0):s.gf(m3),(4*e,0):s.gf(m4)}
    K={(0,0):(s.N0,s.N1),(e,0):(s.N0,s.gamma),
       (2*e,0):(s.N0,beta2),(3*e,0):(s.N0,beta3)}
    if inward:
        need(e==2,'half-order inward term is epsilon9')
        value=-inward if damage=='outward_ninth' else inward
        A=s.pa(A,{(9,0):s.gf(s.ns(s.N1,value))})
        B=s.pa(B,{(9,0):s.gf(s.ns(s.N1,value))})
    return A,B,K
def normal_columns():
    cols=[]
    for j in range(9):
        omega=s.np(s.WW,j)
        Aj=s.na(s.N1,s.ns(s.na(omega,s.nc(omega)),F(-1,2)))
        v=s.np(omega,2)
        Bj=s.na(s.N1,s.ns(s.na(v,s.nc(v)),F(-1,2)))
        cols.append((s.ns(Aj,-1),s.ns(s.nm(s.H,Bj),F(1,7))))
    return cols
def make_signs():
    polynomial=lambda c:8*c**3-6*c-1
    lo,hi=F(15,16),F(47,50)
    need(polynomial(lo)<0<polynomial(hi),'physical positive cubic bracket')
    need(24*lo**2-6>0,'strict positive derivative on physical bracket')
    signs=[]
    for _ in range(24):
        mid=(lo+hi)/2
        if polynomial(mid)<0:lo=mid
        else:hi=mid
    def bound(field):
        a=[F(q) for q in s.field_real_form(s.fc,field)]
        low=high=F(0)
        for degree,q in enumerate(a):
            low+=q*(lo**degree if q>=0 else hi**degree)
            high+=q*(hi**degree if q>=0 else lo**degree)
        return low,high
    def positive(name,field):
        low,high=bound(field)
        need(low>0,'positive physical field: '+name)
        signs.append({'name':name,'whole_cubic':s.field_real_form(s.fc,field),
            'rational_lower':str(low),'rational_upper':str(high),'strict':True})
    positive('minus_L',s.ar.ns(L[0],-1))
    positive('mu_star_minus8',s.ar.na(MUstar[0],s.ar.ns(s.ar.N1,-8)))
    positive('16_minus_mu_star',s.ar.na(s.ar.ns(s.ar.N1,16),s.ar.ns(MUstar[0],-1)))
    positive('minus_old_Gstar',s.ar.ns(Gstar[0],-1))
    positive('strict_fourth_improvement',IMPROVEMENT[0])
    positive('minus_Gmean',s.ar.ns(Gmean[0],-1))
    return signs,positive,[str(lo),str(hi)]
def build(baseline,damage=None):
    raw=Path(baseline).read_bytes()
    need(len(raw)==BASELINE_BYTES and sha256(raw).hexdigest()==BASELINE_SHA256,'whole useful10212 zero baseline bytes')
    old=json.loads(raw)
    ids=[];columns=normal_columns()
    def repair(q3,q4):
        a,b=columns[3];c,d=columns[4]
        det=s.na(s.nm(a,d),s.ns(s.nm(c,b),-1))
        return (s.nm(s.na(s.ns(s.nm(q3,d),-1),s.nm(q4,b)),s.ni(det)),
                s.nm(s.na(s.ns(s.nm(a,q4),-1),s.nm(c,q3)),s.ni(det)))
    def root_rows(parts,tag):
        p=s.actual_polynomial(*parts,4,1)
        np,powers=s.newton_polynomial(*parts,4,1)
        s.eq(ids,tag+' ENTIRE literal vs ALL8 Newton primitive',
            [g for row in p for g in row],[g for row in np for g in row])
        roots=s.roots_and_normals(p,4,ids)
        first=s.direct_first_power(*parts,4,1)
        return p,roots,first,powers
    defaults=(s.C['m3'],s.C['Gamma2'],Mstar,betastar)
    bp,br,bf,bpowers=root_rows(components(*defaults,shift=s.N0),'ZERO')
    need(s.encoded_vector(bf)==old['zero_repaired_first_power_through_eta4'],'WHOLE10212 zero FIRST baseline')
    need([s.encoded_vector(row) for row in bp]==old['zero_repaired_all_primitive_columns_through_eta4'],'WHOLE10212 zero primitive baseline')
    need(s.output_roots(br)==old['zero_repaired_all_nine_roots'],'WHOLE10212 zero all-nine root/normal baseline')
    need(s.decode(old['constants']['M4'])==Mstar and s.decode(old['constants']['beta3'])==betastar,'WHOLE10212 joint repair constants')
    p0,r0,f0,powers0=root_rows(components(*defaults,damage=damage),'UNREPAIRED')
    s.eq(ids,'ENTIRE balanced eta² critical mean',[powers0[1].get((2,0),s.G0)],[s.gf(s.C['Wstar'])])
    # Verify the actual common-center and scale columns at BOTH orders,
    # all nine labels, before solving either two-row repair system.
    for order in (3,4):
        for index in (0,1):
            args=list(defaults)
            slot=(0 if index==0 else 1) if order==3 else (2 if index==0 else 3)
            args[slot]=s.na(args[slot],s.N1)
            p=s.actual_polynomial(*components(*args,damage=damage),4,1)
            delta=[s.ga(a,s.gs(b,-1)) for a,b in zip(p[order],p0[order])]
            expected=[s.G0]*10
            if index==0:
                expected[8]=s.gf(s.ns(s.N1,-9));expected[0]=s.gf(s.ns(s.N1,9))
            else:
                expected[7]=s.gf(s.ns(s.H,F(9,7)));expected[0]=s.gf(s.ns(s.H,F(-9,7)))
            s.eq(ids,'WHOLE actual repair primitive column/'+str(order)+'/'+str(index),delta,expected)
            for j in range(9):
                omega=s.np(s.WW,j)
                value=s.G0
                for exponent,g in enumerate(delta):
                    value=s.ga(value,s.gm(g,s.gf(s.np(omega,exponent))))
                normal=s.gs(s.real(value),F(-1,9))
                s.eq(ids,'ALL9 actual normal repair column/'+str(order)+'/'+str(index)+'/'+str(j),
                     [normal],[s.gf(columns[j][index])])
    dm3,dbeta2=repair(r0[3]['normals'][3][0],r0[4]['normals'][3][0])
    need(set(dm3)<={1} and set(dbeta2)<={1},'third mean repairs are homogeneous affine')
    predicted_m3={1:s.fcf(0,F(56,9),F(-56,9))}
    predicted_beta2={1:s.fcf(F(1,2),2)}
    s.eq(ids,'ENTIRE third center-mean compensation',[s.gf(dm3)],[s.gf(predicted_m3)])
    s.eq(ids,'ENTIRE third pair-mean compensation',[s.gf(dbeta2)],[s.gf(predicted_beta2)])
    lower_m3=s.na(s.C['m3'],dm3);lower_beta2=s.na(s.C['Gamma2'],dbeta2)
    if damage=='freeze_third':lower_m3=s.C['m3']
    if damage=='omit_pair_compensation':lower_beta2=s.C['Gamma2']
    p1,r1,f1,powers1=root_rows(components(lower_m3,lower_beta2,Mstar,betastar,damage=damage),'LOWER')
    for j in (3,4,5,6):
        s.eq(ids,'ALL4 actual third normals repaired/'+str(j),[r1[j]['normals'][3]],[s.G0])
    for e,coefficient in enumerate((s.ns(s.N1,8),s.C['C'],s.C['Bstar'],s.C['Tstar'])):
        s.eq(ids,'WHOLE first-power coefficient through third/'+str(e),[f1[e]],[s.gf(coefficient)])
    dm4,dbeta3=repair(r1[3]['normals'][4][0],r1[4]['normals'][4][0])
    need(set(dm4)<={1,2} and set(dbeta3)<={1,2},'fourth mean repairs are at most quadratic with zero baseline')
    predicted_m4={1:s.fcf(F(-51583,972),F(-175385,486),448)}
    predicted_beta3={1:s.fcf(F(1771,324),F(-94039,1296),F(12347,162)),
                     2:s.fcf(F(2,7),F(2,7))}
    s.eq(ids,'ENTIRE fourth center-mean compensation',[s.gf(dm4)],[s.gf(predicted_m4)])
    s.eq(ids,'ENTIRE fourth pair-mean compensation',[s.gf(dbeta3)],[s.gf(predicted_beta3)])
    if damage=='drop_quadratic_pair':dbeta3={k:v for k,v in dbeta3.items() if k!=2}
    full_m4=s.na(Mstar,dm4);full_beta3=s.na(betastar,dbeta3)
    p2,r2,f2,powers2=root_rows(components(lower_m3,lower_beta2,full_m4,full_beta3,damage=damage),'FULL')
    for j in (3,4,5,6):
        for e in range(1,5):
            s.eq(ids,'ALL4 active actual normals through4/'+str(j)+'/'+str(e),[r2[j]['normals'][e]],[s.G0])
    for e in range(4):s.eq(ids,'repaired whole lower FIRST invariance/'+str(e),[f2[e]],[bf[e]])
    need(f2[4][1]==s.N0 and set(f2[4][0])<={0,1,2},'mean fourth cost is real quadratic')
    predicted_cost=s.na(Gstar,s.nm(L,mu),s.ns(s.np(mu,2),F(4,3)))
    if damage=='wrong_cost_linear':predicted_cost=s.na(Gstar,s.ns(s.nm(L,mu),-1),s.ns(s.np(mu,2),F(4,3)))
    s.eq(ids,'ENTIRE repaired quadratic fourth cost',[f2[4]],[s.gf(predicted_cost)])
    completed_square=s.na(Gmean,s.ns(s.np(s.na(mu,s.ns(MUstar,-1)),2),F(4,3)))
    s.eq(ids,'ENTIRE sharp mean square completion',[f2[4]],[s.gf(completed_square)])
    s.eq(ids,'ENTIRE closed new fourth constant',[s.gf(Gmean)],
        [s.gf(s.const(s.fcf(F(340367352475,839808),F(808137564635,419904),F(-1052841914857,419904))))])
    s.eq(ids,'ENTIRE closed minimizing mean',[s.gf(MUstar)],
        [s.gf(s.const(s.fcf(F(12740,81),F(1218245,1296),F(-31486,27))))])
    # Complete positive-dual fourth repair identity, including BOTH rows.
    w4=s.ni(s.na(s.c,s.ns(s.np(s.c,2),2),s.ns(s.N1,-1)))
    w3=s.ns(s.na(s.ns(s.N1,7),s.ns(s.nm(s.na(s.ns(s.N1,2),s.ns(s.np(s.c,2),-2)),w4),-1)),F(2,3))
    for target,index in ((s.ns(s.N1,-8),0),(s.H,1)):
        payment=s.na(s.nm(w3,columns[3][index]),s.nm(w4,columns[4][index]))
        s.eq(ids,'ENTIRE fourth positive-dual column/'+str(index),[s.gf(payment)],[s.gf(target)])
    if damage=='wrong_dual':w3=s.ns(w3,-1)
    raw_fourth_cost=s.na(f1[4][0],s.ns(dm4,8),s.ns(s.nm(s.H,dbeta3),-1))
    dual_fourth_cost=s.na(f1[4][0],s.nm(w3,r1[3]['normals'][4][0]),s.nm(w4,r1[4]['normals'][4][0]))
    s.eq(ids,'ENTIRE repaired scalar/positive-dual elimination',[s.gf(raw_fourth_cost)],[s.gf(dual_fourth_cost)])
    s.eq(ids,'ENTIRE direct repaired scalar',[f2[4]],[s.gf(raw_fourth_cost)])
    # Actual epsilon9 inward response; equations and normals at EVERY root.
    parts_eps=components(lower_m3,lower_beta2,full_m4,full_beta3,eta_power=2,inward=1,damage=damage)
    peps=s.actual_polynomial(*parts_eps,9,2)
    pneps,powerseps=s.newton_polynomial(*parts_eps,9,2)
    s.eq(ids,'ENTIRE epsilon0to9 literal/ALL8 Newton primitive',
        [g for row in peps for g in row],[g for row in pneps for g in row])
    expected_odd=[s.G0]*10;expected_odd[8]=s.gf(s.ns(s.N1,-9));expected_odd[0]=s.gf(s.ns(s.N1,9))
    s.eq(ids,'ENTIRE epsilon9 inward primitive',peps[9],expected_odd)
    epsrows=[]
    for j,row in enumerate(r2):
        omega=s.np(s.WW,j)
        root=[s.G0]*10
        for e in range(5):root[2*e]=row['root'][e]
        root[9]=s.gf(s.na(s.N1,s.ns(omega,-1)))
        s.eq(ids,'ALL9 entire original equation epsilon0to9/'+str(j),s.equation(peps,root,9),[s.G0]*10)
        normals=s.sm(root,[s.gc(x) for x in root],9)
        normals[0]=s.ga(normals[0],s.gs(s.G1,-1))
        normals=[s.gs(x,F(1,2)) for x in normals]
        predicted=[s.G0]*10
        for e in range(5):predicted[2*e]=row['normals'][e]
        predicted[9]=s.gf(columns[j][0])
        s.eq(ids,'ALL9 entire half-normal epsilon0to9/'+str(j),normals,predicted)
        epsrows.append({'label':j,'root':root,'normals':normals})
    feps=s.direct_first_power(*parts_eps,9,2)
    expected_first=[s.G0]*10
    for e in range(5):expected_first[2*e]=f2[e]
    expected_first[9]=s.gf(s.ns(s.N1,8))
    s.eq(ids,'ENTIRE inward FIRST epsilon0to9',feps,expected_first)
    signs,positive,bracket=make_signs()
    positive('dual_w3',w3[0]);positive('dual_w4',w4[0])
    for j in (0,1,2,7,8):
        positive('inactive_minus_first_normal/'+str(j),s.ar.ns(s.field_value(r2[j]['normals'][1]),-1))
    for j in (3,4,5,6):
        positive('active_minus_ninth_normal/'+str(j),s.ar.ns(columns[j][0][0],-1))
    if damage=='wrong_positivity':
        need(not signs[0]['strict'],'intentional strict physical-sign damage')
    return {
        'schema':1,'agent':'six-sendov-3','role':'researcher','independent_review':False,
        'ordinary_analytic_bridges_unformalized':True,
        'scope':'balanced eta² real-mean direction with coupled third/fourth repairs in the displayed real6+2 class; no universal fourth lower optimum',
        'critical_multiplicities':[6,1,1],'original_count':9,
        'parent_zero_baseline':{'source_commit':'ac5e5ea1bfd10e45fb5acccb775a5061201c842d',
            'whole_bytes':BASELINE_BYTES,'whole_sha256':BASELINE_SHA256,
            'compared':'ALL50 primitive columns/ALL45 original roots and half-normals/ALL5 FIRST coefficients; other parent records not replayed'},
        'constants':{name:s.rpoly(v) for name,v in {'L':L,'MUstar':MUstar,'Gstar':Gstar,'Gmean':Gmean,
            'strict_improvement':IMPROVEMENT,'delta_m3':dm3,'delta_beta2':dbeta2,
            'delta_m4':dm4,'delta_beta3':dbeta3,'dual_w3':w3,'dual_w4':w4}.items()},
        'physical_cubic_bracket':bracket,
        'whole_all_eight_moments_epsilon0to9':[s.encoded_vector([p.get((e,0),s.G0) for e in range(10)]) for p in powerseps[1:]],
        'whole_all_primitive_columns_epsilon0to9':[s.encoded_vector(row) for row in peps],
        'whole_all_nine_original_roots_epsilon0to9':s.output_roots(epsrows),
        'whole_first_power_epsilon0to9':s.encoded_vector(feps),
        'whole_identities':ids,'positive_rational_signs':signs}
