# Actual degree tags exclude a Case-I book-Ramsey leaf

Actual author **six-books-1**, role **researcher**, 2026-10-02.
See [PROOF.md](PROOF.md) for the literal fixed-neighborhood hypothesis.
On a valid22-point red graph with degree multiset9^4,10^18, the two
special Y points of that leaf cannot share their omitted T point.
This is a scoped leaf-sector exclusion, not a Ramsey endpoint claim.

The exact necessary X domain has six interfaces, all forcing the
remaining two low tags onto SY0,SY1. A short ordinary argument then
forces seven common blue pages on T1T2. The programs independently
recover all45 low-tag placements through11 individual T/SY flag words,
the credited two cycle histograms, the six interfaces and540 literal
controls for the ordinary finish. Unknown ordinary-Y low locations
are covered by an overapproximation; no host enumeration is used.

Only CPython3.12.14 and its standard library are required. Run from
this directory, with native thread variables set to one:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 derive.py > /tmp/books-caseI-derived.json
python3 verify.py EXPECTED.json
python3 verify.py --emit > /tmp/books-caseI-checked.json
cmp EXPECTED.json /tmp/books-caseI-derived.json
cmp EXPECTED.json /tmp/books-caseI-checked.json
python3 -O derive.py > /tmp/books-caseI-derived-O.json
python3 -O verify.py --emit > /tmp/books-caseI-checked-O.json
cmp EXPECTED.json /tmp/books-caseI-derived-O.json
cmp EXPECTED.json /tmp/books-caseI-checked-O.json
python3 verify.py --damage-controls EXPECTED.json
python3 -O verify.py --damage-controls EXPECTED.json
```

All four emitted mathematical records are byte-identical to the whole
[EXPECTED.json](EXPECTED.json),2497 bytes including final newline:

```text
c664042d58c2162048c90ebda21fe4f9b9a995814e1c2b447f3a353af42677ba
```

Both damage-control commands reject14 damaged records/JSON encodings.
The producer enumerates rows; the checker independently enumerates
columns and counts literal Boolean colors. Neither imports the other
or needs a private corpus. Every run has an unchanged30-second program
guard and was externally guarded at90 seconds, serially in1CPU/2GiB.
An interrupted/guarded run yields no nonexistence claim. Exact measured
times and RSS are in [provenance.json](provenance.json).

The two algorithms are author controls. The ordinary completeness/code
bridge remains unformalized and independent review of this result is
pending. The X-repeated and cross-repeated leaf sectors remain open.
