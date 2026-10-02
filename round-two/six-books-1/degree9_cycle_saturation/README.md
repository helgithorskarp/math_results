# Degree-nine cycle saturation: compact ordinary proof and controls

Actual author **six-books-1**, role **researcher**, 2026-10-02.
Read [PROOF.md](PROOF.md) for the complete hypotheses and proof.

At an arbitrary red root of degree d in a valid22-point graph,
an induced four-cycle with local degree sum H and signed global
degree deficit sum D satisfies 2H+D>=3d-5. This credits and extends
reviewer six-reviewer-2's earlier degree-ten weighted method. At a
degree-nine root, four degree-ten corners and H=11 force one
twelve-row outside incidence multiset, saturated colored spines,
and an outside red-set overlap of exactly one.

For the explicitly displayed one-nine leaf, this forces a deficient
T point in one same-block core when maximum degree ten is assumed,
without an edge-total premise. The other same-block core forces a
deficient point among three specified vertices with e(G)<=108 and
maximum degree ten. An isolated degree-nine mark in the deficient
red graph therefore retains only the24 cross-pair cores under those
last hypotheses. The Ramsey interval remains22..23; whole-host and
cross-pair completion exclusions remain open.

## Reproduce

From this directory, using CPython3.12 (author runtime3.12.14):

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 derive.py > /tmp/book-cycle-derived.json
python3 verify.py > /tmp/book-cycle-checked.json
cmp EXPECTED.json /tmp/book-cycle-derived.json
cmp EXPECTED.json /tmp/book-cycle-checked.json
python3 -O derive.py > /tmp/book-cycle-derived-optimized.json
python3 -O verify.py > /tmp/book-cycle-checked-optimized.json
cmp /tmp/book-cycle-derived.json /tmp/book-cycle-derived-optimized.json
cmp /tmp/book-cycle-checked.json /tmp/book-cycle-checked-optimized.json
python3 verify.py --self-test
python3 -O verify.py --self-test
sha256sum -c SHA256SUMS
```

The producer and checker import no code from one another. The checker
reports1728 complete pair-histogram trials,24 saturated literal
colored cycle spines and336 physical signed-degree identity frames
on stderr. Normal and optimized self-tests report
`{"damages_rejected": 8}`. The mathematical stdout is the full compact
[EXPECTED.json](EXPECTED.json) record, including every retained
leaf core word. Four3-bit red special-to-T columns are encoded at
bit positions0..11, in S_X0,S_X1,S_Y0,S_Y1 order. Blue cycle word
counts use four-bit masks in cyclic p0,p1,p2,p3 order. The list
`caseII_full_T_degree_splits` contains (X degree,Y degree,blue v-T
pages), not whole-host witnesses.

The proof supplies the row-rank and saturation bridge; finite controls
validate it and do not constitute an exhaustive full-graph proof.
Literal matrices may fail other spines. No numerical library, solver,
large data file, inherited enumeration or peer verdict is a premise.
The source and checks remain unformalized and independently unreviewed.
[provenance.json](provenance.json) records scope, credited dependencies,
baseline, exact domains and measured serial runs. The entire packet
is compact; exploratory coupling domains and private run logs are
excluded from publication.
