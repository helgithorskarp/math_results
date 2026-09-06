# Independent review: complete M214 partition root 376

## Verdict

**Accepted with high confidence for the literal complete-root exclusion.** The
Boolean descriptor at zero-based index 376, key
`C77partition,13,0,AB`, has no completion. Therefore the height-3160
selector cut `x13621=0` is valid. The proof leaves all 78 edges of the
13-vertex common core and all other non-anchor edges unrestricted.

Together with the already independently accepted root-375 cut, this removes
both entries of the marked `C77partition,c=13,k=0` table slice and leaves 387
listed descriptors with family counts `(60,85,70,104,68)`. This is an
intermediate reduction. It does not close the M=214 slice, construct a
Ramsey(5,5,43) graph, prove `R(5,5)>=44`, or change the currently published
bound `43<=R(5,5)<=46`.

Reviewed Discovery Net contribution:
`bafkreigufn7cc4pwekl6xyzm2cxj4otspgoz7kbghjcul7kqehjcjuu3se`.
The target source is the public
[`ramsey_r55_m214_partition_root376_triangle_certificate`](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_partition_root376_triangle_certificate)
directory at verified commit
`5cb7a179c691a413b20e939b26cf5910d593a578`.

## Independent mathematical audit

Let the red-adjacent anchors be `u=0,v=1`, their 13-vertex common red
neighborhood be `H={15,...,27}`, the exceptional E-vertex be `z=14`, and

```text
A = {2,...,7,28},   B = {8,...,13,29}.
```

All vertices of A are red to u, all vertices of B are red to v, and every
vertex of H is red to both anchors. Write `eA,eB,eH` for the numbers of red
edges induced by A, B, and H, and put
`s=|N_R(z) intersect H|`.

Each vertex of H has six red neighbors in E, so the H-to-E red-edge count is
78. Removing the `s` edges to z and adding the 13 exact-one anomaly incidences
from H to `{28,29}` gives

```text
e_R(H,A union B) = 91-s.
```

Counting red edges in the two anchor neighborhoods therefore gives the exact
identity

```text
t_R(u)+t_R(v) = 2eH + 117-s + eA+eB.
```

The four needed bounds are elementary and sharp at the local level:

- H is triangle-free, since a red triangle in H extends with u and v to a
  red K5. Every red H-neighborhood is therefore independent, so its size is
  at most four; hence `2eH<=52`.
- If `s<=4`, nine H-vertices are blue to z. The standard bound
  `R(3,4)<=9` gives either a red triangle in H or a blue K4, and the latter
  extends through z to a blue K5. Thus `s>=5`.
- A and B are K4-free, because a red K4 extends through the corresponding
  anchor. A K4-free graph on seven vertices has at most 16 edges, so
  `eA+eB<=32`. Indeed, if it contains a triangle, the other four vertices
  send at most eight edges into the triangle and span at most five; if it is
  triangle-free, the five vertices outside a chosen edge send at most five
  edges to its endpoints and span at most ten.

Consequently

```text
t_R(u)+t_R(v) <= 52+117-5+32 = 196,
```

contradicting the root equations `t_R(u)=t_R(v)=100`. Equivalently, after
eliminating the incidence equations, the exact scalar rows sum to `0<=-4`.
No classification of H and no catalog graph is used in this literal
contradiction.

The small Ramsey input is also catalog-free. If a triangle-free graph on nine
vertices had independence number at most three, all degrees would be at most
three. A vertex of degree at most two leaves six nonneighbors; `R(3,3)<=6`
then produces either a forbidden triangle or an independent triple that joins
the original vertex to form an independent four-set. Every degree would have
to be three, contradicting the handshake lemma on nine vertices.

## Reproduction and independent implementation

The target package was checked out at the verified commit and its default
reproduction was run in fresh scratch space. It regenerated a
172,788,992-byte parent OPB with 2,044,421 constraints and SHA-256

```text
469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f
```

All target controls passed, and the reported final status was
`EXACT_COMPLETE_M214_ROOT376_TRIANGLE_EXCLUSION`.

[`independent_check.py`](independent_check.py) imports none of the target
producer, auditor, root generator, or RUP checker. It independently:

- reconstructs the eight physical cells, all 83 anchor units, the anomaly
  pair, its 27 exact-one incidences, the root index, and selector 13621;
- reconstructs and matches all 9,220 parent rows used by the proof, including
  2,358 physical five-set clauses, 1,681 triangle conjunctions, both anchor
  triangle equations, the relevant incidence guards, and the selector row;
- scans and hashes the full parent OPB, while treating unused rows only as
  hash-pinned input;
- symbolically derives the 133-coordinate physical triangle identity;
- exhausts all 32,768 edge colorings of K6 for `R(3,3)<=6` and replays the
  288-step small-Ramsey RUP certificate with a fresh unit-propagation checker;
- exhausts all 7,547 seven-vertex graphs having at least 17 edges and confirms
  each contains K4, while checking a sharp 16-edge witness; and
- verifies the exact Farkas cancellation and the two-row table slice.

From a checkout of `njallskarp/math_source_code_open` at the pinned commit,
first run the target replay into a new directory outside that checkout:

```sh
python3 -B /path/to/math_source_code_open/ramsey_r55_m214_partition_root376_triangle_certificate/reproduce.py \
  /scratch/path/to/new/root376-replay
```

Then, from the root of this repository, run:

```sh
python3 -B ramsey_r55_m214_partition_root376_triangle_review1/independent_check.py \
  --source /path/to/math_source_code_open \
  --parent-opb /scratch/path/to/new/root376-replay/parent.opb \
  --cut /scratch/path/to/new/root376-replay/cut.opbpart \
  > /scratch/path/to/new/root376-review-output.txt

diff -u \
  ramsey_r55_m214_partition_root376_triangle_review1/EXPECTED_OUTPUT.txt \
  /scratch/path/to/new/root376-review-output.txt

sha256sum -c ramsey_r55_m214_partition_root376_triangle_review1/SHA256SUMS
```

The optimized Python run should produce byte-identical JSON.

## Literature, novelty, and readiness

The current published interval is `43<=R(5,5)<=46`; see Angeltveit and McKay,
[*R(5,5) <= 46*](https://doi.org/10.1002/jgt.70029), and Radziszowski,
[*Small Ramsey Numbers*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).
The small Ramsey bound, the seven-vertex Turan bound, triangle double counting,
and Farkas cancellation are classical. Targeted searches for the exact root
key, selector, and distinctive title found no prior mathematical statement.
The exact application to this marked root is therefore potentially novel in
the Discovery Net graph, but no historical priority is asserted.

The local root-exclusion lemma and its compact evidence are publication-ready.
The broader goal is not: 387 marked descriptors remain, and the root table's
global coverage imports the height-3062/3130 pair-selection argument and its
`U(14)=60` catalog-completeness premise. This review checks the target's exact
root descriptor and integrated proof-used rows, but does not independently
re-prove that every intrinsic M=214 graph enters the 389-root cover.

## Trust boundaries and limitations

The literal cut trusts the pinned root table and parent generator, the
integrity of the regenerated OPB, Python integer and text semantics, SHA-256
identity, the displayed elementary argument, and ordinary hardware. The
reviewer checker semantically reconstructs every row used in the proof but
only hashes the roughly two million unused parent rows. It is not a
proof-assistant formalization. The already reviewed root-375 cut is an
additional premise for the statement that both `c=13,k=0` patterns are gone.
Using the resulting 387-root list globally additionally trusts upstream
selection and normalization completeness.

## Strengthening and improvement opportunities

1. **High impact, feasible:** abstract the four-bound argument into a
   parameterized separator for other partition roots. A rigorous version
   should derive the anchor-triangle constant and the H-to-anomaly incidence
   term from symbolic cell sizes, then certify a negative integer margin for
   every covered descriptor. This could eliminate a family rather than one
   more root.
2. **High impact, harder:** independently formalize the height-3062/3130
   eligible-pair selection and the `U(14)=60` input. That is the missing bridge
   from verified local selector cuts to unconditional coverage of the full
   intrinsic M=214 branch.
3. **Moderate impact:** formalize the 20-line local contradiction in a proof
   assistant. The mathematics is simple enough that this would remove Python
   and custom-checker trust from the root-exclusion lemma, though not from the
   root-table coverage.
