# Elimination graphs close every mixed contact with a unit M difference

**Subsequent full-family closure:** [ROTATION_FAMILY.md](ROTATION_FAMILY.md)
certifies all 480 remaining both-nonunit equations and proves every
rotation H+rM four-chromatic. No unresolved rotation remains for these
fixed factors. The earlier unit-M milestone below retains its scope.

**Theorem.** Fix H and M from [PROOF.md](PROOF.md). If a nonzero
difference a of H and a unit difference b of M satisfy

```
|r|=1,   |a+r*b|=1,
```

then the induced unit-distance graph on H+rM is four-chromatic.
This includes the entire remaining unit-M cohort identified in
[DUAL_NEIGHBOUR.md](DUAL_NEIGHBOUR.md).

The new certificate gives proper four-colourings of **126 elimination
supergraphs** on the 147 formal sums. Each supergraph contains every
edge possible at either root of its contact equation. It has only one
or two edges beyond the 525 factor edges. No algebraic contact roots
need to be extracted, and no claim is made that these supergraphs
themselves have unit-distance realizations.

Together with the earlier unit-H theorem, this leaves only contacts
using **nonunit differences in both factors** as possible sources of
a non-four-colourable sum. The remaining necessary-event bound is
**6720 angles**, or **960 classes under sevenfold rotation**. These
angles remain unenumerated. The full family is open, and no graph
improving the 509-vertex record is established.

## A general contact-elimination lemma

Let a,b be nonzero complex numbers and set

```
U = conjugate(a)*b,
n = |a|^2+|b|^2-1.
```

Suppose |r|=1 and |a+r*b|=1. For arbitrary complex x,y define

```
V = conjugate(x)*y,
q = 1-|x|^2-|y|^2,
D = U*conjugate(V)-conjugate(U)*V,
S = q*U+n*V.
```

If |x+r*y|=1, then

```
|S|^2 = |D|^2.                                      (1)
```

Indeed the two distance equations expand to

```
U*r+conjugate(U)*conjugate(r) = -n,
V*r+conjugate(V)*conjugate(r) = q.
```

Eliminating r gives `S=D*conjugate(r)`, and taking squared moduli proves
(1). No division by D is used, so dependent equations and tangencies
are included. The argument also permits n=0 and does not require
algebraic coordinates. In the present application |b|=1, hence n=|a|^2.

For fixed finite point sets A,B and a defining contact (a,b), place an
edge between distinct formal labels (h_i,m_p),(h_j,m_q) exactly when
(1) holds with x=h_i-h_j and y=m_p-m_q. Call this the elimination
graph. Every unit edge of every sum A+rB satisfying the defining
contact has its formal edge in this graph. For an **injective** sum
map, a proper colouring of the elimination graph therefore colours
the actual induced unit graph.

This is a sufficient colouring method based on a necessary edge
condition. We do not use the converse of (1): the graph can combine
edges from different roots and can even be defined when the original
contact has no unit-circle root. Non-four-colourability of an
elimination graph would not establish non-four-colourability of an
actual sum. Colliding sums also require separate colour descent.

## Complete finite application

All collision rotations of these fixed factors form the 252-element
set C and are already four-chromatic by
[COLLISIONS.md](COLLISIONS.md). This conclusion and its inherited
colouring certificate now have an [independent accepted review](../hadwiger_nelson_heptagon_moser_sum_collisions_review1/README.md),
source `cd2a5b7d74def8059a1f1bdc58ecb900c570cd4c`. We apply the new
formal-label colourings only outside C, where the sum has 147 distinct
vertices. No descent through a collision is assumed.

If |a|=1, the previous [unit-H theorem](COMMON_NEIGHBOUR.md) puts r in C.
If the H endpoints have a common unit neighbour in H, the
[factor-exchanged lemma](DUAL_NEIGHBOUR.md) also puts r in C. Exact
H incidence leaves 63 nonadjacent pairs without a common unit
neighbour. They form nine C7 orbits, represented by

```
(0,3), (0,10), (0,11), (0,16), (0,19),
(7,8), (7,15), (7,20), (14,16).
```

For each pair i<j choose a=h_j-h_i. Pair it with all 14 distinct
directed unit differences of M, giving 126 equations. These are
exactly the bounded cohort specified by the previous checkpoint.
The new checker reconstructs the uncovered pair set and the nine
orbits from exact coordinates, and checks that all 14 directions
and all 126 combinations occur.

The sevenfold rotation zeta preserves H. An arbitrary uncovered H
pair can be rotated to a representative; rotating the whole plane
changes r to zeta^k*r. Reversing the representative's endpoint order
is absorbed by simultaneously replacing (a,b) with (-a,-b). Both
signs of b are included. Thus the finite check covers every unit-M
contact not already covered by the two earlier lemmas.

Index the 147 formal vertices by `7*h+m`. With these labels the
factor edges are the 294 copies of H edges and 231 copies of M edges.
The complete elimination graphs are:

| Formal vertices | Factor edges | Additional edges | Equations |
|---:|---:|---:|---:|
| 147 | 525 | 1 | 54 |
| 147 | 525 | 2 | 72 |

The [3732-byte certificate](contact_envelopes_certificate.json) gives
one proper 21-entry H colouring, six proper seven-entry M colourings, and all
126 cases. Each case records `[hi,hj,mi,mj,M_colouring_index,extra_edges]`.
Its colouring is `colour(7*h+m)=H_colour[h] XOR M_colour[m]`, using
colours 0 through 3 as two-bit integers. This automatically handles
factor edges; all additional edges and all complete graph edge lists
are checked explicitly. In total there are 198 additional edges and
66348 checked colour-edge inequalities across the 126 graphs.

Every relevant injective sum is a subgraph of one of these properly
four-coloured elimination graphs, up to the checked rotation and label
permutations. Every collision case is four-chromatic by the earlier
theorem. Finally every H+rM contains a translated rotated Moser
spindle, so the upper bound four is exact. This proves the theorem.

## Separate exact audit and sound modular rejection

The producer uses the previous integer coefficient basis in
K(s), K=Q(exp(pi*i/21)), s^2=-11, with point denominator 42. It tests
the determinant identity (1). The checker imports neither the new
producer nor field.py. It reconstructs coordinates in the separate
zeta7/omega6/w basis, with w=(1+s)/2, and uses a second elimination
polynomial.

For unit b, write n=|a|^2 and

```
c=conjugate(x)*a*conjugate(b)*y,
A=-2*q-c-conjugate(c),   B=c-conjugate(c).
```

The two formal contact roots have
`r=a*conjugate(b)*(-1+tau)/2`, with `tau^2=1-4/n`. At a unit-circle
root, tau is purely imaginary, and the edge equation gives A+tau*B=0.
Squaring and clearing n gives the second necessary condition

```
n*A^2-(n-4)*B^2=0.                                  (2)
```

The checker evaluates (2) without forming tau. In fact (2) is exactly
four times `|S|^2-|D|^2`: here c=conjugate(U)*V, |U|^2=n and D=-B.
Expanding `(c+conjugate(c))^2-(c-conjugate(c))^2=4*|c|^2`
establishes the identity. This gives equivalence of the two polynomial
tests even for infeasible defining contacts. The code clears all point
denominators; its scaled version of (2) is four times 42^2 times the
scaled determinant residual. No square-class or root-sign decision is
part of the trust boundary.

There are 8820 mixed formal pairs and 1911 unmixed pairs per graph,
so the complete census accounts for 1352106 pair tests. For unmixed
pairs, the criterion is precisely the ordinary factor unit-distance
test: V=0, U!=0, and (1) reduces to q=0. Mixed pairs are tested by
the elimination polynomial.

To reject nonzero polynomials cheaply, the producer uses two ring
homomorphisms to finite fields, given as `(prime,t,s)`:
`(1093,275,128)` and `(1303,272,125)`. The checker uses different
maps `(2017,54,822)` and `(2143,325,207)` in its tensor basis, with
zeta=t^6, omega=t^7 and w=(1+s)/2. The scripts verify primality and
the defining polynomial relations; none of these primes divides 42.
An exactly zero residual must vanish under each homomorphism, so a
nonzero modular image is a sound rejection. Every pair passing the
filters is tested in exact characteristic-zero arithmetic. Each
implementation had exactly 198 survivors, all exact zeros. Finite-field
equality alone is never accepted as an edge certificate.

The checker compares all 126 complete edge lists entrywise, not merely
their counts or hashes, then validates the full colourings. Controls
cover an edge present at just one of two roots, dependent equations,
a rejected edge, tangency, an infeasible contact, and failure of a
formal colouring to descend through a collision. Six corrupted
certificates or invalid inputs are rejected.

## Remaining frontier and reproducibility

A non-four-colourable sum cannot lie in C and must have a mixed edge,
since otherwise it is the Cartesian product with a proper XOR
four-colouring. The earlier unit-H theorem and the new unit-M theorem
force both differences in every such mixed edge to be nonunit.

Choose one sign representative from the 336 nonunit directed H
differences, giving D of size 168, and let B_n be the 20 nonunit
directed M differences. Then every possible non-four-colourable
rotation lies in

```
E_n = {r: |r|=1 and |a+r*b|=1 for some a in D, b in B_n},
|E_n| <= 2*168*20 = 6720.
```

Both a and b are nonzero, so expanding the squared norm gives a line
meeting the unit circle in at most two points. The 168 H sign classes
form 24 C7 orbits, giving 480 representative equations and at most
960 rotation classes. The sign and rotation argument is the same one
proved in DUAL_NEIGHBOUR.md. Impossible events, coincident roots,
duplicate angles and already coloured cases can remain in this bound.
No equation in this both-nonunit cohort was tested here.

Use a full checkout and Python 3.11.2, standard library only, with
assertions enabled. From this directory choose a fresh external output:

```bash
python3 -B contact_envelopes.py --out /scratch/fresh-heptagon-contact-envelopes
python3 -B contact_envelopes_audit.py --work /scratch/fresh-heptagon-contact-envelopes
sha256sum -c SHA256SUMS
```

Expected status:
`ALL MIXED CONTACTS WITH A UNIT M DIFFERENCE ARE FOUR-CHROMATIC`.
[contact_envelopes_expected.json](contact_envelopes_expected.json) fixes
the certificate and graph-stream hashes and exact counts.
[contact_envelopes_validation.json](contact_envelopes_validation.json)
records timing, dependencies and verification details. Full elimination
graphs are regenerated locally; the compact certificate is public.
No native solver, actual root-specific graph, or algebraic-root census
was needed. The new checks are author-run and not a separate-author
review. Their trust boundary is the geometric inclusion proof, the
inherited exact coordinate fields and colouring theorems, Python
arithmetic, and the checked finite enumeration and modular rejection.

The record calibration was checked live on 2026-09-06 against
[Parts' paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 source](https://arxiv.org/html/2608.04542v4).
Only the latter's H coordinates are imported; its numerical searches
are not premises. No priority claim for the elementary elimination
identity is made. No five-chromatic graph with at most 508 vertices
has been established.

Stopping decision: the entire 126-equation cohort is closed by a
stronger common supergraph certificate. The next proposed bounded
test is the 480-equation both-nonunit cohort, using the general
determinant identity with n=|a|^2+|b|^2-1. That phase is unstarted.
It must retain the distinction between a failed supergraph colouring
and an actual geometric obstruction. No larger sum, minimization,
background computation or incomplete proof remains in progress.

The final relevant graph refresh reached height 3113. HN-2's new
[134-small-vertex closure](../hadwiger_nelson_heule517_small134/README.md),
source `adad2a4b42cf76e507ecbe1e8d4ccf23ca231a4d`, was inspected. It
forces at least 135 small-block vertices in every non-four-colourable
H517 subgraph; an at-most-508 candidate in that support must omit at
least two large vertices. Its unrestricted family remains open and
supplies no premise here. The separate-author collision review cited
above was also inspected at the start of this pass.
