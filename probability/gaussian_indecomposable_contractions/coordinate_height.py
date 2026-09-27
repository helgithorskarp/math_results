#!/usr/bin/env python3
"""Small exact controls for COORDINATE_HEIGHT.md; standard-library Python 3.11+.

No worst-case mesh, reflection-state enumeration or Gaussian integral is run.
The universal height bound is the written proof, not an inference from these tests.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, isqrt, prod
from pathlib import Path
import argparse
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def clog(n):
    need(isinstance(n, int) and n > 0, 'positive integer required')
    return (n - 1).bit_length()


def ht(q):
    q = F(q)
    return clog(max(abs(q.numerator), q.denominator))


def dot(x, y):
    need(len(x) == len(y), 'dimension mismatch')
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def mm(a, b):
    need(len(a[0]) == len(b), 'matrix dimension mismatch')
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def eye(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def mv(a, x):
    return tuple(dot(row, x) for row in a)


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def intersect(planes):
    a = tuple(tuple(p[:3]) for p in planes)
    d = det3(a)
    need(d != 0, 'singular plane triple')
    rhs = tuple(-p[3] for p in planes)
    return tuple(det3(tuple(tuple(rhs[i] if j == col else a[i][j]
                                  for j in range(3)) for i in range(3)))/d
                 for col in range(3))


def plane_value(p, x):
    return dot(p[:3], x) + p[3]


def reflection(p):
    n, c = p[:3], p[3]
    q = dot(n, n)
    need(q > 0, 'zero plane normal')
    return tuple(tuple(F(i == j)-2*n[i]*n[j]/q for j in range(3))
                 + (-2*c*n[i]/q,) for i in range(3)) + ((F(0), F(0), F(0), F(1)),)


def repair_control():
    u = ((F(3,5), F(-4,5), F(0)), (F(4,5), F(3,5), F(0)),
         (F(0), F(0), F(1)))
    t = (F(1,7), F(-2,9), F(3,11))
    a, b = (F(1,13), F(-2,17), F(3,19)), (F(2,5), F(1,7), F(-1,3))
    s = tuple(row + (shift,) for row, shift in zip(u, t)) + (eye(4)[3],)
    ap = tuple(dot(tuple(u[j][i] for j in range(3)), sub(b, t)) for i in range(3))
    n = sub(ap, a)
    c = dot(ap, ap)-dot(a, a)
    h = tuple(2*v for v in n) + (-c,)
    rho = reflection(h)
    updated = mm(s, rho)
    need(mv(updated, a+(F(1),))[:3] == b, 'repair does not hit prescribed image')
    need(plane_value(h, a) == -dot(n, n), 'bisector sign identity failed')
    base = [intersect((h, (F(1),F(0),F(0),-x),
                          (F(0),F(1),F(0),-y)))
            for x in (F(-1),F(1)) for y in (F(-1,2),F(1,2))]
    facets = [(F(1),F(0),F(0),F(1)), (F(-1),F(0),F(0),F(1)),
              (F(0),F(1),F(0),F(1,2)), (F(0),F(-1),F(0),F(1,2))]
    side_planes = []
    for f in facets:
        side = tuple(plane_value(f,a)*hj-plane_value(h,a)*fj for hj, fj in zip(h,f))
        need(plane_value(side,a) == 0, 'side plane misses apex')
        need(sum(plane_value(side,z)==0 for z in base) == 2, 'side misses base edge')
        need(all(plane_value(side,z)>=0 for z in base), 'wrong cone orientation')
        side_planes.append(side)
    for z in base:
        need(mv(rho,z+(F(1),))[:3] == z, 'reflection moves bisector')
        need(mv(updated,z+(F(1),)) == mv(s,z+(F(1),)), 'repair boundary mismatch')
    flat = [v for row in u for v in row] + list(t+a+b) + [v for f in facets for v in f]
    z = max(1, max(map(ht, flat)))
    stages = {'preimage':(ap,14), 'normal':(n,16), 'constant':((c,),95),
              'norm_squared':((dot(n,n),),98), 'bisector':(h,128),
              'reflection':(sum(rho,()),256), 'repaired_map':(sum(updated,()),1024),
              'cone_sides':(sum(tuple(side_planes),()),1024)}
    heights = {}
    for name,(values,factor) in stages.items():
        actual = max(map(ht,values))
        need(actual <= factor*z, 'repair height bound failed: '+name)
        heights[name] = {'observed':actual, 'bound':factor*z}
    return {'input_height':z, 'apex':[str(v) for v in a],
            'image':[str(v) for v in b], 'side_facets_checked':4,
            'boundary_vertices_checked':4, 'stage_heights':heights}


def barycentre_control():
    planes = [(F(1),F(0),F(0),F(-1,2)), (F(0),F(1),F(0),F(1,3)),
              (F(0),F(0),F(1),F(-1,5)), (F(1),F(2),F(3),F(-7,11))]
    a = max(ht(v) for p in planes for v in p)
    vertices=[]
    for triple in combinations(planes,3):
        x=intersect(triple)
        need(all(plane_value(p,x)==0 for p in triple), 'Cramer reconstruction failed')
        vertices.append(x)
    need(len(set(vertices))==4, 'tetrahedral arrangement degenerated')
    vmax=max(ht(v) for x in vertices for v in x)
    need(vmax <=64*a, 'arrangement vertex height failed')
    centers=[]
    for size in range(1,5):
        for face in combinations(vertices,size):
            center=tuple(sum(x[j] for x in face)/size for j in range(3))
            for j in range(3):
                denominator=prod(x[j].denominator for x in face)
                numerator=sum(x[j].numerator*(denominator//x[j].denominator) for x in face)
                need(center[j]==F(numerator,size*denominator), 'cleared barycentre differs')
            need(max(map(ht,center)) <=size*(64*a+2), 'barycentre height failed')
            centers.append(center)
    return {'planes':4,'vertices':[[str(v) for v in x] for x in vertices],
            'plane_height':a,'vertex_height':vmax,'face_means_checked':len(centers),
            'maximum_mean_height':max(ht(v) for c in centers for v in c)}


def word_control():
    planes=[(F(1),F(2,7),F(-3,11),F(4,13)),
            (F(1,97),F(1,97**2),F(1),F(-2,17)),
            (F(2,19),F(-3,23),F(5,29),F(1,31))]
    word=[reflection(p) for p in planes]*4
    source=(F(1,37),F(-2,41),F(3,43),F(1))
    direct=source
    integer_product=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
    denominator=1
    t=max(ht(v) for matrix in word for row in matrix[:3] for v in row)
    k=max(map(ht,source))
    records=[]
    for r,matrix in enumerate(word,1):
        direct=mv(matrix,direct)
        q=prod(v.denominator for row in matrix[:3] for v in row)
        cleared=tuple(tuple(int(v*q) for v in row) for row in matrix)
        need(all(v*q==int(v*q) for row in matrix for v in row), 'matrix not integral after clearing')
        need(q<=2**(12*t), 'matrix denominator exceeds bound')
        need(max(abs(v) for row in cleared for v in row)<=2**(13*t),
             'cleared matrix entry exceeds bound')
        integer_product=mm(cleared,integer_product)
        denominator*=q
        reconstructed=tuple(dot(row,source)/denominator for row in integer_product)
        need(reconstructed==direct, 'cleared and rational word actions differ')
        observed=max(map(ht,direct))
        need(observed<=13*r*t+4*k+2*r, 'word coordinate bound failed')
        need(max(abs(v) for row in integer_product for v in row) <=2**(13*r*t+2*r),
             'cleared product entry bound failed')
        records.append({'length':r,'observed_coordinate_height':observed,
                        'height_bound':13*r*t+4*k+2*r,
                        'cleared_denominator_bits':denominator.bit_length()})
    return {'reflection_coefficient_height':t,'source_height':k,'prefixes':records}


def budget(n,b):
    need(isinstance(n,int) and not isinstance(n,bool) and 1<=n<=64,
         'display budget requires 1<=N<=64; larger bounds stay symbolic')
    need(isinstance(b,int) and not isinstance(b,bool) and b>=1,'input height must be positive')
    h=512*2**n*(n+6)+3*n+comb(n,3)+6
    m=12*h*sum(comb(h,j) for j in range(4))
    hrep=2**(10*n)*(b+4);a=64*hrep;vtx=64*a;j=comb(h,3);k=j*(vtx+2)
    height=2**15*m*k
    return {'N':n,'input_height':b,'planes':h,'tetrahedra':m,'labels':m+3,
            'repair_height':hrep,'arrangement_plane_height':a,'arrangement_vertex_height':vtx,
            'mesh_vertex_height':k,'all_state_coordinate_height':height,
            'coordinate_height_bit_length':height.bit_length(),
            'representation':'Height is stored; coordinate bound 2^H is not expanded.'}


def frontier_input(delta):
    a,b=delta.numerator,delta.denominator
    need(0<a<=b,'deficit outside (0,1]')
    k=(9*b+a-1)//a;ell=clog(k);h=isqrt(ell+1);n=(k+h-1)//h
    count=min(k**3*(2*comb(2*ell+6,3)-1),n**3*(2*comb(4*ell+11,3)-1))
    return {'delta':str(delta),'k':k,'original_atom_bound':count,
            'coordinate_denominator':256*k**3,'original_weight_denominator':4*k*count,
            'input_coordinate_height':clog(768*k**4+1),
            'mesh_and_height':'Use the closed formulas; huge powers are not evaluated here.'}


def endpoint_envelopes():
    records=[]
    # Toy bounds only: neither actual global H nor its exponential is expanded.
    for v,h,r,delta in [(4,1,1,F(1)),(7,2,12,F(1,2)),(11,10,24,F(1,10))]:
        j0=145+2*clog(v)+6*clog(r)+(222*v+30)*h
        dmax=2**(6*v*h);mmax=2**((6*v+1)*h)
        denominator=2**40*v*v*r**6*dmax**7*(6*5040)**5*(2*mmax)**30
        need(clog(denominator)<=j0,'uniform mean-support envelope failed')
        mass=delta/(2*(2+delta)*v)
        inv=1/mass
        ell=max(0,inv.numerator.bit_length()-inv.denominator.bit_length())
        if inv.denominator*2**ell<inv.numerator:ell+=1
        big_b=6*r*r+2*ell
        upper_exp=ell+12*v*h+4
        source_d2=F(1,2**(12*v*h))
        need(mass*source_d2/(8+source_d2)>=F(1,2**upper_exp),'uniform peak envelope failed')
        records.append({'labels_bound':v,'height_bound':h,'radius':r,'delta':str(delta),
                        'mean_support_denominator_bits':denominator.bit_length(),
                        'J0':j0,'mass_log_budget':ell,'E_coefficient':16*big_b**2,
                        'E_power_of_two':2*j0,'upper_gap_exponent':upper_exp})
    return records


def result():
    # Small arithmetic controls for common mass denominators and log envelopes.
    mass_checks=0
    for delta in (F(1),F(1,2),F(1,10)):
        a,b=delta.numerator,delta.denominator
        for v in (4,7,11):
            w=13;numerators=[2,3,8]+[0]*(v-3)
            q=2*(2*b+a)*w*v
            masses=[F((4*b+a)*n*v+a*w,q) for n in numerators]
            need(sum(masses)==1 and min(masses)==delta/(2*(2+delta)*v),'mass denominator formula failed')
            mass_checks+=1
    rejections=[]
    for name,call in [('zero_normal',lambda:reflection((F(0),)*4)),
                      ('singular_planes',lambda:intersect(((F(1),F(0),F(0),F(1)),)*3)),
                      ('zero_input_height',lambda:budget(4,0)),
                      ('out_of_range_deficit',lambda:frontier_input(F(2)))]:
        try:call()
        except ValueError as exc:rejections.append({'name':name,'reason':str(exc)})
        else:raise ValueError('damaged input accepted: '+name)
    return {'status':'RATIONAL_COORDINATE_HEIGHT_CONTROLS_PASS',
            'repair':repair_control(),'barycentres':barycentre_control(),'reflection_words':word_control(),
            'small_bound_displays':[budget(n,10) for n in (1,4,7,10)],
            'global_input_parameters':[frontier_input(d) for d in (F(1),F(1,2),F(1,10))],
            'toy_uniform_endpoint_envelopes':endpoint_envelopes(),
            'mass_denominator_checks':mass_checks,'rejections':rejections,
            'trust':'Finite exact controls, not an exhaustive construction or independent proof.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--record',action='store_true');g.add_argument('--check',action='store_true')
    args=p.parse_args();r=result();s=json.dumps(r,indent=2,sort_keys=True)+'\n'
    path=Path(__file__).with_name('COORDINATE_EXPECTED.json')
    if args.record:path.write_text(s)
    else:need(path.read_text()==s,'expected record mismatch')
    print(r['status'])
    print('EXPECTED sha256='+hashlib.sha256(s.encode()).hexdigest())
    print('No worst-case mesh, interval search or Gaussian computation was run.')


if __name__=='__main__':main()
