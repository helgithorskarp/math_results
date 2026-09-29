# A minimum-eight covering at LCM 70560

This directory proves the constructive bound

\[
L_{\min}(8)\leq 70560.
\]

Here the smallest modulus is **exactly eight**, and all moduli are distinct.
The 101 congruences in `cover_m8.json` cover every integer. They are obtained
by a deterministic prime-digit refinement of the 66-class minimum-seven
covering at LCM 10080 in Section 7 of
[Zhang–Zhang, arXiv:2607.19029](https://arxiv.org/html/2607.19029).
The seed is transcribed in `seed_m7.json` and checked directly.

There is also an exact result for a restricted construction family: among
minimum-eight distinct coverings **containing all 65 classes obtained by
deleting the modulus-seven class from that particular seed**, the least
possible LCM is 70560. A capacity obstruction excludes all smaller multiples
of 10080. Thus improving on this bound requires changing at least one of those
65 congruences. This is not a lower bound for unrestricted `L_min(8)`.

The proof, including a reusable refinement and an exact formula for the
capacity of an added congruence, is in [proof.md](proof.md). No originality
claim is made for the elementary refinement operation, and no global
minimality or exhaustive priority claim is made for the resulting covering.

## Reproduction

From this directory, using Python 3.10 or later (tested with CPython 3.12.14):

```sh
python3 construct.py
python3 verify.py
python3 controls.py
```

All commands use only the Python standard library and exact integer
arithmetic. `construct.py` checks that the stored construction and capacity
manifest match its deterministic output. `verify.py` independently evaluates
the congruence predicates for each residue of the actual LCM and recomputes
the extension capacities by explicitly lifting the holes. It does not import
the construction program. `controls.py` checks a smaller known covering and
rejects malformed and incomplete certificates.

Expected summaries are in `expected.json`. In particular, the constructed
cover has LCM 70560, 101 classes, zero uncovered residues, and multiplicity
counts `{1: 45596, 2: 23346, 3: 1614, 4: 4}`. The 65 retained seed classes
leave 252 holes modulo 10080. For LCM multipliers 2 through 6, the maximum
total added-class capacities are respectively 94, 452, 282, 1066, and 1198,
all strictly below the corresponding hole counts.

## Source context and scope

Primary literature checked on 2026-09-29:

- [Zhang–Zhang, arXiv:2607.19029](https://arxiv.org/html/2607.19029)
  supplies the explicit minimum-seven seed and claims `L_min(7)=10080`.
  This work verifies the seed, and does not rely on or reproduce that paper's
  Gurobi-based nonexistence computations.
- [Harrington–Klein–Lowrance–Trifonov, arXiv:2605.18644](https://arxiv.org/html/2605.18644),
  Theorem 1.11, constructs a minimum-eight covering at LCM 172800 using only
  primes 2, 3, and 5. The present covering also uses 7, so it does not improve
  their restricted prime-support result.
- [Klein, arXiv:2508.18062](https://arxiv.org/html/2508.18062)
  / *Integers* 26 (2026), A38, gives the minimum-five and minimum-six results
  and the earlier minimum-seven conjecture. Its preprint introduction
  credits the 15120 minimum-seven example to Krukenberg; the later seed
  paper's introductory attribution differs. Neither attribution is needed
  for the verified construction here.

Targeted searches for minimum-eight coverings and the period 70560 did not
locate this exact application in the searched primary sources. This is a
limited literature comparison, not a proof of novelty or a claim to a record.
The proof and verification depend only on the explicitly supplied seed and
ordinary integer arithmetic; no solver status, floating-point computation,
or omitted large artifact is part of the evidence.

Actual authoring agent: **six-covering-1**, role: **researcher**.
