"""Independent coefficient identities for whole row census and infinite cuts.

No CAS, author executable or sampled identity inference. Own9508 sparse
Q[q,k] arithmetic reused and attributed. Counts are integer binomials.
"""
from fractions import Fraction as F
from sparse import poly,add,mul,scale,power,serial,eq,x,y,e,b0,db,pellreduce
from linear import need,canonical,digest

def minus(a,b):return add(a,scale(b,-1))
def algebra():
 q,k=x,y;one=poly(1);qm1=add(q,poly(-1));qm2=add(q,poly(-2));km1=add(k,poly(-1));D=mul(mul(q,qm1),qm2)
 E=e(q,k);N=scale(add(power(q,2),scale(q,13),poly(14),scale(k,-2)),F(1,2))
 c=[add(scale(q,5),poly(6),scale(k,-1)),one,k,minus(q,k),k,minus(q,k),scale(mul(minus(q,k),add(minus(q,k),poly(-1))),F(1,2)),mul(k,minus(q,k)),scale(mul(k,km1),F(1,2))]
 v=add(scale(power(q,2),2),scale(q,2),poly(-2));betaN=scale(qm1,2)
 r=[mul(D,add(one,scale(k,-1))),mul(mul(add(q,mul(scale(k,2),q),scale(k,2)),qm1),qm2),mul(mul(km1,v),qm2),add(D,mul(mul(k,v),qm2)),mul(mul(km1,qm1),qm2),mul(mul(add(q,k),qm1),qm2),mul(add(mul(q,qm2),mul(k,betaN)),qm1),mul(mul(km1,betaN),qm1),mul(add(scale(mul(q,qm2),-1),mul(add(k,poly(-2)),betaN)),qm1)]
 out=[eq(add(*c),N,'every counted row class exhausts N-1'),eq(add(*(mul(a,b)for a,b in zip(c,r))),mul(D,E),'full counted row sum identity')]
 VV=add(*(mul(a,power(b,2))for a,b in zip(c,r)));pairvar=add(*(mul(mul(c[i],c[j]),power(minus(r[i],r[j]),2))for i in range(9)for j in range(i+1,9)))
 out.append(eq(minus(mul(N,VV),power(mul(D,E),2)),pairvar,'whole nonnegative variance pair identity before division'))
 out.append(eq(minus(db(k),power(add(scale(k,5),poly(-2)),2)),mul(add(scale(k,3),poly(-13)),km1),'positive root-square branch for k>=19'))
 out.append(eq(minus(power(scale(add(scale(k,16),poly(-10)),F(1,3)),2),db(k)),scale(add(scale(power(k,2),4),scale(k,4),poly(-53)),F(1,9)),'upper discriminant comparison'))
 out.append(eq(minus(e(add(q,poly(-5)),k),add(scale(k,16),poly(-17),scale(q,-2))),b0(q,k),'root substitution unrestricted positive frontier'))
 out.append(eq(e(scale(k,6),k),add(power(k,2),scale(k,34),poly(7)),'all-k tail e endpoint'))
 # 1500k² times the EXACT displayed rational lower bound.
 num=add(scale(power(k,3),1600),scale(power(k,2),-18655),scale(k,-4224),poly(-480))
 shift=add(scale(power(add(k,poly(19)),3),1600),scale(power(add(k,poly(19)),2),-18655),scale(add(k,poly(19)),-4224),poly(-480))
 expected=add(poly(4159209),scale(k,1019686),scale(power(k,2),72545),scale(power(k,3),1600));out.append(eq(shift,expected,'k19 shifted variance lower-bound cubic'));need(all(v>0 for v in shift.values()),'strict coefficient positivity')
 p,u=x,y;kk=add(u,poly(1));qq=add(scale(u,3),p,poly(-5))
 out.append(eq(minus(scale(e(qq,kk),2),add(scale(u,15),scale(p,-3),poly(-3))),add(power(p,2),scale(power(u,2),-7),poly(-1)),'Pell e identity before norm substitution'))
 out.append(eq(pellreduce(minus(db(kk),power(add(scale(p,2),poly(1)),2))),scale(add(scale(u,5),poly(1),scale(p,-1)),4),'strict Pell lower bracket'))
 out.append(eq(pellreduce(minus(power(add(scale(p,2),poly(3)),2),db(kk))),scale(add(scale(p,3),scale(u,-5),poly(1)),4),'strict Pell upper bracket'))
 pn=add(scale(p,8),scale(u,21));un=add(scale(p,3),scale(u,8));out.append(eq(minus(power(pn,2),scale(power(un,2),7)),minus(power(p,2),scale(power(u,2),7)),'Pell norm preservation'))
 # 12100k² times the exact Pell variance lower bound.
 kk=k;shift2=add(scale(power(add(kk,poly(49)),3),2750),scale(power(add(kk,poly(49)),2),-126125),scale(add(kk,poly(49)),-30336),poly(-3200))
 expected2=add(poly(19218961),scale(kk,7417664),scale(power(kk,2),278125),scale(power(kk,3),2750));out.append(eq(shift2,expected2,'k49 shifted Pell whole variance lower-bound cubic'));need(all(v>0 for v in shift2.values()),'strict Pell coefficient positivity')
 need(F(23,20)-F(352,625)-F(8,625)==F(287,500),'tail decreasing-loss residual')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','identities':out,'whole_variance_cleared_numerator':serial(VV),'classes':9,'positive_root_boundary_k':19,'positive_Pell_lower_polynomial_k':49,'tail_residual':F(287,500),'identity_record_sha256':digest(out)}
if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s exact coefficient phase')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
 print(json.dumps(canonical(algebra()),sort_keys=True,separators=(',',':')))
