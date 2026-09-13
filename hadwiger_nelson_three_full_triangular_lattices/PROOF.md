# Three full triangular lattices through a common point

Put `omega=(1+i sqrt(3))/2`, `R=Z[omega]`, and `K=Q(i sqrt(3))`.
Write `rho(a+b omega)=a-b (mod 3)` and `N(z)=z conjugate(z)`.
All graphs here have distinct physical points as vertices and **every**
Euclidean unit pair as an edge. They need not be planar graphs.

**Theorem.** For arbitrary complex numbers `alpha_0,alpha_1,alpha_2` of
absolute value one, the strict unit-distance graph on

```
alpha_0 R union alpha_1 R union alpha_2 R
```

has chromatic number at most four. It has chromatic number four if and only
if there is a unit edge `alpha_i z -- alpha_j w` with `rho(z)=rho(w)=0`.
Otherwise its chromatic number is three.

In particular every finite subset of any three unit triangular lattices
sharing a point is four-colourable. There is no patch-size, denominator,
angle, pairwise-irrationality, or distinct-lattice assumption. Reflections
are included because conjugation preserves R. Translate a common point to
zero and rotate to take `alpha_0=1`.

This is an unbounded construction-family exclusion. It is not a general
vertex lower bound or an improvement of the 509-vertex record.

## 1. Two elementary prerequisites

Reduction rho is a ring homomorphism, commutes with conjugation, and
`N(z)=rho(z)^2 (mod 3)`. In particular it properly three-colours R. Every
proper three-colouring of the full triangular lattice is this colouring
up to permutation: colours on one triangle force those on the adjacent
triangle across each edge, and the triangular tiling is connected.

We use the following pair lemma, proved in the
[earlier two-lattice theorem](../hadwiger_nelson_triangular_overlays/PROOF.md)
and its [independent review](../hadwiger_nelson_triangular_overlays_review1/README.md).
If `|alpha|=1` and `alpha not in K`, there is `epsilon in {1,-1}` such that
every cross unit edge `z -- alpha w` with both residues nonzero satisfies

```
rho(z) rho(w) = epsilon.                                      (1)
```

For completeness, the rational vector space
`W={t in K: alpha t + conjugate(alpha t) in Q}` has dimension at most one:
otherwise evaluation at 1 and omega recovers alpha in K. If contacts exist,
write `R intersect W=Z gamma`, with gamma having coprime integer coefficients,
and `alpha gamma + conjugate(alpha gamma)=p/q` in lowest terms. Each contact
has `w conjugate(z)=m gamma` and

```
mp = q (N(z)+N(w)-1).
```

When both residues are nonzero, the right parenthesis is 1 modulo 3 and
`m rho(gamma)=rho(w)rho(z)` is nonzero. Thus p,q,m,rho(gamma) are units
modulo 3, and (1) follows. If there are no such contacts either epsilon works.

Also, unit elements of K are integral and invertible at its unique place
above 3. Indeed its completion `K_3=Q_3(pi)`, `pi^2=-3`, has ramification
index two, residue field F3, and conjugation-invariant valuation `v(pi)=1`.
From `u conjugate(u)=1` we get `v(u)=0`. For z in R, v(z)>=0 and its residue
is rho(z). The graph on the whole field K is three-colourable: unit
differences have valuation zero and reduce to +/-1; colour each additive
valuation-ring coset by its residue after translation.

## 2. Three active interfaces force one quadratic extension

Call a pair of distinct K-classes of lattices active if there is a unit
contact between nonzero points in the two lattices. Two rotations are in
the same K-class if their ratio belongs to K. Different classes share only
zero, since a nonzero coincidence would express their ratio in K.

For a proper contact `z -- alpha w`, where `z,w in R` are nonzero, put
`c=w conjugate(z)` and `S=N(z)+N(w)-1`. Then

```
c alpha^2 - S alpha + conjugate(c) = 0.                       (2)
```

Here S is a positive integer, because nonzero Eisenstein norms are positive
integers. If alpha is outside K, (2) is its quadratic minimal equation,
its relative trace S/c is nonzero, and its discriminant
`S^2-4N(z)N(w)` is strictly negative. Nonpositivity follows from (2) and
the physical unit circle; equality would put alpha in K. Consequently

```
K(alpha) = K(sqrt(D))
```

for a positive rational D, which can be replaced by a positive squarefree
integer. This is a biquadratic CM field (or K if the extension is trivial).

**Quadratic compatibility lemma.** If alpha,beta have degree two over a
characteristic-zero field K, have nonzero relative traces, and generate
different quadratic extensions, then beta/alpha has degree four over K.

Proof: in their biquadratic compositum write `alpha=a+b u`, `beta=c+d v`,
where `u^2,v^2 in K` and all a,b,c,d are nonzero. Up to the nonzero scalar
`N_(K(u)/K)(alpha)`, their ratio is

```
ac - bc u + ad v - bd uv.
```

All four coefficients in the basis `1,u,v,uv` are nonzero. Each of the
three nonidentity sign automorphisms changes a nonzero coefficient, so
none fixes this ratio. Its orbit and degree are four. QED.

Thus, for three pairwise different K-classes with all three interfaces
active, alpha, beta and beta/alpha all satisfy quadratic equations (2),
and the compatibility lemma forces `K(alpha)=K(beta)=K(sqrt(D))`.

If two of the three rotations have ratio in K and the third class has
any proper cross contact, all three rotations still belong to one such
field. In applying (2), normalize by the rotation of the contacted lattice;
its points before rotation are in R. If there is no such contact, the
two classes glue at zero and can be three-coloured independently. If all
rotations belong to K after normalization, the whole-field colouring above
already applies.

## 3. The case where conjugation fixes a place above 3

Let `L=K(sqrt(D))` in the physical complex embedding, and let c denote
physical conjugation. Choose a place v above the unique place of K over 3.
Suppose c fixes v. The local degree over K_3 is at most two, so the residue
field k is F3 or F9. Every unit displacement d satisfies `d c(d)=1`, hence
`2v(d)=0`. All edges therefore stay in additive cosets of the valuation ring,
and can be coloured by reducing translated differences to k.

If c acts trivially on k, a unit displacement reduces to +/-1. The additive
Cayley graph with these two steps is a disjoint union of triangles, and is
three-colourable. If c acts nontrivially, necessarily `k=F9=F3[j]`, `j^2=-1`,
and c induces Frobenius `a+bj -> a-bj`. Its norm-one elements are exactly
`+1,-1,+j,-j`. The colouring

```
a+bj -> a+b in F3
```

changes on every one of these four steps. This is also a three-colouring.
Thus the entire strict graph UD(L) is three-colourable in this case.

This uses only standard facts about extensions of a discrete valuation:
local degree bounds residue degree; an invariant valuation has an induced
residue automorphism; F9 has its unique nonidentity F3-automorphism. We have
included the colouring and norm arguments, rather than assuming that every
biquadratic field is four-colourable. For the local-degree identity and
valuation extension facts, see J. S. Milne,
[Algebraic Number Theory, v3.08](https://www.jmilne.org/math/CourseNotes/ANT.pdf),
Chapter 7, especially Corollary 7.42, and Chapter 8 on completions at places.

## 4. The case where conjugation exchanges the two places

If c does not fix v, L has two distinct places over the place of K. Since
`[L:K]=2`, both completions are K_3. Let v_1 and `v_2=v_1 o c` be the two
integer-valued valuations, normalized by `v_1(pi)=v_2(pi)=1`. Their residues
on R both equal rho. For every nonzero z in R put

```
m(z)=v_1(z)=v_2(z)>=0.
```

For each unit rotation alpha_i in L put

```
t_i=v_1(alpha_i),        v_2(alpha_i)=-t_i,
eta_i=res_(v_1)(pi^(-t_i) alpha_i) in {1,-1}.                 (3)
```

Consider nonzero points `x=alpha_i z`, `y=alpha_j w`, and write
`m=m(z)`, `n=m(w)`. Their pairs of valuations are

```
x: (t_i+m, -t_i+m),       y: (t_j+n, -t_j+n).               (4)
```

An edge requires `v_1(x-y)+v_2(x-y)=0`.

**Primitive points.** If m=n=0 and `t_i != t_j`, both minima in subtracting
(4) are strict and their sum is `-|t_i-t_j|<0`, so the points are not adjacent.
If m=n=0 and `t_i=t_j=t`, give them sign colours

```
eta_i rho(z),       eta_j rho(w).                            (5)
```

Equal signs would give `v_1(x-y)>=t+1`, whereas `v_2(x-y)>=-t`, contradicting
the norm-one equality. Thus (5) is proper on all edges between primitive
points, including internal lattice edges.

**Residue-zero points.** Suppose m,n>=1. An edge implies

```
m+n = |t_i-t_j|.                                           (6)
```

Here is the complete valuation check, including ties. Equal heights give
both valuations at least their common height offsets plus min(m,n), hence
sum at least 2min(m,n)>0. Otherwise write `delta=t_j-t_i>0`. If
`|m-n|>=delta`, the sum of the two minimum valuations is `2min(m,n)>0`;
cancellation at a tie can only increase it. In the remaining case
`|m-n|<delta`, both minima are strict and their sum is `m+n-delta`.
Equality to zero is exactly (6). No equality case was discarded.

Associate to such a point the half-open interval

```
I(x)=[t_i-m,t_i+m).                                        (7)
```

By (6), adjacent residue-zero points have intervals touching end to end,
with disjoint interiors. Their centres are different. There are at most
three distinct heights t_i. Choose their middle height b; with one or two
distinct heights choose any middle height (either one for two). Colour x
with A if `b in I(x)` and with B otherwise.

This is proper. The interval union for two touching intervals contains both
centres in its interior. For any pair of different centres in a set of at
most three, their closed span contains the chosen middle centre, unless the
pair is on the same side; the latter would require at least four centres.
Thus b lies in exactly one of the two half-open intervals. Half-openness
is essential when their touching point is b. Their colours differ.

Use the two disjoint sign colours in (5) for primitive points and A,B for
residue-zero points. Mixed edges automatically change colour. Give the
origin colour A: its unit neighbours have `N(z)=1`, hence m(z)=0, so they
have sign colours. This proves the four-colour bound.

**Coinciding representations.** If `alpha_i z=alpha_j w != 0`, then
`alpha_j/alpha_i=z/w in K` is a unit complex number. Its K_3 valuation is
zero, so `t_i=t_j` and m(z)=m(w). Both the interval and the residue in (5)
are therefore representation-independent. Thus this colours physical points,
not just labelled copies. It actually proves the stronger statement for
any number of rotations in L having at most three distinct heights (3).

If there is no edge between residue-zero points, A and B may be identified,
giving a three-colouring.

## 5. The remaining active forests and the exact chromatic number

Only the case of three different K-classes whose active graph is a forest
remains. Give each lattice's nonzero residues signs `s_i rho(z)`, choosing
`s_i in {1,-1}` along the forest so that on every active pair
`s_i s_j=-epsilon_ij`, using (1). This is consistent on a forest. Bipartition
the forest and give its nonorigin residue-zero classes A or B accordingly.
All common origin labels receive A. Internal and cross edges are proper:
nonzero/nonzero contacts have opposite signs, zero/zero contacts cross the
bipartition, and mixed contacts use disjoint palettes. The origin has no
residue-zero unit neighbour. If there is no zero/zero contact, one zero colour
suffices. This also handles isolated layers and edgeless active graphs.

Sections 2--5 exhaust all rotations, including transcendental ones with
insufficient contacts to enter a quadratic field. The graph contains a
triangle, so its chromatic number is at least three. If a zero/zero unit
edge exists, any hypothetical three-colouring restricts on each full lattice
to its unique residue colouring. Both zero endpoints must have the colour
of the shared origin, a contradiction. Together with the constructions
above this proves the asserted exact criterion and theorem.

The bound is sharp already on two lattices: take
`alpha=(5+i sqrt(11))/6` and the diamonds `{0,1,omega,1+omega}` and
`alpha {0,1,omega,1+omega}`. Their two outer zero-residue vertices are at
distance one; their union is the seven-vertex Moser spindle.

## 6. Scope, evidence and attribution

The earlier theorem covers two full lattices; the earlier
[three-P48 result](../hadwiger_nelson_three_triangular_patches/PROOF.md)
covers three equal 169-point patches with pairwise-irrational rotations.
The present theorem removes that patch bound and irrationality restriction,
and replaces the finite active-triangle census with the quadratic
compatibility lemma and the valuation-interval colouring. It preserves the
three-versus-four criterion for full lattices. For arbitrary finite subsets
the upper bound transfers, but the lower criterion requires suitable
triangle propagation and must not be asserted automatically.

The explicit larger-patch fixture in verify.py has an active contact triangle
over radicand 33 with zero/zero contacts. Thus the earlier observation that
every active P48 triangle is three-colourable over radicand 21 does not extend
unchanged to larger patches. This does not challenge that finite theorem.

Classical ingredients are Eisenstein residues, uniqueness of the triangular
lattice three-colouring, finite-field and local-field facts, and the Moser
spindle. The conjugation-fixed, trivial-residue-action case in Section 3
is the earlier [inertial-conjugation lemma](../hadwiger_nelson_inertial_field_barrier/README.md);
the F9 case and the conjugation-exchanged interval argument are separately
proved above. A related primary source is Akos Ducz,
[A note on geometric colorings of the Moser lattice](https://arxiv.org/html/2606.12325v1),
which treats a particular Moser additive lattice and multiplicative closure.
It does not supply the arbitrary-three-rotation theorem proved here.
Targeted literature and committed-graph checks on 2026-09-13 found no matching
all-three-lattice statement; this is not a priority claim.

This is an ordinary written proof, not an exhaustive computer-assisted
theorem. The exact finite controls test the residue graph, interval
colouring, valuation inequalities and algebraic fixtures. Their finite ranges
do not prove the infinite theorem. They use only Python integer and rational
arithmetic, no SAT verdict or floating-point distance predicate. There is no
proof-assistant formalization or independent-author review of the new proof.

The [Parts source](https://arxiv.org/abs/2010.12665) and
[Haugland's 2026 introduction](https://arxiv.org/html/2608.04542v1)
support the working record of 509 vertices. This theorem produces no new
five-chromatic graph, does not classify four or more arbitrary lattices,
and does not cover different lattice scales or translations with no common
point. Those distinctions matter for the record search.
