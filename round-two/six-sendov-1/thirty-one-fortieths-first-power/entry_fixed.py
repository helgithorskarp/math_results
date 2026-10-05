"""Fresh fixed full entry replay, independent of every discovery corpus."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util,json
HERE=Path(__file__).resolve().parent
def unique(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError('duplicate JSON key')
        out[key]=value
    return out
s=importlib.util.spec_from_file_location('fresh_thirty_one_fixed_entry',HERE/'core.py')
k=importlib.util.module_from_spec(s);s.loader.exec_module(k)
c=json.loads((HERE/'ENTRY_COVER.json').read_text(),object_pairs_hook=unique)
k.require(set(c)=={'interval','energy','target','TM','initial_shells','splits','leaves'},
          'whole fixed entry schema')
k.require(c['interval']==['3/4','31/40'] and c['energy']=='51/10'
          and c['target']=='2199/2200' and c['TM']=='53816/5041','all new fixed budgets')
shells=[dict(index=i,rectangle=k.strings([k.LOW,k.H,Q(i,8),min(k.TM,Q(i+1,8))])) for i in range(86)]
k.typed_equal(c['initial_shells'],shells,'entire initial86 closed shells')
splits,leaves=c['splits'],c['leaves'];seen=set();cuts=[];pays=[]
k.require(type(splits) is dict and type(leaves) is list and len(leaves)==len(set(leaves))
          and set(splits).isdisjoint(leaves),'all entry node types and uniqueness')
def coord(x):
    k.require(type(x) is str and str(Q(x))==x,'whole canonical exact coordinate');return Q(x)
def walk(index,path,box):
    key=str(index)+':'+path
    k.require(key not in seen and len(path)<=12,'unique bounded fixed entry node');seen.add(key)
    al,ah,tl,th=box
    k.require(k.LOW<=al<ah<=k.H and 0<=tl<th<=k.TM,'complete fixed closed rectangle')
    if key in splits:
        t=splits[key]
        k.require(type(t) is dict and set(t)=={'axis','cut'} and type(t['axis']) is int
                  and t['axis'] in (0,1),'whole cut schema')
        axis,cut=t['axis'],coord(t['cut'])
        k.require(box[2*axis]<cut<box[2*axis+1],'strict fixed interior cut')
        a,b=box.copy(),box.copy();a[2*axis+1]=cut;b[2*axis]=cut
        k.require(a[2*axis+1]==b[2*axis] and all(a[j]==b[j]==box[j]
                  for j in range(4) if j not in (2*axis,2*axis+1)),
                  'both whole closed children meet and retain coordinates')
        cuts.append(dict(key=key,parent=box,axis=axis,cut=cut))
        walk(index,path+'0',a);walk(index,path+'1',b);return
    k.require(key in leaves,'every fixed terminal declared')
    pay=k.polar_payment(al,ah,tl,th,Q(8),max(Q(0),(k.ENERGY-th)/2),key,'')
    margin=Q(c['target'])-Q(pay['integral'])
    k.require(margin>0,'every full fixed exact entry payment meets target')
    pays.append(dict(key=key,rectangle=box,whole_payment=pay,exact_margin=margin))
for shell in shells:walk(shell['index'],'',list(map(coord,shell['rectangle'])))
k.require(seen==set(splits)|set(leaves) and len(cuts)==304 and len(pays)==390
          and len(seen)==694,'all86 roots/304 cuts/390 leaves/694 nodes reached')
out=dict(agent='six-sendov-1',role='researcher',status='ALL_FIXED_CLOSED_ENTRY_ESTIMATES_PASS',
    interval=[k.LOW,k.H],energy=k.ENERGY,target=Q(c['target']),radial_ceiling=k.TM,
    entire_initial_shells=shells,all304_closed_cut_payments=cuts,
    all390_whole_leaf_payments=pays,exact_smallest_margin=min(p['exact_margin'] for p in pays),
    maximum_selected_path_depth=max(len(p['key'].split(':',1)[1]) for p in pays),
    source_hashes={n:sha256((HERE/n).read_bytes()).hexdigest() for n in
                   ('core.py','origin.py','ENTRY_COVER.json','entry_fixed.py')},
    no_runtime_discovery_corpus_or_ancestor_numeric_input=True,
    annular_theorem_proved=False,fresh_face_paid=False,formalized=False,
    independently_reviewed=False,mathematical_nonexistence_claimed=False)
print(json.dumps(k.clean(out),sort_keys=True,separators=(',',':')))
