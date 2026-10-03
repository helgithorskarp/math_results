"""Serial source-only corroboration of the ordinary SY-repeated proof."""
import argparse,hashlib,json,os,subprocess,sys
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
    a.output.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    records={};phases=[]
    for name in ('reduction','transports','terminal','primary21'):
        output=(a.output/(name+'.json')).resolve()
        cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        cmd+=([str(root/'baseline.py'),str(output)] if name=='primary21'
               else [str(root/'phase.py'),name,str(output)])
        r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
        require(r.returncode==0,'incomplete/failed '+name+' phase: '+r.stderr.decode())
        raw=output.read_bytes();record=json.loads(raw)
        require(record.get('complete') is True and raw==canonical(record),'complete canonical '+name)
        records[name]=record;phases.append({'name':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        print(json.dumps({'phase':name,'complete':True,'bytes':len(raw),'sha256':phases[-1]['sha256']}),flush=True)
    require(records['reduction']['T0_surviving_row_rank']==[[3,4]],'T0 C/rank4 interface')
    require(len(records['reduction']['initial_T_rank_triples'])==9,'all nine initial rank triples')
    require(records['reduction']['whole14_X_cores']==
            [z['T_X'][1:]+z['SY_X'] for z in records['terminal']['whole14_original16_models']],
            'entire reduction/terminal labelled row interface')
    require(records['terminal']['all18900_literal_bit_seven_BLUE_witnesses'][0]==18900,
            'entire original-page terminal interface')
    math=canonical({'agent':'six-books-1','role':'researcher','complete':True,'components':records})
    (a.output/'MATHEMATICAL.json').write_bytes(math)
    summary={'agent':'six-books-1','role':'researcher','complete':True,
             'proof_status':'Ordinary conditional written proof; exact same-author source corroboration; unformalized and independent review pending',
             'phases':phases,'whole_mathematical_bytes':len(math),'whole_mathematical_sha256':hashlib.sha256(math).hexdigest(),
             'initial_T_rank_triples':9,'derived_T_Q_ranks':[4,2,2],'whole_X_cores':14,
             'whole_original_T_label_transports':17280,'all_labelled_terminal_Q_roles':18900,
             'terminal_BLUE_pages':7,'terminal_semantic_damage_rejections':84,'density_terminal_dependency':False,
             'baseline_edges_red_blue':[93,117],'baseline_max_pages':[3,6],
             'runtime_external_census_solver_ledger_review_input':False,'threads':1,
             'inner_mathematical_guard_seconds':30,'child_guard_seconds':90}
    compact=canonical(summary)
    if a.check:require(compact==a.check.read_bytes(),'ENTIRE compact expected record differs')
    (a.output/'SUMMARY.json').write_bytes(compact)
    if a.verify_source:seal(root)
    print(json.dumps({'complete':True,'whole_bytes':len(math),'whole_sha256':summary['whole_mathematical_sha256']}),flush=True)
if __name__=='__main__':main()
