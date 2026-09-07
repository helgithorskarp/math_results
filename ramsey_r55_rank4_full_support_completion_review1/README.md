# Independent review: full-support rank-four completion exclusion

This directory records an independent acceptance audit of Discovery Net h3791,
`R(5,5): full-support rank-four physical completion family excluded`, at source
commit `f3ca3be5e96bde79f807192d985b0c63c38d3506`.

The newly computed non-affine family is accepted with high confidence. For a
fixed 20+23 cut, every nonzero vector of `F_2^4` appears in both factor lists;
five row labels and eight column labels are doubled. All 443 internal edges are
free. The audit independently confirms that the 19,279,260 non-affine
doubled-set pairs have exactly 1,348 dual-`GL(4,2)` orbits and that every orbit
completion formula is UNSAT.

Combining this with the previously reviewed affine-column exclusion at
h3757/h3761 closes this precise full-support multiplicity profile. It does not
exclude other rank-four profiles, show that every hypothetical good43 has a
rank-four cut, or improve the Ramsey bound.

## Reproduce the compact independent audit

From the repository root with CPython 3.11 or later:

```sh
python3 -B ramsey_r55_rank4_full_support_completion_review1/audit_review.py --check-expected
python3 -O -B ramsey_r55_rank4_full_support_completion_review1/audit_review.py --check-expected
```

The checker imports no target Python module. It enumerates all 65,536 binary
4-by-4 matrices, applies Burnside's lemma, canonicalizes every manifest
representative, and reconstructs six complete physical CNFs in two ways.

`REPLAY.json` records the completed single-process replay of all 1,348 fresh
CaDiCaL proofs through `drat-trim`; all deterministic per-case fields match the
committed manifests. See [REVIEW.md](REVIEW.md) for the verdict, proof audit,
resource record, scope, and trust boundaries.
