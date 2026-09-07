"""Independent physical adjacency enumeration; does not import domain producer."""
from itertools import combinations,permutations
from pathlib import Path
from collections import Counter
from math import comb,gcd
import hashlib,json,time

ATOMS={'R4':(4,63),'B4':(4,0),'R3':(3,7),'B3':(3,0),'E3':(3,1),'P3':(3,3)}

def has_clique(rows,vertices,k):
 if k==0:return True
 while vertices.bit_count()>=k:
  bit=vertices&-vertices;vertices^=bit;v=bit.bit_length()-1
  if has_clique(rows,vertices&rows[v],k-1):return True
 return False

def actual_domain(left,right):
 a,amask=ATOMS[left];b,bmask=ATOMS[right];n=a+b
 adj=[0]*n
 for size,bits,off in [(a,amask,0),(b,bmask,a)]:
  for k,(u,v) in enumerate(combinations(range(size),2)):
   if bits>>k&1:adj[off+u]|=1<<(off+v);adj[off+v]|=1<<(off+u)
 universe=(1<<n)-1;bitmap=0;previous=0
 # Gray order changes one actual edge at a time; bit positions remain row-major.
 for k in range(1<<(a*b)):
  state=k^(k>>1);change=state^previous
  if change:
   coordinate=change.bit_length()-1;i,j=divmod(coordinate,b);j+=a
   adj[i]^=1<<j;adj[j]^=1<<i
  previous=state
  if has_clique(adj,universe,5):continue
  opposite=[universe^(1<<v)^adj[v] for v in range(n)]
  if has_clique(opposite,universe,5):continue
  bitmap|=1<<state
 return bitmap

def root_orbits(kind,bitmap):
 n,mask=ATOMS[kind];pairs=list(combinations(range(n),2));edge={p:(mask>>k)&1 for k,p in enumerate(pairs)}
 group=[p for p in permutations(range(n)) if all(edge[tuple(sorted((p[i],p[j])))]==edge[i,j] for i,j in pairs)]
 tables=[[sum(((row>>p[j])&1)<<j for j in range(n)) for row in range(1<<n)] for p in group]
 fixed=[0]*len(group);canonical=0;images=0;allowed=[x for x in range(1<<(4*n)) if bitmap>>x&1]
 for x in allowed:
  rows=[(x>>(i*n))&((1<<n)-1) for i in range(4)];least=x
  for k,table in enumerate(tables):
   y=sum(table[row]<<(i*n) for i,row in enumerate(rows));images+=1
   if not bitmap>>y&1:raise ValueError('child permutation left physical domain')
   fixed[k]+=y==x;least=min(least,y)
  if x==least:canonical|=1<<x
 if sum(fixed)!=len(group)*canonical.bit_count():raise ValueError('Burnside orbit census')
 return canonical,{'child':kind,'group_order':len(group),'fixed_point_sum':sum(fixed),'orbits':canonical.bit_count(),'group_images':images}

def verify(certificate,root_certificate,counts):
 seen=set();maps={};cases=0
 for row in certificate:
  left,right=row['left'],row['right'];key=(left,right)
  if left not in ATOMS or right not in ATOMS or key in seen:raise ValueError('catalog keys')
  seen.add(key);n=ATOMS[left][0]*ATOMS[right][0];bitmap=actual_domain(left,right)
  expected=format(bitmap,f'0{(1<<n)//4}x')
  if row['allowed_bitmap_hex']!=expected or row['count']!=bitmap.bit_count() or row['matrix_bits']!=n:raise ValueError(('physical domain mismatch',key))
  if row['bitmap_sha256']!=hashlib.sha256(bytes.fromhex(expected)).hexdigest():raise ValueError('domain hash')
  cases+=1<<n;maps[key]=bitmap
 if seen!={(a,b) for a in ATOMS for b in ATOMS}:raise ValueError('incomplete domain catalog')
 transports=0
 for (a,b),bitmap in maps.items():
  n,m=ATOMS[a][0],ATOMS[b][0]
  for x in range(1<<(n*m)):
   y=sum(((x>>(i*m+j))&1)<<(j*n+i) for i in range(n) for j in range(m))
   if (bitmap>>x&1)!=(maps[b,a]>>y&1):raise ValueError('transpose mismatch')
   transports+=1
 # Enumerate actual child automorphisms and orbit minima, without signature sorting.
 roots={};root_records=[]
 for row in root_certificate:
  kind=row['child']
  if kind not in ATOMS or kind in roots:raise ValueError('root catalog keys')
  bitmap,record=root_orbits(kind,maps['R4',kind]);n=4*ATOMS[kind][0]
  expected=format(bitmap,f'0{(1<<n)//4}x')
  if row['allowed_bitmap_hex']!=expected or row['count']!=bitmap.bit_count():raise ValueError('root orbit representatives')
  if row['bitmap_sha256']!=hashlib.sha256(bytes.fromhex(expected)).hexdigest():raise ValueError('root bitmap hash')
  roots[kind]=bitmap.bit_count();root_records.append(record)
 if set(roots)!=set(ATOMS):raise ValueError('incomplete root catalog')
 # Count independent factors through atom-type frequencies, not vertex pairs.
 def pair_product(frequencies):
  value=1
  for a in ATOMS:value*=maps[a,a].bit_count()**comb(frequencies[a],2)
  for a,b in combinations(ATOMS,2):value*=maps[a,b].bit_count()**(frequencies[a]*frequencies[b])
  return value
 total=0;unrooted_total=0;branches=set();internal_masks=set()
 for row in counts['branches']:
  r,s,t=row['branch'];types=['R4']*r+['B4']*(7-r)+['R3']*s+['B3']*(4-s)+[('B3','E3','P3','R3')[t]]
  if r not in [5,6,7] or s not in range(5) or t not in range(4) or tuple(row['branch']) in branches:raise ValueError('branch key')
  branches.add(tuple(row['branch']));frequencies=Counter(types);unrooted=pair_product(frequencies)
  frequencies['R4']-=1;value=pair_product(frequencies)
  for a in ATOMS:value*=roots[a]**frequencies[a]
  if value!=row['count'] or unrooted!=row['unrooted_count'] or row['atoms']!=types:raise ValueError('whole branch count')
  total+=value;unrooted_total+=unrooted
  code=0;shift=0
  for a in types:
   n,mask=ATOMS[a];code|=mask<<shift;shift+=comb(n,2)
  if shift!=57 or code in internal_masks:raise ValueError('non-disjoint branches')
  internal_masks.add(code)
 if len(branches)!=60 or total!=counts['retained_rooted_family'] or unrooted_total!=counts['retained_pair_domain_family']:raise ValueError('global count')
 base=60*2**(comb(43,2)-57)
 if counts['raw_packing_family']!=base or not total<2**787 or not total*2**65<base or not total*2**36<unrooted_total:raise ValueError('rooted global reduction bound')
 if not unrooted_total<2**823 or not unrooted_total*2**29<base:raise ValueError('unrooted reduction bound')
 divisor=gcd(total,base)
 if counts['retained_fraction_of_packing']!={'numerator':total//divisor,'denominator':base//divisor}:raise ValueError('exact retained fraction')
 if counts['full_labelled_graph_space']!=2**903 or counts['strict_power_of_two_upper_bound']!=total.bit_length():raise ValueError('global baseline metadata')
 return {'status':'VERIFIED_UNCONDITIONAL_ROOTED_PACKING_DOMAINS_AND_COUNTS','physical_matrix_cases':cases,'transpose_cases':transports,'domains':len(seen),'root_orbits':root_records,'branches':len(branches),'retained_count':total,'unrooted_count':unrooted_total,'strict_global_savings_bits':116,'strict_packing_filter_savings_bits':65,'strict_root_normalization_savings_bits':36}

if __name__=='__main__':
 p=Path(__file__).parent;t=time.monotonic();r=verify(json.loads((p/'DOMAINS.json').read_text()),json.loads((p/'ROOT_DOMAINS.json').read_text()),json.loads((p/'COUNTS.json').read_text()))
 (p/'domain-audit.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'seconds':time.monotonic()-t,**r}))
