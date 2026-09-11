# Exhaustive structure at 73 points

This is the historical reduction established in the first mathematical pass.
The subsequent [upper-bound proof](upper_bound72.md) closes every branch and
proves r_5(F_5^3)<=72. References below to unresolved cases describe the
earlier checkpoint; the reduction and its source remain valid.

Let S be a line-free 73-subset of AG(3,5). Write a_j for the number of affine
planes meeting S in j points. There are 31 parallel classes, each comprising
five planes, and 155 affine planes in total.

## 1. Planar bounds and incidence identities

Every plane section has at most 16 points. This is the familiar planar bound;
`plane_caps.cpp` independently verifies it by excluding every 17-subset with
at most four points on each of the 30 affine lines. Taking a subset reduces
any larger counterexample to size 17. Since each parallel class sums to 73,
every section has at least 73-4*16=9 points.

Every pair of distinct affine points belongs to six planes. Hence the sum of
the pair weights of the 31 parallel classes is

\[
\sum_H\binom{|S\cap H|}{2}=6\binom{73}{2}=15768.\tag{1}
\]

For any projective line L in the projective completion PG(3,5), the six planes
through L count each point off L once and each point on L six times. Thus

\[
\sum_{H\supset L}|S\cap H|=73+5|S\cap L|.\tag{2}
\]

The plane at infinity is empty. A 12-point affine plane section would contain
a line with at least four points: the same exhaustive program checks that no
12-subset of AG(2,5) has all line sizes at most three. If that line lies in a
12-plane, (2) gives 93 <= 12+5*16=92, a contradiction. Consequently a_12=0.
This exclusion is needed only for the dual reduction in Section 4; Sections
2 and 3 deliberately allow all thirteen integer profiles.

## 2. Many large plane sections

Call a parallel class type A if its unordered profile is (9,16,16,16,16),
and type B if its profile is (10,15,16,16,16). Put a=#A and b=#B. Their pair
weights are 516 and 510. Among all other sorted integer five-tuples in [9,16]
with sum 73, the maximum pair weight is 506. The complete thirteen-row
table appears in `expected_reduction.json` and is independently generated.
Equation (1) therefore yields

\[
15768\le506(31-a-b)+516a+510b,
\qquad 5a+2b\ge41.\tag{3}
\]

In particular a+b>=9. Notice also that a=a_9 and b=a_10: a class containing
9 must be A and a class containing 10 must be B.

There are at least 74 size-16 affine planes. To see this, let t be their number
in a single parallel class. Here 0<=t<=4. Moving mass from a smaller entry to
a larger one increases the sum of binomial coefficients. Subject to exactly
t entries equal to 16, the maximum is attained at the profile consisting of
one entry 13-t, then 4-t entries 15, and t entries 16. Thus its pair weight is

\[
\binom{13-t}{2}+(4-t)\binom{15}{2}+t\binom{16}{2}
=498+\frac{5t+t^2}{2}\le498+\frac92t.
\]

Summing gives 15768<=31*498+(9/2)*a_16, so a_16>=74.
The complete profile check also verifies this bound without relying on the
mass-transfer description.

## 3. Four global coordinate cases

Parallel-plane directions are projective normal vectors in the dual PG(2,5).
A two-dimensional vector subspace has only six projective directions. The
at least nine A/B directions therefore include three linearly independent
normals. Use their linear forms as affine coordinates.

For type B, the unique size-10 layer and the unique size-15 layer can be sent
to coordinate values 3 and 4 by an invertible affine map of F_5. The other
layers, at values 0,1,2, have size 16. For type A, send the size-9 layer to
3 and any other layer to 4. Coordinate translations and independent nonzero
scalings preserve independence and preserve affine lines.

Finally permute axes so that type A coordinates precede type B coordinates.
Every S is therefore affinely equivalent to one of exactly four specified
**cases**, indexed by h=0,1,2,3: the first h coordinate directions have
ordered layer sizes (16,16,16,9,16), and the remaining directions have
(16,16,16,10,15). The cases may overlap under affine equivalence; disjointness
is unnecessary for exhaustive coverage. `generate.py` encodes these cases
with all point, line and plane constraints. No plane shape is fixed.

## 4. A small strong (3 mod 5) dual

Embed S into PG(3,5) with empty plane H_infinity. Regard a primal plane H as
a point of the dual projective space, and define the nonnegative residue

\[
K(H)=(16-|S\cap H|)\bmod5.
\]

The possible plane sizes are 0 at infinity and 9,10,11,13,14,15,16 elsewhere.
Thus K takes values 0,1,2,3 only, and K(H_infinity)=1. Equation (2) implies
that the sum of K on every dual line is congruent to
96-73=3 modulo 5. By definition, K is a strong (3 mod 5)-arc in PG(3,5).

Put L=a_9+a_10+a_11. Each point of PG(3,5) is on 31 planes. Summing the
unreduced deficits gives 156*16-31*73=233. Reduction modulo 5 subtracts 15
at infinity and 5 for each of the L small affine planes. Therefore

\[
|K|=218-5L\le173,\tag{4}
\]

because L>=a+b>=9. This is an exact formula, not a relaxation.
There is a useful pointed constraint too: every dual line through the
1-point H_infinity has total K-multiplicity 3 or 8. Indeed it is a parallel
class plus H_infinity, with unreduced total 6*16-73=23; the 15 at infinity
and possibly one further 5 are subtracted. There can be at most one plane
of size <=11 in a parallel class.

We now invoke Kurz–Landjev–Rousseva, Theorems 5.2 and 5.3, in the version
specified in the README. A strong (3 mod 5)-arc without a full plane in its
support, and which is not lifted, is projectively equivalent to precisely
one of their three exceptional arcs, of sizes 128,143,168. The two latter
arcs have no points of multiplicity 2.

For a dual with no multiplicity-2 points, a_9=a_14=0. Equation (3) then forces
b=a_10>=21, so (4) forces |K|<=218-5*21=113. This excludes both exceptional
sizes 143 and 168. It is a reusable exclusion for any proposed dual with
no multiplicity-2 points, not just these two examples.

## 5. The complete three-branch cover

We obtain the following exhaustive alternatives, allowing overlap:

**F. A direction with sparse parallel lines.** If the support of K contains
a full dual plane, let P be the corresponding primal point. Every primal
plane through P has size at most 15, since size 16 gives K=0. By (2), every
projective line through P contains at most three points of S.
If P were an affine point in S, the 31 affine lines through P would give
|S|<=1+31*(3-1)=63. If P were affine but outside S, adjoining P would give
a line-free 74-set, contradicting the published upper bound 73. Thus P is
at infinity. The 25 affine lines of its direction each meet S in at most
three points, and their sizes sum to 73. Their deficits from three sum to
two: exactly one line has size 1 or exactly two lines have size 2, with all
others of size 3. This proves the stated two-profile cover of branch F.
One can normalize the direction to the z-axis. The exceptional fibers can
be placed over (0,0), or over (0,0) and (1,0), by an affine change in the
quotient plane; both are global normalizations within this branch.

**L. A lifted dual.** If K is lifted, the definition gives |K|=5|K_0|+3 for
a strong planar (3 mod 5)-arc K_0. Every line of the base has weight at least
3. Its 31 lines count each point six times, giving |K_0|>=16. Also
|K_0| is congruent to 3 modulo 5: summing the six lines through a point
gives |K_0|+5K_0(P) congruent to 18. From (4), |K_0|<=34. Hence the only
base sizes are 18,23,28,33. No base type is presumed absent.

**E. The exceptional dual of size 128.** If neither previous condition holds,
the cited complete classification and Section 4 leave only the unique
exceptional arc of size 128. Here L=18. Its point-multiplicity counts are
(80,40,20,16) for multiplicities (0,1,2,3), respectively. These translate to
a_16+a_11=80, a_15+a_10=39, a_14+a_9=20, and a_13=16; the subtraction of
one in the second equation accounts for the empty plane at infinity.

Every 73-set satisfies this cover as well as the independent four-case
coordinate cover. Branch F and branch L remain open, as does reconstruction
from the exceptional 128 dual. Their unresolved status prevents any claim
that r_5(F_5^3)<=72. The downstream purpose is to replace arbitrary fixed
seeds with a globally exhaustive, structurally constrained reconstruction
problem in the next mathematical pass.
