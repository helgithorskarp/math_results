# Multiplier restrictions at the first two new Schur targets

For a strictly reflection-symmetric classical six-colouring of `[1,n-1]`,
let `G` consist of the units modulo `n` that preserve its colour partition,
allowing permutations of colour labels.

- At `n=538`, `G` has order 2 or 4. An order-four generator can act only as
  the identity, one transposition, or two disjoint transpositions.
- At `n=539`, `G` has order 2 or 4 and **every multiplier fixes every colour**.

These are necessary restrictions on symmetric constructions, **not new bounds
on S(6)**. No six-colouring of `[1,537]` has been found or excluded here.
The remaining group orders are not asserted to be attainable.

The proof combines a general separation of fixed and moved colours on additive
subgroups with a small, exact fibre classification. At modulus 539, the minimum
number of colours with multiplier 67 (order 3) is exactly **9**, and with
multiplier 344 (order 5) it is exactly **10**. Explicit product constructions
attain both values. Their full colour words are included; they are not
six-colour witnesses.

From this directory, using CPython 3.11 or later and no third-party packages:

```sh
python3 -B verify.py
python3 -B check_witnesses.py
sha256sum -c SHA256SUMS
```

`verify.py` must reproduce [expected.json](expected.json), with status
`VERIFIED_COMPOSITE_MULTIPLIER_RESTRICTIONS`. It checks all 524,800 normalized
pairs of subsets of Z/11 for the needed sumset inequality, enumerates seven
possible fibre-size profiles, eliminates the five balanced profiles, checks
the unit-group arithmetic, and verifies the explicit constructions.
`check_witnesses.py` imports no construction code and directly checks every
integer and modular Schur triple, including equal summands, reflection, and
the stated multiplier action.

The full check took about 1.5 seconds and 15 MiB resident memory with CPython
3.11.2 on the research host. Normal and optimized (`python3 -B -O verify.py`)
runs reproduce the same evidence.

The full proof, finite-enumeration completeness arguments, and scope are in
[PROOF.md](PROOF.md). The only imported Schur-number theorem is the established
classical `S(4)=44`; the checker does not reprove it. The other colour lower
bounds follow from an elementary triangle-Ramsey recurrence displayed in the
proof. No solver answer, floating point, unpublished data, or large certificate
is needed for reproduction. Independent researcher review and formalization
are not claimed.
