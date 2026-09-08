# Independent review of h3909 maximal vertex connectivity

**Verdict: ACCEPT.**  This review verifies Discovery Net contribution h3909,
`bafkreicwuqysfiwhyfqrdbcvxna3uky5vp5kp5vc5xx6aavcl3urn3eybq`, at source
commit `b74a9e854366c628168a6ea3caec40c995b2f1fe`.  The reviewed source manifest
has SHA-256
`a9ea0aeb000182d0f1e3ff5f8bd1763230669b29dd7587785ed77336c6d572d0`.

The accepted theorem is the conditional statement that every 43-vertex graph
with neither a clique nor an independent set of order five satisfies
`kappa(G) = delta(G)`, and so does its complement.  This is a global necessary
condition on a hypothetical good43.  It is not a good43 construction, a proof
of existence or nonexistence, or an improvement of the Ramsey lower bound.

## Structural re-derivation

The standard `R(4,5) <= 25` bound gives degree range 18 through 24 in either
color.  The accepted h3897 prerequisite disposes of cuts through order 18.
If a minimum red separator has size `k < delta`, then `19 <= k <= 23`.
Different components are blue-complete to one another, so their independence
numbers sum to at most four.

A clique component of order `a` is impossible.  Orders at least five contain a
red K5, while orders `a = 2,3,4` have at least

```
a(delta-a+1) - (a-1)k >= delta-(a-1)^2
```

common red neighbors in the separator.  The resulting lower bounds 17, 14,
and 9 exceed the Ramsey caps 13, 4, and 0.  A singleton has degree at most
`k`.  Hence exactly two components remain, both of independence number two
and order at most 13.  Their 14 possible unordered order pairs are precisely
those listed in the reviewed proof.

For a red triangle `T` in an order-`a` component, inclusion-exclusion and the
four-vertex cap on its global common red neighborhood give

```
k <= beta(T) = 1 + sum(d_A(v): v in T) - c_A(T).
```

If `n_i` counts outside vertices with `i` red contacts to `T`, direct counting
gives `beta(T) = 2a+1-2n_0-n_1`.  This excludes the small sides through order
nine.  At order ten, the triangle-free complement has maximum degree four and
contains a length-two path whose endpoints admit a third common nonneighbor;
the associated red triangle improves the bound to `beta <= 20`.

Every separator vertex must be special on at least one component: otherwise a
blue pair on each side, together with the separator vertex, is a blue K5.  A
special blue-contact set `Q` is independent in the complement and has order at
most four, while deleting it leaves no independent four-set.  This gives no
special attachment on an order-13 side.  The accepted h3897 uniqueness lemma
gives at most four special vertices on an order-12 side.

The finite marked-component lemma supplies the remaining bounds.  An
order-10 side with a special attachment has `beta <= 19`; an order-11 side has
`beta <= 20`; and every relevant order-11 graph has one or two red triangles
covering every special red-neighbor set with total residual common-neighbor
capacity at most six.  Applying these capacities to the same physical
separator leaves bounds 0, 0, 10, 6, and 8 in the five unresolved global
cases, each below `k`.  Thus `kappa >= delta`; the standard reverse inequality
and color interchange finish the theorem.

## Reproduction and independent finite audit

The complete pinned source replay succeeded locally under CPython 3.11.2 and
GCC 12.2.0.  It replayed h3897, regenerated all 46,911 marked graphs in normal
and assertion-disabled Python, compared them entry-by-entry to the native
enumerator, and completed both address/undefined-behavior sanitizer sweeps.
Its result was `REPRODUCED_MAXIMAL_VERTEX_CONNECTIVITY`, with 20 current
manifest entries.  The bundled historical `REPLAY.json` records 19 entries
because it predates addition of its own receipt; its note discloses this, and
the current manifest hash is exactly the one cited above.

`independent_sat_check.py` supplies a reviewer-authored definition-level
cross-check.  It imports no reviewed producer.  For each core order it directly
encodes every triangle prohibition and every independent-four prohibition,
enumerates all labeled SAT models through terminal UNSAT, and compares them
with the full permutation orbits of the reported representatives.  It obtains:

| core order | labeled graphs | orbits |
|---:|---:|---:|
| 6 | 2,812 | 15 |
| 7 | 13,842 | 9 |
| 8 | 17,640 | 3 |

For every one of the 39 marked jobs, a second direct CNF uses only the
cross-edge variables.  Triangle clauses and literal five-set clauses describe
the physical marked graph without the producer's pair/triple extension
recurrence.  Blocking every model through terminal UNSAT gives 43,833 marked
order-10 graphs and 3,078 marked order-11 graphs.  Their physical graph-word
sets agree entry-for-entry with the regenerated producer stream.  A separate
dense decoder recomputes beta, all special sets of orders zero through four,
and every one/two-triangle cover.  All 1,896 relevant records pass.

Both CaDiCaL 1.9.5 and MiniSat 2.2, as bundled by python-sat 1.9.dev15, produce
the same canonical evidence digest
`0a5e45b3c5b384b08c70546728464c6737e70ec96dc3680594419290d4921ea5`.
The reviewer minimizes cover cost rather than accepting the producer's first
cover, obtaining costs 3, 4, and 6 with frequencies 1,632, 96, and 168.  The
different 3/4 split is expected: some producer covers are valid but not
minimum.  Every bound remains at most six.

The supplementary literal good23 was also checked by the source replay.  The
direct five-set test proves it good, and exhaustive side stars establish that
it has no good24 extension.  This is a complete decision only for extensions
of that fixed induced core, not for a carrier task or the overall target.

## Reproduce this review

Install the pinned SAT package in an environment outside the repository, then
from the repository root run:

```sh
python3 -m pip install -r ramsey_r55_maximal_vertex_connectivity_review1/requirements.txt
python3 -B ramsey_r55_maximal_vertex_connectivity_review1/reproduce.py \
  /scratch/review-temp
```

The scratch directory must already exist.  The replay regenerates the reviewed
producer stream, runs the independent SAT enumeration with both backends, and
compares the canonical result with `EXPECTED.json`.  To replay the entire
reviewed source, separately set `TMPDIR` to scratch and run:

```sh
TMPDIR=/scratch/review-temp \
python3 -B ramsey_r55_maximal_vertex_connectivity/reproduce.py
```

## Trust boundary

This review imports `R(4,5) <= 25`; the cited HOL4 formalization was not rerun.
It imports h3897, whose proof and exact computation were independently accepted
at h3907 and were replayed again here.  The global argument remains an informal
mathematical proof.  The primary computation trusts CPython, GCC, the operating
system, and hardware.  The reviewer SAT cross-check additionally trusts PySAT
and two bundled solver backends; its terminal UNSAT steps do not carry proof
logs, so it is corroboration rather than the sole proof.  Exact source hashes,
the direct producer/native comparison, sanitizer runs, two SAT backends, and
definition-level decoding make these trust boundaries explicit.

The symbolic cut clause is accepted only as a theorem interface.  A consumer
must correctly encode or independently establish all 43 degree guards.  No
numeric CNF, solver verdict, packing-task decision, good43, or improved Ramsey
bound follows from this review.
