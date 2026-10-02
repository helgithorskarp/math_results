"""Bounded serial whole-carrier replay; complete records stay in chosen scratch."""
from pathlib import Path
import subprocess,json,hashlib,time,os,sys,argparse,resource
HERE=Path(__file__).resolve().parent
THREADS={k:'1'for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']}
def need(ok,message):
 if not ok:raise RuntimeError(message)
def canonical(v):return json.dumps(v,separators=(',',':')).encode()
def coverage(records,total=1652):
 need([z['product']for z in records]==list(range(total)),'whole ordered product coverage')
 need(all(z['partial_maps']==2592 and z['represented_full_maps']==15552 for z in records),'every complete partial carrier')
 need(all(z['expanded_full_maps']==6*z['surviving_partials']for z in records),'every surviving partial fully expanded')
 keys=[(z['first_fixture'],tuple(z['first_mark']),z['second_fixture'],tuple(z['second_mark']))for z in records]
 need(len(set(keys))==total,'every unique product')

def run(work,name,args,guard=45):
 t=time.monotonic();r=subprocess.run([sys.executable,*(['-O']if sys.flags.optimize else []),*map(str,args)],env={**os.environ,**THREADS},capture_output=True,timeout=guard)
 (work/(name+'.stdout')).write_bytes(r.stdout);(work/(name+'.stderr')).write_bytes(r.stderr)
 meta={'name':name,'guard_seconds':guard,'seconds':time.monotonic()-t,'returncode':r.returncode,'peak_rss_upper_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
 need(r.returncode==0,'failed '+name+': '+r.stderr.decode());return meta

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--freeze',action='store_true');args=ap.parse_args();work=args.work
 work.mkdir(parents=True,exist_ok=True);need(not any(work.iterdir()),'fresh empty work directory required');meta=[];records=[]
 for lo in range(0,1652,100):
  hi=min(lo+100,1652);meta.append(run(work,f'census-{lo}-{hi}',[HERE/'census.py',lo,hi,work]));piece=json.loads((work/f'census-{lo}-{hi}.json').read_text());need([z['product']for z in piece]==list(range(lo,hi)),'chunk coverage');records.extend(piece)
 coverage(records);domain=json.loads((work/'domain.json').read_text());full={'domain':domain,'products':records};(work/'full-census.json').write_bytes(canonical(full)+b'\n')
 certificate=json.loads((HERE/'cores.json').read_text());expected_positive=[(e['own_product'],e['map'],e['words'])for e in certificate];actual_positive=[(z['product'],a['map'],a['words'])for z in records for a in z['positives']];need(actual_positive==expected_positive,'all actual positive maps and full word arrays')
 branches={}
 for z in records:
  b=str(z['u_replication'])+str(z['v_replication']);entry=branches.setdefault(b,{'products':0,'positive_products':0,'positive_maps':0,'expanded_full_maps':0});entry['products']+=1;entry['positive_products']+=bool(z['positives']);entry['positive_maps']+=len(z['positives']);entry['expanded_full_maps']+=z['expanded_full_maps']
 meta.append(run(work,'colors',[HERE/'colors.py',work/'full-census.json'],45));meta.append(run(work,'verify',[HERE/'verify.py'],45));verified=json.loads((work/'verify.stdout').read_bytes())
 result={'domain':domain,'products':len(records),'partial_maps':sum(z['partial_maps']for z in records),'represented_full_maps':sum(z['represented_full_maps']for z in records),'by_branch':branches,'whole_census_sha256':hashlib.sha256(canonical(full)+b'\n').hexdigest(),'positives_sha256':hashlib.sha256(canonical(actual_positive)).hexdigest(),'certificate_record':verified}
 output=json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n';(work/'RESULT.json').write_bytes(output)
 (work/'METADATA.json').write_text(json.dumps({'python':sys.version,'optimized':bool(sys.flags.optimize),'native_threads':1,'serial':True,'runs':meta},indent=2)+'\n')
 if args.freeze:(HERE/'expected.json').write_bytes(output)
 else:need(output==(HERE/'expected.json').read_bytes(),'whole frozen mathematical record')
 print(json.dumps({'complete':True,'products':len(records),'cores':len(certificate),'bytes':len(output),'sha256':hashlib.sha256(output).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
