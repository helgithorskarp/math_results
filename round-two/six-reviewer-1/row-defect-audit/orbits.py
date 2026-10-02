"""Every star-only free direction; RREF versus separate row elimination."""
from exact import *
from model import *

def audit(n,k):
 sizes=list(range(1,n-1));pairs=[(a,b) for a in sizes for b in sizes if a<=b and a+b<=n]
 A=[]
 for a in sizes:
  A.append([sum(c*comb(n-a,c) for c in sizes if c<=n-a and tuple(sorted((a,c)))==pair) for pair in pairs])
 piv,free,vs=gauss_null(A);expected=[j for j,(a,b) in enumerate(pairs) if a>=2]
 need(free==expected,'all_free_orbits');need(len(piv)==n-2,'full_star_rank')
 T,N,s,h=params(n);p,q,r,f,g=profiles(n,k);counts=[comb(n,a) for a in sizes]
 B=base(n);K,U=physical(n,B);W=energy(K,p)+energy(U,q);need(W==scalar(n,k),'whole_base_scalar')
 for a in sizes:
  need(sum(weight(B,a,b)*comb(n-a,b) for b in sizes if b<=n-a)==T-2,'base_center')
  need(sum(b*weight(B,a,b)*comb(n-a,b) for b in sizes if b<=n-a)==(n-a)*s,'base_stars')
 records=[]
 for j,v in zip(free,vs):
  b={pairs[x]:v[x] for x in range(len(pairs))};direct={pairs[j]:F(1)}
  for a in sizes[1:]:direct[1,a]=-sum(c*comb(n-a,c)*weight(direct,a,c) for c in sizes[1:] if c<=n-a)/F(n-a)
  direct[1,1]=-sum(c*comb(n-1,c)*weight(direct,1,c) for c in sizes[1:])/F(n-1)
  need([weight(direct,*pair) for pair in pairs]==v,'independent_decoder')
  D=[[F(comb(n,a))*weight(b,a,c)*comb(n-a,c) if c<=n-a else F(0) for c in sizes] for a in sizes]
  row=[sum(D[a-1])/counts[a-1] for a in sizes];sigma=dot(counts,row)
  need(any(row),'nonzero_row_defect');need(dot([a*counts[a-1] for a in sizes],row)==0,'cardinality_orthogonality')
  signed=F(0);coeffs=[]
  for a,c in pairs:
   coeff=F((2-(a==c))*comb(n,a)*comb(n-a,c))*(f[a-1]*f[c-1]-g[a-1]*g[c-1])
   if a+c<n and min(a,c)>k:need(coeff>0,'positive_omitted_coefficient')
   else:need(coeff==0,'individual_allowed_cancellation')
   signed+=coeff*weight(b,a,c);coeffs.append(coeff)
  directenergy=energy(D,p)-energy(D,q)
  correction=-F(n*n-6,n*n)*sigma+dot([r[a-1]*counts[a-1] for a in sizes],row)
  need(directenergy==signed+correction,'unaveraged_defect_identity')
  if all(row[a-1]==0 for a in sizes if a>k):need(correction==F(n*n-4,n*n)*sigma,'low_layer_specialization')
  beta=debias(n);R=[r[a-1]-beta*(2*a-n) for a in sizes]
  sharpen=- (F(n*n-6,n*n)+beta*n)*sigma+dot([R[a-1]*counts[a-1] for a in sizes],row)
  need(sharpen==correction,'debiased_exact_identity')
  records.append({'free_pair':pairs[j],'row':row,'sigma':sigma,'physical_energy':directenergy,'signed':signed,'correction':correction,'direction_sha256':digest(D)})
 return {'n':n,'k':k,'rank':len(piv),'directions':records,'base_scalar':W,'pair_count':len(pairs)}
