"""Exact alignment checks for the ordinary proof, not a finite-to-unbounded proof."""
import argparse,hashlib,json,math,os,pathlib,sys,time
from fractions import Fraction as F
from algebra import require,add,scale,mul,evaluate,psd,dot,pascal

def recurrence_records():
    m=[0,1];mp1=[1,1];mp2=[2,1];mp3=[3,1];mm1=[-1,1]
    two_p=[1,2];two_m=[-1,2];two_p3=[3,2]
    ea_den=mul([2],m,two_m,mp3,[2,5,5])
    ea_num=mul(two_p,two_p,mm1,[12,15,5])
    eb_den=mul([4],m,[-1,-2,4])
    eb_num=mul(mm1,[1,6,4])
    oa_den=mul([2],m,mp3,two_p)
    oa_num=mul(two_p3,mp2,two_m)
    ob_den=mul([4],two_p,[-1,2,4])
    ob_num=mul(two_m,[5,10,4])
    claimed=[[12,39,40,-5,10],[1,1,-10,12],[6,1,2],[1,0,16,24]]
    out=[]
    for name,den,num,c in zip(['evenA','evenB','oddA','oddB'],[ea_den,eb_den,oa_den,ob_den],[ea_num,eb_num,oa_num,ob_num],claimed):
        diff=add(den,scale(num,-1));require(diff==c,'whole recurrence '+name)
        out.append(dict(name=name,numerator=num,denominator=den,difference=diff))
    require(add(mul([5],[0,0,0,1],two_m),[12,39,40])==claimed[0],'evenA positive decomposition')
    require(add(mul([2],[0,0,1],[-5,6]),[1,1])==claimed[1],'evenB positive decomposition')
    for k in range(2,35):
        G=pascal(2*k)[k];g=pascal(2*k+2)[k+1]
        ea=F((2*k-1)*G*(5*k*k+5*k+2),2*(k+1)*(k+2)*(k-1)*4**k)
        ean=F((2*k+1)*g*(5*(k+1)**2+5*(k+1)+2),2*(k+2)*(k+3)*k*4**(k+1))
        eb=F(4*k*k-2*k-1,(k-1)*4**k);ebn=F(4*(k+1)**2-2*(k+1)-1,k*4**(k+1))
        oa=F(4*k*(2*k+1)*G,(k+2)*(2*k-1)*4**k)
        oan=F(4*(k+1)*(2*k+3)*g,(k+3)*(2*k+1)*4**(k+1))
        ob=F(4*k*k+2*k-1,(2*k-1)*4**k);obn=F(4*(k+1)**2+2*(k+1)-1,(2*k+1)*4**(k+1))
        for j,(a,b) in enumerate([(ea,ean),(eb,ebn),(oa,oan),(ob,obn)]):
            ratio=F(evaluate(out[j]['numerator'],k),evaluate(out[j]['denominator'],k))
            require(b/a==ratio and 0<ratio<1,'definition-level ratio')
        out.append(dict(m=k,evenA=str(ea),evenB=str(eb),oddA=str(oa),oddB=str(ob)))
    return out

def pair_matrix(s,r,q,lam):
    n=2*q+1;a=[[F(0) for _ in range(n)] for _ in range(n)];a[0][0]=lam
    for i in range(q):
        u=1+2*i;v=u+1
        for x in (u,v):
            a[0][x]=a[x][0]=F(r)
            for y in (u,v):a[x][y]=F(s)
    return a

def matrix_records():
    out=[]
    for s,r,q,cap in ((s,r,q,c) for s in range(1,5) for r in range(1,5) for q in range(0,5) for c in (F(1),F(3,2),F(2))):
        N=2*s+r;h=s+r;t=cap*h+s;v=cap*h-s
        lo=F(q*r*r,s);hi=t-F(2*q*r*r,v)
        require((lo<=hi)==(q*r*r<=s*v),'cap count equivalence')
        if cap==1:
            require(hi==N-2*q*r and (lo<=hi)==(q*r<=s),'original count')
        for side,lam in [('lower',lo),('upper',hi)]:
            a=pair_matrix(s,r,q,lam);upper=[[t*(i==j)-a[i][j] for j in range(len(a))] for i in range(len(a))]
            lower_ok,lp=psd(a);upper_ok,up=psd(upper)
            require(lower_ok==(lam>=lo),'lower exact PSD')
            require(upper_ok==(lam<=hi),'upper exact PSD')
            basis=[[F(int(j==0)) for j in range(len(a))]]
            for i in range(q):basis.append([F(int(j in (1+2*i,2+2*i))) for j in range(len(a))])
            gram=[[sum(x*y for x,y in zip(b,c)) for c in basis] for b in basis]
            lform=[[dot(b,a,c) for c in basis] for b in basis]
            uform=[[dot(b,upper,c) for c in basis] for b in basis]
            for i in range(q+1):
                for j in range(q+1):
                    require(gram[i][j]==((1 if i==0 else 2) if i==j else 0),'unnormalized Gram')
                    le=lam if i==j==0 else 2*r if i==0 or j==0 else 4*s*(i==j)
                    ue=t-lam if i==j==0 else -2*r if i==0 or j==0 else 2*v*(i==j)
                    require(lform[i][j]==le and uform[i][j]==ue,'entire pair-sum form')
            if q:
                ray=[F(q*r,s)]+[F(1)]*(2*q);norm=sum(x*x for x in ray);K=2*s+lo
                require(dot(ray,a,ray)-K*norm==(lam-lo)*F(q*q*r*r,s*s),'Rayleigh identity')
                if lam==lo:
                    require(all(sum(a[i][j]*ray[j] for j in range(len(a)))==K*ray[i] for i in range(len(a))),'restricted endpoint eigenvector')
            out.append(dict(s=s,r=r,q=q,cap=str(cap),side=side,lam=str(lam),lower=lower_ok,upper=upper_ok,lower_pivots=list(map(str,lp)),upper_pivots=list(map(str,up)),matrix=[[str(x) for x in row] for row in a],gram=[[str(x) for x in row] for row in gram],lower_form=[[str(x) for x in row] for row in lform],upper_form=[[str(x) for x in row] for row in uform]))
    return out

def count_records():
    out=[]
    for n in range(4,257):
        N=2**n-n-1;s=2**(n-1)-n;r=n-1;b=pascal(n)
        require(all(v==math.comb(n,j) for j,v in enumerate(b)),'whole Pascal/comb row')
        m=n//2;central=b[m]//2 if n%2==0 else 0;classes=list(range(2,m+(n%2)))
        budget=s//r
        low=[b[a] for a in classes]
        require(sum(low)+central==s-1,'entire complement count')
        necessary=[]
        for ell in range(len(classes)+1):
            residual=sum(low[:len(classes)-ell]);necessary.append(dict(classes=ell,remaining_saturated=residual,allowed=residual<=budget))
        minimum=next(x['classes'] for x in necessary if x['allowed'])
        if n%2==0 and n>=12:require(minimum>=3,'even all-order alignment')
        if n%2 and n>=9:require(minimum>=3,'odd all-order alignment')
        if n in (12,16,24,32,64,128,256):require(minimum=={12:3,16:4,24:5,32:6,64:10,128:15,256:23}[n],'original exact class counts')
        if n<=12:
            ground=(1<<n)-1;members=[x for x in range(1<<n) if x.bit_count()<=n-2];pairs=[(x,ground^x) for x in members if x and ground^x and x<ground^x and ground^x in set(members)]
            require(len(members)==N and len(pairs)==s-1,'literal near cube count')
            require(all(sum(bool(x&(1<<i)) for x in members)==s for i in range(n)),'all literal point stars')
            require([sum(min(x.bit_count(),y.bit_count())==a for x,y in pairs) for a in classes]==low,'all literal size classes')
        out.append(dict(n=n,N=N,s=s,r=r,budget=budget,central_pairs=central,classes=classes,populations=low,minimum_classes=minimum,necessary=necessary))
    even6=-(6-1)*4**6+F((2*6-1)*math.comb(12,6)*(5*6**2+5*6+2),2*(6+1)*(6+2))+4*6**2-2*6-1
    odd4=-(2*4-1)*4**4+F(4*4*(2*4+1)*math.comb(8,4),4+2)+4*4**2+2*4-1
    require(even6==-1110 and odd4==-41,'ordinary induction bases')
    return out

def controls():
    def reject(name,f):
        try:f()
        except ValueError:return dict(name=name,rejected=True)
        raise ValueError('damage accepted '+name)
    out=[]
    out.append(reject('zero diagonal nonzero row',lambda:require(psd([[0,1],[1,2]])[0],'zero PSD kernel')))
    out.append(reject('negative diagonal',lambda:require(psd([[-1,0],[0,2]])[0],'negative PSD')))
    out.append(reject('strictly below lower endpoint',lambda:require(psd(pair_matrix(2,1,2,F(1)-F(1,10)))[0],'lower Schur')))
    a=pair_matrix(2,1,2,F(5)-F(4,1)+F(1,10));up=[[5*(i==j)-a[i][j] for j in range(5)] for i in range(5)]
    out.append(reject('strictly above upper endpoint',lambda:require(psd(up)[0],'upper Schur')))
    out.append(reject('normalized pair sum mistaken Gram',lambda:require(dot([0,1,1],pair_matrix(2,1,1,1),[0,1,1])==4,'Gram normalization')))
    out.append(reject('old cube complement covers enlarged ground',lambda:require((1|2)==7,'entire-ground complement')))
    require((4&1)==(4&2)==0,'new-coordinate disjoint from both old pair')
    out.append(reject('odd central factor half',lambda:require(sum(math.comb(9,a) for a in range(2,5))==F(247-1,2),'odd pair count')))
    out.append(reject('all-order polynomial coefficient changed',lambda:require(add(mul([2],[0,1],[3,1],[1,2]),scale(mul([3,2],[2,1],[-1,2]),-1))==[7,1,2],'odd recurrence')))
    require(psd([[0,0],[0,2]])[0],'genuine singular PSD positive')
    require(psd([[1,1],[1,1]])[0],'genuine zero-kernel positive')
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();t=time.monotonic()
    require(sys.version_info>=(3,10),'Python3.10+')
    out=dict(actual_reviewer='six-reviewer-5',kind='fresh exact alignment and restricted-form controls; ordinary proof separate',recurrences=recurrence_records(),principal_cases=matrix_records(),near_cube=count_records(),controls=controls())
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();pathlib.Path(a.output).write_bytes(raw)
    print(json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),cases=len(out['principal_cases']),near_cube_orders=len(out['near_cube']),damages=len(out['controls']),seconds=time.monotonic()-t,optimized=sys.flags.optimize,python=sys.version)))
if __name__=='__main__':main()
