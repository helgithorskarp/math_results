# A complete 72-state separator interface for the fixed H560 family

The accepted 560-vertex graph admits an exact decomposition with **19 mandatory
interface vertices**. Allowing arbitrary recolouring of the 374 mandatory
vertices in its large field block realizes **exactly 72 interface patterns**,
up to global permutation of four colours. Including all nine optional vertices
of that block leaves **exactly 20** of those patterns. Both exhaustions have
checked DRAT certificates, and all 92 positive witnesses are supplied.

This is a family decomposition and a successful feasibility test. It does not
close the H560 family or establish a five-chromatic graph on at most 508
vertices. The intermediate selector relations and the other block remain to
be computed. No subsequent phase has started.

## Exact graph and separator

Use the host labels and exact coordinates of the accepted
[H560/M492/U68 boundary](../hadwiger_nelson_heule632_minimize/boundary.json),
with its [independent acceptance](../hadwiger_nelson_heule560_family_review1/README.md).
Write its vertex set as `M` (492 mandatory vertices) and `U` (68 optional).
Every non-four-colourable subgraph of this fixed support contains `M`, by that
imported parent theorem. Here we do not repeat its deletion sweep.

Coordinates lie in the basis
`(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165))`
with common denominator 96. Let `L` be the retained points whose two
coordinates have zero coefficients in all four basis positions involving
`sqrt(5)`, and let `S = V \ L`. Exact norm tests on all 199,396 host pairs
recover 3,112 host edges and 2,758 retained edges. The field partition gives
`|L| = 383`, `|S| = 177`, and 33 cross-edges.

All their endpoints on the `L` side form

```text
Q = [0,333,334,335,336,337,338,339,340,341,342,343,344,
     466,467,468,469,470,471].
```

All 19 vertices of `Q` are mandatory, and `G[Q]` has no edges. The supplied
19 pairwise vertex-disjoint cross-edges prove that a vertex cover of the
cross-edge graph needs at least 19 vertices. The set `Q` is such a cover.
This is an exact minimum **for covering these cross-edges**; we do not claim a
globally minimum balanced separator or determine treewidth.

There is no edge between `L \ Q` and `S`. Thus the two blocks are `G[L]` and
`G[S union Q]`, intersecting in exactly `Q`:

| Block | Mandatory vertices | Optional vertices | Full vertices | Full edges |
| --- | ---: | ---: | ---: | ---: |
| `L` | 374 | 9 | 383 | 1,952 |
| `S union Q` | 137 | 59 | 196 | 806 |

The 19 shared vertices account for `383 + 196 - 19 = 560`; the edge sets are
disjoint because `Q` is independent. The mandatory block edge counts are
1,912 and 478, summing to the 2,390 mandatory edges.

The nine optional vertices on the large side are

```text
W = [310,510,512,513,520,521,523,524,535].
```

## Complete endpoint relations

Read the colours on `Q` in increasing host-label order and normalize by first
occurrence: the first colour is 0, the next previously unseen colour is 1,
and so on. This picks exactly one word from each global-palette orbit,
including colourings that use fewer than four colours on the interface.

For `A subseteq W`, let `P_A` be the normalized words on `Q` extendible to a
proper four-colouring of `G[(M intersect L) union A]`. The certificate proves

```text
|P_empty| = 72,       |P_W| = 20,       P_W subsetneq P_empty.
```

The sorted 19-character words, each followed by one newline, have SHA-256:

| Relation | Canonical stream SHA-256 |
| --- | --- |
| `P_empty` | `82f8316b103da3d84974c7d8084cdadcd463929041ac0d89a48bad99dcdbccd1` |
| `P_W` | `cc935bb2ef40ce9234545403061d98e7735e09543056c712cbb4c72ef661806f` |

Every row of [certificate.json](certificate.json) includes a complete proper
colouring of the corresponding block, in its listed vertex order. The checker
verifies all 176,704 positive edge inequalities. It compares the actual state
sets, including the strict inclusion, rather than relying only on their hashes.

For completeness, use four one-hot Boolean variables per vertex. Add one
at-least-one clause and six at-most-one clauses per vertex, and four inequality
clauses per edge. For the `i`-th interface vertex and each `c = 1,2,3`, add

```text
not x[Q[i],c] OR x[Q[0],c-1] OR ... OR x[Q[i-1],c-1].
```

These clauses say that colour `c-1` must occur earlier whenever colour `c`
occurs, exactly expressing first-occurrence normalization. There are no
additional triangle pins. Every proper block colouring can be globally
relabelled to satisfy these clauses, so no boundary orbit is lost.

For each listed word, append the clause excluding exactly that word on `Q`.
The resulting two formulas are UNSAT. Hence every normalized boundary word is
one of the supplied positive rows. This proves the two exact classifications
without trusting AllSAT search or assuming a restricted recolouring family.

| Block | Variables | Base clauses | With word exclusions | DRAT bytes |
| --- | ---: | ---: | ---: | ---: |
| Mandatory `L` | 1,496 | 10,323 | 10,395 | 1,948,302 |
| Full `L` | 1,532 | 10,546 | 10,566 | 1,380,935 |

CNF and proof identities are in [proof_manifest.json](proof_manifest.json).
Kissat returned UNSAT, and drat-trim returned exit 0 and the exact line
`s VERIFIED` for each formula. An independent reconstruction then matched both
CNFs byte for byte and checked both proofs again. Large proof traces and raw
solver logs stay local; the verifier can regenerate the proofs from the
public compact certificate.

## Whole-family gluing equivalence

For `B subseteq U intersect S`, let `R_B` be the normalized boundary words
extendible to `G[(M intersect S) union Q union B]`. For every pair of selector
sets `A subseteq W` and `B subseteq U intersect S`,

```text
G[M union A union B] is four-colourable
    if and only if P_A intersect R_B is nonempty.
```

To prove the forward implication, restrict a proper colouring to both blocks
and normalize its common boundary. For the reverse implication, choose block
colourings with the same normalized word and paste them on `Q`. There are no
edges between their disjoint interiors. This accounts for arbitrary interior
recolourings on both sides.

Monotonicity gives `P_W subseteq P_A subseteq P_empty` for all 512 left
selector masks. Thus the 20 full-block states are always available, and only
the other 52 states can depend on the left selectors. The target within this
accepted support is equivalent to finding `A,B` with `|A|+|B| <= 16` and an
empty intersection. The parent's five-colouring supplies the upper bound for
any such subgraph; a new lower-bound certificate is still required for a
candidate. This pass does not evaluate that selector problem.

An unconstrained independent set of 19 vertices has
`(4^19 + 6*2^19 + 8)/24 = 11,453,377,195` colour orbits, by counting fixed maps
for the identity, six transpositions and eight 3-cycles of the palette group.
The exact realizable relation of the mandatory large block has only 72 states.
This supplies a materially different frontier from fixed-colouring or
one-pair Kempe templates, which do not enumerate arbitrary interior
recolourings. It does not imply that the remaining 59-selector problem is easy.

## Frozen pilot and next boundary

[plan.json](plan.json) was frozen before either AllSAT run. Each endpoint
enumeration was limited to 32,768 states, 120 seconds in total, and 200,000
conflicts/10 seconds per query. The full-block endpoint was permitted only
after checked exhaustion of the mandatory endpoint. The native proof limits
were two million conflicts and 120 seconds per endpoint, with a 135-second
outer timeout. Both enumerations finished in under two seconds; the first
proof generation and checking took about 2.20 and 1.80 seconds respectively.

The decision is **go for a separately bounded selector-relation phase**.
The concrete next unit is the complete 72-by-512 left-block relation, using
the 20 always-available states and monotonicity to reduce its work. It can be
represented by exact minimal forbidden selector sets for each of the other
52 states, with positive witnesses and independently checked negative
certificates. That phase has not begun. The right-block selector mechanism
must be assessed separately before a whole-family solver campaign.

No additional 508-support census was performed. The previous
[Kempe classification](../hadwiger_nelson_heule560_kempe/README.md) and its
[new independent acceptance](../hadwiger_nelson_heule560_kempe_review1/README.md)
remain valid, including the 60,151,956,198,234 supports outside that restricted
certificate. The later [503-vertex four-colouring](../hadwiger_nelson_heule503_endpoint/README.md)
is context, not a premise of this new boundary classification. The teammate's
[paired-circle incidence reduction](../hadwiger_nelson_paired_circle_incidence/README.md)
was inspected as coordination context and remains a separate construction direction.

## Reproduce and trust boundary

From the repository root, use Python 3.11 or later, Kissat, and drat-trim:

```sh
python3 -B hadwiger_nelson_heule560_separator/verify.py \
  --prove --out /tmp/hn560-separator-check \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The output directory must be fresh. This standalone audit requires no PySAT,
AllSAT archive or unpublished input. It reconstructs both complete CNFs,
generates fresh proofs, checks them and the supplied positive witnesses, and
reports `complete_boundary_relations_verified: true`. Compare the substantive
fields with [expected.json](expected.json); fresh proof hashes may vary with
native versions. A local archive can instead be checked with
`--archive /path/to/archive`. `--positives-only` explicitly leaves completeness
unverified and is not a full theorem reproduction.

To repeat the original bounded search as well, install python-sat 1.8.dev24
with Glucose 4.1 and run:

```sh
python3 -B hadwiger_nelson_heule560_separator/run.py \
  --out /tmp/hn560-separator-search \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The public producer's two formula streams were compared byte for byte with
the executed pilot formulas. The independent checker uses sparse-radicand
arithmetic and a direct CNF construction; the producer uses ordered XOR field
multiplication. The checker imports no executable from this contribution's
producer. It trusts the pinned coordinate/boundary inputs, the accepted parent
theorem for the target-family corollary, exact Python arithmetic, linear
independence of the squarefree-radical basis, the written gluing and symmetry
arguments, and the DRAT checking implementation. This is not proof-assistant
formalization or an external review of the present result.

The audit verifies six certificate rejections and 1,364 normalization words
of lengths one through five. An optimized-Python positive audit agrees with
the normal structural report. Native versions, timings and validation scope
are recorded in [run_summary.json](run_summary.json) and
[validation.json](validation.json). No background process remains.
