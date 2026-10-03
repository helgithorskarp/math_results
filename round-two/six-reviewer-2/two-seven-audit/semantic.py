"""Full typed comparisons and concrete altered-evidence controls.

Fresh paired arithmetic, never a hash, is the mathematical comparator. These
controls are interfaces, not a third arithmetic kernel or formal proof.
"""
import copy,json

def need(ok,why):
    if not ok:raise ValueError(why)

def equal(a,b,path=()):
    if type(a)is not type(b):raise ValueError('exact type differs at '+str(path))
    if type(a)is dict:
        if a.keys()!=b.keys():raise ValueError('complete keys differ at '+str(path))
        for k in a:equal(a[k],b[k],path+(k,))
    elif type(a)is list:
        if len(a)!=len(b):raise ValueError('complete lengths differ at '+str(path))
        for i,(x,y)in enumerate(zip(a,b)):equal(x,y,path+(i,))
    elif a!=b:raise ValueError('value differs at '+str(path))

def strict_read(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON key');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError('nonfinite JSON')))

def controls(records):
    results=[]
    def reject(name,key,edit):
        bad=copy.deepcopy(records[key]);edit(bad)
        try:equal(records[key],bad)
        except ValueError:results.append(name)
        else:raise ValueError('bad evidence accepted: '+name)
    reject('drop original inventory','inventory37',lambda x:x['inventories'].pop())
    reject('Q96 unavailable','inventory03',lambda x:x['mode_independent_domain'].__setitem__('Q96_available',False))
    reject('spent original48 returned to H','inventory37',lambda x:x['inventories'][0]['H'].append(3))
    reject('cross-type cofactor wrongly forbidden','inventory03',lambda x:x['mode_independent_domain'].__setitem__('cross_type_equal_cofactors_allowed',False))
    reject('proper-divisor actual LCM removed','inventory03',lambda x:x['mode_independent_domain'].__setitem__('actual_LCM_proper_divisor_allowed',False))
    reject('unproductive selected originals removed','inventory03',lambda x:x['mode_independent_domain'].__setitem__('selected_unproductive_tails_allowed',False))
    reject('essential16_32 requirement dropped','inventory03',lambda x:x['mode_independent_domain'].__setitem__('essential16_32_required',False))
    reject('outside budget perturbed','shadows',lambda x:x['rows'][0].__setitem__('budget',4))
    reject('original BASE phase omitted','shadows',lambda x:x['rows'][0]['all_original_phases'][0]['all_phases'].pop())
    reject('literal CRT endpoint omitted','geometry',lambda x:x['CRT_products'][0]['literal_points'].pop())
    reject('physical lift bit changed','geometry',lambda x:x['all_original_phase_rows'][0]['all_four_quarter_masks'].__setitem__(0,0))
    reject('original quarter conjunction changed','geometry',lambda x:x['quarter_truth_table'][-1].__setitem__('all_quarters_filled',False))
    reject('physical role omitted','branches',lambda x:x['all_physical_roles'].pop())
    reject('one coupled branch case omitted','branches',lambda x:next(r for r in x['all_physical_roles']if r['status']=='BRANCH_CHECKED')['cases'].pop())
    def merge_branch(x):
        r=next(r for r in x['all_physical_roles']if r['status']=='BRANCH_CHECKED')
        r['cases'][0]['projected'][1]['branch']=0
    reject('original mod3 branches merged','branches',merge_branch)
    def collapse(x):
        for r in x['all_physical_roles']:
            for c in r.get('cases',[]):
                for p in c['projected']:
                    v=p['upper_multiset']
                    if len(v)!=len(set(v)):p['upper_multiset']=sorted(set(v));return
        raise ValueError('no repeated-row damage found')
    reject('repeated projected LCM rows collapsed','branches',collapse)
    reject('17 new improvement inventories omitted','improvement',lambda x:x['all_selected_inventories'].pop())
    reject('improvement bound changed','improvement',lambda x:x['summary'].__setitem__('maximum_refined_inventory',83))
    reject('integer confused with Boolean','inventory03',lambda x:x['summary'][0].__setitem__('h',False))
    reject('integer confused with float','inventory03',lambda x:x['summary'][0].__setitem__('h',0.0))
    reject('unknown JSON field','geometry',lambda x:x.__setitem__('extra',0))
    for name,raw in(('duplicate keys',b'{"a":1,"a":2}'),('nonfinite literal',b'{"a":NaN}')):
        try:strict_read(raw)
        except ValueError:results.append(name)
        else:raise ValueError('bad JSON accepted')
    positives=[]
    for key in records:equal(records[key],copy.deepcopy(records[key]));positives.append('whole valid '+key)
    return {'negative':results,'positive':positives,'fresh_exact_data_before_pin_gate':True}
