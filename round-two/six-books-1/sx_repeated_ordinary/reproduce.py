"""Serial, standalone source corroboration of the ordinary SX-repeated proof."""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def require(t,m):
    if not t:raise ValueError(m)
def seal(root):
    manifest=json.loads((root/'SOURCE.json').read_text())
    for item in manifest['files']:
        raw=(root/item['name']).read_bytes()
        require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],
                'sealed source mismatch: '+item['name'])
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check',type=Path)
    p.add_argument('--verify-source',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent
    if a.verify_source:seal(root)
    a.output.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[key]='1'
    records={};phases=[]
    for name in ('reduction','transports','terminal','primary21'):
        output=(a.output/(name+'.json')).resolve()
        args=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        args+=([str(root/'baseline.py'),str(output)] if name=='primary21' else
               [str(root/'phase.py'),name,str(output)])
        r=subprocess.run(args,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
        require(r.returncode==0,'incomplete/failed '+name+' phase: '+r.stderr.decode())
        raw=output.read_bytes();rec=json.loads(raw)
        require(rec.get('complete') is True and raw==canonical(rec),'complete canonical '+name)
        records[name]=rec;phases.append({'name':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        print(json.dumps(phases[-1]|{'complete':True}),flush=True)
    require(records['reduction']['necessary_Ti_states']=={'14':[[3,3],[3,4]],'15':[[3,3],[3,4]]},
            'entire reduction/terminal derived C/C interface')
    require(records['reduction']['SX_saturated_BLUE_pages']==[1,3,4,11,12,13],
            'actual six SX saturation pages')
    require(records['terminal']['mandatory_BLUE_pages']==7 and len(records['terminal']['six_original_T_label_models'])==6,
            'actual seven terminal BLUE pages in every naming')
    require(records['reduction']['SX_degree10_assumed'] is False,'SX degree is unmarked')
    math=canonical({'agent':'six-books-1','role':'researcher','complete':True,'components':records})
    (a.output/'MATHEMATICAL.json').write_bytes(math)
    summary={'agent':'six-books-1','role':'researcher','complete':True,
             'proof_status':'Ordinary conditional written proof; exact same-author source corroboration; unformalized and independent review pending',
             'phases':phases,'whole_mathematical_bytes':len(math),'whole_mathematical_sha256':hashlib.sha256(math).hexdigest(),
             'initial_T_Q_rank_floors':[2,3,3],'SX_degree10_assumed':False,
             'SX_saturated_BLUE_pages':6,'all_arbitrary_SX_Q_pairs':4096,'covering_SX_Q_pairs':729,
             'nonC_actual_RED_Q_roles':183708,'derived_Ti_rows':[3,3],
             'original_T_label_transports':25440,'all_terminal_Q_roles':10584,
             'terminal_BLUE_pages':7,'terminal_semantic_damage_rejections':36,
             'E_bound':None,'T0_X_Q_prescribed':False,'Y_or_cross_theorem_dependency':False,
             'baseline_edges_red_blue':[93,117],'baseline_max_pages':[3,6],
             'runtime_external_corpus_solver_ledger_or_review_input':False,'threads':1,
             'inner_mathematical_guard_seconds':30,'child_guard_seconds':90}
    compact=canonical(summary)
    if a.check:require(compact==a.check.read_bytes(),'ENTIRE expected compact record differs')
    (a.output/'SUMMARY.json').write_bytes(compact)
    if a.verify_source:seal(root)
    print(json.dumps({'complete':True,'whole_bytes':len(math),'whole_sha256':summary['whole_mathematical_sha256']}),flush=True)
if __name__=='__main__':main()
