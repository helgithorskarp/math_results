"""Independent all-order rational certificates, dense shifted polynomial backend."""
from fractions import Fraction as F
from exact import need,determinant3,psd_rank
from symbols import Rat,coefficients
from formulas import formulas

def record(z,weak=False):
    need(z.d[0][0]>0 and (z.n[0][0]>=0 if weak else z.n[0][0]>0),'constant sign')
    need(all(a>=0 for p in (z.n,z.d) for row in p for a in row),'coefficient sign')
    return {'weak':weak,'numerator':coefficients(z.n),'denominator':coefficients(z.d)}

def equations(f):
    v,l,m,b,r,u,s,N=(f[x] for x in ('v','lam','m','b','r','u','s','N'))
    a,c,d,t,w,h=(f[x] for x in ('a','c','d','t','w','h'))
    return {'triple_star':h+(v-4)*d+(r-3*l)*t-s,
      'triple_row':1+s+(v-3)*h-3*(l-1)*t+(v-3)*(v-4)*d/2+(b-3*r+3*l-1)*t-N,
      'pair_star':w+(v-3)*c+(r-2*l)*d-s,
      'pair_row':1+s+(v-2)*w-l*d+(v-2)*(v-3)*c/2+(b-2*r+l)*d-N,
      'point_star':a+(v-2)*w-l*d+(r-l)*h-3*u*t-s,
      'point_row':1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-(l-1)*r*t-N,
      'constant22':s+c-2*c*(v-1)+(c-1)*m-4*l/3,
      'constant23':l*d-2*d*r+(d-1)*b+2*l/3,
      'constant33':s+(3*l-1)*t-3*r*t+(t-1)*b-1}

def small(v,l,t):
    m,b,r,u=F(v*(v-1),2),F(l*v*(v-1),6),F(l*(v-1),2),F(l*(l-1),2)
    s=v+r;N=1+v+m+b;a=-F(l,3)
    c=F(3*v*v-3*(l+3)*v+11*l,3*(v-2)*(v-3));d=F(v*v-v-4,(v-4)*(v-3))
    w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*t
    alpha1=s-c*(v-3);alpha2=s+c;beta=t-d*d/alpha2
    red=t*F(v-6,v-2)+d*d*F((v-4)**2,v-2)/alpha1
    mu=s-t-(r-l)*red;A=(r-l)*d*d*F((v-4)**2,v-2)
    return {'v':F(v),'lam':F(l),'m':m,'b':b,'r':r,'u':u,'s':s,'N':N,
      'a':a,'c':c,'d':d,'t':t,'w':w,'h':h,'alpha1':alpha1,'alpha2':alpha2,
      'beta':beta,'red':red,'mu':mu,'A':A}

def cap_data(v):
    need(v in (7,9),'small missing-STS scope');l=v-3
    f=small(v,l,F(10,3) if v==7 else F(40,17))
    if v==7:
        G=[[F(61,3),F(91,15),F(71,4)],[F(91,15),F(296,15),F(323,24)],[F(71,4),F(323,24),F(77,3)]];B=F(49)
        radicals=[(F(9,4),5),(F(7,4),3),(F(17,12),2),(F(49,20),6)]
        crosses=[abs(f['d']-f['w'])*F(9,4)+f['d']*F(7,4),
                 F(17,12)+F(20,3)*F(49,20),F(19,2)*F(17,12)]
    else:
        G=[[F(35),F(6),F(19)],[F(6),F(704,21),F(20)],[F(19),F(20),F(721,17)]];B=F(82)
        radicals=[(F(8,3),7),(F(17,12),2),(F(7,4),3)]
        crosses=[F(41,105)*F(8,3)+F(34,15)*2,
                 F(25,51)*3*F(17,12)+F(80,17)*2*F(7,4),F(17,3)*2*F(7,4)]
    need(all(a*a>n for a,n in radicals),'radical bound')
    need(all(x<=G[i][j] for x,(i,j) in zip(crosses,((0,1),(0,2),(1,2)))),'cross upper bound')
    need([G[i][i] for i in range(3)]==[f['s']+F(l,3),f['s']+f['c'],f['s']+f['t']*(v-5)],'diagonal bounds')
    M=[[B*(i==j)-G[i][j] for j in range(3)] for i in range(3)]
    minors=[M[0][0],M[0][0]*M[1][1]-M[0][1]**2,determinant3(M)]
    need(all(z>0 for z in minors) and psd_rank(M)==3,'strict cap comparison')
    delta=f['N']-B;loss=f['m']*(v-2)*(v-3)/(4*v*v)
    need(delta>0 and loss<delta/2 and B>F(l*(v+7),6)+1,'constant or trade gap')
    return {'v':v,'lambda':l,'N':int(f['N']),'s':int(f['s']),'centered_cap':str(B),
      'delta':str(delta),'repaired_buffer':str(delta/2),'repair_loss_at_max_eta':str(loss),
      'comparison':[[str(x) for x in row] for row in G],
      'Sylvester_minors':list(map(str,minors)),'radical_bounds':[[str(x),n] for x,n in radicals]}

def run():
    v=Rat(((7,),(1,)));l=Rat(((2,1),));f=formulas(v,l)
    identities=equations(f)
    identities['alpha1_formula']=f['s']-f['c']*(v-3)-f['alpha1']
    identities['Schur_formula']=f['mu']-1/l-f['P']/(l*(v-3)*(v-2)*f['D']*f['E'])
    identities['Schur_red']=f['gamma']-4*f['beta']/(v-2)-f['red']
    identities['density']=f['N']-2*f['s']-(v-1)*((v-2)/2+l*(v-6)/6)
    two=formulas(v,2)
    mu2=v*(3*v**3-13*v*v+32)/((v-3)*(v-2)*(3*v*v-16))
    margin2=2*(v-4)*(v*v+3*v-12)/((v-3)*(v-2)*(3*v*v-16))
    identities['lambda2_mu']=two['mu']-mu2
    identities['lambda2_strict_margin']=mu2-1-margin2
    for name,z in identities.items():need(z.equals(0),'identity:'+name)
    positive={'D':f['D'],'E':f['E'],'alpha1_gt_lv_over2':f['alpha1']-l*v/2,
       'A_lt_2lv2':2*l*v*v-f['A'],'t_gt1':f['t']-1,'d_positive':f['d'],
       'c_simplicity_lower':(8*v-22)/(3*(v-2)*(v-3)),
       'beta_lower':1-Rat(F(361,36))/(2*v-1),'lambda2_mu_gt1':margin2,
       'density':f['N']-2*f['s']}
    records={name:record(z) for name,z in positive.items()}
    records['d_le_19over6']=record(Rat(F(19,6))-f['d'],True)
    records['s_ge_2vminus1']=record(f['s']-(2*v-1),True)
    fp=formulas(v,Rat(((3,1),)))
    records['lambda3plus_Schur_P']=record(fp['P'])
    need(len(coefficients(fp['P'].n))==33 and fp['P'].n[0][0]==89136,'Schur coefficient domain')
    finite=[]
    for vv,ll,tt in ((5,3,F(6)),(6,2,F(2)),(6,4,F(5))):
      ff=small(vv,ll,tt)
      need(all(z==0 for z in equations(ff).values()),'finite equations')
      need(ff['alpha1']>F(ll*vv,2) and ff['alpha2']>0 and ff['beta']>0 and ff['red']>0 and ff['mu']>F(1,ll) and ff['A']<2*ll*vv*vv and ff['N']>2*ff['s'],'finite signs')
      free=(vv,ll) in ((5,3),(6,2))
      if free:need(all(z==0 for tau in (F(0),F(1)) for z in equations(small(vv,ll,tau)).values()),'affine free t')
      finite.append({'v':vv,'lambda':ll,'t':str(tt),'singular_affine_t':free,
        'alpha1':str(ff['alpha1']),'alpha2':str(ff['alpha2']),'beta':str(ff['beta']),
        'red':str(ff['red']),'mu':str(ff['mu']),'A':str(ff['A'])})
    fd=formulas(v,v-3);fn=formulas(v+1,v-2)
    records['missing_STS_density_decreases']=record(fd['s']/fd['N']-fn['s']/fn['N'])
    return {'identity_names':list(identities),'identity_count':len(identities),
       'coefficient_certificates':records,'positive_records':len(records)-2,'weak_records':2,
       'base_domain':'v=7+x,lambda=2+y; x,y>=0','Schur_domain':'lambda=2 or v=7+x,lambda=3+y; x,y>=0',
       'Schur_P_shifted_coefficients':coefficients(fp['P'].n),'small_tables':finite,
       'missing_STS_caps':[cap_data(7),cap_data(9)]}
