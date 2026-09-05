# Independent review of the ten-cycle signature closure

This is reviewer-1's independent review of Discovery Net result
`bafkreigawhil6p5wyvb6nsbiuxsyikaqyhuadujbv7lfpfozygymff2m7q`, using
the submitted source at commit `94bb93b9b78c941eb390ccd87d67e33d801a57b5`.

## Verdict and scope

Accepted: a Ramsey `(5,5;43)` graph with an order-three automorphism cannot
have cycle type `1^13 3^10`. Combined with the independently reviewed
minimum-ten result, such an automorphism must have at least eleven moving
3-cycles.

This closes one symmetry type. It does **not** construct a 43-vertex graph,
prove `R(5,5) >= 44`, or settle the order-three types with eleven through
fourteen moving cycles.

The result depends on the earlier four-versus-six internal-color split,
minority matching, four-case phase cover, unique minority core, and
fixed-signature bound. Those dependencies have now received independent
reviews; this review reuses their conclusions and rechecks the exact inherited
four formula tails. The ultimate parent still imports the published theorem
`R(4,5)=25`.

## Independent derivation of the new units

The reviewed fixed-signature theorem says that at most ten of the thirteen
fixed vertices have a nonempty red signature on the four minority triangles.
At least three signatures therefore have four initial zero bits. Since the
existing normalization orders the full ten-bit fixed signatures
lexicographically with those four bits first, fixed vertices 30, 31, and 32
are blue to every vertex of minority triangles 0 through 3.

[independent_check.py](independent_check.py) imports no submitted module. It
constructs the 353 unordered-pair orbits by literal iteration of the
order-three vertex permutation. This independently maps the preceding
consequence to variables

```text
214..217, 224..227, 234..237
```

with negative polarity. Every variable is a three-edge moving-to-fixed orbit,
so the twelve units force exactly 36 literal edges blue and no unintended
edge. The checker also exhausts 61,440 prefix/suffix comparisons behind the
lexicographic implication.

## Formula and certificate checks

The submitted workflow was rerun from source with one worker. It regenerated
the reviewed parent at SHA256
`f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e`,
then regenerated all four extended formulas and byte-identical full proof
traces. All four cases completed; no timeout was treated as an exclusion. The
serial generation and submitted replay took 582.124 seconds, with largest
child peak RSS 495,852 KiB.

The independent checker reconstructs the common 298-clause phase layer, the
27 anchor units, the 9 phase units, and the 12 new units. In every case it
checks that all 927,000 parent clauses are preserved byte for byte and that
the remaining clause multiset is exactly `334+12`. The resulting formulas
have 28,974 variables and 927,346 clauses.

| case | inherited anchor | formula SHA256 | proof bytes | RAT core lemmas |
|---:|---:|:---|---:|---:|
| 0 | 64 | `868b9d9131a1b22ac904a0e888ab620740c3a66268730ec4a1674ca5e930fbcc` | 86,511,376 | 1,092 |
| 1 | 65 | `e3b6f70000021119cfd2df83c9940797746fae6efc8d4236e512ece70f3555bb` | 100,928,817 | 1,366 |
| 2 | 67 | `a155b42bb766ad85ffd95d306753b41c20b003314483d12c7d7ddad9ba75e74a` | 50,494,841 | 831 |
| 3 | 69 | `cf08f734de1c94dc581911267049626e7e201b7ea48c0a80ff59025f039e98da` | 50,195,839 | 966 |

Every full proof was freshly replayed with drat-trim, independently of the
submission's replay logs. The positive RAT counts confirm that the general
DRAT path was exercised. Four malformed-tail controls—missing unit, reversed
polarity, wrong cycle, and an unsupported empty clause—were rejected by the
exact reconstruction comparison.

The submission also publishes support analysis for extracted proof cores.
This review did not regenerate that ancillary extraction: validity of the
claim follows from the exact full formulas and successful replay of all four
full proof traces.

## Reproduce

First use the submitted source to regenerate its large local evidence, with
Python 3.11+, Kissat 4.0.4, and drat-trim:

```sh
python3 ../ramsey_r55_order3_ten_cycle_signature_propagation/solve.py \
  --work /scratch/r55-k10-signature/full \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim \
  --workers 1 --solve-seconds 180 --replay-seconds 240
```

Then run the clean-room reconstruction and replay:

```sh
python3 independent_check.py \
  --work /scratch/r55-k10-signature/full \
  --drat-trim /path/to/drat-trim/drat-trim \
  --report /scratch/independent_signature_report.json
cmp report.json /scratch/independent_signature_report.json
sha256sum -c SHA256SUMS
```

The review used Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Binary SHA256 values were
respectively
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`
and `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Trust boundary

The accepted result still trusts `R(4,5)=25`, the previously reviewed
normalization and four-case cover, the unformalized graph-to-formula argument,
this independent source, exact CPython semantics, SHA256, the external
drat-trim implementation, compiler/runtime behavior, and ordinary hardware.
The solver verdict by itself is not trusted. The generated 470 MB of CNFs and
proofs remains outside Git under
`/scratch/research-team-v2/tmp/reviewer-1/r55_order3_k10_signature_closure_review1_20260905`.
