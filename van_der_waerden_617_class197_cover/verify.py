"""Independent exact coverage of binary edit-membership splits.

Each leaf uses actual AP/capacity replay. Both children of every split are
mandatory; arbitrary extra inherited restrictions cannot be supplied.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def need(value,message):
    if not value:raise ValueError(message)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


def check(data,base_path,base_checker):
    need(type(data) is dict and set(data)=={'format','phase','class_cap','base_certificate_sha256','tree'},'Tree schema')
    need(data['format']=='QR617_CLASS196_BINARY_COVER_1','Tree format')
    need(type(data['phase']) is int and data['phase'] in [184,201,205,269] and type(data['class_cap']) is int and data['class_cap']==196,'Tree frontier')
    raw=base_path.read_bytes();need(hashlib.sha256(raw).hexdigest()==data['base_certificate_sha256'],'Tree base bytes')
    base=json.loads(raw);v=module(base_checker,'base_for_tree');v.check_case(base)
    need(base['s']==data['phase'],'Tree base phase')
    D=base['denominator'];delta=196*D-sum(e[2] for e in base['color0_APs']);need(delta>=0,'Prior base already excludes')
    load=[0]*3704
    for a,d,num in base['color0_APs']:
        for j in range(7):load[a+j*d]+=num
    eligible=set();s,t=base['s'],base['t']
    for x in range(3704):
        r=(x-1852+(s if x<1852 else t))%617
        if r and (v.Q[r]^int(x>=1852))==0 and D-load[x]<=delta:eligible.add(x)
    leaf_checker=module(Path(__file__).with_name('verify_leaf.py'),'exact_leaf')
    leaves=[];splits=[];nodes=0

    def visit(node,forced,forbidden):
        nonlocal nodes
        nodes+=1;need(nodes<=127,'Bounded finite tree')
        need(type(node) is dict,'Node object')
        if set(node)=={'leaf'}:
            leaf=node['leaf']
            need(type(leaf) is dict and leaf.get('phase')==s and leaf.get('base_certificate_sha256')==data['base_certificate_sha256'],'Leaf phase/base')
            result=leaf_checker.check(leaf,base_path,base_checker,forced,forbidden)
            leaves.append({k:v for k,v in result.items() if k!='cover2_cuts'});return
        need(set(node)=={'split','unchanged','edited'},'Exactly two children required')
        x=node['split'];need(type(x) is int and x in eligible-forced-forbidden,'New eligible split position')
        splits.append({'position_color0':x,'reflected_position_color1':3703-x,
                       'forced_before':sorted(forced),'forbidden_before':sorted(forbidden)})
        visit(node['unchanged'],forced,forbidden|{x})
        visit(node['edited'],forced|{x},forbidden)

    visit(data['tree'],set(),set())
    need(leaves,'No terminal proof')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_EXACT_COMPLETE_CLASS196_BINARY_COVER',
       'phase':s,'key':[s,t,1],'excluded_class_cap':196,'required_edits_per_reference_color':197,
       'root_eligible_positions_per_color':len(eligible),'nodes':nodes,'splits':splits,'leaves':leaves,
       'minimum_leaf_strict_gap':str(min(Fraction(x['strict_gap']) for x in leaves)),
       'checked_AP_instances':sum(x['checked_AP_instances'] for x in leaves),
       'checked_original_incidences':sum(x['checked_original_incidences'] for x in leaves),
       'other_color_budget_required':False,'far_cap_required':False,'pole_colors_free':True,
       'candidate_arbitrary':True,'candidate_symmetry_assumed':False,'solver_trusted':False,
       'unrestricted_exclusion':False,'optimality_or_attainability_claim':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--base',type=Path,required=True)
    p.add_argument('--base-checker',type=Path,required=True);p.add_argument('--output',type=Path)
    args=p.parse_args();raw=args.certificate.read_bytes();out=check(json.loads(raw),args.base,args.base_checker)
    out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='leaves'}),flush=True)


if __name__=='__main__':main()
