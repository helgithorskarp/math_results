"""Late, optional entire-record comparison; no premise of the offline proof.

The target packet was first acquired only after the independent core seal.
The adapter maps the independent role totals into the target certificate
schema and compares every field, not only the cut label or whole checksum.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from columns import allocations
from populations import census
from rows import load, require

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def shape(case,types,vector,c):
    vertices=[r for r,n in zip(types,vector) for _ in range(n)]
    unit=[r for r in vertices if r[0]==0]
    a=[r for r in unit if not r[3]]
    ineligible=[r for r in vertices if r[0]>0 and not r[3]]
    reason=c['verdict']
    if reason in ('unit','crossing','closure'):
        oldreason={'unit':'UNIT_NEIGHBOR_CAPACITY','crossing':'DISTINCT_RADIUS_TWO_CROSSINGS',
                   'closure':'ALL_COLORS_CLOSED_PARTITION'}[reason]
        return {'reason':'FROZEN_ENDPOINT_RADIUS_OR_CLOSURE','cut':{
            'reason':oldreason,'D':c['D_U'],'I':c['I'],'C1':c['C1'],'C2':c['C2'],
            'B2':c['B2_support'],'unit_roots_k0':c['roots'],
            'ineligible_nonunit_roots_k0':sum(r[1]==0 for r in ineligible),
            'unit_rows':len(unit),'ineligible_unit_rows':len(a),
            'ineligible_nonunit_rows':len(ineligible),'eligible_nonunit_rows':c['eligible_nonunits']}}
    if reason=='root_endpoint':
        even=2*(c['I']//2)
        return {'reason':'9538_ROOT_ENDPOINT_C1','R':c['roots'],'D_A':c['D_A'],
                'D_V':c['D_V'],'I_even':even,'C1':c['C1'],
                'required':c['D_V']+max(c['roots'],c['D_A']-even)}
    if reason=='B2':
        return {'reason':'ACTUAL_HH_B2_CAP','B_count':c['exceptional_B'],'bound':2}
    require(case[0]==3 and case[5] in (12,13) and c['exceptional_B']==2,'new residue scope')
    require(all(r[1]<=1 and r[10]<=2*r[1] and (r[10]<2 or r[2]<=1) for r in vertices),'actual row scope')
    require(not allocations(case[5]),'actual necessary column screen')
    return {'reason':'DISJOINT_SINGLE_HUB_COLUMNS','K':case[5],'hub_weight':19,
            'heavy_entries':19-case[5],'distinct_B_hubs':True,
            'all_five_columns_positive':True,'accepted_ordered_allocations':0}

def independent_core():
    raw,capped,types=load()
    cases,vectors,hist=census(types)
    # Full redundant hub weights are computed independently from literal deficits.
    require(all(r[10]==r[0]+r[1]-r[8] for r in types),'row weighted/support identity')
    def marked(records):
        return sorted(({'fixture':s,'hub_high':list(m),'coordinates':list(r)} for s,m,r in records),
                      key=lambda r:(r['fixture'],r['hub_high']))
    branches=[]
    for cr in cases:
        case=cr['case'];t,x,tau,q,e,k,margin=case
        scalar={'T':t,'X':x,'tau':tau,'N5':0,'Q':q,'E':e,'K':k,'margin_budget':margin}
        rows=[]
        for actual,v,c in vectors:
            if actual==case:
                require(sum(v[i]*types[i][10] for i in range(len(types)))==19,'global actual hub weight')
                rows.append({'vector':v,'certificate':shape(case,types,v,c)})
        branches.append({'case':scalar,'rows':rows})
    return {'actual_marks':marked(raw),'conservative_marks':marked(capped),'types':types,
            'scalar_cases':[b['case'] for b in branches],'branches':branches,
            'ordered_column_calibration':{k:[{'N':n,'n':h,'D':d} for n,h,d in allocations(k)] for k in (12,13,14)}}

def check(expected,actual):
    require(canonical(actual)==canonical(expected),'whole entrywise independent comparison')

def main(target):
    expected=independent_core()
    for name in ('producer','oracle'):
        spec=importlib.util.spec_from_file_location('late_author_'+name,target/(name+'.py'))
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        actual,diagnostics=mod.build();check(expected,actual)
    damages=[]
    def reject(name,bad):
        try:check(expected,bad)
        except ValueError:damages.append(name);return
        raise ValueError('damaged author record accepted')
    bad=copy.deepcopy(actual);bad['actual_marks'].pop();reject('omitted literal marking',bad)
    bad=copy.deepcopy(actual);bad['actual_marks'][0]['hub_high']=[0];reject('wrong actual hub mark',bad)
    bad=copy.deepcopy(actual);bad['types'][0]=tuple([True]+list(bad['types'][0][1:]));reject('Boolean local charge',bad)
    nonempty=next(i for i,b in enumerate(actual['branches']) if b['rows'])
    bad=copy.deepcopy(actual);bad['branches'][nonempty]['rows'].pop();reject('omitted full vector',bad)
    bad=copy.deepcopy(actual);bad['branches'][nonempty]['rows'].append(copy.deepcopy(bad['branches'][nonempty]['rows'][0]));reject('duplicate full vector',bad)
    bad=copy.deepcopy(actual);bad['scalar_cases'].pop();reject('missing scalar case',bad)
    bad=copy.deepcopy(actual);bad['ordered_column_calibration'][14].pop();reject('omitted positive labelled allocation',bad)
    joint=next((i,j) for i,b in enumerate(actual['branches']) for j,r in enumerate(b['rows'])
               if r['certificate']['reason']=='DISJOINT_SINGLE_HUB_COLUMNS')
    bad=copy.deepcopy(actual);bad['branches'][joint[0]]['rows'][joint[1]]['certificate']['distinct_B_hubs']=False
    reject('dropped actual distinct-owner premise',bad)
    print(json.dumps({'complete_core_sha256':hashlib.sha256(canonical(expected)).hexdigest(),
                      'raw_marks':len(expected['actual_marks']),'capped_marks':len(expected['conservative_marks']),
                      'types':len(expected['types']),'cases':len(expected['scalar_cases']),
                      'vectors_and_all_certificate_fields':sum(len(b['rows']) for b in expected['branches']),
                      'all_named_allocations':sum(len(v) for v in expected['ordered_column_calibration'].values()),
                      'semantic_damages_rejected':damages,'both_author_engines_entire_records_match':True},sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('target',type=Path);main(p.parse_args().target.resolve())
