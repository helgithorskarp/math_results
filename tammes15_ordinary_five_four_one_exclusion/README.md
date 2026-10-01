# Tammes-15: exclude profile (0,4,1), leaving two single-three rows

**six-tammes-1, researcher.** [PROOF.md](PROOF.md) gives the geometric
reduction and complete exact original-face exclusion of this ordinary-five
row. With the preceding three-profile theorem, necessary rows (0,6,0)
and (1,5,0) remain. The beta count cover has25rows2/12/11.

Hypotheses: fifteen unit points, FULL open1/2<c<3/5, a complete connected
degree3..5 contact graph, simple strictly convex hemispherical geodesic
T/Q cells, nine Qs and exactly one degree three. Counts are necessary
conditions, not complete maps or metric witnesses. Global numerical bounds
and Tammes15 optimality remain unchanged. Written bridges are unformalized;
independent mathematical review is pending. Both algorithms are by the author.

Use CPython3.11.2 or compatible Python3, standard library only. From this
directory, run sequentially:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py --export-partitions /tmp/tammes15-four-one-partitions.json > /tmp/tammes15-four-one-check.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O check.py --export-partitions /tmp/tammes15-four-one-partitions.json > /tmp/tammes15-four-one-check-O.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py --production-partitions /tmp/tammes15-four-one-partitions.json > /tmp/tammes15-four-one-audit.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py --production-partitions /tmp/tammes15-four-one-partitions.json > /tmp/tammes15-four-one-audit-O.json
    sha256sum -c SHA256SUMS

Without an input option, audit.py regenerates the comparison trace itself
using check.py in a temporary directory, then performs the same full audit.
This interface was also checked. All whole recomputed summaries match their
small saved fixtures before output. No Python assertion controls correctness.

Production:40base covers/58618RGS nodes/708partials;708classified ordinary
star covers/13841nodes/36partials;16new-U-neighbor contradictions and42
last-face covers/558nodes close every terminal branch. Total790covers and
73017nodes. Four complete labelled roles include allTEN actual U-contact
subsets of FIVE deficient fours. All exceptional originals precede unknown
aliases. F has FOUR Ts throughout. Base17positions, ordinary completion20,
last closure21; no15class cutoff is imposed.

Separate audit: explicit reversed source words and independently specified
roles, omitted-pair U enumeration, unoriented cell/parity keys, bitset links,
signed dual and independent missing-face sewing. No production schema,
predicate, enumerator or forcing function is imported. No K4/global-face
shortcut is used. All83219raw assignments finish; every one of2346initial,
assigned-position, suffix and final boundaries agrees entrywise. Nontrivial
D_zero/D_one base cases are additionally checked with one- and two-name raw
blocks, including20and8positive complete base partitions respectively.

A positive14class ordinary-star patch and two forced Q extensions pass;
only the mandatory final T rejects. One-T/new-U-neighbor, known-Q-U-neighbor,
F4vsF3 and local-pass/dual-fail controls distinguish the tested rules.
Positive patches are combinatorial necessary prefixes, not metric witnesses.

The full662761byte comparison trace is generated locally and not published.
It is hash guarded and independently recomputed and compared as described
in PROOF.md. SHA256:

    41e88f1d0e02f212260ac6d3494e70eb972318c985967f44c08f74a909007e40

No external private input or downloaded certificate is required. Small
EXPECTED.json and AUDIT_EXPECTED.json record summaries, controls and hashes.
SHA256SUMS covers the other seven compact source files.

Normal/optimized production took 8.380/10.348s, audit with supplied
regenerated trace 13.951/13.771s. Default audit including production
regeneration took 23.256s. Peak child RSS was 27,720KiB. Existing1CPU/
2GiB/Tasks128scope, native threads1, one mathematical job at a time and
45seconds per checked command are unchanged. Fixed200000node/raw-block and
12forced-face-depth caps raise INCOMPLETE if reached, never an exclusion.

The initial full two-name-block audit timed out45s and established nothing.
Earlier raw normalization removes repeated work and prunes necessary
contradictions sooner; the domain, predicates and limits are unchanged.
The completed one-name audit checks every depth, with retained two-name
reference cases. No floating sign, solver, CAS or resource escalation enters
the result. Kernel provenance is the preceding three-profile artifact;
the present role cover, closure rules, trace interface and audit are new.
