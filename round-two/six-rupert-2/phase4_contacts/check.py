#!/usr/bin/env python3
"""Complete fresh conditional local certificate on ENTIRE closed phase4 triangle.

No floating packages, solvers, old source forest or private journal required.
See PROOF.md for the ordinary implication from contacts to closed fits.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,copy,json,time
import geometry as g
import boundary_fit
import duals as d
Q,a,p=g.Q,g.a,d.p
HERE=Path(__file__).resolve().parent
def dec(v):
    g.require(isinstance(v,list) and len(v)==2 and all(isinstance(x,str) for x in v),'literal ordered-field pair')
    return Q(F(v[0]),F(v[1]))
def certificate(data=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    g.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','literal author and schema')
    g.require(data['named_solid']=='original unit-edge J74 metabigyrate rhombicosidodecahedron' and data['receiving_world_raw']=='(x,1,-y)','original named problem and world chart')
    g.require(data['parent_names']==g.NAMES,'all ten literal parent registry including the new half-turn')
    g.require(data['closed_fans']==d.FANS,'single whole closed fan, no boundary/child omitted')
    g.require(len(data['bases'])==6 and [(b['closed_fan'],b['axis'],b['sign']) for b in data['bases']]==list(product(range(1),range(3),(-1,1))),'all six signed contact targets')
    g.require(dec(data['C'])==Q(F(21,20)) and dec(data['closed_physical_Cayley_radius'])==Q(F(1,30)),'fresh literal nonlinear constants')
    g.require(data['axis_mass_bounds']==[11,13,22] and dec(data['absorption_squared'])==Q(F(18963,20000)),'fresh entire-cell absorption bounds')
    g.require(dec(data['closed_relative_trace_gate'])==Q(F(2699,901)) and dec(data['closed_Frobenius_squared_gate'])==Q(F(8,901)),'fresh closed physical gate')
    for b in data['bases']:
        g.require(all(k!=20 for i,j,k in b['literal_original_contacts']),'all signed dual contacts have genuine new-parent spatial preimages')
    return data

def bridge_record(data,geometry,duals):
    fan_areas=[]
    for fan in d.FANS:
        tri=[g.PENT[i] for i in fan];area=sum((v[0]*u[1]-v[1]*u[0] for v,u in zip(tri,tri[1:]+tri[:1])),Q())
        g.require(area>0,'nondegenerate consistently oriented entire closed receiving fan');fan_areas.append(area)
    g.require(sum(fan_areas,Q())==g.area(g.PENT),'literal complete pentagon fan area and shared closed boundaries')
    masses=[max(r['strict_normalized_mass_upper'] for r in duals if r['axis']==k) for k in range(3)]
    g.require(masses==data['axis_mass_bounds'],'all signed fan masses enter the closure')
    C,rho=dec(data['C']),dec(data['closed_physical_Cayley_radius'])
    absorption=C*C*sum((Q(v*v) for v in masses),Q())*rho*rho
    g.require(absorption==dec(data['absorption_squared'])<1,'fresh strict nonlinear absorption on whole closed collar')
    g.require(3-4*rho*rho/(1+rho*rho)==dec(data['closed_relative_trace_gate']) and 8*rho*rho/(1+rho*rho)==dec(data['closed_Frobenius_squared_gate']),'literal Cayley/trace/Frobenius closed gate equivalence')
    # Coefficient identities in three free physical Cayley coordinates.
    variables=[{tuple(int(i==k) for i in range(3)):Q(1)} for k in range(3)];sq={}
    for v in variables:sq=p.add(sq,p.mul(v,v))
    one={p.ZERO:Q(1)};nonlinear_count=0
    for point in g.PENT:
        r=g.raw(point)
        for i,j in g.EDGES:
            m,h=g.support(i,j,r)
            for k in (i,j):
                V=g.V[k];g.require(a.dot(m,V)==h,'literal endpoint equality entering Cayley identity')
                dv={};dm={}
                for z in range(3):dv=p.add(dv,p.scale(variables[z],V[z]));dm=p.add(dm,p.scale(variables[z],m[z]))
                cross=[p.add(p.scale(variables[1],V[2]),p.scale(variables[2],-V[1])),p.add(p.scale(variables[2],V[0]),p.scale(variables[0],-V[2])),p.add(p.scale(variables[0],V[1]),p.scale(variables[1],-V[0]))]
                num=[p.add(p.add(p.scale(p.add(one,p.scale(sq,-1)),V[z]),p.scale(p.mul(variables[z],dv),2)),p.scale(cross[z],2)) for z in range(3)]
                lhs={}
                for z in range(3):lhs=p.add(lhs,p.scale(num[z],m[z]))
                lhs=p.add(lhs,p.scale(p.add(one,sq),-h))
                rhs=p.scale(p.mul(dm,dv),2);rhs=p.add(rhs,p.scale(sq,-2*h));torque=a.cross(V,m)
                for z in range(3):rhs=p.add(rhs,p.scale(variables[z],2*torque[z]))
                g.require(lhs==rhs,'full coefficient Rodrigues/contact nonlinear identity, not sampled d');nonlinear_count+=1
    # Every continuous action follows from P M_n=P and the actual body Mx permutation.
    action_count=0
    for point in g.PENT+[tuple(sum((v[k] for v in g.PENT),Q())/3 for k in range(2))]:
        r=g.raw(point);r2=a.dot(r,r)
        Mn=tuple(tuple(g.I[i][j]-2*r[i]*r[j]/r2 for j in range(3)) for i in range(3))
        P=tuple(tuple(g.I[i][j]-r[i]*r[j]/r2 for j in range(3)) for i in range(3))
        g.require(g.mm(P,Mn)==P and g.mm(Mn,Mn)==g.I and g.mm(P,P)==P,'literal projection/reflection actions')
        g.require(a.dot(Mn[0],a.cross(Mn[1],Mn[2]))==-1,'actual moving reflection improperness')
        for parent in g.POSES:
            companion=g.mm(g.mm(Mn,parent),g.MX);g.proper(companion)
            g.require({g.act(P,g.act(companion,v)) for v in g.V}=={g.act(P,g.act(parent,v)) for v in g.V},'complete sixty-source-point companion action fixture')
            g.require(g.mm(g.mm(Mn,companion),g.MX)==parent,'actual companion involution fixture');action_count+=60
    return {'agent':'six-rupert-2','role':'researcher','all_original_closed_fans':d.FANS,'positive_fan_double_areas':list(map(g.enc,fan_areas)),
            'axis_mass_bounds':masses,'closed_physical_Cayley_radius':g.enc(rho),'absorption_squared':g.enc(absorption),
            'closed_relative_trace_gate':g.enc(dec(data['closed_relative_trace_gate'])),'closed_Frobenius_squared_gate':g.enc(dec(data['closed_Frobenius_squared_gate'])),
            'nonlinear_free_Cayley_polynomial_identities':nonlinear_count,'complete_literal_companion_point_comparisons':action_count,
            'conditional_on_closed_collar':True,'all_source_classification':False,'global_J74_Rupert_status':'OPEN'}

def semantics(data):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,ZeroDivisionError):rejected.append(label);return
        raise ValueError('semantic damage accepted: '+label)
    bad=copy.deepcopy(data);bad['closed_fans'].pop();reject('omitted entire closed receiving fan',lambda:certificate(bad))
    bad=copy.deepcopy(data);bad['bases'].pop();reject('omitted signed physical torque dual',lambda:certificate(bad))
    bad=copy.deepcopy(data);bad['parent_names']=bad['parent_names'][:6];reject('omitted new absolute half-turn parent',lambda:certificate(bad))
    bad=copy.deepcopy(data);bad['bases'][0]['literal_original_contacts'][0]=[20,4,20];reject('missing G spatial preimage used as an alleged contact',lambda:certificate(bad))
    b=copy.deepcopy(data['bases'][0]);b['literal_original_contacts'][0][2]=15
    reject('nongenuine persistent spatial contact',lambda:d.basis_record(b['closed_fan'],b['axis'],b['sign'],b['literal_original_contacts'],b['strict_normalized_mass_upper']))
    b=copy.deepcopy(data['bases'][0]);b['strict_normalized_mass_upper']-=1
    reject('unproved smaller normalized whole-fan mass',lambda:d.basis_record(b['closed_fan'],b['axis'],b['sign'],b['literal_original_contacts'],b['strict_normalized_mass_upper']))
    bad=copy.deepcopy(data);bad['closed_physical_Cayley_radius']=['1/29','0'];reject('larger unproved closed collar radius',lambda:certificate(bad))
    reject('gyrated parent A folded as an actual body symmetry',lambda:g.require({g.act(g.A,v) for v in g.V}==set(g.V),'A is not a full-body source action'))
    reject('false claim A fits the entire original receiving cell',lambda:g.require(all(g.value(w,q)>=0 for q in g.PENT for w in g.constraints(tuple(g.act(g.A,v) for v in g.V))),'A fails literal transformed source supports'))
    return {'agent':'six-rupert-2','role':'researcher','semantic_damages_rejected':rejected}

def complete_record(verify_expected=True):
    start=time.monotonic();data=certificate();geometry=g.record()
    duals=[d.basis_record(b['closed_fan'],b['axis'],b['sign'],b['literal_original_contacts'],b['strict_normalized_mass_upper']) for b in data['bases']]
    for v in duals:v.pop('wall_seconds')
    bridge=bridge_record(data,geometry,duals);semantic=semantics(data);geometry.pop('wall_seconds')
    boundary=boundary_fit.record();boundary.pop('wall_seconds')
    selected=[]
    for b in data['bases']:
        for name,pose,parent in zip(g.NAMES,g.POSES,geometry['parent_motions']):
            for i,j,k in b['literal_original_contacts']:
                source=parent['constant_original_corner_preimages'][g.CYCLE.index(k)]
                g.require(source is not None and g.act(pose,g.V[source])==g.V[k],'every retained physical target has a genuine literal original source preimage for each of ten parents')
                selected.append([name,b['axis'],b['sign'],i,j,k,source])
    math={'agent':'six-rupert-2','role':'researcher','certificate_canonical_sha256':g.digest(data),'geometry':geometry,'new_boundary_fit':boundary,'selected_genuine_parent_contact_preimages':selected,'dual_records':duals,'ordinary_bridge':bridge,'semantic_controls':semantic,
          'scope':'ENTIRE closed phase4 triangle CONDITIONAL local rigidity near F union M_n F Mx; A/AH strictly excluded, G/GH/HB/HBH permitted ONLY at the lower corner. Every parent has a spatial preimage on every support edge; complete receiver-corner preimages are NOT assumed for G/GH/HB/HBH. Sources outside closed collars unclassified.'}
    sha=g.digest(math)
    if verify_expected:
        expected=json.loads((HERE/'EXPECTED.json').read_text())
        g.require(sha==expected['all_math_sha256'] and math['certificate_canonical_sha256']==expected['certificate_canonical_sha256'],'full regenerated mathematical record and compact expected fingerprints')
        g.require(sum(r['exact_control_count'] for r in duals)==expected['exact_controls'] and sum(len(r['zero_cofactor_controls']) for r in duals)==expected['genuine_zero_cofactor_controls'],'every closed control and genuine zero retained')
    return {'all_math_sha256':sha,'mathematics':math,'wall_seconds':time.monotonic()-start}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--emit',action='store_true');args=parser.parse_args();r=complete_record(not args.emit);Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'all_math_sha256':r['all_math_sha256'],'controls':sum(d['exact_control_count'] for d in r['mathematics']['dual_records']),'semantic_damages_rejected':r['mathematics']['semantic_controls']['semantic_damages_rejected'],'wall_seconds':r['wall_seconds']},indent=2))
