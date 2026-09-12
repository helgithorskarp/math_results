"""Generate the full classification, check every witness, and verify its proof."""
from pathlib import Path
import argparse,json,time
import classify,verify,controls

def run(catalog,output,seconds=1800):
 output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 generation=classify.run(catalog,output/'classification',seconds)
 verification=verify.run(catalog,output/'classification',output/'verification')
 checks=controls.run(catalog,output/'classification/witnesses.u112le',output/'controls')
 result=dict(status=verification['status'],generation=generation,verification=verification,controls=checks,seconds=time.monotonic()-start)
 (output/'REPLAY.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('output');p.add_argument('--seconds',type=float,default=1800);a=p.parse_args();r=run(a.catalog,a.output,a.seconds);print(json.dumps(dict(status=r['status'],seconds=r['seconds']),indent=2))
