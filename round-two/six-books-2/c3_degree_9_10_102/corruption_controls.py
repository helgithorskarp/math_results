"""Semantic damage controls on real fresh domains, literal predicates and records."""
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
import hashlib,json,os,resource,shutil,subprocess,sys,time
from candidate_run import compare_streams,verify_record,validate_replay,canonical

def main():
    parser=ArgumentParser();parser.add_argument('--source-work',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
    root=Path(__file__).resolve().parent;source=args.source_work.resolve();work=args.work.resolve()
    if work.exists() and any(work.iterdir()):raise ValueError('Fresh control directory required')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();controls=[]
    python=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',
             VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    def guard():
        if time.monotonic()-start>25:raise RuntimeError('INCOMPLETE corruption-control guard; no verdict')
    def child(name,command,message=None):
        guard();remaining=25-(time.monotonic()-start)
        result=subprocess.run(list(map(str,command)),env=env,capture_output=True,text=True,timeout=remaining)
        (work/(name+'.stdout')).write_text(result.stdout);(work/(name+'.stderr')).write_text(result.stderr)
        if message is None:
            if result.returncode:raise ValueError('Control preparation/positive failure '+name)
        elif not result.returncode or message not in result.stderr or 'INCOMPLETE' in result.stderr:
            raise ValueError('Intended semantic rejection not reached: '+name)
        guard()
    def rejected(name,command,message,**details):
        child(name,command,message)
        controls.append(dict(name=name,rejected=True,intended_check=message,**details))
    def clone(name,mode,files):
        directory=work/name;directory.mkdir()
        for file in files:shutil.copyfile(source/mode/file,directory/file)
        return directory
    def change_json(path,fn):
        data=json.loads(path.read_text());fn(data);path.write_text(canonical(data))
    def in_memory(name,fn,message):
        try:fn()
        except ValueError as exc:
            if str(exc)!=message:raise ValueError('Wrong control rejection '+name) from exc
        else:raise ValueError('Damage accepted '+name)
        controls.append(dict(name=name,rejected=True,intended_check=message))
        guard()

    # Actual full4096-word projection auditor, including whole transport groups.
    for name,mutate,message in [
        ('missing_A_word',lambda d:d['records'].pop(),'ENTIRE independent A word set differs'),
        ('wrong_A_global_degree',lambda d:d['records'][0]['row_sums'].__setitem__(6,d['records'][0]['row_sums'][6]-1),'Entire projection record fields differ'),
        ('wrong_A_pair_capacity',lambda d:d['records'][0]['pair_bounds'].__setitem__(0,d['records'][0]['pair_bounds'][0]+1),'Entire projection record fields differ'),
    ]:
        directory=clone(name,'A9910',['projection.json']);change_json(directory/'projection.json',mutate)
        rejected(name,python+[root/'projection_audit.py','--work',directory,'--mode','A9910'],message)

    files=['incidence-records.json','frames.json','frames.txt']
    directory=clone('wrong_GM_degree_sort','GM',files)
    original=json.loads((directory/'incidence-records.json').read_text());removed=0
    for entry in original['results']:
        old=len(entry['records'])
        entry['records']=[r for r in entry['records'] if r['column_seeds'][1]<=r['column_seeds'][2]]
        removed+=old-len(entry['records'])
    if not removed:raise ValueError('Degree-distinct sorting damage did not alter actual GM domain')
    (directory/'incidence-records.json').write_text(canonical(original))
    rejected('wrong_GM_degree_sort',python+[root/'all9_incidence_audit.py','--work',directory,'--projection',source/'A999','--mode','GM'],
             'Entire all-nine incidence sets differ',removed_actual_records=removed,
             rank4_global_degrees=[9,10])

    directory=clone('wrong_column_weight','GM',files)
    change_json(directory/'incidence-records.json',lambda d:d['column_types']['4'][0]['weights'].__setitem__(0,d['column_types']['4'][0]['weights'][0]+1))
    rejected('wrong_column_weight',python+[root/'all9_incidence_audit.py','--work',directory,'--projection',source/'A999','--mode','GM'],
             'Entire literal column domains differ')

    frames=(source/'A9910/frames.txt').read_text().splitlines();size=len(frames)
    directory=work/'wrong_native_degree';directory.mkdir()
    fields=list(map(int,frames[0].split()));fields[1]^=1
    damaged=[' '.join(map(str,fields))]+frames[1:]
    (directory/'frames.txt').write_text('\n'.join(damaged)+'\n')
    rejected('wrong_native_degree',[source/'direct',directory/'frames.txt',directory,'A9910',size],'marked A global degree')
    directory=work/'missing_native_frame';directory.mkdir()
    (directory/'frames.txt').write_text('\n'.join(frames[:-1])+'\n')
    rejected('missing_native_frame',[source/'direct',directory/'frames.txt',directory,'A9910',size],'complete marked frame prerequisite')

    for stem in ['K-words','outcomes']:
        directory=work/('wrong_'+stem);directory.mkdir()
        original=(source/'G7'/('cached-'+stem+'.txt')).read_bytes()
        damaged=bytearray(original)
        damaged[0]=ord('1') if stem=='outcomes' else (ord('9') if original[0]!=ord('9') else ord('8'))
        if bytes(damaged)==original:raise ValueError('Stream damage must change a byte')
        (directory/'damaged.txt').write_bytes(damaged)
        in_memory('wrong_'+stem,lambda stem=stem,directory=directory:compare_streams('G7',stem,directory/'damaged.txt',source/'G7'/('direct-'+stem+'.txt')),
                  'Entire G7 '+stem+' streams differ')

    record=json.loads((source/'PRE-CONTROLS.json').read_text())
    validate_replay(record);verify_record(record,deepcopy(record))
    for name,mutate in [
        ('missing_root_placement',lambda d:d['analytic']['root_cuts'].pop()),
        ('wrong_ordinary_scalar_target',lambda d:d['low-profile']['mid_scalar_cases'][0].__setitem__('required_pair_common',4)),
        ('wrong_record_integer_type',lambda d:d['analytic'].__setitem__('degree_sum_matches',True)),
    ]:
        damaged=deepcopy(record);mutate(damaged)
        in_memory(name,lambda damaged=damaged:verify_record(damaged,record),'Whole frozen mathematical record differs')
    damaged=deepcopy(record);damaged['patterns'].pop('GM')
    in_memory('missing_marked_case',lambda:validate_replay(damaged),'Entire marked case coverage')

    # Mutate actual ordinary formula code in isolated copies; no changed public input.
    original=(root/'identity_controls.py').read_text()
    for name,before,after,message in [
        ('wrong_vertex_deficit_constant','symbolic=2*E-294+','symbolic=2*E-293+','Literal vertex deficit identity'),
        ('wrong_mixed_cut_parity','(mixed-(DA-9))%2','(mixed-(DA-8))%2','Literal mixed cut deficit parity'),
    ]:
        if original.count(before)!=1:raise ValueError('Unique formula mutation required')
        directory=work/name;directory.mkdir();shutil.copyfile(root/'primary21.rows',directory/'primary21.rows')
        (directory/'mutant.py').write_text(original.replace(before,after))
        rejected(name,python+[directory/'mutant.py','--work',directory/'output'],message)

    # The exact page predicate used on every literal host must reject actual B4/B7.
    cpp=(root/'direct.cpp').read_text()
    for name,before,after,message in [
        ('wrong_red_page_threshold','if (pop(rows[u]&rows[v])>3) return 1;','if (pop(rows[u]&rows[v])>4) return 1;','red B4 page control'),
        ('wrong_blue_page_threshold','if (pop(bu&bv)>6) return 2;','if (pop(bu&bv)>7) return 2;','blue B7 page control'),
    ]:
        if cpp.count(before)!=1:raise ValueError('Unique page mutation required')
        directory=work/name;directory.mkdir();(directory/'mutant.cpp').write_text(cpp.replace(before,after))
        child(name+'-compile',['g++','-std=c++17','-O2',directory/'mutant.cpp','-o',directory/'mutant'])
        rejected(name,[directory/'mutant','--page-controls'],message)
    child('native-positive',[source/'direct','--fixture21',root/'primary21.rows'])
    child('native-negative-pages',[source/'direct','--page-controls'])
    controls.sort(key=lambda r:r['name'])
    result=dict(status='COMPLETE_SEMANTIC_DAMAGE_CONTROLS',damage_rejections=len(controls),controls=controls,
                positive_whole_record_accepted=True,positive_primary21_accepted=True,
                actual_red_B4_and_blue_B7_rejected=True,
                trust='Actual same-author check paths; not independent review or proof of a missing completeness bridge.')
    (work/'controls.json').write_text(canonical(result));guard()
    print(json.dumps(dict(record=result,seconds=time.monotonic()-start,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                         program_guard_seconds=25,child_guard_seconds=30),indent=2))

if __name__=='__main__':main()
