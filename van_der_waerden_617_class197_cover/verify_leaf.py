"""Independent exact conditional class-budget exclusion via original APs.

Imports only the previously published uniform exact checker. Does not import
the new generator, its AP enumeration, triangle search, or numerical libraries.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def need(value,message):
    if not value:raise ValueError(message)


def check(data,base_path,base_checker,forced=None,forbidden=None):
    need(type(data) is dict and set(data)=={'format','phase','class_cap','base_certificate_sha256',
      'denominator','color0_APs','color0_cover2','color0_surcharges'},'Schema')
    need(data['format']=='QR617_UNIFORM_SCREENED_COVER2_1','Format')
    need(all(type(data[k]) is int for k in ['phase','class_cap','denominator']),'Integer fields')
    phase,B,D=data['phase'],data['class_cap'],data['denominator']
    need(phase in [184,201,205,269] and B==196 and D>0,'Frontier')
    raw=base_path.read_bytes();need(hashlib.sha256(raw).hexdigest()==data['base_certificate_sha256'],'Base bytes')
    base=json.loads(raw);spec=importlib.util.spec_from_file_location('uniform_base',base_checker)
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);v.check_case(base)
    need(base['s']==phase,'Base phase')
    d0=base['denominator'];S=sum(e[2] for e in base['color0_APs']);delta=B*d0-S
    need(delta>=0,'Base already excludes budget')
    loads0=[0]*3704
    for a,d,w in base['color0_APs']:
        for aa in [a,3703-a-6*d]:
            for j in range(7):loads0[aa+j*d]+=w
    eligible=[set(),set()];t=(1-phase)%617
    for x in range(3704):
        r=(x-1852+(phase if x<1852 else t))%617
        if not r:continue
        c=v.Q[r]^int(x>=1852);defect=d0-loads0[x]
        need(defect>=0,'Nonnegative base defect')
        if defect<=delta:eligible[c].add(x)
    need(eligible[1]=={3703-x for x in eligible[0]},'Reflected eligible sets')
    forced=set() if forced is None else set(forced)
    forbidden=set() if forbidden is None else set(forbidden)
    need(not forced&forbidden and forced|forbidden<=eligible[0],'Valid inherited branch state')
    need(all(type(x) is int for x in forced|forbidden),'Branch position integers')
    fsets=[forced,{3703-x for x in forced}]
    xsets=[forbidden,{3703-x for x in forbidden}]
    free=[eligible[c]-fsets[c]-xsets[c] for c in [0,1]]
    remaining=B-len(forced);need(remaining>=0,'Forced class budget exceeded')
    loads=[0]*3704;weighted=[0,0];checks=0

    def petal(a,d,c):
        nonlocal checks
        need(type(a) is int and type(d) is int and d>0,'Actual AP integers')
        need(0<=a<1852<=a+6*d<3704,'Actual crossing coordinates');checks+=1
        out=set()
        for j in range(7):
            x=a+j*d;r=(x-1852+(phase if x<1852 else t))%617
            need(r and (v.Q[r]^int(x>=1852))==c,'Actual nonpole monochromatic AP')
            if x in eligible[c]:out.add(x)
        return out

    need(all(type(data[k]) is list for k in ['color0_APs','color0_cover2','color0_surcharges']),'Weight lists')
    seen=set()
    for e in data['color0_APs']:
        need(type(e) is list and len(e)==3 and all(type(x) is int for x in e),'AP entry')
        a,d,w=e;need(w>0 and (a,d) not in seen,'Positive unique AP');seen.add((a,d))
        for c,aa in [(0,a),(1,3703-a-6*d)]:
            p=petal(aa,d,c)
            for x in p&free[c]:loads[x]+=w
            weighted[c]+=int(not p&fsets[c])*w
    cut_seen=set();cut_details=[]
    for e in data['color0_cover2']:
        need(type(e) is list and len(e)==2,'Cut entry')
        triple,w=e;need(type(w) is int and w>0 and type(triple) is list and len(triple)==3,'Positive triple weight')
        need(all(type(ap) is list and len(ap)==2 and all(type(x) is int for x in ap) for ap in triple),'Triple AP integers')
        key=tuple(sorted(tuple(ap) for ap in triple));need(len(set(key))==3 and key not in cut_seen,'Three distinct unique APs');cut_seen.add(key)
        sizes=[]
        for c in [0,1]:
            petals=[petal(a if c==0 else 3703-a-6*d,d,c) for a,d in triple]
            need(all(petals) and not set.intersection(*petals),'Nonempty petals and empty common intersection')
            union=set.union(*petals);sizes.append(len(union))
            for x in union&free[c]:loads[x]+=w
            weighted[c]+=max(0,2-len(union&fsets[c]))*w
        need(sizes[0]==sizes[1],'Reflected union sizes')
        cut_details.append({'triple_APs':triple,'union_size':sizes[0],'weight_numerator':w})
    surcharge=[0]*3704;surcharge_totals=[0,0];seen=set()
    for e in data['color0_surcharges']:
        need(type(e) is list and len(e)==2 and all(type(x) is int for x in e),'Surcharge entry')
        x,num=e;need(x in free[0] and x not in seen and num>0,'Eligible unique positive surcharge');seen.add(x)
        for c,xx in [(0,x),(1,3703-x)]:surcharge[xx]=num;surcharge_totals[c]+=num
    for c in [0,1]:
        for x in free[c]:need(loads[x]<=D+surcharge[x],'Exact point capacity with surcharge')
    need(weighted[0]==weighted[1]>0 and surcharge_totals[0]==surcharge_totals[1],'Equal reflected totals')
    net=weighted[0]-surcharge_totals[0];gap=net-remaining*D;need(gap>0,'No strict exact class-budget exclusion')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_EXACT_CLASS196_EXCLUSION' if not forced and not forbidden else 'VERIFIED_EXACT_CONDITIONAL_BRANCH_EXCLUSION',
       'phase':phase,'key':[phase,t,1],'excluded_class_cap':B,'required_edits_per_reference_color':B+1,
       'forced_positions':sorted(forced),'forbidden_positions':sorted(forbidden),
       'remaining_class_cap':remaining,'free_positions_per_color':len(free[0]),
       'eligible_positions_per_color':len(eligible[0]),'base_screen_slack':str(Fraction(delta,d0)),
       'new_weighted_total':str(Fraction(weighted[0],D)),
       'new_surcharge_total':str(Fraction(surcharge_totals[0],D)),
       'net_weight':str(Fraction(net,D)),'strict_gap':str(Fraction(gap,D)),
       'strict_gap_numerator':gap,'denominator':D,'checked_AP_instances':checks,
       'checked_original_incidences':7*checks,'positive_AP_weights':len(data['color0_APs']),
       'positive_cover2_weights':len(cut_details),'positive_vertex_surcharges':len(data['color0_surcharges']),
       'cover2_cuts':cut_details,'pole_colors_free':True,'candidate_arbitrary':True,
       'candidate_symmetry_assumed':False,'other_color_budget_required':False,
       'far_edit_cap_required':False,'solver_trusted':False,'unrestricted_exclusion':False,
       'optimality_or_attainability_claim':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path)
    p.add_argument('--base',type=Path,required=True);p.add_argument('--base-checker',type=Path,required=True)
    p.add_argument('--output',type=Path);args=p.parse_args();raw=args.certificate.read_bytes()
    out=check(json.loads(raw),args.base,args.base_checker);out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cover2_cuts'}),flush=True)


if __name__=='__main__':main()
