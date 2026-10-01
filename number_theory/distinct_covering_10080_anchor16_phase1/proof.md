# A six-class minimum-eight prefix forces actual LCM at least 15120

Actual author: **six-covering-2**, role **researcher**. This is an exact
computer-assisted conditional lemma checked by the author.

Fix these six congruences, displayed as `(modulus,residue)`:

    [(8,0),(9,0),(10,1),(14,1),(12,3),(16,1)].

**Lemma.** No subset of the remaining distinct moduli `n >= 8` dividing
10080, with arbitrary residues, completes these classes to a covering of
all integers. The actual LCM need only divide 10080.

**Corollary.** Any distinct covering **with minimum exactly eight** retaining
these six classes has actual LCM at least **15120**.

Both claims are conditional on the specified prefix. The unrestricted
period-10080 and period-15120 questions remain open. In particular this
artifact supplies no new global bound on `L_min(8)`.

## Complete finite reduction

Set `D = {n : n divides 10080 and n >= 8}`. Covering all integers by these
moduli is equivalent to covering the 10080 ordinary residues. Adding one
arbitrary class at each missing member of D preserves covering and
distinctness. Thus it suffices to exclude the divisor-completed model with
one class at each unused modulus. This does not require the original
covering to use all members of D, or to have actual LCM equal to 10080.

The complete certificate contains 83 records: 11 expansions, 4 uniform
cuts and 68 weighted cuts. Four weighted leaves use paired resources;
the other 64 use individual resources. There is no pending or covering
leaf. The root branches on modulus 15, with representatives 0, 1, 2 and 6.

At any expanded node the prefix is fixed and an unused modulus m is
chosen. Every actual phase `a = 0,...,m-1` is processed. A phase with zero
new coverage can be replaced by a positive-gain phase without losing any
point already covered by the prefix or by other classes. A positive-gain
phase exists because the prefix has a nonempty residual set and the m
phases partition the ambient residues.

For every positive phase the checker constructs explicit permutations on
the prime-power CRT factors 32, 9, 5 and 7. It checks bijectivity,
compatibility with every prime-power quotient, preservation of each fixed
anchor coordinate and transport of the proposed phase to an advertised
representative. Their product preserves every divisor's residue-class
partition. It therefore transforms a hypothetical completion into a
completion at an advertised child while retaining the moduli. All
advertised children and their prefixes are reconstructed from the edges.
Every actual phase is checked; a reported orbit count is not a premise.

## Exact terminal inequalities

Let U be the ordinary residues not covered by a leaf's prefix. Its
certificate supplies nonnegative integer weights f supported on U,
encoded by disjoint Cartesian CRT boxes. The checker expands all 3555
boxes in the certificate onto ordinary residues, checking support,
disjointness and integer totals. Write `W = sum_x f(x)`.

An unused modulus n can contribute at most

    C_n = max_a sum_(x = a mod n) f(x).

For a disjoint pair of unused resources m,n, charge instead

    C_(m,n) = max_(a,b) sum_(x in (a mod m) union (b mod n)) f(x).

The intersection is counted once. The checker scans every actual residue
class and every actual two-class union. Paired moduli are distinct,
unused and present in only one pair; all other resources are charged
individually. If the chosen classes covered U, their total capacity would
be at least W. Every leaf instead has a strictly greater integer demand
than the sum of capacities. Uniform cuts use `f = 1_U`. Completeness of
the checked tree and these exact strict inequalities prove the lemma.

The six fixed moduli have LCM 5040. An actual LCM below 15120 containing
them must consequently be 5040 or 10080. Both divide the ambient period
10080 and contradict the lemma. This proves the corollary while retaining
the hypothesis **minimum exactly eight**.

## Reproduction and trust boundary

From the repository root, CPython 3.10 or later, standard library only:

```sh
python3 -B number_theory/distinct_covering_10080_anchor16_phase1/check.py
python3 -B -O number_theory/distinct_covering_10080_anchor16_phase1/check.py
python3 -B number_theory/distinct_covering_10080_anchor16_phase1/controls.py
python3 -B -O number_theory/distinct_covering_10080_anchor16_phase1/controls.py
```

Both checker runs must match [expected.json](expected.json), after omitting
the elapsed `seconds` field in each case. They check all 83 records, 213
actual branch phases, 197 positive transports and 134 distinct coordinate
permutation witnesses. The audit-event SHA-256 is
`0c5d47fb575aab32db715f4360dfb8a04fe1cdc61529ef4ed64388f0509ee069`.
The controls reject nine malformed or invalid fixtures in both normal
and optimized Python; the checks do not rely on removable assertions.

The 97336-byte [certificate](certificate.json) is the complete proof input.
Its SHA-256 is
`30b1248843a44c0cb5af1899b1977c7e25d20668e874e095dfc51bccac99a848`.
No private forest, ledger, database, numerical solver or unpublished
prerequisite is needed. Original node identifiers preserve audit-event
provenance and carry no mathematical authority. Hashes alone do not prove
the result. [SHA256SUMS](SHA256SUMS) records the other source-file hashes.

Author replay with CPython 3.11.2 took 4.012 seconds normally and 3.392
seconds with `-O`, using at most 76296 KiB measured child RSS. Timings are
context, not mathematical evidence. Discovery used SciPy/HiGHS LPs with
two-second caps and one solver/BLAS/OpenMP thread to propose integer
weights and branches. The checker trusts no numerical objective, solver
status or discovery cutoff.

The arithmetic and coordinate transport are the author's earlier
[literal two-case checker](../distinct_covering_10080_anchor20_cases/check.py),
ported through the [seven-class envelope](../distinct_covering_10080_anchor15_case/proof.md)
to this six-class certificate. The mechanism uses the standard union
bound, the [residual-weight formulation](../distinct_covering_residual_weight_duals/proof.md)
and the [paired-resource capacities](../distinct_covering_joint_capacity/proof.md).
This reuse is not an independent review or proof-assistant formalization;
no method-priority claim is made.

Primary context is [Zhang–Zhang's minimum-seven paper](https://arxiv.org/html/2607.19029)
and the separate [pure-235 covering problem](https://arxiv.org/html/2605.18644),
both checked live on 2026-10-01. Neither is asserted to resolve this
conditional minimum-eight case. The assigned global minimum-eight
frontier remains separate from those published problems.
