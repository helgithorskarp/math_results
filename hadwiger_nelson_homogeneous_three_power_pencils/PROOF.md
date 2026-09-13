# Homogeneous pencils on three powers cannot concur

Put E=Z[omega], where omega=(1+i sqrt(3))/2, omega^2=omega-1. Its six units are the complex sixth roots of unity. Reducing E modulo 2 gives F4; the two lifts of each nonzero residue among the six units differ by sign.

## 1. General theorem

Fix **distinct nonnegative integers 0<=p<q<r**. Take five coefficient rows in
`({0} union E^units)^3`, each supported on at least two coordinates. Assume their five distinct projective reductions modulo 2 are the projective line of a two-dimensional subspace of F4^3. Thus they define the full five-section homogeneous pencil, with no coordinate (monomial) direction.

**Theorem.** There is no z in C for which all five expressions

    a_j z^p + b_j z^q + c_j z^r       (j=1,...,5)

have modulus exactly one.

The theorem applies to any three nonnegative radix positions, not just positions 1,...,4; exponent zero denotes the constant 1. Here homogeneous refers to the three formal coefficient variables. Setting one variable to z^0=1 produces an affine pencil in the remaining colour variables. It is a physical nonconcurrence theorem: complex conjugation in the squared norms is actual conjugation. No claim is made here about independent complexified conjugate variables for arbitrary exponents.

For the fixed-scale A5 architecture T+zT+...+z^4T, T={0,1,omega}, this excludes all **36** homogeneous pencils supported on exactly three nonconstant positions and all **4,608** lifts. The explicitly selected h4195 residual contains 24 of them and 3,072 lifts. The theorem remains valid if additional event curves are active; these five cannot coexist at a physical parameter at all.

This does not cover pencils involving four or more coefficient positions, or an architecture with an additional arbitrary common scale factor. Including exponent zero recovers the physical exclusion of the earlier two-coordinate affine pencils; it does not assert that every nonhomogeneous pencil is covered. It neither closes A5 nor gives a new chromatic bound for the plane.

## 2. Normalize to 32 unit-form systems

A projective line in F4^3 containing no coordinate direction has exactly three points supported on two coordinates, one on each coordinate pair, and two points supported on all three. Indeed, its two-dimensional normal space intersects each coordinate plane in a line. Two of these intersections could coincide only at a coordinate direction, which is excluded.

Multiply the variables separately by Eisenstein units and rescale individual rows by units. The first two binomial rows become U+V and U+W. The third becomes V+epsilon W, with epsilon in {+1,-1}. To see the third sign, reduce the first two normalized rows modulo 2. Their projective span has third two-coordinate direction (0,1,1); the unit lifting its last coefficient must therefore be +1 or -1.

The two full-support directions in this span are (1,omega,omega^2) and (1,omega^2,omega). After unit row rescaling, the remaining two forms are

    U + sigma omega V + tau omega^2 W,
    U + kappa omega^2 V + lambda omega W,

where sigma,tau,kappa,lambda independently belong to {+1,-1}. There are therefore exactly 32 sign cases.

All variable changes used here preserve |U|,|V|,|W|. More explicitly, if the two original anchor rows are (a,b,0) and (c,0,d), choose

    U=a z^p,   V=b z^q,   W=(a d/c) z^r.

The first row is U+V and the second is the unit c/a times U+W. Dividing each remaining row by its U or V coefficient gives the asserted signs. The checker verifies this algebraic normalization for every lift and also finds the same unique sign case by a separate exhaustive diagonal-unit gauge search.

The unit condition on U+V permits one further common rotation, dividing U,V,W by U+V, so that U+V=1. This preserves all moduli. Write

    U=a+i sqrt(3)b,   V=1-a-i sqrt(3)b,   W=c+i sqrt(3)d,

with a,b,c,d real. In the certificate the monomial variable order is (d,c,b,a). The factor sqrt(3) is part of the representation: squared norm is a^2+3b^2, not a^2+b^2.

## 3. Radius rigidity of the free-vector systems

**Lemma.** Suppose the five normalized forms in Section 2 all have modulus one, with U,V,W arbitrary complex numbers. Then either two of |U|,|V|,|W| are equal, or

    {|U|^2,|V|^2,|W|^2} = {1/4,3/4,7/4}.

For each sign case let F_1,...,F_4 be the four remaining squared-norm-minus-one polynomials after U+V=1 is imposed. These are quadratics over Q in d,c,b,a. Put

    u=|U|^2,  v=|V|^2,  w=|W|^2,
    Delta=(u-v)(u-w)(v-w).

The portable certificate supplies 161 identities in total, organized into the 32 cases. Each has the form

    G_j = sum_{i=1}^4 h_{ji} F_i.

The multipliers h_{ji} have rational coefficients and degree at most two; every identity has total degree at most four. Thus each G_j vanishes at every common zero of the four original equations. The checker reconstructs F_i directly from the unit forms and verifies every coefficient of every identity using integers and Python Fraction arithmetic.

In 20 cases, exact polynomial division by the supplied G_j reduces Delta to zero. In the other 12 cases, it reduces each of

    Delta (4u-1)(4u-3)(4u-7),
    Delta (4v-1)(4v-3)(4v-7),
    Delta (4w-1)(4w-3)(4w-7)

to zero. Products may be reduced after each factor: each division preserves congruence modulo the ideal generated by G_j. A zero final remainder is an exact ideal-membership identity. **The verifier does not need to assume or prove that the G_j form a Groebner basis**; it only uses the identities and successful zero remainders. It does not infer anything from a nonzero remainder.

If Delta=0, two squared moduli are equal. Otherwise u,v,w are three distinct roots of (4t-1)(4t-3)(4t-7), hence are exactly the three stated rational numbers. This proves the lemma. There is no division by a parameter or an unrecorded positivity argument in its algebraic certificate.

Both alternatives really occur for free vectors:

- With all five signs positive, U=V=W=1/2 gives five unit forms and squared radii (1/4,1/4,1/4).
- With all five signs negative, U=i sqrt(3)/2, V=1-i sqrt(3)/2, W=1/2 gives squared radii (3/4,7/4,1/4).

These exact positive witnesses are retained in the controls. The lemma is not an assertion that arbitrary three-vector systems are inconsistent. The first witness also shows why distinct radix exponents are an essential hypothesis in the theorem.

## 4. Exclude the all-unit case

There is no normalized solution with |U|=|V|=|W|=1. Since U+V=1, the only possibilities for (U,V) are (omega,conjugate(omega)) and its swap. The condition |U+W|=1 with |U|=|W|=1 implies W/U is one of the two primitive cube roots of unity. Thus U,V,W all belong to the six Eisenstein units.

Every one of the five unit-valued forms is now an Eisenstein integer of squared modulus one, hence an Eisenstein unit. Its reduction modulo 2 must be nonzero. But the five homogeneous failure hyperplanes form a full F4 pencil and cover F4^3: if its two defining linear values are A,B, then one of A, B, A+B, A+omega B, A+omega^2 B is zero. Applying this to the residue vector of (U,V,W) forces one of the five forms to be zero modulo 2, a contradiction.

For a direct finite check, the verifier enumerates all six-unit triples with U+V=1 for each of the 32 sign cases. There are 384 cases and zero survivors. This count accompanies the elementary argument; it is not a SAT or floating-point calculation.

## 5. Apply the lemma to a common radix

The original variable scalings were units and the final common scaling was a rotation, so

    u=rho^p,  v=rho^q,  w=rho^r,   rho=|z|^2.

If rho=0, at least two of the three distinct exponents are positive. The binomial form on those two positions vanishes and cannot have modulus one. This also treats exponent zero correctly, with z^0=1. If rho=1, all three moduli are one, which Section 4 excludes.

For rho>0 with rho!=1, the three squared moduli are distinct, so the equality alternative is impossible. If p=0, one squared modulus is exactly one, which is absent from the exceptional set. If p>0, all three are less than one when rho<1 and all three are greater than one when rho>1; the exceptional set lies on both sides of one. Thus the exceptional alternative is also impossible. These cases exhaust every physical complex z and prove the theorem.

Consequently, any simultaneously active full F4 pencil of five nonmonomial unit events must involve at least four coefficient positions. A full pencil on just two positions would contain a forbidden monomial direction, and a pencil on three positions is ruled out by the theorem. In A5, allowing the constant position gives 9*C(5,3)=90 such pencils; 54 are the previously excluded two-nonconstant-position family, and 36 are the homogeneous three-nonconstant-position family treated by the present residual interface. No injectivity assumption is used: collisions do not evade the norm equations.

## 6. Exhaustive finite normalization and the A5 interface

There are 54 Eisenstein-unit rows on three variables, supported on at least two coordinates, modulo common unit row scaling. They give 18 realized projective F4 normals. The checker explicitly constructs their 64-point zero masks and tests all five-normal subsets for a cover. Exactly nine covers occur; their bucket sizes are 2,2,2,4,4. Thus there are 9*128=1,152 lifted systems on a fixed triple of positions.

Each of the 32 normalized sign cases occurs 36 times. A second normalization check exhausts 41,472 diagonal-unit gauges and verifies the unique case for every lift, rather than just comparing aggregate counts. Choosing three of the four nonconstant A5 positions gives 36 pencils and 4,608 lifts.

`a5_interface.py` independently constructs the nine projective normal spaces as kernels of (1,alpha,beta), with alpha,beta nonzero in F4, and embeds them at the four position triples. It checks that every selected homogeneous three-position pencil in the pinned h4195 residual is included. The interface records the exact 24 residual indices and signatures; its 3,072 lifts are therefore an entry-level consequence of the general theorem. This comparison does not import global pair-quotient completeness or any orbit allowance.

## 7. Optional stronger finite complex-affine result

For just the selected 24 h4195 pencils, `finite_a5.py` additionally proves that all 3,072 five-curve systems are nonconcurrent even after complexifying x and y independently in z=x+i sqrt(3)y. This is a stronger conclusion on a smaller finite class than the general physical theorem.

The script regenerates the h4105 curve polynomials, chooses the two smallest two-curve buckets of each pencil, and covers the full system by their four anchor pairs. It solves all 96 anchor pairs. For each irreducible algebraic component it substitutes into every curve in every remaining bucket and finds a bucket with no vanishing curve. Consequently no choice of one curve from each of the five sections can be concurrent. All 180 algebraic component records, counted with pair incidence, are covered; no real-root filter is applied.

Two exact elimination routes give the same complete canonical transcript: lexicographic Groebner decomposition with exceptional rational fibers, and a resultant followed by Euclidean gcds over Q[x]/q. Both fail on an unsupported nonlinear nonrational fiber rather than discard it. The 12 previously excluded A5 pencils are not part of this complex-affine claim: an attempted direct extension encountered such a fiber and was stopped. They **are** covered by the general physical theorem above.

This optional check imports SymPy and python-flint and the exact interface/helpers from the earlier C0 package. It is not a premise of the portable radius lemma or general physical theorem. Its 180 records are algebraic components with pair incidence, not 180 distinct parameters or realized graphs.

## 8. Research scope and trust

The general theorem's checker uses only CPython 3.11.2 standard-library integer and Fraction arithmetic. SymPy 1.14.0 and python-flint 0.8.0 were used to discover the 93,468-byte certificate by small exact Macaulay systems; these tools are not needed to verify it. No approximate predicate, solver UNSAT verdict, or unverified CAS ideal-membership assertion is part of the general proof. The reductions and interpretation are written mathematics, not a proof-assistant formalization. External independent review remains outstanding.

The A5 interface is grounded in h4105's norm events, h4171/h4179's pencil definitions, and h4195's literal residual export. The general theorem itself does not need the h4117/h4175/h4177 accounting claims, and this package does not repair or update those conditional allowances. The source review and all newly relevant teammate results were read before selection and refreshed before publication.

There is no physical configuration in the selected five-event class to feed to a chromatic solver. This is an exact construction exclusion, not a new non-four-colourable abstract graph, a plane realization of a five-chromatic graph, or an improvement of the 509-vertex record. Nonhomogeneous and four-position homogeneous pencils remain open here.
