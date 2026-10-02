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
    chosen=(0,1,2,3,4,5,120,229)
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
            for hi,(g,comp) in enumerate(((c.H,True),(c.POSES[4],False),(c.POSES[3],True))):
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
                c.require(actual==reference,'complete independently converted source/receiver product coefficient arrays')
                stream.append(['B',depth,code,[[str(x) for x in v] for v in vertices],[c.enc(x) for x in actual]]);coefficient_checks+=len(actual)
    c.require(len(j.tensor_coefficients(j.GAUGES[0],j.UNIT_TRI,0,0,0))==54 and len(j.tensor_coefficients(j.GAUGES[1],j.UNIT_TRI,0,0,1))==54,'true reduced gauge product count')
    c.require(len(forces)==4140 and len(weights)==2055,'complete stress equations/corner weights')
    return {'agent':'six-rupert-2','role':'researcher','scope':'exact fresh whole-phase56 joint-form layer only; no complete source forest implied','actual_stresses':230,'nonnegative_closed_corner_weights':len(weights),'entire_three_spatial_force_controls':len(forces),'literal_original_physical_cut_fixtures':literal_cuts,'literal_original_world_trace_hole_fixtures':literal_holes,'literal_original_gauge_fixtures':literal_gauges,'independent_full_product_coefficient_comparisons':coefficient_checks,'physical_or_moving_hole_controls_per_product':162,'canonical_gauge_controls_per_product':54,'constant_A_hole_controls_per_product':27,'pair_degree_elevation':'raw r_y=1, positive throughout actual receiving cell','complete_mathematical_records_sha256':c.digest(stream),'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-start}

def tree_inventory(proposal,allow_pending=False):
    if proposal.get('tree_encoding')=='preorder_binary':
        c.require(proposal.get('schema')==1 and proposal.get('agent')=='six-rupert-2' and proposal.get('role')=='researcher','literal actual certificate author/schema')
        c.require(proposal.get('named_solid')=='original unit-edge J74 metabigyrate rhombicosidodecahedron' and proposal.get('receiving_world_raw')=='(x,1,-y)','original named geometry and world chart')
        c.require(proposal.get('source_quaternion_world')=='(1+MU,-1+MU,MV+w,w-MV)' and proposal.get('receiving_domain')=='entire actual closed phase56 triangle from public9677/0','actual complete world source and receiving domain')
        c.require(proposal.get('source_M')==['15/4','0'] and proposal.get('closed_trace_gate')==['661/221','0'] and proposal.get('canonical_known_motion_order')==['C_n(H)','A','C_n(B)'],'actual complete source domain and three proved local collars')
        nodes=proposal['nodes'];c.require(type(nodes) is list and 0<len(nodes)<=80002,'bounded full prefix joint tree')
        leaves=[];pending=[];stack=[(j.UNIT_TRI,0,0,0)];rsplits=0;ssplits=0
        for number,node in enumerate(nodes):
            c.require(stack and type(node) is list and node,'exact prefix tree without disconnected trailing nodes')
            vertices,depth,code,rd=stack.pop()
            c.require(depth<=40,'source refinement bound')
            if node[0]=='S':
                c.require(len(node)==1,'actual prefix source split')
                stack.extend([(vertices,depth+1,2*code+1,rd),(vertices,depth+1,2*code,rd)]);ssplits+=1
            elif node[0]=='R':
                c.require(len(node)==2,'actual prefix receiver split')
                children=j.receiver_split(vertices,node[1]);stack.extend([(children[1],depth,code,rd+1),(children[0],depth,code,rd+1)]);rsplits+=1
            else:
                c.require(node[0] in ('C','G','H'),'every prefix leaf has an actual mathematical witness; unresolved nodes forbidden')
                leaves.append((number,vertices,depth,code,rd,node))
        c.require(not stack and len(leaves)==rsplits+ssplits+1,'entire closed prefix product cover, no missing branches')
        for number,vertices,depth,code,rd,node in leaves:
            which=node[1] if len(node)>1 else None
            if node[0]=='C':
                c.require(type(which) is int and which in range(230),'true current stress index')
                c.require(len(node)==2+len(j.STRESSES[which]['indices']) and all(type(k) is int and k in range(60) for k in node[2:]),'original vertex labels in every true physical cut')
            else:c.require(len(node)==2 and type(which) is int and which in range(3 if node[0]=='H' else 2),'actual trace collar or canonical gauge index')
        return leaves,{'nodes':len(nodes),'leaves':len(leaves),'pending':0,'receiver_splits':rsplits,'source_splits':ssplits,'all_nodes_reachable_once':True,'closed_cover_complete':True}
    nodes=proposal['nodes'];c.require(type(nodes) is list and 0<len(nodes)<=80002,'bounded explicit rooted binary joint tree')
    seen=set();leaves=[];pending=[];stack=[(0,j.UNIT_TRI,0,0,0)];rsplits=0;ssplits=0
    while stack:
        number,vertices,depth,code,rd=stack.pop()
        c.require(type(number) is int and number in range(len(nodes)) and number not in seen,'every reachable actual node exactly once')
        seen.add(number);node=nodes[number];c.require(type(node) is list and node,'literal actual node')
        if node[0] in ('S','R'):
            if node[0]=='S':
                c.require(len(node)==3,'source split row');left,right=node[1:]
                children=[(vertices,depth+1,2*code,rd),(vertices,depth+1,2*code+1,rd)];ssplits+=1
            else:
                c.require(len(node)==4,'receiving split row');edge,left,right=node[1:]
                children=[(v,depth,code,rd+1) for v in j.receiver_split(vertices,edge)];rsplits+=1
            c.require(type(left) is int and type(right) is int and number<left<len(nodes) and number<right<len(nodes) and left!=right,'literal acyclic distinct children')
            stack.extend([(right,*children[1]),(left,*children[0])]);continue
        if node[0]=='?':
            c.require(allow_pending and len(node)==1,'unresolved products forbid complete source theorem')
            pending.append((number,vertices,depth,code,rd));continue
        c.require(node[0] in ('C','G','H'),'physical cut, conditional gauge or proved collar')
        leaves.append((number,vertices,depth,code,rd,node))
    c.require(len(seen)==len(nodes),'no disconnected or unexamined joint tree nodes')
    if not allow_pending:c.require(not pending and proposal['complete_floating_proposal'],'complete actual closed joint product union')
    return leaves,{'nodes':len(nodes),'leaves':len(leaves),'pending':len(pending),'receiver_splits':rsplits,'source_splits':ssplits,'all_nodes_reachable_once':True,'closed_cover_complete':not pending}

def independent_source_box(depth,code):
    lo=[];hi=[]
    for axis in range(3):
        bits=[(code>>(depth-level-1))&1 for level in range(axis,depth,3)]
        integer=0
        for bit in bits:integer=2*integer+bit
        width=F(2,2**len(bits));lo.append(-1+integer*width);hi.append(-1+(integer+1)*width)
    return lo,hi

def partition_record(proposal):
    start=time.monotonic();leaves,inventory=tree_inventory(proposal);stream=hashlib.sha256();counts={'C':0,'G':0,'H':0};holes={'0':0,'1':0,'2':0};maxsd=0;maxrd=0
    for number,vertices,depth,code,rd,node in leaves:
        c.require(all(all(t>=0 for t in v) and sum(v,F())==1 for v in vertices),'every original receiving corner in the whole closed triangle')
        area=abs(sum((v[0]*u[1]-v[1]*u[0] for v,u in zip(vertices,vertices[1:]+vertices[:1])),F()))
        c.require(area==F(1,2**rd),'every receiving product triangle has its exact positive dyadic area')
        c.require(j.source_box(depth,code)==independent_source_box(depth,code),'independent every-leaf closed source cube decoder')
        counts[node[0]]+=1
        if node[0]=='H':holes[str(node[1])]+=1
        maxsd=max(maxsd,depth);maxrd=max(maxrd,rd)
        stream.update(c.canonical([number,node,[[str(x) for x in v] for v in vertices],depth,code,rd]));stream.update(b'\n')
    return {'agent':'six-rupert-2','role':'researcher','scope':'full exact closed joint product partition only, every leaf sign and mathematical bridges still required','certificate_canonical_sha256':c.digest(proposal),'inventory':inventory,'leaf_kinds':counts,'trace_hole_kinds':holes,'maximum_source_depth':maxsd,'maximum_receiver_depth':maxrd,'every_receiver_area_and_independent_source_box_checked':True,'complete_partition_stream_sha256':stream.hexdigest(),'wall_seconds':time.monotonic()-start}

def semantics_record(proposal):
    import copy
    def badtest(name,mutate):
        changed=copy.deepcopy(proposal);mutate(changed)
        try:tree_inventory(changed)
        except (ValueError,IndexError,TypeError):return name
        raise ValueError('damaged certificate was accepted: '+name)
    ci=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='C');hi=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='H');gi=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='G');ri=next(i for i,n in enumerate(proposal['nodes']) if n[0]=='R')
    damaged=[badtest('missing closed final branch',lambda d:d['nodes'].pop()),badtest('disconnected extra branch',lambda d:d['nodes'].append(['H',0])),badtest('unproved local trace threshold',lambda d:d.__setitem__('closed_trace_gate',['3','0'])),badtest('smaller incomplete global source rectangle',lambda d:d.__setitem__('source_M',['1','0'])),badtest('non-original source vertex',lambda d:d['nodes'][ci].__setitem__(2,60)),badtest('unregistered physical collar',lambda d:d['nodes'][hi].__setitem__(1,3)),badtest('unregistered conditional gauge',lambda d:d['nodes'][gi].__setitem__(1,2)),badtest('invalid receiving split',lambda d:d['nodes'][ri].__setitem__(1,3)),badtest('wrong original world quaternion',lambda d:d.__setitem__('source_quaternion_world','relative quaternion mistaken for world quaternion'))]
    return {'semantic_damage_rejections':damaged,'independent_review':False,'scope':'implementation input checks, not a formal proof or independent reviewer verdict'}

def chunk_record(proposal,index,size=32,allow_pending=False):
    start=time.monotonic();leaves,inventory=tree_inventory(proposal,allow_pending);c.require(type(index) is int and index>=0 and index*size<len(leaves),'actual leaf chunk')
    chosen=leaves[index*size:min((index+1)*size,len(leaves))]; f=j.ExactForms();stream=hashlib.sha256();count=0;kinds={'C':0,'G':0,'H':0};mins={}
    for number,vertices,depth,code,rd,node in chosen:
        kind=node[0];which=node[1]
        if kind=='C':mats=f.cut(which,node[2:]);unused=None
        elif kind=='H':
            c.require(len(node)==2 and type(which) is int and which in range(3),'actual fixed/moving known physical trace collar');mats=j.HOLES[which];unused=None
        else:
            c.require(len(node)==2 and type(which) is int and which in range(2),'actual conditional canonical gauge');mats=j.GAUGES[which];unused=which
        vals=j.tensor_coefficients(mats,vertices,depth,code,unused)
        c.require(min(vals)>0,'EVERY exact receiver/source control must be strictly positive, leaf '+str(number))
        count+=len(vals);kinds[kind]+=1;mins[kind]=min(mins.get(kind,vals[0]),min(vals))
        record=[number,node,[[str(x) for x in v] for v in vertices],depth,code,rd,[c.enc(x) for x in vals]]
        stream.update(c.canonical(record));stream.update(b'\n')
    return {'agent':'six-rupert-2','role':'researcher','scope':'actual closed product leaf chunk only; every chunk plus local/source/force bridges required','certificate_canonical_sha256':c.digest(proposal),'chunk_index':index,'chunk_size':size,'leaf_start':index*size,'leaf_end':index*size+len(chosen),'verified_leaves':len(chosen),'strict_exact_controls':count,'leaf_kinds':kinds,'minimum_coefficients':{k:c.enc(v) for k,v in mins.items()},'complete_coefficient_stream_sha256':stream.hexdigest(),'inventory':inventory,'partial_forest':allow_pending,'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-start}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--layer',action='store_true');parser.add_argument('--coordinate',action='store_true');parser.add_argument('--partition',action='store_true');parser.add_argument('--semantics',action='store_true');parser.add_argument('--local',action='store_true');parser.add_argument('--proposal');parser.add_argument('--chunk',type=int,default=0);parser.add_argument('--size',type=int,default=128);parser.add_argument('--allow-pending',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    if args.layer:r=layer_record()
    elif args.coordinate:
        import source_cover
        r=source_cover.record()
    elif args.local:r=c.complete_record()
    elif args.partition:r=partition_record(json.loads(Path(args.proposal).read_text()))
    elif args.semantics:r=semantics_record(json.loads(Path(args.proposal).read_text()))
    else:
        c.require(args.proposal is not None,'explicit proposal input required')
        r=chunk_record(json.loads(Path(args.proposal).read_text()),args.chunk,args.size,args.allow_pending)
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
