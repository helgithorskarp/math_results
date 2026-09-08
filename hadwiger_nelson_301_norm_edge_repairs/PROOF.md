# Proof of the 18-case classification

Let `G=(V,E)` be the pinned 301-vertex source graph. Let `S` be the support of
the weighted norm identity in h3993's accepted certificate. The package checks
that `|S|=18`, that every member of `S` is a source edge, and that `S` is a
subset of h3993's 690-edge necessary repair clause.

## 1. Six cases are four-colourable

For six edges `e` in `S`, `classification.json` supplies one digit in
`{0,1,2,3}` for each source label, in source-label order. The standard-library
verifier checks every edge of `E-{e}` and accepts only if its endpoints have
different digits. Hence these six graphs are four-colourable and cannot be
five-chromatic.

## 2. The other twelve cases are exactly five-chromatic

For the remaining ordered edges `e_1,...,e_12`, introduce colour variables
`x_(v,c)` and gates `g_1,...,g_12`. Each vertex receives at least one of four
colours. For a source edge `uv` outside the selected family, the CNF contains

    NOT x_(u,c) OR NOT x_(v,c)

for every colour `c`. For `e_i=uv`, it instead contains

    g_i OR NOT x_(u,c) OR NOT x_(v,c).

A standard sequential encoding requires exactly one gate to be true. If
`g_i` is true, the four constraints for `e_i` are disabled; every constraint
for every other source edge is active. Three unit clauses pin distinct colours
on the surviving triangle `(1,189,192)`.

Although the vertex clauses require only at least one colour, this encoding is
equivalent to four-colourability. A proper colouring gives a model. Conversely,
from any model choose one true colour variable at each vertex. The active edge
clauses ensure that the choices at adjacent vertices differ. The triangle pins
only remove colour permutations.

The strict checker validates a RUP-only LRAT derivation of the empty clause
from this exact CNF. Therefore none of the twelve graphs is four-colourable.
The pinned source has an explicit proper five-colouring, and deleting an edge
preserves it. Each of the twelve graphs consequently has chromatic number five.

## 3. An odd wheel forbids a noninjective unit-edge map

Suppose a hub is adjacent to every vertex of an odd closed rim walk and
successive rim vertices are adjacent. In a plane unit-edge map the rim images
lie on the unit circle about the hub. Successive points on that circle at
distance one differ in angle by `+pi/3` or `-pi/3`. An odd sum of signs cannot
be divisible by six, so the walk cannot close. The argument permits distinct
rim labels to have the same image.

For nonadjacent vertices `a,b`, identify `b` with `a` in the graph. If the
quotient contains an odd wheel, any unit-edge map must satisfy `p(a)!=p(b)`;
otherwise it would induce the impossible quotient map. Adjacent vertices are
distinct immediately because their required distance is one.

## 4. Certified four-cycles force linear equations

Let `a,b,c,d` be a unit-edge four-cycle with both opposite pairs distinct.
The images of `b,d` are the two common points of the unit circles centred at
the distinct images of `a,c`. Reflection about the midpoint of the centres
interchanges them. Therefore

    p(a)-p(b)+p(c)-p(d)=0.

Each geometric certificate lists four-cycles and proves both diagonal
inequalities by surviving edges or quotient odd wheels. After translating one
vertex to the origin, the alternating cycle equations form an integer matrix
`A`. The certificate provides a sparse rational matrix `P` whose named free
rows form an identity matrix and for which `AP=0`. A modular rank computation
at the checked prime 1,000,000,007 gives `rank(A)=301-columns(P)`. A nonzero
minor modulo the prime is a nonzero integer minor, while the independent
columns of `P` give the reverse bound. Thus the columns of `P` form the full
real kernel of `A`.

## 5. Each five-chromatic repair has a norm contradiction

For a surviving edge `uv`, let `d_uv` be row `u` of `P` minus row `v` of `P`.
Each certificate supplies nonzero integer weights `lambda_uv` on a small set of
surviving edges and verifies exactly that

    sum lambda_uv d_uv^T d_uv = 0,
    sum lambda_uv != 0.

Every possible coordinate pair satisfying the forced linear equations has
the form `x=P s`, `y=P t`. Hence the first identity implies

    sum lambda_uv ||p(u)-p(v)||^2 = 0.

If every surviving graph edge had length one, the left side would instead be
the nonzero coefficient sum. This contradiction excludes all plane unit-edge
maps, including maps that identify arbitrary nonadjacent vertices not already
separated by the certificate.

Applying this independently to all twelve exactly five-chromatic cases, and
combining it with the six direct colourings, proves the stated complete
18-case decision.

## Trust boundary and scope

The theorem depends on the pinned source graph and h3993 interface identities,
the six explicit colourings, the strict LRAT replay, and the twelve direct
standard-library geometric audits. It does not depend on the SAT solver that
found the split, the solver that emitted the DRAT trail, `drat-trim`, FLINT,
floating-point coordinates, injectivity, symmetry, or assumptions on nonedges.

The result concerns exactly one deletion from the 18-edge norm support. It
does not prove that a repair deleting another h3993 clause edge is impossible.
The 7,544,256-byte generated compressed LRAT used for the twelve chromatic
lower bounds is retained locally and deliberately omitted from Git pending
explicit human approval. Its hashes and strict replay receipt are public, but
replaying those twelve lower bounds requires the byte-identical local archive.
