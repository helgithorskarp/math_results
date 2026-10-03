"""Post-seal DATA adapter. No author executable imported.

Compare all130 original QQ(q) forms, all24 entire determinant/shift
certificates, every4115 seed core and4332 repaired original positions.
The native-only baseline/extra controls are corroboration, not independent.
"""
import hashlib,json,pathlib,sys
from fractions import Fraction as F
import original
from frame import build,forms
from uniform import K,q

def decode(data,base=q,positive=False):
    if type(data['denominator']) is not int or data['denominator']<=0:raise ValueError('coefficient denominator')
    answer=K.zero;seen=set();constant=F(0)
    for ex,co in data['terms']:
        if len(ex)!=2 or ex[0]!=0 or type(ex[1]) is not int or ex[1]<0 or ex[1] in seen:raise ValueError('whole polynomial encoding')
        seen.add(ex[1]);a=F(int(co),data['denominator'])
        if not a or str(int(co))!=co:raise ValueError('canonical nonzero integer')
        if positive and a<0:raise ValueError('negative sign coefficient')
        if ex[1]==0:constant=a
        answer+=a*base**ex[1]
    if positive and constant<=0:raise ValueError('missing strict constant')
    return answer
def native_factors(items):
    out=K.one
    for item in items:
        power=item['power']
        if type(power) is not int or power<=0:raise ValueError('factor power')
        old=decode(item['original']);shifted=decode(item['shifted'],q-4,True)
        if old!=shifted:raise ValueError('whole positive factor shift')
        out*=old**power
    return out
def own_poly(coefficients,base=q):
    return sum((F(x)*base**i for i,x in enumerate(coefficients)),K.zero)
def compare(native,primary):
    raw=native['mathematics'];canonical=json.dumps(raw,sort_keys=True,separators=(',',':')).encode()
    digest=hashlib.sha256(canonical).hexdigest()
    if digest!=native['record_sha256'] or digest!='cf3ad87fd27030de8d1230708121f669fa214994732df613c47cbf17d54b58cd':raise ValueError('whole native record hash')
    model=build(q);blocks,off=forms(model,0)
    names=['alphaH','betaH','alphaL','betaL','nu','muL','heavy-anti-1','light-anti','heavy-standard','fixed']
    own_matrices=dict(zip(names,[[[x]] for x in model['scalars']]+blocks))
    cert=raw['certificate']
    if cert['domain']!='realq>=4,q4+v,v>=0' or set(cert['forms'])!=set(names):raise ValueError('complete native domain/catalogue')
    expected=[(name,i+1) for name in names for i in range(len(own_matrices[name]))]
    if [(r['group'],r['order']) for r in cert['rows']]!=expected:raise ValueError('ALL24 native obligation coverage')
    if cert['identities']!={'cross_sector_positions':272,'heavy_anti_equal_positions':8,'physical_change_rank':20,'original_field_positions':99}:raise ValueError('complete native dimension/multiplicity')
    normalization={};positions=0
    for name in names:
        form=cert['forms'][name];matrix=own_matrices[name];size=len(matrix)
        if len(form['raw_original'])!=size or len(form['cleared'])!=size:raise ValueError('native matrix size')
        scales=[]
        for i,row in enumerate(matrix):
            if len(form['raw_original'][i])!=size or len(form['cleared'][i])!=size:raise ValueError('native row size')
            scale=native_factors(form['domains'][i])/native_factors(form['removed'][i])*F(form['constants'][i])
            if F(form['constants'][i])<=0:raise ValueError('positive row scale')
            scales.append(scale)
            for j,own in enumerate(row):
                entry=form['raw_original'][i][j];den=K.one
                for item in entry['denominator_factors']:
                    den*=decode(item['factor'])**item['power']
                if decode(entry['numerator'])/den!=own:raise ValueError('ENTIRE native original-field binding')
                if decode(form['cleared'][i][j])!=own*scale:raise ValueError('ENTIRE native cleared-field binding')
                positions+=1
        normalization[name]=scales
    determinants=[]
    table_map=dict(zip(names,primary['uniform0']['tables']))
    for row in cert['rows']:
        name,k=row['group'],row['order'];table=table_map[name]
        own=own_poly(table['minors'][k-1]['shifted_coefficients'],q-4)
        for domain in table['row_domains'][:k]:own/=own_poly(domain['coefficients'])*domain['positive_scale']
        for scale in normalization[name][:k]:own*=scale
        native_old=decode(row['original']);native_new=decode(row['shifted'],q-4,True)
        if own!=native_old or native_old!=native_new:raise ValueError('ALL complete native determinant and shift coefficients')
        determinants.append(dict(group=name,order=k,native_positive_coefficients=len(row['shifted']['terms']),full_QQ_identity=True))
    literal=[];core_positions=sharp_positions=0
    saved=original.digest
    try:
        for fixture in raw['fixtures']:
            status=fixture['validation'];n=status['n'];captured=[]
            def capture(matrix):captured.append([r[:] for r in matrix]);return saved(matrix)
            original.digest=capture;own=original.fixture(n)
            family=own['original_vertices']
            if family!=fixture['all_original_sets']:raise ValueError('EVERY actual set binding')
            sorted_masks=sorted(family);lookup={a:i for i,a in enumerate(sorted_masks)}
            matrices=[[[a[lookup[x]][lookup[y]] for y in family] for x in family] for a in captured]
            N=own['N'];s=own['s'];h=own['h'];seed,sharp=matrices
            core=[[h*seed[i][j]+s*(i==j)-1 for j in range(1,N)] for i in range(1,N)]
            if core!=[[F(x) for x in r] for r in fixture['all_seed_core_positions']]:raise ValueError('ALL native seed core positions')
            if sharp!=[[F(x) for x in r] for r in fixture['all_sharp_original_positions']]:raise ValueError('ALL native sharp original positions')
            if F(status['kappa'])!=F(own['kappa']) or F(status['delta'])!=F(own['delta']):raise ValueError('whole scalar repair binding')
            core_positions+=(N-1)**2;sharp_positions+=N*N
            literal.append(dict(n=n,N=N,all_core_positions=(N-1)**2,all_sharp_positions=N*N,
                native_sharp_hash=status['sharp_matrix_sha256'],independent_sorted_sharp_hash=own['records'][1]['hash_original_M_sorted_by_mask']))
    finally:original.digest=saved
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',
        native_whole_record_sha256=digest,native_original_QQ_positions=positions,
        native_full_determinant_and_shift_identities=determinants,
        literal=literal,all_literal_seed_core_positions=core_positions,
        all_literal_sharp_positions=sharp_positions,
        native_only_corroboration='Baseline9361,12 scalar controls,18 native damages, '
            'native arithmetic/physical reconstruction/untouched action counts; '
            'no blanket independent audit of every native-only category.')
if __name__=='__main__':
    P=pathlib.Path(__file__).resolve().parent
    native=json.loads(pathlib.Path(sys.argv[1]).read_text())
    common=compare(native,json.loads((P/'PRIMARY.json').read_text()))
    (P/'COMMON.json').write_text(json.dumps(common,sort_keys=True,indent=2)+'\n')
    print(json.dumps(common,sort_keys=True))
