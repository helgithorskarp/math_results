"""Three fixed shards reconstruct the WHOLE closed cover and pay their full leaves.

Runtime inputs are compact geometry and local analytic kernels only. Discovery
records, previous payments and point diagnostics are never imported or read.
"""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util,json
HERE=Path(__file__).resolve().parent
def module(name):
    s=importlib.util.spec_from_file_location('fixed_energy51_face_'+name,HERE/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
k=module('core');product=module('product')
OM=Q(1,3100);JM=Q(1,2200)

def run(batch):
    k.require(type(batch) is int and 0<=batch<3,'three fixed exact face shards')
    c=json.loads((HERE/'FACE_COVER.json').read_text());root=list(map(Q,c['root']))
    k.require(set(c)=={'root','splits','leaves'} and
              root==[k.LOW,k.H,Q(0),Q(51,10),Q(109,160),Q(1),Q(0),Q(13719,25600)]
              and k.ENERGY==Q(51,10) and k.GAMMA==Q(109,160) and k.MASS==8,
              'exact new mass8 closed root')
    splits,leaves=c['splits'],c['leaves'];seen=set();cuts=[];boxes={}
    roles={'retained-mean-product-origin','joint-energy-polar','standard-polar'}
    k.require(set(splits).isdisjoint(leaves),'disjoint node classes')
    def walk(path,box):
        k.require(path not in seen and all(root[2*j]<=box[2*j]<box[2*j+1]<=root[2*j+1]
                    for j in range(4)),'unique whole enclosed node')
        seen.add(path)
        if path in splits:
            t=splits[path];axis=t['axis'];cut=Q(t['cut'])
            k.require(set(t)=={'axis','cut'} and type(axis) is int and 0<=axis<4 and
                      str(cut)==t['cut'] and box[2*axis]<cut<box[2*axis+1],
                      'canonical strict whole face cut')
            a,b=box.copy(),box.copy();a[2*axis+1]=cut;b[2*axis]=cut
            k.require(a[2*axis+1]==b[2*axis] and all(a[j]==b[j]==box[j] for j in range(8)
                        if j not in (2*axis,2*axis+1)),'both full closed children meet')
            cuts.append(dict(path=path,parent=box,axis=axis,cut=cut))
            walk(path+'0',a);walk(path+'1',b)
        else:
            k.require(path in leaves and leaves[path] in roles,'all explicit analytic leaves declared')
            boxes[path]=box
    walk('',root)
    k.require(seen==set(splits)|set(leaves) and len(leaves)==450 and len(splits)==449,
              'whole449-cut450-leaf census, no orphans')
    paths=sorted(boxes);chosen=paths[150*batch:150*(batch+1)]
    k.require(len(chosen)==150,'all three disjoint consecutive150-leaf shards')
    constants,derivations=k.centered_constants('');rows=[]
    for path in chosen:
        box=boxes[path];face=box[:4]+[Q(8),Q(8)]+box[4:];enc=k.enclose(face,'')
        k.require(enc['status']=='nonempty-enclosure','no unlicensed empty leaf')
        tight,T=enc['tightened'],enc['T'];role=leaves[path]
        row=dict(path=path,box=box,face_box=face,enclosure=enc,role=role)
        if role=='retained-mean-product-origin':
            prod=product.payment(k,tight,T);cap=Q(prod['actual_origin_product_upper'])
            attempts=[k.origin.payment(tight+T,ch) for ch in ('energy','joint')]
            k.require(0<cap<=1 and all(x['status']=='bounded' for x in attempts),
                      'both complete mean channels and actual product paid')
            lower=max(x['score'] for x in attempts);margin=lower-cap-OM
            k.require(margin>0,'strict entire origin-product leaf surplus')
            row.update(product=prod,both_mean_channels=attempts,origin_lower=lower,
                       actual_product_cap=cap,margin=margin)
        else:
            al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,T)
            if role=='standard-polar':
                polar=k.polar_payment(al,ah,tl,th,fh,max(Q(0),fl-8*uh),path,'')
                upper=Q(polar['integral']);row['polar']=polar
            else:
                dh=k.ceiling(th/56,4096)
                k.require(el/2-28*dh**2>=0 and al+1-al**2-ah-(1-ah**2)*dh>0,
                          'whole joint phase and chord signs')
                polar=k.energy_payment(path,tight,T,'');upper=Q(polar['integral_upper'])
                row.update(joint_phase_minimum=el/2-28*dh**2,polar=polar)
            margin=1-JM-upper;k.require(margin>0,'strict entire polar leaf surplus')
            row.update(polar_upper=upper,margin=margin)
        rows.append(row)
    out=dict(agent='six-sendov-1',role='researcher',status='ALL_FIXED_SHARD_LEAVES_PAID',
             batch=batch,shard_count=3,root=root,all449_closed_cut_payments=cuts,
             all450_leaf_geometry=boxes,all450_paths=paths,selected150_paths=chosen,
             all150_full_leaf_payments=rows,minimum_exact_margin=min(x['margin'] for x in rows),
             centered_constants=constants,all_centered_derivations=derivations,
             no_discovery_or_prior_numerical_runtime_inputs=True,
             source_hashes={n:sha256((HERE/n).read_bytes()).hexdigest() for n in
                 ('core.py','origin.py','product.py','face_fixed.py','FACE_COVER.json',
                  'face_fixed_'+str(batch).zfill(2)+'.py')},
             formalized=False,independently_reviewed=False,annular_proof_bridge_still_required=True)
    print(json.dumps(k.clean(out),sort_keys=True,separators=(',',':')))
