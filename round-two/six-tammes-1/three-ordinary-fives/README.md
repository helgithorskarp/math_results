# Three ordinary fives excluded from the Tammes-15 nine-Q branch

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) proves that a complete connected fifteen-point contact
graph with degrees3..5 and simple strictly convex hemispherical T/Q faces,
exactly nine Qs and three degree-five vertices cannot have four triangles
at every five, for **1/2<c<3/5**, where c is the minimum-distance cosine.
At least one five must have a triangle deficit. This is an ordinary written
geometric/contact-structure theorem with exact small finite checks. Independent
review and formalization remain pending; global numerical bounds and larger-
face/optimizer coverage are unchanged.

Every three contacts only deficient fours. Those fours have exactly twelve
QQ contact incidences, nine already consumed by the threes. The fives' fans
force either a path or triangle among them. Complete original face links
force at least five further QQ incidences in either case, a contradiction.
The proof retains endpoint/internal reuse, shared opposites and reciprocal
deficient contacts; it never introduces additional actual points.

The public preceding18-row beta source catalogue thereby loses its three
all-ordinary-five r=3 rows, leaving **15 source profiles, split0/7/8**. These
are necessary counts, not realized maps or an exhaustion of all spherical
codes. Older source-only/rejected graph registrations stay distinct. The local
theorem is self-contained and imports no catalogue or external proof data.
See [SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) for exact source/graph distinctions.

From this directory with CPython3.11+ and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B check.py > /tmp/tammes-five-check.json
cmp /tmp/tammes-five-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes-five-check-O.json
cmp /tmp/tammes-five-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes-five-audit.json
cmp /tmp/tammes-five-audit.json AUDIT_EXPECTED.json
python3 -B -O audit.py > /tmp/tammes-five-audit-O.json
cmp /tmp/tammes-five-audit-O.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) exhausts raw fan placements, TT matchings and all remaining
restricted-growth original identifications. [audit.py](audit.py) imports no
primary code and reconstructs the surviving charts through triangle-incidence
Hamiltonian paths; it checks terminal aliases with four-neighbor links and
binary adjacency rows. Complete24-chart sets, all35,118 triangle-terminal
classifications (by exact sorted-record hashes) and all8 path records agree.
The audit is complementary same-author evidence; geometric completeness is
the hand proof, and no independent reviewer verdict is implied.

Normal/-O outputs are byte identical for each checker. Four actual sequential
runs took1.18--1.76seconds each on CPython3.11.2; observed peak child RSS was
25,848KiB, one job/thread under the unchanged1CPU2GiB scope. Fixed55-second
child guards were used; no timeout, UNKNOWN or incomplete enumeration entered
the proof. Nonempty released-common-contact, released QQ-demand and released
zero-T local-link controls are surrogate incidence assignments, not packings.

No solver, float, network, coordinate table or large certificate is required
at runtime. Expected outputs are compact reproduction receipts, not proof
inputs. Written sphere/face/link bridges remain unformalized. Further work
must handle the residual deficient-five cases and larger faces explicitly.
