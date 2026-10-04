"""Whole input-independent signs, original response vectors, moments and motion."""
from fractions import Fraction as Q
from math import comb
from field import E,C,W,Z,I,need
from intervals import physical_cosine
from series import *
from family import family,primitive,from_slots
def decode(s):return [{tuple(e):E(v)for e,v in p}for p in s]
def cubic(v):
    basis=[E(1),C,C*C];rows=[[b.v[j]for b in basis]+[v.v[j]]for j in range(12)]
    for i in range(3):
        k=next(j for j in range(i,12)if rows[j][i]);rows[i],rows[k]=rows[k],rows[i]
        r=rows[i][i];rows[i]=[x/r for x in rows[i]]
        for j in range(12):
            if j!=i:
                r=rows[j][i];rows[j]=[x-r*y for x,y in zip(rows[j],rows[i])]
    need(all(not any(row)for row in rows[3:]),'whole twelve-coordinate real cubic decoding')
    ans=[rows[i][-1]for i in range(3)]
    need(sum((a*b for a,b in zip(ans,basis)),E(0))==v,'entire real cubic reconstruction')
    return ans
def bound(v):
    a=cubic(v);c=physical_cosine();return a[0]+a[1]*c+a[2]*c*c
def run(roots,scalars):
    signs={};checks=[]
    def eq(a,b,name):need(a==b,name);checks.append(name)
    def positive(v,name):
        box=bound(v);need(box.lo>0,'strict original sign '+name);signs[name]=box.record()
    for tau in [0,1]:
        ref=roots[tau][0]['primitive']
        for j in range(9):eq(roots[tau][j]['primitive'],ref,'all whole primitive columns tau'+str(tau)+' label'+str(j))
    ratios=[];motions=[];rnew=[]
    for j in range(9):
        z=W**j;base=decode(roots[0][j]['root']);unit=decode(roots[1][j]['root']);nb=decode(roots[0][j]['normal']);nu=decode(roots[1][j]['normal'])
        eq(base[:10],unit[:10],'all lower original response positions '+str(j))
        eq(pa(unit[10],ps(base[10],-1)),pc(1-z),'entire individual tenth original response '+str(j))
        eq(nb[:10],nu[:10],'all lower normal response positions '+str(j))
        eq(pa(nu[10],ps(nb[10],-1)),pc(-(1-z.real())),'entire individual tenth normal response '+str(j))
        eq(set(base[4]) <= {(0,0)},True,'complete fourth root jet independent of both parameters '+str(j))
        d=base[4].get((0,0),E(0));wj=((3+4*C)*z-(1+2*C)*(1+1/z)-1/z**2)/18
        motions.append({'label':j,'fourth_jet':d.record(),'W':wj.record(),'ideal_square':(d*d.conjugate()).record()})
        if j in [3,4,5,6]:
            A=1-z.real();q=nb[10]
            for k,U in enumerate([7,13,2]):
                v=q.get((k,0),E(0))/A;box=bound(v)
                need(max(abs(box.lo),abs(box.hi))<U,'entire active real-only normal budget '+str((j,k)))
                ratios.append({'label':j,'mu_power':k,'triple':[str(a)for a in cubic(v)],'bound':box.record()})
            aa=-q[0,2];bb=-q[1,2]
            positive(aa,'mixed_a_'+str(j));positive(bb,'mixed_b_'+str(j));positive(2*A-aa,'two_minus_mixed_ratio_a_'+str(j));positive(A-bb,'one_minus_mixed_ratio_b_'+str(j))
            rnew.append((j,aa,bb))
        else:positive(-nb[2][0,0],'inactive_full_original_normal_'+str(j))
    pb=roots[0][0]['primitive'];pu=roots[1][0]['primitive']
    for j in range(10):
        a=decode(pb[j]);b=decode(pu[j]);eq(a[:10],b[:10],'all lower original primitive response '+str(j))
        eq(pa(b[10],ps(a[10],-1)),pc(9 if j==0 else -9 if j==8 else 0),'complete tenth original primitive response '+str(j))
    F0=decode(scalars[0]['F']);F1=decode(scalars[1]['F']);eq(F0[:10],F1[:10],'all lower complete physical scalar response');eq(pa(F1[10],ps(F0[10],-1)),pc(8),'whole physical tenth response eight');eq(F1[11],{},'whole odd scalar response at degree eleven')
    v,A,B,K,p=primitive();H=v['H'];mu=-Q(3,8)*v['L'];Gm=v['Gstar']-Q(3,16)*v['L']**2;ell2=-H*Gm/v['kappa']
    eq(Gm,v['Gmean'],'complete reduced mean-square constant')
    for name,val in [('H',H),('kappa',v['kappa']),('minus_Gstar',-v['Gstar']),('minus_Gmean',-Gm),('gain',v['Gstar']-Gm),('mu_above8',mu-8),('mu_below16',16-mu),('ell2',ell2)]:positive(val,name)
    P0=E(scalars[0]['P0']);P1=E(scalars[0]['P1']);positive(P0,'mixed_fifth_P0');positive(P1,'mixed_fifth_P1')
    fifth=F0[10];fmu=sum((x*mu**i for (i,j),x in fifth.items()if j==0),E(0));J=fmu+(P0+P1*mu)*ell2+5824;U7=2*v['gamma']+3*H*v['k']/7;Lam=U7+J/(2*Gm)
    positive(J-7426,'central_J_lower');positive(7427-J,'central_J_upper');positive(Lam+14,'central_Lambda_lower');positive(-13-Lam,'central_Lambda_upper')
    # Full physical original fourth-motion norms, not scalar averaged surrogates.
    ds=[decode(roots[0][j]['root'])[4].get((0,0),E(0))for j in range(9)];ws=[((3+4*C)*W**j-(1+2*C)*(1+W**(-j))-W**(-2*j))/18 for j in range(9)]
    motionA=(-E(13638695)-64046452*C+83604476*C*C)/972
    sine=(Z**2-Z**34)/(2*I);motionB=sine*(1448+6982*C-8224*C*C)/243;motionQ=(8+25*C+20*C*C)/162
    for j,sgn in [(7,1),(2,-1)]:
        eq(ds[j]*ds[j].conjugate(),motionA,'whole leading motion norm '+str(j));eq(2*(ds[j]*ws[j].conjugate()).imag(),sgn*motionB,'whole mixed motion linear term '+str(j));eq(ws[j]*ws[j].conjugate(),motionQ,'whole mixed motion square '+str(j))
    positive(motionA,'motion_A');positive(motionB/sine,'motion_B_divided_by_positive_sin');positive(motionQ,'motion_Q')
    for j in [0,1,3,4,5,6,8]:positive(motionA-ds[j]*ds[j].conjugate(),'all_other_original_motion_gap_'+str(j))
    # The largest interval on which all four mixed normal t^2 terms are favorable.
    a3,b3=next((a,b)for j,a,b in rnew if j==3);a4,b4=next((a,b)for j,a,b in rnew if j==4)
    positive(a4*b3-a3*b4,'exact_order_of_two_mixed_sign_thresholds');positive(a3-26*b3,'sharp_threshold_above26');positive(27*b3-a3,'sharp_threshold_below27');Rcrit=a3/b3
    # All eight ORIGINAL critical Newton moments from the eight literal slots.
    pair=[{},{}]+ss(sm(K,K),H/2)[:9];moments=[None];el=[sj(1)]
    for k in range(1,9):
        mk=sa(ss(sp(A,k),6),*(ss(sm(sp(B,k-h),sp(pair,h//2)),2*comb(k,h))for h in range(0,k+1,2)))
        moments.append(mk);ek=ss(sa(*(ss(sm(el[k-j],moments[j]),(-1)**(j-1))for j in range(1,k+1))),Q(1,k));el.append(ek)
        eq(ss(ek,(-1)**k),ss(p[9-k],Q(9-k,9)),'whole original critical Newton coefficient '+str(k))
    # Both odd channel primitive columns and all nine original half-normal rows.
    channels=[]
    for order in [7,9]:
        for channel in ['center','scale']:
            aa=[x.copy()for x in A];bb=[x.copy()for x in B];kk=[x.copy()for x in K]
            if channel=='center':put(aa,order,pc(I));put(bb,order,pc(I));factor=9*I;power=8
            else:put(kk,order-2,ONE);factor=9*I*H/7;power=7
            pp0=from_slots(v,aa,bb,kk)[4]
            for j in range(10):
                eq(pp0[j][:order],p[j][:order],'all lower odd primitive channel '+str((order,channel,j)))
                eq(pa(pp0[j][order],ps(p[j][order],-1)),pc(factor if j==0 else -factor if j==power else 0),'whole original odd channel '+str((order,channel,j)))
            for j in range(9):
                z=W**j;response=-factor*(1-z**power)/(9*z**8);normal=(response*z.conjugate()).real();want=z.imag()if channel=='center'else H*(z*z).imag()/7
                eq(normal,want,'whole individual odd normal row '+str((order,channel,j)))
                channels.append({'order':order,'channel':channel,'label':j,'response':response.record(),'normal':normal.record()})
    det=H/7*((W**8).imag()/(W**4).imag()-(W**6).imag()/(W**3).imag());eq(det,-H*(2*C-1)/7,'exact two odd-channel determinant');positive(-det,'nonzero odd channel determinant')
    return {'whole_real_only_ratios':ratios,'all_exact_physical_signs':signs,'all_original_motion_jets':motions,'all_eight_critical_moments':[record(x)for x in moments[1:]],'all_odd_channel_rows':channels,'J16':J.record(),'Lambda16':Lam.record(),'ell_squared':ell2.record(),'sharp_favorable_mixed_mean_threshold':{'Rcrit':Rcrit.record(),'bounds':['26','27'],'new_mean_range':'-min(M,Rcrit)<=mu<=M; tau_M=8+13M+2M^2 on every fixed compact t interval'},'complete_check_names':checks,'complete':True}
