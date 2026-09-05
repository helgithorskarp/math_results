# Exact K5 switch updates and a strict local obstruction

## Eight triangle counts, all in the old graph

Let G be any red/blue coloring of a complete graph, and let a,b,c,d be distinct
vertices with ac,bd red and ad,bc blue. Switch these four colors. Write
S=V(G)\{a,b,c,d}, A=N_R(a) intersect S, and similarly B,C,D. Complements below
are taken inside S. Write t_R(U),t_B(U) for monochromatic triangle counts in
the old induced graph G[U]. If r_5,b_5 count red and blue K5s, then

```text
Delta r_5 = t_R(A intersect D)+t_R(B intersect C)
          - t_R(A intersect C)-t_R(B intersect D),
Delta b_5 = t_B(Abar intersect Cbar)+t_B(Bbar intersect Dbar)
          - t_B(Abar intersect Dbar)-t_B(Bbar intersect Cbar).
```

Proof: every triple of the four switched vertices contains both colors,
before and after the switch. A monochromatic clique therefore contains at
most two of these vertices. A changed monochromatic K5 must contain exactly
two, joined by a changed edge, and its remaining three vertices must lie in
S. For each removed red edge, the destroyed red K5s correspond bijectively to
red triangles in its old common neighborhood in S. For each added red edge,
the created red K5s correspond to the same kind of triangles for its endpoints.
The outside edges and endpoint-to-S incidences do not change. No K5 is counted
twice, because it cannot contain three or four switched vertices. This proves
the red formula; swapping colors proves the blue formula.

Equivalently, for each red triangle T in S, let alpha_v be 1 if v is red to
all of T. Its contribution is (alpha_a-alpha_b)*(alpha_d-alpha_c). For a blue
triangle, the analogous beta variables give (beta_a-beta_b)*(beta_c-beta_d).
This signed product explains the cancellation and allows a local exact
update of the actual target obstruction count, rather than its cap surrogate.
No novelty is claimed for the general local clique-update principle.

The same proof replaces triangles by monochromatic (r-2)-cliques for counts
of K_r, r>=3. We use and implement only r=5 here. In particular, a changed K5
requires at least seven vertices: four for the switch and three outside.
Controls at orders 4,5,6 alone would be vacuous tests of a nonzero K5 update.

## The target-specific graph path

The input is vertex 2 of the
[previous neutral component](../ramsey_r55_neutral_component_barrier), with
238 red and 212 blue K5s. The exceptional red triangle E={0,1,2} has degree
20; all central vertices C={3,...,42} have degree 21. Signatures are fixed
as (0,8,8,6,10,4,4,0), and every exceptional local profile is (92,107).

Allowed moves remain central alternating four-edge switches that preserve
every individual degree, exceptional incidence and signature-cell edge quota,
and retain all mixed-K5 and 884 pointwise root conditions. The complete
four-edge support characterization is inherited from the cell-preserving
repair lemma. No automorphism condition or solver model is imposed.

After the earlier cap-score/K5 mismatch, this run ranks admissible strictly
K5-decreasing moves by total K5 count first, Phi second, then the labeled
move tuple. Phi is recorded but is not an admissibility ceiling. The eleven
verified switches have total K5 counts

```text
450,436,427,416,411,406,401,399,396,394,392,384.
```

Their Phi values are

```text
73,81,84,83,80,82,86,88,86,84,84,84.
```

Every retained invariant is checked on every graph, not merely on aggregate
edge totals. The endpoint has 198 red and 186 blue K5s, all inside C. It also
has 36 central vertices failing the chosen hard local caps and explicit
opposite-color K5s inside exceptional neighborhoods. It is NOT a Ramsey graph.

## A strict one-switch barrier for actual K5 count

All 11,419 central degree/quota-preserving four-edge supports at the endpoint
are independently generated from four-vertex sets and pairs of perfect
matchings. In the pointwise-first classification, 1,515 fail a root inequality,
9,719 remaining supports fail a mixed-K5 condition, and 185 are admissible.
For each admissible graph, the checker performs full monochromatic clique
enumeration, without using the eight-triangle update formula.

Every one of those 185 neighbors has MORE than 384 K5s. There are no decreasing
or neutral admissible neighbors. Three have increase one; the largest increase
is 37. Thus the endpoint is a strict local minimum for actual K5 count under
this move family. Its nonincreasing reachable component is the singleton:
no nontrivial first step is possible. Any permitted path to a lower K5 count
must first visit at least 385. Such first exits exist, but we do NOT prove
that a path capped at 385 can reach a lower count afterward.

This is not a fixed-quota-fiber, signature-case, degree-profile or global
infeasibility theorem. Larger simultaneous edits, other signatures or quotas,
temporary obstruction increases and other descending branches remain open.
No further plateau, uphill or radius phase was started after this barrier.

## Exact checking and limitations

The eight-triangle update is compared to literal full five-set counts for
all 131,072 seven-vertex completions of the alternating switch. There are
1,568 nonzero color-delta vectors. The other two internal support-edge colors
are both varied; the general argument explains why they cannot affect the
delta. Exhaustive smaller controls comprise 4 order-four, 64 order-five and
2,048 order-six completions, all correctly giving zero update.

The path checker imports no search code. Every one of its twelve graphs is
checked over all 962,598 five-subsets, with complete red/blue K5 lists matched
to recursive bitset enumeration. Degrees, quotas, E counts, mixed constraints
and all pointwise conditions are checked at every step.

On the actual 43-vertex endpoint, controls compare the complete support sets,
every feasibility classification, and every admissible color-count update
between the incremental search and literal/full-enumeration checker. The
complete 11,419-entry classification digest agrees, not merely the totals.
Normal and optimized verification and controls are byte-identical. A one-step
bounded discovery control returns STEP_LIMIT, not a local-minimum claim.

The mathematical coverage and update arguments are unformalized; the exact
source/runtime, SHA256-pinned dependencies and ordinary hardware remain
trusted. No solver, floating point or graph catalog is needed for the direct
K5 counts and local-minimum claims. The interpretation of Phi as the selected
hard-cap target still inherits the earlier extremal-catalog boundary.
This is internal verification, not independent peer review. Global 66
profiles/271 anchored splits, 470 aggregate filters and old UNKNOWN SAT models
remain unchanged. The full Ramsey conditions have not been satisfied.
