"""Semantic record damages, exact scope failures and actual point transports."""
import argparse
import copy
import json
from pathlib import Path
import verify

def rejected(call,label):
    try:
        call()
    except (ValueError,KeyError,TypeError):
        return label
    raise ValueError('Damaged object accepted: '+label)

def run(data,catalog,boundary):
    rows,_=verify.check_catalog(catalog,data)
    verify.check_boundaries(boundary,rows)
    controls=[]
    def damaged(label,edit):
        c=copy.deepcopy(catalog)
        edit(c)
        controls.append(rejected(lambda:verify.check_catalog(c,data),label))
    damaged('missing_last_mark',lambda c:c['rows'].pop())
    damaged('duplicate_mark_with_population_preserved',lambda c:c['rows'].__setitem__(1,copy.deepcopy(c['rows'][0])))
    damaged('missing_actual_e4_link_point_mark',lambda c:c['rows'].__delitem__(1))
    damaged('wrong_high_high_hub_charge',lambda c:c['rows'][0].__setitem__('q',c['rows'][0]['q']+1))
    damaged('wrong_eligibility',lambda c:c['rows'][0].__setitem__('eligible',not c['rows'][0]['eligible']))
    damaged('wrong_unit_neighbor_capacity',lambda c:c['rows'][0].__setitem__('g1_S',1))
    damaged('wrong_saturated_excess',lambda c:c['rows'][0].__setitem__('ss_excess',1))
    damaged('wrong_hub_deficit_weight',lambda c:c['rows'][0].__setitem__('hub_weight',1))
    damaged('wrong_psi_sign',lambda c:c['rows'][0].__setitem__('psi',1))
    damaged('wrong_account_consistent_margin',lambda c:(c['rows'][0].__setitem__('psi',1),c['rows'][0].__setitem__('margin',1-3*(c['rows'][0]['k']-c['rows'][0]['e']-c['rows'][0]['q']))))
    damaged('wrong_literal_hub_point',lambda c:c['rows'][0].__setitem__('hub_high',[0]))
    damaged('deleted_actual_five_hub_scope_failures',lambda c:c.__setitem__('rows',[r for r in c['rows'] if r['k']<5]))
    def offer_eligible_mixed_capacity(c):
        r=next(r for r in c['rows'] if r['e']==1 and r['eligible'] and r['g1_S'])
        r['psi']=-r['g1_S']
        r['margin']=r['psi']-3*(r['k']-r['e']-r['q'])
    damaged('eligible_mixed_wrongly_offers_capacity',offer_eligible_mixed_capacity)
    controls.append(rejected(lambda:verify.check_catalog(catalog,data,scope=5),'actual_five_hub_widening'))
    for label,edit in (
        ('missing_quadruple',lambda d:d['stars'][0].pop()),
        ('duplicated_quadruple',lambda d:d['stars'][0].__setitem__(1,copy.deepcopy(d['stars'][0][0]))),
        ('wrong_point',lambda d:d['stars'][0][0].__setitem__(0,17)),
        ('missing_fixture',lambda d:d['stars'].pop())):
        d=copy.deepcopy(data);edit(d)
        controls.append(rejected(lambda:verify.literal_rows(d),label))
    for label,edit in (
        ('deleted_unique_boundary_template',lambda b:b['branches'][2].__setitem__('templates',[])),
        ('changed_boundary_hub_charge',lambda b:b['branches'][2].__setitem__('Q',0)),
        ('even_nonunit_block_fabricated',lambda b:b['branches'][2]['templates'][0].__setitem__(2,10)),
        ('even_handshake_fabricated',lambda b:b['branches'][2]['parity'][0].__setitem__('degree_sum',32)),
        ('deleted_boundary_branch',lambda b:b['branches'].pop())):
        b=copy.deepcopy(boundary);edit(b)
        controls.append(rejected(lambda:verify.check_boundaries(b,rows),label))
    transports=[]
    for g in ([(p+1)%17 for p in range(17)],[16-p for p in range(17)],[(3*p+2)%17 for p in range(17)]):
        verify.require(sorted(g)==list(range(17)),'actual point bijection required')
        inverse=[g.index(p) for p in range(17)]
        relabeled=copy.deepcopy(data)
        relabeled['stars']=[[[g[p] for p in q] for q in star] for star in data['stars']]
        relabeled['groups']=[[[g[a[inverse[p]]] for p in range(17)] for a in group]
                             for group in data['groups']]
        images=verify.literal_rows(relabeled)
        for r in images:
            r['hub_high']=sorted(inverse[p] for p in r['hub_high'])
        images.sort(key=lambda r:(r['fixture'],r['hub_high']))
        verify.require(images==rows,'actual transported row objects differ')
        verify.require(verify.iterative_boundaries(images)==boundary,'transported category proof differs')
        transports.append(dict(point_map=g,actual_stars=23,actual_marked_rows=len(images)))
    return dict(status='PASS_SEMANTIC_DAMAGES_SCOPE_COUNTEREXAMPLES_AND_ACTUAL_TRANSPORTS',
        rejected_count=len(controls),rejected_labels=controls,actual_relabelings=len(transports),
        actual_transported_stars=23*len(transports),actual_transported_marked_rows=len(rows)*len(transports))

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--fixtures',type=Path,default=Path(__file__).with_name('fixtures.json'))
    p.add_argument('--primary',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=run(json.loads(a.fixtures.read_text()),json.loads((a.primary/'catalog.json').read_text()),
               json.loads((a.primary/'boundaries.json').read_text()))
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    main()
