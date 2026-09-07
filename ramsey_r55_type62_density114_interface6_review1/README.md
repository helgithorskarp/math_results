# Independent review: complete type-62 density-114 classification and interface 6

Verdict: **accepted with high confidence** for the coupled classification and
interface-6 consumer in Discovery contribution
`bafkreigr5bbfmyr7q4hl4fabtkyn3yudprp3gd5owctylda6gb3i66jdvm`.

The contribution classifies exactly 1,697 isomorphism classes of
(J\in\mathcal R(4,5;23)) having 114 red edges and a degree-five hub whose
neighborhood is type 62, then excludes both markings of every class at original
interface 6. Thus, under its imported premises, an interface-6 branch with
global hub degree 23 satisfies

\[
e_R(J)\le113,\qquad 122-e_R(J)\ge9.
\]

This is an intermediate local exclusion. It neither constructs a 43-vertex
Ramsey graph nor proves (R(5,5)\ge44).

## Full reproduction

The reviewed source is exact commit
`607d56027ae008e1b02ee1d351e8f9cf9757b752` from the public
[classification and interface-6 package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface6).
All 18 files in its checksum manifest matched.

I ran its complete public command with Python 3.11.2, GCC 12.2.0, Kissat 4.0.4
at commit `8af8e56f`, and drat-trim at commit `2e3b2dc`. The run regenerated
the compact certificate, produced a second full labeled enumeration without
the producer's affine normalization, compared all 461,584 tuple entries,
checked the group action and all representatives, ran definition-level
controls, then generated both encodings and checked a native proof for every
one of the 3,394 interface-6 keys. It ended with
`VERIFIED_TYPE62_DENSITY114_CLASSIFICATION_AND_INTERFACE6_EXCLUSION`.

The replay established:

- 1,697 rigid unique-hub classes, each with orbit size 272;
- 461,584 labeled tuples with stream SHA-256
  `84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8`;
- 3,394 distinct interface-6 matrices and 3,394 distinct CNFs;
- 65,215,510 clauses, with 19,126--19,340 per case;
- 152,151,217 bytes of nonempty DRAT traces, all accepted by drat-trim;
- ordered manifest SHA-256
  `3834410d2a6bd7793f1306db96a34cd6501e6aa39b389e1fd925df31e70b2506`.

## Independent audit

[`audit_review.py`](audit_review.py) imports no claimant module. To avoid three
copies of identical family-independent reviewer code, it hash-pins and loads
the earlier interface-7 reviewer implementation at SHA-256
`d81fa53b8d3b97a710eba27714fbf38f61afbdec1760fa9001ff53a5a00d33ed`.
That implementation uses a third graph6 decoder, bit-set clique decisions, a
direct symmetric physical construction, and literal five-set substitution.

The audit:

1. independently checks every compact representative for 114 red edges, a
   unique degree-five hub, no red (K_4), and no blue (K_5);
2. decodes interface 6 and recovers exactly its two type-62 markings;
3. reconstructs all 3,394 full 903-pair matrices and compares every retained
   matrix, key, hash, solver log, checker log, and manifest row;
4. verifies that all 389 free physical pairs remain variables, exactly 272
   (A\)-to-(T) pairs occur in clauses, and 117 outside pairs remain unused;
5. literally scans all \(\binom{40}{5}=658{,}008\) five-sets for ten
   boundary/stratified keys, reproduces their CNF bytes, and obtains ten new
   Kissat proofs accepted by drat-trim.

Normal and optimized audit runs match [`EXPECTED.json`](EXPECTED.json)
exactly.

## Mathematical audit

The four stated column conditions are necessary and sufficient. Since the
type-62 graph is triangle-free, has no independent four-set, and has the sole
independent triple 234, every forbidden red (K_4) or blue (K_5) in the
23-vertex graph is represented by a single-column, pair-column, or
triple-column condition. The hub adds no omitted forbidden configuration.
The density identity is

\[
e_R(J)=68+5+5+\sum_i|X_i|=78+\sum_i|X_i|,
\]

so density 114 is exactly column sum 36.

The classification's full 136-element Paley automorphism group and the two
type-62 automorphisms act on every labeled tuple. All 1,697 orbits have size
272, and their disjoint expansion agrees entry-by-entry with the independent
unnormalized enumeration. The unique hub forces every graph isomorphism to
preserve the hub and its (S/T) partition, so this product action captures the
complete isomorphism relation.

For the interface consumer, fixing the interface, anchor stars, Paley-17, and
85 attachment colors leaves 389 free pairs. The necessary 40-vertex subsystem
uses exactly 272 of them; the 117 pairs involving the three omitted vertices
remain wholly unrestricted. Every full 43-vertex completion therefore
restricts to a satisfying kernel assignment. The checked kernel contradictions
soundly exclude every completion of every marked template.

## Scope and trust boundary

This verdict accepts h3653's classification and interface-6 exclusion. Together
with the independent reviews of interface 7 and interface 8, all 10,182 marked
density-114 keys across original interfaces 6--8 are now independently
accepted. This combined statement remains subject to their common premises:
order-17 (R(4,4)) uniqueness, the thirteen-interface classification, the
dense-hub/density-115 exclusion, and (U(23)=122). The lower-density layers,
other interfaces, and other hub degrees remain open.

Completeness still trusts the inspected exact enumeration and group-action
programs, Python/compiler semantics, the native DRAT checker, and ordinary
hardware. The literal contradictions for fixed matrices do not require the
external graph catalogues; mapping every hypothetical intrinsic branch into
those matrices does.

## Reproduction

First run the reviewed package's complete command from its README using a new
durable scratch directory. From the root of a checkout containing this review
and the interface-7 review dependency, run:

```sh
python3 -B ramsey_r55_type62_density114_interface6_review1/audit_review.py \
  --source /path/to/math_source_code_open \
  --replay /path/to/fresh-interface6-replay \
  --scratch /path/to/new-reviewer-scratch \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim
```

The scratch path must not exist and is removed after the ten new proof checks.
Compare standard output with `EXPECTED.json`. Run one copy at a time; the full
upstream replay is the resource-dominant step.
