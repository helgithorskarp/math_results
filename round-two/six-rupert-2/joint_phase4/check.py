#!/usr/bin/env python3
"""Exact fresh joint-form audit / leaf replay; partial replay is not a theorem."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, json, sys, time
import forms as j
c,a,Q=j.c,j.a,j.Q

def enc_matrix(A):return [[c.enc(x) for x in row] for row in A]

def evaluate_receiver(matrices,t):
    if len(matrices)==1:return matrices[0]
    factors=[t[i]*t[i] for i in range(3)]+[2*t[i]*t[k] for i,k in j.PAIRS]
    return j.add(*(j.scale(A,x) for A,x in zip(matrices,factors)))

def reference_source_coefficients(A,depth,code):
    # Independent values-to-Bernstein conversion, not the moment construction.
    lo,hi=j.source_box(depth,code)
    out={idx:j.qform(A,(Q(1),*(Q(lo[k]+(hi[k]-lo[k])*F(idx[k],2)) for k in range(3)))) for idx in product(range(3),repeat=3)}
    for axis in range(3):
        old=out.copy()
        for idx in list(out):
            if idx[axis]!=1:continue
            l=list(idx);h=list(idx);l[axis]=0;h[axis]=2
            out[idx]=2*old[idx]-(old[tuple(l)]+old[tuple(h)])/2
    return [out[idx] for idx in product(range(3),repeat=3)]

def layer_record():
    start=time.monotonic(); f=j.ExactForms(); stream=[]; forces=[]; weights=[]
    for ci,rec in enumerate(j.STRESSES):
        ids=rec['indices']; ws=[[a.dot(v,r) for v in rec['weight_vectors']] for r in j.RAWS]
        c.require(all(v>=0 for row in ws for v in row) and all(sum(row,Q())>0 for row in ws),'nonnegative actual stress, positive closed corner total')
        weights.extend(v for row in ws for v in row)
        ms=[[a.cross(j.E[e],r) for e in ids] for r in j.RAWS]
        for i,k in ((0,0),(1,1),(2,2),*j.PAIRS):
            force=tuple(sum(((ws[i][z]*ms[k][z][axis]+ws[k][z]*ms[i][z][axis])/2 for z in range(len(ids))),Q()) for axis in range(3))
            c.require(force==c.Z,'entire original three-spatial-force equilibrium')
            forces.extend(force)
    receiver_ts=[tuple(Q(int(i==k)) for i in range(3)) for k in range(3)]+[tuple(Q(int(i in pair)) for i in range(3)) for pair in j.PAIRS]
    sources=[(Q(),Q(),Q())]+[tuple(Q(sign*int(k==axis)) for k in range(3)) for axis in range(3) for sign in (-1,1)]+[tuple(Q(int(k in pair)) for k in range(3)) for pair in j.PAIRS]
    literal_cuts=0
    chosen=tuple(dict.fromkeys((0,1,2,3,4,5,len(j.STRESSES)//2,len(j.STRESSES)-1)))
    for ci in chosen:
        ids=j.STRESSES[ci]['indices']; ks=tuple((11*e+7*ci+3)%60 for e in ids)
        matrices=f.cut(ci,ks)
        for t in receiver_ts:
            r=tuple(sum((t[k]*j.RAWS[k][axis] for k in range(3)),Q()) for axis in range(3))
            A=evaluate_receiver(matrices,t)
            for src in sources:
                z=(Q(1),*src); actual=j.literal_cut(ci,ks,r,z);wanted=j.qform(A,z)
                c.require(actual==wanted,'literal original world-quaternion/spatial physical cut including elevated opposite pairs')
                stream.append(['C',ci,list(ks),[c.enc(v) for v in t],[c.enc(v) for v in src],c.enc(actual)]);literal_cuts+=1
    literal_holes=0;literal_gauges=0
    for t in receiver_ts:
        r=tuple(sum((t[k]*j.RAWS[k][axis] for k in range(3)),Q()) for axis in range(3));r2=a.dot(r,r)
        Mn=tuple(tuple(c.I[i][k]-2*r[i]*r[k]/r2 for k in range(3)) for i in range(3))
        for src in sources:
            z=(Q(1),*src);Rh=j.rotation_homogeneous(z);qw=c.act(j.LIFT,z);norm=a.dot(qw,qw)
            for hi,(g,comp) in enumerate(j.HOLE_MOTIONS):
                e=c.mm(c.mm(Mn,g),c.MX) if comp else g
                literal=(sum((a.dot(row,col) for row,col in zip(Rh,e)),Q())-j.TAU*norm)*(r2 if comp else 1)
                wanted=j.qform(evaluate_receiver(j.HOLES[hi],t),z)
                c.require(literal==wanted,'actual original fixed/moving trace collar, not a constant old reference')
                stream.append(['H',hi,[c.enc(v) for v in t],[c.enc(v) for v in src],c.enc(literal)]);literal_holes+=1
            x,y,scale=r[0],-r[2],r[1];U,V,w=src
            for gi in range(2):
                v=x+y*w-j.M*scale*V if gi==0 else y-x*w+j.M*scale*U
                literal=v*v-r2;wanted=j.qform(evaluate_receiver(j.GAUGES[gi],t),z)
                c.require(literal==wanted,'actual conditional closed canonical gauge')
                stream.append(['G',gi,[c.enc(v) for v in t],[c.enc(v) for v in src],c.enc(literal)]);literal_gauges+=1
    coefficient_checks=0
    receivers=[j.UNIT_TRI,j.receiver_split(j.UNIT_TRI,1)[0],j.receiver_split(j.receiver_split(j.UNIT_TRI,0)[1],2)[1]]
    matrices=f.cut(120,tuple((11*e+7*120+3)%60 for e in j.STRESSES[120]['indices']))
    for depth,code in ((0,0),(7,91),(26,0)):
        for vertices in receivers:
            T=j.barycentric_restriction(vertices)
            for mats in (matrices,j.HOLES[0],j.HOLES[1],j.GAUGES[0]):
                restricted=mats if len(mats)==1 else [j.add(*(j.scale(A,x) for A,x in zip(mats,row))) for row in T]
                reference=[x for A in restricted for x in reference_source_coefficients(A,depth,code)]
                actual=j.tensor_coefficients(mats,vertices,depth,code)
                c.require(actual==reference==j.tensor_coefficients_reference(mats,vertices,depth,code),'complete independent values-conversion/reference/integer-cleared product coefficient arrays')
                den,ivals=j.tensor_integer_coefficients(mats,vertices,depth,code)
                c.require(all(j.integer_pair_sign(av,bv)==x.sign() for (av,bv),x in zip(ivals,actual)),'every independent coefficient also has matching direct integer-pair sign')
                stream.append(['B',depth,code,[[str(x) for x in v] for v in vertices],[c.enc(x) for x in actual]]);coefficient_checks+=len(actual)
    c.require(len(j.tensor_coefficients(j.GAUGES[0],j.UNIT_TRI,0,0,0))==54 and len(j.tensor_coefficients(j.GAUGES[1],j.UNIT_TRI,0,0,1))==54,'true reduced gauge product count')
    c.require(len(forces)==18*len(j.STRESSES) and len(weights)==3*sum(len(s['indices']) for s in j.STRESSES),'complete stress equations/corner weights')
    return {'agent':'six-rupert-2','role':'researcher','scope':'exact fresh whole-phase4 fan joint-form layer only; no complete source forest implied','actual_stresses':len(j.STRESSES),'closed_fan':j.FAN,'original_triangle_indices':list(j.FANS[j.FAN]),'nonnegative_closed_corner_weights':len(weights),'entire_three_spatial_force_controls':len(forces),'literal_original_physical_cut_fixtures':literal_cuts,'literal_original_world_trace_hole_fixtures':literal_holes,'literal_original_gauge_fixtures':literal_gauges,'independent_full_product_coefficient_comparisons':coefficient_checks,'physical_or_moving_hole_controls_per_product':162,'canonical_gauge_controls_per_product':54,'constant_A_hole_controls_per_product':27,'pair_degree_elevation':'raw r_y=1, positive throughout actual receiving cell','complete_mathematical_records_sha256':c.digest(stream),'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-start}

def local_record():
    import importlib.util
    location=Path(__file__).resolve().parent.parent/'phase4_contacts/check.py'
    spec=importlib.util.spec_from_file_location('published_phase4_conditional_checker',location)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.complete_record()


def tree_inventory(proposal,allow_pending=False,validate_partition=False):
    c.require(proposal['agent']=='six-rupert-2' and proposal['role']=='researcher','actual author and role')
    c.require(proposal['fan']==j.FAN and proposal['closed_fan_original_triangle_indices']==list(j.FANS[j.FAN]),'literal original whole closed fan')
    c.require(proposal['closed_trace_gate']==['2699/901','0'] and proposal['source_M']==['15/4','0'],'current proved local gate and universal actual source cover')
    c.require(proposal['actual_stress_count']==len(j.STRESSES),'fresh actual fan stress inventory')
    c.require(proposal['hole_order']==['I','H','A','AH','B','BH','G','GH','HB','HBH','C_n(I)','C_n(H)','C_n(A)','C_n(AH)','C_n(B)','C_n(BH)','C_n(G)','C_n(GH)','C_n(HB)','C_n(HBH)'],'literal original parent/companion hole order')
    prefix=proposal.get('tree_encoding')=='preorder_binary'
    if prefix:
        c.require(proposal.get('schema')==1 and proposal.get('named_solid')=='original unit-edge J74 metabigyrate rhombicosidodecahedron','literal original named certificate schema')
        c.require(proposal.get('receiving_world_raw')=='(x,1,-y)' and proposal.get('source_quaternion_world')=='(1+MU,-1+MU,MV+w,w-MV)','original receiving and source world coordinates')
    nodes=proposal['nodes'];c.require(type(nodes) is list and 0<len(nodes)<=80002,'bounded explicit rooted binary joint tree')
    seen=set();leaves=[];pending=[];stack=[(0,j.UNIT_TRI,0,0,0)];rsplits=0;ssplits=0
    cursor=0
    while stack:
        pos,vertices,depth,code,rd=stack.pop()
        number=cursor if prefix else pos
        cursor+=1
        c.require(type(number) is int and number in range(len(nodes)) and number not in seen,'each actual node reachable exactly once')
        c.require(0<=depth<=36 and 0<=rd<=14,'declared unchanged finite refinement bounds')
        seen.add(number);node=nodes[number];c.require(type(node) is list and node,'literal actual node')
        if validate_partition:
            for v in vertices:c.require(len(v)==3 and all(x>=0 for x in v) and sum(v)==1,'actual closed fan barycentric corner')
            area=abs(det3(vertices));c.require(area==F(1,2**rd),'every actual closed receiver child has its exact positive dyadic area')
            independent_source_box(depth,code)
        if node[0] in ('S','R'):
            if node[0]=='S':
                c.require(len(node)==(1 if prefix else 3),'source split row');left,right=(0,0) if prefix else node[1:]
                children=[(vertices,depth+1,2*code,rd),(vertices,depth+1,2*code+1,rd)];ssplits+=1
            else:
                c.require(len(node)==(2 if prefix else 4),'receiving split row');edge=node[1];left,right=(0,0) if prefix else node[2:]
                children=[(v,depth,code,rd+1) for v in j.receiver_split(vertices,edge)];rsplits+=1
            if not prefix:c.require(type(left) is int and type(right) is int and number<left<len(nodes) and number<right<len(nodes) and left!=right,'literal acyclic distinct children')
            stack.extend([(right,*children[1]),(left,*children[0])]);continue
        if node[0]=='?':
            c.require(allow_pending and len(node)==1,'unresolved products forbid complete source theorem')
            pending.append((number,vertices,depth,code,rd));continue
        c.require(node[0] in ('C','G','H'),'physical cut, conditional gauge or proved collar')
        if node[0]=='C':
            ci=node[1];c.require(type(ci) is int and ci in range(len(j.STRESSES)),'fresh actual stress')
            c.require(len(node)==2+len(j.STRESSES[ci]['indices']) and all(type(k) is int and k in range(60) for k in node[2:]),'literal original source vertices for all stressed original edges')
        else:c.require(len(node)==2 and type(node[1]) is int and node[1] in range(20 if node[0]=='H' else 2),'proved original collar or canonical gate')
        leaves.append((number,vertices,depth,code,rd,node))
    c.require(len(seen)==len(nodes),'no disconnected or unexamined product nodes')
    c.require(len(leaves)+len(pending)==rsplits+ssplits+1,'full closed binary product partition')
    if not allow_pending:c.require(not pending and proposal['complete_floating_proposal'],'every closed joint product must have an exact witness')
    return leaves,{'nodes':len(nodes),'leaves':len(leaves),'pending':len(pending),'receiver_splits':rsplits,'source_splits':ssplits,'all_nodes_reachable_once':True,'closed_cover_complete':not pending}

def det3(A):
    return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def independent_source_box(depth,code):
    c.require(type(depth) is int and type(code) is int and 0<=code<2**depth,'actual dyadic source address')
    ds=[0,0,0];codes=[0,0,0]
    for level in range(depth):
        axis=level%3;ds[axis]+=1;codes[axis]=2*codes[axis]+((code>>(depth-level-1))&1)
    lo=[F(-1)+F(2*codes[k],2**ds[k]) for k in range(3)]
    hi=[F(-1)+F(2*codes[k]+2,2**ds[k]) for k in range(3)]
    c.require((lo,hi)==j.source_box(depth,code),'independent closed dyadic source endpoint decoding')
    return lo,hi

def partition_record(proposal,allow_pending=False):
    started=time.monotonic();leaves,inventory=tree_inventory(proposal,allow_pending,validate_partition=True)
    counts={'C':0,'G':0,'H':0};holes={str(k):0 for k in range(len(j.HOLE_MOTIONS))};stream=[]
    for number,vertices,depth,code,rd,node in leaves:
        counts[node[0]]+=1
        if node[0]=='H':holes[str(node[1])]+=1
        stream.append([number,node,[[str(x) for x in v] for v in vertices],depth,code,rd])
    return {'agent':'six-rupert-2','role':'researcher','closed_fan':j.FAN,'scope':'exact closed partition ONLY, every sign and original-source/local bridges still required','certificate_canonical_sha256':c.digest(proposal),'inventory':inventory,'leaf_kinds':counts,'trace_hole_kinds':holes,'maximum_source_depth':max((row[2] for row in leaves),default=0),'maximum_receiver_depth':max((row[4] for row in leaves),default=0),'complete_partition_stream_sha256':c.digest(stream),'wall_seconds':time.monotonic()-started}

def semantics_record(proposal):
    import copy
    def badtest(name,mutate):
        changed=copy.deepcopy(proposal);mutate(changed)
        try:tree_inventory(changed)
        except (ValueError,IndexError,TypeError,KeyError):return name
        raise ValueError('damaged certificate accepted: '+name)
    ci=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='C')
    hi=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='H')
    gi=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='G')
    ri=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='R')
    bad=[badtest('missing closed final branch',lambda d:d['nodes'].pop()),
         badtest('disconnected extra closed branch',lambda d:d['nodes'].append(['H',0])),
         badtest('unproved old phase56 local radius',lambda d:d.__setitem__('closed_trace_gate',['661/221','0'])),
         badtest('incomplete reduced source box',lambda d:d.__setitem__('source_M',['1','0'])),
         badtest('wrong original fan',lambda d:d.__setitem__('fan',3)),
         badtest('unproved original collar',lambda d:d['nodes'][hi].__setitem__(1,20)),
         badtest('unregistered original gauge',lambda d:d['nodes'][gi].__setitem__(1,2)),
         badtest('non-original source vertex',lambda d:d['nodes'][ci].__setitem__(2,60)),
         badtest('invalid receiving split',lambda d:d['nodes'][ri].__setitem__(1,3)),
         badtest('wrong original world quaternion',lambda d:d.__setitem__('source_quaternion_world','relative mistaken for world')),
         badtest('reordered moving-hole metadata',lambda d:d['hole_order'].reverse())]
    values=[2*p[1]-p[0]*p[0] for p in c.PENT]
    c.require(min(values)==(3-c.S)/2 and min(values)>0,'identity is physical fit but violates original canonical G1 throughout actual pentagon')
    return {'agent':'six-rupert-2','role':'researcher','closed_fan':j.FAN,'semantic_damage_rejections':bad,'literal_original_identity_physical_fit_violates_G1_corner_minimum':c.enc(min(values)),'scope':'implementation input checks and physical-gauge countercontrol, not a formal proof or independent reviewer verdict','independent_review':False}

def chunk_record(proposal,index,size=64,allow_pending=False):
    start=time.monotonic();leaves,inventory=tree_inventory(proposal,allow_pending);c.require(type(index) is int and index>=0 and index*size<len(leaves),'actual leaf chunk')
    chosen=leaves[index*size:min((index+1)*size,len(leaves))];f=j.ExactForms();stream=hashlib.sha256();count=0;kinds={'C':0,'G':0,'H':0};mins={}
    for number,vertices,depth,code,rd,node in chosen:
        kind=node[0];which=node[1]
        if kind=='C':mats=f.cut(which,node[2:]);unused=None
        elif kind=='H':mats=j.HOLES[which];unused=None
        else:mats=j.GAUGES[which];unused=which
        den,vals=j.tensor_integer_coefficients(mats,vertices,depth,code,unused)
        c.require(den>0 and all(j.integer_pair_sign(av,bv)>0 for av,bv in vals),'EVERY exact receiving/source control must be strictly positive, leaf '+str(number))
        low=vals[0]
        for av,bv in vals[1:]:
            if j.integer_pair_sign(av-low[0],bv-low[1])<0:low=(av,bv)
        minimum=Q(F(low[0],den),F(low[1],den))
        count+=len(vals);kinds[kind]+=1;mins[kind]=min(mins.get(kind,minimum),minimum)
        record=[number,node,[[str(x) for x in v] for v in vertices],depth,code,rd,[[str(F(av,den)),str(F(bv,den))] for av,bv in vals]]
        stream.update(c.canonical(record));stream.update(b'\n')
    return {'agent':'six-rupert-2','role':'researcher','closed_fan':j.FAN,'scope':'exact closed leaf chunk ONLY; every chunk and original-source/local bridges required','certificate_canonical_sha256':c.digest(proposal),'chunk_index':index,'chunk_size':size,'leaf_start':index*size,'leaf_end':index*size+len(chosen),'verified_leaves':len(chosen),'strict_exact_controls':count,'leaf_kinds':kinds,'minimum_coefficients':{k:c.enc(v) for k,v in mins.items()},'complete_coefficient_stream_sha256':stream.hexdigest(),'inventory':inventory,'partial_forest':allow_pending,'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-start}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--local',action='store_true');parser.add_argument('--semantics',action='store_true');parser.add_argument('--layer',action='store_true');parser.add_argument('--coordinate',action='store_true');parser.add_argument('--partition',action='store_true');parser.add_argument('--proposal');parser.add_argument('--chunk',type=int,default=0);parser.add_argument('--size',type=int,default=64);parser.add_argument('--allow-pending',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    if args.local:r=local_record()
    elif args.semantics:r=semantics_record(json.loads(Path(args.proposal).read_text()))
    elif args.layer:r=layer_record()
    elif args.coordinate:
        import source_cover
        r=source_cover.record()
    elif args.partition:r=partition_record(json.loads(Path(args.proposal).read_text()),args.allow_pending)
    else:
        c.require(args.proposal is not None,'literal explicit proposal required')
        r=chunk_record(json.loads(Path(args.proposal).read_text()),args.chunk,args.size,args.allow_pending)
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
