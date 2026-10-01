# All regular seven-point triple downsets: exact capped maximal ranks

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.
The complete 644-class author replay finished successfully on 2026-10-01:
1,619.717 seconds, peak RSS 215,476 KiB, CPython 3.11.2, standard library
only, one CPU-intensive job and one native thread. Every accepted matrix
was checked exactly. The mathematical bridges below are ordinary written
mathematics, unformalized and not independently reviewed.

Let T be any simple regular collection of triples of a seven-point set:
every point occurs in the same number d of triples. Include the **full
two-skeleton**, including the empty vertex and its permitted loop:

~~~
D(T)={A subset[7]:|A|<=2} union T.
~~~

Then d is in {0,3,6,9,12,15}, |T|=7d/3, N=29+7d/3 and every star has
size s=7+d. The complete domain has 644 point-permutation classes and
2,505,122 labelled inputs. For each class the deterministic generator
proposes and the exact checker certifies a rational symmetric matrix M
with

~~~
M[A,B]=0 whenever A intersects B,     M*1=1,
L=(N-s)*M+s*I >= 0,                 M <= I,
rank L=N-7,                        rank(I-M)=N-1.
~~~

The rank N-7 is maximal among all real H matrices on the same domain;
the seven coordinate stars are its only maximum intersecting families.
For arbitrary finite nonempty products of factors in this cohort, the
eligible factors are exactly those with greatest triple degree d. If r
factors are eligible, the tensor matrix has maximal lower rank N_product-7r,
a simple unit endpoint, and exactly 7r maximum families, the coordinate
stars in those factors. This does not cover arbitrary seven-point downsets
or triple collections without regularity or without the full pair layer.

The primary problem is Conjecture H of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
General H and the distinct inertia conjecture I remain open in the
[current primary record](https://arxiv.org/abs/2609.28404), refreshed on
2026-10-01. Classical rank-three EKR is already known from
[Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494); no classical
EKR or historical-priority novelty is claimed. The claimed increment is
complete exact capped spectral coverage and the compact generator.

## Scope, prior coverage and finite completeness

There are fifteen triples through each point. Summing all degrees gives
7d=3|T|, so 3 divides d and 0<=d<=15. This exhausts the six stated degrees.
The degree-zero and degree-fifteen cases are the known uniform two- and
three-skeletons. The earlier
[point-transitive seven-point classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/POINT_TRANSITIVE_SEVEN_PROOF.md)
covers the eleven nonempty transitive triple classes; together with the
uniform two-skeleton there are twelve transitive baselines. The
[complete cubic cohort](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/PROOF.md)
and [degree-twelve cohort](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/degree-twelve/PROOF.md)
cover all ten classes at each of those degrees, including sixteen
nontransitive classes in total. The remaining finite increment is
**616 classes**, the 308 nontransitive classes at each of degrees six
and nine, representing **2,480,310 labelled inputs**. These numbers compare
with the stated published benchmarks, rather than asserting priority over
every possible structural application.

Number the 35 triples by ascending binary subset mask, with point i at bit
i for i=0,...,6. A collection is a 35-bit word. Its canonical word is the
minimum of its full S7 orbit. The parent cubic census supplies the complete
degree-three inputs using two different labelled generators. Its ordinary
completeness and full-stabilizer arguments are credited dependencies.

For degree six there are fourteen triples. Two new generators exhaust
the complete labelled domain:

1. At point zero select exactly six of its fifteen incident triples and
   exactly eight of the twenty avoiding it. Group eight-triple tails by
   their degree vectors on the other six points. Join a six-triple link
   of degree vector v to precisely the tails of vector (6,...,6)-v.
   Every valid collection has a unique such decomposition. Discarding
   a tail with degree greater than six is a necessary-condition pruning.
2. Partition the 35 triple indices into the eighteen even and seventeen
   odd indices. Enumerate all subsets of each block by binary-reflected
   Gray code, updating the seven literal degrees at each single-triple
   flip. Group the first block by its seven-degree vector and join each
   second-block vector v to the first-block vector (6,...,6)-v. Rejecting
   a partial degree above six is necessary. Every subset of all 35 triples
   has a unique two-block decomposition; no point is distinguished here.

Both labelled sets must agree **entry by entry**. Literal triple cardinality
and degrees are checked using incident-position bitmasks: (word & I_i).bit_count()
counts exactly the selected triples through i. For each unseen word every
one of the 5,040 point permutations is applied. Its orbit must stay in the
labelled domain and avoid earlier orbits; its minimum must be the current
representative. Its full stabilizer is determined by literal equality.
Orbit size times stabilizer order must be 5,040, and the orbit union must
equal the labelled domain. This gives 311 classes and 1,241,355 labelled
collections at degree six, including three transitive classes whose
labelled orbit sizes sum to 1,200.

Let W=2^35-1. Complementation word -> W xor word is an involution mapping
degree d to degree 15-d. Every permutation of the 35 triple positions
commutes with this map. The checker verifies that every point permutation
acts bijectively on all 35 triple positions, then complements entire
orbits and minimizes the **dense** word afresh. It does not complement the
least sparse word and assume the result is canonical. If pi sends the
sparse word to its orbit maximum, then pi sends its complementary word
to the dense orbit minimum. The complete dense stabilizer is pi G pi^-1,
where G is the complete sparse stabilizer. The checker verifies all
transported automorphisms literally, uniqueness, stabilizer order,
orbit/stabilizer identity, disjoint dense orbits, total labelled coverage,
and preserved transitivity. The group-conjugation completeness implication
is a written elementary bridge. No matrix transport is inferred from
complementation.

| Triple degree d | Triples | N | s | Classes | Labelled inputs | Transitive classes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 29 | 7 | 1 | 1 | 1 |
| 3 | 7 | 36 | 10 | 10 | 11205 | 2 |
| 6 | 14 | 43 | 13 | 311 | 1241355 | 3 |
| 9 | 21 | 50 | 16 | 311 | 1241355 | 3 |
| 12 | 28 | 57 | 19 | 10 | 11205 | 2 |
| 15 | 35 | 64 | 22 | 1 | 1 | 1 |

The compact results retain every canonical word, degree coverage and
automorphism profile. Sorted degree-six labelled words, as compact JSON,
have SHA256

~~~
cd7e2cc11340378286e4c895bdfffa35c13b8497b9942c04307a19ded86ffe21
~~~

The corresponding degree-nine hash is

~~~
73531e8217443f459a43f241629976d90e131d489f376dca0b62faf3af5c6e20
~~~

Counts and hashes supplement the exhaustive generation and orbit
arguments; neither a count match nor an incomplete run proves coverage.
Point relabelling of each canonical matrix covers every labelled input
by permutation congruence.

## Compact rational generation and the exact proof boundary

Let F=D(T) minus its empty member, in ascending subset-mask order, with
m=N-1. Enumerate the unordered disjoint pairs of F under the full
stabilizer. Each orbit has one unknown q_j and weight w_j equal to its
size. Define

~~~
C[A,A]=s-1,
C[A,B]=-1 for distinct intersecting A,B,
C[A,B]=q[A,B]-1 for disjoint A,B.
~~~

Let X be the m-by-7 point-star incidence matrix. For i in A, the equation
(CX)[A,i]=0 holds automatically because that star has s members. For
i outside A the same equation is exactly

~~~
sum_(B disjoint A, i in B) q[A,B]=s.
~~~

The generator assembles this integer system Aq=s directly from literal
pairs and their point incidences, combining identical equations. Exact
sparse fraction-free Bareiss elimination selects independent original
rows and pivot columns, checks every division, and rejects a nonzero
residual affine equation. Every accepted back-substituted vector is then
checked against **all original integer equations**, so a basis choice or
elimination implementation cannot silently omit an affine constraint.

For target t and weights w, the exact weighted least-squares solution
guides the choice of rational coordinates. If B is
the selected row basis and Omega=lcm(w_j), the Gram matrix

~~~
G=Omega*B*diag(1/w)*B^T
~~~

is an integer positive definite matrix, since the rows are independent.
In exact arithmetic the minimizer solves G lambda=Omega*(s1-(1+t)B1),
then sets q=(1+t)1+diag(1/w)B^T lambda. A fixed **70-digit Decimal LDL solve**
approximates this vector solely as a proposal. Decimal is not an interval method and no
approximate eigenvalue, residual, sign or LDL pivot is a proof of H.
An unsuccessful proposal stops or proceeds to another bounded proposal;
it is not real infeasibility.

Free variables are rounded deterministically with ROUND_HALF_EVEN to
the chosen rational grid. Pivot variables are recovered by exact Fraction
back-substitution in the exact echelon system. The actual matrix entries
are rational from this point onward. The fixed bounded target list is
(-3,-2,-1,0,-4,-6,-8), and the grid denominators are
(20,40,80,160,320,640,1280,2560), in that order. Only exact PSD/rank tests
accept a candidate. No external numerical library, catalogue or fixed
matrix corpus is needed. The particular Decimal proposal may change the
generated certificate, but cannot make an invalid candidate pass the
subsequent exact checks. The completed results record the selected
target/grid and matrix-denominator profiles, plus an aggregate digest of
all exact per-class records.

## Empty-vertex lift, cap and two positivity criteria

Let E=[-1^T;I_m] and J denote the all-ones matrix of the indicated order.
Use the credited structural lift

~~~
L=J_N+E*C*E^T,     M=(L-sI)/(N-s),
U=N*I_m-J_m-C,     N*I_N-L=E*U*E^T.
~~~

Because E^T1=0, L1=N1, hence M1=1. The prescribed nonempty diagonals and
intersecting entries give M[A,B]=0 whenever A intersects B. The permitted
empty loop and every empty incident entry remain in the full lift. The
checker independently verifies every full support entry, symmetry, row
sum, actual downset, actual star size, core star kernel, centered full
star kernel, and upper-lift entry.

Integer fraction-free Schur congruences check C>=0 of rank m-7 and U>0
of rank m. Every nonzero pivot must be positive, every division exact,
and every zero pivot must have a zero residual row. Both full forms L
and NI-L are also checked, with ranks N-7 and N-1. These are the credited
parent positivity helpers, tracing to the earlier
[integer Schur checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/nine_point_exceptions.py).

A second positivity route reduces the lower core without losing a
direction. Reorder F as its seven singleton members S followed by R,
the pairs and triples. Then X=[I_7;Z]. The exact identity CX=0 gives

~~~
C=[-Z^T;I]*B0*[-Z,I],      B0=C[R,R].
~~~

The checker regenerates every cross-block and singleton-block identity
separately. Thus B0>=0 is equivalent to C>=0, and their ranks agree,
since [-Z^T;I] has full column rank. The required B0 size is m-7, and
positive definiteness gives the maximal core rank directly.

Integer Faddeev--LeVerrier regenerates the characteristic polynomials of
**B0 and the full upper core U**, checking trace divisibility and the final
Cayley--Hamilton residual. If a_j are the coefficients of det(xI-A), the
criterion (-1)^j a_j>=0 makes det(tI+A) have nonnegative coefficients and
positive leading coefficient, so it has no positive root. A negative
eigenvalue would give such a root; symmetry makes all eigenvalues real.
Trailing zero coefficients give nullity. The checker requires ranks
m-7 and m respectively. This is the credited
[polynomial criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/verify.py),
applied to the smaller lower principal form and the full upper core.
Different exact criteria are used; no independent peer review is implied.

The full-column-rank E has range 1-perp. The two lower summands have
orthogonal ranges, hence rank L=1+rank C=N-7. U>0 gives rank(I-M)=N-1.
Therefore every certified factor has spectrum in [-s/(N-s),1], lower
multiplicity seven and a simple unit endpoint.

## Universally maximal rank and the equality families

For any real H matrix on this domain, let L=(N-s)M+sI. An intersecting
family of a nonempty members, with indicator x, has centered vector
z=x-(a/N)1 and

~~~
z^T*L*z=a*(s-a)>=0.
~~~

Thus a<=s. If a=s, PSD implies Lz=0. All seven centered stars are
independent: an empty-vertex evaluation of a zero linear combination
forces its coefficient sum to vanish, and singleton i then forces its
i-th coefficient to vanish. Every real H matrix has rank L<=N-7,
without rationality or cap assumptions. The matrices above attain
that bound and their kernels are exactly the centered-star span.

For a maximum family its indicator consequently has the form
f(A)=b+sum_(i in A)a_i. Its empty value is zero, since its size s>=7
excludes a family containing the empty set. Singleton values force
a_i in{0,1}, and the full pair layer allows at most one nonzero
coefficient. Nonemptiness forces exactly one. The only maximum families
are the seven point-stars. These rank/equality mechanisms are credited
prior work, applied to the additional 616 classes.

## All finite mixed products

For arbitrary certified factors on disjoint point supports, their tensor
matrix is rational, symmetric and has row sums one. Intersecting product
members intersect in a factor where the corresponding matrix entry is
zero, preserving support. The star density

~~~
p(d)=(7+d)/(29+7d/3)
~~~

is strictly increasing: for d2>d1 the cross-multiplied difference is
(38/3)(d2-d1)>0. Thus eligible factors are exactly those with largest
degree d_max. Let their number be r, let N_product be the product of
factor cardinalities, and let S=p(d_max)*N_product.

Each endpoint magnitude rho_j=s_j/(N_j-s_j) is at most11/21<1.
A negative eigenvalue product has an odd number of negative factors
and magnitude at most rho_max. Equality requires exactly one negative
factor at an eligible endpoint and eigenvalues one in all other factors.
Three negative factors have magnitude at most rho_max^3<rho_max;
a smaller-degree negative endpoint or any additional nonunit factor
also makes the inequality strict. Since each unit endpoint is simple,
the product lower multiplicity is exactly7r and its unit endpoint
remains simple. This proves the cap and lower rank N_product-7r.

The centered coordinate-star cylinders of eligible factors span the
product kernel. Their independence forces the same rank upper bound
for every real H matrix on the product domain. That domain retains
all singletons and pairs, including pairs across factors. The same
binary-indicator argument gives precisely7r maximum families, all
eligible coordinate stars. The tensor mechanism is credited to the
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md);
the new finite bases extend its exact coverage.

## Reproduction and limits

From the repository root, CPython3.11.2 or compatible Python3.11+,
standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/regular-seven/verify.py --check round-two/six-downset-3/regular-seven/RESULTS.json
~~~

The default command regenerates the complete domain and all matrices;
it requires no saved progress file or numerical package. An explicitly
partial --smoke run checks eight selected cases, and cannot check a
complete expected-results file. Author-side --progress and --resume
support bounded local persistence, with an exact source fingerprint
and checked prefix. Resume trusts earlier per-class records; it is
unnecessary for a clean reader replay and is not a separate independent
proof. Progress files and full per-class logs are local, not publication
inputs. Compact results and source hashes are reproducibility evidence,
not substitutes for finite completeness or the written bridges.

The ordinary completeness, group-conjugation, congruence, eigenvalue,
rank and equality arguments above remain unformalized. Decimal proposals
and the earlier NumPy probes do not prove PSD. Every accepted rational
matrix is checked exactly after generation. A timeout, UNKNOWN result,
failed proposal, memory kill or incomplete enumeration would not be
mathematical nonexistence. No general H/I conclusion is asserted.
