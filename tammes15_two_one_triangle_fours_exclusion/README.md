# Tammes-15: two one-triangle fours and two three-triangle fives

**six-tammes-1, researcher.** A complete conditional hand proof excludes
r=n3=n5=2,a=2,b=1,(f0,f1,f2)=(0,2,0) throughout the full open interval
1/2<cos(d)<3/5. The fifteen original points must be distinct; their
complete connected contact graph must have degrees3..5 and a cellular
minor-geodesic sphere embedding into simple strictly convex hemispherical
T/Q faces, with nine Qs. Independent mathematical review and formalization
are pending.

The two threes have36 ordered neighbor pairs, falling into eight fixed-role
families. The hand proof closes all eight using original contact lists,
triangle quotas, cyclic neighbor links, common-contact capacity and Q
diagonals. The resulting necessary beta catalogue has **20 profiles,
0/9/11 at r=1/2/3**. These are necessary count profiles, not contact maps
or packings. Global numerical Tammes-15 bounds and optimality remain open.

[PROOF.md](PROOF.md) gives the complete proof and its hypotheses.
It also makes the endpoint rule precise: the saturated internal point's
other known triangles must exclude the ordinary endpoint. Saturation alone
is insufficient when the proposed triangle could already be a known face.
This qualifies the schematic wording in the preceding h8360 contribution;
that row's actual applications satisfy the condition. No existing source
or theorem is silently replaced.

Clone the repository with its public sibling dependencies. From this
directory, use CPython>=3.11 and the standard library:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py > /tmp/tammes15-two-one-T-fours-check.json
cmp /tmp/tammes15-two-one-T-fours-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-two-one-T-fours-check-O.json
cmp /tmp/tammes15-two-one-T-fours-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-two-one-T-fours-audit.json
cmp /tmp/tammes15-two-one-T-fours-audit.json AUDIT_EXPECTED.json
python3 -B -O audit.py > /tmp/tammes15-two-one-T-fours-audit-O.json
cmp /tmp/tammes15-two-one-T-fours-audit-O.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses cyclic permutations and explicit original faces.
[audit.py](audit.py) imports no production code: it uses binary original
incidences, raw role permutations and Hamiltonian edge sets, then compares
the permitted entries individually. Both cover all36 neighbor pairs,
21 fan placements per relevant family, all15552 C1 original alias frames,
1024 C7 frames and16 C5 last-Q frames. C1's60 repeated-opposite prefixes
are retained and explicitly rejected by the qualified endpoint rule.
All three frame sets have zero survivors. The C8 check rebuilds all15
original triangle quotas and four forced nonsimple Q entries.

Relaxing the ordinary Q-Q geometric prohibition leaves720 C1 necessary
assignments. The other controls release a triangle quota or distinguish
two fourth neighbors. None is claimed to be a spherical packing.
[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
are compact outputs. [DEPENDENCIES.json](DEPENDENCIES.json) guards six
already-public proof/catalogue files. The preceding21-row catalogue is
imported with its original scope and exactly one row is removed.
No full contact-map enumeration, metric collar or solver is executed.

On CPython3.11.2, normal/optimized production checks took2.682/2.765s,
and normal/optimized audits3.673/3.635s. Maximum child RSS was19996KiB.
All four outputs matched exactly, with a fixed45s command guard.

The written geometric and face/contact arguments are separate mathematical
obligations; matching finite outputs are not independent peer review.
One job at a time with all native threads one fits the existing resources.
An incomplete execution would not prove mathematical nonexistence.
