"""Direct proof checks and corrupted-certificate rejection; no additional search."""
import copy,json
import verify as V
import geometry as P
from fractions import Fraction as Q
# Distinct algebraic reductions on all basis products and conjugates.
for i in range(16):
 for j in range(16):
  V.need(V.to_a(V.W.mul(V.W.basis(i),V.W.basis(j)))==P.F.mul(V.to_a(V.W.basis(i)),V.to_a(V.W.basis(j))),'basis multiplication')
 V.need(V.to_a(V.W.conjugate(V.W.basis(i)))==P.F.bar(V.to_a(V.W.basis(i))),'basis conjugation')
triangle=[V.ZERO,V.ONE,tuple(map(Q,V.W.W))]
V.need(all(V.W.norm(V.W.sub(triangle[i],triangle[j]))==V.ONE for i in range(3) for j in range(i)),'unit triangle')
data,points,addr,edges=V.reconstruct();cert=json.loads((V.HERE/'certificate.json').read_text());V.check_words(cert,data,edges)
bad=[]
for key,value in [('four_word','0'*data['physical_vertices']),('four_word',cert['four_word'][:-1]),('four_word','9'+cert['four_word'][1:]),('five_word',cert['four_word']),('physical_vertices',data['physical_vertices']-1),('strict_edges',data['strict_edges']-1),('coordinate_sha256','0'*64),('edge_sha256','0'*64)]:
 c=copy.deepcopy(cert);c[key]=value;bad.append(c)
c=copy.deepcopy(cert);c['unknown']=True;bad.append(c)
i,j=edges[0];c=copy.deepcopy(cert);w=list(c['four_word']);w[j]=w[i];c['four_word']=''.join(w);bad.append(c)
rejected=0
for c in bad:
 try:V.check_words(c,data,edges)
 except ValueError:rejected+=1
V.need(rejected==len(bad),'all corruptions rejected')
print(json.dumps({'verified':True,'basis_products_checked':256,'basis_conjugates_checked':16,'unit_triangle':True,'corrupt_certificates_rejected':rejected},indent=2,sort_keys=True))
