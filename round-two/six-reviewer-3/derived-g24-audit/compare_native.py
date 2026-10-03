#!/usr/bin/env python3
"""POST-SEAL DATA bridge: all native coordinates and certificate leaves, by Sturm.
No target executable module is imported here. The coordinate export is separate.
"""
import argparse,hashlib,itertools,json,time
from fractions import Fraction as F
from pathlib import Path
import audit as a

def verify(c,coords,system):
    a.require(set(c)=={'system','boundedness_determinant_sign','records'} and c['system']==system,'entire native certificate-system bridge')
    a.require(set(coords)=={'coordinates','Omega'},'complete coordinate export shape')
    a.require(coords['coordinates']==json.loads(json.dumps(a.reconstruct()[0])),'whole39 coordinate polynomial correspondence')
    a.require(coords['Omega']==list(a.OMEGA),'whole clearing polynomial correspondence')
    a.require(system['core_labels']==list(a.LABELS) and system['literal_contacts']==[list(e) for e in a.EDGES],'literal native mask bridge')
    a.require(system['closed_parameter_interval']==[str(a.LO),str(a.HI)] and system['all_additional_points']=='arbitrary unit vectors avoiding all13 core points','complete original domain bridge')
    a.require(system['fixed_coefficient_normal']==[-5,-14,20] and system['cut_bound']==15 and system['short_norm_squared_bound']=='49/50' and system['extra_contact_or_face_or_degree_premise_for_capacity'] is False,'cap/scope bridge')
    a.require(c['boundedness_determinant_sign']==-1,'boundedness orientation')
    y={int(i):tuple(tuple(p) for p in v) for i,v in coords['coordinates'].items()};a.boundedness(y)
    # Native planes independently reconstructed in the physical coefficient basis.
    rows={};rhs={}
    for i in a.LABELS:
        v=y[i];den=a.OMEGA
        for f in (a.A,a.Q,a.L):
            while all(not a.prem(p,f) for p in (*v,den)):
                v=tuple(a.exactdiv(p,f) for p in v);den=a.exactdiv(den,f)
        for old,new in zip(y[i],v):a.require(a.mul(new,a.OMEGA)==a.mul(old,den),'entire point row clearing')
        rows[i]=tuple(a.add(a.mul((1,-1),p),a.mul(a.T,a.sum_poly(v))) for p in v);rhs[i]=a.mul(a.T,den)
    n=((-5,),(-14,),(20,));rows[99]=tuple(a.add(a.mul((1,-1),p),a.mul(a.T,a.sum_poly(n))) for p in n);rhs[99]=(15,)
    triples=list(itertools.combinations(rows,3));a.require([r['triple'] for r in c['records']]==[list(t) for t in triples],'entire ordered364-triple bridge')
    result=[];obligations=4
    for rec in c['records']:
        keys=tuple(rec['triple']);a.require(all(type(k)is int for k in keys),'strict triple label type');d,w=a.cram([rows[k] for k in keys],[rhs[k] for k in keys])
        if rec['type']=='S':a.require(not d and set(rec)=={'type','triple'},'identically singular native record');result.append({'triple':list(keys),'singular':True});continue
        a.require(rec['type']=='COVER' and d,'covered native triple independence')
        for f in a.POS_FACTORS:
            while all(not a.prem(p,f) for p in (d,*w)):
                d,w=a.exactdiv(d,f),tuple(a.exactdiv(p,f) for p in w)
        content=0
        import math
        for p in (d,*w):content=math.gcd(content,math.gcd(*p) if p else 0)
        d,w=tuple(z//content for z in d),tuple(tuple(z//content for z in p) for p in w)
        for k in keys:a.require(a.pdot(rows[k],w)==a.mul(rhs[k],d),'entire native-row Cramer identity')
        norm=a.add(a.mul((1,-1),a.sum_poly(a.power(p,2) for p in w)),a.mul(a.T,a.power(a.sum_poly(w),2)))
        short=a.strip(a.sub(a.scale(a.power(d,2),49),a.scale(norm,50)))
        leaves=[];paths=[]
        for leaf in rec['leaves']:
            path=leaf['path'];a.require(type(path)is list and all(type(b)is int and b in (0,1) for b in path),'strict path decoding');paths.append(path);lo,hi=a.LO,a.HI
            for bit in path:
                mid=(lo+hi)/2
                if bit==0:hi=mid
                else:lo=mid
            if leaf['type']=='N':
                a.require(set(leaf)=={'type','path'} and a.positive(short,lo,hi),'full native norm leaf by independent Sturm');polys=[short]
            else:
                a.require(leaf['type']=='I2' and set(leaf)=={'type','path','positive_residual','negative_residual'},'exact native residual leaf shape');polys=[]
                for field,sign in [('positive_residual',1),('negative_residual',-1)]:
                    k=leaf[field];a.require(type(k)is int and k in rows and k not in keys,'inactive original plane')
                    p=a.strip(a.scale(a.sub(a.pdot(rows[k],w),a.mul(rhs[k],d)),sign));a.require(a.positive(p,lo,hi),'full native residual leaf by independent Sturm');polys.append(p)
            obligations+=len(polys);leaves.append({'native_leaf':leaf,'verified_sign_polynomial_sha256':[a.hash_obj(p) for p in polys]})
        a.require(sum((F(1,2**len(p)) for p in paths),F())==1,'complete native closed cover')
        for p,q in itertools.combinations(paths,2):a.require(p!=q[:len(p)] and q!=p[:len(q)],'prefix-free native closed cover')
        result.append({'triple':list(keys),'singular':False,'leaves':leaves})
    a.require(obligations==706,'all original signs')
    return {'all39_coordinate_polynomials_equal':True,'entire364_triples_and367_leaves':result,'original_sign_obligations_verified_by_Sturm':obligations}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native-dir',required=True);ap.add_argument('--coordinates',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();root=Path(args.native_dir)
    c=json.loads((root/'CERTIFICATE.json').read_text());coords=json.loads(Path(args.coordinates).read_text());s=json.loads((root/'SYSTEM.json').read_text());out=verify(c,coords,s)
    out.update({'status':'PASS','certificate_bytes':(root/'CERTIFICATE.json').stat().st_size,'certificate_sha256':hashlib.sha256((root/'CERTIFICATE.json').read_bytes()).hexdigest(),'seconds':time.monotonic()-a.START,'target_executable_module_imported_by_comparison':False})
    Path(args.output).write_text(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='entire364_triples_and367_leaves'}))
if __name__=='__main__':main()
