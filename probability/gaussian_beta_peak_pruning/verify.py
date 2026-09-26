"""Author exact controls; no independent review or floating point sign claim."""
from copy import deepcopy
from fractions import Fraction as F
import hashlib,json,math
from pathlib import Path
from certify import certificate,common_peak,distance,parse,pressure_block,verify_certificate
ROOT=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok: raise ArithmeticError(msg)


def rejected(fn):
    try: fn()
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return
    raise ArithmeticError('damaged input/certificate accepted')


def rank(rows):
    a=[[F(x) for x in r] for r in rows];r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r


def run():
    case=json.loads((ROOT/'INPUT.json').read_text())
    claim=json.loads((ROOT/'CERTIFICATE.json').read_text())
    verify_certificate(case,claim)
    x,y,w,s=parse(case)
    joined=[a+b for a,b in zip(x,y)]
    r=rank([[a-b for a,b in zip(p,joined[0])] for p in joined[1:]])
    require(r==6,'fixture must retain paired affine rank six')
    radius=max(distance(p,v[0])/s for v in [x,y] for p in v)
    require(radius<=128**2,'fixture does not fit normalized radius128')
    require(claim['peak']['common_normalized_peak_upper_bound']=='13/85','peak control')
    require(claim['rows'][0]['first_j']==0,'first open beta not signed')
    identities=0
    for j in range(13):
        for q in range(13):
            # Differentiate u^(j+2)(1-u)^q in expanded integer coefficients.
            left={j+1+l:(j+2+l)*(-1)**l*math.comb(q,l) for l in range(q+1)}
            right={}
            if q==0:right={j+1:j+2}
            else:
                for l in range(q):
                    c=(-1)**l*math.comb(q-1,l)
                    for power,coef in [(j+1+l,(j+2)*c),(j+2+l,-(j+q+2)*c)]:
                        right[power]=right.get(power,0)+coef
            require(left==right,'pressure derivative identity')
            identities+=1
    checks=0
    for den in range(1,18):
        for num in range(1,den+1):
            M=F(num,den)
            for N in range(25):
                rec=pressure_block(N,M)
                direct=[j for j in range(N+1) if j+2>=(N+2)*M]
                require(direct==list(range(rec['first_j'],N+1)),'block coverage')
                # This lower bound applies to any valid peak with <=A atoms.
                A=den
                if M>=F(1,A):
                    lower=max(0,((N+2+A-1)//A)-2)
                    require(rec['first_j']>=lower,'unresolved-block bound')
                checks+=1
    two={'dimension':3,'x':[[0,0,0],[2,0,0]],'y':[[0,0,0],[1,0,0]],'weights':['1/4','3/4'],'variance':1}
    require(common_peak(two)['common_normalized_peak_upper_bound']=='77/80','pair bound control')
    collapsed=deepcopy(two);collapsed['y']=[[0,0,0],[0,0,0]]
    require(common_peak(collapsed)['common_normalized_peak_upper_bound']=='1','collision bound')
    split=deepcopy(case);split['x'].append(split['x'][0]);split['y'].append(split['y'][0]);split['weights'][0]='1/20';split['weights'].append('1/20')
    require(common_peak(split)['common_normalized_peak_upper_bound']=='13/85','cluster splitting')
    zero=deepcopy(case);zero['x'].append([0,0,0]);zero['y'].append([999,0,0]);zero['weights'].append(0)
    require(common_peak(zero)==common_peak(case),'zero masses')
    before=common_peak(case)
    translated=deepcopy(case)
    translated['x']=[[str(F(c)+v) for c,v in zip(p,[3,-7,2])] for p in case['x']]
    translated['y']=[[str(F(c)+v) for c,v in zip(p,[-2,5,9])] for p in case['y']]
    require(common_peak(translated)==before,'translation invariance')
    scaled=deepcopy(case)
    for key in ['x','y']:scaled[key]=[[str(3*F(c)) for c in p] for p in case[key]]
    scaled['variance']=str(9*s)
    after=common_peak(scaled)
    for key in ['pair_peak_bound','separation_peak_bound','common_normalized_peak_upper_bound']:
        require(after[key]==before[key],'variance scaling')
    bad=deepcopy(claim);bad['rows'][1]['first_j']-=1
    rejected(lambda:verify_certificate(case,bad))
    bad2=deepcopy(claim);bad2['peak']['common_normalized_peak_upper_bound']='1/10'
    rejected(lambda:verify_certificate(case,bad2))
    expanding=deepcopy(two);expanding['y'][1][0]=3
    rejected(lambda:common_peak(expanding))
    badw=deepcopy(two);badw['weights']=['1/4','1/4']
    rejected(lambda:common_peak(badw))
    badv=deepcopy(two);badv['variance']=0
    rejected(lambda:common_peak(badv))
    badf=deepcopy(two);badf['variance']=1.0
    rejected(lambda:common_peak(badf))
    rejected(lambda:pressure_block(True,F(1,2)))
    rejected(lambda:pressure_block(7,F(0)))
    return {'status':'PRESSURE_BETA_BLOCK_EXACT_CONTROLS_PASS',
            'polynomial_identities':identities,'exact_block_and_barrier_checks':checks,
            'damage_controls':8,'fixture_paired_affine_rank':r,
            'fixture_normalized_squared_radius_about_first_label':str(radius),
            'certificate_sha256':hashlib.sha256((ROOT/'CERTIFICATE.json').read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256((ROOT/'INPUT.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    record=run();expected=json.loads((ROOT/'EXPECTED.json').read_text())
    require(record==expected,'expected output mismatch')
    print(json.dumps(record,sort_keys=True,indent=2))
