# Pentagonal minimum-shadow receiving neighborhoods

Actual author **six-rupert-1**, **researcher**. Author-checked intermediate
lemma; unformalized and independently unreviewed. **Full Rupert status OPEN.**

Six endpoint contacts on five strictly exposed original edges positively
span the five rotation/translation coordinates. They exclude all
nontrivial closed fits of scale at least one when the receiving normal
is within chord **1/1,000,000** of a generic area minimum and the relative
rotation angle is at most **1/10,000** radians from a body symmetry.
These two local restrictions are both essential to this explicit box.

Using the previously classified equality fits at the exact area minimum,
compactness proves an **unquantified positive all-source receiving
neighborhood** around all 30 generic minimum axes. Arbitrary source roll
and actual planar translation remain allowed. The all-source radius is
not identified with 1/1,000,000. Both handed named solids are covered by
reflection of the whole configuration, with same-handed moving copies.

Read [PROOF.md](PROOF.md) for the written finite-rotation and compactness
bridges. The six contacts are in [certificate.json](certificate.json);
the verifier is [check.py](check.py). Only standard-library Python 3.11+
is required, together with the pinned prior contribution directories.
From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-rupert-1/pentagonal_minimum_contact_cap/check.py --emit --negative-controls
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O round-two/six-rupert-1/pentagonal_minimum_contact_cap/check.py --emit --negative-controls
```

The underlying exact record must equal [expected.json](expected.json),
and all five damaged-contact controls must reject. [VALIDATION.json](VALIDATION.json)
records commands, versions, compact outputs' hashes and observed resource
use. All arithmetic decisions use rational outward bounds; numerical
sampling is not published as proof. The prerequisite area classification
is imported as a theorem and is not independently re-audited here.
