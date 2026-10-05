# Internal check of Rowan's full uniform upper component, version 1

Checker: Iris, studio-researcher-2, researcher. Date: 2026-10-05, workday5.
Author: Rowan, studio-researcher-4. Canonical author task23.

## Verdict and frozen inputs

ACCEPT Sections1--5 of the exact expanded analytic component at its stated
classification and universal parent-budget imports. Its abstract
integer-parameter lemma is unconditional under its displayed hypotheses.
The tree implication gives

    log2 N(T)<=5n^2/36+6n for n>=2,

conditional on those two separately supplied universal inputs. The
recurrence/potential identity, height conversion, boundary handling and
global-maximum implication are correct at that scope.

Exact PROOF.md:12744bytes, SHA256
89cb5a4a3fef9e32c48a6de6b605cb4ecabdf3cd803493d979a7519142b3e8bc.
Exact README.md:1344bytes, SHA256
a41f12c40840229e1db057b8de652e5b1a6ec5c075548c94a7e1a5a52538072e.
The author's UPPER_HANDOFF_v1.json SHA256 is
c67749eff38e2da063518743a9e13b18a165e96be947c3ad15972f8d26a9d590.
All were copied without changes and their hashes/sizes checked against
the actual handoff. INPUTS.json identifies source/copy paths and scope.

This is another researcher's internal mathematical check, not external
review or formal verification. It does not accept the exhaustiveness of
the inherited classification, the universal structural proof, the lower
component, final assembly or historical priority. Those retain their
separate authors/checkers. The old Iris231 report remains about input
f39ad2a7... only; this is a new check of the changed full version.

## 1. Independent parameter reconstruction

For one parameter triple write h=ell, k=d-1 and Z=X+k. The hypotheses
are n>=3; integer h>=0,1<=d<=n,X>=1; X<=2(n-1)2^h; and

    5(n-1-h)>=9d-4d2^-h.

Multiplying by h and subtracting9h gives

    9hk<=5h(n-1-h)+4hd2^-h-9h.

For integer h>=0, h2^-h<=1/2: h=0 is separate, h=1,2 attain1/2,
and subsequent successive ratios (h+1)/(2h) are below one. Completing
the square bounds h(n-1-h) by (n-1)^2/4. Dropping -9h and using d<=n
therefore gives

    hk<=5(n-1)^2/36+2n/9<=5n^2/36+2n/9.                    (R1)

This independently checks the uniform correction. No large-height
cutoff, approximation of2^-h, or d>=2 assumption was made. Multiplying
the budget by h is valid also at h=0, where it contributes zero.

For k>=1, I reconstructed the binomial estimate through a generating
coefficient rather than merely repeating the author's factorial route.
For t=k/Z>0, positivity of the coefficients of (1+t)^Z gives

    binom(Z,k)t^k<=(1+t)^Z<=exp(Zt)=exp(k),
    binom(Z,k)<=(eZ/k)^k.

Here Z>=k is an integer, so the coefficient expression is legitimate.
The potential bound and2^h>=1 imply

    Z<=2(n-1)2^h+k<=3n2^h.

Thus

    log2 binom(Z,k)<=hk+k log2(3en/k).                     (R2)

As a function of real k in(0,n], k ln(3en/k) has derivative
ln(3n/k)>0; its endpoint at n is n ln(3e). Hence the residual is at
most n log2(3e)<4n. The last strict bound is exact: the factorial
series/geometric comparison gives e<3, and3e<9<16. No floating-point
numerical assertion is involved. For k=0 the original summand is one
and no logarithm containing division by k is taken.

Combining (R1)--(R2), each term is at most
2^(5n^2/36+38n/9). There are at most n terms and the set is nonempty,
so its sum is positive and

    log2 B<=5n^2/36+38n/9+log2 n
          <=5n^2/36+47n/9
          <=5n^2/36+6n.                                   (R3)

This reconstructs the whole abstract lemma under exactly its stated
hypotheses. The author's factorial proof also checks directly:
ln(k!)>=integral_1^k ln(t)dt=k ln k-k+1, including k=1;
binom(Z,k)<=Z^k/k! then gives the same (R2). The source retains the
factorial contribution responsible for the linear entropy remainder.

## 2. Deficit, potential and maximizing-set interface

Induction on the u-side branch after deleting uv gives

    a_{u->v}=1+sum_{w in branch, deg_T(w)>1}
                        deg_T(w)2^dist(v,w).

At a nonleaf u with k children, its full degree is k+1. The recursion's
constant is3+2k=1+2deg_T(u), and each descendant term gains exactly
one distance exponent when moving the boundary from u to v. A terminal
branch has no nonleaf term and deficit1. This verifies source equation12.

For a graph-leaf parent p and sibling z, the p-side branch contains
every nonleaf; dist(z,w)=dist(p,w)+1. Consequently

    (a_{p->z}-1)/2=sum_{w nonleaf}deg_T(w)2^dist(p,w)=X_p.

This matches my separately derived recurrence identity and verifies
Rowan's equations11--13. The degree sum is the full-tree2(n-1), not
the core degree sum. The recurrence alone already establishes the
independence of the chosen sibling z.

The leaf estimator E(z)=1+|L|+2X_p matches the exact imported convention.
Once the classification/threshold input is supplied, P* consists of all
maximizing leaf parents, is nonempty, and has cardinality at most n.
Every parent is a nonleaf for n>=3, so X_p is a positive integer;
1<=d_p<=n and the degree bound supplies every hypothesis of the abstract
lemma. Restricting the sum to P* is essential. All tied parents remain
included; no uniqueness assertion is used.

This check of Rowan's identity is not the required independent check of
my separately authored classification audit. Atlas retains that check.
In particular, I have not used my unreviewed classification artifact to
declare the two imports discharged inside this analytic verdict.

## 3. Core versus full eccentricity and budget conversion

The nonleaf core is nonempty and connected for n>=3: an internal vertex
of the path between two nonleaves has degree at least two. For a parent
p in the core, put h=max_{u in core}dist(p,u). Every graph leaf is one
edge from a core vertex, so full eccentricity H<=h+1.

In a nonstar tree the core is nontrivial and a farthest core vertex q
from p is a core endpoint different from p. It has full degree at least
two but only one core neighbor, hence a graph-leaf neighbor. This leaf
is at distance h+1, proving H=h+1. On a star, p is the center and the
same identity is H=1,h=0. No core-endpoint theorem about maximizing
parents is needed for this purely geometric conversion.

Replacing H by h+1 in the stronger nonstar input gives

    4(d-1)(1-2^-h)<=5(n-d-h-2),
    5n>=5h+9d+6-4d2^-h+4*2^-h,
    n>=h+6/5+9d/5-4d2^-h/5+4*2^-h/5.

Subtracting the required weaker right side h+1+9d/5-4d2^-h/5 leaves
1/5+(4/5)2^-h>0. This confirms all signs and the exact constant in
equations16--18. It is an implication between statements, not a new
proof of the stronger input. Its nonstar restriction is retained.

## 4. Boundaries and final quantifiers

On a star with d=n-1>=2, h=0 and X=d. The weaker budget is n>=1+d,
an equality. Its exact count is binom(2d-1,d-1)=binom(2n-3,n-2), so
the parameter lemma applies directly. The stronger nonstar input is
not applied to the star; its right side would be negative in that case.

At d=1, k=0 and a term equals one. Tied classes add normally; the at
most n count is deliberately coarse. No automorphism orbit quotient
is introduced by stars-and-bars or by taking the maximum over tree types.

For K2, mass2 has exactly(2,0),(1,1),(0,2). Only(1,1) is not already
stacked, and it admits no legal move. At mass3, a supported singleton
is already stacked and either mixed pair(2,1)/(1,2) stacks by one move.
Thus the least permitted threshold is3 and N=1, confirming the
n=2 upper directly without an empty-core convention.

The tree application for n>=3 consumes precisely the separately
supplied classification and universal weaker parent budget. The
unconditional parameter lemma does not assert these for trees. Relabeling
a tree bijects individual configurations and legal move sequences, so
N is isomorphism invariant; there are finitely many tree types at fixed
order. Maximizing the uniform upper over those types is valid, giving
the same explicit C_plus=6 for every n>=2 if the imports hold universally.

## 5. Honest checking and publication scope

I found no defect requiring a source revision in this exact component.
Its new integer lemma, potential derivation, geometric conversion and
boundaries have all been inspected, rather than inferring a new verdict
from the old conditional check. The coefficient argument above gives
a distinct derivation of the binomial bound. No computation, old census,
author module or solver was executed; no new numerical evidence is claimed.

Inherited source URLs/commits match the byte-verified versions from my
separate source audit. Historical priority, classification exhaustiveness,
universal structural proof, all-order lower and full assembled theorem
remain outside this report. The final package must cite their actual
other-researcher internal checks and precise versions. This acceptance
cannot self-certify any author's separate component or imply that a vote,
source manifest or publication establishes correctness.
