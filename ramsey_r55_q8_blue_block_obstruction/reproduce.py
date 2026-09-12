"""One complete replay: 546356 cores, literal witnesses and three full parents."""
from pathlib import Path
import argparse,json,subprocess,time,hashlib
import classify,bridge,controls
HERE=Path(__file__).resolve().parent

def run(cache,output):
 output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 classification=classify.run(Path(cache)/'r44_11.g6',output/'classification')
 if classification['blocked']!=[516166]:raise ValueError('classification changed')
 checker=output/'check_witnesses'
 subprocess.run(['g++','-O2','-std=c++17',str(HERE/'check_witnesses.cpp'),'-o',str(checker)],check=True)
 proc=subprocess.run([str(checker),str(Path(cache)/'r44_11.g6'),str(output/'classification/witnesses.u48le'),str(output/'classification/BLOCKED_IDS.txt')],capture_output=True,text=True,check=True)
 witnesses=json.loads(proc.stdout)
 joined=bridge.run(cache,output/'original-joins')
 tested=controls.run(cache,output/'classification',checker,output/'controls')
 result=dict(status='COMPLETE_CLASSIFICATION_AND_THREE_ORIGINAL_EXCLUSIONS_VERIFIED',classification=classification,witness_check=witnesses,original_join=joined,controls=tested,seconds=time.monotonic()-start)
 (output/'REPLAY.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('output');a=p.parse_args();result=run(a.cache,a.output)
 print(json.dumps(dict(status=result['status'],sat=result['witness_check']['sat'],blocked=result['classification']['blocked'],original_exclusions=result['original_join']['new_original_exclusions'],seconds=result['seconds']),indent=2))
