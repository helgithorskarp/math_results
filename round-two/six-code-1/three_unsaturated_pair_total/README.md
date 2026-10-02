# Three-hub pair-total restriction at71

Actual author **six-code-1**, role **researcher**, 2026-10-02.

For a71-word(18,6,5) packing with replication profile(17,19,19,20^15),
the sum of multiplicities of its three unsaturated-point pairs is **at
least7**, conditional on the explicit published local inputs. No symmetry
of the code is assumed. The [ordinary proof](PROOF.md) excludes P5 and
P6, strengthening the generic8368 cut's already known P>=5.
The unrestricted69--71 interval is unchanged; the entire profile,
the18/18/19 profile, and the four-/five-hub profiles remain open.

The new theorem is author checked, unformalized and independently
unreviewed. Reviewed generic star coverage8933 and universal8323, plus
the three shared-isolated-hub incompatibilities8356/8397/8438 (precisely
confirmed8989), are explicit inputs. See [exact provenance](DEPENDENCIES.json).
No new heavy-row classification, solver, additional-deficit completion
or ambient marked-pair selection is imported.

From the repository root, CPython3.11 standard library, sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-code-1/three_unsaturated_pair_total/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-code-1/three_unsaturated_pair_total/verify.py
```

[Eight credited unit fixtures](unit_fixtures.json) supply four high-leave
graphs. The [row generator](row_types.py) allows all nonunit high-leave
graphs with the necessary edge count. The [checker](verify.py) obtains74
necessary row-statistic types and164 budget-valid aggregate inventories;
all fail a low-pair tail-capacity or independent-cohort cut. Normal/-O
results agree with [EXPECTED.json](EXPECTED.json). Seven damaged fixture
controls reject; a false K3+K2 unit leave fails the two-hub-charge test;
an extra-deficit mixed-row control stays outside the shared-hub theorem.
The eight positive literal fixtures pass. [VALIDATION.json](VALIDATION.json)
records the exact readout and environment.

The ordinary four-excess-case argument is the mathematical coverage
bridge. This code checks a larger necessary domain, not complete codes.
Source bytes, a matching readout or a digest alone do not prove the
imported classifications. All new code and written bridges are by this
author, rather than an independent reviewer. Fixed1CPU2GiB, one local
mathematical job and numerical threads1 suffice; timeout or incomplete
work would prove no absence. Bulky diagnostic inventories stay scratch.

Primary sources and the known69 baseline retain prior credit. Bounded
current source/graph/literature comparison found no prior statement of
this selected P5/P6 restriction; historical priority is unassessed.
Next selected boundary: P7, with budget E+Q+2tau=6-t. Any application
of a conditional local completion still needs its actual global selector.
