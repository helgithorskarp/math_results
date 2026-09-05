# The degree-seven pool plus point 610 is closed through 508 vertices

**Theorem.** Let H be the strict unit-distance graph on the original Parts
509 points, all 76 first-level completion points having at least seven
original unit neighbours, and the one additional point

    q = (-(5+sqrt(33))/12, (5*sqrt(3)-sqrt(11))/12), label 610.

Every subgraph of H on at most 508 vertices is four-colourable. The minimum
order of a five-chromatic subgraph of H is **exactly 509**, attained by the
original Parts graph. H has 586 vertices and 3,089 strict unit edges.

This completes the [previous single-point extension reduction](../hadwiger_nelson_parts509_degree7_extension610/README.md).
It is a negative family closure, not a record improvement or a closure of
the whole degree-six completion pool. It also closes every deletion/addition
choice from this support with more original deletions than additions.
The earlier sealed-pool closures keep original vertices 0 through 373
fixed. This family permits deleting them, and its final residual omits
15 and 23, so that earlier fixed-component scope does not close this case.

## A four-set proof of the remaining case

Use the original labels V={0,...,508} and P={509,...,584}. The published
reduction proved that any possible non-four-colourable subgraph on at most
508 vertices must have exactly 508 vertices, include q, omit original
vertices 15 and 23, and contain **exactly three members of P**. It must meet
every retained killing set: D is a killing set when H minus D has a verified
proper four-colouring.

Four such sets already suffice. Row numbers below are zero-based indices
in the original `certificate_D7.json` family; all four lift to H.

| Row | Verified killing set D | Requirement when 15 and 23 are omitted |
|---|---|---|
| 278 | {23,509,522,528} | select from {509,522,528} |
| 392 | {23,515,518} | select from {515,518} |
| 411 | {15,533} | select 533 |
| 418 | {15,519} | select 519 |

The four required subsets of P are nonempty and pairwise disjoint. Meeting
all four needs at least four members of P, contradicting the required three.
This closes the last residual. The Parts graph supplies the matching upper
bound 509. No SAT encoding is needed for this final combinatorial inference.

The imported reduction used 451 forced vertices, 424 lifted killing sets,
and the earlier degree-seven hitting bound: a set hitting all 425 old killing
sets and containing at least four old pool points has size at least 58.
The present verifier replays the exact geometry and all 875 positive
colourings from the extension package, then checks the four displayed sets
and their disjointness directly. The earlier pseudo-Boolean theorem and
small-augmentation closures remain explicit dependencies; their large
proofs are not rerun here. See the [earlier full proof](../hadwiger_nelson_parts509_degree7_extension610/PROOF.md)
for the reduction, its hypotheses, and the exact counter encoding.

## An additional 19-byte certificate

The previous residual CNF has 1,038 variables and 3,774 clauses, SHA-256

    4c72e503e2c302863589bd35e1b8418e4a5f776dc6267fcca556befbd33a6d8f

One bounded Kissat run returned UNSAT in 0.00781 seconds. drat-trim verified
the complete 11,688-byte binary DRAT in 0.0973 seconds. Its core had 99 input
clauses, three derived clauses and no RAT-only steps. Trimming, then removing
deletions, gives the complete addition-only proof in `residual.rup`:

```text
-771 776 0
771 0
0
```

This file has 19 bytes including its three newlines; SHA-256:

    da1b366b28caffde7940b3248705d3ab302ef5c1a0bbddb034d72a833c7679a3

Each addition follows by reverse unit propagation (RUP): negate its literals
and repeatedly apply unit clauses until a contradiction appears. Such a
clause is entailed by the current formula. Adding the empty clause proves
unsatisfiability. The small pure-Python checker in `rup.py` implements exactly
this rule. It and drat-trim in RUP-only mode both accept the 19-byte proof.
The four-set argument above checks the contradiction independently of the
threshold variables and proof representation.

## Reproduce

In a complete repository checkout, from this directory with Python 3.11 or
later and only the standard library:

```bash
python3 verify.py
python3 controls.py
sha256sum -c SHA256SUMS
```

`verify.py` checks all pinned inputs, exact geometry, all 875 positive
witnesses, the four-set proof, the residual CNF hash, and the three RUP
additions. Expected output is in `expected.json`. The controls compare RUP
implications with truth tables for all 512 formulas over the nine canonical
clauses on two variables (4,608 clause checks), plus explicit valid and
invalid/incomplete proof fixtures. Results are in `controls_expected.json`.

An optional external replay uses drat-trim; no new SAT search is required:

```bash
closure_work=$(mktemp -d)
python3 verify.py --cnf-out "$closure_work/residual.cnf" \
  --drat-trim "$(command -v drat-trim)"
```

To regenerate the native proof, with Kissat and drat-trim on PATH, continue:

```bash
python3 ../hadwiger_nelson_parts509_degree7_extension610/run_native.py residual \
  --work "$closure_work" --solver "$(command -v kissat)" \
  --checker "$(command -v drat-trim)" --seconds 300
drat-trim "$closure_work/residual.cnf" "$closure_work/residual.drat" \
  -l "$closure_work/trimmed.drat"
python3 extract_rup.py --cnf "$closure_work/residual.cnf" \
  --trimmed "$closure_work/trimmed.drat" --out "$closure_work/regenerated.rup"
```

The run used Kissat 4.0.4, source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, one native worker, a 4 GiB
address-space limit, and a 300-second upper time limit. Tool hashes and
measured results are in `measurement.json`. Only the 19-byte text proof and
compact four-set certificate are committed; native traces and verbose logs
remain local. A different solver build may produce a different valid proof.

The imported degree-seven cutting-planes proof was checked in its original
publication and was not rechecked this pass. New geometry and positive
evidence are replayed directly; the new residual conclusion does not require
trusting a native SAT solver. The geometric reduction and checker correctness
are ordinary mathematical/code arguments, not a proof-assistant formalization.

The source dependency is Discovery Net
`bafkreig5j7ai5z3qqaemmh2qgqfukoekxhyhnoux7ki623hcrj6rodqsfe`, source commit
`44fcb922c03d65b3f0b1468a069da10c0f5a24a3`. No candidate graph or new support
was queried after the selector refutation. This support's <=508 search is
finished; any further augmentation is a separate milestone.
