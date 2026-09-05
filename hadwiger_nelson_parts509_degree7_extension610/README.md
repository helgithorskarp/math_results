# Exact boundary for the degree-seven pool plus completion point 610

**Completed follow-up:** the residual is now refuted, and this support is
[closed through 508 vertices](../hadwiger_nelson_parts509_degree7_extension610_closure/README.md).
The minimum obstruction order is exactly 509. The material below preserves
the earlier reduction checkpoint and its then-unsolved residual.

**Result:** In a fixed 586-point extension of the Parts degree-seven completion
pool, every subgraph on at most 507 vertices is four-colourable. The minimum
order of a non-four-colourable subgraph is **508 or 509**. Any possible
508-vertex obstruction is reduced to exactly three deletions from 56 specified
original vertices and three additions from 76 specified completion points,
with vertices 15 and 23 also deleted and completion point 610 included.

The reduced selector formula has **1,038 variables and 3,774 clauses**. It
has not been solved. This is not a closure through 508 or a record improvement.

Let A7 be the original Parts graph together with all 76 completion points
having at least seven original unit neighbours. Add just

    q = (-(5+sqrt(33))/12, (5*sqrt(3)-sqrt(11))/12), label 610.

The strict graph H has 586 vertices and 3,089 edges. Its new point has exactly
six neighbours, labels 0,1,63,163,171,198, all original. Coordinates use the
integer basis of Q(sqrt(3),sqrt(5),sqrt(11)), with denominator 288; all pairs
are checked exactly, without floating-point screening.

The [proof](PROOF.md) combines 875 directly verified lifted colourings with
the imported degree-seven hitting bound. It also proves that the omitted
old killing set {15,23} cannot lift: **H minus {15,23} is five-chromatic**
(584 vertices, 3,071 edges; checked DRAT plus an explicit five-colouring).
This larger graph is evidence about the certificate mechanism, not a new
small-graph record.

## Replay the new evidence

From this directory in a checkout of the whole repository, using Python
3.11 or later:

```bash
extension_work=$(mktemp -d)
python3 verify.py --negative-cnf "$extension_work/kill_188.cnf" \
  --residual-cnf "$extension_work/residual.cnf" \
  --old-opb "$extension_work/imported_degree7.opb"
python3 controls.py
```

The first command verifies 451 forced-vertex colourings and 424 killing-set
colourings, the proper five-colouring, all exact geometry, the imported OPB
input hash, and the residual formula hash. It does **not** check either
negative proof by itself. Expected facts and controls are in `expected.json`
and `controls_expected.json`. The controls cover 4,096 counter assignments
and 2,028 relaxed assignments across 64 small abstract hitting families,
including 25 tight cases of the one-clause-loss argument.

With Kissat and drat-trim available, regenerate and independently check the
new, small negative proof:

```bash
python3 run_native.py kill_188 --work "$extension_work" \
  --solver "$(command -v kissat)" --checker "$(command -v drat-trim)"
python3 verify.py --proof "$extension_work/kill_188.drat" \
  --drat-trim "$(command -v drat-trim)"
```

The measured run used Kissat 4.0.4, took 1.69 seconds to generate the proof,
and 1.18 seconds to check it. The complete binary DRAT is 2,313,278 bytes;
its SHA-256 is recorded in `manifest.json`. Generated proof files and CNFs
are omitted from Git. The generator has one native worker, a 4 GiB address
space limit, and a 300-second solver limit. Every completed refutation is
checked to completion. UNKNOWN is never treated as UNSAT. Proof bytes may
differ under a different solver build; acceptance by drat-trim is decisive.

`verify.py` reconstructs the exact old degree-seven OPB, but the old 381 MB
cutting-planes proof was **not rechecked in this pass**. Its theorem is a
durable dependency. For a complete replay of that dependency, use the
[original proof instructions](../hadwiger_nelson_parts509_degree_pool_minimum/README.md)
and its `expected_D7.txt` hash record. The independent degree-seven review
also accepted the result, but its fresh optimization replay was solver-trusted;
it did not independently obtain the old cutting-planes proof.

## Reproduce the witness search and formula construction

`rank_lifts.py` replays the initial compatibility screen over the 119
degree-six completion points. It ranks failed old forced witnesses, failed
old killing witnesses, and then the point label. Point 610 is first, with
two misses of each kind. This exploratory ranking is not a closure of the
other 118 extensions. Only point 610 received repair queries in this pass.

```bash
python3 rank_lifts.py --out "$extension_work/ranking.json"
python3 build_residual.py --out "$extension_work/residual_again.cnf" \
  --metadata "$extension_work/residual_instance.json"
```

For the original four fixed repair queries, install `python-sat==1.8.dev24`
and run in a fresh directory:

```bash
repair_work=$(mktemp -d)
python3 repair.py --work "$repair_work"
python3 build_certificate.py --repairs "$repair_work/repairs.json" \
  --out "$repair_work/certificate.json"
```

The queries delete forced vertices 44 and 56 and killing sets 94 and 188.
CaDiCaL 1.9.5 gave three SAT colourings and one native UNSAT answer within
the 100,000-conflict limit per query. Only the later checked DRAT establishes
the negative result. The compact certificate has 3,746 bytes and is checked
directly regardless of how its witnesses were found.

One earlier, broader selector encoding (6,401 variables, 25,224 clauses)
returned **UNKNOWN after 300 seconds**. Its unfinished 311 MB trace is not a
proof and remains local. `build_master.py` preserves that exact input's
construction for audit. The smaller exact-three/exact-three formula follows
from the subsequent mathematical reduction. It was generated but not run;
the next bounded milestone is to decide it or preserve a principled new
checkpoint, rather than extend the old timeout. `observations.json` records
the measured queries, formula hashes, tool identities, and ranking result.

## Dependencies and scope

* [Degree-seven pool theorem and hitting bound](../hadwiger_nelson_parts509_degree_pool_minimum/README.md),
  Discovery Net `bafkreieatmp2sjuzzsbbklwx25p63mfjc7blqipzzk6ofnolxo5oxynada`.
* The [criticality](../hadwiger_nelson_parts509_criticality/README.md),
  [one-addition](../hadwiger_nelson_parts509_swap_closure/README.md),
  [two-addition](../hadwiger_nelson_parts509_pair_closure/README.md), and
  [three-addition](../hadwiger_nelson_parts509_triple_closure/README.md)
  closures, giving at least four new points in a possible <=508 obstruction.
* Original exact points from `hadwiger_nelson_parts509_completion_census_degree9`,
  completion coordinates from `hadwiger_nelson_parts509_swap_closure`, and
  integer field arithmetic from `hadwiger_nelson_parts509_pool_shape6_review1`.
  Input files are SHA-256 pinned in `manifest.json`.

The new support is distinct from the closed H574 deletion family and the
teammate's dense 293-gadget/origin-attachment construction. The latter was
inspected at commit `3ccf44f0e22a41892a820b764813645797bd0626` (Discovery Net
height 2791) and is not a dependency. A prepublication refresh through height
2816 found no new relevant HN contribution or objection. While publishing,
commit `dc57db82a86037be322374b20b31a65fb73df452` arrived, closing arbitrary
two-point additions to the teammate's two fixed dense506 hosts. Its statement
was inspected; those fixed-host extensions do not supply a closure of the
present Parts deletion/addition family. Parked overlap
census and timed-out QBF searches were not reopened. The theorem concerns
this single extension; it does not close the whole degree-six completion
pool or any unrestricted family of unit-distance graphs.
