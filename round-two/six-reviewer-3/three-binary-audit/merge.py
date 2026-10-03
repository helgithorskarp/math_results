"""Disjoint complete slice combination; no expected fixture is a proof input."""
import json,sys
from pathlib import Path
from collections import Counter
from engine import digest,require

def merge(root):
    root=Path(root);parts=[json.loads((root/f'audit-{s}.json').read_text()) for s in range(0,1042,128)]
    require([p['slice'] for p in parts]==[[s,min(s+128,1042)] for s in range(0,1042,128)],'function slice partition')
    x={'scope':parts[0]['scope'],'census':parts[0]['census'],'live_heads':sum(p['live_heads'] for p in parts),'freed_tail_alternatives':sum(p['freed_tail_alternatives'] for p in parts),'numerical_bindings':sum(p['numerical_bindings'] for p in parts),'actual_bindings':sum((p['actual_bindings'] for p in parts),[]),'early':parts[0]['early'],'full_case_cover_sha256':parts[0]['full_case_cover_sha256']};ct=Counter();dom=set();use=Counter();first={};cubes={}
    for p in parts:
        require(p['census']==x['census'] and p['early']==x['early'],'part background')
        ct.update(p['binding_kinds']);dom.update(map(tuple,p['original_domains']));use.update(dict(p['witness_uses']))
        for f in p['scalar_first_witnesses']:first.setdefault(f['index'],f)
        for c in p['physical_cubes']:
            k=(tuple(map(tuple,c['word'])),c['low'],c['high']);require(k not in cubes or cubes[k]==c,'cube inconsistency');cubes[k]=c
    require(set(use)==set(range(136)),'witness instances');x.update(binding_kinds=dict(ct),original_domains=sorted(dom),witness_uses=sorted(use.items()),scalar_first_witnesses=[first[i] for i in sorted(first)],physical_cubes=[cubes[k] for k in sorted(cubes)])
    return x

def summary(root):
    root=Path(root);primary=json.loads((root/'primary.json').read_text());cover=json.loads((root/'cover.json').read_text());controls=json.loads((root/'controls.json').read_text());scalar={}
    for kind,total in [('base',442),('cubes',len(primary['physical_cubes']))]:
        ps=[json.loads((root/f'scalar-{kind}-{s}.json').read_text()) for s in range(0,total,128)]
        require([p['slice'] for p in ps]==[[s,min(s+128,total)] for s in range(0,total,128)],'scalar domain partition')
        products=sum((p['products'] for p in ps),[]);scalar[kind]={'cubes':len(products),'assignments':sum(p['assignments'] for p in ps),'products_sha256':digest(products),'chunk_sha256':[digest(p) for p in ps]}
    return {'whole_cover_sha256':digest(cover),'whole_primary_sha256':digest(primary),'whole_controls_sha256':digest(controls),'whole_scalar':scalar,'census':cover['census'],'live_heads':primary['live_heads'],'freed_tail_alternatives':primary['freed_tail_alternatives'],'actual_bindings':primary['numerical_bindings'],'kind_census':primary['binding_kinds'],'domains':len(primary['original_domains']),'unique_whole_binding_cubes':len(primary['physical_cubes']),'semantic_damages':len(controls['rejected_semantic_damages']),'early_scalar_assignments':sum(c['rows'] for c in controls['early_full_scalar_cubes']),'known45_Boolean_rows':controls['known45_rows'],'unclamped_Q_scalar_rows':controls['unclamped_Q_rows']}
if __name__=='__main__':
    x=merge(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(x,separators=(',',':'),sort_keys=True)+'\n');print(digest(x))
