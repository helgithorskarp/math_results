# Proof of the optional-P4 elimination

## 1. List obstruction theorem

Let P have vertices 0,1,2,3 in path order, let T be any selected subset,
and let L_i be any subset of a three-element colour palette. The induced
selected path has a proper list colouring if and only if none of the
37 interval obstructions in the README is present. An obstruction is
present when its whole interval is selected and L_i is contained in its
specified maximal forbidden list M_i at every interval vertex.

Each obstruction is uncolourable. The length-one list is empty. For a
longer interval its first singleton forces colour a. The next pair {a,b}
forces b, and any next pair {b,c} forces c. Its terminal singleton is the
same as the colour just forced at its predecessor, so the last edge fails.
Shrinking lists cannot restore a colouring.

For completeness, consider a selected connected component that is not
list colourable. Let R_i be the set of colours reachable at position i
in proper colourings of its prefix. At the first position R_i=L_i.
At every subsequent position,

`R_i = { c in L_i : some d in R_(i-1) satisfies c != d }`.

Take the first empty R_j. If L_j is empty, there is a one-vertex
obstruction. Otherwise R_(j-1) and L_j must be the same singleton.
Trace backwards from this singleton reachable set. Whenever a singleton
reachable set {b} comes from a list that is not a singleton, the previous
reachable set must be a singleton {a}, a≠b, and the current list must be
exactly {a,b}. Indeed, two or more preceding reachable colours would allow
every current list colour. This trace must end at a singleton list, since
the first reachable set is the first list. The resulting interval has
singleton endpoints and the forced two-element lists in between. It is
one of the listed obstructions. Components have length at most four.
This proves both directions for all lists and selections.

There are four singleton intervals. An interval of length k≥2 has
3·2^(k−2) choices of forcing sequence: its first colour is arbitrary,
and each succeeding colour differs from its predecessor. There are
5−k positions. Hence the counts are 4,9,12,12, totalling 37.

Writing selection as s_i and list membership as a_ic, the absence of one
obstruction is precisely its stated clause. This proves the CNF theorem.
The complete finite audit independently verifies the equivalence for all
65,536 input states without using the recurrence above. In the favourable
coordinates (not s_i, a_ic), each recorded maximal bad state falsifies
exactly one clause; changing any of its clause coordinates from false to
true gives a proper colouring. Thus no clause is redundant and no literal
can be removed from any clause while preserving an implicate of the
extension relation. Every one of the 37 clauses is prime. The audit checks
all 37 bad states and all 286 one-literal changes by direct assignments.

## 2. The exact H514 bridge

The coordinate reconstruction and complete pair check establish the
following decomposition, including all geometric unit edges. The old
vertices induce H510. The four new vertices induce P4. Their complete
old-neighbour sets are {0} union N_i, where the four N_i are exactly the
rows in the README. Their union B has sixteen vertices.

For each v in B, the explicit certificate colours H514−v with four
colours. Therefore every subgraph of H514 missing v is four-colourable,
including graphs with additional edges deleted. Every non-four-colourable
subgraph must retain B.

Fix a vertex set U containing B. Let H be the induced old subgraph on
U intersect {0,...,509}, and T the indices of the new vertices in U.
Take any proper colouring f of H. Relabel its palette so f(0)=0.
The new vertices must avoid 0 because they are adjacent to the origin.
For each i, their other old constraints remove exactly the colours
occurring on N_i, all of whose vertices are retained. Hence the permissible
list is

`L_i(f) = {1,2,3} minus { f(v) : v in N_i }`.

The remaining constraints are exactly the edges of P4[T]. Consequently,

`H514[U] is four-colourable`

if and only if

`there exists a proper old colouring f, f(0)=0, for which K(T,L(f)) holds`,

where K is the 37-clause relation. This is a pointwise equivalence for
EVERY old colouring, before taking the existential quantifier. It uses
no completeness restriction on intact-large-block boundary profiles.
It holds for every U containing B, of which there are 2^498. Supports
missing B are already coloured by the singleton certificates.

For target-order search it suffices to use induced graphs: a colouring
of the induced graph restricts to any graph with fewer edges. The parent
result further reduces existence of a non-four-colourable induced graph
of order at most 508 to its specified 258,914 six-omission residuals.
Every such residual retains B. Substituting K into each residual therefore
preserves the complete family decision, for every omission composition.
This does not assert that any residual is colourable or uncolourable.

## 3. Equivalence of the compiled formula

For a fixed omitted set disjoint from B, let x_vc, c=0,1,2,3, be Boolean
colour indicators for old vertices. The compiler includes an at-least-one
clause at each selected old vertex, and for every retained old edge uv the
four clauses `not x_uc or not x_vc`. It also sets x_00 true. Indicators of
omitted old vertices are unused. Four indicators are reserved per old
index even if that vertex is omitted.

For each i and c=1,2,3 introduce a_ic, with the exact definition

`a_ic iff AND(v in N_i) not x_vc`.

Its clauses are `not a_ic or not x_vc` for each v in N_i, and
`a_ic or OR(v in N_i) x_vc`. They give 3·(15+4)=57 clauses.
The compiler substitutes the fixed path-selection values in K. An omitted
vertex makes any clause containing its negative selection literal true;
otherwise that selection literal is removed. The result has 2,052 declared
variables, consisting of 2,040 old indicators and twelve availability bits.

A proper full colouring, normalized at 0 and encoded one-hot on the old
vertices, satisfies the old clauses. Its actual lists satisfy K by the
list theorem. Setting availability to its exact definition gives a
satisfying projected model.

Conversely, take any projected model. At each selected old vertex choose
one of its true colour indicators; at vertex 0 choose colour 0. Edge
clauses guarantee the chosen old colouring is proper. Availability true
in the model means no neighbour has that true colour indicator, so it is
also absent from the chosen neighbour colours. Thus the model's available
lists are subsets of the actual lists of the extracted old colouring.
By K and the list theorem, the selected path can be coloured from the
model's lists. These colours also lie in the actual lists and avoid 0,
so they give a proper full colouring. This explains why at-most-one
constraints are unnecessary and why extra true indicators cause no
soundness gap. The dynamic program explicitly reconstructs the path.

The formula is therefore satisfiable if and only if the specified induced
H514 graph is four-colourable. Compilation alone does not decide this
existential statement. To certify non-four-colourability later, a solver
would still need an independently checked UNSAT proof for the actual
compiled instance, together with this reduction. No such query or proof
is claimed here.
