"""Reconstruct the complete four-complex-repair cone, with exact ray norms.

Same-author rational evidence; the ordinary convexity, equality and actual
attainment arguments are in CONE_PROOF.md. No reviewer code is imported.
"""
from pathlib import Path
from hashlib import sha256
import argparse,json,resource,sys,time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import verify


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--record',type=Path)
    parser.add_argument('--control',choices=('wrong_row','wrong_ray','wrong_norm',
        'wrong_dual','missing_ray','wrong_sine_ratio'),help=argparse.SUPPRESS)
    args=parser.parse_args()
    if not args.emit:
        verify.source_check()
        listed={line.split('  ',1)[1] for line in (HERE/'SHA256SUMS').read_text().splitlines()}
        actual={p.name for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS'}
        verify.need(listed==actual and {'cone.py','CONE.json','CONE_PROOF.md','validate_cone.py'}<=listed,
                    'SOURCE complete enlarged capsule census')
    import profiles as p
    s,F=p.s,p.F
    start=time.monotonic();ids=[];bounds=[]
    c=s.c;one=s.N1;zero=s.N0
    def add(*z):return s.na(*z)
    def mul(x,y):return s.nm(x,y)
    def sc(x,q):return s.ns(x,q)
    def inv(x):return s.ni(x)
    def eq(name,x,y):p.eq(ids,name,[s.gf(x)],[s.gf(y)])
    h=add(sc(c,16),sc(one,-9))
    r=inv(add(sc(s.np(c,2),4),sc(one,-1)))
    w3=sc(mul(h,inv(add(sc(c,2),sc(one,-1)))),F(2,3))
    w4=inv(mul(add(one,c),add(sc(c,2),sc(one,-1))))
    rows=[
        [sc(one,F(-3,2)),sc(one,F(3,2)),one,one],
        [sc(one,F(-3,2)),sc(one,F(3,2)),sc(one,-1),sc(one,-1)],
        [sc(add(one,c),-1),sc(add(one,sc(s.np(c,2),-1)),2),r,sc(mul(c,r),2)],
        [sc(add(one,c),-1),sc(add(one,sc(s.np(c,2),-1)),2),sc(r,-1),sc(mul(c,r),-2)],
    ]
    v3=[sc(mul(add(one,sc(c,-1)),inv(h)),-2),sc(inv(h),-1),
        sc(mul(c,inv(h)),-3),sc(inv(h),F(3,2))]
    v4=[one,one,mul(add(one,c),inv(r)),sc(mul(add(one,c),inv(r)),-1)]
    flip=lambda v:[v[0],v[1],sc(v[2],-1),sc(v[3],-1)]
    rays=[v3,flip(v3),v4,flip(v4)]
    if args.control=='wrong_row':rows[2][3]=sc(rows[2][3],-1)
    if args.control=='wrong_ray':rays[2][2]=sc(rays[2][2],F(1,2))
    if args.control=='missing_ray':rays=rays[:-1]
    p.ar.need(len(rows)==len(rays)==4,'CENSUS all four normal rows and all four rays')
    sine3=add(s.np(s.WW,3),sc(s.np(s.WW,6),-1))
    for i,j in enumerate((3,6,4,5)):
        omega=s.np(s.WW,j)
        cos1=s.real(s.gf(omega))[0];cos2=s.real(s.gf(s.np(omega,2)))[0]
        ratio1=mul(add(omega,sc(s.np(s.WW,(-j)%9),-1)),inv(sine3))
        ratio2=mul(add(s.np(s.WW,(2*j)%9),sc(s.np(s.WW,(-2*j)%9),-1)),inv(sine3))
        if args.control=='wrong_sine_ratio' and j==4:ratio1=sc(ratio1,-1)
        actual=[add(cos1,sc(one,-1)),add(one,sc(cos2,-1)),ratio1,sc(ratio2,-1)]
        for k in range(4):eq('actual individual trigonometric normal row '+str(j)+' column '+str(k),actual[k],rows[i][k])
    weights=[w3,w3,w4,w4]
    def dot(a,b):return add(*(mul(x,y) for x,y in zip(a,b)))
    cost=[sc(one,8),sc(one,-7),zero,zero]
    for k in range(4):
        dual=sc(add(*(mul(weights[i],rows[i][k]) for i in range(4))),F(-1,2))
        if args.control=='wrong_dual' and k==0:dual=sc(dual,2)
        eq('whole cost dual coordinate '+str(k),dual,cost[k])
    for i,v in enumerate(rays):
        for j,row in enumerate(rows):
            eq('whole ray '+str(i)+' individual normal '+str(j),dot(row,v),sc(inv(weights[i]),-2) if i==j else zero)
        eq('whole ray '+str(i)+' unit objective cost',dot(cost,v),one)
    inverse=[[sc(mul(rays[j][i],weights[j]),F(-1,2)) for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            eq('whole left inverse '+str(i)+','+str(j),dot(rows[i],[inverse[k][j] for k in range(4)]),one if i==j else zero)
            eq('whole right inverse '+str(i)+','+str(j),dot(inverse[i],[rows[k][j] for k in range(4)]),one if i==j else zero)
    C2=sc(inv(add(one,sc(c,-1))),2)
    smallM=sc(mul(add(one,sc(c,-2),sc(s.np(c,2),4)),inv(s.np(h,2))),4)
    smallB=sc(inv(s.np(h,2)),4)
    norms=[]
    for i,v in enumerate(rays):
        nm=add(s.np(v[0],2),sc(s.np(v[2],2),F(4,3)))
        nb=add(s.np(v[1],2),sc(s.np(v[3],2),F(4,3)))
        if args.control=='wrong_norm' and i==2:nm=add(s.np(v[0],2),s.np(v[2],2))
        eq('whole ray '+str(i)+' actual M squared norm',nm,smallM if i<2 else C2)
        eq('whole ray '+str(i)+' actual scaled beta squared norm',nb,smallB if i<2 else C2)
        norms.append([p.encode_g(s.gf(nm)),p.encode_g(s.gf(nb))])
    eq('exact normalized sine square',sc(mul(add(one,sc(s.np(c,2),-1)),s.np(inv(r),2)),4),sc(one,3))
    lo,hi=map(F,p.prior['physical_cosine_interval'])
    p.ar.need(F(15,16)<lo<hi<1,'SIGN physical c above15/16 below1')
    for name,z in (('positive h minus6',add(h,sc(one,-6))),('positive w3',w3),
                   ('positive w4',w4),('one minus small M squared',add(one,sc(smallM,-1))),
                   ('one minus small beta squared',add(one,sc(smallB,-1))),
                   ('sharp C squared above32',add(C2,sc(one,-32)))):
        p.ar.need(set(z)<={0},'TYPE whole constant sign field')
        coefficients=list(map(F,s.field_real_form(s.physical_c,z.get(0,p.ar.N0))))
        lower=sum(q*(lo**j if q>=0 else hi**j) for j,q in enumerate(coefficients))
        p.ar.need(lower>0,'SIGN '+name)
        bounds.append({'name':name,'entire_real_cubic_coefficients':list(map(str,coefficients)),
                       'rational_lower_bound':str(lower)})
    record={'agent':'six-sendov-3','role':'researcher','formalization':False,'independent_review':False,
        'scope':'four-complex-repair-cone-only; ordinary constructed15Dcap bridge in CONE_PROOF.md',
        'coordinates':['Re M','(H/7)Re beta','sin(2pi/3)Im M','(H/7)sin(2pi/3)Im beta'],
        'row_labels':[3,6,4,5],'identity_count':len(ids),'sign_count':len(bounds),
        'whole_identities':ids,'sign_bounds':bounds,
        'whole_rows':[[p.encode_g(s.gf(x)) for x in v] for v in rows],
        'whole_unit_cost_rays':[[p.encode_g(s.gf(x)) for x in v] for v in rays],
        'whole_actual_ray_squared_norms':norms,'whole_dual_weights':[p.encode_g(s.gf(w)) for w in weights],
        'sharp_squared_constant':p.encode_g(s.gf(C2)),
        'physical_cosine_interval':[str(lo),str(hi)],'reviewer_executable_imported':False}
    data=p.ar.canonical(record)
    compact={'identity_count':len(ids),'sign_count':len(bounds),'whole_record_bytes':len(data),
             'whole_record_sha256':sha256(data).hexdigest()}
    if not args.emit:
        expected=json.loads((HERE/'CONE.json').read_text())
        p.ar.need(expected.get('schema')=='four-complex-repair-cone-v1','TYPE cone schema')
        p.ar.need(expected.get('agent')=='six-sendov-3' and expected.get('role')=='researcher','TYPE actual cone author')
        p.ar.need(expected.get('formalization') is False and expected.get('independent_review') is False,'TYPE cone proof/review status')
        p.ar.need(expected.get('scope')=='displayed-four-complex-repair-cone','TYPE cone quantified coverage')
        p.ar.need(type(expected.get('identity_count')) is int and type(expected.get('sign_count')) is int,'TYPE cone counts')
        p.ar.need({k:expected.get(k) for k in compact}==compact,'RECORD whole complete cone differs')
    if args.record:
        target=args.record.resolve();p.ar.need(not target.is_relative_to(HERE),'SOURCE full cone record outside source')
        target.write_bytes(data+b'\n')
    print(json.dumps({'status':'PASS whole four-complex-repair cone','agent':'six-sendov-3','role':'researcher',
        **compact,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'formalization':False,'independent_review':False},sort_keys=True))


if __name__=='__main__':main()
