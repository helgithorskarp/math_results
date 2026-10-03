# A bounded polynomial model for three arbitrary additions to the twelve-point core

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
An ordinary lossless reduction, supported by exact polynomial identities
and exact feasible controls. Independent review and formalization of this
reduction are pending. No infeasibility certificate, whole-frame exclusion,
new global separation bound or optimizer occurrence is established.

**Theorem.** Put I=[14/25,593/1000]. Fifteen distinct unit points whose
different-point products are at most t in I, containing the original
twelve-point twenty-contact core specified below, exist if and only if
the nine-variable polynomial system in this proof has a real solution.
The three points outside the core are arbitrary. The system has one
positive radical equation, six bounded stereographic variables for the
three added points, 72 explicitly cleared packing inequalities, the
original core chart packing inequality and its strict regularity
inequality. The added points need no unit equations. Every core numerator
is an integral polynomial affine in the one radical variable.

The statement holds throughout I, including its endpoints. Adding the
exact condition t<tau gives the equivalent conditional strict-improvement
problem, where tau is the distinguished root of
F(t)=13t^5-t^4+6t^3+2t^2-3t-1. Equivalently add the single integral
strict predicate -F(t)>0, keeping the same nine variables. Neither rational root-bracket endpoint replaces
tau. This preserves the entire critical strip. Feasibility or infeasibility
of that strict-improvement system remains unresolved.

The stereographic construction is classical. The result here is its
explicit, bounded, denominator-safe integration with the complete
original twelve-point frame and all three arbitrary additions. It reduces
their nine coefficient coordinates and three sphere equations to six
coordinates and no sphere equations. It does not assert historical
priority for stereographic coordinates, Gram identities, or known
incumbent configurations.

## The imported complete core

The core labels and twenty required equalities are

```
CORE = {0,1,2,4,5,6,7,8,9,10,11,12}
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12.
```

Additional contacts are allowed. The logical external dependency is the
[complete original twelve-core frame](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-frame/PROOF.md),
Discovery Net LEMMA9774/0. It proves that every such core on I has the
coefficient basis (p1,p2,p4), metric H_t=(1-t)Id+t11^T, with1 the all-ones column, the sole branch
(epsilon,eta)=(-1,+1), the finite circle chart z, and g>1/2. It also proves
the complete converse. Its full interval pruning certificate and ordinary
packing-to-frame proof are imported, rather than inferred from any local
or fixed-point result. The independent
[frame audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-frame-audit/REVIEW.md),
REVIEW9809/0, concerns that prior frame; it does not review this reduction.

Write <x,y>_t=(1-t)sum_i x_i y_i+t(sum_i x_i)(sum_i y_i).
The eigenvalues of H_t are 1-t,1-t,1+2t, so it is positive definite on I.
For later formulas let

```
a=1+t, b=1-t, c=1+2t, D=b^2 c, C=1+D z^2,
K=t(9t^2-2t-3), J=a^2+K=9t^3-t^2-t+1, h=9t^2-1,
S=D(t z^2-2z)+t(2t-1), E=C^2-S^2,
G=a^4[(1-t^2)C^2-S^2]-K^2 C^2+2SKt a^2 C.
```

Then k=K/a^2, s=S/C and g=G/(a^4 C^2) have the meanings in the imported
frame. In particular s is the product p7.p10. These definitions are
integral polynomials. E here is a polynomial denominator factor, and
does not denote the parameter-error quantity in the separate local gate.

## Positive clearing and integral core numerators

Let e0,e1,e2 be the coefficient unit vectors and put
L(v)=c v-t(sum_i v_i)(1,1,1). Thus H_t^{-1}v=L(v)/(bc).
The following six polynomial vectors are a^2 times the B-cluster points:

```
N1=a^2 e0, N2=a^2 e1, N4=a^2 e2,
N8=(-a^2,2ta,2ta), N10=(2ta,2ta,-a^2),
N12=(2t(1+3t),3t^2-2t-1,-2ta).
```

All cross products below are ordinary cross products of coefficient
vectors. Define

```
Wn=(D z^2-1)a^2 e0+2t N12+2bz L(N12 cross e0),
Wd=a^2 C,
Vd=bc a^6 E,
Vn=bc a^2[(KC-St a^2)Wn+C(t a^2 C-SK)N10]
   -w L(Wn cross N10),
Un=K(Vd Wn+Wd Vn)-a(3t-1)L(Wn cross Vn),
Wl=J Vd Wn, Vl=J Wd Vn,
Omega=h J Wd Vd = h J bc a^8 C E.
```

Set twelve polynomial numerators Y_i by

```
Y_i=h J C Vd N_i                    (i=1,2,4,8,10,12),
Y6=h Un, Y7=h Wl, Y9=h Vl,
Y0=a(2t Un+2t Wl+b Vl),
Y5=a(b Un+2t Wl+2t Vl),
Y11=a(2t Un+b Wl+2t Vl).
```

The decoded core is P_i=Y_i/Omega. These are exactly the imported
(-1,+1) frame after substituting

```
w=a^2 C sqrt(Dg),        w^2=D G,        w>0.
```

In particular the minus sign in Vn is the original epsilon=-1. The Un
formula results from its eta=+1 branch and negative mu, not from an
additional orientation quotient. Straight substitution in that frame's
equations proves these formulas. [model.py](model.py) implements the
displayed factored ring operations without division. An independent
exact specialization to every incumbent core coefficient also checks
their scale and orientation.

Here and throughout the model impose the two core predicates

```
b^2 z^2<=1,        2G>a^4 C^2.
```

The second is precisely the imported strict g>1/2. All clearing factors
are strictly positive on this domain. To prove this without any numerical
division test, use the exact square identities

```
G=a^4(1-t^2)E-(KC-St a^2)^2,
G=(a^4-K^2)(1-t^2)C^2-(S a^2-KtC)^2.
```

The first gives
E/C^2>1/[2(1-t^2)]>=625/858>0. The second gives |k|<1 and g<=1.
Also a,b,c,C>0; h>0 since t>=14/25; J>1 since
J(14/25)>1 and J'=27t^2-2t-1>0 on I. Thus Omega>0 and the frame has no
missing zero-denominator branch on its entire feasible domain.

The core chart gives |z|<=1/b<=1000/407<5/2 and
D z^2<=c, so C<=1+c=2a. Since D'=-6t(1-t)<0 and
D(14/25)<1/2, and since a<8/5, one has
w^2=a^4 C^2 Dg<2(8/5)^6<36. The positive lift therefore satisfies
0<w<6. These are whole-domain bounds, not bounds checked only at the
incumbent or at finitely many parameter samples.

For clarity, the generic identities of the core can be checked without
expanding any huge certificate. In Z[t,z,w] reduce modulo the monic
relation w^2-DG. [check.py](check.py) verifies all 12 unit identities,
20 literal contacts, 12 internal noncontact identities, the chart-product
and s-product identities, and all 18 scalar components of the six
reflection identities. The resulting 64 exact identities are zero
polynomials. Every Y_i is affine in w, while Omega is independent of w.
There is no rounding, solver tolerance, or sample-point substitution in
these generic checks.

The internal noncontact products are Hn/a, K/a^2 or ell, where

```
Hn=4t^2-a, r=2t/a, ell=r(Hn/a+K/a^2)-t.
```

Hn/a occurs at (0,9),(5,6),(7,11),(1,8),(2,12),(4,10);
K/a^2 at (6,7),(6,9),(7,9),(4,12),(8,10); ell at (8,12).
All are strictly below t on I, because
Hn-ta=(3t+1)(t-1)<0,
K-ta^2=4t(2t+1)(t-1)<0,
and 0<r<1 gives ell<2rt-t<t. These identities justify omitting exactly
those twelve already satisfied comparisons, not any cross-cluster test.

Of the 36 products between A={0,5,6,7,9,11} and B={1,2,4,8,10,12},
(7,12) and (9,10) are contact identities. The exact identity

```
<P7,P1>_t-t = bc/C * (b^2 z^2-1)
```

turns the (7,1) comparison into the core chart predicate. The remaining
33 comparisons are precisely A cross B except those three pairs.
In particular the (6,8) comparison is retained.

## Six bounded coordinates for the three arbitrary points

For one arbitrary added point use two fresh real variables u,v. Define

```
R=b[(1+t)(u^2+v^2)+2tuv], A=1+R,
T=(R-1-2t(u+v),2u,2v), X=T/A.
```

There is no new radical. In the H_t metric,
f1=e1-t e0 and f2=e2-t e0 are perpendicular to e0, with
<f1,f1>=<f2,f2>=1-t^2 and <f1,f2>=t(1-t). Hence R is the squared norm
of u f1+v f2. In particular
R=b(u^2+v^2)+bt(u+v)^2>=0 and A>=1.
Direct multiplication gives

```
<T,T>_t=A^2, <T,e0>_t=R-1, A-<T,e0>_t=2.
```

Thus X is unit for every real u,v and its anchor product is (R-1)/(R+1).
These three identities and the disk and anchor-gap factorizations are
also checked as integer polynomial identities in fresh local variables
(t,u,v), without using the core radical relation.

Conversely, take any unit X allowed by packing with the actual core
anchor P1=e0. If alpha=<X,e0>_t<=t<1, its unique inverse is

```
u=X_1/(1-alpha),       v=X_2/(1-alpha).
```

Indeed X-alpha e0=(1-alpha)(u f1+v f2); its squared norm is 1-alpha^2,
so R=(1+alpha)/(1-alpha) and A=2/(1-alpha). These give the displayed
X=T/A component by component. The omitted stereographic pole is exactly
the existing anchor e0, forbidden for every arbitrary addition by its
packing inequality. At u=v=0 the antipode -e0 is included. No sign of u
or v, support triple, contact count, initial proximity, or fixed point13
has been imposed.

The same anchor inequality bounds the whole chart:

```
R<=(1+t)/b,
u^2+v^2<=R/b<=(1+t)/b^2<10,
10(407/1000)^2-1593/1000=6349/100000>0.
```

Since (16/5)^2>10, the closed box [-16/5,16/5]^2 covers every permitted
point, with strict slack. Use three distinct variable pairs
(u0,v0),(u1,v1),(u2,v2). Reusing local slots in a universal identity check
never identifies these six variables in the feasibility system.

## The complete nine-variable system and both directions

Use real variables (t,z,w,u0,v0,u1,v1,u2,v2) with

```
t in [14/25,593/1000], z in [-5/2,5/2], w in [0,6],
each uj,vj in [-16/5,16/5],
w^2=DG, w>0, b^2 z^2<=1, 2G>a^4 C^2.
```

For each j let T_j,A_j be its displayed chart polynomials. Impose all of
the following integral polynomial nonnegativities:

```
t Omega^2-<Y_i,Y_k>_t>=0
    for (i,k) in A cross B except (7,12),(9,10),(7,1): 33 tests;
t A_j Omega-<T_j,Y_i>_t>=0
    for j=0,1,2 and i in CORE: 36 tests;
t A_j A_k-<T_j,T_k>_t>=0
    for 0<=j<k<=2: 3 tests.
```

[SYSTEM.json](SYSTEM.json) gives every literal pair and exact bound.
The ring-only `constraints` function in [model.py](model.py) generates all
94 defining polynomials: one equality, two strict domain predicates,
19 weak domain predicates (including the chart), and72 packing tests.
The exact controls check every generated polynomial in all four cases.
The 72 cleared packing tests plus the single core chart packing predicate
give 73 packing inequalities. The twenty contacts and twelve internal
noncontacts are identities already accounted for, so
20+12+1+33+36+3=105 covers every pair of fifteen points. The regularity
inequality is a separate imported necessary restriction. For strict improvement the same generator with `strict_improvement=True`
adds just -F(t)>0, yielding95 defining polynomials. Indeed
F'(t)=65t^4-4t^3+18t^2+4t-3 is bounded below on I by
65(14/25)^4-4(593/1000)^3+18(14/25)^2+4(14/25)-3>0.
The exact root bracket lies inside I and its two endpoint F signs differ,
so F is strictly increasing with unique root tau on all of I. Therefore
F(t)<0 is exactly t<tau, even inside the arbitrarily narrow critical strip.
The four incumbent controls each give -F(tau)=0 and fail precisely this
strict predicate; none is discarded from the base model. The constraints
do not fix or quotient the added-point permutation, and all three mutual
comparisons and all three added-anchor comparisons are retained.

**Forward direction.** Given a fifteen-point packing containing the
original twenty-contact core, apply the complete9774 frame to its twelve
labelled points. Take the surviving z and positive w as above. The proved
bounds put t,z,w in their boxes. Encode each of the three arbitrary
remaining points by its unique pole-free chart inverse; the anchor
inequality puts all six variables in their boxes. Since Omega>0 and every
A_j>0, clearing each actual product comparison gives exactly the 72
displayed polynomial nonnegativities. Every model condition is satisfied.

**Reverse direction.** Given a solution of the polynomial system,
Omega>0 and A_j>=1 make all decodings defined. The positive radical
equation and branch recover precisely the original frame. The generic
identities and its imported converse give the twelve unit points and
twenty required contacts. The internal noncontact formulas, chart
predicate and 33 core comparisons ensure every core product is at most
t. The universal chart identities give three added unit points. Positive
clearing turns all36 added-core and all3 mutual polynomials into their
actual packing comparisons. H_t is positive definite, so choosing any
real three-dimensional basis with this Gram matrix realizes these
coefficient vectors on the unit sphere. All fifteen names are distinct:
equality of any two unit points would give product1>t. This proves the
lossless equivalence.

## Exact controls, trust boundary and what remains open

The copied [INPUT.json](INPUT.json) and [field.py](field.py) are byte-identical
to the credited
[twelve-core stability source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-completion/INPUT.json).
The quotient arithmetic kernel and alternate point are also credited to
[the earlier field certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/thirteen-core-completion/field.py)
and [the alternate completion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/fourteen-point-completion/certificate.json).
Neither a fixed thirteenth point nor either prior capacity theorem is a
logical premise of this reduction. Unused archived metadata such as
candidate Gram permutations and cap bounds is not interpreted as evidence.

[incumbents.py](incumbents.py) isolates the exact root, transforms all
reference coefficients into the anchor basis, checks every new core
numerator, and proves the four known triples {p3,a,b},
a in {p13,q}, b in {p14,c14}, satisfy the new system exactly. It checks
all288 cleared packing comparisons in those four controls. Each has
ten zero and62 strict gaps; the omitted contacts are the twenty automatic
core equalities. These are known positive controls, not new configurations
or evidence for global completeness. Polynomial reduction in Q[T]/F and
the bracketed real-root evaluation suffice; no unproved irreducibility
assumption is needed for an inverse whose identity is checked exactly.

[polynomials.py](polynomials.py) performs sparse integer polynomial
arithmetic and monic radical reduction. [check.py](check.py) executes76
generic identities, the whole-domain scalar bounds and all four exact
controls. [controls.py](controls.py) rejects27 damaged scope descriptions
and5 invalid polynomial inputs, detects two damaged coordinate identities,
and accepts3 harmless scope changes and3 finite chart controls.
Normal and optimized Python run the complete checks independently under
identical frozen runtime pins, with the actual results and costs in
[VALIDATION.json](VALIDATION.json). They are same-author checks, not
independent mathematical review. The trust boundary is ordinary algebra,
the imported complete9774 proof/certificate and the standard-library
exact checkers, rather than a proof assistant or solver UNSAT claim.

The separate
[moving-frame gate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-local-gate/PROOF.md),
LEMMA9866/0, may eventually close a rigorously reached small parameter
tube. It is not a constraint of this system. The complementary
[fullG20 triangle bridge obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/eleven-triangle-bridge-obstruction/PROOF.md),
LEMMA9878/0, supplies geometric context but no premise here. Whole-domain
exclusion for the three arbitrary additions, and occurrence of this core
in every relevant optimizer, both remain open. A concrete next step is
a small exact exclusion or conditional inequality on this bounded model,
keeping the exact t<tau condition and using the local gate only after its
parameter-tube hypothesis has actually been certified.

At the prepublication refresh, the complete signed
[independent audit and derivation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-local-gate-audit/DERIVATION.md),
REVIEW9898/0, was read and bound to its published source. It confirms9866
relative to the named ordinary local lemmas and proves1122delta stability
on the same delta domain, with sufficient subcritical tube
24|t-tau|+3|z-z0|<=2e-10. This is a credited contextual improvement for a
future stopping argument, not a new constraint or a verdict on the present
polynomial reduction. The capacity and occurrence obligations are unchanged.
