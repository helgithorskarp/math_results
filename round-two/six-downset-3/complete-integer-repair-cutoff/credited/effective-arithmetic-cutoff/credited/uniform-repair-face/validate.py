"""Serial isolated normal/-O verification; bulky records remain in ignored work."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,resource,subprocess,sys,time
BASE=Path(__file__).resolve().parent
NATIVE=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
        'VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
PHASES=(('zero-bind','zero_check.py',('bind',)),('zero-controls','zero_check.py',('controls',)),
        ('zero-damage','zero_check.py',('damage',)),
        *((('zero-'+name),'zero_signs.py',(name,)) for name in
          ('H00','H_determinant','vertex_positive','vertex_below_lower_right','compact_joint_gcd','asymptotic')),
        ('zero-recovery10020','zero_recover.py',()),
        ('binding','binding.py',()),('nu','lower.py',('nu',)),('tau','lower.py',('tau',)),
        ('boundary','lower.py',('boundary',)),('bound','lower.py',('bound',)),
        ('cap-controls','cap_controls.py',()),('cap-vectors','cap_fields.py',()),
        ('cap-field','cap_slope.py',('field',)),('cap-signs','cap_slope.py',('signs',)),
        ('joint-dual','dual.py',()),('asymptotic','asymptotic.py',()),('pell','asymptotic.py',('pell',)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=BASE/'work')
    args=ap.parse_args();work=args.work.resolve();work.mkdir(parents=True,exist_ok=True)
    import bundle
    source=bundle.check_bundle(BASE)
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    for name in NATIVE:env[name]='1'
    receipt={'actual_agent':'six-downset-3','role':'researcher','UTC':datetime.now(timezone.utc).isoformat(),
             'source_gate':source,'native_threads':1,'one_serial_intensive_child':True,
             'timeout_per_child_seconds':60,'children':[],'completed':False}
    records={}
    for phase,script,arguments in PHASES:
        campaign=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
        if campaign and any((Path(campaign)/name).exists() for name in ('PAUSED.json','HANDOVER.json')):
            raise RuntimeError('operations pause/handover barrier; retain partial receipt')
        both=[]
        for mode,flags in (('normal',[]),('optimized',['-O'])):
            out=work/(phase+'-'+mode+'.json')
            bootstrap=('import runpy,sys\n'
                       'sys.path.insert(0,sys.argv.pop(1))\n'
                       'sys.argv=sys.argv[1:]\n'
                       'runpy.run_path(sys.argv[0],run_name="__main__")\n'
                       'if any(n=="sympy" or n.startswith("sympy.") for n in sys.modules):\n'
                       '    raise RuntimeError("CAS imported in mathematical checker")\n')
            command=[sys.executable,'-I',*flags,'-B','-c',bootstrap,str(BASE),str(BASE/script),*arguments,'--out',str(out)]
            start=time.monotonic();item={'phase':phase,'mode':mode,'command':command}
            try:
                child=subprocess.run(command,cwd=BASE,env=env,capture_output=True,text=True,timeout=60)
                item.update(exit_code=child.returncode,stdout=child.stdout,stderr=child.stderr,
                            completed=child.returncode==0)
            except subprocess.TimeoutExpired:
                item.update(completed=False,timeout=True,no_mathematical_absence_inference=True)
            item.update(seconds=time.monotonic()-start,
                        peak_children_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            receipt['children'].append(item)
            (work/'VALIDATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
            if not item['completed']:raise ValueError('incomplete operational check, no absence inference: '+phase+' '+mode)
            both.append(json.loads(out.read_text()))
            print(phase+' '+mode+' complete '+format(item['seconds'],'.3f')+'s',flush=True)
        if both[0]!=both[1]:raise ValueError('entire normal/-O records differ: '+phase)
        records[phase]=both[0]
    for name in ('H00','H_determinant','vertex_positive','vertex_below_lower_right','compact_joint_gcd'):
        if not records['zero-'+name]['sign']['completed_positive_certificate']:
            raise ValueError('missing whole zero-endpoint sign: '+name)
    for phase,key in (('nu','strict_negative_derivative_proved'),('tau','strict_positive_derivative_proved')):
        if not records[phase]['signs']['4'][key]:raise ValueError('missing derivative sign: '+phase)
    if not records['boundary']['boundary_strict_negative_proved'] or not records['bound']['lower_derivative_less_than_minus_one_over_2q4_proved']:
        raise ValueError('missing quantitative lower derivative inequality')
    if not all(records['cap-signs']['whole_signs'][key]['strict_positive_proved'] for key in ('leading00','determinant2')):
        raise ValueError('missing complete conservative cap slope certificate')
    if len(records['joint-dual']['all_eight_semantic_damage_probes'])!=8:
        raise ValueError('incomplete original-dual damage coverage')
    if not records['asymptotic']['global_asymptotic_absence_bridge_available']:
        raise ValueError('missing complete homogeneous quotient and denominator signs')
    if not all(records['pell'][key]['all_k_ge48_original_residual_goal_sign_proved']
               for key in ('negative_frontier','positive_adjacent_frontier')):
        raise ValueError('incomplete all-members adjacent Pell signs')
    payload=json.dumps(records,indent=2,sort_keys=True)+'\n'
    expected=BASE/'EXPECTED.json'
    if expected.exists():
        pinned=json.loads(expected.read_text())
        if pinned['whole_math_SHA256']!=hashlib.sha256(payload.encode()).hexdigest() or pinned['whole_math_bytes']!=len(payload.encode()):
            raise ValueError('complete mathematical output differs from compact expected record')
    (work/'RESULT.json').write_text(payload)
    receipt.update(completed=True,complete_phase_count=len(PHASES),
                   entire_normal_optimized_records_equal=True,no_CAS_import_in_math_children=True,
                   whole_math_bytes=len(payload.encode()),whole_math_SHA256=hashlib.sha256(payload.encode()).hexdigest(),
                   ordinary_bridges_unformalized=True,independent_review=False)
    (work/'VALIDATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({key:value for key,value in receipt.items() if key!='children'}),flush=True)

if __name__=='__main__':main()
