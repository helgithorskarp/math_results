"""Replay the whole cap certificate using exact rational Bernstein signs.

The alternate audit uses rational centered Taylor enclosures instead.
Both share the stated coordinate/Cramer reduction and integer polynomial
kernel; they do not constitute independent mathematical peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import argparse,hashlib,json,signal
from polynomials import P,dot
from model import LABELS,CONTACTS,NORMAL,CUT,SECOND_NORMAL,SECOND_CUT,make,positive_factors
from geometry import identities,packing_obligations
from algebra import LO,HI,require,primitive,row_planes,vertex,cramer,parameter_box
from schema import system,validate
from signs import rational_bernstein,taylor_positive

HERE=Path(__file__).resolve().parent
FROZEN=('SYSTEM.json','polynomials.py','model.py','algebra.py','signs.py',
        'schema.py','generate.py','check.py','audit.py','controls.py','geometry.py')

def pins():
    data=json.loads((HERE/'RUNTIME_PINS.json').read_text());require(set(data)==set(FROZEN),'complete eleven-file runtime pins')
    for name in FROZEN:require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==data[name],name+' runtime source pin')
    require(json.loads((HERE/'SYSTEM.json').read_text())==system(),'literal source system agreement')
    return data

def scalar_bounds():
    require(0<LO<HI<1 and 3*LO-1>0 and 5*LO*LO-1>0,'all known factors and branch pruning on CLOSED band')
    low,high=621-620*HI,621-620*LO
    require(low==Q(12667,50) and high==Q(1369,5) and low>CUT*CUT,'proper first cap throughout band')
    pair=2*CUT*CUT/high-1;require(pair==Q(881,1369)>HI,'first cap at most one code point')
    low2,high2=233-232*HI,233-232*LO
    require(low2>SECOND_CUT*SECOND_CUT and SECOND_CUT>0,'proper positive second cap')
    margin=232*LO*LO-LO-71
    require(margin==Q(747,625)>0 and 464*LO-1>0,'second pointwise pair margin positive on entire CLOSED interval')
    require(LO>Q(1,2) and Q(53,8)>0,'positive cubic in sole weak core gap')
    return {'first_normal_squared_closed_bounds':[str(low),str(high)],
            'first_open_cap_pair_product_strict_lower':str(pair),
            'second_normal_squared_closed_bounds':[str(low2),str(high2)],
            'second_pointwise_pair_margin_numerator':'232t^2-t-71',
            'second_margin_numerator_uniform_lower':str(margin),
            'both_caps_at_most_one_code_point':True,'short_vertex_squared_bound':'49/50',
            'other_branch_packing2_violation_strict':True,
            'positive_denominators':'(1+t)^5 Q4 L; both reflected plane denominators strictly positive'}

def obligations(c):
    t=P.var(0);known=positive_factors(t);planes,Y,O=row_planes(t)
    labels=(0,4,9,11);M=[[Y[labels[j]][i] for j in range(3)] for i in range(3)]
    D,C=cramer(M,[-x for x in Y[11]],t);sgn=c['boundedness_determinant_sign']
    require(bool(D.c) and len(C)==3,'spanning boundedness normals')
    for name,p in packing_obligations():yield name,p,LO,HI
    for j,p in enumerate([D]+C):yield 'positive-dependence-'+str(j),primitive(sgn*p,known),LO,HI
    for record in c['records']:
        inds=tuple(record['triple']);D,W=vertex(planes,inds,t)
        if record['type']=='S':require(not D.c,'singular triple is not identically singular');continue
        require(bool(D.c),'covered triple cannot be identically singular')
        N=primitive(49*D*D-50*dot(W,W,t),known);H={}
        for leaf in record['leaves']:
            a,b=parameter_box(leaf['path']);name='-'.join(map(str,inds))+':'+''.join(map(str,leaf['path']))
            if leaf['type']=='N':yield name+':short',N,a,b
            else:
                for role,sign in (('positive_residual',1),('negative_residual',-1)):
                    j=leaf[role]
                    if j not in H:
                        row,rhs=planes[j]
                        H[j]=primitive(sum((x*y for x,y in zip(row,W)),t*0)-rhs*D,known)
                    yield name+':'+role+':'+str(j),sign*H[j],a,b

def positive_control():
    """Twelve-core plus two actual additions at t=29/50, not a15-code."""
    t=Q(29,50);Y,O,_=make(t);Pnt={i:[x/O for x in row] for i,row in Y.items()}
    require(all(dot(x,x,t)==1 for x in Pnt.values()),'rational control12 unit norms')
    allpairs=list(combinations(LABELS,2));require(all(dot(Pnt[i],Pnt[j],t)<=t for i,j in allpairs),'all66 rational control core packing pairs')
    a=1+t;X=[(3*t*t-2*t-1)/(a*a),2*t*(1+3*t)/(a*a),-2*t/a]
    require(dot(X,X,t)==1 and all(dot(X,Pnt[i],t)<=t for i in LABELS),'auxiliary actual unit addition:all12 new comparisons')
    Pnt[13]=X
    pts=(0,4,6);rows=[[(1-t)*x+t*sum(Pnt[i],Q()) for x in Pnt[i]] for i in pts]
    # Definition-level rational Cramer, rather than a symbolic specialization.
    def det(M):
        return M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
    D=det(rows);require(D!=0,'control active-plane independence')
    v=[det([[t if j==k else rows[i][j] for j in range(3)] for i in range(3)])/D for k in range(3)]
    require(all(dot(v,x,t)<=t for x in Pnt.values()),'all13 control avoidance inequalities')
    norm=dot(v,v,t);require(norm>1,'radial projection provides an actual unit addition')
    # Scaling v by1/sqrt(norm)<1 preserves every inequality with positive RHS.
    return {'t':str(t),'prefix_unit_points':12,'prefix_packing_pairs':66,'first_actual_addition_avoidance_tests':12,
            'radial_vertex_active_labels':list(pts),'radial_vertex_squared_norm':str(norm),
            'radial_vertex_avoidance_tests':13,'two_actual_unit_additions_exist':True,
            'known_record_bound_or_new_fifteen_configuration_claimed':False}

def run(c,method='bernstein'):
    validate(c);source=pins();generic=identities();bounds=scalar_bounds();control=positive_control()
    checks=0;maximum=0;taylor_cells=0;taylor_depth=0;digest=hashlib.sha256()
    for name,p,a,b in obligations(c):
        checks+=1;maximum=max(maximum,max((k[0] for k in p.c),default=0));digest.update((name+'\n').encode())
        if method=='bernstein':require(min(rational_bernstein(p,a,b))>0,'nonpositive full-cell Bernstein obligation '+name)
        elif method=='taylor':
            cells,depth=taylor_positive(p,a,b);taylor_cells+=cells;taylor_depth=max(taylor_depth,depth)
        else:raise ValueError('explicit exact positivity method')
    require(checks==751,'all44 packing+4 boundedness+703 cap sign obligations')
    leafs=[l for r in c['records'] for l in r.get('leaves',[])]
    return {'format':'g21-two-cap-replay-v1','actual_agent':'six-tammes-2','role':'researcher',
            'claim':'12-label originalG20 plus5-12 has at most two arbitrary additional code points on closed I; no15-code',
            'method':method,'source_pins':source,'generic_identities':generic,'scalar_bounds':bounds,
            'positive_control':control,'triples_actually_checked':len(c['records']),
            'identically_singular_triples':sum(r['type']=='S' for r in c['records']),
            'complete_parameter_cover_leaves':len(leafs),'short_leaves':sum(l['type']=='N' for l in leafs),
            'opposite_residual_leaves':sum(l['type']=='I2' for l in leafs),
            'all_strict_sign_obligations_actually_checked':checks,'maximum_deflated_sign_degree':maximum,
            'ordered_obligation_names_sha256':digest.hexdigest(),'Taylor_subcells_actually_enclosed':taylor_cells,
            'Taylor_max_extra_depth':taylor_depth,'no_unresolved_cases':True,
            'formalized':False,'independent_mathematical_review':'pending'}

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second exact replay guard')));signal.alarm(50)
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json');p.add_argument('--output',type=Path);args=p.parse_args()
    out=run(json.loads(args.certificate.read_text()));raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(raw)
    print(raw,end='')
if __name__=='__main__':main()
