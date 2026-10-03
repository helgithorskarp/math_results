"""Whole finite physical-basis binding to the independent all-h forms."""
from fractions import Fraction as F
import argparse,json
from pathlib import Path
import original as exact
import symbolic as generic

def rational(expr,h):
    x=expr.subs(generic.h,h)
    return F(int(x.p),int(x.q))

def control(h,forms):
    record,internal=exact.original(h,keep_internal=True)
    names=internal['names']; metric=internal['metric']; rows=internal['rows']
    index={x:i for i,x in enumerate(names)}; n=len(names)
    vectors=[]; blocks=[]
    def vec(terms):
        v=[F(0)]*n
        for name,coef in terms: v[index[name]]+=F(coef)
        return v
    def block(name,basis,scale=F(1)):
        lo=len(vectors); vectors.extend(basis); blocks.append((name,lo,len(vectors),scale))
    for group in range(2):
        for i in range(h):
            block('leaf',[vec([(('T',group,i,0),1),(('T',group,i,1),-1)]),
                          vec([(('WA',group,i),1)])])
    for group in range(2):
        for k in range(1,h):
            profile=[1]*k+[-k]+[0]*(h-k-1)
            basis=[]
            for kind in ['B','T','WF','M']:
                terms=[]
                for i,t in enumerate(profile):
                    if kind=='T': terms += [(('T',group,i,j),t*x) for j,x in enumerate([1,1,-2])]
                    else: terms.append(((kind,group,i),t))
                basis.append(vec(terms))
            block('standard',basis,F(k*(k+1),2))
    allblocks=generic.basis_blocks()
    for name in ['even','odd','untouched']:
        converted=[]
        for v in allblocks[name]:
            terms=[(('old',mask),rational(v['old'][mask-1],h)) for mask in range(1,8)]
            for group in range(2):
                for i in range(h):
                    category=i if i<2 else 2
                    for kind in ['B','M','WA','WF']:
                        terms.append(((kind,group,i),rational(v[kind][group][category],h)))
                    for j in range(3):
                        terms.append((('T',group,i,j),rational(v['T'][group][category][j],h)))
            converted.append(vec(terms))
        block(name,converted)
    size=len(vectors)
    exact.require(size==12*h+4,'whole physical basis cardinality')
    vm=[[sum((vector[k]*metric[k][j] for k in range(n) if vector[k]),F(0))
         for j in range(n)] for vector in vectors]
    gram=[[sum((vm[i][k]*vectors[j][k] for k in range(n) if vectors[j][k]),F(0))
           for j in range(size)] for i in range(size)]
    dots=[[sum((row[k]*vm[j][k] for k in range(n) if row[k]),F(0))
           for j in range(size)] for row in rows]
    frame=[[sum((row[i]*row[j] for row in dots),F(0)) for j in range(size)] for i in range(size)]
    expected_gram=[[F(0)]*size for _ in range(size)]
    expected_frame=[[F(0)]*size for _ in range(size)]
    for name,lo,hi,scale in blocks:
        for i in range(hi-lo):
            for j in range(hi-lo):
                expected_gram[lo+i][lo+j]=scale*rational(forms[name]['metric'][i,j],h)
                expected_frame[lo+i][lo+j]=scale*rational(forms[name]['frame'][i,j],h)
    exact.require(gram==expected_gram,'ENTIRE original physical basis Gram binding')
    exact.require(frame==expected_frame,'ENTIRE original physical frame binding incl empty/cross entries')
    exact.require(exact.rank_psd(gram)[0]==size,'ENTIRE physical basis independence')
    cap=[[(record['N']-1)*gram[i][j]-frame[i][j] for j in range(size)] for i in range(size)]
    exact.require(exact.rank_psd(cap)[0]==size,'ENTIRE physical cap floor')
    return dict(h=h,basis_dimension=size,primitive_dimension=n,
                all_original_vertices=len(rows),all_gram_entries=size**2,
                all_frame_entries=size**2,blocks=blocks,
                whole_basis_coordinates_digest=exact.digest(vectors),
                whole_basis_gram_digest=exact.digest(gram),
                whole_original_frame_digest=exact.digest(frame),
                whole_physical_cap_digest=exact.digest(cap))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    forms=generic.frame_forms(generic.basis_blocks())
    record=dict(schema='reviewer5-q4-balanced-whole-physical-binding-v1',
                controls=[control(2,forms),control(3,forms)])
    payload=exact.canonical(record); args.output.write_bytes(payload)
    print(json.dumps(dict(status='all original full physical bases and frame positions bind exactly',
                          whole_record_bytes=len(payload),whole_record_sha256=exact.hashlib.sha256(payload).hexdigest()),sort_keys=True))

if __name__=='__main__': main()
