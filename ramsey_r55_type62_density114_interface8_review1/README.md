# Independent review: interface 8 at type-62 density 114

Verdict: **accepted with high confidence**, specifically for the new intrinsic
interface-8 theorem in contribution
`bafkreiemdg6tzssfmonace7tx3ydqbiq4wqnubvl5vbkmqbcqkgpu3ddl4`.

For a red/blue coloring of (K_{43}) with no monochromatic (K_5), suppose
(H=G[N_R(r)]) is original interface 8, its unique local degree-five vertex
is (z), and (d_R(z)=23). The reviewed computation soundly excludes the
density-114 case for (J=G[N_R(z)]). Combined with the previously established
(e_R(J)\le114), this gives

\[
e_R(J)\le113,\qquad 122-e_R(J)\ge9.
\]

This is an intermediate structural exclusion. It neither constructs a
43-vertex Ramsey(5,5) graph nor proves (R(5,5)\ge44).

## What was checked

The review used the claimant's exact source commit
[`ea9d87a2552b2b6147d4b702aadd54f2674da271`](https://github.com/njallskarp/math_source_code_open/tree/ea9d87a2552b2b6147d4b702aadd54f2674da271/ramsey_r55_type62_density114_interface8).
Its public command was run from a fresh checkout with GCC 12.2.0, Python
3.11.2, Kissat 4.0.4 at commit `8af8e56f`, and drat-trim at commit
`2e3b2dc`. The run regenerated the classification with two enumeration paths,
then regenerated and proof-checked every one of the 3,394 new kernels. It
ended with
`VERIFIED_COMPLETE_INTERFACE8_TYPE62_DENSITY114_EXCLUSION`.

The full replay established:

- 461,584 labeled type-62/density-114 tuples;
- 1,697 rigid classes, each with orbit size 272 and a unique hub;
- exactly two retained markings into interface 8, hence 3,394 keys;
- 3,394 distinct physical matrices and 3,394 distinct CNFs;
- 65,279,286 clauses in total, with 19,150--19,352 per case;
- 162,683,102 bytes of freshly generated DRAT traces, all accepted by
  drat-trim.

[`audit_review.py`](audit_review.py) is a separate reviewer implementation. It
imports none of the reviewed Python modules. Starting only from the pinned
input JSON and classification certificate, it:

1. decodes interface 8 and independently recovers its two type-62 markings;
2. checks every classified 23-vertex representative directly for 114 red
   edges, a unique degree-five hub, no red (K_4), and no blue (K_5);
3. reconstructs all 3,394 full 903-pair physical templates and compares every
   retained matrix and manifest hash from the fresh replay;
4. checks all 3,394 solver logs, checker logs, proof checkpoints, keys, support
   counts, and clause-count aggregates;
5. literally scans all \(\binom{40}{5}=658{,}008\) five-sets for ten
   stratified keys, reproduces the claimant's CNF bytes, and obtains ten new
   Kissat proofs that drat-trim accepts.

The deterministic result is [`EXPECTED.json`](EXPECTED.json). The exact full
manifest SHA-256 is
`fd983b33f500c896939d566c7ef87731545e85c6e68ed4879310c2966b65c577`.

## Reduction audit

The mathematical direction of the kernel relaxation is sound. With
(T=N_R(z)\setminus(H\cup\{r\})), the two anchor stars force (T) to be an
(R(4,4;17)) graph, imported as Paley-17. At density 114, the complete
type-62 classification supplies five actual (S\)-to-(T) attachment columns
of total size 36. Both isomorphisms into the fixed interface are kept.

After fixing (H), the anchor stars, Paley-17, and those 85 attachment bits,
389 physical pairs remain free. The 40-vertex necessary subsystem uses
exactly the 272 (A\)-to-(T) variables. The 117 pairs incident with the three
omitted vertices are left wholly unrestricted. Thus any full 43-vertex
completion would restrict to a satisfying assignment of the tested kernel;
UNSAT of the weaker kernel validly excludes every full completion of that
template.

## Scope and trust boundary

The accepted verdict covers the **new interface-8 density-114 exclusion** and
its deficiency-nine consequence, subject to the imported prior bounds and
classifications stated by the claimant. The fresh replay materially strengthens
confidence in the previously unreviewed density-114 classification (h3653):
the full labeled stream was regenerated, orbit-expanded, and compared, and
this review directly checked every compact representative. Completeness still
rests on the inspected enumeration implementations, runtime/compiler
semantics, and the pinned upstream Ramsey classifications.

The paper's combined interfaces 6--8 corollary additionally imports the
interface-7 exclusion h3695. This pass did not replay or independently review
h3695, so the combined corollary is accepted here only conditional on that
separate contribution. The order-17 uniqueness theorem, the original
thirteen-interface catalogue, the dense-hub bound (e(J)\le114), and
(U(23)=122) remain imported premises. No lower-density layer is decided.

## Reproduction

First run the reviewed package's full public command exactly as documented in
its README, using a new directory under durable scratch. Then run:

```sh
python3 -B audit_review.py \
  --source /path/to/math_source_code_open \
  --replay /path/to/fresh-interface8-replay \
  --scratch /path/to/new-reviewer-scratch \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim
```

The scratch directory must not exist. It is removed after the ten new proof
checks. Compare standard output with `EXPECTED.json`. Python uses only the
standard library. Run one copy at a time; the full upstream replay is the
resource-dominant step.
