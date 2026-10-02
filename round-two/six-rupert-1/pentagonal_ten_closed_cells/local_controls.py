#!/usr/bin/env python3
"""Independent Fraction determinant polarization, physical identities, closed fans.

These are author controls, not independent review. The theorem also requires
the complete production support/Cramer check and its ordinary argument.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse,copy,hashlib,itertools,json,resource,time
import local as C
H,E=C.H,C.E
HERE=Path(__file__).resolve().parent

def need(x,s):
    if not x:raise ValueError(s)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def area(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def determinant(a):
    """Gaussian Fraction oracle; production uses subset polynomial expansion."""
    a=[list(row)for row in a];value=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a))if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];value=-value
        p=a[j][j];value*=p
        for k in range(j+1,len(a)):
            q=a[k][j]/p
            for i in range(j+1,len(a)):a[k][i]-=q*a[j][i]
    return value
def solve(a,b):
    """Exact Gaussian field solve without using the production Cramer routine."""
    a=[list(row)+[z]for row,z in zip(a,b)];n=len(a)
    for j in range(n):
        k=next((k for k in range(j,n)if a[k][j]!=H.Z),None)
        need(k is not None,'actual independent nonsingular five-wrench system')
        a[j],a[k]=a[k],a[j];inv=a[j][j].inv()
        a[j]=[x*inv for x in a[j]]
        for k in range(n):
            if k==j:continue
            q=a[k][j];a[k]=[x-q*y for x,y in zip(a[k],a[j])]
    return [row[-1]for row in a]

def run(args):
    started=time.monotonic();deadline=started+args.seconds;damages=[]
    def guard():need(time.monotonic()<deadline,'control stage completed inside guard')
    def rejected(name,f):
        try:f()
        except (ValueError,KeyError,IndexError,TypeError):damages.append(name);return
        raise ValueError('Damaged input accepted: '+name)
    work=Path(args.work);cache=(work.parent/'named_geometry.json').read_bytes()
    config=json.loads((HERE/'configuration.json').read_text())
    data=C.verified_cache(cache,config['expected_fresh_named_geometry_sha256'])
    cert=json.loads((HERE/'certificates.json').read_text())[str(args.cell)]
    recpath=work/'local.json';local=json.loads(recpath.read_text())
    need(hashlib.sha256(json.dumps(cert,sort_keys=True).encode()).hexdigest()==local['certificate_sha256'],'same actual certificate')
    root=data['root'];polygon=[tuple(C.decode(z)for z in p)for p in cert['polygon']]
    # Independent triangulation and exact cyclic area. Both diagonals and all
    # fan edges are closed; test integer convex combinations of the whole cell.
    corners=len(polygon);fans=[(0,i,i+1)for i in range(1,corners-1)]
    pieces=[[polygon[i]for i in tri]for tri in fans]
    need(sum(area(*tri)for tri in pieces)==sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(polygon,polygon[1:]+polygon[:1])),'fan area identity with all five cyclic edges')
    expected=C.exact_receiver_pieces(polygon,0)
    need(expected=={str(i):tri for i,tri in enumerate(pieces)},'all three entire literal fans, exact order')
    cover=0;boundary=0
    for weights in itertools.product(range(6),repeat=corners):
        if sum(weights)!=5:continue
        actual=tuple(sum(F(w,5)*v[j]for w,v in zip(weights,polygon))for j in range(2))
        signs=[[H.sign(area(a,b,actual),root)for a,b in zip(tri,tri[1:]+tri[:1])]for tri in pieces]
        valid=[v for v in signs if min(v)>=0]
        need(valid,'independent convex combination lies in at least one whole CLOSED fan')
        cover+=1;boundary+=int(any(0 in v for v in valid))
    closed_children=C.exact_receiver_pieces(polygon,1)
    midpoint_cases=0
    for fan,tri in enumerate(pieces):
        a,b,c=tri
        mid=lambda u,v:tuple((x+y)/2 for x,y in zip(u,v))
        ab,bc,ca=mid(a,b),mid(b,c),mid(c,a)
        children=((a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca))
        need(sum(area(*p)for p in children)==area(a,b,c),'four CLOSED rational children cover parent area')
        for j,p in enumerate(children):
            need(closed_children[str(fan)+str(j)]==list(p)and area(*p)==area(a,b,c)/4,'independent exact child decoder and quarter area')
            midpoint_cases+=1
    guard()
    # Determinant multilinearity supplies a different exact degree5 control
    # oracle: average Gaussian determinants over all column vertex assignments.
    vertices=[[[F((i+1)*(j+2)%7-3,17)+F(int(i==j)*3)+F(v*(i-j+1),31)for j in range(5)]for i in range(5)]for v in range(3)]
    synthetic_controls=0;tensor_cases=0
    for replaced in (-1,0,1,2,3,4):
        vv=copy.deepcopy(vertices)
        if replaced>=0:
            for a in vv:
                for i in range(5):a[i][replaced]=F(int(i==2))
        sums={};counts={}
        for assignment in itertools.product(range(3),repeat=5):
            k,l=assignment.count(1),assignment.count(2)
            value=determinant([[vv[assignment[j]][i][j]for j in range(5)]for i in range(5)])
            sums[k,l]=sums.get((k,l),F(0))+value;counts[k,l]=counts.get((k,l),0)+1
        refs={key:sums[key]/counts[key]for key in sums}
        matrix=[[{(0,0):E.B.rational(vv[0][i][j]),(1,0):E.B.rational(vv[1][i][j]-vv[0][i][j]),(0,1):E.B.rational(vv[2][i][j]-vv[0][i][j])}for j in range(5)]for i in range(5)]
        bounds=E.bernstein(E.determinant(matrix,deadline),5)
        keys=[(k,l)for k in range(6)for l in range(6-k)]
        for interval,key in zip(bounds,keys):
            need(F(interval.lo,E.SCALE)<=refs[key]<=F(interval.hi,E.SCALE),'independent Gaussian column-polarization control inside every production enclosure')
            synthetic_controls+=1
        for u,v in ((F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1,3),F(1,3)),(F(1,5),F(2,5))):
            actual=[[vv[0][i][j]*(1-u-v)+vv[1][i][j]*u+vv[2][i][j]*v for j in range(5)]for i in range(5)]
            reconstructed=sum(refs[k,l]*F(factorial(5),factorial(k)*factorial(l)*factorial(5-k-l))*u**k*v**l*(1-u-v)**(5-k-l)for k,l in keys)
            need(reconstructed==determinant(actual),'independent degree5 barycentric reconstruction equals direct Gaussian determinant')
            tensor_cases+=1
        guard()
    # Actual cubic-field five-wrench vector identities at each of the18 fan
    # centroids. Solve all five entries: physical force is never omitted.
    actual_duals=0;physical=0
    for dual in cert['duals']:
        tri=pieces[int(dual['receiver_path'])]
        r=(H.O,*[sum(v[j]for v in tri)/3 for j in range(2)])
        cols=[]
        for a,b,v,k in dual['contacts']:
            P=data['points'][v];d=tuple(y-x for x,y in zip(data['points'][a],data['points'][b]));m=tuple(F(2)**k*z for z in cross(d,r))
            cols.append((*cross(P,m),m[1],m[2]))
        matrix=[[col[i]for col in cols]for i in range(5)]
        rhs=[H.K.coerce(dual['sign']if i==dual['coordinate']else 0)for i in range(5)]
        weights=solve(matrix,rhs)
        need(all(H.sign(w,root)>0 for w in weights),'actual positive centroid weights')
        need([sum(w*x for w,x in zip(weights,row))for row in matrix]==rhs,'all torque and physical force entries agree exactly')
        actual_duals+=1;guard()
    contacts=sorted(set(tuple(c)for d in cert['duals']for c in d['contacts']))
    c=tuple(H.K.coerce(q)for q in (F(1,32),F(-1,40),F(1,48)))
    for a,b,v,k in contacts:
        for point in (polygon[0],tuple(sum(p[j]for p in polygon)/corners for j in range(2))):
            r=(H.O,*point);P=data['points'][v];d=tuple(y-x for x,y in zip(data['points'][a],data['points'][b]));m=tuple(F(2)**k*z for z in cross(d,r));h=dot(m,P)
            den=1+dot(c,c)
            rotated=tuple(((1-dot(c,c))*x+2*dot(c,P)*y+2*z)/den for x,y,z in zip(P,c,cross(c,P)))
            need(den*(dot(m,rotated)-h)==2*dot(cross(P,m),c)+2*dot(m,c)*dot(P,c)-2*h*dot(c,c),'actual literal cleared Cayley endpoint identity')
            w=(H.Z,H.K.coerce(F(2,7)),H.K.coerce(F(-3,7)))
            T=tuple(x-dot(w,r)*y/dot(r,r)for x,y in zip(w,r))
            need(dot(T,r)==H.Z and dot(m,T)==m[1]*w[1]+m[2]*w[2],'actual physical projection and two translation coordinates')
            for scale in (H.O,H.K.coerce(F(9,8))):
                need(dot(m,tuple(scale*x+t for x,t in zip(rotated,T)))-h==scale*(dot(m,rotated)-h)+dot(m,T)+(scale-1)*h,'original physical translation and enlargement identity')
            physical+=1
        guard()
    def bad_cert(name,mutate):
        z=copy.deepcopy(cert);mutate(z);rejected(name,lambda:C.prepare(z,data,deadline))
    for name,change in (
        ('missing_closed_corner',lambda z:z['polygon'].pop()),
        ('wrong_cyclic_order',lambda z:z['polygon'].reverse()),
        ('changed_facet50',lambda z:z['facet_signs'].__setitem__(50,-z['facet_signs'][50])),
        ('missing_closed_fan',lambda z:z.update(duals=z['duals'][:-6])),
        ('missing_signed_direction',lambda z:z['duals'].pop()),
        ('duplicate_dual',lambda z:z['duals'].append(copy.deepcopy(z['duals'][0]))),
        ('wrong_fan_path',lambda z:z['duals'][0].update(receiver_path='3')),
        ('unproved_midpoint_inventory',lambda z:z.update(receiver_depth=1)),
        ('wrong_contact_endpoint',lambda z:z['duals'][0]['contacts'][0].__setitem__(2,92))):bad_cert(name,change)
    for name,key,value in (
        ('insufficient_coordinate_mass','coordinate_mass_bounds',[1,1,1]),
        ('insufficient_euclidean_mass','mass_euclidean_upper',cert['mass_euclidean_upper']-1),
        ('nonlinear_boundary_not_contracting','closed_cayley_euclidean_radius',str(F(1,2*cert['mass_euclidean_upper']))),
        ('excessive_physical_gap','physical_gap_coefficient','1')):
        z=copy.deepcopy(cert);z[key]=value;rejected(name,lambda z=z:C.close_bounds(z,local['duals']))
    rejected('wrong_named_model_cache',lambda:C.verified_cache(cache,'0'*64))
    need(C.close_bounds(cert,local['duals'])['closed_relative_cayley_euclidean_radius']==cert['closed_cayley_euclidean_radius'],'actual cell-specific collar constants')
    guard()
    result=dict(agent='six-rupert-1',role='researcher',status='WHOLE_CLOSED_CELL_INDEPENDENT_AUTHOR_LOCAL_CONTROLS_PASSED',local_sha256=hashlib.sha256(recpath.read_bytes()).hexdigest(),named_model_fresh_sha256=hashlib.sha256(cache).hexdigest(),fraction_column_polarization_controls=synthetic_controls,direct_degree5_tensor_reconstructions=tensor_cases,actual_five_wrench_centroid_identities=actual_duals,actual_physical_cayley_translation_scale_identities=physical,whole_polygon_closed_fan_location_cases=cover,closed_boundary_location_cases=boundary,independent_midpoint_decoder_area_cases=midpoint_cases,damaged_certificate_rejections=damages,cell_id=args.cell,proof_scope='Conditional local collar only; actual model rebuilt by the driver, all-source classification requires every shell leaf. Author controls, not independent review.')
    raw=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:need(raw==Path(args.compare).read_bytes(),'whole normal/O controls agree')
    Path(args.output).write_bytes(raw)
    print(json.dumps(dict(status=result['status'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cell',type=int,required=True,choices=(19,18,16,33));p.add_argument('--work',required=True);p.add_argument('--seconds',type=float,default=40);p.add_argument('--output',required=True);p.add_argument('--compare');run(p.parse_args())
