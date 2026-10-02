"""Standalone independent reproduction. Fixed90s mathematical guard."""
from pathlib import Path
import argparse,json,hashlib,signal,sys
from exact import COUNTS,canonical,text,digest,need
import orbits,literal,universal,controls

def run():
 COUNTS.clear()
 record={'schema':1,'reviewer':'six-reviewer-1','role':'independent mathematical reviewer','target':9269,'imported_unbounded_scalar':'9201 W<-2T/n+20n+3nB; 9245 prior factor-two criterion','orbits':[orbits.audit(n,k) for n,k in [(7,2),(8,3),(17,3),(20,4)]],'literal':[literal.audit(7,2),literal.audit(8,2),literal.audit(8,3)],'permutation':literal.permutation_control(),'universal':universal.audit(),'thresholds':universal.thresholds(),'controls':controls.audit()}
 record['checks']=dict(sorted(COUNTS.items()));return text(record)

def compare_expected(supplied,generated):
 if supplied!=generated:raise ValueError('complete frozen record mismatch')

def main():
 signal.alarm(90);parser=argparse.ArgumentParser();parser.add_argument('--write');parser.add_argument('--check');args=parser.parse_args();r=run();data=json.dumps(r,sort_keys=True,indent=2)+'\n'
 if args.write:Path(args.write).write_text(data)
 if args.check:
  supplied=Path(args.check).read_bytes();compare_expected(supplied,data.encode())
 signal.alarm(0)
 print(json.dumps({'whole_record_sha256':hashlib.sha256(data.encode()).hexdigest(),'bytes':len(data.encode()),'directions':sum(len(x['directions']) for x in r['orbits']),'literal_orders':[x['N'] for x in r['literal']],'rejected_damages':len(r['controls']['rejected']),'exact_predicates':sum(r['checks'].values()),'new_floor':r['universal']['improved_floor'],'checks':r['checks']},indent=2))
if __name__=='__main__':main()
