# Independent review: two empty fixed signatures

## Verdict

**Accepted, with the stated intermediate scope.** In the three-versus-eight
branch of an order-three action of type `1^10 3^11` on a hypothetical Ramsey
`(5,5;43)` graph, at least two of the ten fixed vertices are blue to all nine
vertices in the three internally red moving triangles.

This conclusion imports the previously accepted parent formula, fourteen-core
cover, and sharp signature reduction. It does not exclude either surviving
minority core: the class-11 and class-13 branches with at least two empty
signatures remain open. The four-versus-seven branch is also open. No
43-vertex target graph or improvement of the lower bound for `R(5,5)` follows.

The reviewed Discovery Net contribution is
`bafkreiehgdsqcps5lzvuqrv6j4vmvub5fxbocm3ib3htgcobp4khx4sjjq`. The source
directory is unchanged from commit
`632619d72b6cfc4f0ade808524c319df302f1ef7`.

## Completeness of the split

Let `z` count fixed vertices with empty red signature on the three minority
triangles. The accepted sharp signature lemma gives `z>=1`. If `z=1`, its
equality case uniquely fixes the multiset to one empty signature, two of each
singleton, one of each pair, and no triple.

The parent orders each fixed vertex's complete eleven-bit attachment row
lexicographically, with the three minority bits first. Sorting the equality
multiset as bit tuples therefore gives

```text
000,001,001,010,010,011,100,100,101,110.
```

Because numeric mask bit `i` represents the attachment to triangle `i`, the
corresponding mask order is `[0,4,4,2,2,6,1,1,5,3]`, not increasing numeric
order. The base already fixes vertex 33 to `000`. The equality branch appends
the remaining 27 prefix units, while the other branch appends
`-222,-223,-224`, fixing vertex 34 to `000`. They are disjoint on variable
224 and, given `z>=1`, are exactly the cases `z=1` and `z>=2`. No
fixed-to-fixed edge or remaining attachment bit is fixed.

## Independent evidence

[independent_check.py](independent_check.py) imports no module from the
reviewed contribution. It reconstructs all 320 primary edge orbits and derives
the prefix units from bit tuples. A stars-and-bars check of all 19,448
signature profiles finds:

- 928 satisfying the basic incidence and singleton bounds;
- exactly one `z=1` profile and 927 `z>=2` profiles;
- after all inherited four-vertex cuts, exactly `1 + 777` profiles;
- the unique equality vector `(1,2,2,1,2,1,1,0)` in mask order.

The two submitted signature bases are byte-identical to the exact instances
used in the accepted preceding review. Every final CNF is that complete
617,204-clause base after its changed header, followed only by the expected 27
or 3 units:

| case | clauses | SHA-256 | result |
|:---|---:|:---|:---|
| `c11_one` | 617,231 | `66a189985febad0f8e08e988cc79aef498a740cf37cfbdf99c7956248a9a5c5d` | independently refuted |
| `c11_many` | 617,207 | `ec5b3113a2a1bb845cf0d22857aa728c937eb629e2730a0d47ba69413a32b96d` | open |
| `c13_one` | 617,231 | `e6fa2416d82fecdfbf09b26c1bd81639bd7d97cea248bae8d33661b474223477` | independently refuted |
| `c13_many` | 617,207 | `57e6219d14e7eefd43881657cfac7d3c06b79127095ced6dee1df257e2d0f99e` | open |

The class-11 equality proof has 11,698,808 bytes and SHA-256
`1cb1b979acbcac3f377cbcde81cd4b2dc781383e8356a99b017fb841b6cb5160`.
The class-13 proof has 11,651,203 bytes and SHA-256
`e3876f1d2a86fe86b30c6106cacb23ea4b3a24ea2c2422c4c4d9fb5b77291d61`.
Serial drat-trim replay returned `s VERIFIED` for both, exercising respectively
86 and 89 RAT core lemmas. [report.json](report.json) records the deterministic
review result. The submitted `UNKNOWN` outcomes for the two many-empty cases
are not certificates and are not used to prove feasibility.

## Reproduction

Retain or regenerate both external proof workspaces, then run from the
repository root with one checker process:

```sh
python3 -B ramsey_r55_order3_eleven_empty_split_review1/independent_check.py \
  --proof-work /scratch/team-r55-1-k11-empty-split/full \
  --reviewed-signature-work /scratch/team-r55-1-k11-signatures/full \
  --drat-trim /path/to/drat-trim \
  --work /scratch/r55-k11-empty-review1 \
  --report /scratch/r55-k11-empty-review1/report.json
python3 -c 'import json,sys; assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2]))' \
  ramsey_r55_order3_eleven_empty_split_review1/report.json \
  /scratch/r55-k11-empty-review1/report.json
cd ramsey_r55_order3_eleven_empty_split_review1
sha256sum -c SHA256SUMS
```

The replay used drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` and binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Kissat is needed only to regenerate proof traces, not to verify this review.

## Trust boundary

The split and row ordering were re-derived independently, and every new unit
and both new proof traces were checked. The conclusion still imports the
accepted parent-formula, core-cover, and signature-reduction reviews, including
the parent normalization, SAT reduction, and external `R(4,5)=25` degree
window. Remaining trust lies in ordinary unformalized reduction arguments,
CPython/runtime/hardware, SHA-256, and the external drat-trim implementation.
This is not a proof-assistant formalization.

The approximately 25 MB formulas and 23.4 MB of successful traces remain
outside Git. Compact hashes alone are not refutations. Reviewer state and logs
are under
`/scratch/research-team-v2/tmp/reviewer-1/r55_k11_empty_split_review1_full`;
no reviewer-owned proof process remains active.
