"""Independent Hermite/phase finite audit; disclosed reuse of own old engines.

No author's module, file certificate or expected output is imported.
"""
import argparse,json
from pathlib import Path
from math import comb,isqrt
from arithmetic import (F,require,add,scale,mul,power,integrate,pad,bproduct,
 bpower,elevate,btopower,bintegrate,kernel_bernstein,ceiling,encode)


def floor_root(x,denom):
    target=x*denom**2;k=isqrt(target.numerator//target.denominator)
    require(k*k<=target<(k+1)**2,'entire rational lower root rounding')
    return F(k,denom)


def constants():
    rho,tau=F(479,512),F(363,1024)
    require(rho*rho>=F(7,8) and tau*tau>=F(1,8),'finite-cardinality root caps')
    eta=[F(0),F(0)]+[F(7,8)**((k-2)//2)*(rho if k%2 else 1)for k in range(2,9)]
    c=[F(1),F(0)];mins=[]
    for l in range(2,9):
        newton=sum((c[l-k]*eta[k]for k in range(2,l+1)),F(0))/l
        maclaurin=comb(8,l)*F(1,8)**(l//2)*(tau if l%2 else 1)
        c.append(min(newton,maclaurin));mins.append({'l':l,'newton':newton,'maclaurin':maclaurin,'chosen':c[l]})
    require(c[2:]==[F(1,2),F(479,1536),F(11,32),F(2541,8192),F(7,128),F(363,65536),F(1,4096)],'every complete recursive minimum')
    return c,eta,mins


def mass_floor():
    h,c,m=F(3,5),F(13,20),F(93,100)
    p=power([h,c*m],8);b=bpower([h,h+c*m],8)
    require(p==btopower(b) and integrate(p)==bintegrate(b)<1,'whole mass floor polynomial and independent integral')
    return {'coefficients':p,'bernstein':b,'integral':integrate(p)}


def polar_cells(m=F(1),damage=None):
    h,c,blo,bhi,Astar=F(3,5),F(13,20),F(16,25),F(279,400),F(3069,8000)
    eta=m-1;gamma=(m-F(5,8))/F(3,8);slope=c+bhi*eta
    require(eta>=0 and gamma>=1,'fixed positive mass-budget perturbation')
    cells=[]
    for k in range(63):
        L,U=gamma*gamma*F(k,8),gamma*gamma*F(k+1,8)
        delta=gamma*floor_root(F(k,8)/56,1024)
        D=gamma*ceiling(F(7,8)*F(k+1,8),256)
        if damage=='radial-lower' and k==0:delta+=F(1,1024)
        require(delta*delta<=L/56 and D*D>=F(7,8)*U,'both full radial root payments')
        P=max(F(0),(F(17,4)-U-8*eta*eta)/2)
        M=h+bhi*(m+D);nu=bhi*(m+D)/M
        require(0<=nu<1 and slope-blo*delta>0,'radial positivity and reciprocal expansion domain')
        G=[(j+1)*nu**j/M**2 for j in range(5)]
        if damage=='phase-reciprocal' and k==0:G[0]*=2
        require(G[0]==1/M**2 and P>=0,'nonnegative phase-loss kernel')
        z=[F(1),F(-1)];K=[F(0)];kernels=[]
        for j,g in enumerate(G):
            payment=Astar*P*g;K=add(K,scale([F(0)]+power(z,j),payment));kernels.append((1,j,payment))
        radial=mul([h,slope+7*blo*delta],power([h,slope-blo*delta],7))
        bracket=add(add([F(1)],scale(K,-1)),scale(mul(K,K),F(1,2)))
        coeff=pad(mul(radial,bracket),18)
        kb=kernel_bernstein(kernels,5)
        require(pad(K,5)==btopower(kb),'entire retained phase polynomial')
        br=[F(1)-v+w/2 for v,w in zip(elevate(kb,10),bproduct(kb,kb))]
        rb=bproduct([h,h+slope+7*blo*delta],bpower([h,h+slope-blo*delta],7))
        whole=bproduct(rb,br)
        if damage=='polar-terminal' and k==4:coeff[-1]+=1
        require(coeff==btopower(whole),'EVERY one of19 polar coefficients, including ordered phase squares')
        integral=integrate(coeff);require(integral==bintegrate(whole),'entire polar integral by two bases')
        require(integral<F(9999,10000),'individual strict polar sufficient bound')
        require(k==0 or L==cells[-1]['U'],'closed adjacent radial cells')
        cells.append({'k':k,'L':L,'U':U,'delta':delta,'D':D,'P':P,'m':m,'slope':slope,'M':M,'nu':nu,'G':G,'K':pad(K,5),'radial':radial,'coefficients':coeff,'bernstein':whole,'integral':integral})
    require(cells[0]['L']==0 and cells[-1]['U']==56*(m-F(5,8))**2,'whole exact perturbed radial domain')
    return cells


def topology(plan,m=F(1),damage=None):
    fixed=tuple(map(F,plan['root']))
    require(fixed==(F(11,20),F(3,5),F(1063,1600),F(1),F(0),F(17,32)),'declared entire original root')
    leaves=list(plan['leaves']);splits=dict(plan['splits'])
    if damage=='missing-leaf':leaves.pop()
    if damage=='illegal-axis':splits['']=3
    require(len(leaves)==len(set(leaves))==272 and len(splits)==271,'whole node census')
    leafset,internal=set(leaves),set(splits);prefixes={p[:i]for p in leaves for i in range(len(p))}
    require(prefixes==internal and not leafset&internal,'all proper prefixes and no prefix leaf')
    require(all(set(p)<={'0','1'}for p in leafset|internal),'all binary paths')
    require(sum((F(1,2**len(p))for p in leaves),F(0))==1,'complete prefix-code coverage')
    require(all(p+'0'in leafset|internal and p+'1'in leafset|internal for p in internal),'EVERY pair of closed children')
    require(all(type(a)is int and a in(0,1,2)for a in splits.values()),'all legal source split axes')
    root=(*fixed[:3],m,*fixed[4:]);boxes={'':root}
    for path in sorted(leafset|internal,key=lambda p:(len(p),p)):
        if not path:continue
        parent=path[:-1];bit=int(path[-1]);box=list(boxes[parent]);j=2*splits[parent];mid=(box[j]+box[j+1])/2;box[j+1-bit]=mid
        require(box[j]<box[j+1],'both nondegenerate closed halves');boxes[path]=tuple(box)
    split_rows=[]
    for path,axis in sorted(splits.items()):
        a,b,r=boxes[path+'0'],boxes[path+'1'],boxes[path];i=2*axis
        require(a[i]==r[i] and a[i+1]==b[i] and b[i+1]==r[i+1] and all(a[j]==b[j]==r[j]for j in range(6)if j not in(i,i+1)),'all closed midpoint unions without discarded boxes')
        split_rows.append({'path':path,'axis':axis,'parent':r,'lower':a,'upper':b})
    return root,[(path,boxes[path])for path in sorted(leaves)],split_rows


def origin_leaves(plan,m=F(1),damage=None):
    root,leaves,splits=topology(plan,m,damage);c,eta,mins=constants();out=[]
    require(F(1063,1600)>F(3,5)*m*m,'whole feasible derivative monotonicity on perturbed mass budget')
    for path,box in leaves:
        A,B,U,V,W,X=box;s=min(m*m,V*V+X)
        # The interval can straddle u=1 after perturbation; retain its interior maximum.
        S=F(17,4)-8*(max(F(0),1-V)**2+W)
        beta=[F(1),-2*A*U,A*A*s];beta1=sum(beta)
        require(s>=U*U and S>=0 and U>A*s and 0<beta1<1 and 1-A*U>0,'all origin signs and feasible budgets')
        ds=min(m,ceiling(s,1024));db=ceiling(beta1,1024);dS=ceiling(S,1024)
        require(ds*ds>=s and db*db>=beta1 and dS*dS>=S,'every upper square-root enclosure')
        q2=A*A*(s-U*U)/(2*(1-A*U));Q=[F(1),-A*U,q2];bb=[F(1),1-A*U,beta1];qb=[F(1),1-A*U/2,1-A*U+q2]
        require(btopower(bb)==beta and btopower(qb)==Q and min(bb)>0 and min(qb)>0,'entire positive mean root envelopes')
        numerator=1-db*beta1**4;require(numerator>0,'strict diagonal numerator');D=numerator/(B*ds);terms=[]
        for l in range(2,9):
            H=power(beta,(8-l)//2);hb=bpower(bb,(8-l)//2)
            if l%2:H=mul(H,Q);hb=bproduct(hb,qb)
            coeff=[F(0)]*l+H;cb=bproduct([F(0)]*l+[F(1)],hb)
            require(coeff==btopower(cb),'ALL coefficients at ALL centered orders2..8')
            I=integrate(coeff)
            if damage=='lost-eighth-integral' and path==leaves[0][0] and l==8:I-=F(1,1000000)
            require(I==bintegrate(cb),'entire rational origin integral in separate basis')
            weight=9*B**l*c[l]*S**(l//2)*(dS if l%2 else 1)
            require(weight>=0,'every nonnegative centered payment')
            terms.append({'l':l,'constant':c[l],'coefficients':coeff,'bernstein':cb,'integral':I,'weight':weight,'term':weight*I})
        R=sum((t['term']for t in terms),F(0));value=D-R
        if damage=='lost-origin-margin' and path==leaves[0][0]:value=F(257,256)
        require(len(terms)==7 and value>F(257,256),'EVERY individual strict origin bound')
        require(value>m**8,'diagonal remainder strictly beats original product mass cap')
        out.append({'path':path,'box':box,'s':s,'S':S,'beta':beta,'beta1':beta1,'Q':Q,'ds':ds,'db':db,'dS':dS,'D':D,'terms':terms,'R':R,'bound':value})
    return root,splits,out,mins


def run(plan,damage=None):
    modes=[]
    for m in [F(1),F(1000001,1000000)]:
        polar=polar_cells(m,damage);root,splits,origin,mins=origin_leaves(plan,m,damage)
        largest=max(polar,key=lambda r:r['integral']);smallest=min(origin,key=lambda r:r['bound'])
        modes.append({'mass_m':m,'first_power_budget':8*m,'radial_gamma':(m-F(5,8))/F(3,8),'polar':polar,'origin_root':root,'all_closed_splits':splits,'all_newton_maclaurin_minima':mins,'origin':origin,'polar_max':{'k':largest['k'],'value':largest['integral']},'origin_min':{'path':smallest['path'],'value':smallest['bound']}})
    base=modes[0]
    require(base['polar_max']['k']==12 and base['origin_min']['path']=='0101101000','complete original extrema positions')
    return encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','target':'10131/index1','written_proof_exposed_NOT_BLIND':True,'no_native_code_import':True,'disclosed_reuse':'own previously published arithmetic/Gaussian engines, source5c74c815; no new native target imports','mass_floor':mass_floor(),'two_exact_mass_budgets':modes,'ordinary_new_annular_gap_claim':'F>8+1/125000 on closed marked annulus[11/20,3/5] ONLY; lower region still uses exact stated parent scope.'})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,default=Path(__file__).with_name('PLAN.json'));p.add_argument('--damage',choices=['radial-lower','phase-reciprocal','polar-terminal','missing-leaf','illegal-axis','lost-eighth-integral','lost-origin-margin']);p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=run(json.loads(a.plan.read_text()),a.damage);a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'mass_budgets':[(m['mass_m'],m['polar_max'],m['origin_min'])for m in out['two_exact_mass_budgets']]}))
