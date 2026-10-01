"""Exact finite hypotheses for a J74 source-support transition.

Python3.11+ standard library. This checks the complete finite certificate
and replays the complete pinned parent record. The uniform Cayley argument
and real-parameter implications are written in PROOF.md, not formalized.
"""
from fractions import Fraction as F
from pathlib import Path
import copy, hashlib, json, math, sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from q5 import Q, add, sub, scale, dot, cross
from model import VERTICES as V
from nonlocal_receiving_patch import check as patch
from nonlocal_arc_wrench.check import field, vector, encoded

def require(ok,message):
    if not ok:raise ValueError(message)

def apply(columns,v):
    return tuple(sum((col[i]*v[j] for j,col in enumerate(columns)),Q()) for i in range(3))

def diagonal(v,signs):return tuple(Q(s)*x for s,x in zip(signs,v))

def replay_patch(dependencies):
    for name,expected in dependencies['pinned_input_sha256'].items():
        observed=hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()
        require(observed==expected,'pinned input '+name)
    parent_dir=HERE.parent/'nonlocal_receiving_patch'
    old,old_record=patch.replay_parent(json.loads((parent_dir/'DEPENDENCIES.json').read_text()))
    raw=(parent_dir/'certificate.json').read_bytes();cert=json.loads(raw)
    record=patch.evaluate(cert,old)
    record['parent_full_record_replayed']=True
    record['parent_certificate_sha256']=old_record['certificate_sha256']
    record['parent_expected_sha256']=hashlib.sha256((HERE.parent/'nonlocal_arc_wrench/expected.json').read_bytes()).hexdigest()
    record['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    record['negative_controls']=patch.damaged_controls(cert,old)
    require(record==json.loads((parent_dir/'expected.json').read_text()),'complete published patch finite record')
    return cert,record

def separation_bound(columns,m,d,e,lo,hi,eps,signs,radius):
    """Tensor Bernstein bound for (3-r^2)||u||^2-tr(Q0 S^t)||u||^2.

    Here S=M_u H, D=Q0 H, and tr(D M_u)=tr(D)-2*u.Du/||u||^2.
    Independent box parameters x,y are in [0,1]. All nine Bernstein
    coefficients are returned; their minimum is a uniform lower bound.
    """
    D=[scale(Q(signs[j]),col) for j,col in enumerate(columns)]
    tr=sum((D[i][i] for i in range(3)),Q())
    basis=[add(add(m,scale(lo,d)),scale(-eps,e)),scale(hi-lo,d),scale(2*eps,e)]
    exponent=[(0,0),(1,0),(0,1)];power={}
    for i,x in enumerate(basis):
        for j,y in enumerate(basis):
            p,q=exponent[i][0]+exponent[j][0],exponent[i][1]+exponent[j][1]
            power[p,q]=power.get((p,q),Q())+(3-radius*radius-tr)*dot(x,y)+2*dot(x,apply(D,y))
    return [sum((coefficient*F(math.comb(i,p),math.comb(2,p))*F(math.comb(j,q),math.comb(2,q))
                 for (p,q),coefficient in power.items() if p<=i and q<=j),Q())
            for i in range(3) for j in range(3)]

def evaluate(cert,parent):
    require(cert['schema']==1,'certificate schema')
    m,d,e=[vector(parent[k]) for k in ('m','d','transverse_vector')]
    lo,hi=map(lambda x:Q(F(x)),parent['t_interval']);eps=Q(F(parent['transverse_radius']))
    require((lo,hi,eps)==(Q(F(3,5)),Q(F(7,10)),Q(F(1,50000))),'exact pinned receiving domain')
    require(dot(m,m)==1,'unit reflection normal')
    octants=[add(add(m,scale(t,d)),scale(s,e)) for t in (lo,hi) for s in (-eps,eps)]
    require(all(u[0]>0 and u[1]<0 and u[2]<0 for u in octants),
            'strict receiving octant at all four box corners')
    columns=[vector(col) for col in cert['proper_motion_columns']]
    require(len(columns)==3 and all(len(col)==3 for col in columns),'three full spatial matrix columns')
    require(all(dot(a,b)==(1 if i==j else 0) for i,a in enumerate(columns) for j,b in enumerate(columns)),
            'full spatial orthogonality')
    require(dot(columns[0],cross(columns[1],columns[2]))==1,'proper spatial motion')
    identity=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1))]
    expected=[sub(v,scale(2*dot(m,v),m)) for v in [identity[0],scale(-1,identity[1]),identity[2]]]
    require(columns==expected,'literal Q0=M_m Hy')
    require(all(x>0 for x in columns[0]) and columns[1][0]<0 and columns[1][1]<0 and columns[1][2]>0,
            'fixed source column octants excluding reflected-center coincidences')
    images=[apply(columns,v) for v in V]
    require(len(V)==len(images)==len(set(images))==60,'all sixty original source vertices')
    require(all(dot(v,v)==Q(11,4)/4 for v in images),'actual common source circumradius')
    require(set(images)!=set(V),'fixed Q0 is not a full-body symmetry')

    cycle=parent['receiver_cycle'];preimages=cert['literal_corner_preimages']
    require(len(preimages)==len(set(preimages))==len(cycle)==18,'complete injective corner preimages')
    require(all(isinstance(k,int) and 0<=k<60 and images[k]==V[i] for i,k in zip(cycle,preimages)),
            'all eighteen literal original spatial corner images')
    signs=cert['companion_body_diagonals']
    require(len(signs)==3,'three companion body symmetries')
    for s in signs:
        require(len(s)==3 and all(x in (-1,1) for x in s),'orthogonal body diagonal')
        require({diagonal(v,s) for v in V}==set(V),'actual full-body companion symmetry')
    require(signs==[[-1,-1,1],[-1,1,1],[1,-1,1]],'G,Hx,Hy companion order')
    require(math.prod(signs[0])==1 and all(math.prod(s)==-1 for s in signs[1:]),
            'correct properness of all four full-source centers')
    for i,k in zip(cycle,preimages):
        for s in signs:
            q=diagonal(V[k],s)
            require(q in V and apply(columns,diagonal(q,s))==V[i],
                    'original preimages for every fixed/reflected companion contact')

    radius=F(cert['relative_cayley_radius'])
    span=Q(2160)
    contraction=span*F(81,32)*radius
    require(radius>0 and contraction<1,'uniform nonlinear Cayley absorption')
    require(radius==F(parent['relative_cayley_radius'])==F(1,14400),'unchanged conditional source radius')

    intercept,slope=map(field,(cert['frontier_intercept'],cert['frontier_slope']))
    require(intercept==Q(-1,1)/2 and slope==Q(-3,1)/4,'exact sloped transition line')
    polygon=[tuple(field(x) for x in p) for p in cert['feasible_polygon']]
    expected_polygon=[(lo,-eps),(intercept-slope*eps,-eps),(intercept+slope*eps,eps),(lo,eps)]
    # First check the actual containment gates; equality with the literal
    # quadrilateral is checked afterward, so expansion controls must protrude.
    require(len(polygon)==4 and all(len(p)==2 for p in polygon),'four full parameter vertices')
    require(all(lo<intercept+slope*s<hi for s in (-eps,eps)),
            'transition cuts both opposite sides inside the original box')
    edges=list(zip(cycle,cycle[1:]+cycle[:1]));constraints=[]
    for a,b in edges:
        delta=sub(V[b],V[a])
        for k,image in enumerate(images):
            coefficients=[dot(cross(delta,u),sub(V[a],image)) for u in (m,d,e)]
            constraints.append(([a,b,k],coefficients))
    require(len(constraints)==18*60==1080,'complete actual-original source inequalities')
    witness=cert['event_witness'];require(witness in [w for w,c in constraints],'actual transition witness')
    event=next(c for w,c in constraints if w==witness)
    require(event==[field(x) for x in cert['event_gap_coefficients']], 'literal actual source-support polynomial')
    require(event==[intercept/2,Q(-1)/2,slope/2], 'support event exactly half the claimed frontier form')
    require(witness==[17,32,39],'named original transition witness')
    zero=[];minimum_strict=None;comparisons=strict=zeros=0
    for w,c in constraints:
        persistent=all(x==0 for x in c)
        if persistent:zero.append(w)
        for t,s in polygon:
            gap=c[0]+c[1]*t+c[2]*s;comparisons+=1
            require(gap>=0,'all sixty ORIGINAL source supports at every feasible vertex')
            if gap>0:strict+=1
            else:zeros+=1
            if not persistent and w!=witness:
                require(gap>0,'no hidden additional transition on the quadrilateral')
                minimum_strict=gap if minimum_strict is None else min(minimum_strict,gap)
    corner_map=dict(zip(cycle,preimages))
    expected_zero=sorted([a,b,corner_map[k]] for a,b in edges for k in (a,b))
    require(sorted(zero)==expected_zero,'exact thirty-six persistent actual endpoint constraints')
    require(polygon==expected_polygon,'entire exact quadrilateral, all four closed boundaries')
    require((comparisons,strict,zeros)==(4320,4174,146),'complete source support sign accounting')

    separation=Q(F(cert['old_center_operator_separation']))
    require(separation>0,'positive separation from original center families')
    fixed=[3-separation*separation-sum((columns[i][i]*s[i] for i in range(3)),Q())
           for s in ((1,1,1),(-1,-1,1))]
    require(min(fixed)>0,'operator separation from fixed old centers I,G')
    bernstein=[separation_bound(columns,m,d,e,lo,hi,eps,s,separation) for s in signs[1:]]
    require(all(min(row)>0 for row in bernstein),'uniform operator separation from both moving old centers')
    require(separation==Q(F(1,2)),'literal operator separation threshold')
    require(4*radius<F(1,2),'the new and old conditional motion neighborhoods are disjoint')
    return {'agent':'six-rupert-2','role':'researcher',
      'finite_hypotheses':'PASS; full written real-parameter Cayley proof in PROOF.md, unformalized',
      'receiving_domain':'3/5<=t<=7/10,|s|<=1/50000; u=m+t*d+s*(m cross d)',
      'source_domain':'four additional conditional proper-motion neighborhoods, not all sources',
      'relative_cayley_radius':str(radius),'nonlinear_contraction':str(contraction.a),
      'proper_motion_columns':cert['proper_motion_columns'],'original_spatial_corner_preimages':preimages,
      'receiving_box_octant':'(+,-,-); four affine corner sign checks',
      'full_body_companion_vertex_checks':180,'event_witness':witness,
      'event_gap_coefficients':cert['event_gap_coefficients'],
      'feasible_halfplane':'t<=(sqrt5-1)/2+((sqrt5-3)/4)*s',
      'closed_feasible_polygon':cert['feasible_polygon'],
      'all_original_source_affine_constraints':len(constraints),'feasible_vertex_support_comparisons':comparisons,
      'strict_feasible_vertex_support_comparisons':strict,'zero_feasible_vertex_support_comparisons':zeros,
      'persistent_original_endpoint_constraints':zero,'strict_other_constraint_minimum':encoded(minimum_strict),
      'old_center_operator_separation':'>1/2','fixed_old_separation_gates':[encoded(x) for x in fixed],
      'moving_old_separation_tensor_bernstein':[[encoded(x) for x in row] for row in bernstein],
      'branch_transition':'every continuous closed lambda>=1 path inside the receiving patch starting at one new center stays on that center family and cannot cross into the infeasible halfplane',
      'global_J74_Rupert_status':'OPEN'}

def damaged_controls(cert,parent):
    results=[]
    names=['improper_motion','false_original_preimage','nonbody_companion','wrong_event_original',
           'freeze_zero_transverse_event','expanded_feasible_polygon','unsafe_motion_radius','false_old_separation']
    for name in names:
        bad=copy.deepcopy(cert)
        if name=='improper_motion':
            bad['proper_motion_columns'][0]=[encoded(-field(x)) for x in bad['proper_motion_columns'][0]]
        elif name=='false_original_preimage':bad['literal_corner_preimages'][0]=54
        elif name=='nonbody_companion':bad['companion_body_diagonals'][1]=[1,1,-1]
        elif name=='wrong_event_original':bad['event_witness']=[17,32,38]
        elif name=='freeze_zero_transverse_event':bad['event_gap_coefficients'][2]=['0','0']
        elif name=='expanded_feasible_polygon':
            bad['feasible_polygon'][1][0]=encoded(field(bad['feasible_polygon'][1][0])+Q(F(1,500000)))
        elif name=='unsafe_motion_radius':bad['relative_cayley_radius']='1/4000'
        else:bad['old_center_operator_separation']='1'
        try:evaluate(bad,parent)
        except (ValueError,IndexError,KeyError,ZeroDivisionError) as error:
            results.append({'control':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('unsafe damaged control accepted: '+name)
    return results

def main():
    dependencies=json.loads((HERE/'DEPENDENCIES.json').read_text())
    parent,parent_record=replay_patch(dependencies)
    raw=(HERE/'certificate.json').read_bytes();cert=json.loads(raw)
    result=evaluate(cert,parent)
    result['parent_complete_finite_record_replayed']=True
    result['parent_certificate_sha256']=parent_record['certificate_sha256']
    result['parent_expected_sha256']=hashlib.sha256((HERE.parent/'nonlocal_receiving_patch/expected.json').read_bytes()).hexdigest()
    result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    result['negative_controls']=damaged_controls(cert,parent)
    if '--write-expected' in sys.argv:(HERE/'expected.json').write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads((HERE/'expected.json').read_text()),'complete frozen expected record')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
