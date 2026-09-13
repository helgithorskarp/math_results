#!/usr/bin/env python3
"""Unshifted square-free fiber cardinalities and direct physical unit graphs.

No producer, event-edge-owner table, SAT solver, or numerical tolerance is used
for physical graph verification. The generator solves in u=x+2y; this checker counts square-free fibers over x
without solving the nonlinear fibers. Arithmetic libraries remain shared.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
from interface import A,HERE,physical,build,selection,pair_interface,colour_word
import roots
import direct


def fiber_audit(args):
    """Certify all distinct complex solutions by unshifted square-free fibers.

    No factorization of a nonlinear polynomial over a number field is needed.
    The certificate points are disjoint by the separating-coordinate contract.
    """
    pair,left,right,cc=args;x,y=A.sp.symbols('x y');V=roots.V
    R=A.sp.Poly(A.sp.resultant(A.expression(left,x,y),A.expression(right,x,y),y),x,domain=A.sp.QQ)
    A.need(not R.is_zero,'finite nonzero unshifted resultant')
    fiber_records=[];assigned=set();nonlinear=0
    for q0,_ in A.sp.factor_list(R)[1]:
        qx=A.primitive(q0,x);coeff=A.coefficients(qx)
        q=physical.polynomial(coeff)
        h=V.outer_gcd(V.fiber(left,q),V.fiber(right,q),q)
        A.need(h,'no whole vertical fiber')
        dh=[i*h[i]%q for i in range(1,len(h))]
        repeated=V.outer_gcd(h[:],dh,q)
        degree=len(h)-len(repeated)
        A.need(degree>=0,'square-free fiber degree')
        if qx.degree()>1 and len(h)>2:nonlinear+=1
        keys=[];count=0
        for c in cc:
            field_q,xx=[physical.polynomial(c[k]) for k in ('q','x')]
            value=physical.polynomial([])
            for v in reversed(coeff):value=(value*xx+physical.polynomial([v]))%field_q
            if value:continue
            A.need(c['key'] not in assigned,'unique x projection factor')
            ev=A.evaluator(c);A.need(ev(left) and ev(right),'claimed point solves both original equations')
            assigned.add(c['key']);keys.append(c['key']);count+=len(c['q'])-1
        A.need(count==qx.degree()*degree,'complete square-free fiber coverage')
        fiber_records.append([coeff,len(h)-1,degree,sorted(keys)])
    A.need(assigned=={c['key'] for c in cc},'every claimed component covered')
    return {'pair':list(pair),'fibers':fiber_records,'nonlinear_nonrational_fibers':nonlinear}


def coverage(pairs,factors,certificate,jobs):
    A.need(len(certificate['pairs'])==len(pairs),'number of anchor pairs')
    records={c['key']:c for c in certificate['components']}
    A.need(len(records)==len(certificate['components']),'distinct component records')
    used=set();tasks=[]
    for pair,claimed in zip(pairs,certificate['pairs']):
        A.need(claimed['pair']==list(pair),'ordered anchor pair')
        keys=claimed['components'];A.need(keys==sorted(set(keys)) and set(keys)<=set(records),'distinct known pair components')
        used.update(keys);a,b=pair;tasks.append((pair,factors[a],factors[b],[records[k] for k in keys]))
    A.need(used==set(records),'exact union of anchor components')
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        transcript=list(pool.map(fiber_audit,tasks,chunksize=1))
    fields={k:{name:c[name] for name in ('q','x','y')} for k,c in records.items()}
    audit={'unshifted_fiber_transcript_sha256':A.digest(transcript),
           'nonlinear_nonrational_fibers':sum(t['nonlinear_nonrational_fibers'] for t in transcript),
           'pairs_with_nonlinear_nonrational_fibers':sum(t['nonlinear_nonrational_fibers']>0 for t in transcript)}
    return fields,records,audit


def concurrency(selected,incidence,records):
    bypair={tuple(r['pair']):r['components'] for r in incidence};transcript=[]
    for idx,domains,pairs in selected:
        for pair in pairs:
            for key in bypair[pair]:
                active=set(records[key]['active_curves'])
                sections=[[i for i in d if i in active] for d in domains]
                A.need(not all(sections),'full five-section complex concurrence')
                transcript.append([idx,list(pair),key,sections])
    return len(transcript),A.digest(transcript)


FACTORS=None
LITERAL=False

def initialize(factors,literal=False):
    global FACTORS,LITERAL
    FACTORS=factors;LITERAL=literal


def check_field(c):
    field={k:c[k] for k in ('q','x','y')};key=A.digest(field)
    A.need(c['key']==key,'component key')
    variable=A.sp.Symbol('s')
    polynomials=[A.sp.Poly(sum(A.sp.Rational(v)*variable**i for i,v in enumerate(field[k])),variable,domain=A.sp.QQ) for k in ('q','x','y')]
    qq,px,py=polynomials
    A.need(A.coefficients(A.primitive(qq,variable))==field['q'] and A.coefficients(px.rem(qq))==field['x'] and A.coefficients(py.rem(qq))==field['y'],'canonical primitive reduced field')
    nr=roots.nreal(field);A.need(c['real_embeddings']==nr,'real embedding count')
    # These canonical shapes make distinct component records disjoint in (x,y).
    deg=len(c['q'])-1
    q,xx,yy=[physical.polynomial(c[k]) for k in ('q','x','y')]
    u=(xx+roots.SHEAR*yy)%q;parameter=physical.polynomial([0,1])
    A.need((deg==1 and c['q']==['0','1'] and len(c['x'])==len(c['y'])==1) or
           (deg>1 and (u==parameter or (u.degree()<=0 and yy==parameter))),'canonical separating coordinate')
    ev=A.evaluator(field);active=[i for i,f in enumerate(FACTORS) if ev(f)]
    A.need(c['active_curves']==active,'all active norm events')
    if not nr:return {'key':key,'nreal':0,'degree':deg,'active':len(active)}
    points,labels,edges,triangle=physical.graph(field) if LITERAL else direct.graph(field)[:4]
    A.need(c['point_count']==len(points) and c['edge_count']==len(edges),'physical graph counts')
    A.need(c['edge_sha256']==A.digest(edges),'complete direct physical unit edges')
    A.need(c['label_map_sha256']==A.digest(labels),'complete physical collision quotient')
    word=colour_word(c['colour_weights'],labels,len(points))
    physical.check_word(word,len(points),edges)
    return {'key':key,'nreal':nr,'degree':deg,'active':len(active),'vertices':len(points),'edges':len(edges),'weights':c['colour_weights'],'unit_circle':ev(((0,0,-1),(2,0,1),(0,2,3)))}


def verify(residual,certificate_path,jobs,literal=False):
    certificate=json.loads(Path(certificate_path).read_text())
    A.need(certificate['schema']=='hn-four-power-binomial-pencils-v1','schema')
    factors,_,_,buckets,_=build();pencils=selection(buckets,residual);selected,pairs=pair_interface(pencils,buckets)
    A.need(certificate['source_residual_sha256']==A.RESIDUAL_HASH and certificate['curve_inventory_sha256']==A.digest(factors),'source hashes')
    A.need(certificate['pencil_interface_sha256']==A.digest([[i,p] for i,p in pencils]),'pencil interface')
    fields,records,audit=coverage(pairs,factors,certificate,jobs)
    with ProcessPoolExecutor(max_workers=jobs,initializer=initialize,initargs=(factors,literal)) as pool:
        results=list(pool.map(check_field,[records[k] for k in sorted(records)],chunksize=1))
    ninc,transcript=concurrency(selected,certificate['pairs'],records)
    graph_hist=Counter();degree_hist=Counter();active_hist=Counter();weight_hist=Counter()
    for c in results:
        n=c['nreal']
        if n:
            graph_hist[f"{c['vertices']}v_{c['edges']}e"]+=n
            degree_hist[str(c['degree'])]+=n;active_hist[str(c['active'])]+=n
            weight_hist[''.join(map(str,c['weights']))]+=n
    return dict(audit,**{'status':'PASS','pencils':len(pencils),'raw_lifts':387072,'anchor_pairs':len(pairs),'distinct_complex_components':len(fields),
            'components_with_pair_incidence':sum(len(r['components']) for r in certificate['pairs']),
            'components_with_pencil_pair_incidence':ninc,'complex_concurrences':0,'real_components':sum(c['nreal']>0 for c in results),
            'distinct_real_parameters':sum(c['nreal'] for c in results),'all_physical_chromatic_numbers':3,
            'physical_graph_histogram_by_parameter':dict(sorted(graph_hist.items())),
            'active_curve_histogram_by_parameter':dict(sorted(active_hist.items())),
            'degree_histogram_by_parameter':dict(sorted(degree_hist.items())),
            'linear_colour_weight_histogram_by_parameter':dict(sorted(weight_hist.items())),
            'concurrency_transcript_sha256':transcript,'physical_transcript_sha256':A.digest(results),
            'certificate_sha256':hashlib.sha256(Path(certificate_path).read_bytes()).hexdigest()})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);p.add_argument('--check-expected',action='store_true');p.add_argument('--literal-distances',action='store_true');args=p.parse_args()
    A.need(1<=args.jobs<=8,'bounded worker count');result=verify(args.residual,args.certificate,args.jobs,args.literal_distances)
    if args.check_expected:A.need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected complete result')
    print(json.dumps(result,sort_keys=True,indent=2))
