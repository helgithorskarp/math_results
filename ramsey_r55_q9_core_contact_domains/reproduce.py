"""One fresh replay of the declared global reduction; all bulky output stays local."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys,time
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)
def run(cache,out,record=False):
    out=Path(out).resolve();out.mkdir();cache=Path(cache).resolve();start=time.monotonic()
    sys.path.insert(0,str(HERE));from inputs import catalogue
    catalogue(cache,download=True)
    def call(command,label):
        with (out/(label+'.log')).open('xb') as log:result=subprocess.run([str(x) for x in command],stdout=log,stderr=subprocess.STDOUT)
        need(result.returncode==0,'stage failed: '+label+'; see '+str(out/(label+'.log')))
        print(json.dumps(dict(completed=label,seconds=time.monotonic()-start)),flush=True)
    base=['g++','-std=c++20','-Wall','-Wextra','-Wpedantic']
    for mode,flags in (('release',['-O3']),('sanitized',['-O1','-g','-fno-omit-frame-pointer','-fsanitize=address,undefined'])):
        for source in ('row_count','column_check'):
            exe=out/(source+'-'+mode);call(base+flags+[HERE/(source+'.cpp'),'-o',exe],'build-'+source+'-'+mode)
            output=out/(source+'-'+mode+'.tsv');command=[exe,cache/'r44_7.g6',output]
            if source=='row_count':command += [362,out/('prefix-'+mode+'.bin')]
            call(command,source+'-'+mode)
    need((out/'row_count-release.tsv').read_bytes()==(out/'row_count-sanitized.tsv').read_bytes()==(HERE/'COUNTS.tsv').read_bytes(),'row reproducibility')
    need((out/'column_check-release.tsv').read_bytes()==(out/'column_check-sanitized.tsv').read_bytes(),'column reproducibility')
    need((out/'prefix-release.bin').read_bytes()==(out/'prefix-sanitized.bin').read_bytes(),'table reproducibility')
    results=[]
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal';python=[sys.executable]+(['-O'] if optimized else [])+['-B']
        census=out/(mode+'-census.json');rows=out/'row_count-release.tsv';columns=out/'column_check-release.tsv';tables=out/'prefix-release.bin'
        call(python+[HERE/'check_counts.py',cache,rows,columns,tables,'--output',census],mode+'-census')
        call(python+[HERE/'controls.py',cache,tables,out/(mode+'-physical')],mode+'-physical')
        call(python+[HERE/'controls.py',cache,tables,out/'unused','--small'],mode+'-small')
        call(python+[HERE/'corruptions.py',cache,tables,rows,columns,out/(mode+'-corruptions')],mode+'-corruptions')
        results.append(dict(census=json.loads(census.read_text()),physical=json.loads((out/(mode+'-physical')/'PHYSICAL.json').read_text()),
            small=json.loads((out/(mode+'-small.log')).read_text()),corruptions=json.loads((out/(mode+'-corruptions')/'CONTROLS.json').read_text())))
    need(results[0]==results[1],'normal/optimized discrepancy');need(results[0]['census']['gate']=='PASS','declared numerical gate')
    if not record:need(results[0]==json.loads((HERE/'EXPECTED.json').read_text()),'committed expectation mismatch')
    (out/'RESULT.json').write_text(json.dumps(results[0],sort_keys=True,indent=2)+'\n')
    receipt=dict(status='RECORDED_Q9_CONTACT_GLOBAL_REDUCTION' if record else 'REPRODUCED_Q9_CONTACT_GLOBAL_REDUCTION',
        seconds=time.monotonic()-start,python=sys.version,platform=platform.platform(),
        result_sha256=hashlib.sha256((out/'RESULT.json').read_bytes()).hexdigest(),target_found=False,new_task_decisions=0,solver_calls=0)
    (out/'REPLAY.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('out');p.add_argument('--record',action='store_true');a=p.parse_args()
    print(json.dumps(run(a.cache,a.out,a.record),sort_keys=True))
