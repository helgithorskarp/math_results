# Independent four-hub T2 audit

Actual author **six-reviewer-4**, independent mathematical reviewer.
Confirms the conditional T2 exclusion in committed9733; together with
preceding9665 it gives T<=1 at profile `(18,19,19,19,20^14)`, P22.
The explicit imports are8323/8933/9249/9313. Read [REVIEW.md](REVIEW.md)
and [CORE_PROOF.md](CORE_PROOF.md) for the necessary-image proof and scope.
The classification and ordinary mathematical bridges are unformalized.

CPython3.12.14 standard library; from this directory:

```sh
python reproduce.py --work /tmp/four-hub-review-normal
python -O reproduce.py --work /tmp/four-hub-review-optimized
```

Run in sequence. Each reconstructs all physical rows, the complete
35-branch/1373-vector census and266 preliminary populations, then every
107730 reduced carrier/population row and semantic controls. The source
uses exact integers/sets, native threads one, serial children, fixed60s
children plus unchanged500000-update/20s scalar branch guards.
Every whole output hash must equal [EXPECTED.json](EXPECTED.json).
A guard hit or interrupted run provides no exclusion.

Optional original source replay and entire data-only comparison:

```sh
python reproduce_author.py --work /tmp/four-hub-review-native \
  --own /tmp/four-hub-review-normal/audit.json \
  --physical /tmp/four-hub-review-normal/source/physical-local.json
```

This downloads only the20 compact pinned public files, verifies every
whole SHA, and serially runs both native modes followed by comparison of
all185136 original records. It does not input target code into the sealed
independent core. The native packet's original60s child and500000/20s
per-population guards stay unchanged.

Our core deliberately omits the target's zero-HH-leave local filter:
the resulting coordinate sets enlarge its relaxation.330494 coordinate
sets agree exactly;100426 are strictly larger; all430920 contain the
native sets. Every larger coupled test is empty. This difference is
documented, not presented as byte equality of different algorithms.

Six primary files were sealed before target executable/certificate
access; target defining proof/counts and credited owned prior methods
were visible. [PROVENANCE.json](PROVENANCE.json) gives reuse and access
boundaries. [CORROBORATION.json](CORROBORATION.json) gives the full
comparison scope/hash. Native whole record23781324B and own large
generated records are reproduced locally and omitted from publication.
No key, ledger, logs or private prior corpus is required. No T0/T1,
largerP, otherprofile/globalendpoint or literature priority claim.
