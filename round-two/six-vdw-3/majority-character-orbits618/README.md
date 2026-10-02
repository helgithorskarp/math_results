# Three-character majority at period618 needs nine column repairs

**six-vdw-3, researcher.** An exact computer-assisted family obstruction
for symmetric two-color/seven-term van der Waerden research.

For all three affine nonzero quadratic-character inputs over F103,
their Boolean majority, any six-row phase and both output palettes,
an AP7-free coloring on Z618 or [1,N], N>=2472, needs at least nine
edited nonroot field columns. All original root columns are free and
edited/root colors may be nonperiodic. Repeated-root cases use the
previous affine-character theorem and have stronger15/16 bounds.

The404 distinct-root normalized states form exactly69 parameter orbits
under the specified S3 root/palette action. The compact certificate gives
nine disjoint actual APs at every representative. A separately implemented
checker verifies all404 transported packs, actual color exchanges and
short orbits. The proof also supplies the necessary masked-distance cut
9-e<=d<=91 and majority correlation bound82+e for arbitrary XOR618
words with zero through three holes, where e counts holes outside the
three reference roots.

Read [PROOF.md](PROOF.md) for exact quantifiers, ordinary proof bridges,
dependencies and scope; [VALIDATION.md](VALIDATION.md) for counts and
trust boundaries. This is not a3704 coloring, a numerical W improvement,
an optimal repair bound or an exclusion of every XOR618 word.

Reproduce using CPython3.11 or later, standard library only:

```sh
python3 reproduce.py --work /tmp/majority618-fresh-check
```

The work directory must initially be empty and outside this source
directory. The wrapper checks [SOURCE_PINS.json](SOURCE_PINS.json), runs
producer/checker serially in normal and optimized modes, imposes a fixed
20-second guard on each child and compares the complete generated
[certificate.csv](certificate.csv) and [expected.json](expected.json).
The resulting status is `FRESH_COMPLETE_MAJORITY618_SOURCE_RECONSTRUCTION`.
On a slower machine a timeout means reproduction is incomplete; it is
not mathematical evidence against the stated claim.

The checker can also be run directly on a supplied certificate:

```sh
python3 check.py --certificate certificate.csv --out /tmp/majority618-checked.json
```

Its successful status is `EXACT_MAJORITY618_69_ORBITS_REPAIR_AT_LEAST9`.
The implementation independence is by the same author, not external peer
review. External review of the earlier affine dependency does not certify
this new finite majority census.
