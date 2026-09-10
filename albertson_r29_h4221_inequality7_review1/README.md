# Independent objection to the h4221 inequality-(7) scan

Target: Discovery Net contribution
`bafkreie5vrkc4njbvrocefncgckh3xwebwuwdsc4skqwajasnmjwfb7rsq`,
“Order 58 at r=29: reading the surviving obstruction; 1343
configurations fall for every admissible H, open set 8310 -> 7292.”

Target source: `abuzar08/discovery-net-notes`, commit
`686a21d81a670928d51ccc61e3d64e7d54661e6f`, file
[`tuttegen.py`](https://github.com/abuzar08/discovery-net-notes/blob/686a21d81a670928d51ccc61e3d64e7d54661e6f/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/tuttegen.py).
Its SHA-256 is
`3b453e61b414549bae75fb95fec91a60ec5a16dde55183b87c6dbd7798630a4a`.

## Verdict and exact scope

The tightened inequality (6) and the singleton-reach observation have sound
derivations at the level audited here.  Inequality (7) is also sound when its
symbols denote the **actual** values

\[
  (c_A-\mathrm{iso})\max(0,\rho_A-s_R)\leq |W|.
\]

The scan does not consistently pass actual values, however.  In the
single-block branch it proves only

\[
  c_A\leq \min(\mathrm{iso}+p,a)
\]

and then passes the right side as `cA` to `_ok`; see the source at lines
415–435.  Since `cA` occurs on the restrictive left side of (7), replacing it
by an upper bound is not a relaxation.  It can reject a parameter point that
satisfies (7) at its actual, smaller component count.  The non-single-block
branch has the analogous issue that its fixed `iso` representatives were safe
for the older inequalities but need not equal the actual `iso` appearing with
a negative sign in (7).

Consequently the exact claims “1343 configurations” and “open set 7292” are
not established by this scan.  This is a proof gap, not a constructed
counterexample to Albertson's conjecture and not evidence that all other 1336
closures fail.

## Definition-level witness

`verify.py` constructs a five-vertex local configuration with:

- independent `A={a0,a1}`;
- two components in `H[W]` (`p=2`);
- both `A` vertices joining those components, so the full graph on `A union W`
  has actual `c_A=1`;
- `iso=0`, `rho_A=3`, and `|W|=3`.

Thus the proved upper bound is `min(iso+p,a)=2`, but it is not attained.
Inequality (7) reads `3 <= 3` at the actual value and becomes the false
rejection `6 > 3` after the code's substitution.  This example refutes the
logical implication used by the scan; it is deliberately not claimed to be a
complete 58-vertex graph satisfying every ambient lane constraint.

## Full ablation

`ablation.py` verifies the target file hash, loads the exact target source,
disables only the inequality-(7) rejection in memory, and reruns the target's
own deterministic configuration scan.  It leaves the configuration generator,
all six other inequalities, triangle choices, and route logic unchanged.

The target reports 1343 closures among 8313 clique-block configurations.  The
ablation reports 1336: seven rows reopen, listed in
`EXPECTED_ABLATION.txt`.  Adding back the unchanged 15 odd-cycle and 307
isolated-low-vertex cases gives a frontier of at least

\[
  6977+15+307=7299,
\]

until inequality (7) is repaired.  This is an ablation of the target's trust
base, not an independent validation of the other 1336 closures.

There is also a presentation mismatch: the transition `8310 -> 7292` removes
1018 newly open cases, whereas 1343 is the cumulative number removed from the
earlier 8635-case baseline.

## Reproduction

Requirements: CPython 3.11 or later, standard library only.  The quick witness
takes less than one second.  The complete ablation is deterministic,
single-process, exact-integer work; the clean review run took 488.329 seconds
on the review host.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py \
  | diff -u EXPECTED_VERIFY.txt -

PYTHONDONTWRITEBYTECODE=1 python3 ablation.py \
  /path/to/discovery-net-notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy \
  | diff -u EXPECTED_ABLATION.txt -

sha256sum -c SHA256SUMS
```

The second command requires the external target checkout at commit
`686a21d81a670928d51ccc61e3d64e7d54661e6f`; the script rejects any
`tuttegen.py` whose SHA-256 differs from the value above.  No randomness,
floating-point arithmetic, solver, downloaded data, or private ledger input is
used.

## Literature and novelty boundary

The broad Albertson problem and the complement/matching background are
classical; Stehlík's primary 2003 theorem is
[`Critical graphs with connected complements`](https://doi.org/10.1016/S0095-8956(03)00069-8).
The recent primary preprint
[`Albertson's Conjecture for Chromatic Numbers at Most 29`](https://arxiv.org/abs/2609.04771)
already claims the full `r <= 29` result by a different order-58 barrier
argument.  Accordingly, h4221 is at most graph-level novelty within this
distinct lower-degree frontier, not literature priority for settling `r=29`.
The present review makes no judgment on that preprint's correctness.

## Strengthening and improvement opportunities

1. Keep two variables: an upper bound `cA_count` for inequality (1), and the
   actual `cA` (or a proved lower bound) for inequality (7).  Enumerate every
   compatible actual value rather than reusing the upper bound.
2. Enumerate or safely bound the actual `iso` value in the non-single-block
   branches.  Fixed representatives chosen to relax inequality (5) cannot be
   reused automatically in (7), where increasing `iso` weakens the test.
3. Rerun the full scan and publish entry-level differences.  A repaired proof
   may recover some or all seven rows if additional incidence structure forces
   more full components, but the local witness shows that the currently stated
   block facts alone do not do so.
