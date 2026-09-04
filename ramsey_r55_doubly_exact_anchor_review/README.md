# Independent review of the stabilized singleton SAT reduction

This directory records reviewer-3's independent audit of Discovery Net
contribution
`bafkreicdv4z45ppuutaavlufppeu3ftyg5l7zwbk3e4wkhexhi2pyppvnm`, checked
against source commit `d688f43d5238cc90cc2d6ff3c0259411a94abf2b`.

## Verdict

The structural singleton reduction, the seven exhaustive typed cases, and the
losslessness of the two-stage symmetry break are verified.  One numerical
statement in the contribution body is false: a stabilized branch has
`3,782,854` clauses, not `3,782,794`.  The latter is the unstabilized typed
count.  The submitted source, README, generated formulas, and stabilized
manifest all consistently give the corrected count.

This is a qualified verification of an intermediate pruning result, not a
verification of `R(5,5) >= 44`.  No branch has a submitted SAT model or UNSAT
certificate.

## Independent checks

[`audit_stabilized_branches.py`](audit_stabilized_branches.py) does not import
the submitted Python modules.  It independently:

1. enumerates the side degree-count vectors and recovers the seven totals
   `1,5,17,40,69,95,122`, hence all 349 split profiles;
2. redoes the red/blue singleton edge accounting (`220 != 219` versus
   `220 = 220`) and the triangle-incidence divisibility giving
   `x=0,3,...,18`;
3. parses and pins both seven-row manifests;
4. reconstructs the edge-variable numbering and all 39 monotonic plus 21
   unit symmetry clauses; and
5. optionally byte-compares regenerated `x=0` formula bodies, checks that the
   unstabilized formula is an exact 3,782,794-clause prefix of the stabilized
   one, and checks the 60-clause suffix and both full-file hashes.

The mathematical losslessness argument is also direct.  The first relabeling
uses the full symmetric action on `C` to make `N_R(z) intersect C` a prefix.
It fixes `c0` inside that nonempty prefix.  The second relabeling uses the
remaining full symmetric action on `O minus {z}` and therefore preserves the
first choice.  The core degree bounds give prefix lengths 3 through 13 and 6
through 16.  Those bounds follow respectively from `R(4,4)=18` on
nonneighbors and `R(3,5)=14` on neighbors of a vertex in a `(4,5;21)` core.

## Reproduction

Quick arithmetic and manifest audit, from the repository root:

```bash
python3 ramsey_r55_doubly_exact_anchor_review/audit_stabilized_branches.py \
  ramsey_r55_doubly_exact_anchor_propagation \
  | cmp - ramsey_r55_doubly_exact_anchor_review/EXPECTED_OUTPUT.txt
```

For the full stream comparison, generate the two temporary formulas outside
the repository and then audit them:

```bash
mkdir -p /scratch/research-team-v2/tmp/reviewer-3/r55-stabilized-audit
python3 ramsey_r55_doubly_exact_anchor_propagation/singleton_sat.py generate \
  /scratch/research-team-v2/tmp/reviewer-3/r55-stabilized-audit/x0-base.cnf \
  --local-profile --red-exceptional 0
python3 ramsey_r55_doubly_exact_anchor_propagation/singleton_sat.py generate \
  /scratch/research-team-v2/tmp/reviewer-3/r55-stabilized-audit/x0-stabilized.cnf \
  --local-profile --red-exceptional 0 --stabilizer-break
python3 ramsey_r55_doubly_exact_anchor_review/audit_stabilized_branches.py \
  ramsey_r55_doubly_exact_anchor_propagation \
  /scratch/research-team-v2/tmp/reviewer-3/r55-stabilized-audit/x0-base.cnf \
  /scratch/research-team-v2/tmp/reviewer-3/r55-stabilized-audit/x0-stabilized.cnf \
  | cmp - ramsey_r55_doubly_exact_anchor_review/EXPECTED_WITH_CNFS.txt
```

Reviewer-3 additionally reproduced the submitted main checker, SAT
self-tests, official-catalog provenance audit, Ramsey-42 bridge, and exact
radius-five target enumeration.  The catalog audit fetched the pinned
official McKay inputs and recovered the stated `(3,5)` catalog counts and
`(4,5)` extremal maxima.  The radius-five audit enumerated 230,503
degree-compatible flip sets and found no Ramsey survivor.

## Trust boundaries

The catalog-distance statement is only relative to the 328 published known
Ramsey-42 graphs and is not a completeness theorem for that catalog.  Catalog
census completeness, the imported local-deficiency theorem, the prior
21-by-21 cross normal form, and the radius-four classification remain imported
trust boundaries.  No SAT solver result is used here.
