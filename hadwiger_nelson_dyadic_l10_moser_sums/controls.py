"""Focused failures for exact geometry, compact words, and pinned decoding."""
import base64,copy,json
from fractions import Fraction as F
import geometry as g
import verify as v
import produce

def pack(w):return base64.b64encode(bytes(sum(w[i+j]<<(2*j)for j in range(4))for i in range(0,len(w),4))).decode()
def reject(f):
 try:f()
 except (ValueError,TypeError,KeyError):return
 raise ValueError('invalid control accepted')

def main():
 w=tuple(i%4 for i in range(448));s=pack(w)
 v.need(v.decode(s,448)==w,'packing round trip')
 cert={'format':'two-bit-little-endian-v1','phase_sha256':'fixture','words':[[1,s]]}
 graphs=[[(0,1),(1,2),(0,2)]];ids={'triangle':[0,1,2]};pats={'triangle':[(0,1,2)]}
 v.check_certificate(cert,graphs,ids,pats);bad=[]
 for mask in (0,-1,2,True):
  c=copy.deepcopy(cert);c['words'][0][0]=mask;bad.append(c)
 for word in ('!',s[:-4],pack((0,)*448)):
  c=copy.deepcopy(cert);c['words'][0][1]=word;bad.append(c)
 c=copy.deepcopy(cert);c['words'].append(c['words'][0]);bad.append(c)
 c=copy.deepcopy(cert);c['words']=[];bad.append(c)
 for c in bad:reject(lambda c=c:v.check_certificate(c,graphs,ids,pats))
 reject(lambda:v.decode(base64.b64encode(bytes([0,4])).decode(),5))
 # Norm rational coefficient equals one, but the nonconstant coefficient
 # is sqrt(3)/2, so this is not a unit vector.
 d=g.make({0:F(1,2),2:F(1,2)})
 v.need(sum(r*x*x for r,x in zip(g.RAD+g.RAD,d))==1,'filter control premise')
 den,ps=g.integral([g.ZERO,d]);v.need(g.exact_edges(den,ps)==[] and v.ref_edges(den,ps)[0]==[],'nonconstant norm false positive')
 class Model:
  def conf_budget(self,n):pass
  def solve_limited(self,assumptions):return True
  def get_model(self):return [4*i+1 for i in range(448)if i!=1]+[2,7]
 decoded=produce.solve(Model(),[2])
 v.need(decoded[0]=='1' and decoded[1]=='2','positive-pin selection regression')
 reject(lambda:produce.solve(Model(),[1,2]))
 reject(lambda:produce.solve(Model(),[3]))
 print(json.dumps({'verified':True,'malformed_certificates_rejected':len(bad),'padding_rejected':True,
                   'rational_norm_false_positive_rejected':True,'positive_pin_regression':True,'invalid_pins_rejected':2},sort_keys=True))
if __name__=='__main__':main()
