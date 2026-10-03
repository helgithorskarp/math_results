"""Late exposed native corroboration of the original target only."""
import argparse,hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path
from fractions import Fraction as Q
from check import need


def run(native):
    here=Path(__file__).resolve().parent;provenance=json.loads((here/'PROVENANCE.json').read_text())
    for n,row in provenance['all6_target_file_whole_byte_pins'].items():
        b=(native/n).read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'whole native source pin '+n)
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[n]='1'
    rows=[]
    with tempfile.TemporaryDirectory(prefix='third-moment-native-')as tmp:
        def child(script,opt,options=()):
            t=time.monotonic();p=subprocess.run([sys.executable,'-B']+(['-O']if opt else [])+[str(script),*options],env=env,capture_output=True,timeout=45)
            need(p.returncode==0 and not p.stderr,'positive native corroboration child')
            rows.append(dict(script=script.name,optimized=opt,options=[x for x in options if not x.startswith(tmp)],seconds=round(time.monotonic()-t,6),returncode=p.returncode,cumulative_peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss));return p.stdout
        own=json.loads(child(here/'check.py',False));records=[]
        for opt in [False,True]:
            file=Path(tmp)/('native-'+str(opt)+'.json');child(native/'verify.py',opt,['--emit-record',str(file)]);records.append(file.read_bytes())
        need(records[0]==records[1]and json.loads(records[0])==json.loads(records[1]),'whole native normal/optimized records')
        actual=json.loads(records[0]);need(records[0]==(native/'expected.json').read_bytes(),'full native result and pinned expected bytes')
        need(len(actual['cases'])==len(own['all_six_minimum_cases'])==6,'all native/independent six cases')
        for a,b in zip(actual['cases'],own['all_six_minimum_cases']):
            need(all(a[k]==b[k]for k in ['n','m','k'])and a['interval']==b['closed_enclosing_interval']and a['cubic']==b['whole_polynomial'],'ALL native/independent case coefficients and intervals')
            need(a['middle']==[str(b['m']),str(-b['k'])],'whole original middle-level polynomial')
        v=list(map(Q,[1,1,1,-1,-1,-1,0,0]));eq=actual['equality'];need(eq['profile']==list(map(str,v))and eq['moments_1_to_6']==[str(sum(x**k for x in v))for k in range(1,7)],'full original equality moments')
        need(eq['original_polynomial']==own['equality_original_polynomial']and eq['ambient_characteristic']==own['equality_entire_ambient_characteristic'],'whole native/independent original and ambient polynomials')
        derivative=[str(i*Q(x)/8)for i,x in enumerate(own['equality_original_polynomial'])if i]
        need(eq['critical_polynomial']==derivative and eq['ambient_H']==own['all_six_original_trace_controls'][1]['whole_compression'],'entire actual derivative/compression bridge')
        need(len(eq['full_projectors'])==len(own['all_five_full_ambient_projectors'])==5,'all native projector groups')
        for a,b in zip(eq['full_projectors'],own['all_five_full_ambient_projectors']):
            need(a['eigenvalue']==b['eigenvalue']and Q(a['rank'])==Q(b['rank'])and a['matrix']==b['full_ambient_projector'],'ALL320 full projector entries/ranks/nodes')
            image=[str(sum(Q(x)*y for x,y in zip(row,v)))for row in b['full_ambient_projector']]
            need(a['image']==image and a['raw_full_mass']==b['unnormalized_full_mass']and a['normalized_full_mass']==b['normalized_mass'],'full projected images and grouped masses')
        need(all(eq[k]==own['equality_'+k]for k in ['X','eta','D','C']),'all normalized equality angular fields')
        need(actual['small_support']==[{'n':n,'cauchy_lower':str(Q(1,n))}for n in range(1,7)],'all small-support bounds')
        need(actual['angular']=={'level_bounds':[{'r':r,'upper':str(Q(24*(r-2),r-1))}for r in range(2,9)],'strict_universal_upper':'144/7','gap_to_49_over_2':str(Q(49,2)-Q(144,7))},'all original level bounds and optional benchmark comparison')
        for opt in [False,True]:
            result=json.loads(child(native/'verify.py',opt,['--self-test']))
            need(result['semantic_damages_rejected']==3 and result['record_sha256']==hashlib.sha256(records[0]).hexdigest(),'fresh native fixture and semantic checks')
    return dict(agent='six-reviewer-1',role='independent mathematical reviewer',native_role='late original-target corroboration; no centered-trace improvement imported',all6_native_source_pins_unchanged=True,all6_entire_case_polynomials_equal=True,all320_full_projector_entries_equal=True,all_complete_equality_and_level_fields_equal=True,native_record_bytes=len(records[0]),native_record_sha256=hashlib.sha256(records[0]).hexdigest(),entire_native_normal_optimized_bytes_equal=True,positive_children=5,native_internal_semantic_rejections=6,serial=True,native_threads=1,fixed_guard_seconds=45,rows=rows,total_child_seconds=round(sum(x['seconds']for x in rows),6),maximum_child_seconds=max(x['seconds']for x in rows))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.native.resolve()),indent=2,sort_keys=True))
