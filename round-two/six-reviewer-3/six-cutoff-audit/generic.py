"""Whole free-variable rank-one identities, using credited OWN Gaussian kernel."""
from polys import symbol,need

def derive():
 T,V,B,A,C,e,t=[symbol(n) for n in ['T','V','B','A','C','e','t']]
 D=T*V-B**2;Ds=D+t*T;oldnum=e*D-(V*A**2-2*B*A*C+T*C**2)
 newnum=(e+t)*Ds-((V+t)*A**2-2*B*A*(C+t)+T*(C+t)**2)
 a=(V+t)*A-B*(C+t);b=T*(C+t)-B*A
 need(T*a+B*b-A*Ds==0,'whole free-variable first adjusted stationary equation')
 need(B*a+(V+t)*b-(C+t)*Ds==0,'whole free-variable second adjusted stationary equation')
 square=(D-(T*C-B*A))**2
 left=newnum*D-oldnum*Ds;right=t*square
 need(left==right,'whole generic adjusted-minus-old residual identity')
 dominant=t*square*Ds-left*D
 need(dominant==t*t*T*square,'whole generic strict comparison numerator')
 return {'residual_difference_left':left.record(),'residual_difference_right':right.record(),'dominance_left':dominant.record(),'dominance_right':(t*t*T*square).record(),'ordinary_conditions':'T>0,D>0,t>0 and D-(T*C-B*A)!=0 make the domination strict; exact universal polynomial identities have no finite sample premise'}
