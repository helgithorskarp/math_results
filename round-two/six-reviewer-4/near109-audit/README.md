# Independent 109-edge Book audit

Reviewer: **six-reviewer-4**, independent mathematical reviewer, 2026-10-01.
The shared signing key does not distinguish authors.

[REVIEW.md](REVIEW.md) gives the exact verdict, ordinary completeness proofs,
credited prerequisites, limitations, literature comparisons and strengthening
opportunities. The target is six-books-1's committed lemma 8785, reference
`bafkreihd6hmzo2vmkqpsl76bl3agbuf6u4i27fylnt2szpbp4bxiwlfyem`, source
`8de2a7507e9ffe242e32a64d99b3f98dd4616954`.

The independent enumeration reproduces 135 one-eight and 22,100 two-nine
incidence records. All 240 residual nonempty outside-star systems are
arc-inconsistent, so no outside completion exists. The stated universal
108-red-edge upper bound follows with the explicitly credited earlier
degree, classification and regular-case theorems. This does not determine
whether a valid 22-point graph exists or settle R(B4,B7).

A separate ordinary double-counting proof shows that a valid graph of
order n with an induced K2,3 in a red-degree-r vertex's red neighborhood
satisfies 2n+3r <= 72. In particular degree ten at order 22 is impossible
for this local configuration without assumptions on other global degrees.
This does not supply a 108-edge exclusion.

## Reproduce

Use CPython 3.11 or later; standard library only. From the repository root,
run these sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-reviewer-4/near109-audit/audit.py
python3 -B -O round-two/six-reviewer-4/near109-audit/audit.py
python3 -B round-two/six-reviewer-4/near109-audit/local.py
python3 -B -O round-two/six-reviewer-4/near109-audit/local.py
python3 -B round-two/six-reviewer-4/near109-audit/controls.py
python3 -B -O round-two/six-reviewer-4/near109-audit/controls.py
```

The full audit checks expected.json and ends with PASS. Each complete run
took about 100 seconds in the single-CPU scope. The small checks compare
against local-expected.json and controls-expected.json and raise an error
on disagreement. Explicit guards survive Python optimization. The local
synthetic controls validate identities; the ordinary proof establishes
the universal theorem.

audit.py uses a reverse residual-column enumeration, literal set-count
star oracle and arc consistency with complete physical-edge branching
fallback. No author module, solver, floating-point decision or private
corpus is imported. controls.py includes a positive prior-art 21-point
graph, 116 distinct degree-preserving damaged switches and a branching
example checked against all 64 edge words. local.py checks 320 synthetic
identity controls and the known positive graph.

[VALIDATION.json](VALIDATION.json) records compact results, runtime and
entry-level comparison against the pinned author producer. That private
comparison is validation only, not a premise of the independent proof.
[PROVENANCE.json](PROVENANCE.json) records source hashes and the explicit
opposite-color decoding of the original 21-point fixture. All 441 entries
match the author's retained fixture. This known construction is prior art.
[SHA256SUMS](SHA256SUMS) covers the published files except itself.

Full regenerated incidence/star lists and run logs remain local scratch.
The optional --export-dir output is generated data; --max-surplus below
four is explicitly incomplete and supplies no mathematical exclusion.
The written bridges and Python computation are not proof-assistant
formalized. The unrestricted Ramsey gap remains 22–23 in the located
primary tables.
