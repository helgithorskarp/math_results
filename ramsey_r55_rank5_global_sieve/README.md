# Four-set distinguishers and an exact global rank-five sieve

Every four vertices of a hypothetical 43-vertex graph with neither a clique
nor an independent set of order five have at least **17 outside vertices
with nonuniform contacts** to them. Consequently, across any 20+23 cut,
an identical-row class on the 20-side has size at most **three**.

We convert this equality obstruction and established uniform/zero-class
constraints into an exact reduction of a complete global 43-vertex family:
the red 20-by-23 cross matrix has binary rank five, its blue complement has
rank at least five, and all **443 internal pairs are arbitrary**. Every
label support and multiplicity pattern is included. No symmetry, fixed
neighborhood, parent graph or graph catalog is prescribed.

| distinct cross matrices | exact count |
|---|---:|
| defined baseline | 5265776463769286448156565145344760253473964876758764876800 |
| removed by the full sieve | 2066365377174402749659084812993090655368806390234845516800 |
| remaining after this sieve | 3199411086594883698497480332351669598105158486523919360000 |

The exact removed fraction is

    72250993667250533318774539803589602314409997
    / 184119220220965173622650664548131290651799397

or **39.241418457313%**. Multiply each count by 2^443 for full labeled
graphs on this one fixed partition. This is not a fraction of actual good
graphs, a union over partitions, an isomorphism count, or a runtime estimate.

This branch has neither color of cut rank four, so it is disjoint from the
previous rank-four families on this partition. The older predicates are
credited as established results, now counted in this new branch. The new
four-set obstruction alone removes **9.083120138796%** after those predicates,
with its changing complementary-rank overlap accounted for exactly. The
stronger row cap also applies to the teammate's rank-four survivor interface;
no new percentage for that contact-filtered family is asserted here.

This meets an all-pattern reduction gate. It does not exclude the entire
baseline or construct a good43. A good43 need not have a rank-five cut.
No improvement to R(5,5) and no historical priority are claimed.

## Reproduce

Python 3.11.2, standard library, exact integers, one process:

    python3 -B reproduce.py
    python3 -B -O reproduce.py
    python3 -B counts.py
    python3 -B model.py fixture_parameters.json
    python3 -B extract.py fixture_parameters.json
    python3 -B verify.py fixture_graph.json fixture_certificate.json

The full replay returns `VERIFIED_RANK5_GLOBAL_SIEVE`, a deterministic audit
SHA-256, and the exact removed/remaining counts. It recomputes the theorem
audit and both counting methods, rather than trusting a saved verdict.
The deliberately rejected fixture demonstrates the new quadruple branch;
it is not a Ramsey candidate.

See [PROOF.md](PROOF.md) for the global equality argument and complete
counting derivation, [VALIDATION.md](VALIDATION.md) for checks and trust
boundaries, and [provenance.json](provenance.json) for antecedent source
hashes. No solver, private proof file, external input or network is needed.
