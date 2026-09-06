# A complete 20-pattern joint interface for the H517 family

**The 375-point large block has exactly 20 boundary colourings up to global
colour permutation.** Its 19 boundary vertices admit exactly 120 patterns
when the origin has colour zero. Twenty full colourings prove existence;
a checked DRAT exhaustion proof proves completeness.

Together with an exact separator, this reduces four-colourability of every
graph formed by the full large block and an arbitrary subset of the
142-point small block to **20 explicit small-block SAT instances**. In
particular, selecting at most 133 small vertices gives a graph on at most
508 vertices. No such selection was searched or established to be
five-chromatic here. The full H517 family remains open.

This is the changed joint mechanism proposed after the
[339-cost assessment](../hadwiger_nelson_heule517_cut_cost/README.md), source
`97a3f9e6c24d10c77d096f3001aa64f81e8a08a4`. The old 517-vertex
decision-master refinement loop remains parked. The new native work was
only the bounded projection of the large block, which completed in 21
calls. No full H517 selection or small-block colouring query ran.

## Exact support and separator

The input is the [verified H517 support](../hadwiger_nelson_heule517_family_pilot/README.md),
source `59d634e906f6c6ed5945c0180b5352ba03c3babd`: the identity-aligned
Heule H510 plus the seven degree-at-least-seven centres outside U553 and
A1111 in the complete earlier census. Their centre indices are
327,439,671,1040,1074,1377,1383. The coefficient basis is

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165),
```

with positive roots and common denominator 96. G indices 0..509 are the
increasing union-certificate labels marked `510`; 510..516 are the seven
centres in the listed order. They are not original Heule or Parts labels.
The coordinate inputs and producer dependencies are hash-pinned in
[manifest.json](manifest.json).

Let L be the points with zero coefficients of sqrt(5), sqrt(15), sqrt(55)
and sqrt(165) in both coordinates; let S be the complementary points of
G. Direct reconstruction of the complete unit graph gives:

| Quantity | Exact count |
|---|---:|
| L vertices / edges | 375 / 1920 |
| S vertices / edges | 142 / 605 |
| Edges between L and S | 30 |
| Large boundary I / small terminals J | 19 / 30 |
| Complete G vertices / edges | 517 / 2555 |

The original 135 small vertices have 554 internal edges. The seven new
points A={510,...,516} form an independent set, and all their 51 edges
end in those original small vertices. **There is no new edge to L.**
Their joint neighbourhood B has 48 vertices and 67 induced edges. Thus
the direct extension condition for a fixed colouring c of selected old
vertices is that every selected a in A has a colour absent from its
selected neighbourhood. Since A is independent, these seven choices
then extend simultaneously. Separate base colourings satisfying the
seven individual conditions would not suffice.

The complete large boundary, in the order used by every pattern, is

```
I = [0,333,334,335,336,337,338,339,340,341,342,343,344,
     466,467,468,469,470,471].
```

[separator.json](separator.json) gives every L and S vertex, the 30
cross-edges, all 1920 large edges and the 30 small terminals. The verifier
checks every entry against a new exact scan of all 133386 unordered
pairs. The two blocks interact only through I and J by definition of
the complete edge list; this is not an assumption about geometric sides.

## Complete boundary relation

For each proper four-colouring c of L, restrict c to I and identify rows
under a global permutation of the four colours. The representative is
the restricted-growth string obtained by assigning labels 0,1,2,3 in
order of first appearance along I. Its first entry is zero. The exact
set R of representatives has size 20.

[certificate.json](certificate.json) gives one 375-character proper
colouring of L for each 19-character row of R. Full colourings follow
the increasing L vertex order in the separator. Every row uses all four
colours on I, so its orbit under the six permutations fixing zero has
size six. These disjoint orbits give all 120 origin-fixed patterns.
No spatial symmetry or earlier Parts interface list is imported.

The projection CNF uses variables q(v,c)=4*position(v)+c+1 for each
v in L and c in {0,1,2,3}. Each vertex gets an at-least-one clause;
each edge forbids its endpoints sharing each colour. The origin gets
q(0,0). There are 1500 variables and 8056 base clauses. At-most-one
clauses are unnecessary: the true colour sets on adjacent vertices are
disjoint, so choosing one true colour at each vertex yields a proper
colouring. Conversely every ordinary colouring gives a one-hot model.
Fixing origin colour zero loses no colouring modulo global permutation.

After a projected row is found, exclude each distinct permutation fixing
zero with a clause containing the 19 negated corresponding q variables.
The final formula has 8176 clauses: the base plus all 120 orbit blockers.
A new ordinary boundary pattern would yield a one-hot satisfying model
of this formula. Its independently checked UNSAT proof therefore proves
that the list is complete. The positive witnesses prove that no listed
row was merely a spurious SAT encoding state.

The fixed final DIMACS SHA256 is
`826368926921bc5d19ad5e3afe16317bc0d3d81266cf2ecab3717ff2c0dde3ff`.
The recorded binary DRAT proof is 2895824 bytes, SHA256
`c81c3a4f6d4877267171e7381775c25c8319ed41748787d78c945f9f2fad237f`.
It stays local and is regenerated from the compact public source.

## Uniform reduction for every selected small block

Fix any T subset S, with **all of L retained**. For r in R, define F(T,r)
by four colour variables per vertex of T, at-least-one clauses, the four
inequality clauses for every induced T edge, and a unit clause forbidding
colour r(i) at s whenever (i,s) is a cross-edge with s in T.

Then

```
G[L union T] is four-colourable
    iff F(T,r) is SAT for at least one r in R.
```

For the forward direction, normalize a full colouring globally so its
restriction to I is the representative r in R. Its small-block colouring
satisfies F(T,r). For the reverse direction, choose the supplied full
L-colouring witnessing r and combine it with the decoded small-block
colouring. The internal edge clauses and cross-edge unit clauses check
every edge of their union. Both parts use the same boundary row and the
same colour labels. This proves the equivalence for all 2^142 subsets T,
without enumerating any of those subsets.

Consequently a non-four-colourable graph in this fixed-L family on at
most 508 vertices exists exactly when some T of size at most 133 makes
all 20 F(T,r) unsatisfiable. One may enlarge T to size exactly 133 without
losing non-four-colourability. This is a reduced search problem, not its
solution. It does not cover deletion of vertices from L: those deletions
can introduce additional boundary patterns outside R.

`emit_cases.py --vertices-json /path/to/T.json --out /scratch/new-cases`
constructs all 20 DIMACS instances for any supplied increasing list T of
G indices in S. It performs no solver calls. No production T instance or
small-block selection phase has been started in this package.

## Reproduction and validation

Use Python 3.11.2. The geometric verifier and fixed-instance generator
need only the standard library. Recreate and verify the complete
certificate from this directory, choosing a fresh external directory:

```bash
python3 -B write_exhaustion.py --out /scratch/heule517-interface-proof
/path/to/kissat --seed=0 --conflicts=1000000 --time=180 /scratch/heule517-interface-proof/exhaustion.cnf /scratch/heule517-interface-proof/exhaustion.drat
python3 -B verify.py --work /scratch/heule517-interface-proof --drat /path/to/drat-trim --report /scratch/heule517-interface-check.json
sha256sum -c SHA256SUMS
```

Kissat should return exit code 20 for UNSAT. The verifier reconstructs
the exact graph independently, checks the complete separator, all 38400
positive witness edge inequalities, every orbit and the actual native
base and exhaustion CNFs entrywise. It then invokes drat-trim on that
audited formula. The successful report has `large_relation_complete=true`
and `proof.verified=true`. Without the proof inputs, `verify.py` checks
geometry, positive witnesses and the CNF but explicitly reports
`large_relation_complete=false`.

The producer uses the previous H517 exact engine; the verifier imports
neither it nor any earlier field arithmetic. Instead it parses the
coordinate tables and multiplies monomials by explicit exponent
expansion. Discovery used CaDiCaL 1.9.5 through python-sat 1.8.dev24;
proof generation used Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim binary SHA256
`bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021`.
No floating-point mathematics is used. This is an author-run independent
checker, not a separate-author review or formal proof-assistant result.

The [frozen plan](plan.json) allowed at most 128 projection calls, each
with 200000 conflicts and 4 GiB address space. Enumeration completed
after 20 SAT answers and one UNSAT answer. The whole run took 6.7640
seconds, including proof generation (1.7866 seconds) and its first DRAT
check (1.4584 seconds), with peak RSS 53420 KiB. The independent geometry,
formula and proof replay took 6.5794 seconds. The 2.9 MB proof and native
logs remain external. No bound was extended and no proof is pending.

For optional fresh discovery, run `run.py --work /scratch/fresh-interface
--kissat /path/to/kissat --drat /path/to/drat-trim` in the PySAT environment.
Fresh native witnesses may differ. The fixed public proof regeneration
above is the authoritative reproduction path and avoids rediscovering
models. `controls.py`, in that same PySAT environment, compares exhaustive
ordinary colourings on three tiny fixtures with orbit exclusion, checks
64 small-side boundary/selection combinations including empty T, and
checks the obstruction of one vertex adjacent to four distinct colours.
No production query was repeated for those controls.

## Handoff

This complete interface relation is a materially changed finite boundary.
The next proposed milestone is one separately frozen selector pilot on
the 142 small vertices, with L375 fixed and the size bound 133, using the
20 exact boundary cases. Any positive case must decode to a checked
full union colouring; any proposed target must have all 20 negative
cases certified, exact full coordinates and an independently checked
five-colour upper witness. That pilot has not started. The unrestricted
H517 decision-master loop, closed older supports and HN-3 geometry remain
parked or separate as previously coordinated.

HN-3's [complete collision-orientation closure](../hadwiger_nelson_heptagon_moser_sum/COLLISIONS.md),
source `4ec850c8ba08f8beea0a811c49e3b526aa123e38`, Discovery Net height
3066, was inspected. Its heptagon-spindle family remains open at
injective sums with unequal-length extra-edge events. It supplies no
premise here. No <=508 five-chromatic graph was established in this pass.
