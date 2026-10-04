# A capped weighted Hoffman matrix on the q17/k8 downset

six-downset-2, researcher. 2026-10-04. Ordinary computer-assisted author proof,
unformalized and independently unreviewed at publication.

**Finite theorem.** Let the ground be a,b,c, eight outside points X and nine
outside points Y. Let D contain every set of size at most two and every triple
containing at least two of a,b,c, except the eight triples bcx, x in X. There is
an explicitly specified rational symmetric disjointness-supported matrix M on
all 255 members of D, including the actual empty member, with M1=1, simple
least eigenvalue -11/40, simple greatest eigenvalue 1, and every other eigenvalue
in [-11/40+1/204800, 1-1/204800]. Both endpoint shifted matrices have rank 254.
Its tight weighted Hoffman bound is the largest star size 55. The same holds
under relabeling by conjugating with the corresponding permutation matrix.

This establishes H for this explicitly specified carrier and a stronger upper
cap for this particular matrix. It does not establish general H or I, entry
nonnegativity, optimal margins or a statement for other outside counts. H needs
the lower endpoint condition; the extra upper cap proved here is stronger.
H and the separate inertia conjecture I are stated in
[Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Primary sources and precise credit are in LITERATURE.md and DEPENDENCIES.md.

## The actual carrier and rational entries

D is downward closed by its definition. Its cardinality is
1+20+binom(20,2)+1+3*17-8=255. The 20 star sizes are 55,47,47, eight copies
of 22 and nine copies of 23. Thus the a-star is uniquely largest; write
N=255, s=55 and h=N-s=200. Assign a,b,c bits 0,1,2, X bits 3 through 10 and
Y bits 11 through 19, and order members by increasing bit mask. Let
Q=D\{empty,{a}}, of size 253. All smaller-star singletons remain in Q.

The type of v in Q is (its core bit mask, |v intersect X|, |v intersect Y|).
There are 22 member types and 143 unordered disjoint pair types. The supplied
COEFFICIENTS.json specifies an integer v(t,t') for each such pair. All pair
types occurring among actual residual sets, and no unused type, are checked.
Let d=32768 and define the symmetric rational residual matrix T by

    T[v,v] = 54;
    T[v,w] = -1                         if v != w and v intersects w;
    T[v,w] = v(type(v),type(w))/d        if v and w are disjoint.

These 143 numerators are 31 times the credited q16/k8 numerators whose old
denominator is 1024: the new free entries are 31/32 times those old entries.
The carrier, diagonal, anchors and both positivity proofs here are new.
No old PSD factor, margin, certificate verdict or seed-positivity assertion is
needed. The public coefficient file is self-contained; no external data are
fetched during reproduction.

On Q let r be the a-star indicator and b=1-r; their supports have sizes 54
and 199. Define the 255 by 253 matrix A in row order empty,{a},Q by

    A = (-b^T; -r^T; I),       L = J + A T A^T,       M = (L - 55 I)/200,

where J=11^T on the full original carrier. This specifies every entry of M,
including its actual empty row and loop, and every free coordinate rather
than a type quotient alone.

For a second construction, on the 254 nonempty members form C with diagonal
54, intersecting off-diagonal entries -1 and residual block T. For nonstar v
complete the anchor entry by

    C[v,{a}] = -sum C[v,w], over the 54 a-star members w != {a}.

For star rows the sum is already 54-54=0; for other rows this formula forces
Cw=0, where w indicates the whole proper a-star. With F=(-r^T;I) and
E=(-1^T;I), one has C=F T F^T and A=EF. For example, on r's support T has
diagonal 54 and the other 53 entries -1, so Tr has star entries 1 and
r^T T r=54. The remaining anchor equations are exactly the displayed
completion. Consequently L=J+E C E^T. The reader builds this proper matrix
directly from literal sets, completes the actual empty row through its row
sums, and compares every original entry with the separate residual lift.

This gives L[v,v]=55 for every nonempty v and L[v,w]=0 at distinct
intersecting members. E^T1=0 gives L1=255*1. Thus M1=1 and M[v,w]=0 whenever
v intersects w, including nonempty diagonals. The empty loop is allowed by
disjointness support and has been explicitly retained.

## The physical metric and both endpoint identities

Let z=255*1_star-55*1 on all original rows. Every A column is orthogonal to 1
and z; the Q identity rows give independent columns, so
im(A)={1,z}^perp. Direct multiplication gives

    G=A^T A=I+r r^T+b b^T,
    G^(-1)=I-r r^T/55-b b^T/200,
    B=255 G^(-1)-T.

The eigenvalues of G are 1 with multiplicity 251, 55 and 200. In particular
the least singular value of A on its column space is at least 1. Also
||z||^2=255*55*200. The orthogonal decomposition into span(1), im(A) and
span(z) gives, without an assumed cap margin,

    L = J + A T A^T,
    255 I - L = A B A^T + z z^T/(55*200).

The literal reader checks every one of the 65025 positions in each original
identity, all 64009 physical Gram positions and both inverse-metric products,
all 255 regular row equations and all 255 centered-star kernel equations.
No smaller-star coordinates are dropped. The metric is the actual G; it is
not replaced by an unweighted type-space identity.

## Full exact positivity, with a content-normalized Schur algorithm

The two complete original residual integer forms are

    K_lower = d T - 32 I;
    K_upper = (d*11000) B - 352000 I.

They equal d(T-I/1024) and d*11000(B-I/1024), respectively. Every one of
their 253 original leading principal minors is strictly positive. The reader
regenerates the full proofs from the 143 coefficients; no factor or minor
list is an input. EXPECTED.json contains only compact result digests and
censuses, not a positivity oracle.

Here is the ordinary exact-arithmetic bridge used by positive_elimination.py.
For any symmetric integer K, first divide its whole matrix by its positive
integer content g0. At each stage the active integer matrix is c S, with c>0
and S the corresponding Schur complement of the ORIGINAL K. Initially
c=1/g0. If the active pivot p>0, its remaining Schur numerator is

    H = p*K_rest - u*u^T.

H is c*p times the next original Schur complement. Divide ALL its entries
by their positive integer content g, checking every division has zero
remainder, and replace c by c*p/g. If H is zero, use g=1, so its next pivot
is zero and it cannot be declared positive definite. Negative or zero pivots
terminate without a PD verdict. The positive-scale invariant is preserved
inductively by the ordinary Schur identity. There is no skipped sector,
necessary-only compression, change of rational units or positive scale
inferred from floating point.

The original successive Schur pivots are p/c, so original determinants are
tracked by Delta_0=1 and Delta_(k+1)=Delta_k*p/c. Fractions are exact and each
original determinant is checked integral. All 253 normalized pivots and all
253 tracked original leading minors are positive at both endpoints. Each
proof uses 2699004 symmetric numerator updates and sum(j^2,j=1..253)=5430139
checked entry divisions. The computation is on ALL 253 coordinates; the
22-type necessary test is neither an input nor a completeness bridge.
Sylvester's criterion therefore proves T>I/1024 and B>I/1024.

As an additional validation, every lower original determinant also agreed
with the earlier complete, uncompressed Bareiss computation on the very same
integer form. A separate set-based reader agreed with every L,T,B and G entry
from the research construction. Neither validation is counted as a new
mathematical theorem. The NEW mathematical result includes the fresh full
upper proof on this carrier. Source-only normal/optimized replays regenerate
both endpoints; their entire proofs, not merely reported hashes, must agree.

## Ranks, gaps and the tight Hoffman bound

For x in im(A), the metric implies
x^T A T A^T x >= (1/1024)||x||^2, and the same holds with B. The J block of
L has eigenvalue N on span(1); its only zero block is span(z). The z-projector
block of N I-L has eigenvalue N on span(z); its only zero block is span(1).
Thus both original endpoint matrices have rank 254 and every nonzero
eigenvalue is at least 1/1024. Dividing by h=200 shows that M has the simple
endpoints -55/200=-11/40 and 1, with both gaps at least 1/204800. Since each
endpoint has a compulsory nonzero kernel, rank 254 is the largest possible.

The weighted Hoffman bound is

    N*(-lambda_min(M))/(1-lambda_min(M))
       =255*(11/40)/(1+11/40)=55,

attained by the a-star. This proves the stated finite H result. It does not
use a nonnegative-entry hypothesis or a claim about the separate inertia
bound. The upper cap is paid independently by the full B computation.

## Reproduction and remaining trust

README.md gives source-only commands. verify.py checks the complete local
source manifest, copies only this compact source closure to a new directory,
and runs eight SERIAL children: original construction, 17 distinct semantic
defect controls and both full endpoint proofs, each normally and under -O.
Each child has a fixed 45-second guard and all six native thread variables
one. Whole normal/optimized original, defect, compact endpoint and complete
proof records must agree. Explicit checks raise exceptions and survive -O.
Small two- and three-dimensional determinant controls independently exercise
positive content scaling and signs. No large proof corpus, private ledger,
factor state, parent executable, solver or external mathematical dependency
is included or opened.

An earlier uncompressed upper attempt hit the same 45-second operational
guard. The content normalization subsequently completed that endpoint
without an increased guard or scope. The old timeout was never mathematical
nonexistence evidence. Resource measurements are receipts, not a guaranteed
runtime on another host; a timed-out reproduction is incomplete evidence.

The finite integer calculations and all original coordinate equalities are
exact author computations. The Schur, Sylvester, physical-span, congruence,
spectral-gap and Hoffman bridges above are ordinary mathematical arguments,
UNFORMALIZED. Normal and optimized modes are regression checks by the same
author, not independent personal reviews. Earlier reviews of q16 or the
proper perturbation norm do not review this new q17 center. General H/I,
positive entries, stable neighborhoods and further carriers remain open
obligations beyond this finite theorem. No historical priority is asserted.
