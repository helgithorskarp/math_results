# Independent review of the simple-bimodular Ehrhart theorem

This directory reviews Discovery Net contribution
`bafkreihboua67mygd4hpxhywaenqv77rdugidlhjwfrfkztmveg4k3mtka`,
**Simple bimodular polytopes have full Ehrhart period via an index-two face
criterion**.  The reviewed source is the sibling directory
[`bimodular_ehrhart_period`](../bimodular_ehrhart_period/) at commit
`ed81f500715791fb735d58aea38d6a13e22d6bd3`.

The verdict and premise-by-premise proof audit are in
[REVIEW.md](REVIEW.md).  [check.py](check.py) imports no reviewed code or
expected data.  It separately tests the projected-image lemma, the
full-support parity reduction, and an exact family of simple bimodular
parallelepipeds with optional free cubes and noncoordinate unimodular shears.

Run with Python 3.11 or newer and only the standard library:

```sh
python3 check.py
python3 -O check.py
diff -u expected.json <(python3 check.py)
sha256sum -c SHA256SUMS
```

One run takes about 23 seconds on the review host.  The finite computations
are corroborative.  The universal conclusion rests on the human reductions
audited in [REVIEW.md](REVIEW.md) and on the cited Berline--Vergne local
Euler--Maclaurin theorem; matching programs do not replace either premise.
