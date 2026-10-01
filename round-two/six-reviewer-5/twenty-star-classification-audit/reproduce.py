"""Cold independent census, classification, full-group fibers and controls."""
from pathlib import Path
import argparse, json, os, subprocess, sys, time, resource
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
 os.environ[name]='1'
from audit import ANCHORS, COLS, ADJ, classify, require, digest
from controls import controls
HERE=Path(__file__).resolve().parent

def invoke(args,work,input_text=None,seconds=35):
 r=subprocess.run(args,input=input_text,text=True,capture_output=True,timeout=seconds)
 require(r.returncode==0,'INCOMPLETE/failed subprocess: '+r.stderr)
 return r

def main():
 a=argparse.ArgumentParser();a.add_argument('--work',type=Path,required=True);a.add_argument('--sanitizers',action='store_true');args=a.parse_args()
 work=args.work.resolve();work.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 flags=['-std=c++17','-Wall','-Wextra','-Wpedantic','-Werror']
 flags += ['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if args.sanitizers else ['-O2']
 binary=work/'cliques';invoke(['g++']+flags+[str(HERE/'cliques.cpp'),'-o',str(binary)],work,seconds=35)
 small=invoke([str(binary),'--self-test'],work);require(small.stdout=='COMPLETE exhaustive-small 6144 22540\n','small exhaustive mismatch')
 graph='225 11\n'+''.join(str(len(row))+' '+' '.join(map(str,row))+'\n' for row in ADJ)
 (work/'graph.txt').write_text(graph)
 cold=invoke([str(binary)],work,input_text=graph)
 fields=cold.stderr.split();require(len(fields)==4 and fields[0]=='COMPLETE','missing native completeness')
 native=dict(nodes=int(fields[1]),leaves=int(fields[2]));require(native['nodes']<=3000000 and native['leaves']<=200000,'native guards')
 leaves=[tuple(map(int,line.split())) for line in cold.stdout.splitlines()]
 require(len(leaves)==native['leaves'],'native output count')
 (work/'leaves.txt').write_text(cold.stdout);(work/'native.txt').write_text(cold.stderr)
 fixtures=json.loads((HERE/'fixtures.json').read_text())['stars']
 result,maps=classify(leaves,fixtures)
 checks=controls(leaves,fixtures,binary,graph)
 result['native']=native;result['controls']=checks
 (work/'positive-maps.json').write_text(json.dumps(maps,separators=(',',':'))+'\n')
 (work/'result.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 expected=json.loads((HERE/'EXPECTED.json').read_text());require(result==expected,'stable expected result differs')
 metrics=dict(wall_seconds=time.monotonic()-start,peak_self_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,python=sys.version,gcc=invoke(['g++','--version'],work).stdout.splitlines()[0],sanitizers=args.sanitizers,result_sha256=digest(result))
 (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
 print(json.dumps(dict(status='COMPLETE',stars=result['labelled_stars'],classes=result['class_count'],full_labelled_count=result['full_labelled_count'],native=native,result_sha256=digest(result),wall_seconds=metrics['wall_seconds']),sort_keys=True))
if __name__=='__main__':main()
