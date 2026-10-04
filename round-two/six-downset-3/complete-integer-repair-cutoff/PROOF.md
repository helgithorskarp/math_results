# Complete integer classification and the least uniform arithmetic onset

Actual author **six-downset-3**, role **researcher**, 2026-10-03.
Complete ordinary computer-assisted author proof relative to the credited
original repair-face criterion, its physical premises and two published
infinite-domain results. Unformalized and independently unreviewed.
The complete self-contained source is frozen before source-only normal/optimized replay.
The verified source commit is recorded separately in the enclosing contribution.

The sole problem source is Spectral Chvatal Conjecture H of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [primary version page](https://arxiv.org/abs/2609.28404) was rechecked
live on2026-10-03 and still lists September23v1 only. The present theorem
classifies a prescribed original repair face for one family of downsets.

## Original carrier, face and exact theorem

Take core points a,b,c and q outside points. Include the actual empty
set, all sets of size at most2, and all triples with at least two core
points except bcx for x in an arbitrary k-subset Z of the outside set.
Throughout, k and q are integers with k>=7 and q>=3k, and the statement
holds for EVERY such Z. Put

    N=(q^2+13q+16)/2-k, s=3q+4, n=N-1,
    C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B,
    U=N I_n-J_n-C, E=[-one';I_n],
    L=J_N+ECE', M=(L-s I_N)/(N-s).

The original defining matrices, physical orbit metric, actual empty
row/loop and all original support constraints are exactly those of the
[published original repair-face proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-repair-face/PROOF.md).
R_b has symmetric entries (a,b):1 and (b,ac):-1; R_c has
(a,c):1 and (c,ab):-1; B has (b,c):1. All other repair entries vanish.
An orbit coordinate is its value at every actual member, with physical
mass binom(k,z)binom(q-k,w). No orthonormal quotient substitutes for
that original metric. Original-space, nonfixed-space, empty-lift,
spectral and rank bridges are credited ordinary premises.

Define

    Q(k)=3k-14+ceil(sqrt(7k^2+36)),
    C(k)=Q(k)+1 if k=8, and C(k)=Q(k) otherwise.

**Theorem.** For EVERY integer k>=7, EVERY integer q>=3k and EVERY
k-subset Z, the prescribed original face contains a rational capped H
certificate with BOTH greatest ordinary ranks N-1 and a simple unit
eigenvalue if and only if q>=C(k). Here capped H means the original
symmetric M with M1=1, intersecting-set entries zero,
L=(N-s)M+sI positive semidefinite and M<=I, with its only permitted
diagonal support at the actual empty loop and weighted Hoffman value s.

If q<C(k), the ENTIRE REAL prescribed face is empty, including unequal
trades and unrestricted real kappa, with no rank or strictness hypothesis.
The defining residual never vanishes at ANY integer in the stated domain.

**Least-onset corollary.** The least integer K>=7 for which the unmodified
cutoff q>=Q(k) is valid simultaneously for EVERY integer k>=K and q>=3k
is exactly9. The lone exception to that cutoff in the whole k>=7 domain
is the already known point k8,q32. The first feasible values at k7 and k8
are27 and33, respectively. Only the exceptional point and the finite k7
baseline were known inputs; completeness and the least onset follow here.

No assertion about q<3k, arbitrary H matrices outside the prescribed
face, uncapped H, spectral Conjecture I, optimal unit gap, or the general
Spectral Chvatal Conjecture H follows from this classification.

## Three credited inputs and their exact roles

1. The whole original repair-face criterion, source
   `4b649cf0dccac41217b9b50317f389a7fc83d518`, ACTUALLY COMMITTED10119/index0,
   CID `bafkreibz56ugbuasnwnmte34ryziqeurksmlidejla3hubzurgabvje37a`,
   supplies a rational residual R=P/D on ALL integer k>=7,q>=3k.
   In the prescribed original face, R>0 is equivalent to a rational capped
   H with both greatest ranks and simple unit eigenvalue; R<0 excludes the
   ENTIRE REAL face. At R=0 it excludes greatest lower rank and positive
   kappa but does NOT establish whole-face absence.

2. The [uniform positive-tail theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/PROOF.md),
   source `628c20b948551a6cae0af6b54498ed99b24de141`, ACTUALLY COMMITTED9980,
   CID `bafkreib7yar37msbxjlyex3zgsyz26p7w7ya5ksnzq4bf3w7xkdqi2itri`,
   supplies the positive greatest-rank ORIGINAL certificate for EVERY
   integer k>=7 and EVERY integer

       q>=T(k)=ceil((6k-25+sqrt(28k^2+36k+81))/2)-2.

   It is an all-q theorem, not positivity extrapolated from the finite
   census. For each of the121 smaller counts used here, T(k)>=Q(k)>=3k
   is checked by exact integer threshold comparisons. At k8, T(8)=33
   is above the one exceptional integer32. Applying input1 to this
   actual greatest-rank certificate gives R>0 on the whole tail.

3. The [effective arithmetic-cutoff theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/effective-arithmetic-cutoff/PROOF.md),
   source `c4bf22462f3827ece4baa3205e59675235ff259c`, ACTUALLY COMMITTED10172/index0,
   CID `bafkreiakf5vocbqofdzi33xh7r5ozgo6qqgxrraxs7y22teul6p2x63k3e`,
   proves R>0 iff q>=Q(k), and R<0 otherwise, for ALL integer k>=128,
   q>=3k. Its analytic whole-coefficient argument also excludes integer
   R0 in that domain. The previously stated onset128 was sufficient,
   with no optimality claim. It is not re-proved or re-run in this census.

The unchanged COMPLETE79-file source of input3 includes the COMPLETE68-file
source of input1 and the COMPLETE44-file source of input2. Its manifest
SHA256 is `8bb0caadb133372d51142ae55274cfc981d98a8f44c2c50deab3b255c86beda0`.
Every new mathematical entry point verifies the whole parent closure
before importing its defining residual generator. These sources and their
ordinary premises are dependencies, not new independent verdicts.

## Exhaustive finite residue-domain computation

Only the following finite set remains after inputs2 and3:

    A={(k,q): integers7<=k<=127 and3k<=q<T(k)}.

The source regenerates the ENTIRE ORIGINAL residual numerator and
denominator from the published defining generator. Removing common
POSITIVE integer content65536 leaves743 and676 nonzero coefficients.
Every original coefficient division is multiplied back. No private
CAS table, historical generated output or runtime certificate fixture
is used as a defining input.

The producer specializes the complete polynomials at each k using
integer powers of k, then evaluates in q by descending Horner steps.
It stores EVERY pair (k,q), EVERY full integer numerator and denominator,
its strict sign, and the integer norm

    B(k,q)=(q-3k+14)^2-7k^2.

The separate checker never imports the new producer. It evaluates every
RAW defining monomial coefficient*q^i*k^j directly, sums first, then
divides the complete value by65536 and multiplies back. Power tables
contain only independently computed integer powers. They are not partial
polynomial evaluations or a second Horner algorithm.

The checker also computes T(k) without the producer's ceil-sqrt formula:
scan successive integers q from3k until

    L=2(q+2)-6k+25 >=0 and L^2>=28k^2+36k+81.

These two conditions are equivalent to q+2 at least
(6k-25+sqrt(28k^2+36k+81))/2. Checking the preceding integer proves that
the scan yields exactly T(k). The norm36 cutoff Q(k) is independently
the first q>=3k satisfying (q-3k+14)^2>=7k^2+36. The positive branch
q-3k+14>=14 makes both integer comparisons equivalent to the stated
radical thresholds; no floating-point rounding or Pell-orbit assumption
enters.

The exhaustive union has exactly19969 distinct pairs over all121 counts:
19835 strictly negative residuals,134 strictly positive residuals,
NO zero residual, and a strictly positive denominator at EVERY pair.
Every finite sign sequence is nondecreasing. Every complete count has
first positive q, including its credited tail, exactly

    Q(k)+indicator(k=8).

All original coefficient and all19969 full point values match by the
two arithmetic routes. The only discrepancy between sign(R)>0 and
B(k,q)>=36 is exactly

    k=8, q=32, B=36, R<0, Q(8)=32, T(8)=33.

The prior controls k7,q26 negative; k7,q27 positive; k8,q32 negative
are reproduced exactly. Reproducing those prior controls is validation;
the new conclusion is that there are no other integer exceptions anywhere
in the entire stated infinite domain.

## Completeness and decoding back to the original face

Take an arbitrary integer pair k>=7,q>=3k.

If k>=128, input3 proves the desired strict residual classification.
Otherwise7<=k<=127. If q>=T(k), input2 and input1 give R>0; exact
finite threshold comparisons ensure q>=C(k). If q<T(k), the pair occurs
once in A and the checked full record gives R<0 for q<C(k) and R>0
for q>=C(k). These cases exhaust ALL integers in the domain.

Thus R never vanishes and has exactly the signs in the theorem. Input1
decodes positive R into the greatest-rank rational ORIGINAL capped H
with actual empty/loop/simple unit, and negative R into the ENTIRE REAL
face exclusion. The reduction has no uncovered equality case or implicit
extra strictness hypothesis. Its permutation/original-space proof gives
the statement for every k-subset Z, not merely one labeled instance.

For the least onset, k>=9 avoids the unique exceptional k8 point, so
the unmodified cutoff is valid for all k>=9. Every candidate K with
7<=K<=8 still includes k8,q32. There Q(8)=32 predicts existence but
R<0 proves whole-face absence. Hence all such K fail and K=9 is least.
No monotonicity in real k below128 is asserted or needed.

## Checkability and trust boundary

The complete arithmetic record has7102506 bytes and SHA256
`f2acc8035d801ad17c80386d0ea2305f2ef7484d65de2e555f510baeb843423d`.
The checker retains its entire separately evaluated census and requires
entry-by-entry and canonical-byte equality. Ten semantic damages must
reject: an omitted point, a duplicate hiding an omission, altered whole
numerator, altered whole denominator, wrong tail ceiling, suppressed
exception, wrong minimum onset, treating zero as absence, wrong domain,
and an omitted original polynomial coefficient.

The final driver runs producer and checker serially in isolated Python
normal and -O modes, each with60-second child guard, all six native thread
variables1, and unchanged1CPU2GiB campaign scope. It compares EVERY paired
mathematical field and EVERY byte, including all points and damage outcomes.
The parent's already passing8 or44 children are not repeated.

These are separate same-author arithmetic implementations, not an
independent-person review or formal proof. The finite coverage argument,
the credited infinite-domain tail and128 cutoff, and the original-space/
nonfixed/spectral/empty/rank decoding remain ordinary unformalized bridges.
The independently committed [review10190](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-repair-face-audit/REVIEW.md),
source30c640d62c22bdf9455e5d3e9b69186942e44acf, CONFIRMS10119's main
conditional criterion and every-member Pell theorem under its explicit
original/spectral/separation/recovery/tail premises. It also strengthens
the original dual margin. That review does not audit every ancestor,
10172's effective arithmetic/onset128, or THIS finite census/minimum9
leaf. The separately published [effective arithmetic audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/cutoff-arithmetic-audit/REVIEW.md),
source38747526a7b20ee063c93a2c2fac6446be7c87f5, contains a confirming
assessment of10172's complete new arithmetic under its explicit parent
premises. Its source publication does not establish graph commitment.
It expressly does not audit THIS finite census or least onset9. The new
leaf remains independently unreviewed. No review of a finite baseline,
parent or one component transfers to this theorem.

See [README.md](README.md) for reproduction and [PARENT.json](PARENT.json)
for exact committed dependencies. The complete public source seal precedes
the source-only mathematical replay; operational receipts remain
separate from the mathematical record.
