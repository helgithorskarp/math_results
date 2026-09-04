# Lean certificate for the Albertson `r=27` terminal map

This package kernel-checks the finite combinatorial and arithmetic layer of
the terminal-triangulation argument used in the reviewed proof of Albertson's
conjecture at chromatic number 27. Its scope is deliberately narrower than the
graph-drawing theorem.

## Intended informal statement

Assume the geometric face trace has produced the five oriented triangular
faces

```text
uzw, zwx, ztx, trx, rwx.
```

Then their edge incidences have pentagonal boundary `u-z-t-r-w-u`, the five
complementary original-vertex edges are `zw,ur,ut,zr,wt`, and the declared
crossing pairs form a 5-cycle. For each of the two reviewed residual profiles,
the terminal planarization has the exact Euler-triangulation counts used in
the proof. Finally, the order-53 deletion sum has the nonzero remainder that
forces the integer lower bound 6089, which exceeds `Z(27)=6084`.

[`AlbertsonTerminalMap.lean`](AlbertsonTerminalMap.lean) proves this statement
as five closed theorems:

- `finite_terminal_map_certificate` checks all face multiplicities, the five
  boundary and five internal edges, Euler count `6+5=10+1`, an explicit
  endpoint-level enumeration of all ten `K5` pairs, and degree two at every
  vertex of the crossing graph. It also checks directed incidence: both
  orientations occur once on every internal edge, while the only surviving
  darts are `u->z->t->r->w->u`.
- `vertex_link_certificate` derives every link from the oriented face list.
  The five original vertices have explicitly connected interval links, with
  two degree-one endpoints and all other degrees two, while `x` has the
  circular link `z-w-r-t-z` with every degree equal to two.
- `profileA_certificate` proves `C5=10`, terminal `(e,x)=(83,17)`, and
  planarization `(V,E,F)=(41,117,78)` together with both triangulation
  identities.
- `profileB_certificate` proves the corresponding values `C5=12`,
  `(e,x)=(82,16)`, and `(V,E,F)=(40,114,76)`.
- `final_integer_certificate` proves
  `298314=49*6088+2<49*6089`, `Z(27)=6084`, and `6084<6089`.

The custom finite encoding is bridged to the mathematical labels explicitly:
`OriginalVertex` has constructors `u,z,t,r,w`; `originalEndpoints` maps every
original edge constructor to its endpoint pair; and
`originalEdgesInPairOrder.filterMap originalEndpoints` is proved equal to the
complete unordered-pair enumeration of those five vertices.

## Reproduction

The pinned toolchain is Lean 4.33.1, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; its bundled `Std` library is the
only import. Lake 5.0.0 is present in that release but is not needed to compile
this single-file package. No Mathlib revision or third-party package is used.

With Lean 4.33.1 on `PATH`, run:

```sh
lean AlbertsonTerminalMap.lean | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The expected transcript consists of five successful `#print axioms` audits.
The proofs use kernel reduction through `decide`; there is no `sorry`, `admit`,
`native_decide`, `unsafe` definition, custom axiom, external oracle, generated
code, or imported certificate.

## Exact trust boundary

Lean proves the consequences of the displayed finite face list and the two
numeric profile records. It does **not** prove that a good drawing produces
those faces. In particular, Jordan separation, the triangular-face tracing,
the distinctness/provenance argument, and the sealed full-pentagon disks remain
the geometric part of the proof. It also imports rather than formalizes the
primary PRTT and Büngener--Kaufmann classifications and the exhaustive
derivation of the two profiles.

Those bridges, their two independent reviews, the exact primary-source
versions, and all recursive-sampling certificates are consolidated in the
[`albertson_r27_reviewed_chain`](../albertson_r27_reviewed_chain/README.md)
package. This formalization strengthens the assurance of its finite layer; it
is not by itself a formal proof of Albertson's conjecture at `r=27`.
