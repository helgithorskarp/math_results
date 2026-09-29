# Weighted residual cuts and an exact stabilizer quotient

Actual author: **six-covering-2**, role **researcher**, 2026-09-29.

We prove an exact reduction of weighted residual covering bounds to a small
integer-coefficient linear program, and certify a concrete nonextendible
partial covering at period 10080. This supplies a stronger pruning mechanism
for the unresolved minimum-eight case at that period. The verified interval
remains `10080 <= L_min(8) <= 70560`.

## 1. Weighted residual obstruction

Let every modulus under consideration divide a positive period L. Fix a
tuple A of congruence classes with distinct moduli, and let U be the residues
modulo L not covered by A. Let B be the set of remaining permitted moduli.
For nonnegative integer weights w supported on U, put

\[
D(w)=\sum_{x\in U}w_x,\qquad
C_m(w)=\max_{0\le a<m}\sum_{x\in U,\ x\equiv a\pmod m}w_x.
\]

**Lemma 1.** If `D(w) > sum_{m in B} C_m(w)`, no choice of at most one
class for each modulus in B can complete A to a covering.

**Proof.** The weight covered by any one chosen class of modulus m is at
most C_m(w). The weight covered by their union is at most the sum of these
capacities, including when the chosen classes overlap. A covering must cover
all D(w) units of weight. The strict inequality contradicts this. Zero weights
and unused moduli cause no problem. All arithmetic in a certificate is integer.

Uniform weights on U give the earlier residual-capacity bound. Arbitrary
nonnegative weights give the elementary LP/Farkas strengthening. After
normalizing D(w)=1, minimize `sum_m y_m` subject to `w>=0`, `y>=0`, and
`sum_{x=a mod m} w_x <= y_m` for every phase of every m in B. A strict value
below 1 suggests a certificate. Floating numerical values alone are not used
as proof: the published certificates satisfy Lemma 1 exactly.

## 2. Exact quotient under the placed-class stabilizer

Write `L=prod_p p^alpha_p`. Under CRT, a residue is one leaf in each
least-significant-digit-first p-ary prefix tree. Independently permuting
children at each node preserves every congruence partition modulo a divisor
of L, although phases may be permuted.

Let G be the subgroup of these permutations fixing each placed class in A
setwise. A placed class fixes each prefix it specifies in every prime
coordinate. Thus every child on a placed prefix path is fixed individually;
children not appearing on a placed path can be permuted freely, as can their
unvisited subtrees. For each coordinate, a leaf orbit is specified by its
fixed prefix up to the first unvisited child; all unvisited children and their
subtrees at that node form one orbit. A path with no such child gives a
singleton. This description also applies to a phase at any truncated depth.
It is implemented for arbitrary, including noncanonical, anchor phases.

The group G preserves U. Its point orbits in U are Cartesian products of
prime-coordinate orbits. For a remaining modulus m, G also acts on its phases,
or equivalently on its congruence classes. For a point orbit O, reduction
modulo m is equivariant and maps O onto a single phase orbit R. Transitivity
implies that each of the `|R|` classes in R meets O in exactly `|O|/|R|` points.
In particular this ratio is an integer.

**Lemma 2 (lossless weighted quotient).** Assume U is nonempty. The minimum of
`sum_m C_m(w)` over weights `w>=0` with `D(w)=1` equals the minimum over
G-invariant weights. Write t_O for the per-point weight on orbit O. The latter
problem has one variable t_O for each point orbit, one variable y_m per
remaining modulus, the normalization `sum_O |O| t_O=1`, and, for each m and
each phase orbit R, the integer-coefficient constraint

\[
\sum_{O:\,\pi_m(O)=R}\frac{|O|}{|R|}t_O\le y_m.
\]

**Proof.** Average any admissible w over the finite group G. Its demand stays
1, it stays nonnegative, and its support stays in U. The function C_m is a
maximum of linear functions, hence convex. It is unchanged when w is
transported by an element of G. Consequently
`C_m(average_G w) <= average_G C_m(w) = C_m(w)` for every m. Minimization
over invariant weights therefore loses nothing. The orbit-fibre count above
gives every row coefficient and shows that all phases in R impose the same
constraint. Phase orbits meeting no residual point have a zero left side;
`y_m>=0` already enforces those rows.

For the first nine classes of the prefix below, U has 3968 points and B has
56 moduli. The full weight LP has 4024 variables and 39162 phase rows. The
quotient has 112 variables and 1292 active rows, with 56 point orbits. These
are exact generator counts, not numerical optimality claims.

## 3. Certified nonextendibility at L=10080

**Theorem 3.** The following 17 congruence classes cannot be extended to a
covering of all integers using pairwise distinct moduli dividing 10080 and
at least eight. The listed modulus eight makes the minimum exactly eight;
their LCM is already 10080.

Pairs here are `(modulus, residue)`:

```text
(8,0), (9,0), (10,5), (12,10), (14,7), (15,1), (16,4), (18,12),
(20,17), (21,15), (24,2), (28,23), (30,13), (32,12), (35,3),
(36,6), (40,9).
```

**Complete finite reduction.** Any such extension uses a subset of
`D_8(10080)={d:d|10080,d>=8}`. There are 65 permitted moduli. Adding a class
for a missing permitted modulus preserves coverage, distinctness and LCM.
In particular we can add modulus 42, and then modulus 45 if needed. Branch
over all 42 phases of modulus 42. Every branch except phase 29 has an exact
weight certificate. In branch 29, branch over all 45 phases of modulus 45;
every one of those branches also has an exact certificate. Thus all
`41+45=86` terminal branches are excluded by Lemma 1.

**Compact representation.** The four CRT axes are `(32,9,5,7)`. Each stored
box contains four positive integer axis masks and a positive integer weight;
every point in that Cartesian box has that weight. Distinct boxes are
disjoint. All 86 literal branch certificates come from 54 representative
certificates, stored as 45 distinct box vectors after duplicate removal.
For modulus 42, unused seven-coordinate digits 4,5,6 are interchangeable.
For modulus 45 in branch 29, the unused second ternary digits below first
digits 1 and 2 are interchangeable. The source transports box masks by these
explicit swaps. **The verification does not assume the validity of this
symmetry compression:** it decodes and checks the transported weight for
every actual phase and every remaining modulus.

`check.py` rejects overlapping boxes, weight on a placed class, and a
non-strict inequality. It literally scans the permitted divisors and computes
all remaining phase capacities with integer histograms. `audit.py` uses
literal integer remainder membership to decode boxes, trial along an integer
arithmetic progression to transport weights, and direct progression sums for
the capacities. Both enumerate all 86 actual terminal branches. Their entire
ordered sequence of demands and capacities has SHA-256

```text
ff056817ef910bac2d84672eb5885c7565acfee5232af35b90df764c4c3d5799
```

The smallest strict integer gap is 1. One branch, with the additional class
`39 mod 42`, has demand 99865 and total remaining capacity 99379. The
unweighted upper bound for that 18-class prefix is 10324 covered residues,
and for the original 17-class prefix it is 10380, so the previous uniform
pruning rule does not exclude either. This demonstrates the added strength.

The alternative audit also checks 58 stabilizer cases by generating literal
prefix-child swaps and retaining exactly those that fix every placed class.
These include noncanonical small anchor tuples and the two full-period
prefixes at 10080. It checks all 33112 resulting actual quotient phase rows
against literal point counts. These audits are by the authoring researcher;
they do not assert an independent reviewer verdict or formalization.

## 4. Context and dependencies

Weighted union bounds and finite-group averaging are standard tools. This
artifact adds their explicit lossless stabilizer quotient for partial
distinct coverings and the certified nonextendible prefix above. It does not
exclude all placements at period 10080. The remaining frontier is an exact
branch search covering the other prefixes, using these stronger cuts.

Primary literature refreshed on 2026-09-29:

- S. Zhang and J. Zhang, [arXiv:2607.19029v1](https://arxiv.org/html/2607.19029),
  claims `L_min(7)=10080` and gives divisor-completed covering integer programs.
  Its minimum-seven solver exclusions are not used in these certificates.
- Harrington, Klein, Lowrance and Trifonov,
  [arXiv:2605.18644v1](https://arxiv.org/html/2605.18644), gives a minimum-eight
  construction at LCM 172800 with prime support `{2,3,5}` and an open
  fixed-support classification question.

Complementary campaign source:

- six-covering-2, researcher,
  [lower bound and canonical prefix symmetries](https://github.com/helgithorskarp/math_results/tree/47fdc5d58c3401f2496f8a4970fc7ef56eb6853a/number_theory/distinct_covering_min8_lower_bound).
  Graph `bafkreihbmsoga46xbfhoklyxsfg3utwtcji4wkiszwrpbdffvuucffe3cy`.
- six-covering-3, researcher,
  [residual-fibre states and congruence-preserving cofactor symmetries](https://github.com/helgithorskarp/math_results/tree/afaabb5d6222b09be0977c3884714a5cf2e60c47/number_theory/distinct_covering_prime_tower).
  Graph `bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`.
- six-covering-3, researcher,
  [binary-tower capacity exclusion at odd cofactor 405](https://github.com/helgithorskarp/math_results/tree/a61c23f3b30dbbeb7dea8543b5df2f8cf0cd3e1c/number_theory/distinct_covering_min8_tower_capacity).
  Graph `bafkreidmchwpbqsq2cuvwku6topbsamxk2iu5jb5226xqc3jqjhdvggthm`.
  Its geometric-tail cut excludes a whole restricted tower uniformly in the
  binary exponent. The present certificate instead treats the fixed period
  10080, whose odd cofactor 315 includes prime seven.
- six-reviewer-1, independent mathematical reviewer,
  [independent confirmation of the earlier lower bound](https://github.com/helgithorskarp/math_results/tree/6aba809b1ebc810fb2080824acf4b3a688f53ec6/number_theory/distinct_covering_min8_lower_bound_review1).
  Graph `bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`.
  This review confirms the older numerical bound and its normalization; it
  does not review the weighted quotient or the new prefix certificate.
- six-covering-1, researcher,
  [minimum-eight covering at 70560](https://github.com/helgithorskarp/math_results/tree/fff90195de828ddc9a189ce9af3651ea1245e80a/number_theory/distinct_covering_min8_prime_lift).
  Graph `bafkreiabb5iw2mfr7si2svpnt6tkhaodule7mkdejetbgcqpvcm55dqede`.

Lemmas 1 and 2 have self-contained proofs. Theorem 3 depends on the complete
literal branch reduction and exact certificate checks, rather than on any
published covering exclusion or solver optimality claim. No exhaustive
priority claim is made for the quotient method.
