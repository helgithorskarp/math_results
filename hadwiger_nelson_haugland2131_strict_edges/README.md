# Exact strict-edge census for Haugland's 2,131-vertex construction

## Result

This directory strengthens the exact reconstruction of Jan Kristian
Haugland's 2026 Moser-spindle-free construction by deciding **every unordered
pair of vertices exactly**.  For the point sets reconstructed from the 231
Appendix A paths, the strict unit-distance graphs (two vertices adjacent if and
only if their Euclidean distance is exactly one) have:

```text
     vertices   all pairs   strict unit edges   canonical edge SHA-256
G1        740     273,430               3,985   3b01cdfc34edc58e6883f5da69cf06457701a5c76110d32a89af8fab30b453f5
G2      1,066     567,645               6,264   35e3ef29be2caddcdf64977f85001b90ec9e1147d07500ba47721b928641ae60
G3      2,131   2,269,515              12,530   980bdb02e133be0e4257bab1a204f2942f554e59822136fab632f45494a6c113
```

The edge hash is SHA-256 of the canonical UTF-8 stream `u v\n`, with pairs in
lexicographic order.  The exact G1 and G3 edge sets equal the edge lists in the
sibling reconstruction byte-for-byte at the pair-list level.  The sibling
stores only the G2 count, so the two checkers here additionally agree on the
displayed canonical G2 hash.

They also agree point-by-point on canonical coefficient serializations, with
coordinate hashes
`77bacadacfedbf1d71f3c6651700c6d9a0b35979614448e583adc8c76d2c7736`,
`c450c335d446647890189542ad66d1443095772e5aeef2e7c7f41e417d9bad1e`,
and `fcdcba9dee3c2e0ea6044e17cb5f32bc9c989b8155d8c377863d41d357f72cab`
for G1, G2, and G3.

This closes the sibling result's explicit floating-screen limitation: all
3,110,590 pairs are covered by an exact argument, so the claimed edge counts
are counts of the induced strict unit-distance graphs, not merely of declared
unit-edge subgraphs.

This is an exact reproduction/refinement of a known construction, not a
smaller 5-chromatic graph.  It does not prove the still-pending endpoint
forcing SAT statement, improve the 509-vertex unrestricted record, or change
the bounds `5 <= chi(R^2) <= 7`.

## Finite reduction and completeness proof

All G1 and G2 coordinates lie in `K = Q(zeta_84)`, while G3 lies in
`K(sqrt(5))`.  Choose a prime `p`, an element of exact order 84 in `F_p`, and a
square root of 5 in `F_p`.  Evaluation gives a ring homomorphism on every
coordinate because none of its rational denominators is divisible by `p`.
Consequently,

```text
(x_u-x_v)^2 + (y_u-y_v)^2 = 1 in characteristic zero
```

implies the same equality after every chosen specialization.  Therefore a pair
that fails even one modular test cannot be a unit pair.  The checker retains
all modular survivors and tests their squared distances exactly back in
characteristic zero.  This proves both directions and cannot lose a true edge.

The primary checker reconstructs the existing SymPy algebraic-field points and
uses the specialization

```text
p = 1009, zeta_84 -> 527, sqrt(5) -> 244.
```

It leaves 4,069, 6,492, and 14,013 survivors for G1, G2, and G3, respectively,
then confirms exactly 3,985, 6,264, and 12,530 unit pairs.

The independent checker does not import SymPy or the primary reconstruction.
Using only the Python standard library, it implements

```text
Q[x] / (x^24 + x^22 - x^18 - x^16 + x^12 - x^8 - x^6 + x^2 + 1)
```

as 24-tuples of `Fraction`, derives the 84 unit vectors algebraically, and
rebuilds G1, G2, and G3 directly from the path table.  It intersects sieves at

```text
p = 2521, zeta_84 -> 1397, sqrt(5) -> 643;
p = 2689, zeta_84 -> 2025, sqrt(5) -> 172.
```

The surviving pair counts are already 3,985, 6,264, and 12,530; it nevertheless
checks every survivor in the rational cyclotomic quotient.  The independent
point counts, complete edge sets, and three hashes agree with the primary
route.

## Reproduction

Run from the repository root with CPython 3.11 or newer.  Put the environment
outside the repository, for example under `/scratch`:

```bash
python3 -m venv /scratch/haugland-strict-edges-venv
/scratch/haugland-strict-edges-venv/bin/pip install -r \
  hadwiger_nelson_haugland2131_strict_edges/requirements.txt

/scratch/haugland-strict-edges-venv/bin/python \
  hadwiger_nelson_haugland2131_strict_edges/strict_edge_certificate.py \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland2131_strict_edges/certificate.json

python3 hadwiger_nelson_haugland2131_strict_edges/independent_check.py \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland2131_strict_edges/certificate.json

python3 hadwiger_nelson_haugland2131_strict_edges/test_strict_edges.py
```

Expected final prefixes are:

```text
primary_all_checks=true prime=1009
independent_all_checks=true primes=2521,2689
...
Ran 3 tests ... OK
```

On the reference host, the primary run took about two minutes and the
independent run about one minute.  Both are deterministic and write no solver
trace or generated coordinate file.

## Artifacts and trust boundary

- `certificate.json` fixes the input hash, specializations, all-pair counts,
  sieve counts, exact edge counts, and canonical edge hashes.
- `strict_edge_certificate.py` is the primary SymPy route.
- `independent_check.py` is a separate standard-library exact-field route.
- `test_strict_edges.py` checks the cyclotomic relation, generator order,
  inversion, and the sieve's no-false-negative property on a small exact case.

The shared input is the path transcription and graph JSON in
`hadwiger_nelson_haugland2131_exact_reproduction`; its SHA-256 is
`201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d`.
Identification with Haugland's paper therefore inherits that transcription
trust boundary.  The primary route additionally trusts CPython, SymPy 1.14.0,
and its algebraic-field arithmetic.  The independent route trusts CPython's
`Fraction`, integer, tuple, dictionary, JSON, and SHA-256 implementations and
the short quotient-field code here.  The modular maps are not trusted to prove
an edge: they only reject pairs, and every survivor is checked exactly.  No
floating-point comparison, SAT solver, proof log, or proof assistant is used.

Primary source: J. K. Haugland,
[*A Moser-spindle-free 5-chromatic unit distance graph on 2131 vertices in the
plane*](https://arxiv.org/abs/2608.04542v2), 2026.
