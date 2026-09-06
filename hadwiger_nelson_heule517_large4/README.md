# H517: the four-large-deletion family is four-colourable

**Every graph obtained from the fixed H517 support by deleting four large
vertices and five small vertices is four-colourable.** By enlargement and
restriction, every subgraph retaining at most 371 large and at most 137
small vertices is four-colourable, including edge-deleted graphs.

Together with the [three-large closure](../hadwiger_nelson_heule517_large3/README.md),
this proves that every non-four-colourable H517 subgraph on at most 508
vertices must retain **at least 138 small vertices and at most 370 large
vertices**. It must delete at least five large vertices. The unrestricted
at-most-508 family remains open. No record graph or unconditional
138-small lower bound for larger graphs is asserted.

## Exact input and inherited positive evidence

G is the fixed [H517 graph](../hadwiger_nelson_heule517_family_pilot/README.md).
Its first 510 points are the increasing union-certificate labels marked
`510`; points 510..516 are completion-centre indices
327,439,671,1040,1074,1377,1383, in that order. These G indices are not
original Heule or Parts labels.

Coordinates have denominator 96 in the positive-radical basis
1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165).
L is the set of points whose sqrt(5),sqrt(15),sqrt(55),sqrt(165)
coefficients vanish in both coordinates, and S is the complement.
The exact graph has 517 distinct points, |L|=375, |S|=142, and all 2555
unit edges: 1920 in L, 605 in S and 30 cross-edges.
[manifest.json](manifest.json) pins the input coordinates, earlier
colourings and reused source. The latest input commit is
`6dcd0080ce1004ab86d743ce9498a9a065e0ccd9`.

Every witness colours G minus a nonempty set D. Hence every
non-four-colourable subgraph must intersect D. The initial 922 positive
rows comprise 526 full-pilot, 202 small134, 86 large2 and 108 large3 rows.
Their inclusion antichain has 584 rows. Singleton witnesses force 467
individual vertices, comprising 340 large and 127 small vertices.
All these positive colourings are checked directly.

## Finite proof

Enumerate all binomial(15,5)=3003 five-subsets O of the initially
nonforced small vertices. Exactly 94 contain no pure-small cut. Every
other five-small deletion already inherits a four-colouring.

For each surviving O, inspect all inherited cuts whose small part is
contained in O. Their large parts have sizes one, two or three. A
singleton part forbids omission of its vertex. A larger part forbids
every large omission quadruple containing that part. This complete
reduction leaves **31695 large quadruples**, summed over the 94 cases.
They are merely not yet covered by the inherited witnesses, not known
non-four-colourable graphs. No symmetry or sampling is used.

The new [certificate.json](certificate.json), 18610 bytes, supplies 33
full 517-character colour strings over `.0123`, with dots exactly at the
increasing omission list D. `native_index` records the zero-based position
in the original run; it is provenance, not a required external input.
The new rows are 23 singletons, five pairs, four triples and one four-set.

For **every** surviving quadruple A, the checker finds a new D contained
in O union A. The proper colouring of G minus D restricts to that candidate.
Together with the cases covered initially, this proves all four-large/
five-small deletions. Enlarging a smaller blockwise selection to 371+137
vertices, and then restricting its colouring, proves the subgraph claim.

For the target-order corollary, the prior three-large theorem colours
every at-most-508 subgraph having at most 136 small vertices. If such a
graph has exactly 137 small vertices, it has at most 371 large vertices
and the new theorem applies. Thus any remaining non-four-colourable
target has at least 138 small vertices and at most 370 large vertices.
This corollary invokes the published prerequisite; the new checker does
not rerun that completed family proof. The prerequisite's public
solver-free checker remains available in its linked directory.

There is also an unconditional consequence of the positive witnesses:
**490 vertices are mandatory in every non-four-colourable subgraph of G**,
comprising 362 large and 128 small vertices. Each is certified by a proper
colouring of G minus that single vertex. The new checker verifies these
counts and lists the other 27 vertices. This is not itself a closure of
all at-most-508 subgraphs.

## Frozen bounded discovery

The [plan](plan.json) allowed at most 256 full-graph queries, each with
100000 conflicts and 4 GiB address space. The producer cycles through
lexicographic small omission sets and takes the least uncovered large
quadruple per case. Every queried graph has exactly 371+137=508 vertices.

The full H517 activation formula has 2585 variables and 10738 clauses:
four colour variables and one activation per vertex, guarded at-least-one
clauses, four inequalities per unit edge and an origin-colour normalization
guarded by the origin's activation. All activations are specified on every
call. Inactive vertices may have all colour variables false. Adjacent
true-colour sets are disjoint, so choosing one true colour per active
vertex is sound without at-most-one clauses. The full graph oracle imposes
no completeness assumption about intact-L boundary profiles after L deletions.

Each returned colouring is checked on the entire candidate, greedily
extended over omitted L and then omitted S vertices, and checked again.
Only candidates whose omitted vertices contain the resulting D are removed.

The family closed after **45 queries, all SAT**, touching 38 of the 94
small cases. Other cases were covered by witnesses obtained elsewhere.
There was no UNKNOWN or negative target, and no bound was extended.
The run took 5.1773 seconds with peak RSS 39552 KiB. The 33 retained
public rows subsume all 45 native witnesses. The original witnesses,
formulas, transcript and logs remain local. [run_summary.json](run_summary.json)
records the outcome.

The producer includes the frozen negative-target procedure: fresh bounded
Kissat proof, independent DRAT and exact CNF checks, and a checked
five-colouring. That branch was not exercised. No negative solver answer
or proof trace is a premise of the new theorem.

## Reproduction and verification

From this directory in a complete repository checkout:

```bash
python3 -B verify.py --report /scratch/heule517-large4-check.json
sha256sum -c SHA256SUMS
```

Python 3.11.2 and the standard library suffice. Expected fields include
`five_sets_checked=3003`, `large_quadruples_checked=31695`,
`remaining_quadruples=0`, `final_global_forced=490` and
`negative_solver_proof_required=false`. The corollary fields explicitly
record their dependence on the prior large3 theorem.

[verify.py](verify.py) imports the hash-pinned independent monomial
geometry routine, not the producer or a SAT solver. It reconstructs all
133386 pair distances, checks the 922 inherited witnesses (2342639 edge
inequalities), checks the 33 new witnesses (83854 inequalities), and
exhausts the five-small omissions and remaining large quadruples.

The author also ran `--work /path/to/native-run`, which checked all 45
native witnesses (114122 inequalities), public subset and subsumption,
the full round-robin candidate sequence, all removal counts and the
actual activated CNF entry by entry. This audit took 6.2574 seconds,
including 0.1738 seconds for the coupled cover; see
[verification.json](verification.json). The checker is independently
implemented and author-run. No separate-author review or formalization
is claimed. Exact coordinates, Python integer arithmetic, positive
colouring decoding and complete finite enumeration are the new proof's
trust boundary. No floating-point or negative solver trust is required.

To reproduce discovery, use python-sat 1.8.dev24 / CaDiCaL 1.9.5:

```bash
python3 -B run.py --work /scratch/heule517-large4-fresh \
  --kissat /path/to/kissat --drat /path/to/drat-trim
```

Kissat 4.0.4 and drat-trim would be used only for a negative target.
The actual activated formula SHA256 is
`21fcfe71a6162a4ac3577456d50e607479dd2358001991e814e49aa95ff29a9f`.

## Next boundary and shared evidence

This family is closed. The accumulated 490 mandatory vertices leave
only 27 possible omission vertices. A next, separately frozen decision
can test the **whole at-most-508 support** by considering all
binomial(27,9)=4686825 nine-omission sets against the published positive
cuts. An uncovered set would be a remaining candidate, not a proof of
non-four-colourability. That whole-support enumeration, any further
deletion level and all new native queries are unstarted here. No job or
unfinished proof remains.

HN-3's fixed-baseline extension for 252 coupled heptagon sums was inspected
at commit `0d969bf958f978d156e81fee807e70c6cc51d878`, Discovery Net height
3140. It includes all exclusive cross-edges but does not prove simultaneous
extension to several attached components. The accepted independent review
of the prior single-sum rotation closure was also inspected at commit
`274d3df31b172e63f2b766e3c6d352a4a80e3211`, height 3144. Neither result
supplies a premise here; that geometric lane remains separate.
