"""Whole exact maps; ordinary analytic bridges are in PROOF.md."""
import profiles as p
from profiles import s,F


def lower_centers():
    """Actual lower-order maps with both independent center means present."""
    ids=[]
    base=s.actual_polynomial(p.A0,p.B0,p.K0,6,2)
    baseline_F=s.direct_first_power(p.A0,p.B0,p.K0,6,2)
    for balanced,name in ((False,'independent'),(True,'sumzero')):
        small,B,D2=p.family(True,lower_centers=True,balanced_means=balanced)
        poly=p.literal_primitive(small,B,D2,6)
        newton=p.newton_primitive(p.actual_moments(small,B,D2,6),6)
        for e in range(7):
            p.eq(ids,name+' complete lower-center literal/Newton epsilon'+str(e),poly[e],newton[e])
        S=s.N0 if balanced else s.na(s.ns(p.mean_A,6),s.ns(p.mean_B,2))
        distances,_,_=p.squared_distances(small,B,D2,6)
        actual=p.vector(s.pa(*(p.reciprocal_distance(v,6) for v in distances)),6)
        for e in range(5):
            target=s.ga(baseline_F[e],s.gf(S)) if e==4 else baseline_F[e]
            p.eq(ids,name+' complete actual lower-center FIRST epsilon'+str(e),[actual[e]],[target])
        for j in range(9):
            omega=s.np(s.WW,j)
            root=[s.gf(omega)]+[s.G0]*6
            for e in range(1,7):
                root[e]=s.gs(s.gm(s.equation(poly,root,e)[e],s.gf(omega)),F(-1,9))
            p.eq(ids,name+' complete actual lower-center original equation label'+str(j),
                 s.equation(poly,root,6),[s.G0]*7)
            norm=s.sm(root,[s.gc(g) for g in root],6)
            norm[0]=s.ga(norm[0],s.gs(s.G1,-1));norm=[s.gs(g,F(1,2)) for g in norm]
            old=p.prior['all_nine_shrinking_roots_epsilon0to9'][j]
            p.ar.need(old['label']==j,'CENSUS lower-center baseline original label')
            oldnorm=[p.retag(s.decode_g(g)) for g in old['all_half_normals']]
            cosine=s.real(s.gf(omega))[0]
            target=s.ns(s.nm(s.na(s.N1,s.ns(cosine,-1)),S),F(-1,8))
            p.eq(ids,name+' entire individual second lower-center normal CHANGE label'+str(j),
                 [s.ga(norm[4],s.gs(oldnorm[4],-1))],[s.gf(target)])
            if balanced:
                cos2=s.real(s.gf(s.np(omega,2)))[0]
                cos3=s.real(s.gf(s.np(omega,3)))[0]
                third=s.nm(s.nm(s.H,p.mean_A),s.na(
                    s.ns(s.nm(s.rho,s.na(s.N1,s.ns(cos2,-1))),F(-3,7)),
                    s.ns(s.na(s.N1,s.ns(cos3,-1)),p.LOWER_THIRD_PAIR_FACTOR)))
                p.eq(ids,'sumzero entire individual third lower-center normal CHANGE label'+str(j),
                     [s.ga(norm[6],s.gs(oldnorm[6],-1))],[s.gf(third)])
    return p.complete_record('lower_centers',{'status':'PASS entire lower-center closure in actual thirteen-parameter class',
        'identity_count':len(ids),'whole_identities':ids})


def algebra():
    """Full field identities and exact rational physical signs for new constants."""
    ids=[]
    c,H=s.c,s.H
    w4=s.ni(s.na(c,s.ns(s.np(c,2),2),s.ns(s.N1,-1)))
    w3=s.ns(s.na(s.ns(s.N1,7),s.ns(s.nm(s.na(s.ns(s.N1,2),s.ns(s.np(c,2),-2)),w4),-1)),F(2,3))
    def eq(name,a,b):p.eq(ids,name,[s.gf(a)],[s.gf(b)])
    eq('whole even determinant',p.determinant,s.ns(s.nm(H,s.na(c,s.ns(s.np(c,2),2),s.ns(s.N1,-1))),F(3,14)))
    eq('whole even repair row3',s.na(p.q3,s.ns(s.nm(p.A3,p.mI),-1),s.nm(p.b3,p.betaI)),s.N0)
    eq('whole even repair row4',s.na(p.q4,s.ns(s.nm(p.A4,p.mI),-1),s.nm(p.b4,p.betaI)),s.N0)
    eq('whole odd repair row3',s.na(p.o3,p.nu,s.ns(s.nm(H,p.sigma),F(-1,7))),s.N0)
    eq('whole odd repair row4',s.na(p.o4,p.nu,s.ns(s.nm(s.nm(c,H),p.sigma),F(-2,7))),s.N0)
    raw=s.ns(s.nm(H,s.na(s.ns(s.rho,2),s.N1)),F(-3,8))
    eq('whole actual chi payment',s.na(raw,s.ns(p.mI,8),s.ns(s.nm(H,p.betaI),-1)),p.chi)
    eq('whole first positive dual row',s.na(s.nm(p.A3,w3),s.nm(p.A4,w4)),s.ns(s.N1,8))
    eq('whole second positive dual row',s.na(s.ns(s.nm(p.b3,w3),F(7)),s.ns(s.nm(p.b4,w4),F(7))),s.ns(H,7))
    eq('whole physical cosine cubic',s.na(s.ns(s.np(c,3),8),s.ns(c,-6),s.ns(s.N1,-1)),s.N0)
    bounds=[]
    lo,hi=(F(v) for v in p.prior['physical_cosine_interval'])
    def cubic(x):return 8*x**3-6*x-1
    p.ar.need(F(15,16)<lo<hi<1 and cubic(lo)<0<cubic(hi) and 24*lo**2-6>0,'SIGN unique physical cosine isolating interval')
    def positive(name,z):
        p.ar.need(set(z)<={0},'TYPE whole constant real field sign')
        coefficients=[F(v) for v in s.field_real_form(s.physical_c,z.get(0,p.ar.N0))]
        lower=sum(v*(lo**j if v>=0 else hi**j) for j,v in enumerate(coefficients))
        p.ar.need(lower>0,'SIGN '+name)
        bounds.append({'name':name,'entire_real_cubic_coefficients':[str(v) for v in coefficients],
                       'rational_lower_bound':str(lower)})
    lower3=s.ns(s.rho,F(-9,14))
    lower4=s.na(s.ns(s.nm(s.na(s.ns(s.N1,5),s.ns(c,-1)),s.na(s.N1,s.ns(s.np(c,2),-1))),F(2,7)),s.ns(s.N1,F(-3,4)))
    for name,z in (('H',H),('kappa',s.kappa),('chi',p.chi),('even determinant',p.determinant),
                   ('odd absolute determinant',s.ns(s.nm(H,s.na(s.ns(c,2),s.ns(s.N1,-1))),F(1,7))),
                   ('dual w3',w3),('dual w4',w4),('lower mean label3',lower3),('negative lower mean label4',s.ns(lower4,-1)),
                   ('negative Gstar',s.ns(p.con['G4'],-1))):positive(name,z)
    return p.complete_record('algebra',{'status':'PASS exact new-profile field identities and rational signs',
        'identity_count':len(ids),'whole_identities':ids,'physical_cosine_interval':[str(lo),str(hi)],'sign_bounds':bounds})

def literal():
    ids=[]
    p.eq(ids,'six imaginary coordinates have exact zero sum',[s.gf(s.na(*p.I))],[s.G0])
    p.eq(ids,'six real coordinates have exact zero sum',[s.gf(s.na(*p.R))],[s.G0])
    base=s.actual_polynomial(p.A0,p.B0,p.K0,9,2)
    records={}
    for paid,name in ((False,'raw'),(True,'paid')):
        small,B,D2=p.family(paid)
        literal=p.literal_primitive(small,B,D2)
        moments=p.actual_moments(small,B,D2)
        newton=p.newton_primitive(moments)
        predicted=p.predicted_delta(paid)
        for e in range(10):
            p.eq(ids,name+' actual six-factor versus ALL8 Newton primitive epsilon'+str(e),literal[e],newton[e])
            delta=[s.ga(a,s.gs(b,-1)) for a,b in zip(literal[e],base[e])]
            p.eq(ids,name+' literal primitive versus entire invariant pencil epsilon'+str(e),delta,
                 predicted[e])
        records[name]={'all8_actual_moments':[p.encode_poly(z) for z in moments[1:]],
                       'all100_actual_primitive_columns':[[p.encode_g(g) for g in row] for row in literal]}
    record={'status':'PASS exact actual eleven-parameter literal/Newton reconstruction',
            'whole_identities':ids,'identity_count':len(ids),'records':records,
    }
    return p.complete_record('literal',record)

def distance():
    ids=[]
    baseline=s.direct_first_power(p.A0,p.B0,p.K0,9,2)
    records={}
    for paid,name in ((False,'raw'),(True,'paid')):
        small,B,D2=p.family(paid)
        distances,K,L=p.squared_distances(small,B,D2)
        squared=s.pp(K,2,8)
        for e in range(9):
            p.eq(ids,name+' actual analytic pair-square-root epsilon'+str(e),
                 [squared.get((e,0),s.G0)],[L.get((e,0),s.G0)])
        reciprocals=[p.reciprocal_distance(v) for v in distances]
        for j,(v,r) in enumerate(zip(distances,reciprocals)):
            product=s.pm(s.pp(r,2,9),v,9)
            p.eq(ids,name+' individual reciprocal-square distance equation slot'+str(j),
                 p.vector(product),[s.G1]+[s.G0]*9)
            p.eq(ids,name+' entire real squared distance slot'+str(j),p.vector(v),
                 [s.gc(g) for g in p.vector(v)])
        total=s.pa(*reciprocals)
        actual=p.vector(total)
        VIcost=p.chi if paid else s.ns(s.nm(s.H,s.na(s.ns(s.rho,2),s.N1)),F(-3,8))
        extra=s.na(s.ns(p.VR,F(1,2)),s.nm(VIcost,p.VI))
        for e in range(10):
            target=s.ga(baseline[e],s.gf(extra)) if e==8 else baseline[e]
            p.eq(ids,name+' ENTIRE actual FIRST distance sum epsilon'+str(e),[actual[e]],[target])
            for component in actual[e]:
                p.ar.need(all(p.digits(i)[11]==0 for i in component),'all odd radical terms cancel in full FIRST sum')
        records[name]={'all8_actual_squared_distances':[p.encode_poly(v) for v in distances],
                      'all8_actual_reciprocal_distances':[p.encode_poly(v) for v in reciprocals],
                      'analytic_normalized_pair_square_root':p.encode_poly(K),
                      'all_actual_FIRST_coefficients':[p.encode_g(g) for g in actual]}
    record={'status':'PASS all eight actual distances and positive joint fourth cost',
            'whole_identities':ids,'identity_count':len(ids),'records':records,
    }
    return p.complete_record('distance',record)

def roots():
    ids=[]
    small,B,D2=p.family(True)
    poly=p.literal_primitive(small,B,D2)
    base=s.actual_polynomial(p.A0,p.B0,p.K0,9,2)
    changes=[[s.ga(a,s.gs(b,-1)) for a,b in zip(row,old)] for row,old in zip(poly,base)]
    records=[]
    p.ar.need([r['label'] for r in p.prior['all_nine_shrinking_roots_epsilon0to9']]==list(range(9)),'CENSUS all9 individual originals')
    for old in p.prior['all_nine_shrinking_roots_epsilon0to9']:
        j=old['label'];omega=s.np(s.WW,j)
        root=[p.retag(s.decode_g(g)) for g in old['all_root_coefficients']]
        oldroot=list(root)
        p.eq(ids,'individual baseline has no epsilon1 root term '+str(j),[root[1]],[s.G0])
        for e in (8,9):
            value=s.G0
            for degree,g in enumerate(changes[e]):
                value=s.ga(value,s.gm(g,s.gf(s.np(omega,degree))))
            root[e]=s.ga(root[e],s.gs(s.gm(value,s.gf(omega)),F(-1,9)))
        p.eq(ids,'ALL9 entire actual original equation epsilon0to9 label'+str(j),
             s.equation(poly,root,9),[s.G0]*10)
        p.eq(ids,'ALL9 full baseline original coefficients epsilon0to7 label'+str(j),root[:8],oldroot[:8])
        half=s.sm(root,[s.gc(g) for g in root],9)
        half[0]=s.ga(half[0],s.gs(s.G1,-1));half=[s.gs(g,F(1,2)) for g in half]
        oldnorm=[p.retag(s.decode_g(g)) for g in old['all_half_normals']]
        p.eq(ids,'ALL9 earlier individual normals unchanged label'+str(j),half[:8],oldnorm[:8])
        if j in (3,4,5,6):
            p.eq(ids,'ALL4 individual zero normals epsilon0to8 label'+str(j),half[:9],[s.G0]*9)
            p.eq(ids,'ALL4 strict inward epsilon9 unchanged label'+str(j),[half[9]],[oldnorm[9]])
        else:
            p.eq(ids,'ALL5 inactive first epsilon2 sign unchanged label'+str(j),[half[2]],[oldnorm[2]])
        records.append({'label':j,'all_root_coefficients':[p.encode_g(g) for g in root],
                        'all_half_normals':[p.encode_g(g) for g in half]})
    
    K,L=p.pair_square_root(D2,8)
    def imag(point):
        return {key:s.real((g[1],s.ns(g[0],-1))) for key,g in point.items()}
    yB=imag(B)
    yD={(e+1,k):s.gm(s.gf(p.radical_b),g) for (e,k),g in imag(K).items() if e+1<=9}
    cubes=s.pa(*(s.pp(imag(point),3,9) for point in small),
                s.ps(s.pp(yB,3,9),2),s.ps(s.pm(yB,s.pp(yD,2,9),9),6))
    yA0,yB0,yK0=imag(p.A0),imag(p.B0),imag(p.K0)
    old_variance={(e+2,k):s.gm(s.gf(s.ns(s.H,F(1,2))),g)
                  for (e,k),g in s.pp(yK0,2,9).items() if e+2<=9}
    oldcubes=s.pa(s.ps(s.pp(yA0,3,9),6),s.ps(s.pp(yB0,3,9),2),
                  s.ps(s.pm(yB0,old_variance,9),6))
    skew_difference=s.na(p.TI,s.ns(s.nm(s.nm(p.t,p.VI),s.ni(s.H)),F(-4,3)))
    for e in range(10):
        target=s.ga(oldcubes.get((e,0),s.G0),s.gf(skew_difference)) if e==9 else oldcubes.get((e,0),s.G0)
        p.eq(ids,'ENTIRE actual cubic-skew numerator epsilon'+str(e),[cubes.get((e,0),s.G0)],[target])
    record={'status':'PASS actual all-nine maps, strict inward jets and cubic skew',
            'whole_identities':ids,'identity_count':len(ids),'all9_originals':records,
            'actual_skew_cubic_numerator':[p.encode_g(g) for g in p.vector(cubes)],
            'skew_difference':'(TI-4*t*VI/(3*H))*epsilon5 + O_K(epsilon6*(VI+VR)) after division by epsilon4',
    }
    return p.complete_record('roots',record)

def repair_column(column):
    ids=[]
    small,B,D2=p.family(True)
    base=p.literal_primitive(small,B,D2)
    def first(points,center,sep):
        distances,_,_=p.squared_distances(points,center,sep)
        return p.vector(s.pa(*(p.reciprocal_distance(v) for v in distances)))
    baseF=first(small,B,D2)
    unitI=(s.N0,s.N1)
    for name,M,beta,cost in (
        ('real_center',s.G1,s.G0,s.ns(s.N1,8)),
        ('imaginary_center',unitI,s.G0,s.N0),
        ('real_pair',s.G0,s.G1,s.ns(s.H,-1)),
        ('imaginary_pair',s.G0,unitI,s.N0)):
        if name!=column: continue
        shift={(8,0):M}
        newpoints=[s.pa(point,shift) for point in small]
        newB=s.pa(B,shift)
        newD=s.pa(D2,{(8,0):s.gs(s.gm(s.gf(s.H),beta),-1)})
        poly=p.literal_primitive(newpoints,newB,newD)
        expected=[s.G0]*10
        expected[8]=s.gs(M,-9)
        expected[7]=s.gs(s.gm(s.gf(s.H),beta),F(9,7))
        expected[0]=s.gs(s.ga(expected[8],expected[7]),-1)
        for e in range(10):
            delta=[s.ga(x,s.gs(y,-1)) for x,y in zip(poly[e],base[e])]
            p.eq(ids,name+' entire complex-repair primitive epsilon'+str(e),delta,
                 expected if e==8 else [s.G0]*10)
        actual=first(newpoints,newB,newD)
        for e in range(10):
            p.eq(ids,name+' entire ACTUAL FIRST complex-repair epsilon'+str(e),
                 [s.ga(actual[e],s.gs(baseF[e],-1))],
                 [s.gf(cost) if e==8 else s.G0])
    record={'status':'PASS all four complex fourth-repair primitive and actual-distance columns',
            'whole_identities':ids,'identity_count':len(ids),
    }
    p.ar.need(len(ids)==20,'CENSUS exactly20 whole repair-column comparisons')
    return p.complete_record(column,record)
