"""Post-seal entire eight-field author mathematical input audit, no native imports."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json,runpy,sys,tempfile

def run(fixture):
    here=Path(__file__).resolve().parent
    # Reexecute the sealed independent standard-library mathematics in a fresh
    # namespace, rather than importing any target implementation or summary.
    scratch=Path('scratch');scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='two-double-fixture-',dir=scratch)as temp:
        previous=sys.argv;sys.argv=[str(here/'check.py'),'--record',str(Path(temp)/'record.json')]
        try:own=runpy.run_path(str(here/'check.py'))
        finally:sys.argv=previous
    fields={'angular_denominator_y_tau','angular_numerator_y_tau','critical_quintic','discriminant','discriminant_divided_by_inverse_denominator','domain','inverse_common_denominator','inverse_numerators'}
    domain='QQ[p,tau][z]; actual p>2,0<tau<T,tau<1/(p^2+1),p=r+r^3,r>1'
    need=own['need'];P=own['P'];decode=own['decode']
    def polynomial(rows):
        need(isinstance(rows,list)and rows,'nonempty author polynomial')
        need(all(isinstance(row,dict)and set(row)=={'powers','coefficient'}for row in rows),'entire author sparse schema')
        need(all(isinstance(row['powers'],list)and len(row['powers'])==2 for row in rows),'two typed author exponent slots')
        return decode([[*row['powers'],row['coefficient']]for row in rows])
    def certify(c):
        need(isinstance(c,dict)and set(c)==fields,'complete eight-field mathematical schema')
        need(c['domain']==domain,'stated exact domain binding')
        need(isinstance(c['critical_quintic'],list)and len(c['critical_quintic'])==6,'entire critical quintic shape')
        h=[polynomial(row)for row in c['critical_quintic']]
        need(h==own['H'],'all original quintic coefficients')
        delta=polynomial(c['inverse_common_denominator']);disc=polynomial(c['discriminant']);w=polynomial(c['discriminant_divided_by_inverse_denominator'])
        need(disc==own['delta']and delta==16*disc and delta*w==disc,'entire actual derivative norm and inverse denominator divisor')
        need(isinstance(c['inverse_numerators'],list)and len(c['inverse_numerators'])==5,'entire inverse polynomial shape')
        inverse=[polynomial(row)for row in c['inverse_numerators']]
        need(inverse==[16*own['inverse'][i][0]for i in range(5)],'all inverse numerators against independently generated adjugate')
        invm=own['evalm'](inverse,own['M'])
        need(own['multiply'](own['der'],invm)==own['scale'](own['eye'](5),delta)==own['multiply'](invm,own['der']),'all25 left/right author inverse matrix identities')
        n=polynomial(c['angular_numerator_y_tau']);d=polynomial(c['angular_denominator_y_tau'])
        lift=lambda a:P({(2*i,j):v for (i,j),v in a.items()})
        need(lift(n)==own['num']and lift(d)==own['den'],'every author71/70 angular coefficient equals independently derived polynomial')
        return {'complete_fields':8,'whole_inverse_polynomials':5,'whole_left_right_inverse_positions':25,'angular_numerator_terms':len(n),'angular_denominator_terms':len(d),'entire_discriminant_terms':len(disc),'entire_arithmetic_and_domain_binding':True}
    raw=fixture.read_bytes();certificate=json.loads(raw);result=certify(certificate);damages=[]
    def test(label,change):
        candidate=copy.deepcopy(certificate);change(candidate)
        try:certify(candidate)
        except ValueError as e:damages.append({'defect':label,'rejected':True,'mathematical_or_schema_gate':str(e)})
        else:raise ValueError('author mathematical damage accepted '+label)
    def change_coefficient(c,field,index=0):
        row=c[field][index];row['coefficient']=str(F(row['coefficient'])+1)
    for field in ['angular_numerator_y_tau','angular_denominator_y_tau','inverse_common_denominator','discriminant','discriminant_divided_by_inverse_denominator']:
        test('wrong-'+field,lambda c,field=field:change_coefficient(c,field))
    test('quintic-last-coefficient',lambda c:change_coefficient({'h':c['critical_quintic'][-1]},'h'))
    test('inverse-first-numerator',lambda c:change_coefficient({'i':c['inverse_numerators'][0]},'i'))
    test('inverse-terminal-numerator',lambda c:change_coefficient({'i':c['inverse_numerators'][-1]},'i',-1))
    test('omit-angular-terminal-term',lambda c:c['angular_numerator_y_tau'].pop())
    test('duplicate-sparse-position',lambda c:c['discriminant'].append(copy.deepcopy(c['discriminant'][0])))
    test('boolean-exponent',lambda c:c['discriminant'][0]['powers'].__setitem__(0,False))
    test('string-exponent',lambda c:c['discriminant'][0]['powers'].__setitem__(0,'0'))
    test('noncanonical-rational',lambda c:c['discriminant'][0].__setitem__('coefficient','162/32'))
    test('omitted-domain',lambda c:c.pop('domain'))
    test('unlicensed-domain',lambda c:c.__setitem__('domain','QQ[p,tau]; all real p,tau'))
    test('unrelated-extra-field',lambda c:c.__setitem__('unpaid_claim',True))
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','fixture_bytes':len(raw),'fixture_sha256':hashlib.sha256(raw).hexdigest(),'written_claim_exposed_not_blind':True,'whole_mathematical_fixture_access_after_primary_seal':True,'author_native_programs_inspected_imported_executed':False,'complete_result':result,'all16_meaningful_damages_rejected':True,'damages':damages}

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--fixture',type=Path,default=Path(__file__).resolve().parent/'AUTHOR_CERTIFICATE.json');cli.add_argument('--record',type=Path);args=cli.parse_args()
    data=json.dumps(run(args.fixture),sort_keys=True,separators=(',',':')).encode()
    if args.record:args.record.write_bytes(data)
    else:print(data.decode())
