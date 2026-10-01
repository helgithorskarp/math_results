# Exclusion of the ten-regular 22-vertex Book Ramsey case

Actual author **six-books-3**, role **researcher**, 2026-10-01.

Under the committed local-fourteen exclusion and triangle-free neighborhood
lemma, every hypothetical ten-regular red graph on 22 vertices avoiding
ordinary red B4 and blue B7 is locally Petersen. A new four-column counting
argument forces this: a local four-cycle has total miss-pair capacity at most
eight, whereas its four columns must contribute at least nine pair incidences.
The elementary ten-vertex Moore construction then identifies Petersen.
Hall's existing classification of connected locally Petersen graphs, of orders
21, 63, and 65, excludes the entire regular case.

With the previously committed maximum red degree ten, this also gives
**at most 109 red edges in any unrestricted 22-vertex witness**. The Ramsey
endpoint remains **22 <= R(B4,B7) <= 23**. Irregular candidates remain open.

[PROOF.md](PROOF.md) gives the ordinary argument and all dependencies, including
the external Hall theorem. This new bridge is analytic and unformalized; the
imported local-fourteen theorem has a computer-assisted proof. Independent
review of the present result is pending.

## Reproduce compact validation

Use CPython 3.11, standard library only, from this directory:

```sh
python3 check.py
python3 verify.py
python3 controls.py
python3 -O check.py
python3 -O verify.py
python3 -O controls.py
```

No solver, package installation, network access, or external generated corpus
is needed. Both implementations verify the packing lower bound nine and the
primary 21-vertex construction (93 red edges, red pages at most three; 117 blue
edges, blue pages at most six). They also reproduce the known six triangle-free
cubic ten-vertex classes from the included 60-byte primary graph6 fixture.
This census is validation, not new classification and not a proof premise.

The first program uses eight cross-incidence multigraph profiles and 11 rooted
classes. The independent verifier uses forward stars and all normalized labels
of the six representatives; they cover exactly 21,780 graphs, with class sizes
900, 2160, 2160, 10800, 5400, and 360. The sorted decimal edge-word digest is

```text
89062482c76071a010005eec73dddbd6bf7abcb7ba6b849b3f492bacaaf24c81
```

Five damaged graph/cycle inputs are rejected, and the 19-versus-20 occurrence
boundary is checked. Resource measurements and provenance are recorded in
[provenance.json](provenance.json). No 22-vertex graph was found or claimed.
