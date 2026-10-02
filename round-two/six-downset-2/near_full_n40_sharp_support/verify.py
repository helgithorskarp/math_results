"""Exact original n40 least-cutoff11 certificate; six-downset-2, researcher.

Full model/PSD/baseline and star decoder credited public9592 and its priors.
EVERY42 original physical forms checked; no low-degree omission is a premise.
The whole projected gap uses Q0=I-J/N, not a necessary core-I floor.
"""
import argparse,copy,hashlib,json
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from affine import direct,supported_pairs
from fixed40 import fixed_rref,ordinary_reference
from baseline import arithmetic_audit,check_original,digest,harmonic_literal_control,literal_baseline,rejected
from exact import both
from model import affine,blocks,original,parameters,require
ROOT=Path(__file__).resolve().parent
SEMANTICS='ORIGINAL full projected gap; Q0=I-J/N, all other Qj=I'


def gap_metric(n,j,aa):
    N=2**n-n-1
    return [[Q(int(a==b))-(Q(comb(n,b),N) if j==0 else Q(0)) for b in aa] for a in aa]


def seed_fixture(doc):
    require((doc['n'],doc['r'],doc['N'],doc['s'])==(40,38,1099511627735,549755813848),'Fixed original domain')
    require(doc['proper_support_cutoff']==11 and doc['star_only'] is True,'Full real-star S11 scope')
    require(doc['common_denominator']==10**24 and doc['upper_floor']=='1/4096'
            and doc['upper_floor_semantics']==SEMANTICS,'Exact defining gap metadata')
    pairs=[p for p in supported_pairs(40) if p[0]>=2]
    require(doc['free_pairs']==[list(p) for p in pairs] and len(pairs)==361,'Full free-coordinate census')
    require(len(doc['free_values'])==361 and all(type(v) is str for v in doc['free_values']),'All exact strings')
    values=[Q(v) for v in doc['free_values']]
    require(all(10**24%v.denominator==0 for v in values),'Common rational denominator')
    beta=direct(40,values);free,recover=fixed_rref()
    require(free==pairs and recover(values)==beta,'Independent all-row star decoders')
    excluded=[(a,b) for a,b in pairs if a>=12 and a+b<40]
    require(len(excluded)==72 and all(beta[a][b]==0 for a,b in excluded),'Every original proper bulk zero')
    return pairs,beta


def obstruction():
    """ALREADY PUBLISHED9471 GENERAL eta criterion, not merely sufficient6B."""
    n,k=40,10;r,N,s=parameters(n);h=N-s;q=comb(n,2);mu=Q(5625,16)
    v={a:max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n)) for a in range(k+1,n-k)}
    A=sum(a*a*comb(n,a) for a in range(2,k+1))
    S=sum((comb(n,a)*t*t for a,t in v.items()),Q(0))
    upper=n*h-2*q*s+(h-Q(s*s,h))*A+(n-1)*S
    eta=upper+mu*(4*s-4)
    delta=-eta/(2*h*mu)
    require(eta==Q(-9431218658090337964074823,1570730896820)<0,'Exact imported GENERAL criterion')
    require(delta==Q(18862437316180675928149646,1214322809876348231445946875)>0,'Exact parent margin')
    B=A-4*q;R=s-12*n*n
    require(6*B>R,'Weaker sufficient criterion FAILS, not an obstruction here')
    rho={(a,b):1-(a-v[a])*(b-v[b])/mu for a in v for b in v if a<=b and a+b<n}
    require(len(rho)==90 and all(0<x<1 for x in rho.values()),'All strict original weights')
    return {'parent':9471,'n':n,'k':k,'eta':str(eta),'positive_original_mass_floor':str(delta),
            'B':B,'R':R,'simpler6B_holds':False,'weighted_classes':90},rho,delta


def seed_checks(doc):
    pairs,beta=seed_fixture(doc);n=40;r,N,s=parameters(n);h=N-s;epsilon=Q(doc['upper_floor'])
    rows=[Q(s-(N-1))+sum(beta[a][b]*comb(n-a,b) for b in range(1,min(r,n-a)+1)) for a in range(1,r+1)]
    require(any(rows),'Core is noncentered, not constrained to mean zero')
    empty00=1+sum(comb(n,a)*rows[a-1] for a in range(1,r+1));emptyrow=[1-x for x in rows]
    require(empty00+sum(comb(n,a)*emptyrow[a-1] for a in range(1,r+1))==N,'Actual empty row including loop')
    require(all((N-1)+rows[a-1]+emptyrow[a-1]==N for a in range(1,r+1)),'Every actual nonempty row')
    records=[];dimension=core_rank=0
    for j,aa,g,K,U in blocks(n,beta):
        d=len(aa);metric=gap_metric(n,j,aa)
        lower=[[g[i]*x for x in row] for i,row in enumerate(K)]
        upper=[[g[i]*(U[i][t]-epsilon*metric[i][t]) for t in range(d)] for i in range(d)]
        if j<=1:
            v=aa if j==0 else [1]*d
            require(all(sum(K[i][t]*v[t] for t in range(d))==0 for i in range(d)),'COMPLETE required star kernel')
        rank=d-int(j<=1);both(lower,rank);both(upper,d)
        mult=comb(n,j)-(comb(n,j-1) if j else 0);dimension+=mult*d;core_rank+=mult*rank
        records.append({'j':j,'layers':aa,'order':d,'multiplicity':mult,'lower_rank':rank,
                        'upper_shifted_rank':d,'lower_sha256':digest(lower),'FULL_upper_shifted_sha256':digest(upper)})
    require(len(records)==21 and records[0]['order']==38 and dimension==N-1,'ALL42 complete forms including FULL upper0')
    require(core_rank==N-n-1,'Whole greatest lower rank through complete dimension')
    parent,rho,delta=obstruction();mass=weighted=Q(0);classes=[]
    for a,b in pairs:
        if a<=10 or a+b>=n:continue
        count=comb(n,a)*comb(n-a,b)//(2 if a==b else 1)
        value=Q(count,h)*beta[a][b];weighted+=rho[a,b]*value
        if value>0:mass+=value;classes.append([a,b,str(beta[a][b]),count,str(value)])
    require(weighted>=delta and mass>delta and classes and all(a==11 for a,b,v,c,m in classes),
            'Original proper layer11 carrier matches imported all-real obstruction')
    return {'n':n,'N':N,'s':s,'h':h,'all_supported_coordinates':399,'free_coordinates':361,
            'active_S11_coordinates':289,'excluded_proper_pairs':72,'star_rank':38,'star_decoders':2,
            'least_support_cutoff':11,'core_lower_rank':core_rank,'whole_lower_rank':core_rank+1,
            'whole_upper_rank':N-1,'whole_cap_floor':str(epsilon),'gap_semantics':SEMANTICS,
            'noncentered_core_row_sums':[str(x) for x in rows],'actual_empty_L00':str(empty00),
            'actual_empty_L0a':[str(x) for x in emptyrow],'sectors':records,
            'positive_original_bulk_mass_k10':str(mass),'original_weighted_parent_sum':str(weighted),
            'positive_bulk_classes':classes,'credited9471_GENERAL_control':parent}


def reference_checks():
    pairs,values,beta=ordinary_reference();records=[]
    for j,aa,g,K,U in blocks(40,beta):
        d=len(aa);lower=[[g[i]*v for v in row] for i,row in enumerate(K)]
        rank=both(lower,d-int(j<=1))
        if j:both([[g[i]*v for v in row] for i,row in enumerate(U)],d)
        else:require(U[0][0]==-10170482555447,'Known full mean-containing cap failure')
        records.append({'j':j,'order':d,'lower_rank':rank,'lower_sha256':digest(lower),
                        'upper_sha256':digest([[g[i]*v for v in row] for i,row in enumerate(U)])})
    require(sum((comb(40,z['j'])-(comb(40,z['j']-1) if z['j'] else 0))*z['lower_rank'] for z in records)+1
            ==1099511627695,'Credited ordinary greatest rank')
    return {'credited':'8106 ordinary z1 H, not a capped seed','upper0_diagonal':-10170482555447,'sectors':records}


def metric_control():
    """Prior9689 credited n6 example distinguishes exact whole gap from core-I."""
    meta,recover=affine(6);beta=recover([Q(24)]);records=[];energy=None
    for j,aa,g,K,U in blocks(6,beta):
        metric=gap_metric(6,j,aa)
        full=[[g[i]*(U[i][t]-2*metric[i][t]) for t in range(len(aa))] for i in range(len(aa))]
        rank=both(full)
        if j==0:
            wrong=[[g[i]*(U[i][t]-2*int(i==t)) for t in range(len(aa))] for i in range(len(aa))]
            energy=sum((x for row in wrong for x in row),Q(0))
            require(energy==-56,'False same core-I necessity rejected by whole original baseline')
        records.append({'j':j,'order':len(aa),'original_gap_shifted_rank':rank,'sha256':digest(full)})
    return {'credited':'9689 metric refinement; underlying n6 seed already published','n':6,
            'whole_projected_gap':'2','core_I_shift_constant_energy':str(energy),'complete_sectors':records}


def controls(seed):
    cases=[];excluded=next(i for i,(a,b) in enumerate(seed['free_pairs']) if a>=12 and a+b<40)
    for name,change in [
        ('missing coordinate',lambda z:z['free_values'].pop()),
        ('floating coordinate',lambda z:z['free_values'].__setitem__(0,.5)),
        ('wrong denominator',lambda z:z.__setitem__('common_denominator',1000)),
        ('wrong cutoff',lambda z:z.__setitem__('proper_support_cutoff',12)),
        ('false centering',lambda z:z.__setitem__('star_only',False)),
        ('wrong free pair',lambda z:z['free_pairs'].__setitem__(0,[1,1])),
        ('wrong cap floor',lambda z:z.__setitem__('upper_floor','0')),
        ('wrong original metric',lambda z:z.__setitem__('upper_floor_semantics','Core I floor')),
        ('bulk support damage',lambda z:z['free_values'].__setitem__(excluded,'1/1000000000000000000000000'))]:
        bad=copy.deepcopy(seed);change(bad)
        require(rejected(lambda:seed_fixture(bad)),'Reject '+name);cases.append(name)
    bad=copy.deepcopy(seed);bad['free_values'][0]='1000000000000000000000000'
    require(rejected(lambda:seed_checks(bad)),'Reject damaged positivity');cases.append('damaged positivity')
    meta,recover=affine(6);beta=recover([Q(24)]);F,C,L=original(6,beta,Q(1,528));L[0][0]+=1
    require(rejected(lambda:check_original(6,C,L,F)),'Reject actual empty loop damage');cases.append('actual empty loop')
    require(rejected(lambda:original(40,seed_fixture(seed)[1])),'Forbid trillion-order allocation');cases.append('n40 literal allocation')
    require(rejected(lambda:both([[Q(1),Q(2)],[Q(2),Q(1)]])),'Reject indefinite input');cases.append('indefinite input')
    return cases


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();seed=json.loads((ROOT/'seed.json').read_text())
    result={'agent':'six-downset-2','role':'researcher',
        'status':'Exact author rational certificate; ordinary bridges unformalized; independent review pending',
        'seed':seed_checks(seed),'credited_n40_ordinary_reference':reference_checks(),
        'literal_published_n6_baseline':literal_baseline(),'whole_literal_harmonic_control':harmonic_literal_control(),
        'arithmetic_audit':arithmetic_audit(),'exact_original_gap_control':metric_control(),
        'rejected_controls':controls(seed),'seed_sha256':hashlib.sha256((ROOT/'seed.json').read_bytes()).hexdigest(),
        'arithmetic':'integers and fractions.Fraction','no_original_n40_allocation':True}
    body=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:require(args.check.read_text()==body,'ENTIRE frozen record mismatch')
    if args.output:args.output.write_text(body)
    print(json.dumps({'ok':True,'record_sha256':hashlib.sha256(body.encode()).hexdigest(),'complete_sectors':42,
                      'least_support_cutoff':11,'literal_action_columns':112,'controls':len(result['rejected_controls'])}))


if __name__=='__main__':main()
