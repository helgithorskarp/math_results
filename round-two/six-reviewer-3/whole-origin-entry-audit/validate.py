"""Full typed external record and independently consequential damage controls."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit import build,canonical,typed_equal,need

def check(candidate,expected):
    need(typed_equal(candidate,expected),'whole typed record differs')

def main():
    r=build();out={}
    changes=[('sector_last_omitted',lambda x:x['sectors']['full_sector_rows'].pop()),
             ('whole_sector_coefficient',lambda x:x['sectors']['full_sector_rows'][7]['whole_integrand_coefficients'].__setitem__(2,'0')),
             ('quadrature_weight',lambda x:x['sectors']['quadrature_weights'].__setitem__(0,'0')),
             ('hessian_budget',lambda x:x['margins']['strict_margins'].__setitem__('local_hessian_1_over_16','0')),
             ('bootstrap_third',lambda x:x['margins']['bootstrap_budgets'].__setitem__(2,'0')),
             ('fourth_Newton_term',lambda x:x['newton']['whole_majorants'][2].__setitem__('whole_majorant',{})),
             ('last_Newton_term',lambda x:x['newton']['whole_majorants'].pop()),
             ('direct_H59_relabel',lambda x:x['margins'].__setitem__('new_direct_H_budget','59')),
             ('Gaussian_hessian',lambda x:x['controls'][2]['all_ordered_second_derivatives'][1].__setitem__(2,{})),
             ('actual_feasibility_relabel',lambda x:x['controls'][5].__setitem__('abstract_only',False)),
             ('radial_face_8',lambda x:x['credited_owned_radial_faces'].pop()),
             ('false_variance_division',lambda x:x.__setitem__('zero_variance_division',True)),
             ('false_inverse_disk_transfer',lambda x:x.__setitem__('original_disk_assumed_on_normalized_tuple',True)),
             ('schema_bool_int',lambda x:x.__setitem__('schema',True))]
    for label,f in changes:
        candidate=copy.deepcopy(r);f(candidate)
        try:check(candidate,r)
        except ValueError:out[label]='rejected'
        else:raise ValueError('damage accepted '+label)
    for label,c in [('empty',{}),('list',[]),('null',None)]:
        try:check(c,r)
        except ValueError:out[label]='rejected'
        else:raise ValueError('malformed record accepted')
    pins={};root=Path(__file__).resolve().parent;env=os.environ.copy()
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    for name,old,new in [('audit.py',"F(1,65536)","F(1,32768)"),
                         ('polys.py',"n*v[0],n*v[1]","(n+1)*v[0],n*v[1]"),
                         ('radial.py',"F(39,5)","F(8)")]:
        text=(root/name).read_text();need(text.count(old)==1,'unique meaningful source damage')
        for mode in [[],['-O']]:
            with tempfile.TemporaryDirectory() as temp:
                t=Path(temp)
                files=[line.split('  ',1)[1] for line in (root/'CORE.sha256').read_text().splitlines()]+['CORE.sha256']
                for f in files:(t/f).write_bytes((root/f).read_bytes())
                (t/name).write_text(text.replace(old,new))
                run=subprocess.run([sys.executable,'-I','-B',*mode,str(t/'audit.py')],capture_output=True,text=True,env=env,timeout=45)
                need(run.returncode!=0,'source damage accepted')
                pins[name+(' optimized' if mode else ' normal')]='rejected'
    print(json.dumps({'whole_record_sha256':hashlib.sha256(canonical(r)).hexdigest(),
                     'external_typed_damages':out,'meaningful_source_damages':pins,
                     'mathematical_budget_failures':r['damaged_mathematical_budgets']},sort_keys=True))

if __name__=='__main__':main()
