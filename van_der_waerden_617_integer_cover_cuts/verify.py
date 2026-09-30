"""Independent exact original-AP, screened-petal and cover-two checker.

The only imported checker is the earlier exact Euler/capacity checker.
Every new triple is tied to actual integer APs, with empty common petal.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def need(value,message):
    if not value:raise ValueError(message)


def check(data,source):
    need(type(data) is dict and set(data)=={'format','phase','class_cap','far_cap',
         'base_certificate_sha256','denominator','mu_numerator','color0_APs','color0_cover2'},'Schema')
    need(data['format']=='QR617_SCREENED_COVER2_DUAL_1','Format')
    need(all(type(data[k]) is int for k in ['phase','class_cap','far_cap','denominator','mu_numerator']),'Integer fields')
    s=data['phase'];B,L=data['class_cap'],data['far_cap'];den,mu=data['denominator'],data['mu_numerator']
    need(s in [184,201,205,269] and 0<=B<=3704 and 0<=L<=3704 and den>0 and mu>=0,'Domain')
    raw=(source/'certificates'/f'phase-{s:03d}.json').read_bytes();need(data['base_certificate_sha256']==hashlib.sha256(raw).hexdigest(),'Base bytes')
    base=json.loads(raw);spec=importlib.util.spec_from_file_location('base_exact',source/'verify.py')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    _,base_loads=v.check(base,[B],return_loads=True)
    D,u=base['denominator'],base['mu_numerator'];S=sum(e[2] for e in base['color0_APs'])
    delta=B*u+L*D-S;need(delta>=0,'Base already excludes these budgets')
    t=(1-s)%617;lo,hi=base['inner'];eligible=[set(),set()]
    for x in range(3704):
        r=(x-1852+(s if x<1852 else t))%617
        if not r:continue
        c=v.q[r]^int(x>=1852);defect=u+(0 if lo<=x<hi else D)-base_loads[x]
        need(defect>=0,'Nonnegative defect')
        if defect<=delta:eligible[c].add(x)
    need(eligible[1]=={3703-x for x in eligible[0]},'Reflected eligibility')
    loads=[0]*3704;totals=[0,0];APchecks=0;incidences=0;screened=0
    def petal(a,d,c):
        nonlocal APchecks,incidences
        need(type(a) is int and type(d) is int and d>0,'Actual AP integers')
        need(0<=a<1852<=a+6*d<3704,'Actual crossing AP bounds')
        APchecks+=1;out=set()
        for j in range(7):
            x=a+j*d;r=(x-1852+(s if x<1852 else t))%617
            need(r!=0 and (v.q[r]^int(x>=1852))==c,'Required nonpole original color')
            incidences+=1
            if x in eligible[c]:out.add(x)
        need(out,'Nonempty required petal');return out
    need(type(data['color0_APs']) is list and type(data['color0_cover2']) is list,'Weight lists')
    seen=set()
    for entry in data['color0_APs']:
        need(type(entry) is list and len(entry)==3 and all(type(x) is int for x in entry),'AP weight integers')
        a,d,w=entry;need(w>0 and (a,d) not in seen,'Positive unique AP weight');seen.add((a,d))
        for c,aa in [(0,a),(1,3703-a-6*d)]:
            p=petal(aa,d,c)
            for x in p:loads[x]+=w;screened+=1
            totals[c]+=w
    cuts=[];cut_seen=set()
    for entry in data['color0_cover2']:
        need(type(entry) is list and len(entry)==2,'Cover entry')
        triple,w=entry;need(type(w) is int and w>0 and type(triple) is list and len(triple)==3,'Positive triple weight')
        need(all(type(ap) is list and len(ap)==2 and all(type(z) is int for z in ap) for ap in triple),'Triple AP integers')
        key=tuple(sorted(tuple(ap) for ap in triple));need(len(set(key))==3 and key not in cut_seen,'Unique three-AP cut');cut_seen.add(key)
        sizes=[]
        for c in [0,1]:
            petals=[petal(a if c==0 else 3703-a-6*d,d,c) for a,d in triple]
            need(not set.intersection(*petals),'Cover-two common intersection must be empty')
            union=set.union(*petals);sizes.append(len(union))
            for x in union:loads[x]+=w;screened+=1
            totals[c]+=2*w
        need(sizes[0]==sizes[1],'Reflected cover unions')
        cuts.append({'triple_APs':triple,'weight':str(Fraction(w,den)),'eligible_union_size':sizes[0]})
    need(totals[0]==totals[1]>0,'Equal positive reflected sums')
    for c in [0,1]:
        for x in eligible[c]:need(loads[x]<=mu+(0 if lo<=x<hi else den),'Exact final point capacity')
    gap=totals[0]-B*mu-L*den;need(gap>0,'No strict exact budget contradiction')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_EXACT_SCREENED_COVER2_EXCLUSION',
            'phase':s,'key':[s,t,1],'class_cap':B,'excluded_far_cap':L,
            'required_far_edits_per_budgeted_class':L+1,'eligible_positions_each_color':len(eligible[0]),
            'base_screen_slack':str(Fraction(delta,D)),
            'final_weight_sum_each_color':str(Fraction(totals[0],den)),
            'final_mu':str(Fraction(mu,den)),'strict_gap':str(Fraction(gap,den)),
            'strict_gap_numerator':gap,'D':den,'checked_new_AP_instances':APchecks,
            'checked_new_AP_incidences':incidences,'screened_load_incidences':screened,
            'cover2_cuts':cuts,'candidate_arbitrary':True,'pole_colors_free':True,
            'candidate_symmetry_assumed':False,'solver_trusted':False,
            'repair_optimum_or_attainability_claim':False,'unrestricted_exclusion':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();raw=args.certificate.read_bytes()
    source=Path(__file__).resolve().parent/'base';out=check(json.loads(raw),source)
    out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
