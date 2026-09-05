# Exceptional-profile-preserving switches and a quota-release escape

## 1. Exact switch criterion

Let E be any fixed set of k vertices of a red/blue complete graph. For
v outside E, let X_v be its k-bit red adjacency signature to E. Take
distinct a,b,c,d outside E with ac,bd red and ad,bc blue. Switch these
four edges, making ac,bd blue and ad,bc red. All vertex degrees and all
incidences with E stay fixed.

For e in E write x_v=1 if ev is red and 0 otherwise. The local red
profile t_R(e) is the number of red edges inside N_R(e); t_B(e) is the
number of blue edges inside N_B(e). Since both neighborhoods stay fixed,
the only changes in their internal edge counts are the four switched
edges. Consequently

```text
Delta t_R(e) = x_a*x_d + x_b*x_c - x_a*x_c - x_b*x_d
             = (x_a-x_b)*(x_d-x_c),
Delta t_B(e) = -Delta t_R(e).
```

The second identity follows by replacing each x by 1-x and reversing
the edge-color changes. Thus **every exceptional local profile is
preserved if and only if**

```text
((X_a XOR X_b) AND (X_c XOR X_d)) == 0.
```

This is a coordinatewise condition: no exceptional vertex distinguishes
both opposite pairs. It imposes no automorphism, cell-edge quota, or
Ramsey assumption. The seven-vertex controls exhaust all 4096 choices
of four 3-bit signatures and all 32 assignments to the remaining five
edges (the three E edges and ab,cd). Direct local counts in both colors
agree in all 131072 completions. Exactly 1728 signature assignments,
or 55296 completions, preserve all exceptional profiles.

## 2. Why this strictly broadens the former quota family

Let z_{XY} count red central edges between signature cells X,Y, including
internal-cell edges when X=Y. Associate an indeterminate Z_X to each
signature cell. The change in the polynomial encoding all quotas is

```text
Z_{X_a}*Z_{X_d} + Z_{X_b}*Z_{X_c}
  - Z_{X_a}*Z_{X_c} - Z_{X_b}*Z_{X_d}
 = (Z_{X_a}-Z_{X_b})*(Z_{X_d}-Z_{X_c}).
```

The integer polynomial ring is an integral domain. Therefore all cell
quotas stay fixed exactly when X_a=X_b or X_c=X_d. This implies the
exceptional-profile condition but is stronger when k>=2. For k=3,
960 of the 4096 ordered assignments preserve quotas, leaving 768
additional assignments preserving the profiles only. The controls
also check the quota characterization by direct edge-type multisets.

Every nonempty degree-preserving edit of exactly four distinct edges
in a simple graph is an alternating four-cycle. Indeed each affected
vertex has equally many additions and deletions, so the changed edges
decompose into alternating closed trails. A nonempty such trail has
at least four edges, and with only four edges it is one four-cycle.
Thus the criterion describes **all central four-edge edits preserving
degrees and exceptional profiles**, not merely one orientation family.

The production generator considers each opposite pair a<b, chooses c
red only to a and d red only to b, tests the bitwise condition, and
deduplicates the four-edge supports. The verifier instead considers
each central four-set and every pair of its three perfect matchings.
It requires opposite monochromatic matching colors and checks the
literal changes of all six exceptional local edge counts. These
algorithms produce identical support sets at both certified endpoints.

## 3. Retained feasibility gates and the four-row requirement

Here E={0,1,2}, a red triangle, and C={3,...,42}. Every vertex of E
has degree 20 and every vertex of C degree 21. Signatures have fixed
multiplicities (0,8,8,6,10,4,4,0) in mask order 0,...,7. Every graph
on the recorded path retains the exceptional profiles (92,107).

We also retain absence of every monochromatic K5 meeting E, and all
884 named pointwise root inequalities from the original realization.
Their root sets and bounds depend only on E and its incidences, which
are unchanged. The pointwise inequalities examine individual adjacency
rows; only the four support rows change. It is therefore sufficient
to check those four rows, and all other rows inherit their validity.

Checking only a,b is not generally sufficient for the broader family.
On both certified endpoints, move (3,27,5,24) has signatures (1,4,1,3)
and satisfies the profile criterion. The first two rows pass, but at
vertex 24 the red pointwise inequality for roots A={0}, B={2} has
actual value 9 and upper bound 8. The exhaustive controls compare the
four-row gate to the literal all-884 gate for every support.

This is not a defect in the former search: it oriented its quota moves
with X_a=X_b, making the c,d rows' root-set counts unchanged. The new
canonical orientation need not have that equality, even when the
other pair has equal signatures. At the seed, naive reuse of the
first-pair check would miss 2103 lifting failures, 1012 on genuinely
quota-changing supports; at the endpoint these counts are 1936 and 976.

A new mixed K5 must contain a newly colored central edge and an E root.
The fast gate tests these cases; the independent census enumerates
literal monochromatic triples in each changed edge's common neighborhood.
Every accepted path graph additionally undergoes a full five-set audit.

## 4. The actual-K5 escape and bounded descent

The seed is the prior 384-K5 graph with SHA-256
`c343c8ace3fb1c9dff6e90175ecdb1035989e0caf40a976a44d464a1381dc03c`.
Its 11419 quota-preserving supports contain 185 admissible switches,
all strictly increasing the actual total K5 count. The broader family
has 17256 supports, including 5837 quota-changing ones. After lifting
and mixed-K5 gates, exactly three additional switches are admissible.
Their total K5 changes are -1,+1,+4. The unique decreasing switch is

```text
(a,b,c,d) = (7,37,39,25),
(X_a,X_b,X_c,X_d) = (1,5,6,4),
(X_a XOR X_b) = 4,  (X_c XOR X_d) = 2.
```

It changes the cell quotas by
`Delta z_{1,6}=-1, Delta z_{4,5}=-1, Delta z_{1,4}=+1, Delta z_{5,6}=+1`
and decreases (red K5,blue K5) from (198,186) to (197,186).
This certifies that the former strict local barrier depended on the
extra cell-quota restriction. It does not contradict the former census.

Strict actual-K5 descent then produces totals

```text
384,383,379,374,373,370,368,367,365,364,359,358.
```

Only the first of these eleven moves changes quotas. The tie breaker
Phi measures central local-cap violations and is not the objective:
it takes values 84,85,89,88,87,88,85,88,91,87,87,86. The exact K5 update
is the previously proved outside-triangle formula from the parent
artifact. It applies to any alternating four-cycle, so requires no
new quota assumption. Each accepted move is checked by full red/blue
K5 recounts, and the separate path verifier compares the complete
literal and recursive five-set lists on every path graph.

The endpoint has 172 red and 186 blue K5s, all in C. Its 17276 broader
supports divide into 3032 lifting failures, 14052 further mixed-K5
failures, and 192 admissible switches. None decreases total K5s, but
three preserve the total. The complete neutral support list and both
endpoint census hashes are in report.json. The endpoint is therefore
a non-strict local minimum for this one-switch family, **not a certified
neutral-component barrier**. No neutral continuation is explored here.

## 5. What has and has not been established

The exact signature criterion, its strict relation to quota preservation,
the four-row gate, the quota-release escape, and the finite endpoint
censuses are the results. This is solver-free exact integer computation
with two enumeration methods, full graph audits, exhaustive small
controls, mutation controls, and normal/optimized Python replay.

The graph still has 358 forbidden five-sets, 34 central vertices failing
the chosen hard local caps, and opposite-color neighborhood gaps at all
three exceptional vertices. It is not a Ramsey graph and does not settle
the degree profile, the retained signature case, the entire switch
fiber, larger edits, or R(5,5). The common signature counts do not mean
that cell quotas remain fixed. No historical-priority claim is made for
the elementary switch identities. The sources, their unformalized
proof alignment, Python semantics, hardware, and hash integrity remain
trust boundaries; this is not an external peer review or formal proof.
