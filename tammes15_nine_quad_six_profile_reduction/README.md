# Tammes-15: a sixteen-point face obstruction

Author: **six-tammes-1**, role: **researcher**.

Under the complete connected fifteen-point T/Q contact-graph hypotheses
in [PROOF.md](PROOF.md), exactly one degree three and profile
`(delta,a,b)=(2,2,1)` are impossible. All three necessary original-face
prefixes force sixteen distinct points, after every vertex alias is
allowed. This leaves six r1 profiles on `1/2<c<3/5`, and29necessary
profiles6/12/11 on the earlier beta interval with its stated dependencies.
No global separation improvement or unrestricted optimality is claimed.

The small integer-only [checker](check.py) exhausts equality partitions
of two sixteen-slot face patches. [audit.py](audit.py) uses full raw
label tuples, unoriented link graphs and a signed dual orientation
system, and compares every normalized early and final partition with
the production fixture. The role-free paired patch lemma covers both
paired prefixes. The one-paired patch uses its prescribed triangle roles.

CPython>=3.11, standard library only. Run from this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > replay-audit.json
cmp replay-audit.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

Set solver/BLAS/OpenMP thread variables to1 when reproducing in a
shared research environment. Execute these jobs sequentially.
The audit enumerates300,625raw tuples; no large certificate, external
package, solver or private input is required.

Both algorithms are by the author; independent mathematical review and
formalization remain pending. Original face forcing and its translation
to partial vertex links remain a written trust boundary. A sixteen-slot
positive consistency control is not asserted to be a realizable packing.
An eleven-class nonorientable quotient is included to verify the
essential sphere-orientation condition.
