"""Replay the exact frozen proof, controls, and optional fresh LP proposals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import check_all
import controls
import verify

HERE=Path(__file__).absolute().parent


def fresh_guides(work):
    """Every LP domain comes from the separately checked frozen predecessor chain.

    This validates regenerated numerical proposals as exact certificates on
    those domains. Pure fresh chains are not claimed when rounded screens
    differ. The complete frozen route remains the primary reproducible proof.
    """
    import highspy
    import numpy
    verify.need(highspy.Highs().version()=='1.11.0' and numpy.__version__=='2.2.6', 'Pinned optional numerical versions')
    manifest=json.loads((HERE/'manifest.json').read_text());work.mkdir(parents=True,exist_ok=True)
    rows=[]
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    for case in manifest['cases']:
        tree=HERE/case['zero_tree'] if case['zero_tree'] else None
        colors,V,_=verify.base_premise(HERE/case['base'],tree)
        cover=json.loads((HERE/case['cover']).read_text())
        for chain in cover['chains']:
            vertices=set(V[1])
            for fn in chain['certificates']:
                original=(HERE/fn).read_bytes();frozen=json.loads(original)
                checked=verify.check_stage(frozen,colors,vertices,case['phase'],chain['root'])
                plan=manifest['proposals'][fn]
                verify.need(plan['phase']==case['phase'] and plan['root']==chain['root'] and
                            plan['denominator']==frozen['denominator'], 'Numerical plan agrees with actual frozen stage')
                path=work/Path(fn).name;domain=path.with_suffix('.domain.json');guide=path.with_suffix('.guide.json')
                domain.write_text(json.dumps({'permitted_screen':sorted(vertices)})+'\n')
                cmd=[sys.executable]
                if sys.flags.optimize:cmd.append('-'+'O'*sys.flags.optimize)
                cmd += [str(HERE/'generate.py'),'--phase',str(case['phase']),'--root',str(chain['root']),
                        '--domain',str(domain),'--plans',str(HERE/'plans.json'),'--output',str(path),
                        '--summary',str(guide),'--denominator',str(plan['denominator'])]
                if plan['trial_opposite'] is not None:
                    verify.need(type(plan['trial_opposite']) is int and plan['trial_opposite'] in vertices,
                                'A numerical trial point belongs to the full proved domain')
                    cmd += ['--trial-opposite',str(plan['trial_opposite'])]
                subprocess.run(cmd,check=True,env=env,stdout=subprocess.DEVNULL)
                g=json.loads(guide.read_text())
                verify.need(g.get('direct_empty_petal') or g['solver_status']=='Optimal',
                            'Incomplete guide: pause expensive work, no mathematical exclusion')
                new=verify.check_stage(json.loads(path.read_text()),colors,vertices,case['phase'],chain['root'])
                verify.need(not checked['exclusion'] or new['exclusion'], 'Fresh final guide checked as a strict exact exclusion')
                rows.append({'phase':case['phase'],'root':chain['root'],'stage':fn,
                             'exact_fresh_certificate_valid':True,'fresh_exclusion':new['exclusion'],
                             'frozen_exclusion':checked['exclusion'],'fresh_gap_numerator':new.get('gap_to_cap_numerator'),
                             'recovers_frozen_next_screen':set(new['next_domain'])<=set(checked['next_domain']),
                             'certificate_bytes_match':path.read_bytes()==original,
                             'native_status':g.get('solver_status'),'native_seconds':g.get('seconds'),
                             'native_peak_rss_kib':g.get('peak_rss_kib')})
                vertices=set(checked['next_domain'])
                print(json.dumps({'fresh_stage':len(rows),'phase':case['phase'],'root':chain['root'],
                                  'valid':True,'gap':new.get('gap_to_cap_numerator')}),flush=True)
    return {'versions':{'highspy':'1.11.0','numpy':'2.2.6'},'stages':rows,
            'fresh_stages_exactly_checked':len(rows),'fresh_final_exclusions':sum(r['frozen_exclusion'] and r['fresh_exclusion'] for r in rows),
            'all_guides_checked_on_independently_proved_frozen_domains':True,
            'all_fresh_screens_recover_frozen':all(r['recovers_frozen_next_screen'] for r in rows),
            'pure_fresh_chain_claim':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--fresh',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
    start=time.monotonic();a.work.mkdir(parents=True,exist_ok=True)
    out=check_all.compact(check_all.replay())
    expected=(HERE/'expected.json').read_bytes()
    verify.need(out==json.loads(expected), 'Complete compact frozen expected result')
    checked_controls=controls.run(a.work/'controls')
    report={'success':True,'agent':'six-vdw-3','role':'researcher','python_version':platform.python_version(),
            'python_optimization':sys.flags.optimize,'expected_sha256':hashlib.sha256(expected).hexdigest(),
            'coverage_counts':out['uniform']['coverage_counts'],'new_root_cases':out['uniform']['new_root_cases'],
            'new_packing_stages':out['uniform']['new_packing_stages'],
            'minimum_total_nonpole_edits':out['uniform']['minimum_total_nonpole_edits'],'controls':checked_controls,
            'default_numerical_dependencies':False,'imported_old_proofs_replayed':False}
    if a.fresh:report['fresh']=fresh_guides(a.work/'fresh')
    report.update(elapsed_seconds=time.monotonic()-start,self_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    if a.output:a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('controls','fresh')}))


if __name__=='__main__':main()
