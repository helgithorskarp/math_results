"""Sequential exact products with fresh outputs, fixed20s guards and mode audit."""
from pins import verify_pins
verify_pins()
from pathlib import Path
from time import monotonic
import argparse,json,os,subprocess,sys
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from kernel import need
from check_cell import CELLS
HERE=Path(__file__).resolve().parent
RUNTIME={'seconds','peak_kib','optimized','python'}

def semantic(row):return {k:v for k,v in row.items() if k not in RUNTIME}

def main():
    p=argparse.ArgumentParser();p.add_argument('--optimized',action='store_true')
    p.add_argument('--compare',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    target=a.output_dir or HERE/'.generated'/('optimized' if a.optimized else 'normal')
    need(not target.exists(),'entire fresh output directory required; existing outputs are not executions')
    target.mkdir(parents=True);jobs=[];compared=[]
    def run(script,args,output,category,cell=None,part=None,layer=None):
        before=verify_pins();need(not output.exists(),'fresh exact child output required')
        cmd=[sys.executable,*(['-O'] if a.optimized else []),str(HERE/script),*args,'--output',str(output)]
        start=monotonic()
        try:r=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
        except subprocess.TimeoutExpired:
            jobs.append({'category':category,'cell':cell,'part':part,'layer':layer,'timeout':True,'complete':False})
            (target/'run-journal.json').write_text(json.dumps({'complete':False,'jobs':jobs},indent=2)+'\n')
            raise RuntimeError('exact child timed out; no mathematical nonexistence conclusion')
        job={'category':category,'cell':cell,'part':part,'layer':layer,'exit':r.returncode,
             'fresh_record_written':output.exists(),'wall_seconds':round(monotonic()-start,3),'guard_seconds':20}
        jobs.append(job);(target/'run-journal.json').write_text(json.dumps({'complete':False,'jobs':jobs},indent=2)+'\n')
        need(r.returncode==0 and output.exists(),'exact child failed: '+r.stderr[-1800:])
        need(before==verify_pins(),'input source changed through actual exact child')
        data=json.loads(output.read_text())
        if a.compare:
            old=json.loads((a.compare/output.name).read_text())
            need(semantic(data)==semantic(old),'every actual mathematical field/coefficient differs between modes')
            compared.append(output.name)
        print(r.stdout.strip(),flush=True)
        return data
    collar_paths=[]
    for layer in range(3):
        output=target/('collar'+str(layer)+'.json')
        run('check_collar.py',['--layer',str(layer)],output,'closed collar layer',layer=layer);collar_paths.append(output)
    cell_paths=[]
    for cell in CELLS:
        paths=[]
        for part in range(6):
            output=target/(cell+'-part'+str(part)+'.json')
            run('check_cell.py',['--cell',cell,'--part',str(part)],output,'closed18-root source product',cell=cell,part=part);paths.append(output)
        output=target/(cell+'-complete.json')
        run('assemble.py',['--cell',cell,'--inputs',*(str(x) for x in paths)],output,'whole closed cell assembly',cell=cell);cell_paths.append(output)
    run('join.py',['--cells',*(str(x) for x in cell_paths),'--collars',*(str(x) for x in collar_paths)],target/'complete.json','closed inner triangle join')
    result={'agent':'six-rupert-3','role':'researcher','complete':True,'optimized':a.optimized,
        'actual_guarded_children':len(jobs),'source_products':48,'closed_collar_layers':3,'cell_assemblies':8,
        'every_mathematical_field_compared':compared,'threads':1,'guard_seconds':20,'jobs':jobs,
        'input_pins':verify_pins(),'author_execution_evidence_not_independent_review':True}
    (target/'run-journal.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'complete':True,'children':len(jobs),'mode':'optimized' if a.optimized else 'normal','full_mathematical_records_compared':len(compared)}),flush=True)

if __name__=='__main__':main()
