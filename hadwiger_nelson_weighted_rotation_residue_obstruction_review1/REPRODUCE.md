# Reproduction

The principal audit needs CPython 3.11 or later and a C++17 compiler. From
the repository root, use a fresh directory:

```sh
review_tmp=$(mktemp -d /tmp/hn-weighted-review.XXXXXX)
python3 -B hadwiger_nelson_weighted_rotation_residue_obstruction_review1/independent_audit.py \
  --prepare "$review_tmp/input"
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -pedantic \
  hadwiger_nelson_weighted_rotation_residue_obstruction_review1/independent_contacts.cpp \
  -o "$review_tmp/contacts"
"$review_tmp/contacts" < "$review_tmp/input/differences.txt" \
  > "$review_tmp/contacts.txt"
python3 -B hadwiger_nelson_weighted_rotation_residue_obstruction_review1/independent_audit.py \
  --contacts "$review_tmp/contacts.txt" --check-expected
python3 -O -B hadwiger_nelson_weighted_rotation_residue_obstruction_review1/independent_audit.py \
  --contacts "$review_tmp/contacts.txt" --check-expected
python3 -B hadwiger_nelson_weighted_rotation_residue_obstruction_review1/controls.py \
  --contacts "$review_tmp/contacts.txt" \
  | diff -u hadwiger_nelson_weighted_rotation_residue_obstruction_review1/EXPECTED_CONTROLS.json -
```

For the checked-in undefined-behaviour control:

```sh
g++ -std=c++17 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all \
  -Wall -Wextra -Wconversion -pedantic \
  hadwiger_nelson_weighted_rotation_residue_obstruction_review1/independent_contacts.cpp \
  -o "$review_tmp/contacts-ubsan"
"$review_tmp/contacts-ubsan" < "$review_tmp/input/differences.txt" \
  > "$review_tmp/contacts-ubsan.txt"
cmp "$review_tmp/contacts.txt" "$review_tmp/contacts-ubsan.txt"
```

The auxiliary lower bound requires CaDiCaL 1.9.5 and `drat-trim`. The CNF is
generated independently by the review script. CaDiCaL's UNSAT exit code is
20:

```sh
set +e
cadical "$review_tmp/input/auxiliary.cnf" "$review_tmp/auxiliary.drat"
cadical_status=$?
set -e
test "$cadical_status" -eq 20
drat-trim "$review_tmp/input/auxiliary.cnf" "$review_tmp/auxiliary.drat" \
  | grep 's VERIFIED'
```

The recorded review proof had 495,355 bytes and SHA-256
`dd926c453010d146020cd45a81b67ccdefde82cd9a2ae68925100ee71afcfc6e`.
It is transient and deliberately not committed. The canonical mathematical
input is the 26,431-byte CNF with SHA-256
`4f308ac0cc7ba3aecb51ae36464ec79eabf7af1f77f703ce925157bc4cb7e8f7`.

The secondary symbolic audit uses SymPy 1.14.0:

```sh
python3 -B hadwiger_nelson_weighted_rotation_residue_obstruction_review1/symbolic_audit.py \
  | diff -u hadwiger_nelson_weighted_rotation_residue_obstruction_review1/EXPECTED_SYMBOLIC.json -
```

Finally run the manifest:

```sh
(cd hadwiger_nelson_weighted_rotation_residue_obstruction_review1 && sha256sum -c SHA256SUMS)
```

The review imports the target's compact positive auxiliary certificate and
the existing hash-bound Parts coordinate table. It imports no target code and
does not read the target quotient certificate or contact list. The C++ scan
checks every one of the `11,651^2=135,745,801` ordered difference pairs from
the defining weighted-coordinate formula.
