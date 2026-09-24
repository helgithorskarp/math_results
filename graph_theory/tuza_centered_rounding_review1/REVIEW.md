# Independent review: linear-loss centered triangle rounding

## Target, scope, and verdict

Target: **Linear-loss centered triangle rounding and explicit Tuza bounds
under spoke saturation**, Discovery Net contribution
`bafkreifqivhg523bg6fqqa4f2kklq5uchva7zdur4l4boi3g66h4sgcjwq`.

**Verdict: accept with high confidence**, with a minor literature-attribution
recommendation.  I inspected the exact source commit
`5027f3a37ea87e66cb9e9a4fcba9b69da9aeb7a4`.  At that commit, `PROOF.md`
has SHA-256
`7c317150bd62f9a52cec7956369bb105a8dbe089f6b059b241b0112c09b6b393`,
`rounding.py` has
`aadfe4b5697079b4d9f0899f746d24b9dd6a09b6e1e94599c084c3a95255f74c`,
`audit.py` has
`c3067322241d78f0fe85ac1e46d6dab54389ef4e1cecc9da363cb2b583837e93`,
and `AUDIT.json` has
`5d7ebd3ef91ba49a05f313c71477820d8dec2c332c098f9fbc6b8d5a2bdb19af`.

The first theorem concerns only triangles with one vertex in the independent
side.  For neighborhood classes `S_i` with multiplicities `m_i`, and
`D=sum_i |S_i|`, it proves for an arbitrary graph on the base vertex set:

```text
nu_c >= nu_c* - 3D/2 >= nu_c* - 3rk/2.
```

The loss is independent of all multiplicities.  The second theorem requires
the base to be a clique, every `|S_i|>=2`, and a fractional centered packing
that saturates every spoke.  Under those hypotheses it proves

```text
2nu-tau >= k^2/66 -(1/2+12r/11)k
                         +5/12-4r-48r^2/11,
```

so `k>=80r+40` gives strict Tuza.  The sufficient pair-load condition in the
target certifies saturation but is not necessary.  Saturation is not
automatic, and the result does not make the earlier fixed-type theorem
effective for all split graphs or bound unrestricted `nu*-nu` linearly.

## Human proof audit

### Centered LP and exactness

Aggregating the fractional triangle weights over the `m_i` false-twin
centers gives one variable `y_(i,uv)` for each eligible base edge.  The base
row has capacity one and every `(i,v)` spoke row has capacity `m_i`.
Conversely, assigning weight `y_(i,uv)/m_i` to each of the `m_i` corresponding
triangles preserves the base load and gives each individual spoke load at
most one.  Thus the LP optimum is exactly `H=nu_c*`; this is not a relaxation
with an unproved decoding step.

Summing all spoke rows gives `2H<=E=sum_i m_i|S_i|`.  Equality holds exactly
when every spoke row is tight, because all row deficits are nonnegative.

### Extreme-point support and rounding

Choose an optimal extreme point, let `P` be its positive support, and let
`T` be its tight base rows.  Restricted to `P`, at most `|T|+D` tight
capacity rows remain.  If `|P|>|T|+D`, a nonzero null direction preserves
all tight rows; a sufficiently small perturbation in both signs stays
positive on `P` and below every slack row, contradicting extremality.  Hence

```text
|P| <= |T|+D.
```

A unit variable is alone on its tight base row.  After cancelling all such
variables and rows, a tight fractional base edge supports at least two
positive variables, whereas a slack one supports at least one.  If their
counts are `a,b`, respectively, then `2a+b<=a+D`, so at most `D` base edges
are fractional.  Discarding them loses at most `D` total LP mass.

For each type, the remaining unit assignments form a simple graph `F_i` of
maximum degree at most `m_i`, and different types use disjoint base edges.
Vizing gives at most `m_i+1` matching colors.  Keeping the `m_i` largest
colors discards at most

```text
|E(F_i)|/(m_i+1) <= |S_i|m_i/[2(m_i+1)] <= |S_i|/2.
```

Assigning the retained colors to distinct centers produces actual
edge-disjoint triangles.  Summing the two losses gives `3D/2`.  No hidden
assumption that the types, neighborhoods, or spoke sets are disjoint occurs.

The odd complete-split family correctly shows that a sublinear loss is
impossible: with one neighborhood `S=C`, odd `k`, and `m=k-1`, the fractional
value is `k(k-1)/2`, while `k-1` near-perfect matchings give the exact integer
value `(k-1)^2/2`.

### Residual clique packing

After `h` centered triangles, the residual clique graph has
`e=binom(k,2)-h` edges.  For every edge `uv`, inclusion--exclusion gives at
least `d(u)+d(v)-k` common neighbors.  Summing and applying Cauchy--Schwarz
proves

```text
t(R) >= e(4e-k^2)/(3k).
```

Labeling vertices by distinct residues modulo `k` partitions all triangles
by label sum; triangles in one class cannot share an edge because the shared
edge and class determine the third label.  Averaging therefore supplies the
claimed `t(R)/k` residual packing.  A negative right-hand side is harmless.

The resulting polynomial

```text
f_k(h)=k^2/6-k/2+1/3+4h/(3k)+4h^2/(3k^2)
```

is increasing on `h>=0` and convex.  If the rounded packing has
`h>=H-3D/2`, its actual `h` is still nonnegative.  The global tangent
inequality at `H`, together with `f_k'(H)>0`, yields

```text
2nu >= 2f_k(H)-3D f_k'(H).
```

This explains why the proof remains valid even when `H-3D/2<0`; it does not
substitute a negative argument into the monotonicity statement.

### Cover, saturation, and numerical cutoff

Put every independent vertex on one cut side and choose `ell` clique
vertices for the other.  The complement of the cut is a triangle cover.
Its expected size is

```text
q-ell(k-ell)+E(1-ell/k).
```

The real minimizer `(k+E/k)/2` lies in `[0,k]`, since spoke saturation gives
`E/2<=q`.  Rounding `ell` costs at most `1/4`, proving the stated cover
bound.  Subtracting it from the packing bound, using `D<=rk`, and retaining
the correct signs gives the quadratic in `t=E/k^2`.  Completing the square
produces exactly

```text
k^2/66 -(12r/11)k-48r^2/11
```

for its quadratic part.  Substitution `k=80r+40+u` expands to a sum with all
positive coefficients and constant `205/44`, so the strict cutoff is sound.

Finally, the local certificate sets every eligible variable to
`m_i/(|S_i|-1)`.  Each type-vertex row then has load exactly `m_i`, and the
pair condition is exactly base-row feasibility.  This proves sufficiency,
not necessity, as claimed.  The four-vertex obstruction and the 280-clique
crossing-neighborhood example respect the stated scope.

## Reproduction and independent computation

Using CPython 3.11.2, I reran the target audit.  It matched `AUDIT.json` byte
for byte in normal execution, with SHA-256
`5d7ebd3ef91ba49a05f313c71477820d8dec2c332c098f9fbc6b8d5a2bdb19af`.
The target checks 33,868 edge-coloring instances, 290 exact LP pairs,
190 definition-level integer centered optima, 1,881 scalar identities, 31
sharpness cases, and regenerates the large feasible packing and cut.

The new [`independent_check.py`](independent_check.py) imports no target code,
output, or certificate.  It independently builds and solves the centered LP
over the rationals, proves each computed optimum with a dual solution,
computes the integer centered optimum by a separate matching-mask dynamic
program, and audits the extreme-point row counts.  Across all one- and
two-type instances in its specified exhaustive domain, including every base
graph through four vertices, it checks:

```text
16,076 exact LP/integer pairs
718 nonintegral instances
75 local saturation certificates
87 spoke-saturated complete-base instances
worst observed gap = 1, with gap/D = 1/3
record digest = 1f36703a497438a6ca276a6cf54bc890c44e575c0157ffda526673ffcff0bb0e
```

It also exhausts all 33,867 graphs through six vertices for the residual
degree-sum and modular-label packing lemmas, encountering 83,233 triangles.
For all 87 small saturated instances it separately computes exact full-graph
triangle packing and cover numbers by definition-level recursion.  Finally,
it checks 214,137 convex-tangent instances, 10,250 square completions, 1,050
threshold cases, and the odd complete-split family through clique order 31.
Normal, repeated, and optimized executions agree byte for byte.  Expected
output SHA-256:
`cb50ad446198bc57489f3d9e65c85b6266fe61ab36a422ee748369a7c5231160`.

## Checker guarantees and trust boundary

The universal proof, not either finite audit, establishes the two theorems.
The target checker guarantees the listed exact finite computations, generated
packing membership, edge disjointness, cut size, LP primal/dual feasibility,
and deterministic hashes.  The independent checker covers a different,
fully stated finite domain and uses no target implementation.

Both audits trust CPython integer and `Fraction` arithmetic and their short
visible algorithms.  Neither uses floating-point evidence, random solver
verdicts, an external dataset, a downloaded certificate, or an omitted bulk
witness.  The theorem additionally relies on finite-dimensional LP
extremality/duality and Vizing's theorem.  The Misra--Gries program is only a
finite implementation of the edge-coloring step; its correctness is not a
premise once Vizing's theorem is accepted.

## Literature status, novelty, and publication readiness

The primary literature confirms that matching and edge-coloring methods are
standard in complete split and threshold-graph triangle packing.  In
particular, Puleo's 2017 paper explicitly identifies centered packings in a
one-neighborhood join with partial `k`-edge-colorable subgraphs.  This is
close enough that it should be cited in the target's literature discussion;
the omission is an attribution gap, not a mathematical defect.

Puleo does not state the multi-type fractional LP rounding estimate, the
multiplicity-independent `3D/2` loss, or the spoke-saturated numerical cutoff.
The threshold-graph theorem, the dense minimum-degree theorem, and the recent
eight-clique/two-type finite theorem likewise have different hypotheses.
Targeted searches recorded in [`SOURCES.md`](SOURCES.md) found no matching
statement.  The two quantitative results therefore appear new relative to
the inspected sources, without any claim of absolute priority.

The result is publication-ready as a conditional split-graph theorem once
the nearby edge-colorable-subgraph attribution is added.  The saturation
hypothesis and centered-versus-unrestricted distinction must remain prominent.

## Remaining gaps

- Spoke saturation is a genuine additional hypothesis.  The theorem does not
  handle every fixed collection of neighborhood types.
- The `3/2` constant is not sharp; the demonstrated lower bound on any
  universal constant is only `1/2`.
- The numerical cutoff `80r+40` is uniform and explicit but deliberately
  discards favorable terms and instance-specific values of `D,E`.
- Neither universal proof has been formalized in a proof assistant or checked
  by external peer review.
- The independent exhaustive computations stop at base order four for the LP
  comparison and order six for the residual graph lemma.
- Novelty is based on a bounded primary-literature search.

## Strengthening and improvement opportunities

1. **Remove or characterize spoke saturation.**  The highest-impact next
   step is a necessary-and-sufficient dual or cut characterization for
   simultaneous type-wise degree saturation under shared base-edge
   capacities.  A repair theorem that discards only `O(D)` unsaturated spoke
   mass would extend the explicit Tuza bound to substantially broader
   fixed-type split graphs.
2. **Reduce the `3D/2` rounding loss.**  The complete-split example forces at
   least `D/2` in general, but the proof separately pays `D` for fractional
   base rows and `D/2` for edge coloring.  Coupling the choice of optimal
   extreme point with a maximal `m_i`-edge-colorable subgraph argument, such
   as the structures studied by Puleo, may avoid paying both losses in full.
3. **Optimize the explicit cutoff.**  Retaining `4E/(3k)`, using the actual
   `D` instead of `rk`, and minimizing the exact integer cut quadratic would
   give a sharper instance-dependent criterion.  A rigorous optimization
   over the feasible `(D,E)` region could lower the uniform coefficient 80.
4. **Round centered and clique fractions jointly.**  The present theorem
   deliberately realizes only centered mass before using a residual clique
   count.  A joint extreme-point or absorption argument for both kinds of
   fractional triangles is the missing bridge toward an effective theorem
   for arbitrary bounded-type split graphs.
