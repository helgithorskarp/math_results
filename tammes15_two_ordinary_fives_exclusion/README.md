# Two ordinary fives in the nine-quadrilateral branch

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) excludes the complete row
`r=2,a=2,b=2,f=(2,0,0)` on the full open interval `1/2<c<3/5`.
Here c is the cosine of the minimum geodesic separation of fifteen
distinct unit points. Their complete connected contact graph has
degrees3..5 and a cellular minor-geodesic sphere embedding into simple
strictly convex hemispherical T/Q faces, with nine quadrilaterals.
The row has two zero-T threes, two four-T fives, two one-T fours, two
zero-T fours and seven ordinary two-T fours.

All three relationships between the fives are covered. Opposite fives
in a shared Q would require eight distinct ordinary fours. Noncontacting
fives with distinct Qs force a full ordinary F-fan internal to be a
G-fan endpoint. Contacting fives force a Q at a full shared ordinary
point; the opposite's three contact and complete degree-four links
then close both its zero/one-T possibilities. Every unknown Q opposite
retains all fifteen actual original aliases. The older shared-fan
alignment is explicitly credited; its exclusion theorem, which assumes
thirteen fours and no threes, is not applied here.

The hand proof and small exact checks remove exactly one row from the
preceding checked [19-profile source](../tammes15_four_two_triangle_fives_exclusion/PROOF.md),
verified commit `4861a67cd96e3eb9e8ea38f1e41102c772a95e92`. This leaves
**18 beta profiles, split0/7/11 at r=1/2/3**, under that catalogue's
inherited hypotheses. The geometric, original-face and coverage bridges
remain written and unformalized. Independent mathematical review is
pending. Global numerical Tammes15 bounds, unrestricted optimizer
occurrence, larger-face coverage and optimality remain open.

This is a source publication. No new graph attempt or commitment is
asserted. The preceding19-profile source also had no graph attempt;
the preceding20-profile source's original registration was rejected
and remains uncommitted. The last actually committed graph cover is
**21 profiles at h8360**, source
`8e69194e595ae7411d3624537473870f67ff79c8`, graph reference
`bafkreicjsndjhrckpkt2flkpfa7pawhzyb6k4k6xpecudodmdmfvqb2aue`.
The exact rejected registration is retained in the private checkpoint.
It has not been retried or stripped of known relations.

From this directory, with CPython3.11 or newer and only its standard
library:

```sh
python3 -B check.py > /tmp/tammes15-two-ordinary-check.json
cmp /tmp/tammes15-two-ordinary-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-two-ordinary-check-O.json
cmp /tmp/tammes15-two-ordinary-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-two-ordinary-audit.json
cmp /tmp/tammes15-two-ordinary-audit.json AUDIT_EXPECTED.json
python3 -B -O audit.py > /tmp/tammes15-two-ordinary-audit-O.json
cmp /tmp/tammes15-two-ordinary-audit-O.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses cyclic neighbor words, canonical actual face
sets and complete contact lists. [audit.py](audit.py) imports no production
code; it uses Hamiltonian edge sets, binary incidences, union/find link
components and five-bit internal-subset pairs. This is a different
same-author representation, not an independent mathematical reviewer.
Both compare all permitted entries, including the full3600-entry
opposite-five common-contact matrix and terminal alias matrices.

The finite checks cover12 ordered three-neighbor pairs/3 role families,
144 shared-fan pairs/32 necessary permitted charts,3600 opposite-five
original assignments,105 noncontact endpoint/internal assignments,
60 one-T opposite K assignments,30 forced ordinary-end T assignments,
and1800 zero-T K/O assignments. Both associations of the one-T endpoint's
three are retained. Cross-fan identifications and the K=Y two-corner
link are checked explicitly. Thirty pre-final-Q assignments and20
terminal assignments with the three-neighbor restriction released
provide nonempty controls; they are not spherical packings.

[DEPENDENCIES.json](DEPENDENCIES.json) guards ten public sibling proof
and catalogue files by SHA256. The preceding19-profile catalogue is
imported and exactly one row is removed; it is not regenerated.
No private input, solver, floating-point sign, metric collar or packing
enumeration is used. [EXPECTED.json](EXPECTED.json) and
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) are compact expected outputs.

Recorded CPython3.11.2 runs: production normal/-O0.262/0.376s,
separate audit normal/-O0.352/0.623s; maximum child RSS20044KiB.
All four complete outputs match their expected files byte for byte.
The production output is62036bytes, SHA256
`f376a4cdebfad5e8d0e3eef5e52e7755ee0a151c25148e3695b639d9b425944a`;
the audit output is936bytes, SHA256
`6d5a5ecdd68e36cf31dcc6b785253469d917bed0e1ca8ea6212be99b0363f79e`.
Each run used a45s outer guard, one local job at a time and one
native/BLAS/OpenMP thread within the existing1CPU/2GiB researcher scope.
