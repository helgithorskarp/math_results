# Critical co-gem/bull-free graphs

The new result is a sharp, uniform obstruction theorem for critical
**(P5,bull)-free** graphs. Every noncomplete graph G in this class contains

\[
P_4+(\alpha(G)-2)P_1.
\]

Thus, for every k>=1 and ell>=0, a k-vertex-critical (P5,bull)-free graph is
`(P4+ell P1)`-free **exactly when** its independence number is at most ell+1.
Its order is at most `(ell+1)(k-1)+1`. An explicit recursive construction
attains the independence bound for every ell, at specified chromatic numbers.
We do not claim the general order bound is optimal.

[proof.md](proof.md) proves a more general theorem for hereditary classes whose
nonperfect prime graphs have independence number at most two. Its application
uses the published structural theorem of Karthick–Maffray–Pastor (2019),
standard modular decomposition and perfect-graph replication. It does not
depend on an enumeration or an unchecked solver result. [literature.md](literature.md)
distinguishes the new deduction from its prior inputs.

## Relation to the open target

At ell=1, the theorem gives the **complete all-k, all-order identity**

\[
\operatorname{crit}_k(P_5,\mathrm{bull},P_4+P_1)
=\operatorname{crit}_k(P_3+P_1).
\]

The selected open question omits P5 on the left. That question remains open.
The proved identity makes it equivalent to showing that every vertex-critical
co-gem/bull-free graph is P5-free. We have not proved that exclusion, found a
counterexample, or bounded the order of P5-containing seven-critical candidates.

## Reproduce finite controls

Run from this directory, using Python 3.11+ and its standard library:

```sh
python3 controls.py
sha256sum -c SHA256SUMS
```

The program compares its complete deterministic output with `expected.json`.
It checks chromatic numbers by a general independent-set partition DP, all
vertex deletions, independence numbers, forbidden induced subgraphs, and the
largest independent set anticomplete to an induced P4.

| Constructed control | Vertices | Chromatic number | Independence number | Maximum isolated vertices beside P4 |
|---|---:|---:|---:|---:|
| T1 | 1 | 1 | 1 | No P4 |
| T2 | 5 | 3 | 2 | 0 |
| T3 | 17 | 8 | 3 | 1 |

All three are vertex-critical. T3 is **not co-gem-free**, and is not a
counterexample to the selected problem. Compact edge lists are in the expected
output. The program also checks all 1099 labeled graphs on 1–5 vertices and
the palette construction for odd demands from 1 through 99.

Two negative controls show why hypotheses matter. The join of C5 and an
independent triple is P5/bull/co-gem-free but is not critical; it has alpha=3
and no P4 with an anticomplete vertex. The Mycielski graph of C5 is critical
and bull-free but contains P5; its alpha is 5, while the largest such
anticomplete independent set has size 2 rather than 3.

These controls take about 0.2 seconds and 13 MiB on the recorded Python 3.11.2
environment. They test concrete consequences and necessity examples. The
arbitrary-order theorem and all-ell sharpness use the written induction.
This is unformalized mathematics without independent peer review.
