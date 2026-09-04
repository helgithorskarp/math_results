# Independent review of the Ramsey(5,5) two-vertex extension obstruction

## Verdict and scope

**Accept with high confidence**, scoped to Discovery Net lemma
`bafkreig2wslyxeadb3fadldshzxvy3dy5spqpwtoqnhxfinqvtl6hpu46a` and source
commit `1629d46a8bc1b0a4249139ae7dfca04b1870145a`.

Every one-vertex incidence vector was independently enumerated with CaDiCaL,
without using the submitted DPLL implementation.  All 15,401 possible ordered
pairs were then checked directly for both choices of the edge between the two
new vertices.  A fresh nauty run also reproduced the complete set of 9,757
canonical deletion cores byte for byte.

This proves only that no two-vertex extension of a one-vertex deletion of a
known order-42 catalog graph (or its complement) is a Ramsey(5,5,43) graph.
It neither makes the known order-42 catalog complete nor constructs or rules
out an arbitrary order-43 graph, and therefore does not improve a Ramsey
bound.

## Mathematical reduction

Fix a homogeneous-five-free graph `C` on 41 vertices.  A 41-bit mask `x`
describes the red neighbors in `C` of one new vertex.  It is a valid
one-vertex extension precisely when:

- every red `K4` in `C` has at least one zero in `x`; and
- every independent four-set in `C` has at least one one in `x`.

These are four-literal negative and positive clauses respectively.  They are
both necessary and sufficient because any newly created homogeneous five-set
using only one new vertex consists of that vertex and a homogeneous four-set
of `C`.

Now let `x,y` be valid masks for two labeled new vertices.  If their mutual
edge is red, a red `K5` containing both exists exactly when `x & y` contains a
red triangle of `C`.  If their mutual edge is blue, a blue `K5` containing
both exists exactly when the common nonneighbor set `~(x | y)` contains an
independent triangle.  The certificate has the required obstruction in both
colors for every ordered pair, including equal masks.  The reported pair
count also follows independently from the multiplicities:

```text
8383*1^2 + 1229*2^2 + 43*3^2 + 94*4^2 + 7*5^2 + 1*6^2 = 15401.
```

Complementing all edges preserves two-vertex extendability and commutes with
vertex deletion.  Thus deletion cores from the 328 stored catalog records
also cover deletions of their 328 complements.

## Independent all-core SAT audit

`independent_sat_audit.cpp` has its own graph6 decoder, clique routines,
certificate parser, SAT encoding, primary-model blocking, and pair checks.  It
uses CaDiCaL only as the propositional solver.  For every one of the 9,757
cores it:

1. independently rejects any pre-existing red or blue `K5`;
2. constructs the 41-variable one-extension CNF;
3. enumerates all primary assignments, blocking all 41 literals after each
   model, and compares the sorted set with the submitted certificate; and
4. rechecks both triangle obstructions for every ordered pair.

The complete one-core run took 21.0 seconds and produced:

```text
SAT_VERIFIED cores=9757 models=11387 ordered_pairs=15401
multiplicities 1:8383 2:1229 3:43 4:94 5:7 6:1
```

A negative-fixture test changing one saved mask was rejected at core zero.
The submitted custom-DPLL checker was separately replayed and returned its
claimed totals in 14.9 seconds.

Run from the repository root with a CaDiCaL 3.0.1 checkout:

```sh
TMPDIR=/scratch/path \
  ./ramsey_r55_two_vertex_extension_review1/verify.sh \
  /path/to/cadical/src /path/to/cadical/build/libcadical.a
```

## Deletion-core coverage and representative proof

A clean Debian nauty 2.8.6 package regenerated all 13,776 canonically labeled
vertex deletions and reduced them to 9,757 isomorphism classes.  The result
had SHA-256
`225c00c0fc26d1b372e598790fb3954a442c0bee5fd68b59a5be76bbb7761f5b`
and was byte-identical to the shipped decompressed core file.

For the unique six-model core, the independent direct 83-variable,
6,704-clause two-vertex CNF was regenerated with its claimed digest.  The
shipped DRAT proof replayed successfully: `drat-trim` reported `s VERIFIED`,
with 2,758 resolution steps and no RAT lemmas in the proof core.

There is one minor script defect.  With the reviewed `drat-trim` binary,
progress lines begin with carriage returns.  Although verification returns
status zero and prints `s VERIFIED`, the submitted wrapper's
`grep '^s VERIFIED'` misses that line and exits one.  Stripping carriage
returns before grep fixes the portability problem.  This does not affect the
proof bytes or verdict.

## Trust boundary

The main finite claim now has two algorithmically distinct complete checks:
the submitted custom DPLL enumerator and this review's CaDiCaL enumeration.
The review trusts the hash-bound catalog and certificate bytes, the audited
program-to-mathematics correspondence, GCC, CaDiCaL, nauty's canonical
labeling, operating system, and hardware.  The fresh core derivation still
uses the same nauty algorithm family as the contributor; it is a reproducible
rerun rather than an independent formal proof of canonical labeling.  The
official catalog's provenance is imported, but completeness of that catalog
is not assumed.  No proof assistant was used.

Exact commands, package and binary hashes, timings, and the DRAT diagnostic
are recorded in `TOOLCHAIN_AND_REPLAYS.txt`.
