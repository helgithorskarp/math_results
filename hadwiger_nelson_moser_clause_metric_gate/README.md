This package rejects a finite attempt to glue certified Moser11 forcing
interfaces. Its 62 clauses on seven terminal roles exclude every four-colour
assignment and have a conditional budget of **441 labels**, but their exact
metric requirements are inconsistent in the plane. No plane graph or record
candidate is supplied.

The imported [eleven-point source](../hadwiger_nelson_moser_four_terminal_relation/README.md)
has four independent terminals A,B,C,D and the complete four-colour relation

```text
colour(A) != colour(B) OR colour(C) != colour(D).
```

Both marked pairs AB and CD have distance sqrt(7). The source has an
[independent acceptance](../hadwiger_nelson_moser_four_terminal_relation_review1/README.md).
Source commits and file hashes are pinned in `provenance.json`. This package
uses that relation theorem without repeating its review.

The declared finite design

There are 105 ways to choose two disjoint unordered pairs on seven roles.
Each specifies one copy of the source, with the two pairs occupying AB and
CD. The producer greedily covers all 715 canonical four-colour partitions,
breaks ties by the fixed lexicographic clause index, and then removes
redundant selected clauses in reverse selection order. This leaves the
62-clause system in `certificate.json`.

Seven shared terminal roles and seven private interior vertices per clause
would give 7+62*7=441 abstract labels. No clause-count optimality or minimum
graph claim is made. This calculation was the initial cap check; 441 is
conditional on a realization which does not exist.

The independent checker enumerates all 4^7=16,384 named colour words directly.
Every word violates a selected clause; normalizing these words recovers all
715 canonical patterns. The five-colour terminal word `0110234` satisfies
every selected clause. This is evidence about the relation system only;
it is not a five-colouring of an actual plane support.

Exact geometric contradiction

Each selected clause requires two of its physical terminal pairs to be at
distance sqrt(7), regardless of rotations, reflections, endpoint reversals
or additional contacts. In fact all 21 terminal pairs occur. Six explicitly
cited clause occurrences already require every pair among roles 0,1,2,3 to
have squared distance 7. Role collisions cannot avoid a positive required
distance, and identifying private vertices cannot alter those six lengths.

Let the four proposed points be p0,p1,p2,p3 and set vi=pi-p0 for i=1,2,3.
Their Gram matrix must have diagonal 7 and off-diagonal 7/2, since
`2 vi dot vj = |vi|^2+|vj|^2-|vi-vj|^2`. Its determinant is

```text
(7/2)^3 * det([[2,1,1],[1,2,1],[1,1,2]]) = 343/2.
```

Three vectors in the plane have a Gram matrix of rank at most two and
therefore determinant zero. This contradiction excludes every exact
co-realization of the selected incidence system. The checker derives the
source pair lengths from the published exact coordinate rows, verifies the
six clause witnesses, and computes the determinant using rational arithmetic.
The design stops here; there was no numerical embedding or solver search.

A general limitation of this selection method

Suppose a system uses only these Moser clauses, with terminal identifications,
and its relation inconsistency is derived solely from the imported clauses.
For any proposed exact terminal placement T, form H on T with the marked
AB and CD pairs as edges. Each edge has length sqrt(7). Every proper
four-colouring of H satisfies every clause (both its inequalities are true).
Consequently an inconsistent clause system would already require H to be
non-four-colourable. Scaling T by 1/sqrt(7) would give a plane unit-distance
non-four graph on the terminal points alone.

Thus pure Moser-clause packing does not supply a new relation contradiction
before one has a non-four terminal-distance graph. This is a necessary
condition for that proof architecture, not a proof that all Moser compositions
are four-colourable. Additional unit contacts, other interfaces, relations
involving private vertices, or unequal marked distances change the premise.
No claim about a proper five-colouring of that hypothetical scaled graph is
needed or made. The selected seven-role design fails the stronger explicit
four-point metric check above.

This handoff is a construction-selection rejection, not progress on the
sub-509 record. Retire the fixed incidence design and do not enlarge a
homogeneous Moser clause cover to evade the failed metric gate. The source
relation remains valid. A successor needs a physically compatible interaction
whose contradiction does not merely assume a non-four terminal graph.

Replay with Python 3.11 and its standard library:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B produce.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The first two commands print `expected.json`; the producer reproduces the
exact selected clauses. Controls reject six damaged certificates and check
two realizable Gram matrices. `validation.json` records versions, times and
output hashes. Enumeration takes well below one second on the producing
host. No native solver, hidden input, floating predicate, or omitted large
certificate is needed. The imported relation, exact Python arithmetic,
complete loops and written planar-rank argument are the trust boundary.
Checks are author-run, without a new independent review or formalization.
