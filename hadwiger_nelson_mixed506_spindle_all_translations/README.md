# All translations of mixed506 at (7+i sqrt(15))/8

For fixed `u=(7+i sqrt(15))/8`, every complex translation of
`B292 union (u V214+h)` is four-colourable, where
`B292=A159 union ((5+i sqrt(11))/6)A159`. Disjoint placements have 506
vertices. [PROOF.md](PROOF.md) combines the prior overlap certificate
with this complete disjoint-placement result. No five-chromatic graph
or record improvement is obtained. Other rotations and inner constructions
remain outside the result.

Three cross contacts force the translation into `K=E(sqrt(5))`.
An exact two-circle criterion then gives a finite census:

- 76,612,202 nonzero pairs of source differences;
- 7,028 pairs with certified circle intersections in `K`;
- 1,438,349 distinct disjoint translations in `K` having at least two
  contacts, all supplied with checked four-colourings;
- 318 rejected square-root cases, each independently certified modulo 29.

Translations outside `K` have at most two contacts and are coloured by
permuting the source colours. This is a proof for arbitrary complex
translations, not an assumed algebraic search. The largest cross-edge
count at this fixed rotation is 16.

An independent implementation checks the full modular scan, every circle
certificate, every projected translation and every colouring witness.
Its Cartesian representation and source reconstruction differ from the
producer's. One former colouring-library residual also receives a full
strict-distance check on all 127,765 pairs of its 506 physical vertices.
A single positive SAT query supplied two new component rows, totalling
508 bytes; no solver is needed for proof replay.

## Reproduce the certificate

Use a complete repository checkout and CPython 3.11.2 or compatible Python
3.11. From this directory, choose a work path that does not already exist:

```sh
python3 verify.py --work /tmp/hn-spindle-all > /tmp/hn-spindle-result.json
cmp expected.json /tmp/hn-spindle-result.json
python3 audit.py --work /tmp/hn-spindle-all > /tmp/hn-spindle-audit.json
cmp expected_audit.json /tmp/hn-spindle-audit.json
python3 controls.py > /tmp/hn-spindle-controls.json
cmp expected_controls.json /tmp/hn-spindle-controls.json
sha256sum -c SHA256SUMS
```

Both enumeration and audit use only the Python standard library. The audit
reads the producer's proposed centres as certificates, checks their exact
geometry and completeness, and independently proves every negative answer.
It compares the full regenerated translation/colouring stream entry by
entry, not merely by counts. The proof imports the preceding
[overlap certificate](../hadwiger_nelson_mixed505_spindle_rotation/README.md),
whose separate reproduction commands remain available there.

The work directory contains generated state, including an 85,070,356-byte
translation stream. Keep it outside the repository. Full runs use substantial
memory: the exploratory projection process was observed at 1,278,496 KiB
RSS; this is an observation rather than a measured maximum. Its projection
stage took 67.106 seconds. The complete independent Python modular scan took
65.196 seconds in a separately measured run. These figures describe the
producing host, not runtime limits or required output.

## Optional accelerated first screen

The first screen can use the included C++17 program. The remaining exact
classification, projection and positive cover are unchanged. GCC 12.2.0
was used with the following flags:

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -pedantic filter.cpp -o /tmp/hn-spindle-filter
python3 verify.py --native /tmp/hn-spindle-filter --work /tmp/hn-spindle-native > /tmp/hn-spindle-native-result.json
cmp expected.json /tmp/hn-spindle-native-result.json
python3 audit.py --work /tmp/hn-spindle-native > /tmp/hn-spindle-native-audit.json
cmp expected_audit.json /tmp/hn-spindle-native-audit.json
```

The native full screen took 3.906 seconds in the measured exploratory run.
Its complete output matched the independent Python scan. The checking build
used `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer` and matched
565,632 reference pairs. Numeric bounds and trust distinctions are in the
proof. `validation.json` records the performed comparisons and controls.

## Optional positive-witness discovery

With `python-sat==1.8.dev24` and CaDiCaL195 available, use another new path:

```sh
python3 discover.py --out /tmp/hn-spindle-positive
cmp new_B.txt /tmp/hn-spindle-positive/new_B.txt
cmp new_V.txt /tmp/hn-spindle-positive/new_V.txt
```

This makes one bounded query for the fixed former residual. The producing
query returned SAT in 0.093 seconds under a one-million-conflict budget.
A repeated run produced identical source rows. `solver_provenance.json`
records the exact translation, contact labels, encoding dimensions and
CNF array hash. Only explicit positive colourings enter the proof.

`SHA256SUMS` pins the package and transitive source/data dependencies.
These checks are by independent author implementations; external review
and proof-assistant formalization are not claimed. No large certificate,
solver trace, binary, or private state is committed.
