#!/usr/bin/env python3
"""Whole finite analytic checks. Standard-library rational arithmetic, same author.

All coefficients and integrals are compared before any extrema/fingerprint.
The compact expected record is a change detector, not the proof of coverage.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb, factorial, isqrt
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
LOW=Q(3,5); H=Q(5,8); C=Q(123,200)
BM=Q(39,64); BX=Q(16,25); AB=Q(195,512); TM=Q(1400,169)
ENERGY=Q(23,5); MASS=Q(184,25); GAMMA=Q(253,400)
ROOT=(LOW,H,Q(0),ENERGY,MASS,Q(8),GAMMA,Q(1),Q(0),ENERGY/8)
PINS=('.gitignore','PROOF.md','LITERATURE.md','README.md','verify.py',
      'validate.py','COVER.json','EXPECTED.json')

def require(ok,message):
    if not ok: raise ValueError(message)
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x): return sha256(canonical(x)).hexdigest()
def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for j,x in enumerate(a):out[j]+=x
    for j,x in enumerate(b):out[j]+=x
    return out
def scale(a,c):return [x*c for x in a]
def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):out[j+k]+=x*y
    return out
def power(a,n):
    out=[Q(1)]
    for _ in range(n):out=mul(out,a)
    return out
def integral(a):return sum((x/Q(j+1) for j,x in enumerate(a)),Q(0))
def strings(a):return [str(x) for x in a]
def ceiling(x,den):
    require(x>=0,'nonnegative square operand')
    n=isqrt(x.numerator*den*den//x.denominator)
    if Q(n,den)**2<x:n+=1
    r=Q(n,den)
    require(r*r>=x and (n==0 or Q(n-1,den)**2<x),'complete rational ceiling')
    return r

def typed_equal(x,y,where='expected'):
    require(type(x) is type(y),'type '+where)
    if isinstance(x,dict):
        require(set(x)==set(y),'keys '+where)
        for k in x:typed_equal(x[k],y[k],where+'.'+k)
    elif isinstance(x,list):
        require(len(x)==len(y),'length '+where)
        for k,(a,b) in enumerate(zip(x,y)):typed_equal(a,b,where+'.'+str(k))
    else:require(x==y,'value '+where)

def floor_root(x,den):
    require(x>=0,'nonnegative lower square operand')
    n=isqrt(x.numerator*den*den//x.denominator);r=Q(n,den)
    require(r*r<=x<(r+Q(1,den))**2,'complete rational lower root')
    return r

def polar_payment(al,ah,tl,th,fh,P,label,damage):
    bm,bx=1-ah**2,1-al**2;ab=min(al*(1-al**2),ah*(1-ah**2))
    c=al+1-al**2-ah
    if damage=='chord-slope':c+=Q(1,1000)
    require(c==al+1-al**2-ah and Q(1,2)<=al<=ah<1,'whole chord endpoint identity')
    require(0<=tl<=th<=TM and 0<=P and 0<fh<=8,'polar input signs '+label)
    delta=floor_root(tl/56,1024);ds=ceiling(Q(7,8)*th,256)
    if damage=='radial-lower-cap':delta+=Q(1,1024)
    require(delta**2<=tl/56<(delta+Q(1,1024))**2,'radial lower root '+label)
    cap=fh-7/(1+ah)-1;D=min(ds,cap)
    require(D>=0 and c-bm*delta>0,'radial positive factors '+label)
    mc=ah+bx*(1+D);nu=bx*(1+D)/mc;mb=ah+c;alpha=c/mb
    require(0<=nu<1 and 0<=alpha<1,'positive reciprocal expansions '+label)
    g2=[Q(0)];g1=[Q(0)]
    for n in range(5):
        z=power([Q(1),-Q(1)],n)
        value=(n+1)*nu**n/mc**2
        if damage=='drop-polar-series' and n==4:value=Q(0)
        g2=add(g2,scale(z,value))
        g1=add(g1,scale(z,alpha**n/mb))
    phase=ab*P;deficit=Q(3,4)*bm*(8-fh)
    if damage=='drop-deficit' and deficit>0:deficit=Q(0)
    K=add(scale([Q(0)]+g2,phase),scale([Q(0)]+g1,deficit))
    radial=mul([ah,c+7*bm*delta],power([ah,c-bm*delta],7))
    if damage=='radial-coefficient':radial[-1]+=Q(1,1000)
    full=mul(radial,add(add([Q(1)],scale(K,-1)),scale(mul(K,K),Q(1,2))))
    if damage=='last-polar-coefficient':full[-1]+=1
    # Independent binomial radial vector and reciprocal basis coefficients.
    factors=[]
    for i in range(9):
        value=Q(0)
        if i<=7:value+=comb(7,i)*ah**(8-i)*(c-bm*delta)**i
        if i>=1:value+=(c+7*bm*delta)*comb(7,i-1)*ah**(8-i)*(c-bm*delta)**(i-1)
        factors.append(value)
    require(radial==factors,'all radial coefficients '+label)
    kernels=[ab*P*(n+1)*nu**n/mc**2+Q(3,4)*bm*(8-fh)*alpha**n/mb for n in range(5)]
    alternateK=[Q(0)]*6
    for n,v in enumerate(kernels):
        for j in range(n+1):alternateK[j+1]+=v*comb(n,j)*(-1)**j
    require(K==alternateK,'all phase/deficit coefficients '+label)
    terms=[(1,n,v) for n,v in enumerate(kernels)]
    weighted=[(0,0,Q(1))]+[(r,n,-v) for r,n,v in terms]
    weighted +=[(r+s,n+k,v*w/2) for r,n,v in terms for s,k,w in terms]
    alternate=[Q(0)]*19;beta_area=Q(0)
    for r,n,v in weighted:
        for i,f in enumerate(factors):
            for j in range(n+1):alternate[i+r+j]+=f*v*comb(n,j)*(-1)**j
            beta_area+=f*v*Q(factorial(i+r)*factorial(n),factorial(i+r+n+1))
    require(len(full)==19 and full==alternate,'whole19 polar coefficients '+label)
    area=integral(full)
    require(area==beta_area,'coefficient/beta integral '+label)
    return dict(label=label,a=strings([al,ah]),T=strings([tl,th]),F_upper=str(fh),phase_lower=str(P),delta=str(delta),max_e_upper=str(D),sqrt_e_upper=str(ds),radius_e_upper=str(cap),kernel_coefficients=strings(K),radial_coefficients=strings(radial),all_coefficients=strings(full),integral=str(area))

def enclose(box,damage):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=box;steps=[]
    for iteration in range(4):
        old=(al,ah,el,eh,fl,fh,ul,uh,wl,wh)
        uh=min(uh,fh/8);ul=max(ul,fl/8-eh/16)
        fl=max(fl,8*ul);fh=min(fh,8*uh+eh/2)
        el=max(el,2*max(Q(0),fl-8*uh),8*((1-uh)**2+wl))
        wh=min(wh,(fh/8)**2-ul*ul,eh/8-(1-uh)**2)
        new=(al,ah,el,eh,fl,fh,ul,uh,wl,wh)
        # Each step is an enclosing intersection; no retained interval grows.
        require(all(new[2*j]>=old[2*j] and new[2*j+1]<=old[2*j+1] for j in range(5)),'enclosing intersection monotonicity')
        steps.append(dict(iteration=iteration,before=strings(old),after=strings(new)))
        failed=[j for j in range(5) if new[2*j]>new[2*j+1]]
        if failed:return dict(status='empty-necessary-inequalities',steps=steps,empty_axes=failed,tightened=strings(new))
    tl=max(Q(0),el-2*(fh-8*ul),(8-fh)**2/8)
    if damage=='wrong-T-lower':tl+=Q(1,1000)
    independent_tl=max(Q(0),el-2*fh+16*ul,(fh**2-16*fh+64)/8)
    require(tl==independent_tl,'retained full lower radial/energy coupling')
    floor=1/(1+ah)
    th=min(eh-2*max(Q(0),fl-8*uh),(fh-7*floor-1)**2+7*(floor-1)**2)
    independent_th=min(eh-max(Q(0),2*fl-16*uh),fh**2-2*fh*(7*floor+1)+56*floor**2+8)
    require(th==independent_th,'retained full upper radial/energy coupling')
    require(fl>=MASS and fh<=8 and floor<=Q(5,8) and fl>7*floor+1,'convex radius-budget endpoint regime')
    out=dict(status='empty-derived-T' if tl>th else 'nonempty-enclosure',steps=steps,tightened=strings(new),T=strings([tl,th]))
    if damage=='false-empty' and out['status']=='nonempty-enclosure':
        require(tl>th,'false whole-box pruning rejected')
    return out

def multinomial_quadratic(a,n):
    out=[Q(0)]*(2*n+1)
    for j in range(n+1):
        for k in range(n-j+1):
            i=n-j-k
            out[j+2*k]+=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*a[0]**i*a[1]**j*a[2]**k
    return out

def origin_payment(path,tight,T,constants,damage):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,T)
    sm=min(Q(1),uh**2+wh,(fh/8)**2)
    energyS=eh-8*((1-uh)**2+wl);jointS=th+2*fh-8-8*(ul**2+wl)
    SM=min(energyS,jointS)
    if damage=='uncouple-energy':SM=eh
    alternate_energy=eh-8+16*uh-8*uh**2-8*wl
    alternate_joint=th+2*fh-8-8*ul**2-8*wl
    require(SM==min(alternate_energy,alternate_joint),'whole mean/energy coupling '+path)
    require(sm>=ul**2,'mean enclosure nonnegative root '+path)
    if SM<0:return dict(status='empty-negative-centered-energy',Smax=str(SM),smax=str(sm))
    beta=[Q(1),-2*al*ul,al*al*sm];b1=sum(beta)
    require(ul>al*sm and 0<b1<1 and 1-al*ul>0,'beta/odd-root signs '+path)
    ds,db,dS=ceiling(sm,1024),ceiling(b1,1024),ceiling(SM,1024)
    require(1-db*b1**4>0 and ah*ds>0,'diagonal signs '+path)
    D=(1-db*b1**4)/(ah*ds)
    root=[Q(1),-al*ul,al**2*(sm-ul**2)/(2*(1-al*ul))]
    if damage=='origin-odd-root':root[-1]*=2
    alternate_root=[Q(1),beta[1]/2,(beta[2]-beta[1]**2/4)/(2+beta[1])]
    require(root==alternate_root,'whole odd-root expression '+path)
    rows=[];R=Q(0)
    for l in range(2,9):
        pol=power(beta,(8-l)//2)
        if l%2:pol=mul(pol,root)
        factor=9*ah**l*constants[l]*SM**(l//2)*(dS if l%2 else 1)
        pol=[Q(0)]*l+scale(pol,factor)
        alternate=multinomial_quadratic(beta,(8-l)//2)
        if l%2:
            raw=[Q(0)]*(len(alternate)+2)
            for j,v in enumerate(alternate):
                raw[j]+=v;raw[j+1]+=v*alternate_root[1];raw[j+2]+=v*alternate_root[2]
            alternate=raw
        alternate=[Q(0)]*l+[v*factor for v in alternate]
        require(pol==alternate,'whole centered coefficients '+path+' order '+str(l))
        area=integral(pol);other=Q(0);n=(8-l)//2
        for j in range(n+1):
            for k in range(n-j+1):
                i=n-j-k;v=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*beta[0]**i*beta[1]**j*beta[2]**k
                base=l+j+2*k+1;pay=Q(1,base)
                if l%2:pay+=alternate_root[1]/Q(base+1)+alternate_root[2]/Q(base+2)
                other+=factor*v*pay
        require(area==other and area>=0,'complete centered integral '+path+' order '+str(l))
        if damage=='origin-drop-eighth' and l==8:continue
        rows.append(dict(l=l,integral=str(area),all_coefficients=strings(pol)));R+=area
    require([x['l'] for x in rows]==list(range(2,9)),'all seven centered orders '+path)
    return dict(status='bounded',path=path,smax=str(sm),Smax=str(SM),energyS=str(energyS),jointS=str(jointS),beta=strings(beta),odd_root=strings(root),dmean=str(ds),dbeta=str(db),dS=str(dS),D=str(D),R=str(R),score=str(D-R),terms=rows)

def compute(damage):
    require(BM==1-H**2 and BX==1-LOW**2 and AB==min(LOW*(1-LOW**2),H*(1-H**2)),'marked endpoint budgets')
    require(C==LOW+1-LOW**2-H and GAMMA==MASS/8-ENERGY/16 and GAMMA>H,'chord/mean budgets')
    require(TM==56*(1-Q(8,13))**2,'complete global radius budget')
    mass=power([H,H*MASS/8],8)
    alternate_mass=[comb(8,i)*H**(8-i)*(H*MASS/8)**i for i in range(9)]
    require(mass==alternate_mass,'whole mass coefficients')
    mass_area=integral(mass)
    require(mass_area==Q(58643076666481,58982400000000) and mass_area<1,'strict mass floor')
    shell=[]
    for k in range(67):
        tl=Q(k,8);th=min(TM,Q(k+1,8));P=max(Q(0),(ENERGY-th)/2)
        row=polar_payment(LOW,H,tl,th,Q(8),P,'energy-'+str(k),damage)
        require(Q(row['integral'])<Q(9999,10000),'energy shell strict inequality '+str(k))
        shell.append(row)
    require(Q(shell[0]['T'][0])==0 and Q(shell[-1]['T'][1])==TM,'whole energy shell endpoints')
    require(all(x['T'][1]==y['T'][0] for x,y in zip(shell,shell[1:])),'whole closed energy shell')
    rho,tau=ceiling(Q(7,8),1024),ceiling(Q(1,8),1024)
    require(rho==Q(479,512) and tau==Q(363,1024),'centered root ceilings')
    c=[Q(1),Q(0)];caps=[]
    for l in range(2,9):
        factors={k:Q(7,8)**((k-2)//2)*(rho if k%2 else 1) for k in range(2,l+1)}
        newton=sum((c[l-k]*factors[k] for k in range(2,l+1)),Q(0))/l
        cs=Q(comb(8,l),8**(l//2))*(tau if l%2 else 1);chosen=min(newton,cs)
        if damage=='centered-third' and l==3:chosen+=Q(1,1000)
        if damage=='newton-eighth' and l==8:chosen+=Q(1,1000)
        c.append(chosen);caps.append(dict(l=l,power_caps={str(k):str(v) for k,v in factors.items()},newton=str(newton),cauchy_maclaurin=str(cs),chosen=str(chosen)))
    require(c==[Q(1),Q(0),Q(1,2),Q(479,1536),Q(11,32),Q(2541,8192),Q(7,128),Q(363,65536),Q(1,4096)],'all finite centered coefficients')
    cover=json.loads((HERE/'COVER.json').read_text())
    require(set(cover)=={'root','splits','leaves'},'complete cover schema')
    typed_equal(cover['root'],strings(ROOT),'root')
    splits=cover['splits'];leaves=cover['leaves'].copy()
    require(type(splits) is dict and type(leaves) is dict,'cover dictionary types')
    if damage=='omit-leaf':leaves.pop(next(iter(leaves)))
    require(all(type(k) is str and type(v) is int and 0<=v<=4 for k,v in splits.items()),'whole split path/axis types')
    require(all(type(k) is str and v in ['empty-necessary-inequalities','origin-passes','polar-excluded'] for k,v in leaves.items()),'whole leaf status types')
    require(not(set(splits)&set(leaves)),'internal/leaf disjointness')
    visited=set();rows=[]
    def walk(path,box):
        require(path not in visited and len(path)<=18,'finite path census')
        visited.add(path)
        require(all(ROOT[2*j]<=box[2*j]<box[2*j+1]<=ROOT[2*j+1] for j in range(5)),'closed box containment')
        if path in splits:
            axis=splits[path];mid=(box[2*axis]+box[2*axis+1])/2
            lo=list(box);hi=list(box);lo[2*axis+1]=mid;hi[2*axis]=mid
            require(lo[2*axis]==box[2*axis] and lo[2*axis+1]==hi[2*axis] and hi[2*axis+1]==box[2*axis+1],'both closed children boundary payment')
            walk(path+'0',tuple(lo));walk(path+'1',tuple(hi));return
        require(path in leaves,'missing closed-cover leaf '+path)
        enclosure=enclose(box,damage);row=dict(path=path,box=strings(box),enclosure=enclosure)
        if enclosure['status'].startswith('empty'):
            require(leaves[path]==enclosure['status'],'exact independently recomputed empty status '+path)
            row['status']=enclosure['status'];rows.append(row);return
        ori=origin_payment(path,enclosure['tightened'],enclosure['T'],c,damage);row['origin']=ori
        require(ori['status']=='bounded','fixed cover retained whole origin '+path)
        if Q(ori['score'])>1:
            require(Q(ori['score'])>Q(2049,2048),'strict coupled origin margin '+path)
            row['status']='origin-passes'
        else:
            al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,enclosure['tightened']);tl,th=map(Q,enclosure['T'])
            po=polar_payment(al,ah,tl,th,fh,max(Q(0),fl-8*uh),path,damage)
            require(Q(po['integral'])<Q(9999,10000),'strict whole coupled polar exclusion '+path)
            row['status']='polar-excluded';row['polar']=po
        require(row['status']==leaves[path],'whole defining leaf choice '+path)
        rows.append(row)
    walk('',ROOT)
    require(visited==set(splits)|set(leaves),'no unreachable cover entry')
    counts={s:sum(x['status']==s for x in rows) for s in sorted(set(x['status'] for x in rows))}
    require(len(visited)==983 and len(splits)==491 and len(leaves)==492,'complete fixed coupled census')
    require(counts=={'empty-necessary-inequalities':16,'origin-passes':230,'polar-excluded':246},'whole three-case census')
    whole=dict(mass_coefficients=strings(mass),mass_integral=str(mass_area),energy_shell=shell,centered_constants=strings(c),constant_derivations=caps,cover=cover,coupled_leaves=rows,trust='ordinary analytic bridges; same-author full cross-method rational coefficients')
    allpolar=shell+[x['polar'] for x in rows if x['status']=='polar-excluded']
    origins=[x for x in rows if x['status']=='origin-passes']
    worst=max(allpolar,key=lambda x:Q(x['integral']))
    least=min(origins,key=lambda x:Q(x['origin']['score']))
    compact_worst={k:v for k,v in worst.items() if k not in ['all_coefficients','radial_coefficients','kernel_coefficients']}
    compact_least={k:least[k] for k in ['path','box','enclosure']}
    compact_least['origin']={k:v for k,v in least['origin'].items() if k!='terms'}
    expected=dict(agent='six-sendov-1',role='researcher',result='PASS',full_checked_record_sha256=digest(whole),mass_integral=str(mass_area),energy_shell_cells=67,coupled_leaves=492,internal_splits=491,leaf_status_counts=counts,full_polar_vectors=313,full_origin_vectors=3332,polar_strict_target='9999/10000',origin_strict_target='2049/2048',worst_polar=compact_worst,least_origin=compact_least,all_coefficients_checked=True,all_closed_cells_checked=True,formalized=False,independent_review=False)
    return expected,whole

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--damage',default='',choices=['','last-polar-coefficient','drop-polar-series','radial-lower-cap','radial-coefficient','chord-slope','drop-deficit','wrong-T-lower','uncouple-energy','centered-third','newton-eighth','origin-odd-root','origin-drop-eighth','omit-leaf','false-empty'])
    parser.add_argument('--record',type=Path,help='Optional private verbose regenerated record')
    args=parser.parse_args()
    if not args.emit:
        manifest=json.loads((HERE/'MANIFEST.json').read_text())
        actual={name:dict(bytes=len((HERE/name).read_bytes()),sha256=sha256((HERE/name).read_bytes()).hexdigest()) for name in PINS}
        typed_equal(actual,manifest['files'],'manifest')
    expected,whole=compute(args.damage)
    if args.emit:
        require(not args.damage and args.expected==HERE/'EXPECTED.json','explicit author emit only')
        args.expected.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:typed_equal(expected,json.loads(args.expected.read_text()))
    if args.record:
        require(HERE not in args.record.resolve().parents,'verbose record remains outside publication')
        args.record.write_text(json.dumps(whole,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(result='PASS',record_sha256=expected['full_checked_record_sha256'],full_polar_vectors=313,full_origin_vectors=3332,coupled_leaves=492,whole_coefficients_cross_checked=True)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
