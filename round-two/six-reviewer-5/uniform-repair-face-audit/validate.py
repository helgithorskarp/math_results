"""Source-only independent audit; serial cold normal/-O, whole records, damages.

CPython 3.12; SymPy 1.14.0 generation; portable Fraction/integer checks.
No target program, saved mathematical stream, private ledger or network input.
"""
import argparse,datetime,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent
phases=[['lower_sectors.py'],['lower_signs.py'],['refine_lower.py'],['literal_check.py'],['bind_lower.py'],['check_polynomials.py'],
    ['stages.py','standard'],['stages.py','trivial'],['polynomial_cap.py','vectors'],['polynomial_cap.py','derivative'],['polynomial_cap.py','psi'],['polynomial_cap.py','short'],
    ['optimization.py'],['shift_signs.py'],['optimization_signs.py'],['inverse_sign_check.py','cap'],['inverse_sign_check.py','optimization'],['bind_cap.py'],['pell.py'],['pell_division_check.py'],['asymptotic_check.py']]
outputs=['lower-sectors.json','lower-signs.json','lower-refinement.json','literal-original.json','lower-binding.json','polynomial-check.json','standard-stage.json','trivial-stage.json','cap-vector-polynomials.json','cap-derivative-polynomials.json','psi-polynomials.json','cap-short-polynomials.json','optimization-polynomials.json','cap-signs.json','optimization-signs.json','inverse-cap-result.json','inverse-optimization-result.json','cap-binding.json','pell-result.json','pell-division-result.json','asymptotic-result.json']
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--campaign-state',type=pathlib.Path);args=parser.parse_args()
    source=sorted(P.glob('*.py'));source=[p for p in source if p.name!='validate.py'];work=P/'work';work.mkdir(exist_ok=True)
    env=dict(os.environ)
    for key in THREADS:env[key]='1'
    runs=[];primary=json.loads((P/'PRIMARY.json').read_text());all_sealed_outputs=primary['outputs']
    def child(cold,opts,program,expected=0,reason=None):
        if args.campaign_state:
            health=json.loads((args.campaign_state/'monitor/health.json').read_text())
            barriers=[p.name for p in args.campaign_state.iterdir() if 'paused' in p.name.lower() or 'handover' in p.name.lower()]
            if barriers or health['reasons'] or health['credit_budget']['status']!='authorized':raise RuntimeError('operations barrier')
        start=time.monotonic()
        try:r=subprocess.run([sys.executable,'-B',*opts,*program],cwd=cold,env=env,text=True,capture_output=True,timeout=45)
        except subprocess.TimeoutExpired as ex:raise RuntimeError('INCOMPLETE fixed45s child, not a mathematical conclusion') from ex
        rec=dict(mode=cold.name,program=program,optimized=bool(opts),returncode=r.returncode,seconds=time.monotonic()-start,
            stdout=r.stdout,stderr=r.stderr)
        runs.append(rec);print(cold.name,' '.join(program),r.returncode,round(rec['seconds'],4),flush=True)
        if r.returncode!=expected or reason is not None and reason not in r.stderr:raise RuntimeError(json.dumps(rec))
    try:
        for opts,mode in (([],'normal'),(['-O'],'optimized')):
            cold=work/mode;cold.mkdir(exist_ok=False)
            for path in source:shutil.copyfile(path,cold/path.name)
            for phase in phases:child(cold,opts,phase)
            for name in outputs:
                if sha(cold/name)!=all_sealed_outputs[name]['sha256'] or (cold/name).stat().st_size!=all_sealed_outputs[name]['bytes']:raise RuntimeError('entire sealed mathematical record differs '+name)
                if mode=='optimized' and (cold/name).read_bytes()!=(work/'normal'/name).read_bytes():raise RuntimeError('entire normal/O record differs '+name)
            for program,reason in [(['check_polynomials.py','--damage'],'ENTIRE coefficient identity F_strict_bound'),
                (['inverse_sign_check.py','cap','--damage'],'ENTIRE inverse coefficient identity psi_leading'),
                (['inverse_sign_check.py','optimization','--damage'],'ENTIRE inverse coefficient identity M_denominator'),
                (['pell_division_check.py','--damage'],'ALL independent Pell remainder coefficients'),
                (['bind_cap.py','--omit-standard'],'every ORIGINAL cap stationary row')]:child(cold,opts,program,1,reason)
            path=cold/'lower-sectors.json';old=path.read_bytes();data=json.loads(old);tau=data['tau']
            tau['right_derivative']='('+tau['right_derivative']+')+('+tau['alpha']+')*('+tau['shift']+')**2/q'
            path.write_text(json.dumps(data,indent=2)+'\n');child(cold,opts,['bind_lower.py'],1,'literal right derivative');path.write_bytes(old)
            for name in outputs:
                if sha(cold/name)!=all_sealed_outputs[name]['sha256']:raise RuntimeError('damage did not preserve complete record '+name)
        summary=dict(status='independent full source-only audit passed',actual_agent='six-reviewer-5',role='independent mathematical reviewer',
            positive_children=2*len(phases),damage_children=12,whole_normal_optimized_private_records=len(outputs),
            output_hashes={n:dict(bytes=(work/'normal'/n).stat().st_size,sha256=sha(work/'normal'/n)) for n in outputs},
            output_bytes=sum((work/'normal'/n).stat().st_size for n in outputs),
            maximum_child_seconds=max(r['seconds'] for r in runs),sum_child_seconds=sum(r['seconds'] for r in runs),
            peak_child_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,guard_seconds=45,native_threads=1,serial=True,
            solver_used=False,target_native_source_used=False,proof_formalized=False,
            semantic_damages=['F coefficient','cap coefficient','optimizer coefficient','Pell remainder','omitted complete standard component','omitted singular-gauge correction'])
        (work/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');(work/'RUNS.json').write_text(json.dumps(runs,indent=2)+'\n')
        print(json.dumps(summary,indent=2),flush=True)
    except BaseException as ex:
        (work/'INCOMPLETE.json').write_text(json.dumps(dict(status='incomplete; no verdict',error=str(ex),runs=runs),indent=2)+'\n');raise
if __name__=='__main__':main()
