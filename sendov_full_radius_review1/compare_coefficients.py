import importlib.util,json,pathlib,hashlib
path=pathlib.Path(__file__).with_name('audit.py')
spec=importlib.util.spec_from_file_location('reviewer_fartrace',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
author_path=pathlib.Path(__file__).resolve().parent.parent/'sendov_degree9_full_radius_energy_minimizers/expected.json'
if hashlib.sha256(author_path.read_bytes()).hexdigest()!='30e7a5c3bf9ef654f4972e9bd1e985021402d6b58fd2022691f58b4a7197ae93':raise RuntimeError('reviewed author fixture changed')
a=json.loads(author_path.read_text())
author={r['name']:r['value'] for r in a['complete_records']}
alias={'t':'s','radial':'R','psi':'Psi'}
def decode(p):
 if 're' in p:return decode(p['re'])+m.ii*decode(p.get('im',{'terms':[]}))
 result=m.P()
 for monomial,(num,den) in p['terms']:
  term=m.P(m.Q(num,den))
  for name,power in monomial:term=term*m.var(alias.get(name,name),power)
  result=result+term
 return result
comparisons={
 'near second moment quadratic coefficient':m.near[2].coef(2),
 'complete near second moment quartic, including nonlinear mean':m.near[2].real().coef(4),
 'complete near third moment quartic':m.near[3].real().coef(4),
 'complete near fourth moment quartic':m.near[4].real().coef(4),
 **{'complete characteristic near trace jet '+str(k):m.near[k] for k in range(1,5)},
 'far second coefficient imaginary nonlinear mean':m.qfar.imag().coef(2),
 'far second coefficient real balanced shape':m.qfar.real().coef(2),
 'full universal angular-mean-inward fixed-energy quartic':m.excess.coef(4),
 'radius-parametric angular coefficient A':m.A,
 'radius-parametric angular coefficient B':m.B,
 'radius-parametric spectral coefficient C':m.C,
 'credited one-plus-seven quartic baseline':m.K1,
 'positive-slope polynomial factor':m.S,
}
for name,value in comparisons.items():
 if (value-decode(author[name])).d:raise RuntimeError('full coefficient mismatch '+name)
result={'status':'COMPLETE','scope':'16 complete symbolic coefficient records compared entrywise; not all58 author records','compared_records':list(comparisons),'all_exact':True,'author_fixture_sha256':hashlib.sha256(author_path.read_bytes()).hexdigest(),'author_executable_imported':False,'independent_derivation_reads_no_fixture':True}
print(json.dumps(result))
