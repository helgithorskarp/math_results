"""POST-SEAL data-only correspondence; no producer calls in independent core.
Reproduce with a separate byte-pinned author source directory as argv1.
"""
from pathlib import Path
from fractions import Fraction as F
import os,json,hashlib,subprocess,sys,time
from audit import build,canonical,cyclic
from polys import Poly,symbol,cast,need
HERE=Path(__file__).resolve().parent
EXPORT='''import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import verify,arithmetic
captured=[];original=arithmetic.identity
def capture(rows,name,left,right):
 original(rows,name,left,right)
 captured.append({'name':name,'lhs':arithmetic.encoded(left),'rhs':arithmetic.encoded(right)})
arithmetic.identity=capture;verify.identity=capture
record=verify.build_record()
print(json.dumps({'record':record,'captured':captured},sort_keys=True))
'''
def from_record(p):
    terms={}
    for mono,val in p.items():
        key=() if mono=='1' else tuple((a.split('^')[0],int(a.split('^')[1]) if '^' in a else 1) for a in mono.split('*'))
        terms[key]=(F(val[0]),F(val[1]))
    return Poly(terms)
def from_native(p,names):
    out=cast(0)
    for exponents,value in p:
        term=cast(F(value))
        for j,n in enumerate(exponents):
            if n:
                need(j<len(names),'unknown occupied native variable');term*=names[j]**n
        out+=term
    return out

def main():
    if len(sys.argv)!=2:raise ValueError('supply separate byte-pinned native source directory')
    source=Path(sys.argv[1]).resolve();pins=json.loads((HERE/'NATIVE_PINS.json').read_text());seal=json.loads((HERE/'SEAL.json').read_text())
    for name,pin in pins['files'].items():need(hashlib.sha256((source/name).read_bytes()).hexdigest()==pin['sha256'],'preimport native pin '+name)
    for name,digest in seal['files'].items():need(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,'sealed file changed '+name)
    env=dict(os.environ)
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
    args=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])+['-c',EXPORT,str(source)]
    child=subprocess.run(args,capture_output=True,text=True,env=env,timeout=45)
    need(child.returncode==0,'native export failed '+child.stderr)
    data=json.loads(child.stdout);record=data['record'];wanted=json.loads((source/'EXPECTED.json').read_text())
    need(canonical(record)==canonical(wanted),'entire native typed record differs')
    need(hashlib.sha256(canonical(record)).hexdigest()=='8aa72365968645d14796f25a0b02dd72bb81e268ca28ab4cbc2d944a8618ed57','native record hash')
    fresh=build();need(hashlib.sha256(canonical(fresh)).hexdigest()==json.loads((HERE/'SUMMARY.json').read_text())['record_sha256'],'sealed independent core differs')
    maps={x['name']:x for x in data['captured']}
    names=[symbol('x'+str(j)) for j in range(8)]+[symbol('y'+str(j)) for j in range(8)]+[symbol('A'),symbol('B')]
    pairs=[('whole centered quadratic feedback mean','quadratic_sum',names),('whole retained quartic feedback expansion','quadratic_square_sum',names),('whole8 squared-coordinate variance identity','scalar_fourth_variance',names),('whole retained variance kernel and three nonnegative remainders','full_variance_remainder',names),('whole physical positive determinant completion','physical_completion',[symbol('E'),symbol('V')]),('whole objective positive determinant completion','objective_completion',[symbol('E'),symbol('V')]),('whole paired signed cubic combined BEFORE absolute values','combined_signed_cube',[symbol('x'),symbol('y'),symbol('t')**-4,symbol('t')**-1,symbol('w')])]
    compared=[];coefficients=0
    for native,own,variables in pairs:
        for side in ['lhs','rhs']:
            l=from_native(maps[native][side],variables);r=from_record(fresh['symbolic_maps'][own][side])
            need(l==r,'entire corresponding map '+native+'/'+side);coefficients+=len(l.terms)
        compared.append(native)
    free=[symbol('x'+str(j)) for j in range(7)]+[symbol('y'+str(j)) for j in range(7)]
    eliminated={'x7':-sum(free[:7]),'y7':-sum(free[7:])}
    own=from_record(fresh['symbolic_maps']['free_quartic_with_mean_correction']['lhs']).substitute(eliminated)
    native='whole complex zero-sum quartic SOS credited9845'
    for side in ['lhs','rhs']:
        l=from_native(maps[native][side],free);need(l==own,'whole eliminated quartic correspondence');coefficients+=len(l.terms)
    compared.append(native)
    # Compare full original certificate scalars and both routes, not rounded summaries.
    b=record['budgets'];p=fresh['records']['parameters']
    for nk,ok in [('eta_endpoint','e'),('local_radius_floor','a_star'),('V_endpoint','v'),('beta_cap','beta_upper'),('G','G'),('k','k'),('q','q')]:need(b[nk]==p[ok],'native scalar '+nk)
    for row in b['routes']:
        own=fresh['records']['absorption_certificates'][row['name']]
        for nk,ok in [('delta','delta'),('lambda','lambda'),('a0','a0'),('b0','b0'),('determinant','det')]:need(row[nk]==own[ok],'entire route '+nk)
        need(F(row['V_fourth_square_remainder'])==F(own['det'])/F(own['a0']),'full fourth coefficient')
        need(b['complete_'+row['name']+'_cost']==own['cost'],'entire cost')
        need(b[row['name']+'_error']==own['error'],'separate error')
    need(b['Cramer_endpoint_equalities']=={'determinant':'651/256','B4':'31/128'},'Cramer equalities')
    phase=record['whole_signed_and_dual_maps'][1]['rows']
    for row in phase:need(row['all6_field_coefficients']==fresh['records']['nine_paired_cube_coefficients'][row['phase']],'entire native phase')
    for j,constant in [(2,'8'),(3,'7'),(5,'1'),(6,'1')]:need(record['whole_signed_and_dual_maps'][j]['all6_field_coefficients']==[constant]+['0']*5,'entire native dual/profile field')
    # Native C is checked in our independent cyclotomic multiplication, no inversion.
    c=cyclic([(4,-F(1,2)),(5,-F(1,2))]);one=[F(1)]+[F(0)]*5;den=[one[j]+c[j] for j in range(6)]
    C=list(map(F,record['whole_signed_and_dual_maps'][4]['all6_field_coefficients']))
    product=cyclic([(i+j,x*y) for i,x in enumerate(den) for j,y in enumerate(C)])
    need(product==[F(8,3)*v+(F(1,3) if i==0 else 0) for i,v in enumerate(den)],'entire native slope field')
    # Every producer Gaussian control scalar recomputed from its complete data.
    for row in record['complete_arbitrary_critical_controls']:
        z=[tuple(map(F,q)) for q in row['complete_critical_multiset']];need(len(z)==8 and sum(q[0] for q in z)==sum(q[1] for q in z)==0,'native control multiplicity/center')
        E=sum(x*x for x,y in z);V=E+sum(y*y for x,y in z);A=F(row['A']);B=F(row['beta']);f=[A*x*x-B*y*y for x,y in z];bar=sum(f)/8;R=sum(x*q for (x,y),q in zip(z,f));var=sum((q-bar)**2 for q in f)
        vals={'E':E,'V':V,'R':R,'centered_f_variance':var,'retained_variance_kernel':F(3,4)*B*B*V*V+B*(A+B)*E*(V-E)/4,'S4':sum((x*x+y*y)**2 for x,y in z)}
        for name,v in vals.items():need(row[name]==str(v),'whole native literal control '+name)
        need(row['original_disk_feasibility_or_objective_cut_asserted'] is False,'controls assert no feasibility')
    result={'status':'PASS','independent_core_unchanged':True,'entire_native_record_replayed':True,'native_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),'corresponding_whole_maps':compared,'full_lhs_and_rhs_entries_compared':coefficients,'all5_native_control_scalars_rebuilt':True,'all4_paired_phase_rows_equal':True,'all5_dual_profile_field_rows_equal':True,'both_full_certificate_scalars_equal':True,'all8_pre_native_sealed_files_unchanged':True,'scope':'8 raw polynomial correspondences; remainder of native25/8 map record is replay evidence, not blanket independent map equality'}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
