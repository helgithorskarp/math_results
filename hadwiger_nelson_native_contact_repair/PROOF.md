# Construction, certification and search logic

## Exact physical objects

The source table gives 159 distinct Cartesian points at denominator12.
Its oriented unit displacements define D, so the addition rule uses only
actual unit vectors. All additions remain in E. Multiplication by
rho=(7+i sqrt15)/8 preserves norm because (49+15)/64=1.
Repeated coordinates are merged before graph construction.

Every resulting point has the form

```
x=(a+b sqrt5+c sqrt33+d sqrt165)/96,
y=(e sqrt3+f sqrt15+g sqrt11+h sqrt55)/96.
```

The real field Q(sqrt3,sqrt5,sqrt11) has degree8: the three independent
prime square classes give its usual multiquadratic basis. Consequently
coefficient equality is physical equality in the displayed embedding.
Expanding `(x1-x2)^2+(y1-y2)^2` and requiring the resulting coefficient
vector to be `(1,0,...,0)` is an exact unit-distance decision.

`build.py` constructs the seed enlargement in four native integer
coefficients, rotates it by explicit coefficient formulas, and uses four
expanded norm equations. `radical_check.py` instead parses the original
sixteen Cartesian coefficients, multiplies radical monomials by bit masks,
and constructs the rotation by multiplication by sqrt15. It derives the
quadratic norm forms from this monomial algebra rather than importing the
expanded equations. The two constructions and all ordered edge entries were
compared exactly for the radius-2 host. The independent implementation also
checks every physical pair in the larger host.

The radius cutoff uses the sign of an integer expression a+b sqrt33; its
sign is decided by signs and, when required, comparing a^2 with33b^2.
No floating-point test enters either published host or its graph. The
radius-2 host is a subset of the unrestricted host, and its strict edges
are the induced unit edges there.

## Five-colour certificate

The selected point IDs define an induced graph. Its four-colour CNF has
one Boolean variable X(v,c) per point and colour c in{0,1,2,3}. Each vertex
has an at-least-one clause and the six at-most-one clauses. Every unit edge
uv has clauses `not X(u,c) or not X(v,c)` for all four colours. A genuine
unit triangle is pinned to three distinct colours. Every proper colouring
can be renamed to satisfy these pins, so this is a sound symmetry reduction.
Thus the CNF is satisfiable if and only if the actual selected graph is
four-colourable.

The independent geometry implementation emits the exact CNF. Kissat's
UNSAT refutation is checked by DRAT-trim. It follows that the selected graph
needs at least five colours. Restricting the supplied radius-2 host word
gives a proper five-colouring of the selected graph; every induced unit
edge is checked. Hence its chromatic number is exactly five. The two host
graphs contain this graph and have separately checked proper five-colour
words, proving the same chromatic number for them.

The five-colour words were discovered by colouring the two field components
and recolouring an independent cover of 29 monochromatic cross edges to a
fifth colour. A separate unrestricted five-colour SAT run also produced a
proper word for the radius-2 host. The finite certification depends on the
published words and direct edge checks, not on a field-colouring theorem or
on the SAT solver's correctness for a positive verdict.

The trust boundary consists of the exact source coordinate transcription,
ordinary integer arithmetic and program execution, the written CNF
correspondence, and the DRAT checker. This is not a proof-assistant
formalisation. A supplied hash identifies the observed proof; a hash alone
is not a refutation. `reproduce.py` generates and checks a fresh one.

## Positive construction controls

For a fixed base B in a host, let P be B together with every host point
having at least two unit neighbours in B. All pair distances of the host
are reconstructed before P is selected. A directly checked proper
four-colouring of P colours every subgraph of P by restriction. This proves
only the stated 1,587-point pool result for its 482-point base.

The separate displayed-coordinate comparison with the original Parts input
identifies a 503-point base in the larger host. The included 507-point
control is checked on its actual complete unit-edge graph. Its positive
word establishes four-colourability of this candidate, without an UNSAT
claim about other candidates.

## Logic of the unresolved repair search

Fix the 503-point base B and the finite host H. A successful repair is a set
T in H minus B with |T|<=5 and chi(B union T)>4.

If a repair exists, choose an inclusion-minimal such T. Every new vertex
v in T has at least four neighbours in B union T. Otherwise a four-colouring
of B union(T minus{v}), supplied by minimality, extends to v using an unused
colour. It is therefore sound for an existence search to impose these
minimum-degree conditions on selected new vertices. No minimum-degree
condition is imposed on the fixed base vertices: some of those may be
redundant.

Suppose C is any subset of H containing B with a verified four-colouring.
Every successful repair T must meet H minus C; otherwise B union T is a
subgraph of C and inherits its colouring. This gives the hitting clause
`OR(x_v : v in (H minus C))`, where x_v means that the new point is selected.
The saved extension witnesses supply C by beginning with a checked colouring
of a candidate and greedily assigning colours to further physical points.
The complete resulting colouring is checked on all retained unit edges.

The master search imposes the cardinality bound, the necessary degree
conditions, and these hitting clauses. Its satisfying assignments are only
candidates and must be tested on the full physical graph. Its UNSAT answer
could prove nonexistence in this fixed finite repair family only after its
refutation, every witness, and the guarded cardinality encoding were
validated. The current package asserts no such completed master proof.

The optional code uses python-sat's sequential-counter encodings. At-least
constraints for a vertex's selected neighbours are guarded by the negation
of that vertex's selection variable. Guarded auxiliary clauses can be
satisfied independently when the vertex is absent. When it is present they
encode precisely the required number of selected neighbours. A native
master timeout or a candidate's conflict limit is UNKNOWN, not evidence for
either a positive or a negative mathematical conclusion.

For the native-cardinality variant, put d=|N(v) minus B| and
r=4-|N(v) intersect B|>0. The guarded condition is equivalent to

    sum(1-x_u : u in N(v) minus B) + r*x_v <= d.

When x_v=0 this is automatic; when x_v=1 it requires at least r selected
neighbours. The implementation uses r distinct clones, each equivalent to
x_v, instead of passing duplicate literals to a native cardinality constraint.
Its master UNSAT status still requires separate proof validation before a
mathematical exclusion is claimed.
