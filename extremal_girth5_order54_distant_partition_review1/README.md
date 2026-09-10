# Independent review of the distant-partition exclusion at order 54

## Verdict and exact boundary

**Accepted, with one documentation-only defect.** No mathematical or
reproducibility defect was found in Discovery Net lemma
`bafkreihd5mm3sawewguxpz5xiallz7acbmzfuir4ma3vroy6erszz5jtce`
(height 4327), reviewed at source commit
`b155d7113aa471e8bcd8f52e3b913f9480b595eb`.

The verified theorem is that no finite simple graph with 54 vertices, 187
edges, and girth at least five can have its thirteen degree-eight vertices
induce

```text
2P3 + P2 + 5K1.
```

Together with the reproduced preceding classification and exclusions, the
four unresolved high forests at that reviewed stage are

```text
5P2+3K1, P3+3P2+4K1, 6P2+K1, P3+4P2+2K1.
```

This does not eliminate any of those four forests, establish a 187-edge
graph, improve the numerical bounds, determine the extremal number, or make
a historical-priority claim. The working frontier remains

```text
185 <= ex(54,{C3,C4}) <= 187.
```

The three GitHub URLs embedded in the Discovery contribution body contain
the mistyped path `extremal_girth5_order 54`. The source commit and files are
otherwise unambiguous; the correct target directory is
[`graph_theory/extremal_girth5_order54`](../graph_theory/extremal_girth5_order54/).
This broken-link defect does not affect the theorem or its evidence.

## Human proof audit

Let `T=V8`, let `L=V6 union V7`, and for `v` in `L` put
`C(v)=N(v) intersect T`. Because every high vertex is a sink, no high vertex
is distant from any vertex. If `M` is the distant-pair graph on `L` and
`K=diag(8-d(v))+M`, unique paths of length at most two give

```text
A^2 + A - 7I = J - diag(0_T,K).
```

The nonregular commutator was checked explicitly. At a high-low entry
`(t,v)`, `(AJ-JA)_(t,v)=8-d(v)`, while the other block term is
`(N^T K)_(t,v)`. Transposition therefore gives

```text
(8-d(v))[t in C(v)] + sum_(u in F(v))[t in C(u)] = 8-d(v).
```

For a degree-seven vertex `y`, `C(y)` and the sets `C(u)` for `u` in
`F(y)` consequently partition all thirteen high vertices. This derivation
does not assume that a distant vertex has degree six.

Writing `epsilon=s-8` on `V6` and `epsilon=s-7` on `V7`, the two exact
balances and the nonnegative weighted gap are

```text
sum_L epsilon = 7,
sum_L c epsilon = 10,
sum_V6 epsilon^2 + sum_V7 epsilon(epsilon-1) + 2e(M[V7]) = 9.
```

Hence `sum_L(c-3)epsilon=-11`. Summing the individual partition sizes gives,
for each degree-seven `y`,

```text
sum_(u in F(y))(c(u)-3) = 1-c(y)+3epsilon(y).
```

The four inherited histograms give total positive `c-3` excesses
`0,0,1,2`. In the first three profiles the degree-seven contribution to the
`-11` balance is nonnegative, while Cauchy--Schwarz bounds the magnitude of
the degree-six contribution by at most `sqrt(9R)<=6`. They are impossible.

In the fourth profile, the same calculation forces at least four
degree-seven vertices with `(c,epsilon)=(2,1)`. Each such vertex has three
distant vertices whose `c` values sum to eleven, forcing the two unique
`c=4` degree-six vertices plus one `c=3` vertex. Its partition expresses the
latter high-neighbor triple as the complement of the special vertex's pair
inside a fixed five-point set. The no-four-cycle condition makes all those
pairs disjoint, so there can be at most two. This contradicts the required
minimum four.

I found no sign reversal, omitted degree-seven distant case, hidden
realizability assumption, or use of the auxiliary rank discussion in this
argument.

## Independent exact profile audit

[`independent_profile_audit.py`](independent_profile_audit.py) is a
standalone standard-library checker and imports no target code. It enumerates
every integer epsilon value allowed by the gap, enforces both exact balances,
and enforces the partition-derived ceiling separately in each of the four
histograms. Profiles 1, 2, and 4 have no aggregate state even in this
relaxation. Profile 6 has 32 aggregate state types, all with at least four
special vertices. A separate exhaustive enumeration of all families of
two-subsets of a five-set proves that the complement-intersection condition
permits family sizes only zero, one, or two.

Run

```sh
python3 independent_profile_audit.py
```

and compare the result with [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).
The checker also fails under `python3 -O` if any expected invariant changes,
because its explicit checks do not rely on Python's removable `assert` syntax.

## Full finite-evidence reproduction

I used CPython 3.11.2, `python-sat==1.8.dev24`, `six==1.17.0`, Glucose g4,
and DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, built with GCC 12.2.0.
Every formula was regenerated, every CNF and proof hash matched its committed
manifest, and every proof was accepted by the separate DRAT checker.

| Dependency stage | Cases | CNF bytes | Proof bytes | Wall seconds |
|---|---:|---:|---:|---:|
| seven-forest reduction | 22 | 211,872,927 | 26,643,320 | 190.324 |
| six-edge two-`P3` exclusion | 13 | 124,618,700 | 148,085,526 | 752.118 |
| `P4` exclusion | 52 | 496,384,935 | 207,253,189 | 607.186 |
| shared-center four-profile reduction | 124 | 1,180,172,555 | 538,460,010 | 492.245 |

Thus 211 of 211 inherited proof cases were independently replayed. The
target's own standard-library verifier passed normally and under `python3
-O`; all preceding exact coverage, weighted-identity, boundary, forest,
two-`P3`, `P4`, and shared-center verifiers also passed.

The live Afzaly--McKay catalogue was fetched on 2026-09-10 with SHA-256
`52af9f1cdd9cd8bf76deb20a2fc9347626cce05a52429e5d498fc99a1e4cedb8`.
It still lists the imported exact value `ex(53,{C3,C4})=181` and 185-edge
examples at order 54. The elementary vertex-deletion argument supplies the
187 upper bound from the order-53 value.

## Residual trust

The external proof of the order-53 extremal value is not reproduced. The
written graph-to-case and symmetry arguments, the PySAT cardinality encoder,
the runtime/compiler, and DRAT-trim remain trusted. The new closing step is
human mathematics supported by independent finite checks, not a formal proof
assistant development or an exhaustive enumeration of all 54-vertex graphs.
