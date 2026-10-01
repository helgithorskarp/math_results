"""Universal seven-variable identities from ORIGINAL edges and vertices.

Author six-rupert-2, researcher. Sparse exact polynomial comparison, no samples.
"""


def require(ok,message):
    if not ok:
        raise ValueError(message)


def identities(M, MV, contacts, coefficients, c0, b, S, B, K, wrong_sign=False):
    Q, V = M.Q, M.V
    R = MV.Ring(Q, 7)
    z = R.zero
    r = (z, R.variable(0), R.variable(1))
    w = (R.variable(2), R.variable(3), R.variable(4))
    C = (z, R.variable(5), R.variable(6))
    e = R.vector(M.E)
    w0 = R.cross(e,r)
    p, rho = w[1:], w[0]
    rt, wt = r[1:], w0[1:]
    bp, bt = [R.constant(x) for x in b], [R.constant(x) for x in B[1:]]
    sr = [R.add(*(R.scale(S[i][j],rt[j]) for j in range(2))) for i in range(2)]
    jsp = (R.neg(sr[1]),sr[0])
    actual = z
    for weight, (a,bb,j) in zip(coefficients,contacts):
        edge = M.sub(V[bb],V[a]); h = M.dot(M.cross(edge,M.E),V[j])
        v = R.vector(V[j])
        m = R.vector_scale(R.constant(1/h),R.cross(R.vector(edge),R.vector_add(e,r)))
        f = R.dot(m,R.vector_add(R.cross(w,v),R.cross(w,R.cross(w,v)),C))
        actual = R.add(actual,R.scale(weight,f))
    # Independent aggregate moment expansion.
    bpart = R.add(R.dot((R.neg(bp[1]),bp[0]),p),
                  R.multiply(R.dot(bp,rt),R.dot(p,p)),
                  R.multiply(rho,R.dot(bp,p)))
    base = R.add(R.dot(jsp,p),R.neg(R.multiply(rho,R.dot(p,sr))),
        *(R.scale(S[i][j],R.multiply(p[i],p[j])) for i in range(2) for j in range(2)),
        R.neg(R.scale(c0,R.dot(w,w))))
    rest = R.add(R.multiply(rho,R.dot(bt,rt)),R.neg(R.scale(B[0],R.dot(rt,p))),
        R.scale(B[0],R.multiply(rho,R.dot(wt,p))),
        R.multiply(R.dot(p,bt),R.dot(wt,p)),
        R.neg(R.multiply(R.dot(bt,wt),R.dot(w,w))),
        R.scale(K,R.dot(w0,C)))
    formula = R.add(bpart,base,rest)
    if wrong_sign:
        formula = R.add(formula,R.scale(-2,R.dot((R.neg(bp[1]),bp[0]),p)))
    require(actual == formula, 'direct original edges equal aggregate moment formula')
    # Bilinear companion form, denominator cleared; no samples.
    A = [[c0*int(i==j)-S[i][j] for j in range(2)] for i in range(2)]
    Nt = [R.add(wt[i],R.neg(p[i]),R.multiply(rho,rt[i])) for i in range(2)]
    Nx = R.add(rho,R.dot(rt,p))
    Den = R.add(R.one,R.dot(wt,p))
    pair = R.add(bpart,
        *(R.scale(A[i][j] + B[0]*((0,-1),(1,0))[i][j],R.multiply(p[i],Nt[j])) for i in range(2) for j in range(2)),
        R.neg(R.scale(c0,R.multiply(rho,Nx))),
        R.multiply(rho,R.dot(bt,rt)),
        R.neg(R.multiply(R.dot(p,rt),R.determinant2(p,bt))),
        R.neg(R.multiply(R.dot(bt,wt),R.multiply(rho,rho))),
        R.scale(K,R.dot(w0,C)))
    require(actual == pair,'direct original edges equal bilinear companion formula')
    # Exactly zero identity and exact mirror-root slack, all r independent.
    def substitute(polynomial, substitutions):
        out = z
        for powers, coefficient in polynomial.items():
            term = R.constant(coefficient)
            for variable,power in enumerate(powers):
                for _ in range(power):
                    term = R.multiply(term,substitutions.get(variable,R.variable(variable)))
            out = R.add(out,term)
        return out
    require(substitute(actual,{2:z,3:z,4:z,5:z,6:z})==z,'identity root retained')
    mirror = substitute(actual,{2:z,3:wt[0],4:wt[1],5:z,6:z})
    require(mirror==R.multiply(R.add(R.one,R.dot(rt,rt)),R.dot(bp,rt)),
            'entire exact mirror slack (1+|r|^2)b.r retained')
    return {'variables':7,'monomials':len(actual),'degree':max(map(sum,actual)),
            'polynomial_sha256':M.digest(R.terms(actual)),
            'direct_moment_identity':True,'bilinear_companion_identity':True,
            'identity_zero':True,'mirror_slack_identity':True}
