"""Fresh complete replay of the single three-block global-reduction milestone."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys,time
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)
def run(out,record=False):
    out=Path(out).resolve();out.mkdir();start=time.monotonic()
    def call(command,label):
        with (out/(label+'.log')).open('xb') as log:r=subprocess.run([str(x) for x in command],stdout=log,stderr=subprocess.STDOUT)
        need(r.returncode==0,'stage failed: '+label+'; inspect '+str(out/(label+'.log')))
        print(json.dumps(dict(completed=label,seconds=time.monotonic()-start)),flush=True)
    # No input downloads, solver, historical source states, or h4059 replay.
    call([sys.executable,'-B',HERE/'count.py',out/'producer'],'producer')
    call([sys.executable,'-B',HERE/'global_bound.py',out/'producer/LOCAL.json','--out',out/'GLOBAL.json'],'global')
    for mode,flags in (('release',['-O3']),('sanitized',['-O1','-g','-fno-omit-frame-pointer','-fsanitize=address,undefined'])):
        exe=out/('independent-'+mode);(out/mode).mkdir()
        call(['g++','-std=c++20','-Wall','-Wextra','-Wpedantic',*flags,HERE/'independent_count.cpp','-o',exe],'build-'+mode)
        need((out/('build-'+mode+'.log')).stat().st_size==0,'strict compiler warning')
        call([exe,out/mode],'count-'+mode)
    for p in (out/'release').iterdir():need(p.read_bytes()==(out/'sanitized'/p.name).read_bytes(),'native mode mismatch')
    results=[]
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal';python=[sys.executable]+(['-O'] if optimized else [])+['-B']
        call(python+[HERE/'verify.py',out/'producer',out/'release',out/'GLOBAL.json'],mode+'-numerical')
        call(python+[HERE/'corruptions.py',out/'producer',out/'release',out/'GLOBAL.json',out/(mode+'-corruptions')],mode+'-corruptions')
        call(python+[HERE/'physical_controls.py',out/(mode+'-physical')],mode+'-physical')
        result=dict(local=json.loads((out/'producer/LOCAL.json').read_text()),global_bound=json.loads((out/'GLOBAL.json').read_text()),
            independent=json.loads((out/(mode+'-numerical.log')).read_text()),corruptions=json.loads((out/(mode+'-corruptions.log')).read_text()),
            physical=json.loads((out/(mode+'-physical/PHYSICAL.json')).read_text()))
        results.append(result)
    need(results[0]==results[1],'Python mode mismatch');need(results[0]['global_bound']['gate']=='PASS','declared gate failed')
    if not record:
        need(results[0]==json.loads((HERE/'EXPECTED.json').read_text()),'published expectation mismatch')
        for name in ('HISTOGRAM.tsv','PROFILE.tsv'):need((out/'producer'/name).read_bytes()==(HERE/name).read_bytes(),'public table mismatch')
        need((out/'normal-physical/FIXTURES.json').read_bytes()==(HERE/'FIXTURES.json').read_bytes(),'public fixture mismatch')
    (out/'RESULT.json').write_text(json.dumps(results[0],sort_keys=True,indent=2)+'\n')
    receipt=dict(status='RECORDED_THREE_BLOCK_GLOBAL_REDUCTION' if record else 'REPRODUCED_THREE_BLOCK_GLOBAL_REDUCTION',seconds=time.monotonic()-start,
        result_sha256=hashlib.sha256((out/'RESULT.json').read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),
        new_task_decisions=0,target_found=False,solver_calls=0,q10_child_inputs_inspected=0)
    (out/'REPLAY.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--record',action='store_true');a=p.parse_args()
    print(json.dumps(run(a.out,a.record),sort_keys=True))
