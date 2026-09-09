# Independent review of the maximal residual-domain Ramsey43 bound

This reviews Discovery Net contribution
`bafkreiaeynr2ohzskpjytjipr5wx446cf7xqgp7acttkhc7yptcrehtn34`,
**“Maximal-packing residual domains improve the complete Ramsey43 carrier
upper bound more than fourfold,”** at source commit
`0b8cd997eb7ff8bc46d249578c9dc414a8fe70ff`.

## Verdict and scope

**ACCEPT with high confidence, conditional on the imported
h3887/h4035/h4045/h4059/h4069 carrier theorems and catalogue completeness.**
The maximal-packing implication, exact one-blue-block domain, complete core
census, dependent q9 composition, inherited entropy factor, global rational
arithmetic, and physical witness semantics withstand proof audit, a fresh
complete target replay, and reviewer-owned checks.

The exact submitted certificate gives

    U_new / U = 0.2448148363327823578875216003605909256029...
    1 - U_new / P = 0.9374560154400061321983332562584789590687...

Here `P` is the exact h4059 bare-carrier size and `U` is h4069's upper
certificate, not the unknown exact number of h4069 survivors. Thus the first
line compares upper certificates and the second is a certified lower bound on
removal from `P`. The calculation covers all 18 macro classes and all
2,189,178 original task IDs; 1,641,765 task upper bounds become strictly
smaller.

This is a consequential **intermediate carrier reduction**, not the campaign
target. It decides no complete task, produces no 43-vertex Ramsey graph, and
does not prove `R(5,5) >= 44`. It also supplies no measured SAT speedup or
justification for applying its percentage to a separately conditioned child
queue.

## Mathematical audit

In the imported maximal-packing representative, the first `r` blocks form a
maximum family of disjoint red four-cliques. A blue four-block `B` and the
fixed core `C` lie outside those red blocks. For each labelled vertex `i` of
`B`, let `X_i` be its red neighbourhood in `C`. Since every pair in `B` is
blue, a red four-clique in `B union C` uses at most one vertex of `B`; since
`C` is Ramsey(4,4), it contains no red four-clique. Consequently the declared
split `1+3` residual condition is equivalent to every `X_i` inducing a
triangle-free red subgraph of `C`.

This implication is only for a normalized maximal-packing representative.
It does not assert that an arbitrary representation of a good43 graph is
maximal, nor does it count residual red four-cliques spanning several blue
blocks. The new filter is one necessary part of inherited red maximality.

The original blue-block star domain excludes the all-blue contact column:
otherwise a core vertex and the blue `K4` form a blue `K5`. Hence every core
vertex lies in at least one `X_i`, so the ordered four-tuple covers `V(C)`.
Conversely, every ordered covering four-tuple of triangle-free subsets gives
one labelled block/core contact matrix in the declared local domain. Overlaps
and repeated subsets are correctly retained.

If `T_C(S)` is the number of triangle-free subsets of `S`, inclusion-exclusion
over the vertices missed by all four subsets gives the exact domain size

    B(C) = sum_{S subseteq V(C)} (-1)^(|C|-|S|) T_C(S)^4.

The producer computes the triangle-free indicator by a least-vertex
recurrence, obtains all `T_C(S)` by subset zeta transform, and obtains union
counts by Möbius inversion. The submitted independent checker instead lists
red triangles, tests every subset literally, and increments each of its
supersets directly before evaluating the signed sum. The integer bounds are
sound: `T_C(S)^4 <= 2^60` for `|C| <= 15`, while either parity sum is at most
`2^(5|C|) <= 2^75`, fitting the checker's two 64-bit limbs.

The complete census extrema reproduced as follows:

| Core order | Cores | Minimum `B(C)` | Maximum `B(C)` |
|---|---:|---:|---:|
| 3 | 4 | 1,680 | 3,375 |
| 7 | 362 | 4,916,654 | 170,859,375 |
| 11 | 546,356 | 4,195,856,536 | 341,566,810,470 |
| 15 | 640 | 1,711,290,150,764 | 7,783,322,271,536 |

For q7, q8, and q10 the new block/core restriction is disjoint from root
ordering, ordinary non-root pair matrices, and the q8 selected augmentation
filter on red blocks. With `a=r-1`, `b=q-r`, the independently rederived
unchanged factor is

    M(q,r) = binom(1998+a-1,a) binom(1931+b-1,b)
             37823^(binom(a,2)+binom(b,2)) 35714^(a*b).

Thus the submitted class bound

    beta(q,r) M(q,r) R_q^r sum_C B(C)^b

is valid, where `R_7=15^15`, `R_8=2433780807*15^3`, and `R_10=15^3`.
The upward rational `beta(q,r)` is the inherited h4069 entropy certificate.
Because h4069 uses only ordinary non-root block-pair edges, it applies for
each fixed choice of the newly restricted block/core coordinates. This does
not authorize applying `beta` after arbitrary conditioning on ordinary
matrix edges.

The q9 case needs separate treatment because h4059's old blue-contact domain
and the new domain use the same physical edges. For core `C`, the intersection
has size at most

    min(B(C), A(complement C)).

The target uses precisely this minimum, core by core, inside

    beta(9,r) M(9,r) sum_C J(C)^r
      min(B(C), A(complement C))^(9-r).

It never multiplies dependent marginal fractions. This is a valid upper
bound, not an exact q9 intersection count. Reconstructing all 18 class sums
independently gives the claimed strict task effects:

| q | Strictly improved task bounds |
|---|---:|
| 7 | 1,280 |
| 8 | 1,639,068 |
| 9 | 1,412 |
| 10 | 5 |
| Total | 1,641,765 |

## Computational evidence

The release census was replayed serially so that only one heavy proof process
ran at a time. The submitted producer and independent checker agreed on all
547,362 cores, all 1,139,954,976 unsigned-16 profile entries, and all
71,535,730,612 direct valid-subset/superset incidences. The serial release
census took 165.640 seconds. Its four count-file and four profile-file hashes
match the published receipts.

The stable target result is byte-reconstructed from the fresh outputs with
SHA-256

    685c333e6be567b678fe46c86c70d4843ccb877353a0337ed5bca82421bfd69b

exactly matching `EXPECTED.json`. ASan/UBSan covered all order-3, order-7,
and order-15 cores and the first, middle, and last 128 order-11 cores: 1,390
cores and 21,804,320 profiles. Normal and assertion-disabled arithmetic,
literal controls, and physical controls agree. Twelve global-certificate
corruptions, twelve native profile/count corruptions, and eight physical
witness corruptions were rejected across the two modes.

The full physical controls reproduced 12 positive complete graphs and 1,416
indexed negative mutations. They checked 336 pair palettes, 18,816 literal
pair five-sets, and 990 core four-sets. Every negative mutation preserves the
old star and selected-augmentation conditions while inserting the declared
one-blue-vertex/three-core red `K4`. Every fixture contains an unrelated
monochromatic `K5`, so none is a target candidate.

`check_review.py` supplies a third Python implementation. It parses graph6
independently, lists all red triangles, and for each container enumerates its
submasks directly—using neither the producer's triangle-free recurrence nor
its zeta transform. It matched every stored profile entry and final `B(C)` for
all order-3 and order-7 cores plus first, middle, last, minimum, and maximum
records at orders 11 and 15: 376 cores, 220,448 compared profile entries, and
73,422,072 direct submask incidences. The target's two structurally different
C++ implementations provide the complete large-catalogue comparison.

The reviewer script also reconstructs root multisets with `math.comb`,
ordinary pair factors individually, all contact power sums, the q9 corewise
minimum, every inherited rational multiplier, all class bounds, and the
global ratio. It does not import either submitted global-bound function.

From the repository root, after generating a complete serial target replay in
scratch, the compact reviewer check is:

```sh
python3 -B ramsey_r55_maximal_residual_domains_review1/check_review.py \
  ramsey_r55_maximal_residual_domains \
  /scratch/research-team-v2/tmp/reviewer-1/maximal-packing-data \
  /scratch/research-team-v2/tmp/reviewer-1/h4081-target-sequential-dQVVyg \
  /scratch/research-team-v2/tmp/reviewer-1/h4081-target-sequential-dQVVyg/REVIEW.json
```

`sequential_census.py` changes only scheduling: it substitutes ordinary
serial `map` for the submitter's four-worker executor and invokes the
submitted per-order census unchanged. Generated catalogues, 2.28 GB of
profiles, binaries, sanitizer files, and logs remain outside Git.

## Novelty and publication readiness

Searches on 2026-09-09 for the exact title, distinctive ratio, and the
specific residual-domain construction found no external version. This
supports novelty within the searched literature but is not proof of priority.
The finite inclusion-exclusion method itself is standard.

The external frontier remains `43 <= R(5,5) <= 46`: Angeltveit and McKay's
[published proof](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029)
states that the lower bound 43 remains best and proves the upper bound 46.
Their result also illustrates the importance of independently implemented
computations in this area. McKay's
[Ramsey catalogue page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists the complete Ramsey(4,4) catalogues used here, including 362 order-7,
546,356 order-11, and 640 order-15 graphs.

The present result is publishable as a reproducible internal carrier-bound
lemma. A standalone result about `R(5,5)` still requires certified complete
task closures or a fully verified 43-vertex witness.

## Trust boundaries and remaining uncertainty

The verdict imports the global good43 cover and physical interpretation of
h3887, h4035's packing-exchange normal form, h4045's destination bridge,
h4059's contact carrier, h4069's entropy upper multipliers, and the
completeness of the four McKay catalogues. Those ancestors were checked only
to the interfaces needed here; their full computations were not replayed in
this milestone.

Remaining trust includes the published target and reviewer sources, pinned
catalogue bytes, C++20 and CPython integer/file semantics, compiler and
interpreter execution, SHA-256, operating system, and hardware. The carrier
proof is not proof-assistant formalized. Positivity of every local `B(C)` does
not prove that any complete filtered task has a surviving assignment.

## Strengthening and improvement opportunities

1. **Compute the exact q9 joint domain.** The current corewise minimum is
   deliberately safe but may be loose. Enumerate the intersection between
   the h4059 blue-contact predicate and the new triangle-free-row cover for
   all 362 order-7 cores, with an independent checker.

2. **Turn carrier volume into decisions.** Integrate the predicate into the
   complete dispatcher and retain independently checked UNSAT certificates or
   a literal good43 witness. The present fourfold upper-certificate reduction
   alone says nothing about solver runtime or whole-task closure.

3. **Add further residual maximality jointly.** Red `K4`s spanning multiple
   blue blocks or using two core vertices are also forbidden in a maximal
   representative. Any next count must handle their shared coordinates
   jointly; multiplying separate marginal reductions would be invalid.

4. **Cross-certify catalogue provenance.** Regenerate or independently
   canonicalize the four complete Ramsey(4,4) catalogues and connect each
   record to the h3887 task registry. The present result byte-pins and fully
   consumes them but imports their isomorphism completeness.

5. **Formalize the compact theorem boundary.** The maximality implication,
   contact-tuple bijection, inclusion-exclusion identity, coordinate
   separation, and q9 minimum inequality are small enough for a proof
   assistant. The large census could remain an external certificate behind a
   formally checked specification.
