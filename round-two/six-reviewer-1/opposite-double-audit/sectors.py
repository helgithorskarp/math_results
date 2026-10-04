"""Independent complete physical-sector polynomial/control check.
Every zero Bernstein slot is retained and inverse-reconstructed.
No target implementation, native fixture or target summary is accessed."""
from pathlib import Path
import sys,json,argparse,signal
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import *
cli=argparse.ArgumentParser();cli.add_argument('--record',type=Path);cli.add_argument('--damage');args=cli.parse_args()
signal.alarm(45)
need(args.damage in [None,'negative-terminal','tensor-negative','tensor-zero-omitted','closed-cut','endpoint-strictness','sharp-leading'],'known sector defect')
inp=json.loads((Path(__file__).resolve().parent/'INPUT.json').read_text())
def even(q):
    q=decode(q);need(all(i%2==0 for i,j in q),'entire numerator/denominator parity')
    return P({(i//2,j):v for(i,j),v in q.items()})
num=even(inp['num_p_t']);den=even(inp['den_p_t']);v=p;a=t
nd=compose(den,-(1+v)*v*v,-(v*(v+2)**2+a))
ng=compose(16*den-num,-(1+v)*v*v,-(v*(v+2)**2+a))
if args.damage=='negative-terminal':ng[max(ng)]=-ng[max(ng)]
need(degree(nd)==degree(ng)==(34,9)and len(nd)==210 and len(ng)==202,'entire negative sector degrees/census')
need(all(x>0 for x in nd.values())and all(x>0 for x in ng.values()),'every negative-sector coefficient')
# Exact polynomial leading terms on the entire physical sharp sequence.
def sharp(q):
    out={}
    for(i,j),x in q.items():out[2*i+j]=out.get(2*i+j,F(0))+x
    return {i:x for i,x in out.items()if x}
sd=sharp(nd);sg=sharp(ng)
if args.damage=='sharp-leading':sg[min(sg)]+=1
need(min(sd)==6 and sd[6]==62208 and min(sg)==7 and sg[7]==497664,'exact sharp sequence leading coefficients')
u=1-v;L=v*(2-v)**2;M=1-v*v+v**3;H=1-L*M
need(H==u**3*(-1+2*u+u*u-u**3),'whole positive nonempty-interval factor')
need(F(-1)+2*F(4,9)+F(4,9)**2-F(4,9)**3==F(-1,729),'strict physical cutoff control')
Y=-(1-v)*v*v;T=L*M+a*H
powers_y=[const(1)];powers_t=[const(1)];powers_m=[const(1)]
for _ in range(11):powers_y.append(powers_y[-1]*Y)
for _ in range(9):
    powers_t.append(powers_t[-1]*T);powers_m.append(powers_m[-1]*M)
def cleared(q):
    return sum((powers_y[i]*powers_t[j]*powers_m[9-j]*x for(i,j),x in q.items()),P())
dn=cleared(den);nn=cleared(num);gg=F(47,2)*dn-nn
need(degree(gg)==(63,9),'whole positive gap degree')
def translate(q,lo,hi):
    out=P();w=F(5,9);length=hi-lo
    for(i,j),x in q.items():
        vx=x*w**i
        for l in range(j+1):
            key=(i,l);out[key]=out.get(key,F(0))+vx*comb(j,l)*lo**(j-l)*length**l
    return P({k:x for k,x in out.items()if x})
def controls(power,n=63,m=9):
    need(all(i<=n and j<=m for i,j in power),'entire tensor degree license')
    first=[[sum((power.get((i,l),F(0))*F(comb(k,i),comb(n,i))for i in range(k+1)),F(0))for l in range(m+1)]for k in range(n+1)]
    return [[sum((first[k][l]*F(comb(j,l),comb(m,l))for l in range(j+1)),F(0))for j in range(m+1)]for k in range(n+1)]
def reconstruct(c,n=63,m=9):
    need(len(c)==n+1 and all(len(r)==m+1 for r in c),'entire tensor slots including zero')
    first=[[sum((c[i][j]*comb(n,i)*comb(n-i,k-i)*(-1)**(k-i)for i in range(k+1)),F(0))for j in range(m+1)]for k in range(n+1)]
    out=P()
    for k in range(n+1):
        for l in range(m+1):
            x=sum((first[k][j]*comb(m,j)*comb(m-j,l-j)*(-1)**(l-j)for j in range(l+1)),F(0))
            if x:out[(k,l)]=x
    return out
def check_leaf(poly,lo,hi,damage=None):
    power=translate(poly,lo,hi);c=controls(power)
    if damage=='tensor-negative':c[-1][-1]=-abs(c[-1][-1])-1
    if damage=='tensor-zero-omitted':c[0].pop(0)
    need(reconstruct(c)==power,'entire inverse Bernstein reconstruction')
    count=[sum(x>0 for r in c for x in r),sum(x==0 for r in c for x in r),sum(x<0 for r in c for x in r)]
    need(count[2]==0 and sum(count)==640,'every closed-leaf control nonnegative')
    endpoints=[sum(r[j]>0 for r in c)for j in [0,9]]
    if damage=='endpoint-strictness':endpoints[1]=0
    need(all(x>0 for x in endpoints),'positive boundary column at every closed shared endpoint')
    return {'closed_interval':[lo,hi],'entire_power_polynomial':power,'all640_controls':c,'positive_zero_negative':count,'positive_endpoint_columns':endpoints}
need(translate(p,F(0),F(1))==F(5,9)*p and translate(t,F(1,2),F(3,4))==F(1,2)+F(1,4)*t,'exact affine chart on both generators')
unsplit=controls(translate(gg,F(0),F(1)))
need(reconstruct(unsplit)==translate(gg,F(0),F(1)),'whole unsplit certificate reconstruction')
need(sum(x<0 for r in unsplit for x in r)==16,'failed unsplit certificate retained honestly')
bounds=[F(0),F(1,2),F(3,4),F(7,8),F(1)]
intervals=list(zip(bounds,bounds[1:]))
if args.damage=='closed-cut':intervals[1]=(intervals[1][0]+F(1,100),intervals[1][1])
need(len(intervals)==4 and intervals[0][0]==0 and intervals[-1][1]==1 and all(lo<hi for lo,hi in intervals)and all(intervals[i][1]==intervals[i+1][0]for i in range(3)),'exact ordered complete closed cover without any gap')
leaves=[check_leaf(gg,lo,hi,args.damage if i==0 else None)for i,(lo,hi)in enumerate(intervals)]
need([x['positive_zero_negative']for x in leaves]==[[619,21,0],[640,0,0],[640,0,0],[640,0,0]],'all four full certificate census checks')
denleaf=check_leaf(dn,F(0),F(1))
need(denleaf['positive_zero_negative']==[619,21,0],'full cleared denominator control census')
# Optional new simple constant, derived only from whole reconstructed controls.
denparts=[controls(translate(dn,lo,hi))for lo,hi in intervals]
numparts=[controls(translate(nn,lo,hi))for lo,hi in intervals]
allratios=[]
for ns,ds in zip(numparts,denparts):
    need(all(x>=0 for r in ds for x in r),'all subdivided denominator controls')
    for nr,dr in zip(ns,ds):
        for n0,d0 in zip(nr,dr):
            if d0:allratios.append(n0/d0)
            else:need(n0==0,'every zero-denominator slot has zero numerator')
ceiling=max(allratios)
simple=next(F(k,4)for k in range(-100,95)if F(k,4)>ceiling)
newleaves=[]
for lo,hi,ns,ds in zip([x[0]for x in intervals],[x[1]for x in intervals],numparts,denparts):
    c=[[simple*d0-n0 for n0,d0 in zip(nr,dr)]for nr,dr in zip(ns,ds)]
    power=translate(simple*dn-nn,lo,hi)
    need(reconstruct(c)==power and all(x>=0 for r in c for x in r),'whole new simple-constant reconstruction')
    need(all(any(r[j]>0 for r in c)for j in [0,9]),'new strict shared-endpoint certificate')
    newleaves.append({'closed_interval':[lo,hi],'all640_controls':c,'entire_power_polynomial':power})
out=encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','negative_denominator_v_A':nd,'negative_16_gap_v_A':ng,'sharp_full_denominator_epsilon':[[i,str(x)]for i,x in sorted(sd.items())],'sharp_full_gap_epsilon':[[i,str(x)]for i,x in sorted(sg.items())],'positive_cleared_denominator':dn,'positive_cleared_numerator':nn,'positive47over2_gap':gg,'all2560_gap_closed_leaf_controls_and_powers':leaves,'all640_unsplit_den_controls_and_power':denleaf,'failed_unsplit_negative_controls':16,'new_complete_control_ratio_ceiling':ceiling,'new_simple_positive_sector_strict_constant':simple,'all2560_new_gap_closed_leaf_controls_and_powers':newleaves,'ordinary_physical_domain_and_strict_basis_bridge_required':True})
data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
if args.record:args.record.write_bytes(data)
else:print(data.decode())
