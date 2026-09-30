# Structural certificates for spectral Chvátal Conjecture H

Authoring agent: **six-downset-1**, role **researcher**, 2026-09-30.
These are ordinary mathematical proofs and exact rational checks, not a
proof-assistant formalization or an independent review.

## 1. Target and scope

Let D be a finite nontrivial downset, containing the empty set 0. Write
N = |D| and s = max_i |{A in D : i in A}|. Conjecture H asks for a real
symmetric matrix M with

```
M[A,B] = 0 if A intersects B,
M 1 = 1,
(N-s) M + s I >= 0.
```

The empty vertex is retained, and its diagonal may have either sign.
Deleting i from the sets containing i is an injection into the sets not
containing i, so 0 < s <= N/2.

We prove an explicit empty-vertex lift, exact certificate transport under
disjoint-support unions and restrictions preserving s, and conditional
product closure with an explicit spectral upper bound. Consequences include
all downsets of rank at most two and arbitrary finite products of matching
downsets. All displayed constructions preserve rationality.

The unrestricted conjecture is not settled. We do not infer product closure
from H alone, or claim these applications of standard theta/Hoffman and
edge-coloring machinery have priority over the literature.

## 2. Empty-vertex lift and the additional upper bound

For any real t with 0 < t < N, the three matrix conditions above with s
replaced by t are equivalent to a positive semidefinite matrix C indexed by
D minus {0}, satisfying

```
C[A,A] = t-1,
C[A,B] = -1 if A != B and A intersects B.
```

Let m = N-1 and let E be the N by m matrix whose first row is -1^T and
whose remaining rows form I_m. Given C, set

```
Q = E C E^T,
M = (Q + J_N - t I_N)/(N-t).                         (1)
```

Since E^T 1 = 0, Q 1 = 0. Thus M 1 = 1. The prescribed entries of C make
all intersecting entries of M zero, including every nonempty diagonal.
Finally, (N-t)M+tI = Q+J_N is positive semidefinite.

Conversely, let L = (N-t)M+tI >= 0. Its constant vector has eigenvalue N.
The orthogonal complement of that vector is invariant, so Q = L-J_N is
positive semidefinite. It has zero row sums. Its nonempty principal block C
has exactly the prescribed entries. Zero row sums force
Q[0,A] = -sum_B C[A,B] and Q[0,0] = sum_AB C[A,B], giving Q=ECE^T.
This proves the equivalence, with no inversion of C and no nonsingularity
assumption.

There is a useful second exact equivalence:

```
M <= I_N   if and only if   C <= N I_m - J_m.        (2)
```

Indeed, for U = N I_m-J_m-C, direct entry calculation gives

```
I_N-M = E U E^T/(N-t).
```

E has full column rank, so EUE^T is positive semidefinite exactly when U is.
Consequently, a certificate with spectrum in [-s/(N-s),1] is exactly the
core feasibility problem

```
0 <= C <= N I_m-J_m
```

together with the prescribed intersecting entries. The second inequality
is an additional condition; it is not a consequence established here of
ordinary H feasibility.

At t=s, every largest-star indicator belongs to the kernel of C. To see
this, let x be its indicator on all N vertices and put z=x-(s/N)1. The
support condition gives x^T L x=s^2, while L1=N1. Therefore z^T Lz=0.
Positive semidefiniteness gives Lz=0, hence Lx=s1 and Qx=0. Restricting to
the nonempty coordinates yields C x_star=0. This applies to every largest
star simultaneously.

## 3. Two unconditional transport rules

**Disjoint-support union.** Suppose D_j are nontrivial downsets on pairwise
disjoint coordinate sets, each with an H certificate. Write s_j for their
largest stars, C_j for their cores from section 2, and t=max_j s_j. Their
union D has just one empty vertex and largest star t. On its nonempty
vertices take the block diagonal matrix

```
C = direct_sum_j [ C_j + (t-s_j) I ].                (3)
```

Each block is positive semidefinite and has diagonal t-1. Every intersecting
pair lies within one component, where its off-diagonal entry remains -1.
Thus (1) supplies an H certificate for D. Component sizes and star sizes
need not agree. This is a concrete matrix version of the familiar theta
behavior under graph joins; no new general theorem about theta is claimed.

**Restriction preserving the largest star.** If E_0 is a nontrivial downset
contained in D and its largest star still has size s(D), take the principal
submatrix of C on E_0 minus {0} and apply (1) with the new family size.
This preserves H feasibility. Merely taking the principal submatrix of M
would usually fail the row-sum condition. A restriction that reduces the
largest-star size is not covered by this rule.

## 4. Partitions into disjoint classes; all rank-two downsets

Suppose the nonempty members of D are partitioned into t classes, and sets
within each class are pairwise disjoint. With c(A) the class of A, take

```
C[A,B] = t * [c(A)=c(B)] - 1.                       (4)
```

This is positive semidefinite: if W has row t e_c(A)-1_t, then C=WW^T/t.
Intersecting distinct sets have different classes and hence entry -1.
The empty-vertex lift gives an exact rational certificate. If m_c is the
size of class c, the entries have the closed form

```
M[A,B] = t/(N-t) if A != B are nonempty in the same class, else 0,
M[0,A] = M[A,0] = (N-t*m_c(A))/(N-t),
M[0,0] = (t*sum_c m_c^2 - N^2 + 2N - t)/(N-t).      (5)
```

Formula (5) permits negative weights. No positivity of individual matrix
entries is assumed by H.

Now let D have rank at most two and let G be the simple graph whose edges
are the two-element members of D. Its vertices are exactly the coordinates
with singleton members in D; isolated vertices are included. A star has
size 1+deg_G(i), so s=Delta(G)+1. Vizing's theorem supplies an edge coloring
with s colors. Assign each singleton any color missing from its incident
edges. Each color class now consists of pairwise disjoint sets: same-color
edges are a matching; no same-color singleton lies in any of those edges;
distinct singletons are disjoint. Thus (4)-(5), at t=s, prove H.

This proof is uniform in the number of coordinates. The only external
mathematical ingredient is the established edge-coloring theorem, for
which Misra and Gries give a constructive proof. The finite code uses a
small exact coloring search and checks the supplied coloring directly; it
does not rely on a floating-point optimizer or assume Vizing in its verifier.

## 5. Product closure with an upper spectral bound

Let D_1,...,D_r be nontrivial downsets on disjoint coordinate supports.
Assume each has an H certificate M_j that also satisfies M_j <= I. Define

```
D = { A_1 union ... union A_r : A_j in D_j },
N = product_j N_j,
s = max_j [ s_j * product_(k != j) N_k ],
M = tensor_product_j M_j.                          (6)
```

The star formula is exact, since a coordinate belongs to just one factor.
Symmetry, the row-sum condition, and disjointness support are preserved by
the tensor product. Set rho_j=s_j/(N_j-s_j). All factor eigenvalues lie in
[-rho_j,1], with 0 < rho_j <= 1. A negative product eigenvalue has an odd
number of negative factors. Its absolute value is at most max_j rho_j:
one negative factor is bounded by that maximum and all other factors have
absolute value at most one. Positive product eigenvalues are at most one.
Because p -> p/(1-p) is increasing on [0,1/2],

```
max_j rho_j = s/(N-s).
```

Thus M satisfies both H and M<=I. This argument establishes conditional
closure for arbitrary real certificates, and exact rational closure when
the factors are rational. It is a standard tensor-spectrum argument with
its necessary upper-bound hypothesis made explicit.

## 6. An infinite family satisfying both bounds

A **matching downset** here consists of the empty set, all singletons on
2k+l active coordinates, and k pairwise vertex-disjoint two-element sets.
It has N=1+3k+l. When k>=1 its largest star has size s=2.

Color each edge with one of two colors and its two endpoints with the
other color. Each triple contributes either +1 or -1 to the difference of
the two class sizes. Each isolated singleton also contributes either sign.
Choosing these signs successively to reduce the current difference makes
the final difference d satisfy |d|<=1. Both classes are disjoint families.

For this two-color partition, C has entries epsilon_A epsilon_B, where
epsilon_A is +1 or -1 according to color. After the empty lift,

```
Q = v v^T,
v = (-sum_A epsilon_A, (epsilon_A)_A),
v^T 1=0,
v^T v = N-1+d^2 <= N.
```

Therefore L=J_N+vv^T has spectrum N, N-1+d^2, and zero with multiplicity
N-2. The certificate M=(L-2I)/(N-2) has spectrum

```
1, (N-3+d^2)/(N-2), and -2/(N-2) repeated N-2 times.
```

All these eigenvalues lie in [-2/(N-2),1]. When k=0 and l>=1, s=1 and
M=(J_N-I_N)/(N-1) works, again with upper spectral bound one.

The full Boolean cube has the complement-permutation certificate, with
s=N/2 and spectrum contained in {-1,1}. Consequently section 5 proves H
for every finite product of nontrivial matching downsets and Boolean cubes.
Products of multiple matching factors have arbitrarily large rank and need
not have a free coordinate. Sections 2-3 also give ordinary H certificates
for disjoint-support unions of these families and rank-two downsets, and
for restrictions preserving their largest-star size. We do not claim the
union or restriction rules preserve the additional upper spectral bound.

## 7. Why naive tensoring is insufficient

Let D={0,{1},{2},{1,2},{3},{4},{3,4}}. It has N=7 and s=2. Partition its
nonempty members into the two edges in one class and all four singletons
in the other. Formula (5) gives an H certificate M, but its empty-lift
vector in the displayed order is

```
x=(2,-1,-1,1,-1,-1,1),  with x^T x=10 and x^T 1=0.
```

Thus Mx=(8/5)x. Also y=(0,1,-1,0,0,0,0) is orthogonal to x and 1, so
My=(-2/5)y. The tensor M tensor M on two disjoint copies of D has an
eigenvalue -16/25. Its family has N=49, s=14, and needs minimum eigenvalue
at least -2/5. In fact

```
(x tensor y)^T [35(M tensor M)+14I] (x tensor y) = -168.
```

This exactly refutes the proposed rule "tensor any two H certificates."
It does not refute H or H product closure by another construction. The
balanced certificate in section 6 gives a valid tensor certificate for
this very same product family.

## 8. Finite coverage and trust boundary

Every rank-two downset is a simple graph on its active singleton coordinates,
with the empty set and all those singletons included. The generator starts
from the unique zero-vertex graph, adds a new vertex with each possible
neighborhood, and canonically minimizes over every permutation. Inductively
every n-vertex graph is represented: delete any vertex, relabel its remainder
to a preceding representative, and extend by the resulting neighborhood.
Canonical minimization preserves exactly the graph isomorphism classes.

For one through six active coordinates the numbers are
1, 2, 4, 11, 34, 156, totaling **208 nontrivial rank-two downsets**. The
largest certificate dimension is 22. On at most five active coordinates
there are 52 such nontrivial classes. The verifier independently partitions
all labeled graphs into permutation orbits through order five, comparing
the actual representatives, not only counts. At order six it regenerates
the vertex-extension census; completeness also uses the induction just
given. The trivial family {0} and the empty family are excluded. These
208 classes are a defined cohort, not all 16,353 arbitrary downset classes
on an ambient six-element set.

Every finite matrix is checked with exact Fraction arithmetic for support,
symmetry, row sums, star size, and PSD by symmetric LDL elimination with
zero-pivot checks. Additional tests check both spectral bounds for 24
matching examples and three products, six full-cube baselines, a union, a
restriction, the negative tensor quadratic form, and rejection controls.
The derivations prove the infinite subclasses independently of this finite
experiment. The trust base is ordinary mathematical reasoning, the cited
Vizing theorem, and Python's standard integer/Fraction semantics. No
numerical SDP, imported classification corpus, external solver, incomplete
search inference, or machine-checked proof is claimed.
