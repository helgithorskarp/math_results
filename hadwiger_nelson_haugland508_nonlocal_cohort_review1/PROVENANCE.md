# Provenance

The reviewed package is
`hadwiger_nelson_haugland508_nonlocal_cohort` at immutable mathematical
commit `49b81225ca13eb0c4c4e184c25e61499da65dd2c`.  Its certificate is pinned
by SHA-256 in `DEPENDENCIES.json`.  The source package deliberately made no
Discovery Net submission; this review therefore cites its immutable Git
commit rather than inventing a graph reference.

The exact physical parent comes from Haugland's Appendix-A paths as archived
in `hadwiger_nelson_haugland2131_exact_reproduction`.  The complete strict
edge census is the earlier two-route reproduction at commit
`45e8ee56c3aa351ad00c8b870bdc2eeb1875d393`.  This review uses the SymPy
route while the target used the separately implemented standard-library
quotient-field route.

All six target/dependency files named in the review were fetched from their
pinned raw GitHub URLs on 2026-09-16 and matched the local bytes and declared
SHA-256 digests.

The new union word was found in one ordinary four-colour query using
python-sat 1.9.dev15 / CaDiCaL 1.9.5.  The solver output was decoded and
checked immediately against all 4,773 union edges.  No generated CNF, solver
log or SAT return code is retained as mathematical evidence because the
literal word is a smaller solver-free certificate.

A live literature refresh on 2026-09-16 found no unrestricted construction
below Jaan Parts's 509-vertex, 2,442-edge graph.  Haugland's 2,131-point graph
is a Moser-spindle-free restricted record, not an unrestricted vertex record.
Primary sources:

- https://arxiv.org/abs/2010.12665
- https://arxiv.org/abs/2608.04542

The committed Discovery ledger was still stale at indexed height 4,363 while
the RPC node reported 4,364, last block 2026-09-11T02:40:58.067131057Z.
