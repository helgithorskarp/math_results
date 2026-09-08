"""Audit a fixed LRAT retained-base order obstruction; no SAT or extraction."""
from pathlib import Path
import argparse,hashlib,json,copy
S=Path(__file__).resolve().parent

def need(x,message):
 if not x:raise ValueError(message)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def audit(work,certificate):
 expected=json.loads((S/'EXPECTED.json').read_text());n=expected['vertices'];N=4*n
 need(digest(work/'gate.cnf')==expected['CNF_sha256'],'fixed original CNF hash')
 need(digest(work/'gate.lrat')==expected['LRAT_sha256'],'fixed checked LRAT hash')
 with (work/'gate.cnf').open() as f:
  header=f.readline().split();need(header[:3]==['p','cnf',str(N)],'CNF header');m=int(header[3])
  # Check every one-based original vertex-clause label against its actual CNF row.
  for v in range(n):need(list(map(int,f.readline().split()))==[4*v+c+1 for c in range(4)]+[0],'source vertex clause '+str(v+1))
 with (work/'gate.lrat').open('rb') as f:prelude=f.readline()
 words=prelude.split();need(words[:2]==[str(m).encode(),b'd'] and words[-1]==b'0','initial LRAT deletion record')
 removed=bytearray(m+1);ndel=0
 for word in words[2:-1]:
  j=int(word);need(1<=j<=m and not removed[j],'invalid or duplicate original deletion');removed[j]=1;ndel+=1
 retained=[j for j in range(1,n+1) if not removed[j]];pins=sum(not removed[j] for j in range(m-2,m+1))
 actual={'source_vertices':n,'original_clauses':m,'initial_deletions':ndel,'retained_original_clauses':m-ndel,'retained_vertex_ALO_clauses':len(retained),'retained_edge_clauses':m-ndel-len(retained)-pins,'retained_pins':pins,'prelude_sha256':hashlib.sha256(prelude).hexdigest(),'retained_ALO_labels_sha256':hashlib.sha256(json.dumps(retained,separators=(',',':')).encode()).hexdigest(),'CNF_sha256':expected['CNF_sha256'],'LRAT_sha256':expected['LRAT_sha256']}
 def check(c):
  need(c['scope']=='all_original_clauses_retained_after_fixed_LRAT_prelude','certificate scope')
  for key,value in actual.items():need(c[key]==value,'certificate field '+key)
  witness=c['retained_ALO_witness_509'];need(len(witness)==len(set(witness))==509,'509 distinct witness clauses')
  need(all(type(j)is int and 1<=j<=n and not removed[j] for j in witness),'witness must name retained original vertex clauses')
  need(c['target_vertices']==508 and c['direct_retention_vertex_lower_bound']==len(retained)>508,'retained-base order bound')
 check(certificate)
 bad=[]
 a=copy.deepcopy(certificate);a['retained_ALO_witness_509'][0]=1;bad.append(a) # Clause 1 is deleted by this exact prelude.
 a=copy.deepcopy(certificate);a['retained_ALO_witness_509'][1]=a['retained_ALO_witness_509'][0];bad.append(a)
 a=copy.deepcopy(certificate);a['retained_vertex_ALO_clauses']-=1;bad.append(a)
 a=copy.deepcopy(certificate);a['scope']='all_subgraphs_of_VND_source';bad.append(a)
 for c in bad:
  try:check(c)
  except ValueError:pass
  else:raise ValueError('corrupted certificate accepted')
 return {'verified':True,'status':'VERIFIED_VND_FIXED_RETAINED_BASE_ORDER_GATE','retained_vertex_ALO_clauses':len(retained),'direct_retention_vertex_lower_bound':len(retained),'target_508_possible_for_this_retained_base':False,'negative_controls':len(bad),'SAT_queries':0,'physical_core_extraction_performed':False,'arbitrary_subgraphs_ruled_out':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);a=ap.parse_args();c=json.loads((S/'SUPPORT_GATE.json').read_text());print(json.dumps(audit(a.work.resolve(),c),indent=2))
if __name__=='__main__':main()
