# External-root lifting and the degree-20 triple frontier

An external vertex can impose a Ramsey degree bound into a rooted common
neighborhood **without itself belonging to that neighborhood**. The lemma
below gives general linear constraints on central cell-edge counts. Applied
to the hard profile `20^3 21^40`, these constraints and the preceding density
caps reduce a completely enumerated aggregate feasibility problem from
**731 labeled core/signature pairs to 470**.

Both exceptional-core types remain feasible in this relaxation. This does
**not** exclude the degree profile, produce a graph, or improve a Ramsey
bound. The inherited campaign totals remain 66 global profiles / 271 anchored
splits. The exact positive certificates establish the limitation as well as
the pruning: every retained case has integer aggregate edge counts.

## 1. External-root lifting lemma

Let G have no red or blue K5. Let A be a red clique of size a and B a disjoint
blue clique of size b, with `0<=a,b<=3` and `a+b>0`. Define

```text
S = {v outside A union B : v is red to every A vertex
                             and blue to every B vertex}.
```

For any `u outside A union B`:

```text
u red to A  => |N_R(u) intersect S| <= U(4-a,5-b)-1,        (1)
u blue to B => |N_B(u) intersect S| <= U(5-a,4-b)-1.        (2)
```

Here U is any valid Ramsey upper-bound table. Crucially, (1) requires no
blue incidence from u to B, and (2) requires no red incidence from u to A.
Thus u need not lie in S. Neighborhoods exclude u itself if u is in S.

For (1), `A union {u}` is a red clique. A red `(4-a)`-clique in
`N_R(u) intersect S` would extend it to a red K5; a blue `(5-b)`-clique
would extend B to a blue K5. The set is therefore `(4-a,5-b)`-Ramsey and
has at most `U(4-a,5-b)-1` vertices. Color reversal proves (2).

The implementation uses `U(1,b)=U(a,1)=1` and the ordinary Ramsey recurrence,
subtracting one when both predecessor upper bounds are even. For that
refinement, a counterexample on `r+s-1` vertices would have every red degree
equal to the odd number `r-1`; its order is odd, contradicting handshaking.
This is an elementary upper table, not an imported catalog of higher Ramsey
numbers. In particular `U(3,4)=U(4,3)=9`.

The special case `a=b=1` gives the previously used common-root cap eight,
now in a uniform form for all exceptional-root cliques and both colors.
[controls.py](controls.py) constructs an eleven-vertex Ramsey graph with an
external u attaining eight red neighbors in S. It also checks 43,480 lifted
inequalities across every five-vertex Ramsey graph and rejects the two
monochromatic five-vertex counterexamples when the Ramsey hypothesis is
deliberately dropped. This is a small-instance audit, not a substitute for
the hand proof.

## 2. Explicit hard-profile hypotheses and core reduction

Assume G is Ramsey `(5,5;43)` with three vertices E of degree 20 and forty
vertices C of degree 21. Then `m=450=231+219`, so this is M=219. We use the
following explicit local caps, implied by the campaign's hard branch:

```text
degree of v     t_R(v) upper bound    t_B(v) upper bound
20                       93                   107
21                      100                   100.
```

Here t_R(v) counts red edges inside its red neighborhood and t_B(v) counts
blue edges inside its blue neighborhood. The hard-branch interpretation
imports the previously established local extrema `U45(20)=100`,
`U45(21)=107`, `U45(22)=114`, with every deficiency at least seven; see
[local-extremal deficiency](../ramsey_r55_local_extremal_deficiency).
The new finite theorem can instead be read simply under the displayed
local-cap hypotheses, without importing any wider profile classification.

The exact local identity is

```text
t_R(v)+t_B(v) = choose(42-d(v),2)-m + sum_(w red to v) d(w).
```

Indeed, splitting edges into the two neighborhoods and the cross edges
cancels the latter and leaves exactly the red and blue local edge counts.
For i in E, this identity becomes `201-deg_F(i)`, where `F=G[E]`.
Since 93+107=200, every F degree is at least one. On three vertices the
only possibilities are a path and a triangle. Their lexicographic edge-bit
representatives are mask 3 (edges 01,02) and mask 7 (all three edges).
The path has three labeled versions, masks 3,5,6; the triangle has one.

For a central vertex with signature `X=N_R(v) intersect E`, the identity
becomes `201-|X|`. Its upper bound is 200, so X is nonempty. Put `y_X=|C_X|`.
Every actual graph has

```text
sum_X y_X=40,
sum_(X containing i) y_X = 20-deg_F(i),
y_X integral and nonnegative.
```

For every disjoint red clique A and blue clique B in F, let F_AB be the
exceptional vertices outside A union B that are red to A and blue to B.
The inherited root-union capacities require

```text
|F_AB| + sum_(X containing A, X disjoint B) y_X
 <= U(5-|A|,5-|B|)-1.                                  (3)
```

These conditions leave 164 cell vectors for each labeled path and 239 for
the triangle: **731 labeled core/cell-vector pairs**. All are enumerated,
not just the earlier published first primal per core. For coverage, one
implementation enumerates the three pair cells and the triple cell and
solves for the singleton cells. A separate implementation enumerates two
singletons and the triple cell, then solves the three pair margins by
halving their pairwise sums/differences. Their complete sets agree.

No automorphism is assumed for G. Permuting the three named exceptional
vertices merely partitions the labeled input pairs into 141 orbits, each
with a canonical certificate. Every inequality and its right-hand side
is explicitly transported under all six permutations.

## 3. The exact aggregate integer-edge relaxation

For each unordered pair of nonempty signature cells X,Y, let z_XY count
red central edges between them; diagonals count internal edges once.
Variables of capacity zero are omitted. The boxes are

```text
0<=z_XY<=y_X*y_Y       (X!=Y),
0<=z_XX<=choose(y_X,2),
z_XY integral.
```

For each cell X, its aggregate central red degree is
`(21-|X|)*y_X`, so internal edges contribute twice. For each i in E,
the exact local red-edge count is the sum of z_XY with both signatures
containing i, plus the fixed core/core and core/central incidences. It
must lie in `[94-deg_F(i),93]`, by the local identity and blue cap 107.

Let S be a rooted set represented by (3), including F_AB. Its unknown
red degrees are linear in z; fixed exceptional incidences are added
explicitly. Three nested stages are certified:

1. **Internal-root degree stage.** For central cells inside S, enforce the
   standard maximum red and blue degrees of a `(5-a,5-b)` graph. Enforce
   those bounds at its fixed exceptional vertices too. Include all cell
   degree equations, exceptional local-edge intervals, and boxes above.
2. **Density stage.** Additionally, for each opposite-colored singleton
   root pair with `|S|=15` or 16, impose the entire red-edge interval
   `50--55` or `58--62` respectively, including all fixed edges. These are
   the [preceding catalog-free density bounds](../ramsey_r55_rooted15_density_bound).
3. **Lifted stage.** Additionally, impose (1) summed over each central cell
   red to A, even if it is outside S; impose (2) over each cell blue to B,
   again without requiring membership in S. Existing internal bounds remain.

For example, writing T=C_X and using red-edge degree sums,

```text
D_R(T,S)=sum_(u in T) |N_R(u) intersect S|
        <= (U(4-a,5-b)-1)*y_X      if X contains A.
```

The left side counts an edge twice when both endpoints lie in T and S.
Blue bounds subtract this red form from the number of possible incidences,
excluding self-pairs. This convention is important for diagonal variables.

The complete result is:

| Core family | Input pairs | After internal degree stage | After density stage | After lifting |
|---|---:|---:|---:|---:|
| Three labeled paths | 492 | 474 | 468 | 387 |
| Triangle | 239 | 212 | 152 | 83 |
| Total | 731 | 686 | 620 | 470 |

Thus density alone removes 66 further labeled pairs, and external-root
lifting removes another 150. The 470 final pairs occupy 93 relabeling
orbits. These are **core/signature pairs with aggregate edge-count
witnesses**, not 470 graphs, global degree profiles, or anchored splits.

The aggregate witnesses do not supply individual central edges, individual
central degrees, or central neighborhood triangle counts. They need not
admit a simple-graph realization and do not certify absence of a central
monochromatic K5. In particular, feasibility of both core families is a
proved stopping boundary for this relaxation, not evidence for existence
of a Ramsey `(5,5;43)` graph.

## 4. Certificates, independent reconstruction, and reproduction

[CERTIFICATE.json](CERTIFICATE.json) contains one record per orbit. Each
records its first failed stage (or null), an integer primal at the last
feasible stage, and nonnegative integer Farkas multipliers at the first
failed stage. A stage matrix is canonically written `A z<=b`, merging equal
coefficient rows by their tightest right-hand side and sorting rows
lexicographically. The multipliers satisfy exactly `lambda*A=0` and
`lambda*b<0`. Thus rejected cases are infeasible even over the reals, while
every retained case has an integer primal. No solver status is trusted.

[model.py](model.py) constructs coefficients directly from signature masks.
[literal_model.py](literal_model.py) independently expands all 43 vertices,
their fixed incidences, and each literal unordered vertex pair. It checks
that coefficients are uniform inside every unknown cell-pair edge class
before aggregation. All **423 stage matrices** agree exactly. The checker
then verifies **2,538 complete matrix transports** under exceptional
relabeling, as well as full input orbit coverage. This is an independent
encoding check within the same research artifact, not a peer review.

Using Python 3.11.2 and its standard library, from this directory:

```bash
python3 verify.py --report /tmp/external-root.json
cmp report.json /tmp/external-root.json
python3 -O verify.py --report /tmp/external-root-O.json
cmp report.json /tmp/external-root-O.json
sha256sum -c SHA256SUMS
```

The default command pins and replays the preceding density proof's complete
production computation. Its separate literal proof remains available there.
The final normal and optimized runs took 72.332 and 72.637 seconds, respectively,
including this parent replay and while running concurrently; peak child
resident memory was at most 22,940 KiB. Their reports match byte for byte.
The option `--skip-density-replay` checks the new certificates **conditional
on that imported density lemma**, and is useful for quick development checks.
It does not change the deterministic report's mathematical scope.

Optional certificate discovery uses the versions in
[requirements-discovery.txt](requirements-discovery.txt):

```bash
python3 generate.py --output /tmp/alternative-certificates.json
python3 verify.py --certificate /tmp/alternative-certificates.json
```

SciPy/HiGHS proposes integer primals and numerical LP duals. Duals are
rationally reconstructed and converted to primitive integer multipliers;
all proposals must pass exact checks. Each integer-primal search has a
five-second bound and aborts rather than classifying a missing witness.
Alternative valid witnesses may depend on solver/platform behavior. No
numerical package is used by the verifier.

Normal and optimized verification must agree byte for byte. Forty orbit
certificates contain exact witnesses that pass one stage and fail the next,
so the strengthening is nonvacuous. Three altered certificates are rejected.
The literal graph controls test the lifting lemma in both colors, including
an external vertex attaining the cap. Python exceptions remain active under -O.

## Provenance, novelty, and next boundary

This follows the general common-root method, the preceding density proof,
and the signature-union relaxation. Discovery Net's h2665 transfer-barrier
witnesses show that count-only exceptional-root reasoning does not activate
order-15/16 cuts on five remaining double-degree-19 profiles. That result
motivated coupling central edges here, on a **different** degree-20 profile.
Nothing in this artifact contradicts those count-only witnesses or reopens
the already excluded `19^2 20^3 21^38` branch.

The lifting lemma is a direct rooted Ramsey argument; no literature priority
or new Ramsey-number claim is made. Its value here is a systematically
generated, exact edge-aware constraint family and a fully certified finite
feasibility boundary. Trust remains in the unformalized reduction, explicit
local-cap hypotheses (or the inherited extremal inputs interpreting the hard
branch), the imported density lemma, source correctness, Python exact
semantics, SHA256, and hardware. The new result is internally checked,
not formally proved or independently peer reviewed.

For primary literature context, Angeltveit and McKay's
[R(5,5)<=46](https://arxiv.org/abs/2409.15709), especially Section 2, combines
linear programming with overlap-and-gluing computations on actual pointed
neighborhood graphs. The aggregate witnesses here do not perform that
individual-edge gluing step and should not be confused with such graphs.

This milestone is complete. A subsequent pass may test these lifted edge
constraints against the existing transfer-barrier witnesses, or add genuinely
new individual-edge/central-triangle information to a surviving case. Merely
rerunning the present relaxation cannot exclude this profile.
