"""Exact seven-core stability checker using the pinned complete parent proof.

Six-tammes-2, researcher, 2026-10-01. All signs and RHS transfers are exact;
no search optimizer or floating approximation is a verification input.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import lcm
import hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'tammes15_octagon_model2_extension_exclusion'

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def read_config():
    config=json.loads((HERE/'certificate.json').read_text())
    need(config['format']==1 and config['real_core_labels']==list(range(1,8)) and config['auxiliary_label']==0,'fixed real and auxiliary labels')
    need(config['closed_interval']==[[29,50],[593,1000]],'fixed complete closed interval')
    need(config['upstream_directory']==BASE.name,'fixed published prerequisite')
    for name,expected in config['upstream_source_sha256'].items():
        need(Path(name).name==name and hashlib.sha256((BASE/name).read_bytes()).hexdigest()==expected,'pinned upstream source '+name)
    epsilon=Q(*config['epsilon'])
    need(epsilon>0,'strictly positive radius')
    return config,epsilon

def verify(config,epsilon):
    sys.path.insert(0,str(BASE))
    spec=importlib.util.spec_from_file_location('parent_octagon_check',BASE/'check.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    from certificates import Rows,verify_dual
    from model import box_bounds,gmetric
    data=json.loads((BASE/'certificate.json').read_text())
    old,leaves,adjacency,discards,deletions,active,rmins,integer=parent.verify(data,details=True)
    lo,hi=parent.LO,parent.HI
    # On this strip the two eigenvalues of G(t), 1-t and 1+t-2t^2,
    # decrease. R(t,z)<=R(lo,z); a convex quadratic reaches its maximum
    # on a rectangle at a corner. D(t)<=(1+hi)^3.
    need(lo>=Q(1,4) and hi<1,'decreasing positive chart Gram eigenvalues')
    def denominator_bound(c):
        lower,upper=box_bounds(tuple(c))
        return (1+hi)**3*(1+max(gmetric((u,v),lo) for u,v in product(*zip(lower,upper))))
    rational=parent.t_bernstein_forms(2,lo,hi)
    den=lcm(*(z.denominator for p in rational[0] for z in p))
    grid=2**(max(c[0] for c in leaves+[tuple(z) for z in data['refined_cells']])+1-3)
    bernstein=[]
    for c,method,label in discards:
        if method!='bernstein' or label!=0:continue
        d,i,j=c;h=8*grid//2**d;u=-4*grid+i*h;v=-4*grid+j*h
        values=[]
        for f,l,m,a,b in integer[0]:
            c00=4*f*grid**2+4*l*u*grid+4*m*v*grid+4*a*(u*u+v*v)+4*b*u*v
            c10=2*h*(l*grid+2*a*u+b*v);c01=2*h*(m*grid+2*a*v+b*u)
            c20=4*h*h*a;c11=h*h*b
            for r,s in product(range(3),repeat=2):
                values.append(c00+r*c10+s*c01+(int(r==2)+int(s==2))*c20+r*s*c11)
        margin=Q(min(values),4*den*grid**2);factor=denominator_bound(c)
        relaxed=margin-epsilon*factor
        need(relaxed>0,'strict relaxed label-zero Bernstein margin '+str(c))
        bernstein.append([list(c),str(margin),str(factor),str(relaxed)])
    rows=Rows(lo,hi);duals=[];gaps=[];affected=0
    for kind,certificates in [('single',data['single_cells']),('pair',data['conditioned_pairs'])]:
        for z in certificates:
            if kind=='single':
                cells=[tuple(z['cell'])];system=rows.single(cells[0]);indices=(0,);nvars=3
            else:
                cells=list(map(tuple,z['cells']));system=rows.pair(*cells);indices=(0,8);nvars=5
            original=verify_dual(system,z)
            factors={index:denominator_bound(c) for index,c in zip(indices,cells)}
            weight=sum((Q(w)*factors[k] for k,w in zip(z['support'],z['weights']) if k in factors),Q(0))
            relaxed=original+epsilon*weight
            need(relaxed<0,'strict relaxed dual RHS')
            gaps.append(relaxed);affected+=int(weight>0)
            duals.append([nvars,[list(c) for c in cells],str(original),str(weight),str(relaxed)])
    # Every earlier omitted region and pair cut remains justified. Therefore
    # the complete old cover, capacity tests, graph and no-K7 proof are also
    # the necessary cover/graph proof for the weaker auxiliary inequality.
    return {'agent':'six-tammes-2','role':'researcher',
            'status':'AUTHOR_AUDITED_EXACT_SEVEN_CORE_OMITTED_POINT_STABILITY',
            'certified_closed_interval':data['interval'],'epsilon':str(epsilon),
            'actual_core_size':7,'actual_extra_points':8,'auxiliary_extension_points':7,
            'relaxed_label_zero_Bernstein_discards':len(bernstein),
            'minimum_label_zero_relaxed_Bernstein_margin':min((z[3] for z in bernstein),key=Q),
            'Bernstein_transfer_sha256':digest(bernstein),'dual_transfer_sha256':digest(duals),
            'single_cell_certificates':len(data['single_cells']),
            'conditioned_pairs':len(data['conditioned_pairs']),'affected_duals':affected,
            'maximum_affine_rhs':str(max(gaps)),
            'cover_cells':old['cover_cells'],'discarded_cells':old['discarded_cells'],
            'basic_edges':old['basic_edges'],'compatibility_edges':old['compatibility_edges'],
            'domination_deletions':old['domination_deletions'],'reduced_vertices':old['reduced_vertices'],
            'clique_search_states':old['clique_search_states'],
            'tree_sha256':old['tree_sha256'],'graph_sha256':old['graph_sha256'],
            'domination_sha256':old['domination_sha256'],
            'core_coordinates_sha256':old['core_coordinates_sha256'],
            'certificate_sha256':hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),
            'point_distance_statement':'Every actual extra point is at Euclidean chord distance strictly greater than epsilon from auxiliary p0(t).',
            'global_tammes15_bounds':'unchanged','independent_peer_review':'pending',
            'trust_boundary':'Pinned complete parent proof plus exact local margin transfer; written reflection/chart/Cauchy--Schwarz reduction, not formalized.'}

if __name__=='__main__':
    config,epsilon=read_config()
    result=verify(config,epsilon)
    expected_path=HERE/'EXPECTED.json'
    if expected_path.exists():
        expected=json.loads(expected_path.read_text())
        need(result==expected,'complete expected primary receipt')
    print(json.dumps(result,indent=2,sort_keys=True))
