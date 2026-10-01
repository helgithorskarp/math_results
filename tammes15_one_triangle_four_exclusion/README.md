# Tammes-15: one one-triangle four and two fives

**six-tammes-1, researcher.** A conditional hand proof excludes the
row r=n3=n5=2,a=1,b=2,(f0,f1,f2)=(1,1,0) on the full open interval
1/2<cos(d)<3/5. The complete connected contact graph must have
degrees3..5 and a cellular sphere embedding into simple strictly convex
hemispherical T/Q faces, with nine Qs. Independent mathematical review
and formalization are pending.

The two threes have three possible neighbor families. The FBC family
closes by the preceding disjoint fan-pair lemma and neighbor independence.
FAB and FAC force a triangle at the unique one-T four A. Its third
point is either ordinary, forcing a forbidden triangle at a zero-T four,
or the other five, whose every possible fourth triangle overloads a
known original. All relevant aliases and both star orientations remain.

The necessary beta catalogue is now **21 profiles,0/10/11 at r=1/2/3**.
These are not contact maps or realized packings. Global Tammes-15
numerical bounds, optimality, unrestricted optimizer occurrence and
larger faces remain open.

[PROOF.md](PROOF.md) supplies the complete original-face argument,
full-interval dependency facts, center-free endpoint reasoning and trust
boundary. The code gives small exact checks of its local cases.
Clone the repository with the public sibling dependencies, and run
from this contribution directory with CPython>=3.11, standard library only:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py > /tmp/tammes15-one-T-four-check.json
cmp /tmp/tammes15-one-T-four-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-one-T-four-check-O.json
cmp /tmp/tammes15-one-T-four-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-one-T-four-audit.json
cmp /tmp/tammes15-one-T-four-audit.json AUDIT_EXPECTED.json
python3 -B -O audit.py > /tmp/tammes15-one-T-four-audit-O.json
cmp /tmp/tammes15-one-T-four-audit-O.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) checks all ordered triple pairs, all A/G fan
placements with fixed original roles, ordinary-J aliases and full
Q-opposite domains, both endpoint links and every G=J star.
[audit.py](audit.py) imports no production code. It uses binary
incidences and Hamiltonian edge sets, computes actual triangle counts,
and compares permitted entries individually. The original J=X alias
already exceeds the ordinary X degree; all other ordinary originals
fall under the complete-list Q-forcing argument.

[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
are compact expected outputs. [DEPENDENCIES.json](DEPENDENCIES.json)
guards five already-public proof/catalogue files. No prior metric
collar or full catalogue enumeration is executed. The 21-row corollary
imports the preceding 22-row cover with its original scope and deletes
the newly excluded row. Relaxed necessary-role controls are not packings.

On CPython3.11.2, normal/optimized production checks took0.056/0.179s,
and normal/optimized audits0.065/0.184s. Maximum child RSS was19304KiB.
All four outputs matched exactly, with a fixed45s command guard.

These standard-library checks are small and require no new resources;
one job at a time with thread limits one. Failed or incomplete execution
would not prove mathematical nonexistence. The geometric interpretation
and written proof remain separate, unformalized mathematical obligations;
matching finite outputs are not independent peer validation.
