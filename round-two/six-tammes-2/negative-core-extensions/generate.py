"""Check every active triple on each closed dyadic plan cell.

Bulk witness output is optional and belongs outside the publication directory.
Every incomplete cell or runtime guard is an error, never a theorem.
"""
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,time
import polytope as p
HERE=Path(__file__).resolve().parent
def cells(plan=None):
    if plan is None:plan=json.loads((HERE/'PLAN.json').read_text())
    p.e.require(plan['format']==1 and plan['domain']==[str(p.LO),str(p.HI)],'literal plan domain')
    p.e.require(plan['label_order']==list(p.LABELS),'literal label order')
    p.e.require(len(plan['cells'])==95,'literal finite cell count')
    rows=[]
    for depth,index in plan['cells']:
        p.e.require(type(depth)is int and type(index)is int and 0<=depth<=8 and 0<=index<2**depth,
                    'valid dyadic cell')
        a=p.LO+(p.HI-p.LO)*p.Q(index,2**depth)
        b=p.LO+(p.HI-p.LO)*p.Q(index+1,2**depth)
        rows.append((a,b,depth,index))
    p.e.require(rows[0][0]==p.LO and rows[-1][1]==p.HI,'closed endpoints covered')
    p.e.require(all(a[1]==b[0] for a,b in zip(rows,rows[1:])),'ordered gap-free interval partition')
    return rows
def produce(audit=False,trace_path=None):
    if audit:
        import audit as independent
    start=time.monotonic();digest=hashlib.sha256();counts=Counter();worst=0;min_nn=None
    anchor=p.Q(117,200);qa,qb=p.root(anchor,anchor,48)
    original,anchor_H=p.e.build(p.I(anchor),p.I(qa,qb),-1)
    orientation=sum((a*b for a,b in zip(original[9],p.e.cross(original[6],original[10]))),p.I())
    p.e.require(orientation.l>0,'original selected model has the positive square-root orientation')
    records=[]
    for number,(a,b,depth,index) in enumerate(cells()):
        if time.monotonic()-start>160:raise RuntimeError('160-second guard: incomplete certificate')
        A,rhs,H,br,nn,model=p.geometry(a,b)
        min_nn=nn if min_nn is None else min(min_nn,nn)
        cert=[]
        for triple in p.TRIPLES:
            result=p.classify(triple,A,rhs,H)
            if result is None:result=p.cut_gram_norm(triple,model)
            if result is None:result=p.classify_centered(triple,model)
            p.e.require(result is not None,'unresolved cell '+str((depth,index,triple)))
            if audit:independent.verify(triple,result,A,rhs,H,model)
            counts[result[0]]+=1
            if result[0] in ('norm','mvt-norm','gram-norm'):worst=max(worst,result[1])
            cert.append([list(triple),result])
        record={'cell':[depth,index],'q_bracket':[str(x) for x in br],
                'normal_norm2_lower':nn,'certificates':cert}
        digest.update(json.dumps(record,sort_keys=True,separators=(',',':')).encode()+b'\n')
        if trace_path:records.append(record)
    p.e.require(worst<p.S,'strict norm threshold')
    if trace_path:Path(trace_path).write_text(json.dumps(records,sort_keys=True)+'\n')
    return {'status':'ALL_CLOSED_CELLS_AND_TRIPLES_CHECKED','cells':95,'triples_per_cell':364,
            'total_triples':95*364,'dyadic_scale':str(p.S),'witness_counts':dict(counts),
            'largest_strict_norm_upper':str(worst),'strict_norm_margin_lower':str(p.Q(p.S-worst,p.S)),
            'normal_norm2_lower':str(p.Q(min_nn,p.S)),'canonical_witness_sha256':digest.hexdigest(),
            'separate_same_author_witness_audit':audit,
            'original_branch_orientation_lower':str(p.Q(orientation.l,p.S)),
            'critical_analytic_dependency':9003,
            'original_curve_dependency':8929}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--audit',action='store_true')
    parser.add_argument('--trace',type=Path);args=parser.parse_args()
    print(json.dumps(produce(args.audit,args.trace),sort_keys=True))
