"""six-reviewer-2: independent complete two-five-row exclusion audit."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,subprocess,time,resource
import cores as c
HERE=Path(__file__).resolve().parent
THREAD_ENV={'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','BLIS_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'}

def inputs(target):
 pin=json.loads((HERE/'INPUT.json').read_text())
 for name in ['expected.json','negative_vectors.json']:
  c.need(hashlib.sha256((target/name).read_bytes()).hexdigest()==pin['files'][name],'target input bytes differ: '+name)
 expected=json.loads((target/'expected.json').read_text());cert=json.loads((target/'negative_vectors.json').read_text())
 c.need(cert['dimension']==10 and len(cert['vectors'])==880 and len(cert['profiles'])==56,'certificate dimensions differ')
 from math import gcd
 for v in cert['vectors']:
  c.need(len(v)==10 and all(type(x) is int and abs(x)<=820 for x in v) and gcd(*v)==1 and next(x for x in v if x)>0,'malformed primitive integer vector')
 c.need(len(set(map(tuple,cert['vectors'])))==880,'duplicate vectors')
 for i,p in enumerate(cert['profiles']):
  ids=p['vector_indices'];c.need(p['index']==i and len(ids)==len(set(ids)) and all(type(k) is int and 0<=k<880 for k in ids),'malformed certificate pool')
 return expected,cert

def encode_case(index,a,b,base,d,vec):
 return '\n'.join([str(index),' '.join(map(str,a)),' '.join(map(str,b))]+[' '.join(map(str,r)) for r in base]+[' '.join(map(str,d)),str(len(vec))]+[' '.join(map(str,v)) for v in vec])+'\n'

def run(work,target,node_cap=200000):
 start=time.monotonic();work.mkdir(parents=True,exist_ok=True)
 expected,cert=inputs(target);profiles,core=c.build(expected)
 pairhash=hashlib.sha256();specs=[];records=[];sample=[]
 for index,p in enumerate(profiles):
  localhash=hashlib.sha256();pairs=list(c.row_pairs(p));pool=cert['profiles'][index]['vector_indices'];vec=[cert['vectors'][k] for k in pool]
  for a,b,base,d in pairs:
   encoded=(json.dumps([p['F_mask'],p['stars'],a,b],separators=(',',':'))+'\n').encode();pairhash.update(encoded);localhash.update(encoded)
   # Derive the same degrees by the structural formula, independently of row sums.
   f=c.graph(p['F_mask']);x=[int(i in a)+int(i in b) for i in range(10)]
   direct=[2-x[i] if i<4 else 5-len(f[i-4])-x[i] for i in range(10)]
   c.need(d==direct,'literal row-sum versus incident-slack formula differs')
   specs.append(encode_case(index,a,b,base,d,vec))
  c.need(len(pairs)==expected['profiles'][index]['row_pairs'] and localhash.hexdigest()==expected['profiles'][index]['row_pairs_sha256'],'complete selected row-pair stream differs')
  records.append(dict(index=index,F_mask=p['F_mask'],stars=p['stars'],row_pairs=len(pairs),row_pairs_sha256=localhash.hexdigest()))
 c.need(len(specs)==933 and pairhash.hexdigest()==expected['row_pairs_sha256'],'complete selected-pair census differs')
 (work/'native.input').write_text(str(len(specs))+' '+str(node_cap)+'\n'+''.join(specs))
 prep=time.monotonic()-start
 subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(HERE/'paired_stubs.cpp'),'-lcrypto','-o',str(work/'paired_stubs')],check=True,timeout=60)
 with (work/'native.input').open() as stdin,(work/'native.out').open('w') as stdout:
  subprocess.run([str(work/'paired_stubs')],stdin=stdin,stdout=stdout,check=True,timeout=180)
 lines=(work/'native.out').read_text().splitlines();cases=[];by_profile={}
 for line in lines:
  t=line.split()
  if t[0]=='C':cases.append(dict(case=int(t[1]),index=int(t[2]),states=int(t[3]),nodes=int(t[4]),largest_selected_negative_form=int(t[5])))
  elif t[0]=='P':by_profile[int(t[1])]=dict(states=int(t[2]),state_matrix_sha256=t[3])
  elif t[0]=='COMPLETE':total,nodes,digest=int(t[1]),int(t[2]),t[3]
  else:raise ValueError('unrecognized native output')
 c.need(len(cases)==933 and [x['case'] for x in cases]==list(range(933)),'native omitted selected pair')
 for i,p in enumerate(records):
  actual=by_profile.get(i,dict(states=0,state_matrix_sha256=hashlib.sha256(b'').hexdigest()))
  c.need(actual['states']==expected['profiles'][i]['states'] and actual['state_matrix_sha256']==expected['profiles'][i]['state_matrix_sha256'],'full profile matrix sequence differs')
  p.update(actual)
 c.need(total==1747161 and digest==expected['state_matrix_sha256'],'full residual matrix sequence differs')
 stable=dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='COMPLETE literal paired-stub audit; all negative integer forms checked',core=core,profiles=records,row_pairs=len(cases),states=total,pairing_nodes=nodes,max_pairing_nodes=max(x['nodes'] for x in cases),largest_selected_negative_form=max(x['largest_selected_negative_form'] for x in cases if x['states']),row_pairs_sha256=pairhash.hexdigest(),state_matrix_sha256=digest,certificate_vectors=880,certificate_references=sum(len(p['vector_indices']) for p in cert['profiles']),largest_certificate_coordinate=820,node_guard=node_cap,time_guard_seconds=10)
 (work/'result.json').write_text(json.dumps(stable,sort_keys=True,indent=2)+'\n')
 metrics=dict(seconds=time.monotonic()-start,preparation_seconds=prep,parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,result_sha256=c.sha(stable),max_pairing_nodes=stable['max_pairing_nodes'])
 (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))
 return stable
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--target',type=Path,default=HERE.parent/'book_ramsey_b4_b7_regular110_neighborhood_floor14');a=p.parse_args();run(a.work.resolve(),a.target.resolve())
