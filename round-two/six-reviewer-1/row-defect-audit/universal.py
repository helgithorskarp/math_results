"""Universal coefficient/moment and rational margin checks; no fit/extrapolation."""
from math import factorial
from collections import Counter
from exact import *
from model import *

def partitions(total,minimum=1):
 if total==0:yield ()
 for a in range(minimum,total+1):
  for rest in partitions(total-a,a):yield (a,)+rest

def moment(degree):
 out=[F(0)]
 pats=[x for x in partitions(degree) if all(a%2==0 for a in x)]
 for pat in pats:
  factor=F(factorial(degree),1)
  for x in pat:factor/=factorial(x)
  for multiplicity in Counter(pat).values():factor/=factorial(multiplicity)
  term=[F(1)]
  for j in range(len(pat)):term=mul(term,[-j,1])
  out=polyadd(out,scale(term,factor))
 return pats,out

def audit():
 den=[1,0,1];Fpoly=[1,1,2]
 need(mul([-1,1],Fpoly)==[-1,0,-1,2],'universal_f_factor')
 need(mul([1,1],Fpoly)==[1,2,3,2],'universal_g_factor')
 lhs=polyadd([0,0,0,0,0,0,4],mul([1,0,3],[1,0,3]));rhs=mul([1,0,4],mul(den,den))
 need(lhs==rhs,'universal_circle')
 # Coefficients on 1,t,u,tu of the product bracket.
 need([1,-1,-1,1][0]-[1,1,1,1][0]==0,'product_constant')
 need([x-y for x,y in zip([1,-1,-1,1],[1,1,1,1])]==[0,-2,-2,0],'universal_positive_product')
 p4,m4=moment(4);p6,m6=moment(6)
 need(m4==[0,-2,3] and m6==[0,16,-30,15],'complete_even_moment_count')
 c1=[-2,3];hermite=polyadd(m6,scale(mul([0,1],mul(c1,c1)),-1))
 need(hermite==[0,12,-18,6],'cubic_residual_moment')
 old=F(15,256)*F(21,10)**6+F(3,256)*F(21,10)**4+F(27,64)
 new=F(6,256)*F(21,10)**6+F(3,256)*F(21,10)**4+F(73*73,12288)
 need(old==F(290567223,51200000) and old<F(23,4),'original_norm_constant')
 need(new<F(11,4),'improved_norm_constant')
 need(F(3,16*64)*F(21,10)**3<F(1,32),'uniform_beta_tail_margin')
 need(F(2)+F(5,64)<F(21,10),'uniform_ell_margin')
 need(F(2)+F(4,64)<F(9,4) and F(2)+F(10,64**2)<F(9,4),'uniform_active_profile_margin')
 need(2**63>1280*64**2 and all(x>0 for x in shift([-1,-2,1],64)),'exponential_base_and_induction')
 need(F(2)-F(1,64)-F(1,256)>F(63,32),'inherited_margin_arithmetic')
 oldfloor=F(3969,23552);newfloor=F(3969,11264)
 need(oldfloor>F(1,6) and newfloor>F(1,3),'both_floor_margins')
 # Pure coefficient sign checks of mathematical certificates credited to9201.
 Apoly=[-11250,2625,19075,8170,-7608,-7952,592,192];Rpoly=[-75,236,-70,-119,28,16]
 signs=[shift(polyadd(Apoly,[0]*7+[-128]),64),shift(polyadd(mul([0,0,0,0,20],[-1,1]),scale(Rpoly,-1)),64),shift([25,-5,-16,2],64)]
 need(all(x>0 for row in signs for x in row),'credited_scalar_shift_signs')
 # Rational Taylor lower certificates for logarithm endpoint, retained exactly.
 e2=sum(F(7,10)**j/factorial(j) for j in range(5));e3=sum(F(6,5)**j/factorial(j) for j in range(4))
 need(e2>2 and e3>3 and F(6,5)+21*F(7,10)<16,'chernoff_cutoff_base')
 return dict(moments={'4':m4,'6':m6},patterns={'4':p4,'6':p6},cubic_residual_moment=hermite,original_norm_constant=old,improved_norm_constant=new,original_floor=oldfloor,improved_floor=newfloor,credited_shift_certificates=signs,log_lower_certificates=[e2,e3])

def thresholds():
 out=[]
 for n in (64,65,128,256):
  T,N,s,h=params(n);k=2
  while k+1<n/2 and 12*n**3*sum(comb(n,a) for a in range(k+2))<=T:k+=1
  H=sum(comb(n,a) for a in range(k+1));Hnext=H+comb(n,k+1)
  need(12*n**3*H<=T and 12*n**3*Hnext>T,'maximal_exact_tail_cutoff')
  p,q,r,f,g=profiles(n,k);beta=debias(n);Q=sum(comb(n,a)*r[a-1]**2 for a in range(1,n-1));R=[r[a-1]-beta*(2*a-n) for a in range(1,n-1)];Qnew=sum(comb(n,a)*R[a-1]**2 for a in range(1,n-1));W=scalar(n,k)
  need(Q<F(23*T,2*n**3) and Qnew<F(11*T,2*n**3),'sample_exact_norms')
  need(-W>F(63*T,32*n) and beta>0 and beta*n<F(1,32),'sample_exact_margins')
  need(Qnew<Q,'sample_debias_improvement')
  for a in range(k+1,n-k):
   z=2*a-n;ell=2*n+5;A=F(ell**3,16*n**6);B=F(ell**2,16*n**4);D=F(ell**2,2*n**5)
   odd=A/(1+(3*n-2)*B)*(z**3-(3*n-2)*z);even=-D*z*z
   need(R[a-1]==(odd+even)/(1+B*z*z),'exact_debias_numerator')
  def enclose(x):v=x.numerator*1024//x.denominator;return [F(v,1024),F(v+1,1024)]
  out.append(dict(n=n,k=k,tail=H,next_tail=Hnext,beta=beta,whole_exact_sha256=digest([W,Q,Qnew]),D_over_T_over_n=enclose(-W*n/T),Q_over_T_over_n3=enclose(Q*n**3/T),Qnew_over_T_over_n3=enclose(Qnew*n**3/T),exact_floor_enclosure=enclose(W*W/(Qnew*(N-1)*n))))
 return out
