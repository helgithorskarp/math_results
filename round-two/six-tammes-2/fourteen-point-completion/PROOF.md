# Two completions of fourteen incumbent points, and a smaller near-contact reduction

Actual author **six-tammes-2**, role **researcher**, 2026-10-01.
Status: exact computer-assisted conditional lemma, author checked;
independent review and formalization pending. No global bound changes.

The asymmetric and cyclic fifteen-point constructions, their equal separation
and their quintic are prior work. This contribution certifies every arbitrary
unit completion of a specified fourteen-point fragment, proves a linear
stability estimate for relaxed avoidance, and removes two contact hypotheses
from the earlier neighborhood reduction. It does not claim a new construction
or historical priority. Occurrence of the prescribed motif in an unrestricted
optimizer remains unproved.

Let tau be the bracketed root of

```
F(t)=13t^5-t^4+6t^3+2t^2-3t-1,
0.59260590292507377809642492233275 < tau <
0.59260590292507377809642492233276.
```

Use the labeled exact asymmetric incumbent p_0,...,p_14 of
[the prior local certificate](../../../tammes15_exact_local_certificate/README.md).
Its vectors are copied into certificate.json with their source hash.
The basis is (p_0,p_5,p_11), with Gram matrix H=(1-tau)I+tau J.
All coefficients below are relative to this basis, not orthonormal coordinates.
Fix the fourteen points with labels 0 through 13. Define c_14 by the coefficients

```
s1 = -9/4 -5*tau/2 +11*tau^2 -9*tau^3/2 +65*tau^4/4,
s2 = -5 +19*tau^2/2 -8*tau^3 +39*tau^4/2,
s3 = 41/4 +6*tau -37*tau^2 +27*tau^3 -221*tau^4/4.
```

**Exact completion.** A unit vector x satisfying x.p_i<=tau for all
0<=i<=13 is exactly p_14 or c_14. Both are admissible. Replacing p_14
by c_14 gives the known cyclic incumbent, not a third packing. The first
completion has exactly the three new contacts (0,14),(3,14),(6,14);
the second has (3,14),(4,14),(6,14).

**Relaxed completion.** If x is unit and x.p_i<=tau+delta for all these
fourteen labels, with 0<=delta<=1/1000, then

```
min(||x-p_14||,||x-c_14||) <= 1000 delta.
```

**Twenty-six near-contact reduction.** Let I=[14/25,593/1000]. Start
with the two anchor triangles (0,5,11),(1,2,4), and add the two contacts
new-a,new-b for each tuple below:

```
A: (6,0,11,5) (7,0,5,11) (9,5,11,0)
B: (3,1,4,2) (8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4).
```

Add (6,8),(7,12),(9,10),(9,13). This is a 26-edge graph on fourteen
labels; the fifteenth point has no prescribed contact. If fifteen distinct
unit vectors q_i have all pair dots<=t in I, and every one of those 26 dots
belongs to [t-e,t], with 0<=e<=10^-13, then

```
|t-tau| <= 30000e,
```

and, after an orthogonal transformation, their maximum labeled Euclidean
distance to one of the two configurations

```
(p_0,...,p_13,p_14),  (p_0,...,p_13,c_14)
```

is at most **2100000000e**. If additionally e<=10^-16 and t<tau, the
asymmetric neighborhood is excluded by the existing local-stress theorem:
only the cyclic neighborhood remains. If t<=tau and the asymmetric
neighborhood applies, necessarily t=tau and the packing is exactly that
incumbent up to O(3). No cyclic local-exclusion theorem is asserted here.
At e=0 the exact completion classification applies to either branch.

The edge count is smaller than the previous 28-edge neighborhood result,
but the present conclusion retains two branches and its metric constant is
larger. It is not a full 26-edge strict-improvement exclusion.

## 1. Complete exact polytope certificate

In basis coefficients let

```
P={v in R^3 : (H a_i).v <= tau, 0<=i<=13},
```

where a_i is the coefficient vector of p_i. It is a full-dimensional
polytope: zero satisfies every inequality strictly. The checker verifies
that a_0,a_1,a_2 are independent and that positive numbers w_0,w_1,w_2
satisfy

```
w_0 a_0 + w_1 a_1 + w_2 a_2 + a_5 = 0.
```

The weights are obtained by an exact three-by-three Cramer computation.
Multiplication by the invertible H preserves this positive dependence and
independence of three normals. Any recession direction has nonpositive dot
with all four normals; positive dependence makes all four dots zero, and
independence makes the direction zero. Thus P is bounded.

Every vertex has three independent active constraint normals. Enumerate
all C(14,3)=364 triples, with no symmetry reduction. For a triple let M be
its normal-row matrix, D=det(M), and U its homogeneous Cramer vector for
right-hand side (tau,tau,tau). If D=0, the triple does not define a unique
vertex. Otherwise its candidate is U/D. An exact violated inequality
discards an infeasible candidate. Every feasible candidate is checked against
all fourteen inequalities. The metric squared norm is U^T H U / D^2.
Division signs are handled using the separately certified sign of D.

All expressions are computed in Q[t]/(F). Zero remainder establishes an
identity at tau; strict signs are enclosed at the rational root bracket.
An unseparated sign aborts the computation. No floating-point sign or
incomplete enumeration is used.

The complete enumeration has **24 distinct feasible vertices**:

| Vertex type | Count | Certified squared norm |
|---|---:|---:|
| Short vertices | 22 | strictly below 3/4 |
| Triple (0,3,6) | 1 | exactly 1; vector p_14 |
| Triple (3,4,6) | 1 | exactly 1; vector c_14 |

Their squared separation is strictly above 1/25. Every vertex of P is
therefore in the closed unit ball. Since P is the convex hull of these
vertices, the strict convexity of the ball implies that P intersects the
unit sphere only at the two unit vertices. This proves the exact completion
statement, including arbitrary positions of the last point.

For identification of the second packing, reconstruct the previously
published cyclic incumbent from the same anchor triples and its reflection
tuples. The new complete Gram matrix equals its Gram matrix under the
following map from new labels 0,...,14 to the prior cyclic labels:

```
1,0,11,7,5,4,10,3,9,8,6,2,14,13,12.
```

The checker verifies every entry, not just contact-graph isomorphism.
The spanning anchors then identify the realizations by O(3).

## 2. Linear stability from the two exposed unit vertices

Let x be a relaxed admissible unit vector and set

```
y=x/(1+delta/tau),  E=1-||y||^2.
```

All exact avoidance inequalities hold for y, so y is in P. Since tau>1/2,

```
0 <= E <= 2delta/tau <= 4delta,
||x-y|| <= 2delta.
```

Write y as a convex combination of P's vertices. Let alpha,beta be the
masses on p_14,c_14 and let L be the total mass on the short vertices.
The exact identity

```
1-||sum_j lambda_j v_j||^2
 = sum_j lambda_j(1-||v_j||^2)
   + sum_{j<k} lambda_j lambda_k ||v_j-v_k||^2
```

gives L<=4E and alpha beta<=25E. Also L<=16delta<=1/2, hence
max(alpha,beta)>=(1-L)/2>=1/4. Therefore min(alpha,beta)<=100E.
Choose the unit vertex with larger mass. Every other vertex is in the
unit ball and is at distance at most two from it, so

```
distance(y, chosen unit vertex) <= 2(L+min(alpha,beta)) <= 208E.
distance(x, chosen unit vertex) <= (208*4+2)delta < 1000delta.
```

This proves a linear estimate, including delta=0. A square-root estimate
would lose the separation between the two isolated unit vertices.

## 3. Removing the last point's two contact assumptions

The proof of [the previous incumbent-neighborhood lemma](../robust-incumbent-pattern/PROOF.md)
has a fourteen-point subargument that uses only the present 26 edges.
We spell out the dependency restriction; the conclusion does not follow
merely by dropping two assumptions from its final theorem.

In Sections 1--4 of that proof, align the two approximate anchor triangles
and reflect only the tuples listed above. Omitting tuple (14,0,6,11)
removes the comparison error for label14. Every other error remains below
80e. The four cross constraints, the branch-separation packing inequality
for labels9,2, the two-orientation linear system, and both augmented
determinants involve only the thirteen-point core. The same exact bounds give

```
||V_A-V_*||<=1000e, ||U-U_t||<=40000e,
||W-W_t||<64000e, |D_sigma|<=120000e,
D_minus>=1/10, D_plus=JF, J<=-2/5, F'>=10.
```

Thus the wrong orientation is excluded and |t-tau|<=30000e.
Section5's reflection inverse and parameter-path estimates apply to
all fourteen present labels, including label3 from its unchanged B tuple.
They give, after O(3) identification,

```
max_{i<=13} ||q_i-p_i|| <= 2000000e.
```

The separately verified old rational-function manifest covers all these
identities and quantitative bounds. The written approximate-geometric
argument and its restriction to these fourteen labels are unformalized
proof obligations; the replay is an arithmetic check of that argument.

For the arbitrary fifteenth unit point, packing implies

```
q_14.p_i <= q_14.q_i + ||q_i-p_i||
          <= tau + (30000+2000000)e.
```

Use Section2 with delta=2030000e<=1/1000. It gives distance to one
of the two completions at most 2030000000e, below the claimed
2100000000e whole-configuration bound.

For the asymmetric branch and e<=10^-16, the previous two-rotation gauge
estimate multiplies the whole-configuration distance by at most ten:

```
10*2100000000e <= 21/10000000 < 1/400000.
```

The pinned asymmetric local-stress theorem applies. It forces the actual
largest pair dot to be at least tau, with equality only at that incumbent.
Since this dot is at most t, it gives the stated asymmetric-branch exclusion
and equality case. A cyclic local certificate is a concrete next dependency,
not an assumed result. For a strictly improving fifteen-point packing, the
published N14 optimum bounds its cosine above14/25; its cosine is below
tau<593/1000, so the interval I covers that consequence.

## 4. Reproduction and limits

[check.py](check.py) uses exact five-coefficient arithmetic, full active-plane
enumeration and exact Gram identification. [audit.py](audit.py) imports none
of that arithmetic. It uses unreduced ordinary-polynomial row-cross-product
Cramer formulas, homogeneous vertex comparisons and exact centered Taylor
sign enclosures at the root. It separately checks the full enumeration,
unit fixtures, norm/separation gaps and scalar bridges. It does not rederive
the old proximity proof or the old local stress. Neither checker formalizes
the convex-hull argument, the geometric perturbation estimates, or published
prerequisite proofs. Independent mathematical review remains pending.

Source inputs and old-source hashes are in certificate.json. The optional
full replay checks five pinned files of the previous neighborhood package,
which in turn checks eight pinned files from the old core/local packages.
The compact certificate is construction data, not a large enumeration dump.

Primary context: [Cohn's maintained table](https://cohn.mit.edu/spherical-codes/)
and [coordinate dataset](https://spherical-codes.org/data/3/15) retain the
unstarred N15 quintic entry. The two incumbent constructions are described
by Kottwitz, *The densest packing of equal circles on a sphere*,
[DOI10.1107/S0108767390011370](https://doi.org/10.1107/S0108767390011370),
and Buddenhagen--Kottwitz, *Multiplicity and symmetry breaking in
(conjectured) densest packings of congruent circles on a sphere*.
The latter's searched abstract confirms the two varieties; its full PDF
was not newly retrievable this pass. [Musin--Tarasov](https://arxiv.org/abs/1410.2536)
prove N14, supplying the interval comparison, not N15 global optimality.
No priority assertion follows from this bounded literature search.
