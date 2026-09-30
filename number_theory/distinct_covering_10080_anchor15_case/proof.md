# A seven-class minimum-eight prefix forces actual LCM at least 15120

Actual author: **six-covering-2**, role **researcher**. Exact computer-assisted
conditional lemma, checked by the author. No independent reviewer verdict
or new method-priority claim is made.

Fix these seven congruences, displayed as `(modulus,residue)`:

    [(8,0),(9,0),(10,1),(14,1),(12,6),(16,4),(15,1)].

**Lemma.** No subset of the remaining distinct moduli `n >= 8` dividing
10080, with arbitrary residues, completes these classes to a covering of
all integers. The actual LCM need only divide 10080.

**Corollary.** Any distinct covering **with minimum exactly eight** retaining
these seven classes has actual LCM at least **15120**.

These are conditional claims. The unrestricted period-10080 and
period-15120 questions remain open. No claim about minimum seven, general
minimum-at-least-eight systems, or a pure-235 restriction is substituted
for the stated lemma.

## Reduction and exact proof

Set `D = {n : n divides 10080 and n >= 8}`. Covering all integers by such
moduli is equivalent to covering the 10080 ordinary residues. Adding one
arbitrary class at each missing member of D retains coverage and
distinctness. Thus it suffices to exclude the divisor-completed model with
one class at every remaining resource; the original covering need not use
all of them.

The supplied certificate is a complete 139-record tree with 20 expansions,
39 uniform cuts and 80 weighted cuts. Eighteen weighted leaves use paired
resources; the other 62 use individual resources. There is no pending or
covering leaf.

At an expanded node, the prefix is fixed and an unused modulus m is
selected. Every actual phase `a = 0,...,m-1` is processed. A phase with
zero new coverage may be replaced by a positive-gain phase without losing
any point already covered by the prefix or other classes. For each positive
phase, the checker constructs coordinate permutations on the prime-power
CRT factors of 10080. It checks bijectivity, compatibility with each
prime-power quotient, every fixed anchor, and transport to an advertised
representative. The combined CRT permutation preserves every divisor's
residue-class partition. It therefore transforms any completion into a
completion at an advertised child without changing the moduli.

This is a check of all actual phases, not reliance on a reported orbit
count. The root modulus-32 split has representatives 1, 2 and 12. All
advertised children and their full prefixes are reconstructed from the
certificate's edges, and every leaf is checked.

At a leaf let U be the ordinary residues left uncovered by its fixed
prefix. The certificate supplies nonnegative integer weights f supported
on U, encoded by disjoint Cartesian boxes. The checker expands those
boxes onto ordinary residues and verifies their support and totals.
The residual demand is `W = sum_x f(x)`.

An unused modulus n can contribute at most

    C_n = max_a sum_(x = a mod n) f(x).

For a disjoint pair of unused resources m,n, charge instead

    C_(m,n) = max_(a,b) sum_(x in (a mod m) union (b mod n)) f(x).

The intersection is counted once. The checker scans every actual residue
class and every actual two-class union. Paired moduli are distinct, unused
and present in only one pair. Remaining resources are charged individually.
Any covering has demand at most the sum of these capacities, since at most
one class is selected per resource. Every leaf has a strictly larger
integer demand. Uniform cuts are the special case `f = 1_U`. This excludes
all leaves, and completeness of the checked branch tree proves the lemma.

The seven fixed moduli have LCM 5040. An actual LCM smaller than 15120 must
therefore be 5040 or 10080. Either hypothetical covering also covers the
ambient period 10080, contradicting the lemma and proving the corollary.
The hypothesis **minimum exactly eight** is essential to the stated
completion domain and is retained in the corollary.

## Reproduction and trust boundary

From the repository root, CPython 3.10 or later, standard library only:

```sh
python3 number_theory/distinct_covering_10080_anchor15_case/check.py
python3 -O number_theory/distinct_covering_10080_anchor15_case/check.py
python3 number_theory/distinct_covering_10080_anchor15_case/controls.py
```

The checker processes 139 records, all 439 actual branch phases and 390
positive transports. The event hash is
`249ace7755dedbf23b40701231dc44904d0da86ee93fb829a734dd07f5cc627b`.
Normal and optimized Python must agree with [expected.json](expected.json).
The controls reject nine malformed or invalid fixtures.

The 107884-byte [certificate](certificate.json) is the complete proof input.
No private forest, SQLite database, numerical solver or unpublished
prerequisite is required. Original identifiers only preserve audit-event
provenance; they carry no mathematical authority. Hashes alone do not
prove correctness.

Discovery used SciPy/HiGHS LPs with two-second caps and one numerical thread
to propose integer weights and branch choices. The standalone proof
checker uses literal Python integer arithmetic and explicit permutations;
it trusts no numerical objective, infeasibility status or discovery cutoff.
The author's earlier literal checker is ported here with a different
prescribed-prefix envelope. This reuse is not an independent review or
formalization.

The mechanism is the standard residual-weight union bound and the credited
[paired-resource bound](../distinct_covering_joint_capacity/proof.md),
using the author's earlier [literal two-case checker](../distinct_covering_10080_anchor20_cases/check.py).
Current primary context is [Zhang–Zhang's minimum-seven paper](https://arxiv.org/html/2607.19029)
and the separate [pure-235 covering problem](https://arxiv.org/html/2605.18644),
both checked on 2026-09-30. Neither paper is asserted to prove this
conditional minimum-eight case. No priority claim follows from the bounded
literature or graph search.
