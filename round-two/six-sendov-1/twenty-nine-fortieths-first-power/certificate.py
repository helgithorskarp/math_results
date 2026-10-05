"""Standalone CLOSED[7/10,29/40] exact certificate kernels.
Own c1cf4584119f20ac6c6447541429eaa6717e48de method provenance; no ancestor, peer, reviewer or discovery corpus runtime input.
Unformalized and independently unreviewed; ordinary proof/trust in PROOF.md.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
import argparse,hashlib,importlib.util,json,resource,time

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def unique(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'duplicate JSON key');out[key]=value
    return out

def local(name):
    spec=importlib.util.spec_from_file_location('combined_twenty_nine_private_'+name,HERE/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def read(name):return json.loads((HERE/name).read_text(),object_pairs_hook=unique)


def read_path(path):
    return json.loads(path.read_text(),object_pairs_hook=unique)

def canonical_q(text):
    need(type(text) is str and str(Q(text))==text,'canonical rational coordinate')
    return Q(text)

def face_schema(cover):
    need(type(cover) is dict and set(cover)=={'root','splits','leaves'},'exact face cover schema')
    root=list(map(canonical_q,cover['root']))
    need(root==list(map(Q,['7/10','29/40','0','23/5','51/80','1','0','23/40'])),
         'exact face root value')
    splits,leaves=cover['splits'],cover['leaves']
    need(type(splits) is dict and type(leaves) is dict,'face dictionary types')
    need(all(type(path) is str and set(path)<={'0','1'} and len(path)<=43 and
        type(obj) is dict and set(obj)=={'axis','cut'} and type(obj['axis']) is int
        and 0<=obj['axis']<4 and type(obj['cut']) is str for path,obj in splits.items()),
        'exact face cut path/axis/rational types')
    roles={'retained-mean-product-origin','joint-energy-polar','standard-polar'}
    need(all(type(path) is str and set(path)<={'0','1'} and len(path)<=43 and
        type(role) is str and role in roles for path,role in leaves.items()),'exact face leaf types')
    need(set(splits).isdisjoint(leaves),'face internal/leaf disjointness')
    seen=set()
    def walk(path,box):
        need(path not in seen,'unique face node');seen.add(path)
        if path in splits:
            axis=splits[path]['axis'];cut=canonical_q(splits[path]['cut'])
            need(box[2*axis]<cut<box[2*axis+1],'strict face interior cut')
            a,b=box.copy(),box.copy();a[2*axis+1]=cut;b[2*axis]=cut
            walk(path+'0',a);walk(path+'1',b)
        else:need(path in leaves,'missing closed face leaf')
    walk('',root)
    need(seen==set(splits)|set(leaves),'all face entries reached')
    need(len(splits)==328 and len(leaves)==329 and len(seen)==657,'whole fixed face census')

def entry_schema(ec):
    keys={'interval','energy','target','TM','initial_shells','splits','leaves'}
    need(type(ec) is dict and set(ec)==keys,'exact entry cover schema')
    expected=dict(interval=['7/10','29/40'],energy='23/5',target='2199/2200',TM='47096/4761')
    need(all(type(ec[key]) is type(value) and ec[key]==value for key,value in expected.items()),
         'exact entry marked/energy/target/radial budgets')
    shells=[dict(index=i,rectangle=['7/10','29/40',str(Q(i,8)),str(min(Q(47096,4761),Q(i+1,8)))])
            for i in range(80)]
    need(type(ec['initial_shells']) is list and len(ec['initial_shells'])==80,
         'complete80 initial entry shells')
    for got,want in zip(ec['initial_shells'],shells):
        need(type(got) is dict and set(got)==set(want) and type(got['index']) is int
             and got==want,'whole ordered closed initial entry shell')
    splits,leaves=ec['splits'],ec['leaves']
    need(type(splits) is dict and type(leaves) is list and len(leaves)==len(set(leaves))
         and all(type(key) is str for key in leaves),'entry container types/unique leaves')
    need(set(splits).isdisjoint(leaves),'entry internal/leaf disjointness')
    seen=set()
    def walk(index,path,box):
        key=str(index)+':'+path
        need(key not in seen and len(path)<=4,'unique bounded entry node');seen.add(key)
        if key in splits:
            spec=splits[key]
            need(type(spec) is dict and set(spec)=={'axis','cut'} and type(spec['axis']) is int
                 and spec['axis'] in (0,1),'whole entry split schema')
            axis=spec['axis'];cut=canonical_q(spec['cut'])
            need(box[2*axis]<cut<box[2*axis+1],'strict entry interior cut')
            a,b=box.copy(),box.copy();a[2*axis+1]=cut;b[2*axis]=cut
            walk(index,path+'0',a);walk(index,path+'1',b)
        else:need(key in leaves,'missing closed entry leaf')
    for shell in shells:walk(shell['index'],'',list(map(Q,shell['rectangle'])))
    need(seen==set(splits)|set(leaves),'all entry entries reached')
    need(len(splits)==154 and len(leaves)==234 and len(seen)==388,'whole fixed entry census')

def run(damage='',cover_path=None,entry_path=None):
    k=local('core');product=local('product');coupled=local('coupled')
    need((k.LOW,k.H)==(Q(7,10),Q(29,40)),'whole fixed adjacent interval')
    need(k.C==k.LOW+1-k.LOW**2-k.H and k.BM==1-k.H**2 and k.BX==1-k.LOW**2
         and k.AB==min(k.LOW*(1-k.LOW**2),k.H*(1-k.H**2))
         and k.TM==56*(1-1/(1+k.H))**2,'whole fresh marked budgets')
    target=Q(2199,2200);omargin=Q(1,3100);jmargin=Q(1,2200)
    constants,constant_rows=k.centered_constants(damage)
    need(constants[2:]==list(map(Q,['1/2','151/512','3/16','5/64','1/54','13/4096','1/4096'])),
         'ALL seven proved centered constants')
    mass=k.power([k.H,k.C*k.MASS/8],8)
    need(mass==[comb(8,i)*k.H**(8-i)*(k.C*k.MASS/8)**i for i in range(9)],
         'ALL9 scalar entry coefficients')
    slope=k.C*k.MASS/8;area=k.integral(mass)
    need(area==((k.H+slope)**9-k.H**9)/(9*slope),'fresh whole unused scalar antiderivative identity')
    # F is EXACTLY8 by homothety or clipping. This old conservative scalar
    # F<=37/5 test is NOT an entry premise; all234 actual entry rectangles
    # below pay their own full polar estimates. Retain its actual failed
    # inequality as non-input evidence, never silently loosen a needed gate.
    ec=read_path(entry_path or HERE/'ENTRY_COVER.json')
    entry_schema(ec)
    need(set(ec)=={'interval','energy','target','TM','initial_shells','splits','leaves'}
         and ec['interval']==k.strings([k.LOW,k.H]) and Q(ec['energy'])==k.ENERGY
         and Q(ec['target'])==target and Q(ec['TM'])==k.TM,'complete fixed entry schema')
    es,el=ec['splits'],ec['leaves'];need(len(el)==len(set(el)),'unique entry leaves')
    expected_shells=[dict(index=i,rectangle=k.strings([k.LOW,k.H,Q(i,8),min(k.TM,Q(i+1,8))]))
                     for i in range((8*k.TM).__ceil__())]
    need(ec['initial_shells']==expected_shells,'all80 closed ordered initial shells')
    eseen=set();epays=[];ecut=[]
    def entry_walk(index,path,rect):
        key=str(index)+':'+path;need(key not in eseen and len(path)<=4,'bounded unique entry node')
        eseen.add(key);al,ah,tl,th=rect
        need(k.LOW<=al<=ah<=k.H and 0<=tl<th<=k.TM,'whole closed entry containment')
        if key in es:
            spec=es[key];need(set(spec)=={'axis','cut'} and type(spec['axis']) is int
                             and spec['axis'] in (0,1),'whole entry split schema')
            axis=spec['axis'];cut=Q(spec['cut'])
            need(str(cut)==spec['cut'] and rect[2*axis]<cut<rect[2*axis+1],'canonical entry cut')
            a,b=rect.copy(),rect.copy();a[2*axis+1]=cut;b[2*axis]=cut
            need(a[2*axis+1]==b[2*axis] and all(a[i]==b[i]==rect[i]
                 for i in range(4) if i not in (2*axis,2*axis+1)),'both whole closed entry children')
            ecut.append(dict(key=key,rectangle=rect,axis=axis,cut=cut))
            entry_walk(index,path+'0',a);entry_walk(index,path+'1',b);return
        need(key in el,'one paid entry leaf per terminal node')
        pay=k.polar_payment(al,ah,tl,th,Q(8),max(Q(0),(k.ENERGY-th)/2),key,damage)
        need(Q(pay['integral'])<target,'whole noncircular entry paid '+key)
        epays.append(dict(key=key,rectangle=rect,payment=pay))
    for shell in expected_shells:entry_walk(shell['index'],'',list(map(Q,shell['rectangle'])))
    need(eseen==set(es)|set(el) and len(es)==154 and len(epays)==234,'complete388-node entry census')
    cover=read_path(cover_path or HERE/'COVER.json');face_schema(cover);need(set(cover)=={'root','splits','leaves'},'whole face schema')
    root=list(map(Q,cover['root']))
    need(root==[k.LOW,k.H,Q(0),k.ENERGY,k.GAMMA,Q(1),Q(0),k.ENERGY/8],
         'complete closed face-root')
    need(k.GAMMA==k.MASS/8-k.ENERGY/16 and Q(8)>=k.MASS,'licensed conservative face mean floor')
    fs,fl=cover['splits'],cover['leaves'];seen=set();cuts=[];rows=[]
    def face_walk(path,box):
        need(path not in seen and len(path)<=43,'bounded unique face node');seen.add(path)
        need(all(root[2*j]<=box[2*j]<box[2*j+1]<=root[2*j+1] for j in range(4)),
             'all closed face containment')
        if path in fs:
            spec=fs[path];need(set(spec)=={'axis','cut'} and type(spec['axis']) is int
                             and 0<=spec['axis']<4,'whole face cut schema')
            axis=spec['axis'];cut=Q(spec['cut'])
            need(str(cut)==spec['cut'] and box[2*axis]<cut<box[2*axis+1],'canonical interior face cut')
            a,b=box.copy(),box.copy();a[2*axis+1]=cut;b[2*axis]=cut
            need(a[2*axis+1]==b[2*axis] and all(a[i]==b[i]==box[i]
                 for i in range(8) if i not in (2*axis,2*axis+1)),'both whole closed face children')
            cuts.append(dict(path=path,box=box,axis=axis,cut=cut))
            face_walk(path+'0',a);face_walk(path+'1',b);return
        need(path in fl,'face terminal label exists');role=fl[path]
        face=box[:4]+[Q(8),Q(8)]+box[4:];enc=k.enclose(face,damage)
        need(enc['status']=='nonempty-enclosure','no failed gate used as nonexistence')
        tight,T=enc['tightened'],enc['T'];prod=product.payment(k,tight,T,damage);cap=Q(prod['actual_origin_product_upper'])
        need(0<cap<=1,'whole positive actual origin product cap')
        row=dict(path=path,box=box,face_box=face,role=role,enclosure=enc,product=prod)
        if role=='retained-mean-product-origin':
            attempts=[k.origin.payment(tight+T,channel,damage) for channel in ('energy','joint')]
            need(all(x['status']=='bounded' for x in attempts),'BOTH whole selected mean channels bounded')
            best=max(x['score'] for x in attempts)
            need(best-cap>omargin and 3100*(best.numerator*cap.denominator-cap.numerator*best.denominator)
                 >best.denominator*cap.denominator,'whole strict origin margin, two exact representations')
            row.update(both_mean_channels=attempts,best_origin=best,origin_margin=best-cap)
        elif role in ('standard-polar','joint-energy-polar'):
            al,ah,el,eh,ff,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,T)
            if role=='joint-energy-polar':
                pay=k.energy_payment(path,tight,T,{'ET-last-bivariate-coefficient':'last-bivariate-coefficient','ET-last-Bernstein-control':'last-Bernstein-control'}.get(damage,damage));upper=Q(pay['integral_upper'])
            else:
                pay=k.polar_payment(al,ah,tl,th,fh,max(Q(0),ff-8*uh),path,damage);upper=Q(pay['integral'])
            need(1-upper>jmargin and 2200*upper.numerator<2199*upper.denominator,
                 'whole strict polar margin, two exact representations')
            row.update(polar_payment=pay,upper=upper,polar_margin=1-upper)
        else:raise ValueError('explicit actual selected face role')
        rows.append(row)
    face_walk('',root)
    need(seen==set(fs)|set(fl) and len(cuts)==328 and len(rows)==329 and len(seen)==657,
         'complete fixed closed face coverage')
    roles={x:sum(r['role']==x for r in rows) for x in sorted(set(fl.values()))}
    need(roles=={'retained-mean-product-origin': 273, 'joint-energy-polar': 54, 'standard-polar': 2},
         'all selected face roles')
    continuity=coupled.payment(damage)
    need(continuity['epsilon']==Q(1,10000) and continuity['origin_margin']==omargin
         and continuity['polar_margin']==jmargin and continuity['entry_target']==target,
         'fresh clipping payments cover every face and entry target')
    conditional=local('check_origin').compute()
    literal=local('literal');endpoints={str(a):literal.compute(endpoint=a) for a in (k.LOW,k.H)}
    affine=local('homothety').compute()
    return k.clean(dict(agent='six-sendov-1',role='researcher',status='COMPLETE LOCAL FIXED MATHEMATICAL CERTIFICATE',
        interval=[k.LOW,k.H],gap=Q(1,10000),constants=constants,constant_derivations=constant_rows,
        entry_cover=ec,entry_scalar_coefficients=mass,entry_scalar_integral=area,
        unused_scalar_floor_target_met=area<target,
        unused_scalar_floor_is_not_an_entry_premise=True,
        entry_mass_is_exactly_eight=True,
        all_entry_cut_payments=ecut,all_entry_leaf_payments=epays,cover=cover,
        all_face_cut_payments=cuts,all_face_leaf_payments=rows,role_counts=roles,
        fresh_continuity=continuity,conditional_controls=conditional,
        both_endpoint_literal_controls=endpoints,homothety_controls=affine,
        no_ancestor_private_or_reviewer_runtime_input=True,contour_prior_art_credited=True,
        ordinary_continuum_proof_supplied=True,
        no_parent_numeric_exclusion_input=True,formalized=False,independently_reviewed=False))
