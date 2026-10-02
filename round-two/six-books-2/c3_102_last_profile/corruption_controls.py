"""Intended semantic negatives, including real empty-case and normalization faults."""
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
import json,os,resource,shutil,subprocess,sys,time
from candidate_run import compare_streams,verify_record,validate_replay,canonical

def main():
    p=ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    args=p.parse_args();root=Path(__file__).resolve().parent;source=args.source_work.resolve();work=args.work.resolve()
    if work.exists() and any(work.iterdir()):
        raise ValueError('Fresh control directory required')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();controls=[]
    python=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',
             VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    def guard():
        if time.monotonic()-start>25:
            raise RuntimeError('INCOMPLETE corruption-control guard; no verdict')
    def child(name,command,message=None):
        guard();remaining=25-(time.monotonic()-start)
        result=subprocess.run(list(map(str,command)),env=env,capture_output=True,text=True,timeout=min(30,remaining))
        (work/(name+'.stdout')).write_text(result.stdout);(work/(name+'.stderr')).write_text(result.stderr)
        if message is None:
            if result.returncode:
                raise ValueError('Control preparation/positive failure '+name)
        elif not result.returncode or not result.stderr.strip().splitlines()[-1].endswith(message) or 'INCOMPLETE' in result.stderr:
            raise ValueError('Intended semantic rejection not reached '+name)
        guard()
    def rejected(name,command,message,**details):
        child(name,command,message);controls.append(dict(name=name,rejected=True,intended_check=message,**details))
    def clone(name,case,files):
        directory=work/name;directory.mkdir()
        for f in files:
            shutil.copyfile(source/case/f,directory/f)
        return directory
    def mutate(path,fn):
        value=json.loads(path.read_text());fn(value);path.write_text(canonical(value))
    def in_memory(name,fn,message):
        try:
            fn()
        except ValueError as exc:
            if str(exc)!=message:
                raise ValueError('Wrong control rejection '+name) from exc
        else:
            raise ValueError('Damage accepted '+name)
        controls.append(dict(name=name,rejected=True,intended_check=message));guard()

    for name,fn in [
        ('missing_root_placement',lambda v:v['placements'].pop(0)),
        ('wrong_root_deficit',lambda v:v['placements'][0].__setitem__('root_deficit',v['placements'][0]['root_deficit']+1)),
    ]:
        directory=clone(name,'root-cuts',['root-capacity.json']);mutate(directory/'root-capacity.json',fn)
        rejected(name,python+[root/'capacity_audit.py','--work',directory],'ENTIRE typed root/capacity/column table differs')
    for name,fn,message in [
        ('missing_A_word',lambda v:v['records'].pop(),'ENTIRE independent A word set differs'),
        ('wrong_A_global_degree',lambda v:v['records'][0]['row_sums'].__setitem__(0,v['records'][0]['row_sums'][0]+1),'Entire projection record fields differ'),
        ('wrong_A_pair_capacity',lambda v:v['records'][0]['pair_bounds'].__setitem__(0,v['records'][0]['pair_bounds'][0]+1),'Entire projection record fields differ'),
    ]:
        directory=clone(name,'P2_81010',['projection.json']);mutate(directory/'projection.json',fn)
        rejected(name,python+[root/'projection_audit.py','--work',directory,'--mode','P2_81010'],message)
    files=['projection.json','incidence-records.json','frames.json','frames.txt']
    directory=clone('wrong_J_degree_sort','P2_8910_J',['projection.json'])
    original=(root/'marked_incidences.py').read_text()
    before="marks=list(zip(C['B'],C['alpha']))"
    if original.count(before)!=1:
        raise ValueError('Unique actual incidence marking mutation required')
    shutil.copyfile(root/'cases.py',directory/'cases.py')
    (directory/'mutant.py').write_text(original.replace(before,"marks=list(C['alpha'])"))
    child('wrong_J_degree_sort-produce',python+[directory/'mutant.py','--work',directory,'--case','P2_8910_J'])
    if json.loads((directory/'frames.json').read_text()) or json.loads((source/'P2_8910_J/frames.json').read_text()):
        raise ValueError('The actual degree-sorting control must retain the empty-frame boundary')
    rejected('wrong_J_degree_sort',python+[root/'marked_incidence_audit.py','--work',directory,'--case','P2_8910_J'],
             'Whole marked incidence count/margin/capacity fields differ',rank3_global_degrees=[8,10],both_original_and_damaged_frame_sets_empty=True)
    directory=clone('wrong_column_weight','P2_8910',files)
    mutate(directory/'incidence-records.json',lambda v:v['column_types']['4'][0]['weights'].__setitem__(0,v['column_types']['4'][0]['weights'][0]+1))
    rejected('wrong_column_weight',python+[root/'marked_incidence_audit.py','--work',directory,'--case','P2_8910'],
             'Entire independent marked column domain differs')

    frames=(source/'P2_81010/frames.txt').read_text().splitlines();size=len(frames)
    directory=work/'wrong_native_degree';directory.mkdir();fields=list(map(int,frames[0].split()));fields[1]^=1
    (directory/'frames.txt').write_text('\n'.join([' '.join(map(str,fields))]+frames[1:])+'\n')
    rejected('wrong_native_degree',[source/'direct',directory/'frames.txt',directory,'P2_81010',size],'marked A global degree')
    directory=work/'missing_native_frame';directory.mkdir();(directory/'frames.txt').write_text('\n'.join(frames[:-1])+'\n')
    rejected('missing_native_frame',[source/'direct',directory/'frames.txt',directory,'P2_81010',size],'complete marked frame prerequisite')
    for stem in ['K-words','outcomes']:
        directory=work/('wrong_'+stem);directory.mkdir();old=(source/'P2_8910'/('cached-'+stem+'.txt')).read_bytes();damaged=bytearray(old)
        damaged[0]=ord('1') if stem=='outcomes' else (ord('9') if old[0]!=ord('9') else ord('8'))
        if bytes(damaged)==old:
            raise ValueError('Stream damage must alter a byte')
        (directory/'damaged.txt').write_bytes(damaged)
        in_memory('wrong_'+stem,lambda directory=directory,stem=stem:compare_streams('P2_8910',stem,directory/'damaged.txt',source/'P2_8910'/('direct-'+stem+'.txt')),
                  'Entire P2_8910 '+stem+' streams differ')
    record=json.loads((source/'PRE-CONTROLS.json').read_text());validate_replay(record);verify_record(record,deepcopy(record))
    damaged=deepcopy(record);damaged['patterns'].pop('P2_8910')
    in_memory('missing_marked_case',lambda:validate_replay(damaged),'Entire marked case coverage')
    damaged=deepcopy(record);damaged['patterns']['P2_8910_J']['cached']['counts'].pop('completion_choices')
    in_memory('missing_empty_case_counter',lambda:validate_replay(damaged),'Missing exact completion counter')
    damaged=deepcopy(record);damaged['patterns']['P2_8910']['literal']['K_degree_words']=True
    in_memory('wrong_census_integer_type',lambda:validate_replay(damaged),'Typed exact census integer')
    damaged=deepcopy(record);damaged['root-capacity']['placements'][0]['root_deficit']=True
    in_memory('wrong_frozen_record_integer_type',lambda:verify_record(damaged,record),'Whole frozen mathematical record differs')
    damaged=deepcopy(record);damaged['patterns']['P2_81010']['literal']['B_orbits'][0]=10
    in_memory('wrong_literal_degree_marks',lambda:validate_replay(damaged),'Literal whole declared degree/column marks')

    damaged=deepcopy(record);damaged['ordinary-cut']['cases'].pop()
    in_memory('missing_ordinary_case',lambda:validate_replay(damaged),'Entire ordinary/search case partition')
    damaged=deepcopy(record);damaged['ordinary-cut']['weighted_load_lower']=84
    in_memory('wrong_ordinary_load_lower',lambda:validate_replay(damaged),'Exact ordinary summed-row gap')
    damaged=deepcopy(record);damaged['ordinary-cut']['gap']=True
    in_memory('wrong_ordinary_integer_type',lambda:validate_replay(damaged),'Typed ordinary cut integers')
    directory=work/'actual_missing_fifth_root_case';directory.mkdir()
    shutil.copyfile(root/'root_capacity.py',directory/'mutant.py')
    cases=(root/'cases.py').read_text()+"\nCASES.pop('P2_8910_J')\n"
    (directory/'cases.py').write_text(cases)
    rejected('actual_missing_fifth_root_case',python+[directory/'mutant.py','--work',directory/'output'],
             'Unexpected necessary marked root case: extend coverage before a claim')
    ordinary=(root/'ordinary_cut.py').read_text()
    before='row=gamma[a]+sum(c for pair,c in caps.items() if a in pair)'
    if ordinary.count(before)!=1:
        raise ValueError('Unique ordinary row mutation required')
    directory=work/'ordinary_missing_diagonal';directory.mkdir()
    (directory/'mutant.py').write_text(ordinary.replace(before,'row=sum(c for pair,c in caps.items() if a in pair)'))
    rejected('ordinary_missing_diagonal',python+[directory/'mutant.py','--work',directory/'output'],
             'Literal full upper Gram row, diagonal retained')
    audit=(root/'capacity_audit.py').read_text()
    for name,before,after,message in [
        ('doubled_capacity_edge_term','cap=8*DA-15*36+17*h-3*sum','cap=8*DA-15*36+34*h-3*sum','Independent complete residual marks differ'),
        ('missing_Gram_diagonal','actual=margins[u]+sum(cap','actual=sum(cap','Literal complete AA Gram-row identity differs'),
    ]:
        if audit.count(before)!=1:
            raise ValueError('Unique actual audit mutation required')
        directory=clone(name,'root-cuts',['root-capacity.json']);(directory/'mutant.py').write_text(audit.replace(before,after))
        rejected(name,python+[directory/'mutant.py','--work',directory],message)
    original=(root/'identity_controls.py').read_text()
    for name,before,after,message in [
        ('wrong_vertex_deficit_constant','symbolic=2*E-294+','symbolic=2*E-293+','Literal vertex deficit identity'),
        ('wrong_mixed_cut_parity','(mixed-(DA-9))%2','(mixed-(DA-8))%2','Literal mixed cut deficit parity'),
    ]:
        if original.count(before)!=1:
            raise ValueError('Unique actual identity mutation required')
        directory=work/name;directory.mkdir();shutil.copyfile(root/'primary21.rows',directory/'primary21.rows')
        (directory/'mutant.py').write_text(original.replace(before,after))
        rejected(name,python+[directory/'mutant.py','--work',directory/'output'],message)
    cpp=(root/'direct.cpp').read_text()
    for name,before,after,message in [
        ('wrong_red_page_threshold','if (pop(rows[u]&rows[v])>3) return 1;','if (pop(rows[u]&rows[v])>4) return 1;','red B4 page control'),
        ('wrong_blue_page_threshold','if (pop(bu&bv)>6) return 2;','if (pop(bu&bv)>7) return 2;','blue B7 page control'),
        ('wrong_native_profile','{"P2_81010",{8,10,10},{8,9,10,10},{3,4,5,5}}','{"P2_81010",{8,10,10},{9,9,10,10},{3,4,5,5}}','literal P2 marked profile'),
    ]:
        if cpp.count(before)!=1:
            raise ValueError('Unique actual native mutation required')
        directory=work/name;directory.mkdir();(directory/'mutant.cpp').write_text(cpp.replace(before,after))
        child(name+'-compile',['g++','-std=c++17','-O2',directory/'mutant.cpp','-o',directory/'mutant'])
        command=[directory/'mutant','--page-controls'] if name!='wrong_native_profile' else [directory/'mutant',source/'P2_81010/frames.txt',directory,'P2_81010',size]
        rejected(name,command,message)
    child('native-positive',[source/'direct','--fixture21',root/'primary21.rows'])
    child('native-negative-pages',[source/'direct','--page-controls'])
    controls.sort(key=lambda v:v['name'])
    result=dict(status='COMPLETE_SEMANTIC_DAMAGE_CONTROLS',damage_rejections=len(controls),controls=controls,
                positive_whole_record_accepted=True,positive_primary21_accepted=True,actual_red_B4_and_blue_B7_rejected=True,
                positive_empty_frame_case_explicit_zero_counters=True,
                trust='Actual intended same-author checks, including preserved normalization/schema faults; not external review or completeness formalization.')
    (work/'controls.json').write_text(canonical(result));guard()
    print(json.dumps(dict(record=result,seconds=time.monotonic()-start,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                         program_guard_seconds=25,child_guard_seconds=30),indent=2))

if __name__=='__main__':
    main()
