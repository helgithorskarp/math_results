"""Definition-level rational check of the full screened AP-cover relaxation.

No generator or numerical library is imported. The underlying spatial
certificate is independently rechecked, and every integer AP is inspected.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import time


def need(value,message):
    if not value:raise ValueError(message)


def check(data,source):
    need(type(data) is dict and set(data)=={'format','phase','class_sum','far_sum',
         'denominator','base_certificate_sha256','position_weights'},'Schema')
    need(data['format']=='QR617_FRACTIONAL_HITTING_1','Format')
    need(all(type(data[k]) is int for k in ['phase','class_sum','far_sum','denominator']),'Integer fields')
    s=data['phase'];D=data['denominator'];B=data['class_sum'];L=data['far_sum']
    need((s,B,L)==(184,196,55) and D>0,'Stated phase and budgets')
    base_raw=(source/'certificates'/f'phase-{s:03d}.json').read_bytes()
    need(data['base_certificate_sha256']==hashlib.sha256(base_raw).hexdigest(),'Base bytes')
    base=json.loads(base_raw);spec=importlib.util.spec_from_file_location('base_exact',source/'verify.py')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    _,loads=v.check(base,[B],return_loads=True)
    d,u=base['denominator'],base['mu_numerator'];S=sum(e[2] for e in base['color0_APs'])
    delta=B*u+L*d-S;need(delta==514543,'Exact screen slack')
    t=(1-s)%617;lo,hi=base['inner'];colors=[];eligible=set();defects={}
    for x in range(3704):
        r=(x-1852+(s if x<1852 else t))%617
        c=-1 if r==0 else v.q[r]^int(x>=1852);colors.append(c)
        if c==0:
            defect=u+(0 if lo<=x<hi else d)-loads[x]
            need(defect>=0,'Nonnegative base defect');defects[x]=defect
            if defect<=delta:eligible.add(x)
    need(len(eligible)==881,'Exact eligible domain')
    weights=[0]*3704;seen=set();weighted_far=0;defect_sum=0;fractional=0
    need(type(data['position_weights']) is list and data['position_weights'],'Nonempty point weights')
    for e in data['position_weights']:
        need(type(e) is list and len(e)==2 and all(type(z) is int for z in e),'Point entry integers')
        x,num=e;need(x in eligible and x not in seen and 0<num<=D,'Eligible unique rational point')
        seen.add(x);weights[x]=num;weighted_far+=num*int(not lo<=x<hi)
        defect_sum+=num*defects[x];fractional+=int(num<D)
    need(sum(weights)==B*D,'Exact weighted class sum196')
    need(weighted_far==L*D,'Exact weighted far sum55')
    need(defect_sum<=delta*D,'Aggregate defect inequality')
    need(fractional>0,'This must be stated as fractional,not an integer witness')
    all_APs=0;mono=0;cross=0;minimum_coverage=None
    for step in range(1,618):
        for a in range(3704-6*step):
            all_APs+=1;points=[a+j*step for j in range(7)]
            if any(colors[x]!=0 for x in points):continue
            mono+=1;cross+=int(a<1852<=a+6*step)
            coverage=sum(weights[x] for x in points)
            need(coverage>=D,'Uncovered original monochromatic AP '+str((a,step)))
            minimum_coverage=coverage if minimum_coverage is None else min(minimum_coverage,coverage)
    need(all_APs==1141450 and mono==3065 and cross==mono,'Full actual AP domain')
    out={'agent':'six-vdw-3','role':'researcher','status':'EXACT_FRACTIONAL_FEASIBILITY_VERIFIED',
         'phase':s,'key':[s,t,1],'weighted_class_sum':str(Fraction(sum(weights),D)),
         'weighted_far_sum':str(Fraction(weighted_far,D)),'positive_point_weights':len(seen),
         'fractional_point_weights':fractional,'eligible_class0_positions':len(eligible),
         'aggregate_normalized_defect':str(Fraction(defect_sum,D*d)),
         'maximum_normalized_defect':str(Fraction(delta,d)),
         'checked_integer_APs':all_APs,'original_color0_monochromatic_APs':mono,
         'within_flank_monochromatic_APs':mono-cross,
         'minimum_AP_coverage':str(Fraction(minimum_coverage,D)),
         'binary_edit_set_claim':False,'AP_free_coloring_claim':False,'new_W_bound':False,
         'solver_trusted':False}
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path)
    p.add_argument('--output',type=Path);args=p.parse_args();begin=time.monotonic()
    raw=args.certificate.read_bytes()
    out=check(json.loads(raw),Path(__file__).resolve().parent/'base')
    out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    out['seconds']=time.monotonic()-begin
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
