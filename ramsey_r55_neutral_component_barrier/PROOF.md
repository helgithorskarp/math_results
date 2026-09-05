# A closed five-graph repair plateau

## Objects and permitted moves

Fix the labeled exceptional red triangle E={0,1,2}, with red degree 20 at
each exceptional vertex and red degree 21 at C={3,...,42}. Fix every E-C
incidence and every red signature-cell edge quota to the values in the
[previous escape graph](../ramsey_r55_neutral_switch_escape). The signature
vector is (0,8,8,6,10,4,4,0), in mask order 0,...,7. Every exceptional local
profile is (92,107), and the total number of red edges is 450.

A graph is admissible here if it also satisfies the previously defined
mixed-K5 and 884 pointwise root conditions. These are necessary retained
conditions, NOT all the Ramsey conditions. In particular, admissible graphs
may contain monochromatic K5s inside C.

A permitted edge in the repair graph is a four-edge central alternating
switch preserving all individual degrees and cell quotas, with both endpoints
admissible. In tuple notation (a,b,c,d), remove red ac,bd and add red ad,bc.
At least one opposite pair belongs to the same signature cell; the discovery
orientation chooses X_a=X_b.

The predecessor proves that this covers every central four-edge edit
preserving degrees and cell quotas: a degree-preserving four-edge support
must be an alternating C4. For its two opposite matchings, equality of the
multiset of unordered cell pairs is equivalent to X_a=X_b or X_c=X_d.
The checker independently enumerates all four-vertex sets and all pairs
among their three perfect matchings, testing quota equality literally.
There is no isomorphism quotient: all component vertices are labeled graphs.

## The objective and explicit path

For central v with exceptional signature X_v, the local degree identity is

```text
t_R(v)+t_B(v) = binom(21,2)-450+(21*21-|X_v|) = 201-|X_v|.
Phi(G) = sum_(v in C) max(0,t_R(v)-100,101-|X_v|-t_R(v)).
```

Thus Phi=0 exactly enforces the two chosen central hard-cap inequalities
t_R,t_B<=100. It does NOT enforce the absence of every monochromatic K5.
The interpretation of these caps retains the earlier extremal-catalog
boundary; their direct integer evaluation on the graphs does not.

PATH.json contains eleven permitted switches from the previous Phi-78 graph.
Literal verification gives

```text
78,78,78,78,78,77,77,75,74,74,74,73.
```

Every path step retains all individual degrees, all cell-edge quotas,
exceptional local counts, mixed-K5 conditions and pointwise bounds. The
endpoint GRAPH.json is vertex 0 of COMPONENT.json. The five supplied graphs
all have Phi=73. Exhaustive five-set checking establishes their admissibility
and counts their remaining monochromatic K5s.

## Component closure and the necessary uphill step

Independent complete matching-based censuses give the following adjacency
in the neutral repair graph:

| component vertex | all neutral neighbors | all degree/quota-preserving four-edge supports |
|---:|---|---:|
| 0 | 1,2,3 | 11,428 |
| 1 | 0,4 | 11,420 |
| 2 | 0,3,4 | 11,422 |
| 3 | 0,2 | 11,424 |
| 4 | 1,2 | 11,416 |

These 57,110 state/support incidences are checked individually. There is
no admissible strictly decreasing switch at ANY of the five states. Every
neutral neighbor is one of the listed states, and the six undirected neutral
edges connect them all. Consequently these five labeled graphs form the
entire neutral component of GRAPH.json, not just a finite search sample.

Proof of the barrier: suppose a permitted nonincreasing path begins at any
listed state. Its next step cannot decrease Phi, by the complete census,
and every neutral next step stays in the list. Induction keeps the entire
path within the same five states. Therefore no such path reaches Phi<73,
regardless of its length. More generally, any permitted path from the
component to a lower-Phi graph must leave it, and the first exit must increase
Phi. Integer scores force a visit to at least 74.

The positive score-change histogram has minimum 1 at every component state.
Thus the bound 74 is sharp for a FIRST EXIT. It is NOT a proof that score 74
suffices along a path to any lower-Phi graph; that barrier-height decision
has not been attempted.

Across the component, 10,848 state/support incidences would decrease Phi:
2,463 fail a pointwise bound, and the remaining 8,385 create a mixed K5.
There are 1,099 admissible directed incidences: 12 neutral and 1,087 uphill.
These are incidence counts, not distinct outside graphs.

## Scope and limitations

The component's red/blue K5 counts are (238,223), (237,229), (238,212),
(237,227), (237,216), respectively. Their central cap-failure counts are
27,26,29,29,28. None is a Ramsey graph. Component vertex 2 has the fewest
monochromatic K5s within this component, 450, but that is still far from zero.

The obstruction is local to this exact component, fixed E incidences, fixed
cell quotas and permitted four-edge switches. It is NOT an exclusion of
the whole quota fiber, signature case, degree profile, or hard branch. It
does NOT rule out other nonincreasing routes from the earlier Phi-78 graph:
discovery chose one successful descent branch, not all branches. It does
not classify arbitrary six-edge or larger simultaneous repairs, different
move families, or routes allowing temporary objective increases.

The older 66 profiles/271 anchored splits and 470 aggregate filters remain
unchanged. No verdict follows for either earlier UNKNOWN SAT model. External
hereditary-deletion cuts were not added or certified for these graphs.

## Evidence boundary

Discovery uses the previously validated incremental bitset switch routines.
Verification imports only the pinned literal predecessor checker, not search
code. Its matching-based support generation, set-based root conditions and
literal affected-triangle changes give a different implementation from the
discovery path. Each of the five graphs is also checked over all 962,598
five-subsets, with complete monochromatic lists compared against recursive
bitset clique enumeration. The path is replayed by literal triangle counts
and full pointed-K4 checks at every step.

The induction argument is unformalized. The finite certificate additionally
trusts the pinned sources, exact Python/runtime, SHA256 and ordinary hardware.
No solver, floating-point arithmetic or automorphism program is used. These
are internal certificate checks, not independent peer review. Source pins,
complete per-state census hashes and negative controls are supplied.
