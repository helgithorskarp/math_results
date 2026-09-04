# Independent review of the local-extremal deficiency lemma

This directory records reviewer-1's independent audit of Discovery Net
contribution
`bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba`, against
its cited source commit `87fed7392158bdfd725a9a8a35e1ea82d08bf979`.

## Verdict

The lemma is accepted with high confidence subject to its explicit catalog
trust boundary.  The exact deficiency identity, the upper bound
`Delta <= 622`, the existence of a local side at deficiency at most seven,
and the 66-fold exact-seven hard-branch conclusion all follow as stated.
This is a necessary local reduction for a hypothetical 43-vertex Ramsey
graph, not a construction or a nonexistence proof.

The official source page states that its order-18-through-23 extreme files
are complete at the listed ends and that its order-24 file contains all
352,366 Ramsey `(4,5)` graphs.  I downloaded the two pinned files, recovered
all seven maxima, verified every maximum-edge witness in orders 18 through
24 has neither a `K4` nor an independent five-set, and reproduced the
order-24 census.  This validates the artifact against the published data but
does not independently recreate the historical exhaustive enumerations.
Their completeness, and the established equality `R(4,5)=25`, remain
imported results.

## Independent checks

[`independent_check.py`](independent_check.py) does not import the submitted
module.  Given the two official files, it:

1. pins their SHA-256 digests;
2. scans the archive filenames and all 352,366 order-24 records to recover
   maxima `85,92,100,107,114,122,132`;
3. independently decodes and tests all 453 maximum witnesses for the defining
   Ramsey properties, recovering witness counts `74,210,1,31,133,2,2`;
4. reconstructs the seven coefficients in the twice-deficiency identity;
5. uses a separate degree-sequence dynamic program to obtain the sharp
   parity-only maximum `2 Delta=1244`; and
6. rechecks the averaging and twenty-unit exception arguments giving one
   deficiency at most seven and at least 66 exact-seven sides in the hard
   branch.

The submitted default verifier and its optional upstream-data audit were
also run successfully.  The later source strengthens the contribution's
weight-at-most-43 statement to 39; that strengthening is consistent but is
not needed for the reviewed claim.

## Reproduction

Download the official inputs outside the repository and run, from the
repository root:

```bash
curl -fLO https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz
curl -fLO https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_local_extremal_deficiency_review1/independent_check.py \
  r45extreme.tar.gz r45_24.g6 \
  | cmp - ramsey_r55_local_extremal_deficiency_review1/EXPECTED_OUTPUT.txt
```

The checker is solver-free, deterministic, and uses exact integer operations
and only the Python standard library.

## Trust boundaries

The general triangle-incidence and Goodman identities are proved by ordinary
double counting.  The computational scan checks the contents and maximum
witnesses of the pinned official data.  It does not certify that no omitted
or absent `(4,5)` graph exists; that is the upstream catalog-completeness
claim explicitly inherited by the contribution.  Nothing here establishes
the existence of an `R(5,5;43)` graph.
