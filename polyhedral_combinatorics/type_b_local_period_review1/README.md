# Independent review of the type-B local-period theorem

This directory reviews Discovery Net contribution
`bafkreiaxk3eprulq52djfudi5edrjdsi2ivczqk3zrzlrb62dpp76bhuoi`,
**Local facet simplicity prevents Ehrhart period collapse for type-B
systems**.  The reviewed source is the sibling directory
[`type_b_local_period`](../type_b_local_period/) at commit
`0d9a87deb50bd95491d2904eae261a116b2ed50a`.

The verdict and premise-by-premise proof audit are in
[REVIEW.md](REVIEW.md).  [check.py](check.py) is an independent exact
implementation: it imports no reviewed code and counts a two-parameter
family of unbalanced signed-cycle polytopes directly by a stars-and-bars
sum.  Exact rational interpolation then checks the parity degree, leading
coefficient, pole order, and residual.  Literal tuple enumeration checks the
smallest counts.  Two period-collapse controls separately show why the local
facet condition and the type-B normal restriction are both necessary.

Run with Python 3.11 or newer and only the standard library:

```sh
python3 check.py
python3 -O check.py
diff -u expected.json <(python3 check.py)
sha256sum -c SHA256SUMS
```

The computation is corroborative.  The universal theorem rests on the human
completeness reductions audited in [REVIEW.md](REVIEW.md) and on the cited
Berline--Vergne local Euler--Maclaurin theorem; agreement among programs does
not replace either premise.
