# Two shrinking bags can have a growing disk union

Four unit disks give a robust counterexample to a proposed local-volume
gluing rule. Their two three-disk subunions both shrink, their intersection
graph stays the same diamond, and their full union grows.

| Label | Initial center | Final center |
|---|---|---|
| A | (-1/5,0) | (-1/1000,0) |
| B | (1/5,0) | (1/1000,0) |
| C | (0,1001/1000) | (0,6/5) |
| D | (0,-1001/1000) | (0,-6/5) |

All centers within each configuration are distinct. Every pair of disks
intersects except CD, which is strictly disjoint at both endpoints.

The [elementary proof](PROOF.md) establishes

    area(ABC_initial) - area(ABC_final) > 17/500,
    area(ABD_initial) - area(ABD_final) > 17/500,
    area(ABCD_final) - area(ABCD_initial) >= 7/125.

At each endpoint the two bags intersect in exactly the central union AB.
The decrease in that separator's area exceeds the combined decreases in
the two bags. Thus local union-volume inequalities alone cannot be glued
across a moving two-ball separator, even with unchanged overlap graph.
The invariant singleton-ball separator case follows from elementary
inclusion-exclusion.

This **is not a counterexample to Kneser--Poulsen**: AC, AD, BC, BD and
CD center distances increase. Nor does it disprove a gluing theorem that
retains pairwise contraction or quantitatively controls the separator.
The need for separator compensation is already explicit in Gorbovickis's
central-set paper. Our contribution is the small rational realization
with strict margins and reproducible evidence; see [attribution](REFERENCES.md).

## Reproduce

Run from this directory with Python 3.11+ (validated with 3.11.2):

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c MANIFEST.sha256
```

There are no external packages or inputs. The verifier reads
[fixtures.json](fixtures.json), bounds eight union areas with integer
inner and outer rectangle covers, and compares every output field with
[expected.json](expected.json). It also checks reflection, rotation,
translation, coincident-disk and single-disk controls, and rejects the
identity and reversed transitions as witnesses for the stated signs.
The run uses 256080 strips across the witness and controls, about
1.5 seconds on the development host. `--emit` prints the deterministic
summary without comparing it to the expected file.

For orientation, the exact enclosures imply that each local loss lies
between 0.295 and 0.298, whereas the global gain lies between 0.196 and
0.199. These decimal intervals are coarse rational consequences of the
printed fractions, not floating-point area estimates.

The written geometric proof is independent of the strip-cover method.
Both remain unformalized and were not independently peer reviewed at
publication. No search completeness, solver output, or floating-point
assumption is used. The result closes this precise inference rule; no
parameter census or general contraction theorem is claimed.
