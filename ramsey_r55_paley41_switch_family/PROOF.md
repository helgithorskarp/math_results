# Paley(41) switching-class obstruction

## Statement and scope

Let P be the graph on Z/41Z with red indicator P_uv=1 if u-v is a
nonzero square modulo 41, and blue otherwise. For any s in {0,1}^41 let
G_s have red indicators P_uv XOR s_u XOR s_v.

**Computer-assisted theorem.** Every G_s contains a red K5 or a blue K5.

**Global 43-vertex corollary.** No Ramsey(5,5) graph on 43 vertices contains
an induced 41-vertex subgraph switching-equivalent to P, including after
arbitrary relabeling. In particular, the complete labeled family consisting
of all G_s plus two vertices with arbitrary incident edges is excluded.
There are exactly 2^123 distinct labeled graphs in this family.

This is a whole-family exclusion, not a statement about arbitrary 43-vertex
graphs. It gives no improved Ramsey bound, no catalog completeness claim,
and no restriction to automorphism-preserving switches. No priority claim
is made. Paley graphs and Seidel switching are classical; see Brouwer and
Van Maldeghem, *Strongly regular graphs*, sections 1.1.9 and 1.1.11:
https://homepages.cwi.nl/~aeb/math/srg/rk3/srgw.pdf .

## Normalization and the complete family

Replacing every s_v by 1-s_v leaves every core edge unchanged. Thus one
may set s_0=0 without losing a graph. Conversely, equality of two normalized
core colorings forces equality of s_v for every v: compare edge {0,v}.
Consequently the normalized switching class has 2^40 distinct labeled
graphs. The two added vertices have 2*41+1=83 independently free edges;
their choices are distinct and do not affect the core. This proves the
2^123 family count and its complete coverage, without an isomorphism
quotient or symmetry hypothesis on the resulting graph.

## Physical clauses and the compact certificate

Variable v, for 1 <= v <= 40, denotes s_v. A signed clause C is false
precisely when s_v=0 for each positive literal v and s_v=1 for each
negative literal -v. Every input clause in `obstruction.dimacs` has width
4 or 5 and has distinct variables. For a width-4 clause adjoin physical
vertex 0 with s_0=0; for a width-5 clause use its five variable labels.

`check_certificate.py` evaluates all ten physical edge colors on these
five vertices directly, using Euler's criterion to define P. Each of the
1,184 clauses excludes one actual monochromatic K5 switch pattern.
There are 423 width-4 and 761 width-5 clauses; 542 prohibit a blue K5 and
642 prohibit a red K5. Only variables 1,...,40 occur in the input clauses.
Thus every hypothetical Ramsey graph in the switching class must satisfy
all these clauses. Completeness of this selected clause set is **not**
required: they are necessary conditions, and their conjunction is UNSAT.

The compact ASCII certificate has 501 additions and 1,669 deletions.
The standalone checker verifies every addition in forward order:

1. A clause C is RUP if repeated unit propagation on F together with the
   negation of every literal of C reaches an empty clause.
2. Otherwise, the first literal p of C is its proposed RAT pivot. For
   every clause D in F containing -p, the checker requires that
   C union (D minus {-p}) is RUP with respect to F.
3. Deleting one copy of a clause weakens F and therefore preserves
   satisfiability. The checker maintains clause multiplicities. Deleting
   an absent clause is harmless, although none occurs in this certificate.
4. The final empty clause must itself pass RUP. No subsequent line is
   accepted.

RUP implies logical consequence by the soundness of unit propagation.
RAT preserves satisfiability: take a model of F that falsifies C. Flip
the variable of p to make p true. A clause that could become false must
have contained -p and have all its other literals false before the flip.
But then C union (D minus {-p}) would have been false in the original
model, contradicting its RUP implication from F. Hence the modified
assignment satisfies F and C. This also permits newly introduced proof
variables. Induction through all proof steps shows that a satisfying
assignment to the input would give one to the final formula containing
the empty clause, a contradiction.

The checked trace uses 284 RUP additions and 217 RAT additions, with 135
explicit RAT-side clause checks (fresh pivots can have no opposite-pivot
clause to check). These counts are not claimed minimal.
The certificate directly proves the switching-class theorem. Every
43-vertex family member contains such a core, proving the corollary
regardless of the 83 added-edge choices. Relabeling preserves the K5
property, so the induced-subgraph formulation follows as well.

## Full-family formula used to discover the certificate

The search used 123 variables: the 40 switch variables, followed by
83 physical added-edge variables in lexicographic pair order. No degree,
automorphism, fixed-neighborhood, or imported feasibility assumptions are
present. Every five-set has k=3,4,5 core vertices.

For a core subset T with anchor a, a monochromatic color c forces
s_v XOR s_a = P_av XOR c for every other v in T. Set s_a=0 and compute
this unique candidate; test all core edges. If it succeeds, the candidate
and its bitwise complement are exactly the two switch patterns giving
color c. If it fails, no such pattern exists. Equivalently, every core
triangle must have edge-parity c; the anchored test is sufficient because
it directly tests every pair.

For each surviving pattern and each choice of added vertices completing
the five-set, append the condition that all its added edges have color c.
Negating this conjunction gives the forbidden-event clause. Impossible
events requiring s_0=1 are skipped; the s_0=0 literal is otherwise removed.
This is an exact formula for the full family, not merely necessary local
conditions. It has 137,950 distinct clauses.

The independent full-formula auditor imports no producer code. It enumerates
all switch assignments on **every** 3-, 4-, and 5-vertex base graph (33,856
truth cases), then looks up each of the 962,598 physical five-sets and
reconstructs its forbidden events. It compares the complete clause sets,
not just counts. The producer uses a square-residue set; both direct
auditors independently use modular exponentiation.

Kissat's single bounded invocation returned UNSAT. DRAT-trim verified and
extracted the compact core/trace; that pair also passed DRAT-trim directly.
The final standalone physical/DRAT checker is independent of Kissat,
DRAT-trim, the full generator, and the full-formula auditor. It needs only
the two compact committed certificate files and Python's standard library.

## Trust boundary

This is exact finite, computer-assisted evidence, not a formal proof-assistant
theorem or an independently reviewed result. Trust remains in the written
reduction, the direct physical and DRAT checking implementation, Python,
and its execution platform. The standalone certificate removes any need
to trust the solver's verdict, proof extraction, or full-formula coverage
for the stated exclusion. The extra full-formula reconstruction and small
truth-table/negative controls are validation evidence, not external review.
The historical H92/H93 gluing route is parked and is not a dependency.
