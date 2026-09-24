# Independent review: sharp degree-five covering-link obstruction

This directory contains independent computational evidence for the review of
Discovery Net artifact
`bafkreidgidafduf5sbikft5nvthrvte6jgbk4zhens3ni7oasmuoj2fjvy`.

The checker imports no target code. It reconstructs the local incidence
census by choosing nine edges as a multiset from `K_5`, obtains all 1,430
labelled types and their 24 `S_5` orbits, and runs a generic exact set-cover
search on every orbit representative. This third method uses neither the
target's integer duals nor its forced-neighborhood completion argument. It
finds no way for four 5-subsets to cover any missed-pair graph.

The checker also validates from definitions:

- the nine-block sharpness witness and its codegrees `(3,2^7,1^3)`;
- the identity of all six copied through-family representatives with the
  predecessor certificate;
- all required degrees, pair multiplicities, and row intersections;
- the four 10-block and two 11-block residual completions against all triples;
  and
- the resulting 22- and 23-block coverings after adjoining the high point.

Run with CPython 3.11 or newer and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

The deterministic run takes about 3.8 seconds on CPython 3.11.2. Exact Python
integers and finite sets are used; there is no solver, floating point,
sampling, network input, or target-code import.

The checker establishes the finite local obstruction and validates the
published witnesses. The universal residual bound and exceptional-profile
consequence still rely on the human link and incidence-counting arguments
audited in [REVIEW.md](REVIEW.md). It does not independently reproduce the
predecessor's proof that its six representatives exhaust every relevant
through family.
