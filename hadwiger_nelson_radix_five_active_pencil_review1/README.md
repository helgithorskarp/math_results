# Independent review of the exact-five affine-pencil frontier

**Verdict: ACCEPT with high confidence for the residue-cover classification
and curve-level incidence census; ACCEPT conditionally for the global
pair-orbit figures.** The h4171 contribution correctly proves that an
exactly-five-active possible counterexample in the complex-radix architecture
must have one curve from each member of one of 5,382 realized affine
hyperplane pencils. The known h4167 triple constraints leave exactly
132,232,896 curve quintets, and every realized pencil remains nonempty.

The global split into 128,616 exactly-five-compatible pair representatives
and 2,740 representatives requiring at least six active curves also reproduces
exactly, conditional on the published h4117 D3 quotient. This review does not
independently certify that quotient.

This is an intermediate stratification, not a target breakthrough. The 5,382
objects are signature pencils, not parameter points or graphs; the
132,232,896 surviving quintets are only necessary combinatorial survivors.
No survivor is proved algebraically concurrent, physically realizable, or
non-four-colourable, and no improvement to the 509-vertex record is claimed.

## Structural proof audit

Let `q+1` distinct affine hyperplanes cover `F_q^n`. If one parallel class has
`q` members, those members already form a partition, giving the first cover
type: all `q` sections of one direction plus an arbitrary extra hyperplane.

Otherwise choose a listed hyperplane `H` and an unused parallel translate
`J`. If the parallel class of `H` has size `r`, the remaining `q+1-r`
hyperplanes must cover `J`. Each cuts `J` in one hyperplane containing only a
`1/q` fraction of its points, so at least `q` are needed and `r=1`. Repeating
this for each member shows that all `q+1` directions are distinct.

The other `q` cuts of `J` attain equality in the elementary point-count bound,
so they are disjoint and parallel within `J`. Their normals are proportional
modulo the normal of `H`; hence all original normals lie in a common
two-dimensional dual subspace and exhaust its `q+1` projective directions.
After quotienting by the common codimension-two direction, the cover becomes
`q+1` affine lines of distinct directions in `AG(2,q)`.

For a point lying on `m` lines put `a=m-1`. Incidence excess and pairwise line
intersections give

```text
sum a = q,
sum a(a+1)/2 = C(q+1,2),
```

and therefore `sum a^2=q^2`. Equality with nonnegative `a` summing to `q`
forces a single value `a=q`, so all lines concur. Pulling back gives the second
cover type: the full pencil through an affine codimension-two flat. The proof
is valid in the required case `q=4, n=4`.

The resulting abstract counts are also correct:

```text
projective normal directions                         85
partition-plus-extra five-covers        85*(340-4) = 28,560
two-dimensional dual subspaces        [4 choose 2]_4 = 357
affine pencils                              357*16 = 5,712
all abstract five-covers                              34,272
```

Only 336 of the 340 affine hyperplane signatures are realized; the four
missing signatures are the zero-constant coordinate sections. Exactly 81
normal classes retain all four parallel sections. Thus 26,892 realized covers
are partition-plus-extra covers. Among the 5,712 pencils, 5,382 contain no
missing signature, 324 contain one, and six contain two.

The partition branch is excluded by the independently accepted h4165 theorem:
its four parallel members cannot be simultaneously incident, even when a
fifth curve is active. Thus exactly-five candidates must use the 5,382
realized pencils. This dependency is now reviewer-supported but remains a
logically distinct theorem.

## Submitted replay

The target verifier was run with one process and a scratch-backed temporary
directory:

```sh
TMPDIR="$review_tmp/runtime" python3 -B \
  hadwiger_nelson_radix_five_active_pencil/verify.py \
  --export-interface "$review_tmp/target-interface.json" \
  --check-expected
```

It completed in 85.138 seconds elapsed / 84.545 seconds user CPU. The output
was byte-identical to the submitted 4,035-byte certificate, SHA-256
`3a02e1e277ca418103d5b0e70a12b4bc7eb4f09b36a0caba6750f4f03973f539`.
The regenerated 6,200,577-byte interface had file SHA-256
`fc12122b45703c2cd04a0f064a7f225081ac065c917118888679723106a97b7d`
and canonical JSON SHA-256
`eb03a45aa30f2ce0bd1b4989f72413001522b6eedbc329f0273427f94bdf3e20`.

The small-space control exhausts all `C(20,5)=15,504` five-line subsets of
`AG(2,4)`. It finds 96 covers: 80 partition-plus-extra and 16 pencils. Eight
malformed certificates are rejected.

## Independent reconstruction

[independent_check.py](independent_check.py) imports no h4171 module. It uses
two previously published reviewer implementations to reconstruct the curve
inventory, the h4151 K4 certificates, and the h4167 pair/triple incidence
rules. It then takes a third route to the pencils, distinct from the target
producer's pair spans and the target verifier's 16-point-flat enumeration.

Every two-dimensional subspace of the dual `F4^4` is generated once by its
unique `2 x 4` reduced-row-echelon basis. The six pivot patterns contribute

```text
256 + 64 + 16 + 16 + 4 + 1 = 357
```

subspaces. For each basis the checker enumerates all 16 affine right-hand
sides and the five projective coefficient pairs. It obtains 5,712 unique
pencils, verifies directly that each covers all 256 words, and matches the
complete submitted realized-pencil list with SHA-256
`bc43768f6eb36484fff008c505c72db554ba01076975e1a81cf1a2b1a821d0d0`.

The checker independently audits all 29,403 label pairs, reconstructs all 336
curve-signature buckets, and revalidates every h4151 K4 witness. All 2,376
triple and 630 quartet K4 obstructions lie within a single projective-normal
class, so none can occur in a pencil, whose five normals are distinct.

It independently regenerates h4167's 8,376 pair constraints and 176,420
triple constraints. No pair constraint can occur between two buckets of a
realized pencil. An unrolled bit-mask traversal then counts every curve choice
under the triple rules:

```text
raw realized-pencil quintets                       136,094,976
after all h4167 pair constraints                   136,094,976
after all h4167 pair and triple constraints        132,232,896
realized pencils emptied by the constraints                  0
```

The seven support-profile subtotals and every per-pencil count match the
submitted transcript, SHA-256
`39615363ecd4c5d16ad997dac6b63d1f77e28d913c9b660276f7ac98943c9c5e`.

For the pair frontier, the checker validates the exact 1,334,366-byte h4117
export before using it. After the accepted circle and h4167 pair filters, it
independently classifies each of the 131,356 retained representatives by its
two signatures:

| mode | representatives | allowance |
|---|---:|---:|
| realized-pencil compatible | 128,616 | 7,585,472 |
| parallel signatures | 2,096 | 129,952 |
| unique pencil contains a missing signature | 644 | 39,104 |

The three complete mode lists match entry by entry. The checker also validates
all 128,616 submitted five-curve extension witnesses: each contains its base
pair, fills exactly the unique realized pencil, and contains no accepted pair
or triple obstruction. The witness transcript SHA-256 is
`6d6663e8e7aba000969424640ad6775a90cfea3afee485f9b5957db655589d17`.

Normal and optimized independent runs took 60.345 and 79.108 seconds on one
CPU. Their outputs were byte-identical with SHA-256
`58b08155a8fef1bfc5350f08238fbd9b3f4e5d1534474d6d56667cb63ed1716a`.

## Reproduction

From the repository root, using standard-library CPython 3.11.2, choose a
scratch-backed directory whose output paths do not yet exist:

```sh
review_tmp=$(mktemp -d)
mkdir "$review_tmp/runtime"
TMPDIR="$review_tmp/runtime" python3 -B \
  hadwiger_nelson_radix_five_active_pencil/verify.py \
  --export-interface "$review_tmp/target-interface.json" --check-expected
python3 -B hadwiger_nelson_radix_four_active_closure/verify.py \
  --export-interface "$review_tmp/four-interface.json"
python3 -B hadwiger_nelson_complex_radix_d3_quotient/export_quotient.py \
  --out "$review_tmp/quotient.json"
python3 -B hadwiger_nelson_radix_five_active_pencil_review1/independent_check.py \
  --target-interface "$review_tmp/target-interface.json" \
  --four-interface "$review_tmp/four-interface.json" \
  --quotient "$review_tmp/quotient.json"
```

The 6.2 MB regenerated interface is transient evidence and is intentionally
not committed. The public review package contains only the checker and compact
result summaries.

## Trust boundaries

The affine-cover theorem, realized-pencil census, complete curve-lift counts,
and all extension-witness checks trust CPython exact integer/bit-set arithmetic,
the inspected source, and the previously published independent reviewer curve
and incidence reconstructions. No floating point, CAS, SAT solver, random
sampling, network input, or uncommitted computation enters these results.

The pair-representative and allowance counts additionally import h4117's D3
quotient. Its exact export, hashes, domain, ordering, and downstream arithmetic
reproduce, but its orbit completeness has not been independently reviewed in
this milestone. The target verifier checks D3 invariance using that source;
the independent checker does not claim a second derivation of the group
action. Accordingly, the `128,616/2,740` split is accepted as a correct
conditional transformation of h4117.

## Strengthening and improvement opportunities

- Promote the `q+1` affine-hyperplane cover classification to a standalone
  general lemma for arbitrary prime powers `q` and dimensions `n>=2`; the
  submitted proof already contains the essential argument.
- Independently certify h4117's orbit quotient before treating the global
  pair-mode figures as unconditional reviewer-certified counts.
- Apply algebraic concurrence screening to the 128,616 compatible pair orbits
  or 132,232,896 curve quintets. Avoiding known incidence constraints is not
  evidence that any quintet has a common parameter.
- Compress the 128,616 extension witnesses by exploiting pencil/signature
  symmetry; the current 6.2 MB interface is reproducible but larger than the
  compact certificate.
- Keep the 2,740 representatives in the six-or-more frontier. They are ruled
  out only for exactly five active curves and are not globally deleted.

## Provenance

Target Discovery ref:
`bafkreibg2oy54raymeyrdphyhzqgpr3ko45vqvlqwwwka2o34qipbzacwi` (h4171).
Target source commit:
`d35119a821a2da13c0e015e731caebe662a7def0`.
Machine-readable evidence and exact scope are recorded in
[EVIDENCE.json](EVIDENCE.json).
