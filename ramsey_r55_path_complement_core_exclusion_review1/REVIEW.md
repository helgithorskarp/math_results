# Independent review of h3931 hereditary core exclusion

**Verdict: ACCEPT as a complete hereditary-family exclusion, not as the
Ramsey target result.**

This review verifies Discovery Net h3931,
`bafkreif2yr3qvnkolxmmzy44ntigchjluornje6majm63gjsmj2z3c2wd4`, at source
commit `e7d5932b57e804bf1f2dcb00f89360af0f76fa2e`.  Write `C` for the hereditary
class of graphs with neither an induced `P5` nor an induced complement of
`P5`, and let

```text
f(a,b) = max {|V(G)| : G in C, omega(G) <= a, alpha(G) <= b}.
```

The accepted exact table, with rows indexed by `a` and columns by `b`, is

```text
      b=1  2   3   4
a=1    1  2   3   4
  2    2  5   7  10
  3    3  7  11  16
  4    4 10  16  25.
```

The equality graph for `f(4,4)=25` is uniquely `C5[C5]` up to isomorphism.

## Structural proof audit

Take a modular partition with as few parts as possible and form its quotient
`Q`.  If a proper vertex set of `Q` were homogeneous, the corresponding union
of parts would coarsen the partition, so `Q` is prime (with the harmless
two-vertex cases included below as perfect quotients).  Representatives show
that `Q` also belongs to `C`.

The imported Fouquet decomposition says a prime member of `C` is `C5` or is
`C5`-free.  A `C5`-free member of `C` has no odd hole: a hole of length at
least seven contains an induced `P5` on five consecutive vertices.  Applying
the same observation to the complement rules out odd antiholes.  The Strong
Perfect Graph Theorem therefore makes this second kind of quotient perfect.

For a part `M_i`, put

```text
p_i = omega(G[M_i]),     q_i = alpha(G[M_i]).
```

Clique and stable-set numbers under substitution are the corresponding
weighted maxima over cliques and stable sets of `Q`.  No proper part has
`(p_i,q_i)=(a,b)`: any outside vertex is uniformly complete or anticomplete to
the part and would then create a clique of size `a+1` or a stable set of size
`b+1`.  Thus every part uses an already established, lower parameter-sum
entry of the induction.

Define

```text
rho = max f(p,q)/(pq)
```

over those proper child pairs.  If `Q` is perfect, replicate its vertex `i`
to a clique of order `p_i`.  The replication lemma preserves perfectness, and
the resulting graph has clique number at most `a`, so it has an `a`-coloring.
Each color class maps to a stable set of `Q` and hence has total `q_i`-weight
at most `b`.  Summing over colors gives

```text
sum_i p_i q_i <= ab,
|V(G)| <= sum_i f(p_i,q_i) <= floor(ab rho).
```

If `Q=C5`, the only constraints are

```text
p_i+p_(i+1) <= a,       q_i+q_(i+2) <= b
```

cyclically.  Exhausting these positive integer weights closes each table row.
The reviewer implementation organizes this as two independent recursive
five-coordinate enumerations and then takes their Cartesian product; it does
not import the source enumerator.

At `(a,b)=(4,4)`, the perfect-quotient bound is 21.  The `C5` calculation has
the unique maximizing weight vector

```text
p_0=...=p_4=q_0=...=q_4=2,
```

and all five parts must attain `f(2,2)=5`.  An exhaustive five-vertex check
finds 12 labeled such graphs, all cycles, hence one isomorphism type `C5`.
It follows inductively that equality at order 25 is uniquely `C5[C5]`.

## Target-facing consequences

A good43 is a graph with clique and independence numbers at most four.  Since
`f(4,4)=25`, every induced 26-vertex subgraph of a hypothetical good43 contains
an induced `P5` or induced complement-`P5`.  Therefore:

1. deleting vertices until both patterns disappear requires at least 18
   deletions; and
2. greedily applying the 26-vertex statement at residual orders
   `43,38,33,28` gives four vertex-disjoint copies drawn from the two patterns.

These are necessary conditions on a hypothetical target.  They do not produce
a good43, decide any of the 2,189,178 physical packing tasks, or prove
`R(5,5) >= 44`.

## Reproduction and independent checks

The source manifest SHA-256 is
`164b68e641bc1401a76fcd61b44191b52075b86e493ccfcc6c83d3e955c3daf3`.
All 17 entries passed.  The complete source replay matched its committed
outputs both normally and with `-O`; its own replay in turn checks every
producer, witness, checker, and physical-interface control in both modes.

The reviewer-authored checker independently:

- reconstructs all 16 recurrence rows and all 4,761 admissible weighted-cycle
  cap incidences;
- reproduces the exact upper-bound table, rational envelope attainers, and
  every cycle maximizer set;
- uses a separate bit-set branch-and-bound algorithm to find exact clique and
  independence numbers for all 16 committed witnesses;
- checks all 62,875 witness five-subsets for both forbidden induced patterns;
- classifies all 1,024 labeled five-vertex edge words, finding 60 path words
  and 60 complement-path words;
- exhausts the 1,024 five-vertex graphs to establish the single `C5`
  isomorphism type at `f(2,2)=5`; and
- constructs `C5[C5]` independently and matches the literal 25-vertex top
  witness, including its 150 edges and constant degree 12.

Normal and assertion-disabled independent runs produce exactly
[EXPECTED.json](EXPECTED.json).

## Imported trust boundary

The Fouquet decomposition theorem and the Strong Perfect Graph Theorem are
not reproved.  Their statements were checked against primary mathematical
sources:

- Chudnovsky et al., *Graphs with no induced P5 or complement-P5*, Theorem
  2.1, restating Fouquet's decomposition:
  <https://web.math.princeton.edu/~mchudnov/decompP4CP4.pdf>
- Chudnovsky, Robertson, Seymour, and Thomas, *The Strong Perfect Graph
  Theorem*, Theorem 1.2:
  <https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n1-p02.pdf>

The review independently supplies the short bridge from those statements to
the quotient dichotomy used here, but trusts the published theorem proofs.
Residual trust also includes the modular-decomposition argument, the written
replication and substitution proof, CPython integer and file semantics,
SHA-256, the two implementations, the operating system, and hardware.  No
catalog completeness, SAT solver, or external computational dataset is used.
