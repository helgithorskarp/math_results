# Uniform realization of robust triangle profiles

Complete author proof, awaiting independent mathematical review. This package
extends the [accepted fixed rational-ray result](../tuza_rational_ray_rounding/README.md)
to varying proportions and real profile values in a specified robust region.
The new mechanism assigns integer vertex roles and uses private auxiliary
edges to prescribe the number of copies of each component in a family
decomposition. The existence input is Keevash's Theorem 5.15; this package
does not prove a new general design-existence theorem.

For a graph with at most `d` mixed twin classes, let `N` be its order. Each
class is a clique or independent set and each pair is completely joined or
empty. A full profile consists of triangle-type masses `x_T` and spare-edge
masses `s_e`, satisfying every exact edge-capacity equality. Include repeated
clique types: this is the **full** fractional triangle-packing LP.

Fix `alpha,epsilon>0`. Suppose each class has at least `alpha N` vertices,
and every positive coordinate of the triangle-plus-spare profile is at least
`epsilon N^2`; zero coordinates are allowed. Put

```text
M = binom(d+2,3) + binom(d+1,2),       lambda = 8M/alpha.
```

For all `N>=N_0(d,alpha,epsilon)`, a packing realizes **exactly**
`floor((1-lambda/N)x_T)` triangles of each positive type. Its size is at least
`sum_T x_T - (lambda/6)N - M`. If such a profile is optimal, this proves

```text
nu*(G) - nu(G) <= (lambda/6)N + M.
```

The threshold is uniform over the indicated region: neither fixed rays nor
rational profile values are required. It remains existential. The result
does not cover positive masses becoming `o(N^2)` or classes becoming `o(N)`;
it is **not** an unrestricted uniform `O_d(N)` theorem or a solution of
all-order three-neighborhood Tuza.

For split templates there is a sharper consequence. If every allowed triangle
type has mass at least `epsilon N^2` in a full fractional decomposition,
then, for all sufficiently large orders uniformly in this region, an actual
triangle decomposition exists **if and only if** all vertex degrees are even
and the edge count is divisible by three. This remains sufficient after
any deletion of fixed bounded maximum degree. A parity cleanup consequently
gives

```text
nu*(G) - nu(G) <= [p + floor(k/2) + 5]/3 <= (N+5)/3,
```

where `k` is the core order and `p` the independent-side order.

The Boolean example has eight clique membership cells and three independent
bit-neighborhood cells. A positive 150-coordinate profile has minimum mass
`1/26`. A rational right inverse proves the hypotheses throughout the box
`0.999t <= n_i <= 1.001t`: once `t` exceeds one fixed existential threshold,
the split criterion and the sharper loss bound apply to **arbitrary integer
proportions** in this box. The explicit `t>=1000` bound in the proof ensures
profile positivity only; it does not bound the design-existence threshold.

Separately, a literal certificate decomposes the unmodified Boolean split
graph with sizes `(5,4,4,4,4,4,4,4,4,4,4)` into 240 triangles. It has 45
vertices and 720 edges. Its correctness is checked directly, without an
asymptotic theorem. See [PROOF.md](PROOF.md) and [SOURCES.md](SOURCES.md).

## Reproduce

Python 3.11.2 was used; the checker needs only the standard library.
From this directory:

```bash
python3 check.py > /tmp/uniform-profile-audit.json
cmp /tmp/uniform-profile-audit.json AUDIT.json
python3 -O check.py > /tmp/uniform-profile-optimized.json
cmp /tmp/uniform-profile-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected output is byte-identical to [AUDIT.json](AUDIT.json), with `PASS`.
[RUN.json](RUN.json) records the interpreter, timing and audit hash.
[check.py](check.py) checks:

- exact profile equations, a 48-column right inverse, and the box estimates;
- quotient/remainder role allocations on all 74 mixed templates with at most
  three classes, plus four complete-graph profiles with large denominators;
- 60 literal realizations of bounded degree lists;
- 156 global and 92 singleton signed lattice witnesses on 26 split templates;
- 818 auxiliary edge constructions and all 120 valid embeddings of a padded
  test graph, including normalization after removing an original edge;
- 33 literal parity cleanups and the 240-triangle decomposition;
- eight negative controls, all rejected.

The role audits use compressed intervals representing classes of at least
`10^12` vertices. They verify every interval's count and degree identities;
they do **not** claim to construct or check a triangle packing of that order.
The small degree-list and embedding checks are finite audits of proof steps,
not a replacement for their universal arguments.

[construct.py](construct.py) supplies the finite constructions.
[CERTIFICATES.json](CERTIFICATES.json) contains only the positive profile and
literal finite packing. The checker reconstructs their graph and incidence
constraints from the definitions, using exact integers and fractions.
It does not verify Keevash's proof, formalize our specialization, determine
`N_0`, or turn finite testing into evidence of universal existence.

## Optional witness discovery

[produce.py](produce.py) uses NumPy and SciPy (originally SciPy 1.17.1):

```bash
python3 produce.py > /tmp/uniform-profile-candidate.json
python3 check.py /tmp/uniform-profile-candidate.json
```

The profile model maximizes a common lower bound on its 150 triangle masses,
subject to the 48 exact capacity equations. A separate binary exact-cover
model searches actual triangles in the 45-vertex graph, with a 30-second
limit. The exact checker validates rational reconstruction and every covered
edge. Neither a solver optimality claim nor an infeasibility claim is needed.
The producer may return another valid certificate or fail within its limit.
No solver, private input, large certificate or downloaded data is needed to
verify the published certificate.
