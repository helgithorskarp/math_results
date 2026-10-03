"""Three exact original physical widths and original translation closure."""
from fractions import Fraction as Q
from math import comb
from primitives import F,Z,O,phi,dot,cross,sub,encode,rotate,need

def evaluate(a,z):
    return sum((value*z**i for i,value in enumerate(a)),Z)

def multiply(a,b):
    out=[Z]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):out[i+j]+=u*v
    return out

def bernstein(a,rho):
    n=len(a)-1
    return [sum((a[k]*rho**k*F(Q(comb(i,k),comb(n,k))) for k in range(i+1)),Z)
            for i in range(n+1)]

def verify(cert,g):
    V,M,c,U,rho=[g[k] for k in ['V','M','c','U','rho']]
    lo,hi=[F(*a) for a in cert['receiving_x_interval']]
    need(Z<lo<hi,'entire closed midpoint receiver interval differs')
    A=O+dot(c,c);need(A>O,'positive original Cayley clearing factor differs')
    edges=cert['width_edges'];rows=cert['width_rows']
    need(len(edges)==2 and set(rows)=={'32','40','96'},'three-width certificate incomplete')
    records=[]
    for si,(ia,ib) in enumerate(edges):
        edge=sub(V[ib],V[ia]);corners=[]
        for x in (lo,hi):
            r=(x,Z,O);m=cross(edge,r);h=dot(m,V[ia])
            need(h>Z,'actual original width support is not positive')
            gaps=[h-sign*dot(m,v) for sign in (-1,1) for v in V]
            need(all(a>=Z for a in gaps),'genuine whole-segment paired width support fails')
            corners.append({'x':x.encode(),'normal':encode(m),'height':h.encode(),
                            'all120_actual_paired_support_gaps':encode(gaps)})
        records.append({'support':si,'actual_original_edge':[ia,ib],
                        'all2_closed_endpoint_records':corners})
    coefficients={};fixtures=[]
    for name,(si,source) in rows.items():
        ia,ib=edges[si];edge=sub(V[ib],V[ia]);v=M[source];values=[]
        for x in (Z,O):
            m=cross(edge,(x,Z,O));h=dot(m,V[ia]);a=dot(m,v)
            values.append([A*(a-h),2*A*dot(cross(v,m),U),
                           A*(-a-h+2*dot(m,U)*dot(v,U))])
        b=values[0];a=[values[1][j]-b[j] for j in range(3)]
        stated=cert['width_coefficients'][name]
        need(encode(a)==stated['x_coefficients'] and encode(b)==stated['constant_coefficients'],
             'full stated original physical width polynomial differs')
        coefficients[name]=(a,b)
        for x in (lo,hi):
            m=cross(edge,(x,Z,O));h=dot(m,V[ia])
            for z in (-rho,Z,rho):
                literal=A*(O+z*z)*(dot(m,rotate(tuple(z*u for u in U),v))-h)
                need(literal==x*evaluate(a,z)+evaluate(b,z),
                     'full direct physical Rodrigues support identity differs')
                fixtures.append({'row':name,'x':x.encode(),'z':z.encode(),
                                 'literal_cleared_support':literal.encode()})
    a32,b32=coefficients['32'];K=F(Q(8,5))*(2*phi-1)
    need(a32==[Z,2*K,-K] and b32==[Z,-K,-2*K] and K>Z,
         'written actual32 factor differs')
    controls32=[2*x-O-(x+2)*z for x in (lo,hi) for z in (-rho,rho)]
    need(all(a<Z for a in controls32),
         'actual32 factor does not force z>=0 on the entire closed receiver/source rectangle')
    a40,b40=coefficients['40'];a96,b96=coefficients['96']
    need(a96[0]==b96[0]==Z,'actual96 is not exactly divisible by z')
    controls40=bernstein(a40,rho);controls96=bernstein(a96[1:],rho)
    need(all(a<Z for a in controls40),'actual40 x coefficient is not negative throughout')
    need(all(a>Z for a in controls96),'actual96 x coefficient over z is not positive throughout')
    ab=multiply(b40,a96);ba=multiply(b96,a40);D=[u-v for u,v in zip(ab,ba)]
    C=F(Q(64,5))*(3-phi)
    need(D==[Z,Z,C,Z,C] and C>Z,
         'full actual determinant is not positive C*z^2*(1+z^2)')
    translation=[];N=tuple(F(*a) for a in cert['translation_axis'])
    source=cert['translation_source'];ia,ib=edges[0]
    for x in (lo,hi):
        r=(x,Z,O);m=cross(sub(V[ib],V[ia]),r);h=dot(m,V[ia])
        need(dot(m,M[source])==h,'claimed original translation contact is not persistent')
        need(N==U and cross(m,N)==r,'genuine original translation normals fail to span r-perp')
        translation.append({'x':x.encode(),'normal':encode(m),'height':h.encode(),
            'actual_touching_source':source,'normal_cross_U':encode(cross(m,N))})
    return {'entire_closed_receiving_x_interval':encode((lo,hi)),
        'positive_original_Cayley_clearing_factor':A.encode(),
        'all2_original_paired_width_supports':records,'all480_endpoint_paired_support_controls':480,
        'all3_full_actual_physical_width_polynomials':{
            name:{'support':rows[name][0],'source':rows[name][1],
                  'x_coefficients':encode(a),'constant_coefficients':encode(b)}
            for name,(a,b) in coefficients.items()},
        'all18_direct_physical_Rodrigues_fixtures':fixtures,
        'all4_strict_negative32_bracket_controls':encode(controls32),
        'all3_strict_negative40_x_coefficient_controls':encode(controls40),
        'all2_strict_positive96_x_coefficient_over_z_controls':encode(controls96),
        'full_two_support_determinant_coefficients':encode(D),
        'all2_original_translation_contact_and_spanning_controls':translation,
        'ordinary_necessary_fit_conclusion':'delta0,originallambda1,originalt0 on the entire closed midpoint segment; all original physical quantifiers retained'}
