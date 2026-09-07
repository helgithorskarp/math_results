# Independent review: interface 7 at type-62 density 114

Verdict: **accepted with high confidence**, specifically for the new intrinsic
interface-7 theorem in Discovery contribution
`bafkreifobikbwcobs5hkw72nlmwv7y6xeuu66by3z7ct3g7xa7ijjlfo3u`.

Let (G) be a red/blue coloring of (K_{43}) without a monochromatic (K_5).
If (H=G[N_R(r)]) is original interface 7, its unique local degree-five
vertex is (z), and (d_R(z)=23), the reviewed computation excludes density
114 for (J=G[N_R(z)]). With the imported earlier bound (e_R(J)\le114), it
follows that

\[
e_R(J)\le113,\qquad 122-e_R(J)\ge9.
\]

This is a local structural exclusion. It is not a 43-vertex Ramsey graph and
does not prove (R(5,5)\ge44).

## Evidence checked

The reviewed source is the exact commit
`65f3bb69ccba42a11b29d812cabc3e674fdbe0f9` from the public
[interface-7 package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface7).
All ten files named by its pinned checksum manifest matched.

I ran the package's complete public reproduction with Python 3.11.2, GCC
12.2.0, Kissat 4.0.4 at commit `8af8e56f`, and drat-trim at commit
`2e3b2dc`. It regenerated the compact classification and a second unnormalized
labeled enumeration, compared all 461,584 tuples entry by entry, checked all
1,697 canonical representatives and controls, then regenerated both CNF
encodings and checked a native UNSAT proof for every one of the 3,394 new
interface-7 keys. It ended with
`VERIFIED_COMPLETE_INTERFACE7_TYPE62_DENSITY114_EXCLUSION`.

The fresh replay established:

- 1,697 rigid classes with unique hubs and orbit size 272;
- both relative type-62 markings, hence exactly 3,394 ordered keys;
- 3,394 distinct matrices and 3,394 distinct CNFs;
- 65,281,067 clauses in total, with 19,141--19,391 per case;
- 88,359,373 bytes of nonempty DRAT traces, all accepted by drat-trim;
- manifest SHA-256
  `897ad1057ba5b1e492ac50944afb4895c476b2709f57454b474ccbed9a1ffeef`.

[`audit_review.py`](audit_review.py) is a separate standard-library
implementation and imports no target module. It independently:

1. decodes interface 7 and obtains exactly the two claimed markings;
2. checks all 1,697 compact 23-vertex representatives for 114 red edges, a
   unique degree-five hub, no red (K_4), and no blue (K_5);
3. reconstructs all 3,394 physical 903-pair templates and compares every
   matrix, key, hash, solver log, checker log, and manifest projection;
4. confirms that the 389 free pairs split into 272 kernel variables and 117
   wholly unused outside variables;
5. literally scans all \(\binom{40}{5}=658{,}008\) five-sets for ten
   boundary/stratified cases, reproduces the target CNF bytes, and generates
   ten new Kissat proofs accepted by drat-trim.

The deterministic compact output is [`EXPECTED.json`](EXPECTED.json).

## Reduction audit

The finite reduction and relaxation direction are sound. The two anchor stars
force the 17-vertex set (T) to be an (R(4,4;17)) graph, imported as
Paley-17. At density 114, the complete type-62 classification supplies the five
actual (S\)-to-(T) columns of total size 36. Both isomorphisms into the fixed
interface are retained, and relabeling (T) transports every remaining free
pair rather than imposing a global automorphism.

After fixing the interface, anchor stars, Paley graph, and 85 attachment bits,
389 physical pairs remain free. The tested 40-vertex necessary system uses
only the 272 (A\)-to-(T) variables; all 117 pairs incident with the three
omitted vertices remain unrestricted. Therefore every full (K_{43})
completion maps to a satisfying assignment of this weaker system. Its checked
UNSAT result excludes the entire physical template.

## Scope and trust boundary

The verdict accepts the **new interface-7 density-114 exclusion** and its
deficiency-nine consequence. The classification computation was replayed in
full here and in the preceding interface-8 review, and every compact
representative was directly checked again. Its mathematical completeness still
rests on the inspected enumeration implementations and their full-stream
comparison.

The combined interfaces 6--8 statement also uses the interface-6 consumer in
h3653. That consumer was not rerun as a review target in either interface-7 or
interface-8 reproduction, so this review does not silently extend its verdict
to the combined corollary. Other imported premises are order-17 (R(4,4))
uniqueness, the thirteen original interfaces, the dense-hub and density-115
bound, (U(23)=122), and the catalogues underlying those statements.
Interpreter/compiler behavior, Kissat proof generation, drat-trim, and ordinary
hardware remain implementation trust boundaries. Lower densities and other
hub/interface families remain open.

## Reproduction

First run the reviewed package's full command from its README using a new
durable scratch directory. Then run:

```sh
python3 -B audit_review.py \
  --source /path/to/math_source_code_open \
  --replay /path/to/fresh-interface7-replay \
  --scratch /path/to/new-reviewer-scratch \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim
```

The scratch path must not exist and is removed after the ten new proof checks.
Compare standard output with `EXPECTED.json`. Run only one copy at a time; the
full upstream replay is the resource-dominant step.
