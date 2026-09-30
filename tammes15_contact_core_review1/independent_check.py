#!/usr/bin/env python3
"""Independent exact Tammes contact-core audit by six-reviewer-1.

No author code, factor certificate or coordinate input is imported.
Domains: QQ(t) for identities, QQ[t]/(F) for the unique real root.
Requires SymPy 1.14.0; all checks use explicit exceptions.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sympy as sp

T = sp.Symbol('t')
FIELD = sp.QQ.frac_field(T)
t = FIELD.gens[0]
Z, O = FIELD.zero, FIELD.one
F = sp.Poly(13*T**5-T**4+6*T**3+2*T**2-3*T-1, T, domain=sp.QQ)
LO = sp.Rational('0.59260590292507377809642492233275')
HI = sp.Rational('0.59260590292507377809642492233276')
A_STEPS = ((6,0,11,5), (7,0,5,11), (9,5,11,0))
B_STEPS = ((8,2,4,1), (10,1,2,4), (12,1,10,2), (13,2,8,4))
CROSS = ((6,8), (7,12), (9,10), (9,13))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y, metric):
    return sum((x[i]*metric[i][j]*y[j] for i in range(3) for j in range(3)), metric[0][0]*0)


def cross(x, y):
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]


def matvec(a, x):
    return [sum((u*v for u,v in zip(row,x)), x[0]*0) for row in a]


def linear(a, zero):
    """Full exact RREF; returns matrix and pivot columns."""
    a = [row[:] for row in a]
    pivot_columns = []
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r,len(a)) if a[i][c] != zero), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        inv = (a[r][c]**0)/a[r][c]
        a[r] = [v*inv for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] != zero:
                q = a[i][c]
                a[i] = [v-q*w for v,w in zip(a[i],a[r])]
        pivot_columns.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivot_columns


def solve(a, b, zero):
    rr, pivots = linear([row+[v] for row,v in zip(a,b)], zero)
    require(pivots == list(range(len(a))), 'singular exact solve')
    return [row[-1] for row in rr]


def determinant(a):
    """Elimination in the function field; no geometric pivot assumption."""
    a = [row[:] for row in a]
    total = O
    for c in range(len(a)):
        p = next((i for i in range(c,len(a)) if a[i][c]), None)
        if p is None:
            return Z
        if p != c:
            a[c],a[p]=a[p],a[c]
            total=-total
        pivot = a[c][c]
        total *= pivot
        for i in range(c+1,len(a)):
            q=a[i][c]/pivot
            for j in range(c+1,len(a)):
                a[i][j] -= q*a[c][j]
            a[i][c]=Z
    return total


def polynomial(x):
    return sp.Poly(x.as_expr(), T, domain=sp.QQ)


def sign_poly(p, a=sp.Rational(1,2), b=sp.Rational(3,5)):
    """Sturm root count and endpoint signs, independent of Bernstein tests."""
    p = sp.Poly(p,T,domain=sp.QQ)
    require(not p.is_zero, 'zero sign polynomial')
    require(p.eval(a) != 0 and p.eval(b) != 0, 'endpoint zero')
    require(p.count_roots(a,b) == 0, 'polynomial has an interval root')
    return 1 if p.eval(a) > 0 else -1


def sign_rat(x):
    return sign_poly(polynomial(x.numer))*sign_poly(polynomial(x.denom))


def reflect(roots, steps, metric, parameter):
    zero=parameter*0
    one=zero+1
    coords={v:[one if k==j else zero for k in range(3)] for j,v in enumerate(roots)}
    edges={tuple(sorted(e)) for e in combinations(roots,2)}
    for n,i,j,o in steps:
        require(all(tuple(sorted(e)) in edges for e in ((i,j),(i,o),(j,o))), 'old triangle missing')
        coords[n]=[2*parameter/(1+parameter)*(x+y)-z for x,y,z in zip(coords[i],coords[j],coords[o])]
        edges.update((tuple(sorted((n,i))),tuple(sorted((n,j)))))
    for v in coords.values():
        require(dot(v,v,metric)==one,'unit reflection identity')
    for i,j in edges:
        require(dot(coords[i],coords[j],metric)==parameter,'reflection contact identity')
    return coords,edges


def encode_polynomial(p):
    return [str(c) for c in reversed(sp.Poly(p,T).all_coeffs())]


def field_encode(x):
    # ANP coefficient representation in descending order, normalized modulo F.
    return [str(c) for c in x.to_list()]


def bound_at_root(x, algebraic_field):
    """Rational interval Horner enclosure, with exact arithmetic only."""
    a,b=Fraction(str(LO)),Fraction(str(HI))
    low=high=Fraction(0)
    for q in x.to_list():
        values=(low*a,low*b,high*a,high*b)
        low,high=min(values)+Fraction(str(q)),max(values)+Fraction(str(q))
    return low,high


def audit(with_rigidity=False):
    require(F.is_irreducible,'F not irreducible')
    require(F.count_roots(-sp.oo,sp.oo)==1,'real embedding is not unique')
    require(sign_poly(F.diff())==1,'F not strictly increasing')
    require(F.eval(sp.Rational(1,2))<0<F.eval(sp.Rational(3,5)),'root endpoint bracket')
    require(F.eval(LO)<0<F.eval(HI),'fine root bracket')
    H=[[O if i==j else t for j in range(3)] for i in range(3)]
    Hinv=[[((1/(1-t)) if i==j else Z)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
    a,ea=reflect((0,5,11),A_STEPS,H,t)
    b,eb=reflect((1,2,4),B_STEPS,H,t)
    edges=sorted(ea|eb|{tuple(sorted(e)) for e in CROSS})
    require(len(edges)==24 and len(a)+len(b)==13,'graph size')
    k=dot(a[6],a[7],H)
    require(all(dot(a[i],a[j],H)==k for i,j in combinations((6,7,9),2)),'new anchor triangle')
    w=dot(b[10],b[13],H)
    parent=[[dot(x,y,H) for y in (b[2],b[10],b[13])] for x in (b[2],b[10],b[13])]
    geometric_quantities={'1-t':1-t,'1+2t':1+2*t,'1+t':1+t,
                         '1-k':1-k,'1+2k':1+2*k,'1+k':1+k,
                         '1-w':1-w,'1+w':1+w,'common_neighbor_Gram':determinant(parent)}
    for name,value in geometric_quantities.items():
        require(sign_rat(value)==1,'geometric positive quantity: '+name)
    v=[2*t/(1+w)*(x+y)-z for x,y,z in zip(b[10],b[13],b[2])]
    require(dot(v,v,H)==O and dot(v,b[10],H)==dot(v,b[13],H)==t,'cross common neighbor')
    gamma=k/(1+k)
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t**2-t+1)
    require(mu**2==(1-t)**2*(1+2*t)*(1+2*k)/(1+k)**2,'orientation square')
    require(sign_rat(mu)!=0,'nonzero orientation')
    normal=matvec(Hinv,cross(b[12],v))
    factors={}
    coordinate_functions=None
    for epsilon in (-1,1):
        c=[gamma*x+epsilon*mu*y for x,y in zip(b[12],normal)]
        columns=[v,b[8],c]
        G=[[dot(x,y,H) for y in columns] for x in columns]
        rhs=[k,t,t-gamma*dot(v,b[12],H)]
        u=solve([[sum((x[i]*H[i][j] for i in range(3)),Z) for j in range(3)] for x in columns],rhs,Z)
        # Solve generically to calculate the norm residual, then clear its
        # determinant. This equals the bordered Gram determinant identically,
        # including all parameters at which the generic solve was singular.
        residual=O-dot(u,u,H)
        D=determinant(G)*residual
        bordered=[row+[value] for row,value in zip(G,rhs)]+[rhs+[O]]
        require(D==determinant(bordered),'Schur identity not exact')
        numerator=polynomial(D.numer)
        denominator=polynomial(D.denom)
        require(sign_poly(denominator)!=0,'determinant denominator')
        content, fs=sp.factor_list(numerator)
        for factor,multiplicity in fs:
            if factor.monic()==F.monic():
                require(epsilon==1 and multiplicity==1,'unexpected F factor')
            else:
                sign_poly(factor)
        require(numerator.gcd(F).degree()==(5 if epsilon==1 else 0),'branch root gcd')
        factors[str(epsilon)]={'constant':str(content),
            'factors': [{'coefficients_ascending':encode_polynomial(p),'multiplicity':m} for p,m in fs],
            'denominator_ascending':encode_polynomial(denominator),
            'auxiliary_Gram_numerator_coprime_F':polynomial(determinant(G).numer).gcd(F).degree()==0}
        if epsilon==1:
            require(factors[str(epsilon)]['auxiliary_Gram_numerator_coprime_F'],'root-specific singularity')
            U=u
            W=[gamma*(x+y)+mu*z for x,y,z in zip(u,v,matvec(Hinv,cross(v,u)))]
            R=[[a[j][i] for j in (6,7,9)] for i in range(3)]
            require(sign_rat(determinant(R))==1,'anchor reconstruction pivot')
            # Matrix [U W V] R^-1 recovers all three A anchor columns.
            Rinv=[[x for x in solve(R,[O if i==j else Z for i in range(3)],Z)] for j in range(3)]
            anchors=[matvec([[U[i],W[i],v[i]] for i in range(3)],col) for col in Rinv]
            coordinate_functions=dict(b)
            for label,col in zip((0,5,11),anchors):coordinate_functions[label]=col
            for n,i,j,o in A_STEPS:
                coordinate_functions[n]=[2*t/(1+t)*(x+y)-z for x,y,z in zip(coordinate_functions[i],coordinate_functions[j],coordinate_functions[o])]
    # No imported incumbent input: evaluate the just-derived rational vectors
    # in QQ[t]/F, with real embedding selected by the certified rational box.
    K=sp.QQ.algebraic_field(sp.CRootOf(F.as_expr(),0))
    tau=K.unit
    def specialize(x):
        x=FIELD.convert(x)
        def evaluate_poly(p):
            result=K.zero
            for q in polynomial(p).all_coeffs():result=result*tau+K.convert(q)
            return result
        den=evaluate_poly(x.denom)
        require(den!=K.zero,'coordinate divisor at F')
        return evaluate_poly(x.numer)/den
    HK=[[K.one if i==j else tau for j in range(3)] for i in range(3)]
    coords={i:[specialize(x) for x in col] for i,col in coordinate_functions.items()}
    for n,i,j,o in ((3,1,4,2),(14,0,6,11)):
        coords[n]=[2*tau/(1+tau)*(x+y)-z for x,y,z in zip(coords[i],coords[j],coords[o])]
    contacts=[]
    max_noncontact_upper=Fraction(-2)
    for i in range(15):
        require(dot(coords[i],coords[i],HK)==K.one,'derived norm')
    for i,j in combinations(range(15),2):
        g=dot(coords[i],coords[j],HK)
        if g==tau:
            contacts.append((i,j))
        else:
            lo,hi=bound_at_root(g,K)
            require(hi<Fraction(17,40),'derived noncontact bound')
            max_noncontact_upper=max(max_noncontact_upper,hi)
    require(len(contacts)==30 and set(edges)<=set(contacts),'derived exact contacts')
    require((3,7) in contacts and (3,14) in contacts,'28-edge corollary restored contacts')
    core=sorted(set(range(15))-{3,14})
    digest=hashlib.sha256(json.dumps({str(i):[field_encode(x) for x in coords[i]] for i in range(15)},sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','sympy_version':sp.__version__,
            'core_vertices':core,'core_edges':edges,'factorizations':factors,
            'geometric_positive_quantities':sorted(geometric_quantities),
            'all_factor_signs_by_exact_Sturm':True,'allowed_orientation':1,'excluded_orientation':-1,
            'F_ascending':encode_polynomial(F),'F_irreducible':True,'F_has_one_real_root':True,'fine_root_bracket':[str(LO),str(HI)],
            'derived_incumbent_contacts':contacts,'derived_incumbent_noncontacts_below':'17/40',
            'derived_coordinate_digest':digest,'original_author_input_files':0,
            'strengthened_hypothesis_unequal_pairs':sorted([sorted((n,o)) for n,i,j,o in A_STEPS+B_STEPS]+[[2,9]])}
    if with_rigidity:
        result['rigidity']=rigidity(coords,edges,core,HK,K)
    return result


def modular_rank(rows):
    """An independent prime-field lower-rank certificate from a root of F."""
    for prime in (101,103,107,109,113,127,131,137,139,149):
        for root in range(prime):
            if int(F.eval(root)) % prime:
                continue
            a=[]
            try:
                for row in rows:
                    out=[]
                    for entry in row:
                        value=0
                        for c in entry.to_list():
                            q=Fraction(str(c))
                            if q.denominator % prime == 0:
                                raise ZeroDivisionError
                            value=(value*root+q.numerator*pow(q.denominator,-1,prime)) % prime
                        out.append(value)
                    a.append(out)
            except ZeroDivisionError:
                continue
            rank=0
            pivots=[]
            for col in range(len(a[0])):
                pivot=next((i for i in range(rank,len(a)) if a[i][col]),None)
                if pivot is None:
                    continue
                a[rank],a[pivot]=a[pivot],a[rank]
                inv=pow(a[rank][col],-1,prime)
                a[rank]=[(v*inv)%prime for v in a[rank]]
                for i in range(rank+1,len(a)):
                    if a[i][col]:
                        q=a[i][col]
                        a[i]=[(v-q*w)%prime for v,w in zip(a[i],a[rank])]
                pivots.append(col)
                rank+=1
            require(rank==36,'independent modular rank differs')
            return {'prime':prime,'F_root_mod_prime':root,'rank':rank,'pivot_columns':pivots}
    raise ValueError('no bounded valid prime specialization')


def rigidity(coords, edges, labels, metric, K):
    """Independent infinitesimal circuit audit at the unique core."""
    positions={v:i for i,v in enumerate(labels)}
    rows=[]
    for v in labels:
        row=[K.zero]*39
        p=matvec(metric,coords[v])
        row[3*positions[v]:3*positions[v]+3]=[2*x for x in p]
        rows.append(row)
    for i,j in edges:
        row=[K.zero]*39
        row[3*positions[i]:3*positions[i]+3]=matvec(metric,coords[j])
        row[3*positions[j]:3*positions[j]+3]=matvec(metric,coords[i])
        rows.append(row)
    _,pivots=linear(rows,K.zero)
    rank=len(pivots)
    transposed=[list(col) for col in zip(*rows)]
    rr,cols=linear(transposed,K.zero)
    free=[j for j in range(37) if j not in cols]
    require(rank==36 and len(free)==1,'not a one-stress rigid circuit')
    stress=[K.zero]*37;stress[free[0]]=K.one
    for row,c in zip(rr,cols):stress[c]=-row[free[0]]
    require(all(sum((rows[i][j]*stress[i] for i in range(37)),K.zero)==K.zero for j in range(39)),'stress not exact')
    edge_stress=stress[13:]
    nonzero_edges=[list(e) for e,x in zip(edges,edge_stress) if x!=K.zero]
    total=sum(edge_stress,K.zero)
    require(total!=K.zero,'zero t derivative stress')
    require(len(nonzero_edges)==24,'a core contact has zero stress')
    signs=[]
    for x in edge_stress:
        if x==K.zero:signs.append(0)
        else:
            a,b=bound_at_root(x/total,K)
            require(a>0 or b<0,'stress sign interval inconclusive')
            signs.append(1 if a>0 else -1)
    modular=modular_rank(rows)
    return {'independent_modular_rank_certificate':modular,
            'normalized_edge_stress_coefficients_descending': [field_encode(x/total) for x in edge_stress],
            'fixed_t_jacobian_rank':rank,'position_columns':39,'rows':37,
            'nonzero_contact_stress_edges':nonzero_edges,'stress_sum_nonzero':True,
            'normalized_edge_stress_signs':signs,
            'negative_normalized_stress_edges':[list(e) for e,s in zip(edges,signs) if s==-1],
            'positive_normalized_stress_edges':[list(e) for e,s in zip(edges,signs) if s==1],
            'stress_digest':hashlib.sha256(json.dumps([field_encode(x) for x in stress],separators=(',',':')).encode()).hexdigest()}


def main():
    p=argparse.ArgumentParser();p.add_argument('--rigidity',action='store_true');p.add_argument('--check',type=Path)
    args=p.parse_args();result=json.loads(json.dumps(audit(args.rigidity)))
    if args.check:
        require(result==json.loads(args.check.read_text()),'expected output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
