#!/usr/bin/env python3
"""Exact bounded replay and explicit assembly of the full J74 rectangle proof.

The standard-library local and joint checks are separate finite jobs. A partial
chunk is not the theorem; assembly requires the local bridge and all chunks.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import argparse,copy,hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('j74_rectangle_forms',HERE/'forms.py')
j=importlib.util.module_from_spec(spec);sys.modules[spec.name]=j;spec.loader.exec_module(j)
c,p,Q,a=j.c,j.p,j.Q,j.a
CHUNK_SIZE=768
def digest(x):return hashlib.sha256(c.canonical(x)).hexdigest()
def certificate(data=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    c.require(set(data)=={'schema','agent','role','scope','parent_source_commit','parent_certificate_canonical_sha256',
                         'raw_receiving_halfwidth','point_hole_Cayley_gate','leaves'},'exact compact forest schema')
    c.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','forest schema and actual author')
    c.require(data['parent_source_commit']==p.DEPENDENCIES['parent_source_commit'],'pinned parent provenance')
    parent=json.loads((c.HERE/'certificate.json').read_text())
    c.require(data['parent_certificate_canonical_sha256']==digest(parent),'entire original pose/contact certificate fingerprint')
    c.require(data['raw_receiving_halfwidth']==['1/1000','0'] and data['point_hole_Cayley_gate']==['1/17','0'],
              'fixed proved receiver and derived source-hole scopes')
    charts=c.validate_partition(data['leaves'])
    return data,charts
def local_record(full=False):
    data,charts=certificate();math=p.preflight(Q(F(1,1000)))
    math={k:v for k,v in math.items() if k!='wall_seconds'}
    record={'agent':'six-rupert-2','role':'researcher','kind':'complete conditional local bridge on entire receiver rectangle',
        'certificate_canonical_sha256':digest(data),'whole_local_mathematical_record_sha256':digest(math),
        'original_vertex_count':60,'complete_receiving_cycle':math['complete_receiving_cycle'],
        'actual_receiver_corner_support_comparisons':math['actual_receiver_corner_support_comparisons'],
        'actual_source_corner_offendpoint_comparisons':math['actual_source_corner_offendpoint_comparisons'],
        'exact_raw_dual_families':len(math['local_families']),'exact_comparison_inverses':math['distinct_exact_raw_comparison_inverses'],
        'strict_uniform_raw_weight_floor':['1/2000','0'],'strict_uniform_component_Neumann_infinity_upper':['1/20','0'],
        'strict_uniform_coordinate_contact_mass_upper':[6,7,8],'uniform_contact_quadratic_constant':['5/4','0'],
        'closed_relative_Cayley_Euclidean_gate':['1/16','0'],'simple_squared_local_absorption':['3725/4096','0'],
        'raw_rectangle_center':math['raw_rectangle_center'],'raw_rectangle_halfwidth':['1/1000','0'],
        'source_hole_point_gate':['1/17','0'],'persistent_opposite_spatial_edge_pairs':math['persistent_opposite_spatial_edge_pairs'],
        'whole_box_strict_positive_cofactor_triples':math['whole_box_strict_positive_cofactor_triples'],
        'failing_point_circuits':math['failing_point_circuits'],'closed_chart_leaf_counts':charts}
    c.require(not record['failing_point_circuits'],'all advertised receiver stresses valid on entire box')
    return (record,math) if full else record
def chunk_record(index,profile=None,data=None):
    data,charts=certificate(data);leaves=data['leaves'];n=(len(leaves)+CHUNK_SIZE-1)//CHUNK_SIZE
    c.require(type(index) is int and index in range(n),'actual bounded chunk index')
    start=index*CHUNK_SIZE;end=min(start+CHUNK_SIZE,len(leaves))
    if profile is not None:
        c.require(type(profile) is int and 0<profile<=end-start,'partial exact chunk length')
        end=start+profile
    forms=j.Forms();stream=hashlib.sha256();counts={'C':0,'H':0};minimum={};checks=0
    for number,leaf in enumerate(leaves[start:end],start):
        values=forms.exact_leaf_coefficients(leaf)
        c.require(min(values)>0,'strict exact whole receiver/source leaf '+str(number))
        checks+=len(values);counts[leaf[3]]+=1
        minimum[leaf[3]]=min(minimum.get(leaf[3],values[0]),min(values))
        stream.update(c.canonical([leaf,[c.enc(x) for x in values]]));stream.update(b'\n')
    return {'agent':'six-rupert-2','role':'researcher','scope':'exact bounded source chunk; whole local bridge and every other chunk remain required',
        'certificate_canonical_sha256':digest(data),'chunk_index':index,'chunk_size':CHUNK_SIZE,'required_chunks':n,
        'leaf_start_inclusive':start,'leaf_end_exclusive':end,'verified_leaf_count':end-start,
        'profile_partial':profile is not None and end<min(start+CHUNK_SIZE,len(leaves)),
        'verified_leaf_kinds':counts,'strict_joint_Bernstein_coefficient_count':checks,
        'minimum_exact_Bernstein_coefficients':{k:c.enc(v) for k,v in minimum.items()},
        'complete_chunk_coefficient_stream_sha256':stream.hexdigest(),'unique_exact_cut_forms':len(forms.cache),
        'closed_chart_leaf_counts':charts,'source_quaternion_charts':4,'actual_stresses':168,
        'exact_receiver_polynomial_force_component_identities':168*6*3}
def assemble(local,chunks):
    data,charts=certificate();leaves=data['leaves'];n=(len(leaves)+CHUNK_SIZE-1)//CHUNK_SIZE
    c.require(len(chunks)==n,'every bounded source chunk required')
    c.require(local['certificate_canonical_sha256']==digest(data),'local bridge belongs to this entire forest')
    end=0;counts={'C':0,'H':0};checks=0
    for index,record in enumerate(chunks):
        c.require(record['chunk_index']==index and record['leaf_start_inclusive']==end and not record['profile_partial'],
                  'ordered source ranges have no missing or partial chunk')
        c.require(record['certificate_canonical_sha256']==digest(data),'source chunk belongs to this forest')
        wanted_end=min(end+CHUNK_SIZE,len(leaves))
        c.require(record['leaf_end_exclusive']==wanted_end,'whole actual source range required')
        c.require(record['verified_leaf_count']==wanted_end-end,'range count matches actual source leaves')
        end=wanted_end;checks+=record['strict_joint_Bernstein_coefficient_count']
        for kind in counts:counts[kind]+=record['verified_leaf_kinds'][kind]
    c.require(end==len(leaves) and sum(counts.values())==len(leaves),'entire four-chart source forest verified')
    c.require(counts=={kind:sum(x[3]==kind for x in leaves) for kind in counts},'actual full forest inventory')
    c.require(checks==243*counts['C']+27*counts['H'],'entire biquadratic coefficient inventory')
    return {'agent':'six-rupert-2','role':'researcher','scope':'all-source closed-fit rigidity on entire closed nonminimal raw receiving rectangle; global J74 remains open',
        'certificate_canonical_sha256':digest(data),'verified_source_leaves':len(leaves),'verified_leaf_kinds':counts,
        'strict_exact_joint_Bernstein_coefficient_count':checks,'closed_chart_leaf_counts':charts,
        'required_completed_source_chunks':n,'whole_local_mathematical_record_sha256':local['whole_local_mathematical_record_sha256'],
        'ordered_complete_chunk_records_sha256':digest(chunks),'coefficient_stream_hashes_in_chunk_order':[x['complete_chunk_coefficient_stream_sha256'] for x in chunks],
        'receiving_raw_halfwidth':['1/1000','0'],'actual_equal_shadow_motions':12,'source_entry_hypothesis':False,
        'arbitrary_original_translation_retained':True,'all_scales_at_least_one':True,'includes_all_halfturns':True,
        'local_verification_and_all_chunks_required':True}
def audits():
    """Different exact conversion algorithms on the complete symmetric basis."""
    comparisons=0
    for chart in range(4):
        for depth,code in ((0,0),(7,91)):
            lo,hi=c.box(depth,code);W=j.quaternion_moments(chart,lo,hi)
            for i in range(4):
                for k in range(i,4):
                    B=[[Q() for v in range(4)] for u in range(4)];B[i][k]=Q(1);B[k][i]=Q(1)
                    original=c.coefficients(B,chart,lo,hi);direct=j.moment_coefficients(B,W)
                    c.require(original==direct,'two exact quaternion Bernstein conversion algorithms')
                    comparisons+=len(original)
    e=Q(F(1,1000));basis1=((1,-2,1),(0,2,-2),(0,0,1));receiver_checks=0
    for kind in range(6):
        components=[[[Q() for v in range(4)] for u in range(4)] for k in range(6)]
        components[kind][0][0]=Q(1)
        controls=[B[0][0] for B in j.receiver_controls(components,e)]
        expanded=[[Q() for b in range(3)] for a in range(3)]
        for (i,k),v in zip(product(range(3),repeat=2),controls):
            for x in range(3):
                for y in range(3):expanded[x][y]+=v*basis1[i][x]*basis1[k][y]
        wanted=[[Q() for b in range(3)] for a in range(3)]
        if kind==0:wanted[0][0]=Q(1)
        elif kind==1:wanted[0][0]=-e;wanted[1][0]=2*e
        elif kind==2:wanted[0][0]=-e;wanted[0][1]=2*e
        elif kind==3:wanted[0][0]=e*e;wanted[1][0]=-4*e*e;wanted[2][0]=4*e*e
        elif kind==4:wanted[0][0]=e*e;wanted[1][0]=-2*e*e;wanted[0][1]=-2*e*e;wanted[1][1]=4*e*e
        else:wanted[0][0]=e*e;wanted[0][1]=-4*e*e;wanted[0][2]=4*e*e
        c.require(expanded==wanted,'receiver tensor coefficients re-expand the whole ordinary polynomial')
        receiver_checks+=9
    return {'quaternion_basis_coefficient_equalities':comparisons,'receiver_ordinary_coefficient_equalities':receiver_checks}
def damages():
    data,charts=certificate();parent=json.loads((c.HERE/'certificate.json').read_text());passed=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,StopIteration,ZeroDivisionError):passed.append(label)
        else:raise ValueError('damaged control accepted: '+label)
    bad=copy.deepcopy(data);bad['leaves'].pop(0);reject('missing closed source cube',lambda:certificate(bad))
    bad=copy.deepcopy(data);bad['leaves']=[x for x in bad['leaves'] if x[0]!=3];reject('omitted half-turn component chart',lambda:certificate(bad))
    leaf=next(x[:] for x in data['leaves'] if x[3]=='C');leaf[5:]=[0]*len(leaf[5:])
    reject('same original at every receiver stress',lambda:c.require(min(j.Forms().exact_leaf_coefficients(leaf))>0,'actual wrong-source gap'))
    bad=copy.deepcopy(parent);x=bad['poses'][0]['proper_matrix_rows'][0][0];x[0]=str(F(x[0])+F(1,1000))
    reject('wrong named proper source pose',lambda:p.preflight(Q(F(1,1000)),bad))
    bad=copy.deepcopy(parent);x=bad['poses'][0]['coordinate_duals'][0]['weights'][0];x[0]=str(F(x[0])+F(1,10**6))
    reject('false positive point force balance',lambda:p.preflight(Q(F(1,1000)),bad))
    bad=copy.deepcopy(data);bad['raw_receiving_halfwidth']=['1/500','0']
    reject('enlarged receiver rectangle without new proof',lambda:certificate(bad))
    reject('unsupported moving equality hole',lambda:j.Forms(hole_gate=F(1,4)))
    def bad_receiver_square():
        e=Q(F(1,1000));components=[[[Q() for v in range(4)] for u in range(4)] for k in range(6)]
        components[3][0][0]=Q(1);controls=[B[0][0] for B in j.receiver_controls(components,e)]
        for k in range(3):controls[3+k]=e*e
        basis=((1,-2,1),(0,2,-2),(0,0,1));expanded=[[Q() for y in range(3)] for x in range(3)]
        for (i,k),v in zip(product(range(3),repeat=2),controls):
            for x in range(3):
                for y in range(3):expanded[x][y]+=v*basis[i][x]*basis[k][y]
        c.require(expanded[0][0]==e*e and expanded[1][0]==-4*e*e and expanded[2][0]==4*e*e,
                  'damaged receiver controls must re-expand the actual raw square')
    reject('false quadratic Bernstein middle control',bad_receiver_square)
    return passed
def main():
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--local',action='store_true');mode.add_argument('--chunk',type=int);mode.add_argument('--aggregate',type=Path)
    mode.add_argument('--self-test',action='store_true');parser.add_argument('--profile-leaves',type=int)
    parser.add_argument('--no-expected',action='store_true');parser.add_argument('--print-record',action='store_true')
    args=parser.parse_args();expected=None
    if not args.no_expected:expected=json.loads((HERE/'expected.json').read_text())
    if args.self_test:
        result={'agent':'six-rupert-2','role':'researcher','exact_algebra_audits':audits(),'damaged_controls_rejected':damages()}
        if expected is not None:c.require(result==expected['self_test'],'complete control record mismatch')
    elif args.local:
        compact,full=local_record(True);result=full if args.print_record else compact
        if expected is not None:c.require(compact==expected['local'],'whole exact local bridge record mismatch')
    elif args.chunk is not None:
        result=chunk_record(args.chunk,args.profile_leaves)
        if expected is not None and args.profile_leaves is None:c.require(result==expected['chunks'][args.chunk],'complete exact source chunk record mismatch')
    else:
        c.require(expected is not None,'assembly needs independently fixed complete expected records')
        local=json.loads((args.aggregate/'local.json').read_text());chunks=[]
        c.require(local==expected['local'],'complete journal local record required')
        for i,wanted in enumerate(expected['chunks']):
            record=json.loads((args.aggregate/('chunk-%02d.json'%i)).read_text())
            c.require(record==wanted,'complete journal source chunk required: '+str(i));chunks.append(record)
        result=assemble(local,chunks);c.require(result==expected['aggregate'],'complete assembled mathematical record mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
