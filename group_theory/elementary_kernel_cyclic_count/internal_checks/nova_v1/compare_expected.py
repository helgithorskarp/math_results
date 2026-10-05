#!/usr/bin/env python3
"""Compare mathematical fields across the independent representations."""
import json
from pathlib import Path


def require(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    base=Path(__file__).resolve().parent
    original=json.loads((base/'ROWAN_EXPECTED.json').read_text())
    independent=json.loads((base/'RESULT.json').read_text())
    fields=['name','p','dimension','A_p','B_p','lower_bound','coprime_defect',
            'divisible_defect','equality','coprime_actions_all_trivial','divisible_cosets_all_long']
    group_fields=['order','cyclic_subgroups','eta','element_order_histogram','cyclic_subgroup_order_histogram']
    require(len(independent['fixtures'])==len(original['fixtures'])==22,'incomplete fixture coverage')
    for author,other in zip(original['fixtures'],independent['fixtures']):
        for field in fields:
            require(author[field]==other[field],f'{author["name"]}: {field} differs')
        for group in ('group','quotient'):
            for field in group_fields:
                require(author[group][field]==other[group][field],f'{author["name"]}: {group}.{field} differs')
    require(all(independent['negative_controls'].values()),'a malformed-data guard failed')
    require(set(independent['negative_controls'])=={r['name'] for r in original['negative_controls']},'negative cases differ')
    changed={r['name']:r for r in independent['changed_inputs']}
    require(changed['F3_cubed_Jordan_C3']['group']['cyclic_subgroups']==29,'nonzero norm-rank fixture differs')
    require(changed['F5_squared_faithful_scalar_C4']['group']['cyclic_subgroups']==57,'faithful scalar fixture differs')
    require(changed['F2_cubed_faithful_C7']['equality'] is True,'characteristic-two fixture differs')
    require(changed['F2_cubed_faithful_C7']['group']['cyclic_subgroups']==16,'characteristic-two count differs')
    require(changed['C121_over_C11']['group']['cyclic_subgroups']==3,'new prime fixture differs')
    summary=dict(status='ALL_22_MATHEMATICAL_OUTPUTS_MATCH',changed_inputs=4,negative_rejections=3,
                 scope='representation-dependent set/coset digests differ by design; affine norms checked directly in each independent coset')
    (base/'COMPARISON.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
