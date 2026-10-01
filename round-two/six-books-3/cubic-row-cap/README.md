# A degree-floor-free Petersen-root row bound

Actual author six-books-3, researcher. Ordinary proof: in a valid
22-vertex (B4,B7) graph of maximum red degree ten, with a degree-ten
root whose ten degree-ten neighbors induce Petersen, every outside
miss row has size at most eight. No minimum outside degree or edge
count is assumed. See [PROOF.md](PROOF.md) for the full quantified
claim, proof, credited Gram identities, and the conditional 108-edge
application. Independent review is pending; the Ramsey gap is unchanged.

Use Python 3.11 or later, standard library only. Run sequentially from
the repository root, with OMP, OPENBLAS, MKL and NUMEXPR thread counts
set to one:

```sh
python3 -B round-two/six-books-3/cubic-row-cap/gram.py
python3 -B -O round-two/six-books-3/cubic-row-cap/gram.py
python3 -B round-two/six-books-3/cubic-row-cap/literal.py
python3 -B -O round-two/six-books-3/cubic-row-cap/literal.py
python3 -B round-two/six-books-3/cubic-row-cap/controls.py
```

`gram.py` checks exact contraction identities and all 30 canonical
nine-row patterns. `literal.py`, without importing `gram.py`, checks
31,744 physical outside stars, the forced-page contradictions, and the
known primary21 fixture. Each program compares its complete result
with [expected.json](expected.json), including deterministic hashes.
The optional `--derive` prints a freshly computed result without the
expected-output comparison; it does not bypass any mathematical check.
`controls.py` runs negative input checks both normally and under `-O`.
Explicit exceptions remain active under optimization; no Python assert
is used for a mathematical decision.

The primary21 input has zeros red off the diagonal and is known prior
art. The generated signed controls deliberately violate the book
bounds. Neither them nor the ten-row degree-ten control are witnesses.
No 22-vertex host census, solver, floating point or large corpus is
required. Ordinary proof correctness and peer review are separate from
passing these support checks. [provenance.json](provenance.json) records
primary/source inputs and [MANIFEST.json](MANIFEST.json) hashes the
compact files. Generated scratch, caches and logs are not published.
