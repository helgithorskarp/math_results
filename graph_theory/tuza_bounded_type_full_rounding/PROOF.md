# Full fractional rounding and an effective bounded-type Tuza theorem

All graphs are finite and simple. Write `nu` for the maximum number of
edge-disjoint triangles, `nu*` for the fractional triangle-packing
optimum with unit edge capacities, and `tau` for the minimum number of
edges meeting every triangle. Fractional packings here include **all**
triangles, including those wholly within a split graph's clique.
All logarithms are natural.

A **twin partition** has classes, each inducing a clique or an independent
set, such that between any two classes all edges or no edges occur. We
only need a specified partition with at most `d` classes; it need not be
a minimum partition. This is the usual neighborhood-diversity setting.

## 1. Quantitative full-packing theorem

**Theorem 1.** A graph on `n>=3` vertices with a twin partition into at
most `d>=1` classes satisfies

```text
0 <= nu*(G)-nu(G)
   <= [10^10 d log(400n)]^(1/7) n^(13/7).                (1)
```

In particular, for fixed `d`, the additive error is
`O_d(n^(13/7) (log n)^(1/7))`, with the displayed numerical constant.
This is an estimate for the full LP. It uses neither the previously
refuted centered-cover estimate nor a spoke-saturation assumption.

We first prove the following finite parameter bound. For any
`0<epsilon<=1/2`, set

```text
s = ceil(2 + 10^8 epsilon^(-6) log(400 n^2/epsilon^2)).
```

Then

```text
nu*(G)-nu(G) <= epsilon n^2/6 + d s n/2.                 (2)
```

Delete every twin class of size less than `s`. At most `d(s-1)` vertices
are removed. In an optimal fractional packing, the total weight of
triangles containing a vertex `v` is at most `deg(v)/2`, since each such
triangle uses two edges incident with `v`. Summing over removed vertices
bounds the lost fractional weight by `d s n/2`, even when some triangles
are counted more than once. Let the remaining induced graph be `G'`.

Average an optimal fractional packing of `G'` over all permutations
within its remaining classes. These permutations are automorphisms, so
the average is feasible, optimal, and constant on triangle orbits. Fix
any supported triangle, fix one of its edges, and vary its third vertex
within that vertex's class, while avoiding the two fixed endpoints.
There are at least `s-2` choices, all giving triangles with the same
weight `x`. The fixed edge's capacity gives `(s-2)x<=1`. Consequently
every weight in the averaged optimum is at most `1/(s-2)`.

Form the triangle hypergraph of `G'`: its vertices are graph edges and its
hyperedges are the three edge sets of graph triangles. This hypergraph is
linear: two distinct graph triangles share at most one graph edge. It
has at most `n^2` vertices. The definition of `s` permits application of
the [quantitative fractional-matching lemma](NIBBLE.md), giving

```text
nu(G') >= (1-epsilon) nu*(G').
```

If `G'` is triangle-free the same conclusion is immediate. Since
`nu*(G')<=n(n-1)/6<=n^2/6`, the deletion bound and packing monotonicity
prove (2). No assumption that an optimal packing has small weights before
symmetrization was made.

To derive (1), put `L=log(400n)` and

```text
epsilon = [10^10 d L/n]^(1/7).
```

If `epsilon>1/2`, the trivial bound `nu*-nu<=n^2/6` is already smaller
than `epsilon n^2`. Otherwise `epsilon>=n^(-1/7)`, and hence

```text
log(400 n^2/epsilon^2) <= 3L,
s <= 3 + 3*10^8 epsilon^(-6)L.
```

Using `epsilon^7=10^10 d L/n`, the right side of (2) is at most

```text
epsilon n^2 (1/6+3/200) + 3dn/2.
```

Moreover `(3dn/2)/(epsilon n^2)=3epsilon^6/(2*10^10 L)<1/100`.
Thus this bound is smaller than `epsilon n^2`. This proves (1), including
the cases in which the displayed estimate is larger than the trivial
bound. The exponent and constants are not claimed sharp.

## 2. The existing finite fractional Tuza gap

We use the accepted finite result h5713, with proof and independent review
linked in [SOURCES.md](SOURCES.md). For a split graph with clique order
`k` and at most `r>=1` active independent-neighborhood types, it gives

```text
2nu* - tau >= [k^2-2k-32(r+1)] / [8(8r+11)].            (3)
```

Here an active neighborhood has at least two vertices. Arbitrary original
multiplicities are allowed. Its previously known integer consequence
used an unspecified Haxell--Rodl cutoff. The new ingredient is (1).
Equation (3) is an explicit external mathematical dependency; this
package does not describe that prior result as newly proved here.

For completeness, recall why multiplicities can be capped for applying
(1). Delete inactive centers, and replace each multiplicity `m_i` by
`min(m_i,|S_i|-1)`. The cap preserves `tau` and cannot increase `nu`.
In a minimum cover of the capped graph let `F` be the surviving
triangle-free clique core. Copies of a given type can all keep the same
maximum independent set `A` in `F[S]`. Every edge of `F[S]` meets `S\A`,
so `e(F[S])<=(|S|-1)|S\A|`. For a capped type, deleting these surviving
core edges costs at most restoring its deleted spokes. All its spokes
can now be restored and arbitrarily many identical centers added.
Repeat for each capped type. Core-edge deletion preserves earlier
repairs. This proves the nontrivial inequality for cover preservation;
the reverse and packing monotonicity follow by subgraph containment.

The capped graph has at most `(r+1)k` vertices. Its core splits into at
most `2^r` clique classes according to membership in the neighborhoods.
Its independent side has at most `r` classes. This is a twin partition
with at most

```text
d_r=2^r+r
```

classes, including arbitrary overlaps and unequal cell sizes.

## 3. An entirely numerical cutoff

For each integer `r>=1`, define the following integers:

```text
A = 8r+11,
d = 2^r+r,
C = 400(r+1),
B = 10^10 d (64A)^7 (r+1)^13,
ell = bit_length(4BC),
K_r = max(16(r+1), 4B ell).                             (4)
```

Here `bit_length(t)` is the unique positive integer `ell` satisfying
`2^(ell-1)<=t<2^ell`. Formula (4) contains no unspecified existence
constant, LP threshold, or unevaluated asymptotic modulus.

**Theorem 2.** Every split graph with a specified clique of order
`k>=K_r` and at most `r` active neighborhood types satisfies

```text
2nu(G)-tau(G) >= k^2/[16(8r+11)] > 0.                   (5)
```

There is no restriction on the original independent-side multiplicities
or on the number of inactive centers.

Work in the capped graph, of order `n<= (r+1)k`. Theorem 1 gives

```text
nu*-nu <= [10^10 d log(Ck)]^(1/7) ((r+1)k)^(13/7).
```

This is at most `k^2/(64A)` whenever `k>=B log(Ck)`.
To verify the latter inequality, put `K=4B ell`. Since
`log(4BC)<=ell` and `log ell<=ell`,

```text
log(CK)=log(4BC)+log ell<=2ell=K/(2B).
```

For any `k>=K`, `log(k/K)<=k/K-1` and `K>=2B` give
`log(Ck)<=K/(2B)+(k-K)/K<=k/(2B)<=k/B`. The maximum with
`16(r+1)` in (4) also ensures `2k+32(r+1)<=k^2/4`.

Equation (3) therefore gives `2nu*-tau>=3k^2/(32A)`, while
`2(nu*-nu)<=k^2/(32A)`. Subtracting proves (5) in the capped graph.
Cover preservation and packing monotonicity transfer it to the original
graph.

The explicit integer for three types is printed and independently
checked in `AUDIT.json`. Its magnitude is very large. This supplies an
effective theorem and a fully specified finite-exception reduction, not
a practically enumerable three-type classification. Tuza for every
three-type graph, including all smaller clique orders, remains open in
this research lane.

## 4. Scope and assurance

The main new mechanism is full fractional rounding through a quantitative
weighted nibble and twin-class symmetry. It applies to all graphs with
a specified twin partition, not just split graphs. The Tuza application
uses the earlier finite fractional gap. No centered-cover formula,
centered-only rounding, saturation hypothesis, or general asymptotic
packing theorem is substituted for the full rounding step.

The universal proof is unformalized and awaits independent mathematical
review. The concentration argument, dependence calculation, termination
rule, and accumulated objective are proved in NIBBLE.md. The finite exact
audit checks one-round probabilities, influences, constants, symmetry,
and cutoff arithmetic. Such audits cannot certify a universal probability
inequality or replace the analytic proof, and they do not run the process
on a graph of order `K_r`.
