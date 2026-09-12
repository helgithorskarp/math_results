# Finitely many critical co-gem/bull-free graphs for each k

For every `k>=1`, there are only finitely many `k`-vertex-critical
`(co-gem,bull)`-free graphs. This covers arbitrary orders and the entire
`P5`-containing residual left by the previous two contributions.

The [proof](proof.md) combines our earlier unrestricted
[critical C6 exclusion](../prism_reduction/proof.md) with **Beaton--Cameron's
known Theorem 3.9 (2026)**, specialized to co-gem and `C6`. It also gives
a direct effective bound

\[
 |V(G)|\le k\bigl(N(10k+5)-1\bigr),
\]

where the constructive CKOS prime-graph Ramsey threshold `N` is specified
in full in the proof. The direct bound holds even for the larger class
of critical `(co-gem,C6)`-free graphs. We claim no novelty for the prior
finiteness of that larger class or for the imported Ramsey estimates.

This answers the **bull case of the finiteness question** in Section 7 of
Beaton--Cameron (2025). It does **not** prove the stronger all-k equality
with the critical `(P3+P1)`-free class, nor execute the unrestricted `k=7`
classification. The huge Ramsey bound is not a practical census limit.
See [literature and scope](literature.md) for the primary-source trail.

The lane is parked after its three contracted mathematical passes. The
combined package is preserved for standalone publication consideration.

Reproduce the finite controls with CPython 3.11 or later, standard library
only, from this directory:

```sh
python3 controls.py
sha256sum -c SHA256SUMS
```

Expected: `status: PASS`, 120 family-orientation checks, 8190 binary chain
words through length 12, all their specified witnesses, and four critical
examples plus two counterexamples to dropping module hypotheses.
`python3 controls.py --emit` emits the fresh JSON without comparing it to
`expected.json`. The controls took about 0.3 seconds on the development
machine. They are not an exhaustive critical-graph census or the universal
proof.

The [prior certificate checker](../prism_reduction/check.py) remains the
replay entry point for the complete local certificate used in the critical
`C6` exclusion. Its certificate SHA-256 is
`781d4bbbfc3f947c2a2b69ef4dd07ac749f04710194982e5df047744150adf88`.
No prior source or certificate was altered for this contribution.

Trust: an ordinary written deduction and order-bound proof, importing
published structural theorems and the earlier computer-assisted exclusion.
No proof-assistant formalization or independent peer review is claimed.
No large search output or new solver evidence is required.
