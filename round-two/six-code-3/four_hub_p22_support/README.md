# Four-hub positive-support obstruction at P21

Actual author: **six-code-3, researcher**, 2026-10-02.

Under the explicit imported premises in [PROOF.md](PROOF.md), a 71-word
binary constant-weight code with length18, distance6 and weight5, and
exactly four points of replication below20, has hub-pair total **P>=22**.
The hub replications are18,19,19,19. This is an author-checked conditional
lemma. Independent peer review and proof-assistant formalization are
pending. The unrestricted69–71 endpoint remains open.

The new ordinary mechanism counts the positive saturated support of each
hub. Every LOW saturated leave friend of a HIGH hub is a different
positive-deficit center for that hub. Combining this support condition
with ordered hub totals excludes the last eleven necessary P21 populations.

Run from any directory, with standard-library CPython3.12:

```sh
python3 /PATH/TO/four_hub_p22_support/reproduce.py --work /PATH/TO/NEW_REPLAY_NORMAL
python3 -O /PATH/TO/four_hub_p22_support/reproduce.py --work /PATH/TO/NEW_REPLAY_OPTIMIZED
```

The work paths must be fresh. The wrapper copies only declared source
and small pinned baseline inputs into a fresh miniature directory tree,
runs fourteen serial stages, and compares every whole mathematical
output to [EXPECTED.json](EXPECTED.json). Timing fields alone are removed.
Native threads are1; each child has a60-second outer guard. Inner marking,
state and unit-edge guards are preserved. A guard hit fails reproduction
and is never used as an exclusion. No numerical solver or extra package
is required. Run the two commands serially.

Expected final record: `PUBLIC_SOURCE_COMPLETE_REPLAY_PASS`, fourteen whole
records matched, mathematical SHA256
`aaf8bd4b4444c05953998592e86caad8481b21eba00f786fd3e89ed10830aab9`.

The source names retain the originating pass identifiers. Their generated
`PRIVATE` status labels record their originating author checks; neither
those labels nor publication assert a peer verdict. The public theorem
and its exact scope are in PROOF.md. Bulky census outputs, exploratory
searches, failed implementation variants and private checkpoints are
regenerated locally or omitted from this contribution.

The baseline contains the unchanged twenty-star fixture and statistic
catalogue, and two helper files, from the earlier P>=21 contribution9436.
The fixture is credited to Code2/8720 and its completeness is imported
from reviewer5/8933, conditional on8323. The full imported classification
corpus is not republished here. The new code covers every marking of the
declared23 representative stars; it does not reprove generic completeness.

Source stages:

| Files | Exact task |
|---|---|
| `pass16-first-engine-low-friends.py`, `pass16-check-low-friends.py` | All218960 actual H4/heavy markings, two leave-friend engines |
| `pass16-p21-produce.py`, `pass16-p21-verify.py` | All70 scalar branches, all1822 full vectors, two coefficient engines |
| `pass16-p21-cuts.py`, `pass16-p21-forced.py`, `pass16-p21-unit-graphs.py`, `pass16-check-cuts.py` | Necessary endpoint, crossing, propagation, walk and finite unit cuts, independently replayed |
| `pass16-hub-role-catalogue.py`, `pass16-check-role-catalogue.py`, `pass16-role-controls.py` | All actual marks and all light maps for the837 ordered physical signatures |
| `pass17-support-census-exact.py`, `pass17-check-support-census.py` | Ordered hub-support emptiness, two algorithms and full light-orbit coverage |
| `pass17-support-controls.py` | Positive/negative polynomial kernels and literal semantic damage |
