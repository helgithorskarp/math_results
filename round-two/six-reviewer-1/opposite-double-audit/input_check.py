"""Post-primary-seal check of the entire public target mathematical INPUT.
Fresh actual-ring companion mathematics verifies every embedded defining field.
No native author program or EXPECTED is inspected, imported or executed."""
from pathlib import Path
import sys,json,argparse,runpy,tempfile,hashlib,signal
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import *
def run(fixture,damage):
    here=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='opposite-input-')as temp:
        previous=sys.argv;sys.argv=[str(here/'actual.py'),'--record',str(Path(temp)/'actual.json')]
        try:own=runpy.run_path(str(here/'actual.py'))
        finally:sys.argv=previous
    q=json.loads(fixture.read_text())
    need(type(q)is dict and set(q)=={'actual_agent','inherited_defining_data','negative_bound','new_domain','positive_bound','positive_closed_b_cover','positive_v_upper','role','source_certificate_sha256','source_commit','whole_embedded_fields_canonical_sha256'},'entire target input root schema')
    need(q['actual_agent']=='six-sendov-2'and q['role']=='researcher','explicit author credit')
    need(q['source_commit']=='39ccb1eef4b190986e60a79154cbd07cef0ed671','inherited generic polynomial source pin')
    need(q['new_domain']=='QQ[s,lambda][z]; actual s>0,exacttwo opposite-sign doubles,four singles,4+4; equal-magnitude branch separate9416','complete new physical-domain and singular-branch metadata')
    need(q['negative_bound']=='16'and q['positive_bound']=='47/2'and q['positive_v_upper']=='5/9','original claimed constants')
    need(q['positive_closed_b_cover']==[['0','1/2'],['1/2','3/4'],['3/4','7/8'],['7/8','1']],'complete original closed cover')
    c=q['inherited_defining_data']
    need(type(c)is dict and set(c)=={'angular_denominator_y_tau','angular_numerator_y_tau','critical_quintic','discriminant','discriminant_divided_by_inverse_denominator','domain','inverse_common_denominator','inverse_numerators'},'all eight inherited defining fields')
    need(c['domain']=='QQ[p,tau][z]; actual p>2,0<tau<T,tau<1/(p^2+1),p=r+r^3,r>1','old physical string retained only as source metadata')
    def poly(rows):
        need(type(rows)is list and bool(rows),'whole nonempty target polynomial')
        out=[]
        for r in rows:
            need(type(r)is dict and set(r)=={'powers','coefficient'},'entire canonical target coefficient schema')
            need(type(r['powers'])is list and len(r['powers'])==2,'all two exact exponent slots')
            out.append([*r['powers'],r['coefficient']])
        return decode(out)
    def rotate(poly,k=0,shift=0):
        need(all((i+k-shift)%2==0 for i,j in poly),'real coefficient rotation parity')
        return P({(i,j):x*(-1)**i*(-1)**((i+k-shift)//2)for(i,j),x in poly.items()})
    if damage=='target-terminal':c['critical_quintic'][-1][-1]['coefficient']='2'
    if damage=='target-input-factor':c['inverse_numerators'][-1][-1]['coefficient']=str(F(c['inverse_numerators'][-1][-1]['coefficient'])+1)
    if damage=='target-domain':q['new_domain']='all complex formal profiles'
    if damage=='target-boolean':c['angular_denominator_y_tau'][-1]['powers'][0]=False
    need(q['new_domain']=='QQ[s,lambda][z]; actual s>0,exacttwo opposite-sign doubles,four singles,4+4; equal-magnitude branch separate9416','post-damage precise actual domain')
    need(len(c['critical_quintic'])==6 and [rotate(poly(row),k,1)for k,row in enumerate(c['critical_quintic'])]==own['H'],'every actual transferred quintic coefficient')
    need(rotate(poly(c['discriminant']))==own['delta']and rotate(poly(c['inverse_common_denominator']))==16*own['delta']and poly(c['discriminant_divided_by_inverse_denominator'])==const(F(1,16)),'entire actual discriminant and inverse normalization')
    need(len(c['inverse_numerators'])==5 and [rotate(poly(row),k)for k,row in enumerate(c['inverse_numerators'])]==[16*own['inv'][k][0]for k in range(5)],'all transferred inverse coefficients equal independently computed actual cofactors')
    for name,actual in [('angular_numerator_y_tau',own['num']),('angular_denominator_y_tau',own['den'])]:
        po=poly(c[name]);need(P({(2*i,j):x*(-1)**i for(i,j),x in po.items()})==actual,'entire transferred angular map '+name)
    canonical=(json.dumps(c,indent=2,sort_keys=True)+'\n').encode()
    need(hashlib.sha256(canonical).hexdigest()==q['whole_embedded_fields_canonical_sha256']==q['source_certificate_sha256'],'whole old defining source byte identity')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_input_bytes':fixture.stat().st_size,'target_input_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'whole_eight_defining_fields_paid_against_fresh_actual_ring':True,'all_inverse_and_angular_coefficients_checked':True,'target_native_or_EXPECTED_inspected_imported_executed':False,'prior_polynomial_identity_not_prior_physical_license':True}
if __name__=='__main__':
    signal.alarm(45)
    cli=argparse.ArgumentParser();cli.add_argument('--record',type=Path);cli.add_argument('--fixture',type=Path,default=Path(__file__).resolve().parent/'TARGET_INPUT.json');cli.add_argument('--damage');a=cli.parse_args()
    need(a.damage in [None,'target-terminal','target-input-factor','target-domain','target-boolean'],'known mathematical/schema defect')
    raw=json.dumps(run(a.fixture,a.damage),sort_keys=True,separators=(',',':')).encode()
    if a.record:a.record.write_bytes(raw)
    else:print(raw.decode())
