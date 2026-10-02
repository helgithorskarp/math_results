"""Exact boundary controls: necessity, zero pivots and good-prime discipline."""
from fractions import Fraction as F
from polys import cast,symbol,need
from exact import sylvester,evaluate,determinant,coefficients,mt,unit,ma,mm

def checks():
 E,r,v=symbol('E'),symbol('r'),symbol('v');out=[]
 for name,p,q,root in [
  ('leading degree loss',r*E*E+E,r*(E+1),0),
  ('identically zero specialization',r*(E*E+1),E+1,-1)]:
  matrix=sylvester(p,q,'E',2,1);a=evaluate(matrix,{'r':0});column=[F(root)**j for j in [2,1,0]]
  need(determinant(a)==0 and all(sum(x*y for x,y in zip(row,column))==0 for row in a),'full formal-degree evaluation kernel')
  out.append({'name':name,'fixed_matrix':[[str(z) for z in row] for row in a],'whole_evaluation_column':list(map(str,column)),'determinant':'0'})
 # A cross equation is necessary even when a pivot vanishes, never sufficient.
 for name,a0,b0,a1,b1,want in [('one zero affine slope',0,1,1,-2,-1),('both slopes zero incompatible constants',0,0,0,1,0),('both entire affine equations zero',0,0,0,0,0)]:
  cross=a0*b1-a1*b0;need(cross==want,'all affine slopes retained')
  need(a0*(a1*v+b1)-a1*(a0*v+b0)==cast(cross),'whole affine elimination syzygy at zero slopes')
  out.append({'name':name,'rows':[[a0,b0],[a1,b1]],'necessary_cross':cross,'sufficiency_claim':False})
 # Bad reduction can hide a genuine complex factor: coprime images alone fail.
 prime=263;factor=prime*r+1;p=factor*(r+1);q=factor*(r+2)
 aa=mt([int(x) for x in coefficients(p,'r')],prime);bb=mt([int(x) for x in coefficients(q,'r')],prime);u,z=unit(aa,bb,prime)
 need(ma(mm(u,aa,prime),mm(z,bb,prime),prime)==[1],'entire bad-prime image unit')
 need(p.substitute({'r':F(-1,prime)})==q.substitute({'r':F(-1,prime)})==0,'actual common rational root despite image unit')
 need(len(aa)<3 and len(bb)<3,'both leading degrees lost, Gauss rejects')
 out.append({'name':'coprime images with lost common leading degree','prime':prime,'polynomials':[p.record(),q.record()],'common_root':str(F(-1,prime)),'images':[aa,bb],'U':u,'V':z,'unit':[1],'valid_characteristic_zero_exclusion':False})
 # Matrix rank cannot replace scalar conic membership.
 for name,m,point,conic in [('rank2 off scalar conic',[[1,0,-2],[0,1,-1],[0,0,0]],[2,1,1],False),('rank2 on scalar conic',[[1,0,-4],[0,1,-2],[0,0,0]],[4,2,1],True)]:
  need(all(sum(x*y for x,y in zip(row,point))==0 for row in m),'literal whole kernel');need((point[0]*point[2]==point[1]**2)==conic,'exact conic test')
  out.append({'name':name,'matrix':m,'kernel':point,'on_scalar_conic':conic,'actual_original_feasibility_claim':False})
 return out
