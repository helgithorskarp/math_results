# Excluding the exceptional degree profile for C(13,6,3)

**A twenty-block `(13,6,3)` covering cannot have point-degree profile
`(12,9^12)`.** Consequently every twenty-block covering has profile
`(10^3,9^10)` or `(11,10,9^11)`.

The result closes the entire exceptional profile, including the previously
unresolved maximum-intersection-three and maximum-intersection-four cases.
It does **not** exclude the other two profiles or determine `C(13,6,3)`;
the unrestricted bounds remain 20–21.

The new finite theorem excludes a precisely stated pair of regular
incidence families. Its application to coverings imports the previously
proved optimal-link degree bound and through-triple multiplicity bound.
See [PROOF.md](PROOF.md) for every assumption and [SOURCES.md](SOURCES.md)
for the dependency and review boundaries.

## Proof mechanism

A low point's complete nine-block link reduces to five four-subsets and
four five-subsets on eleven points. The required through incidence systems
have **736** isomorphism types. Only **22** admit a completion. Their **72**
labelled completions give **36** pointed-link classes.

Each such link has another point of through multiplicity at least three.
Joining complete links at those two points gives only **254** compatible
partial global systems. Every survivor has seven through blocks and seven
away blocks. Of these, **142** cannot reach the required away degrees with
one more block. In the other **112**, the last away block is forced.

Those 112 cases have small nonnegative integer weights on still-uncovered
pairs and triples. If their total weight is `W` and a possible remaining
five-subset has capacity at most `M`, direct exhaustive checks give
`W > 5M`. Five remaining through blocks therefore cannot finish the cover.
Weights are at most five; the entire weight certificate is approximately
23 KB. All 252 possible remaining five-subsets are checked in every case.

## Reproduction

Use CPython 3.11 or newer, standard library only, from this directory:

```bash
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 audit.py > actual_audit.json
diff -u AUDIT_EXPECTED.json actual_audit.json
python3 -O controls.py > actual_controls.json
diff -u CONTROLS_EXPECTED.json actual_controls.json
sha256sum -c SHA256SUMS
```

The main status is `VERIFIED_NO_EXCEPTIONAL_12_9_PROFILE`.
The independent status is `INDEPENDENT_AUDIT_NO_EXCEPTIONAL_PROFILE`.
The main verification takes approximately 50 seconds and 28 MiB on the
recorded host; the independent audit takes about 105 seconds and 25 MiB.
Exact measured resource costs and interpreter checks are in `VALIDATION.json`.
Neither computation has a time limit, node cutoff, or heuristic failure exit.

The audit uses a different through-system census, a dual point-signature
completion algorithm, and direct point-bijection matching. It uses all 72
labelled link roots rather than the 36-class quotient. It closes its final
cases by exact set cover without reading the integer weight certificate.

## Files

- `census.py`, `local.py`, `complete.py`: complete local classification.
- `symmetry.py`, `glue.py`: explicit automorphisms and two-link compatibility.
- `finish.py`, `weights.json`: small integer closure certificates.
- `verify.py`: complete primary proof computation.
- `controls.py`: all 72 definition-level positive witnesses and three
  deliberately corrupted witness/certificate controls.
- `audit_census.py`, `audit_local.py`, `audit_glue.py`, `audit.py`:
  independent census, completion, joining, and final exclusion.
- `LOCAL.json`, `LINKS.json`: small, regenerated local fixtures; they are
  checked against complete enumeration rather than accepted as input truth.
- `EXPECTED.json`, `AUDIT_EXPECTED.json`, `VALIDATION.json`, `SHA256SUMS`:
  expected outputs, provenance, and integrity checks.

## Scope and trust

The new finite computation uses exact integers and finite exhaustive loops.
No solver, LP library, graph-isomorphism package, network input, generated
CNF, or large certificate is required. Floating-point LP was used only to
discover the final weights; their published verification is entirely exact.

The written reductions, algorithms, Python runtime, and hardware remain
trusted. The audit is an internal independent proof architecture, not
external peer review or proof-assistant formalization. External review of
the new theorem is pending. In particular, the application imports the
earlier through-triple exclusion and its upstream proof obligations; this
packet does not independently reproduce that predecessor's SAT corpus.
