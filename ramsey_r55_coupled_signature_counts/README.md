# Coupled signatures: 73 global hard-branch candidates and 290 anchored splits

The coupled exceptional-neighborhood signature equations exclude eight more
hard-branch global degree profiles and 17 anchored splits. The team's
remaining counts decrease from **81 to 73 globals** and **307 to 290 splits**.
No automorphism assumption is used.

More precisely, all 4,937 labeled exceptional cores surviving the previous
small-core screen are classified for the full capped signature-count system:
4,800 have explicit integer solutions and 137 are infeasible even over the
reals. The certificates represent 374 orbits under degree-preserving
relabelings: 332 primal and 42 dual. Every labeled instance is covered and
checked after transport, not just counted indirectly.

This is not a graph-existence classification. The positive objects assign
central vertices to exceptional-neighborhood signatures, but do not enforce
the Ramsey edges within and between these cells. The 56 inherited profiles
with more than six exceptional vertices remain unclassified here. The low-
deficiency branch and the desired 43-vertex construction remain unresolved.

## Mathematical system and input scope

We inherit the hard branch of a hypothetical `(5,5;43)` graph, with red chosen
to be the sparser color and `m=231+M`. The local extrema and weighted-neighbor
inequality are

```text
d        18   19   20   21   22   23   24
U(d)     85   92  100  107  114  122  132
b(d)    220  221  220  220  221  223  223,
sum_(w in N_R(v)) (d(w)-21) <= M-b(d(v)).                (1)
```

Let `E={v:d(v)!=21}`, `F=G[E]`, `k=|E|`, `C=V(G)\E`, and `N=43-k`.
The symbols `d_i` are the exceptional vertices' global degrees, not their
degrees in `F`. Put `epsilon_i=d_i-21`. Every actual core obeys

```text
sum_(j in N_F(i)) epsilon_j <= M-b(d_i),
sum_i epsilon_i*(d_i-deg_F(i)) <= N*(M-220),             (2)
```

and has no red or blue `K_5`. Order its vertices by nondecreasing `d_i`.

For a central vertex, its signature is `X=N_R(v) intersect E`. The previous
[signature-capacity lemma](../ramsey_r55_exceptional_signature_capacity/README.md)
sets capacity zero unless

```text
sum_(i in X) epsilon_i <= M-220,
r_X=omega(F[X]) <= 3,       s_X=alpha(F[E\X]) <= 3.
```

For an admissible signature it gives

```text
c_X=min(N,choose(8-r_X-s_X,4-r_X)-1).                    (3)
```

This uses only the elementary Ramsey recurrence. The cell of vertices with
signature `X` cannot contain a red `K_(5-r_X)` or blue `K_(5-s_X)`, since
either extends to a forbidden five-set through its common exceptional
neighbors. Formula (3) is a conservative upper bound, not proof that a cell
of order `c_X` exists.

The exact coupled count problem studied here is

```text
sum_X y_X=N,
sum_(X containing i) y_X=d_i-deg_F(i) for every i,
0<=y_X<=c_X,       y_X integer.                          (4)
```

The previous result tested only individual red/blue capacity projections.
Its 25 surviving profiles with `k<=6` contain 4,937 labeled cores. This
entire universe, not a selection of favorable cores, is the input here.
The earlier seven rejected small profiles and all larger profiles retain
their previous status.

## Exact primal and dual evidence

Write `a_X=(1,1_(0 in X),...,1_(k-1 in X))` and
`b=(N,d_0-deg_F(0),...,d_(k-1)-deg_F(k-1))`. Then (4) is
`sum_X a_X*y_X=b` with the stated integer box bounds.

A primal certificate lists all nonzero `(X,y_X)` pairs. The checker verifies
integrality, all capacities, and every equality by exact integer arithmetic.

A dual certificate is an integer vector `lambda` with

```text
lambda dot b > sum_X c_X * max(0,lambda dot a_X).        (5)
```

This proves real infeasibility: for any `0<=y_X<=c_X`,
`sum_X y_X*(lambda dot a_X)` cannot exceed the right side, but the
equalities would make it exactly the left side. No optimization verdict or
numerical tolerance appears in this proof. All stored dual coordinates have
absolute value at most three.

Numerical MILP finds candidate primal certificates; an auxiliary LP finds
candidate separating vectors when needed. Rounding is not trusted: primal
vectors and rationally reconstructed, integer-scaled dual vectors must pass
(4) or (5) exactly before the generator emits anything. Unfinished solves,
missing certificates, or failed reconstruction stop generation with an error.

For these particular 4,937 systems, real and integer feasibility give the
same verdict. This does **not** assert that their polytopes are integral or
that all related signature systems have this property.

## Relabeling is not an automorphism assumption

Vertices of `F` with equal global degree can be renamed. Such a permutation
preserves (2), transports signatures and capacities, and simply permutes the
last `k` coordinates of `a_X,b,lambda`. An integer witness or a contradiction
therefore transports to every graph in the orbit.

The generator forms these permutations as a product over the degree classes.
The checker instead filters all `k!` permutations for preservation of the
degree labels. It requires each representative to be the least edge mask in
its orbit, checks the stated orbit size, rejects overlap, and requires the
union to be exactly the independently reconstructed marginal-survivor set.
It then transports and verifies the certificate at **every labeled core**.
No symmetry of a hypothetical full 43-vertex graph is assumed or imposed.

## Classification and structural consequences

The 137 rejected labeled cores lie in 14 profiles. Eight of those profiles
lose all their cores; six lose some but retain an integer witness. The other
11 input profiles lose no core. Thus 17 of the 25 small profiles remain.

| Newly excluded global degree multiset | M | Rejected input cores | Removed splits |
|---|---:|---:|---:|
| `19^2 20^1 21^40` | 218 | 1 | 1 |
| `19^3 21^39 22^1` | 218 | 3 | 1 |
| `18^1 20^2 21^38 22^2` | 219 | 16 | 3 |
| `18^1 20^3 21^38 22^1` | 218 | 39 | 3 |
| `18^1 20^4 21^38` | 217 | 38 | 2 |
| `18^1 19^1 21^39 22^2` | 219 | 2 | 2 |
| `18^1 19^1 20^1 21^39 22^1` | 218 | 2 | 3 |
| `18^1 19^1 20^2 21^39` | 217 | 2 | 2 |

The eight full-profile exclusions account for 103 of the rejected labeled
cores; the other 34 are in the six partially retained profiles. The complete
25-row [SUMMARY.tsv](SUMMARY.tsv) gives every profile-level count.

The remaining global counts for `M=214,...,220` are
`1,3,7,11,15,18,18`; remaining anchored split counts are
`1,5,17,35,59,80,93`. These sum to 73 and 290, respectively. These are
remaining **candidates**, not feasible graph counts: 17 small profiles with
count witnesses plus 56 larger profiles not classified by this computation.

**Corollary.** A hard-branch graph with a degree-18 or degree-24 vertex must
have at least seven vertices of degree different from 21. Indeed, all 17
remaining small profiles lack both extreme degrees. The complete inherited
profile universe and its earlier exclusions cover the other small cases.
Complementing preserves the exceptional set and interchanges 18 and 24.

### Two count-cover obstructions visible without optimization

For `19^2 20^1 21^40`, the individual exceptional rows force `F=K_3`.
Each central signature must include a degree-19 vertex: without either one
it has weighted sum at least -1, whereas (1) requires at most -2.
There are 40 central vertices, but the two degree-19 vertices have only
`(19-2)+(19-2)=34` red incidences into `C`. The cover is impossible.
The certificate is `lambda=(1,-1,-1,0)`, with left side six and right side
zero in (5).

For `19^3 21^39 22^1`, the three degree-19 vertices must form a red triangle.
For a central vertex let `l` count its red neighbors among those three and
`h` be its incidence to the degree-22 vertex. The weighted condition is
`2l-h>=2`. Since `h` is zero or one, it implies `l-h>=1`.
Summing over 39 central vertices requires at least 39. In fact the sum is

```text
(3*19-22) - (sum_low deg_F(i)-deg_F(high)) = 35-6 = 29,
```

because the low triangle contributes six internal incidences and the
low-high edges cancel. This is another contradiction; the stored dual is
`(1,-1,-1,-1,1)`. Such rounded incidence-cover constraints explain why
joint signatures can fail when every separate marginal passes.

## Positive certificates and the graph boundary

For each of the 332 primal representatives, the checker makes `y_X` copies
of each signature and attaches them to `F`. Their remaining red degrees are
`21-|X|`. A deterministic largest-residual-degree construction fills edges
inside `C`, after which the checker verifies all 43 prescribed global
degrees, the edge count, and all weighted inequalities (1).

Every one of these chosen completions contains an explicitly found
monochromatic five-set, whose ten pairs are checked literally. Thus they
are actual degree/weighted-relaxation graphs, not Ramsey witnesses. This
finite validation does not appeal to a general degree-sequence theorem;
each completed graph is checked directly. It does not assert that every
possible choice of an integer signature witness admits this construction.
Other labeled cores inherit a completion by relabeling the representative.

The original local edge-count caps, sharper cell Ramsey bounds, and the
edges within/between cells are not enforced by (4). A positive certificate
must never be reported as a hard-branch Ramsey graph.

## Reproduction and certificate format

Solver-free checking requires only Python 3.11.2 and its standard library:

```bash
set -o pipefail
python3 ramsey_r55_coupled_signature_counts/verify_certificate.py \
  | cmp - ramsey_r55_coupled_signature_counts/EXPECTED_OUTPUT.txt
python3 -O ramsey_r55_coupled_signature_counts/verify_certificate.py --emit-summary \
  | cmp - ramsey_r55_coupled_signature_counts/SUMMARY.tsv
cd ramsey_r55_coupled_signature_counts
sha256sum -c SHA256SUMS
```

The checker rebuilds all 209,443 raw labeled cores in the prior 32-profile
small universe using Gray-code neighbor sets, computes clique numbers by
literal subset enumeration, derives capacities by the Ramsey recurrence,
and compares every prior stage count and first surviving mask. It imports no
generator or solver code. It also rejects altered primal and zero-dual
evidence. Full verification takes about four seconds on the research host.

`CERTIFICATE.tsv` has 374 rows. Columns specify the global profile, `M`,
representative red-edge mask, orbit size, kind, and payload. Edge bits follow
lexicographic pairs `(i,j)`, `i<j`, on degree-sorted exceptional vertices.
A primal payload is a sorted list `signature:count`; omitted signatures
have count zero. Signature bit `i` means a red neighbor at exceptional
vertex `i`. A dual payload is `lambda_0,lambda_1,...,lambda_k`, with the
constant/total row first. No large proof trace or graph dump is required.

Optional regeneration uses NumPy 2.2.6, SciPy 1.15.3, and its bundled HiGHS 1.8.0:

```bash
task_run=$(mktemp -d /tmp/r55-coupled.XXXXXX)
python3 -m venv "$task_run/venv"
"$task_run/venv/bin/pip" install -r ramsey_r55_coupled_signature_counts/requirements.txt
"$task_run/venv/bin/python" \
  ramsey_r55_coupled_signature_counts/generate_certificate.py > "$task_run/certificate.tsv"
python3 ramsey_r55_coupled_signature_counts/verify_certificate.py \
  --certificate "$task_run/certificate.tsv"
```

Regeneration takes about three seconds on this host. A different valid
primal or dual output is acceptable if the exact checker accepts it; solver
choices are not part of the theorem. Stored evidence has fixed hashes in
`SHA256SUMS`. Regeneration exits on a timeout or missing exact certificate
and does not silently classify such outcomes.

## Trust, context, and next boundary

The [aggregate profile sieve](../ramsey_r55_exceptional_degree_sieve/README.md),
the [signature-capacity reduction](../ramsey_r55_exceptional_signature_capacity/README.md),
and their upstream hard-branch/extremal facts are imported with pinned
manifests. Their catalog-completeness and unformalized-reduction boundaries
remain. The new primal/dual evidence is checked with exact integers and
does not trust SciPy or HiGHS soundness. The new argument is not formally
verified, and this internal checking is not an independent peer review.

The combinatorial method turns local weighted degree conditions into
collective incidence-cover constraints. LP separation is used only to
discover short exact certificates; no historical priority for this standard
convex separation principle is claimed.

The next boundary is sharper feasible cell capacities and edge compatibility
between cells, or a separately scoped larger exceptional stratum. No such
new phase is launched here. Team-r55-1 retains its independent symmetry and
structured-construction direction; no order-five or catalog-radius search
is restarted. This pass ends at the complete coupled-count classification.
