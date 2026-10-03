"""PRIVATE separate univariate sign/identity checker for a fixed h.

Based on credited9838 checker; imports no producer polynomial engine.
The same-author Fraction physical recipe is disclosed, not peer review.
Degree-complete Gaussian and clearing checks establish polynomial identities.
"""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json,signal,time,resource
from sectors import sectors

def require(ok,msg):
    if not ok:raise ValueError(msg)
def decode(data,positive=False):
    den=data['denominator'];require(type(den) is int and den>0,'positive coefficient denominator')
    terms={};require(len(data['terms'])<=512,'unchanged512 term guard')
    for ex,value in data['terms']:
        require(type(ex) is list and len(ex)==2 and ex[0]==0 and type(ex[1]) is int and ex[1]>=0,'univariate embedded exponent')
        co=int(value);require(str(co)==value and co and ex[1] not in terms,'canonical unique nonzero integer coefficient')
        terms[ex[1]]=co
    if positive:require(terms.get(0,0)>0 and all(c>=0 for c in terms.values()),'strict shifted coefficient positivity')
    return terms,den
def degree(p):return max(p[0],default=0)
def value(p,q):return F(sum(c*q**e for e,c in p[0].items()),p[1])
def determinant(a):
    a=[[F(z) for z in row] for row in a];answer=F(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];answer=-answer
        d=a[j][j];answer*=d
        for i in range(j+1,len(a)):
            c=a[i][j]/d
            for k in range(j+1,len(a)):a[i][k]-=c*a[j][k]
    return answer
def shift_identity(original,shifted):
    bound=degree(original);require(degree(shifted)<=bound,'exact shift degree bound')
    for v in range(bound+1):require(value(original,4+v)==value(shifted,v),'FULL q4 composition identity')
    return bound+1
def factor(data):
    old,new=decode(data['original']),decode(data['shifted'],True)
    count=shift_identity(old,new);power=data['power'];require(type(power) is int and power>0,'positive factor exponent')
    return old,power,count
def factors_value(fs,q):return prod(value(p,q)**e for p,e in fs)
def factors_degree(fs):return sum(degree(p)*e for p,e in fs)

def check(data):
    h=data['fixed_heavy_count'];require(type(h) is int and 2<=h<=10,'ENTIRE literal heavy-count domain')
    require(data['coefficient_domain']=='QQ(q), q=4+v,v>=0','ENTIRE q-uniform domain')
    require(data['complete_cap_requested'] is True and data['uniform_h_theorem'] is False,'ENTIRE declared scope')
    scalar_names=['alphaH','betaH','alphaL','betaL','nu','muL']
    expected=[(name,1) for name in scalar_names]+[(name,k) for name,size in [('antiH',2),('antiL',2),('standard',4),('fixed',10)] for k in range(1,size+1)]
    require([(r['group'],r['order']) for r in data['rows']]==expected,'ALL24 scalar/Sylvester obligations')
    require(set(data['forms'])==set(name for name,k in expected),'ENTIRE original-field catalogue')
    cache={};live_positions=0
    def live(q):
        if q not in cache:
            p,G,S,C=sectors(F(h),F(q));cache[q]={name:[[p[name]]] for name in scalar_names}|C
        return cache[q]
    parsed=[]
    for row in data['rows']:
        original,shifted=decode(row['original']),decode(row['shifted'],True)
        points=shift_identity(original,shifted);parsed.append((row,original,shifted,points))
    form_records=[];factor_shifts=0;entry_points=0
    for name,form in data['forms'].items():
        raw=form['raw_original'];size=len(raw);a=[[decode(z) for z in row] for row in form['cleared']]
        require(len(a)==size and all(len(row)==size for row in a) and all(len(row)==size for row in raw),'ENTIRE original raw/cleared dimensions')
        require(len(form['domains'])==len(form['removed'])==len(form['constants'])==size,'ENTIRE row normalization')
        for i in range(size):
            domains=[];removed=[]
            for group,out in [(form['domains'][i],domains),(form['removed'][i],removed)]:
                for f in group:
                    p,e,count=factor(f);out.append((p,e));factor_shifts+=count
            const=F(form['constants'][i]);require(const>0,'strict positive row constant')
            for j in range(size):
                z=raw[i][j];numerator=decode(z['numerator']);den=[]
                for item in z['denominator_factors']:
                    p=decode(item['factor']);e=item['power'];require(type(e) is int and e>0,'raw rational factor exponent')
                    allowed=[{1:1},{0:-1,1:1}]+[{0:b,1:1} for b in (3*h-4,3*h-3,3*h)]
                    require(p[1]==1 and p[0] in allowed,'only stated original rational poles')
                    den.append((p,e))
                lhs=degree(a[i][j])+factors_degree(removed)+factors_degree(den)
                rhs=degree(numerator)+factors_degree(domains);bound=max(lhs,rhs)
                for q in range(4,5+bound):
                    left=value(a[i][j],q)*factors_value(removed,q)*factors_value(den,q)
                    right=value(numerator,q)*factors_value(domains,q)*const
                    require(left==right,'FULL original clearing polynomial identity')
                    require(value(numerator,q)/factors_value(den,q)==live(q)[name][i][j],'EVERY independent Fraction original-form binding')
                    entry_points+=1;live_positions+=1
        form_records.append(dict(group=name,size=size,whole_positions=size*size))
    checks=[];shift_points=0;det_points=0
    for row,original,shifted,points in parsed:
        name,k=row['group'],row['order'];form=data['forms'][name]
        a=[[decode(z) for z in values[:k]] for values in form['cleared'][:k]]
        shift_points+=points;bound=max(degree(original),sum(max((degree(z) for z in values),default=0) for values in a))
        for q in range(4,5+bound):
            require(value(original,q)==determinant([[value(z,q) for z in values] for values in a]),'FULL degree-bounded Gaussian determinant identity');det_points+=1
        require(row['total_degree']==degree(original) and row['shifted_terms']==len(shifted[0]) and row['original_terms']==len(original[0]) and row['positive'] is True,'ENTIRE sign metadata')
        checks.append(dict(group=name,order=k,positive_coefficients=len(shifted[0]),determinant_identity_bound=bound,determinant_identity_points=bound+1,shift_identity_points=points))
    return dict(fixed_heavy_count=h,checks=checks,positive_coefficients=sum(z['positive_coefficients'] for z in checks),full_determinant_identity_points=det_points,full_shift_points=shift_points,positive_clearing_factor_shift_points=factor_shifts,full_original_entry_identity_points=entry_points,live_original_fraction_bindings=live_positions,whole_original_form_positions=sum(z['whole_positions'] for z in form_records),cached_q_values=len(cache),complete=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('file');ap.add_argument('--output');args=ap.parse_args()
    def alarm(signum,frame):raise TimeoutError('unchanged60s fixed-count checker guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    result=check(json.loads(Path(args.file).read_text()));signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',status='PASS: all fixed-h coefficient/clearing/determinant identities; ordinary physical bridge separate',checks=result)
    h=result['fixed_heavy_count'];Path(args.output or f'work/check-h{h}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='checks'}|{k:v for k,v in result.items() if k!='checks'}))
