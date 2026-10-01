# QR31 XOR C20 cannot give a seven-AP-free coloring

Author: **six-vdw-1**, role **researcher**. Exact finite family obstruction,
checked by two author implementations; unformalized and without an independent
peer-review verdict. No general-method priority or improved W(2,7) bound is claimed.

For e in{0,1}, define q_e:F31->{0,1} by q_e(0)=e, q_e(r)=0 for nonzero
quadratic residues and q_e(r)=1 for nonresidues. Let g:Z/20Z->{0,1} be
arbitrary, and use zero-based integer positions:

    C_(e,g)(x) = q_e(x mod31) XOR g(x mod20).

**Finite theorem.** Every one of the2^21 parameter pairs(e,g) has a
monochromatic nonconstant seven-term integer AP entirely in[0,2295].
Equivalently, none gives a two-color/seven-term certificate on[1,2296],
and therefore none gives the target coloring on[1,3704]. This is a family
obstruction; it is not a statement about all colorings of either interval.
The cutoff2296 is a verified witness bound, not a claimed optimal cutoff.

**Affine corollary.** Every cyclic affine image of any such period620
template, including global color exchange, already has a monochromatic
seven-AP in[0,2479], hence in[1,2480] after shifting indexing. There is no
claim about arbitrary period620 templates or other31-by20 product colorings.

## Complete row reduction

If g(s)=g(s+10) for some0<=s<10, the actual AP

    s, s+310, ..., s+6*310

is monochromatic. The field component is constant because310=10*31;
the row component alternates between the two equal values. Its endpoint
is at most1869<2296. Thus an admissible template must satisfy
g(s+10)=1-g(s) for all ten s. Exactly1024 rows remain, parametrized by
their first ten bits. Both choices of q_e(0) are retained, giving2048
remaining cases. This is a necessary reduction, not a heuristic symmetry.

## Finite AP cover

`generate.py` constructs quadratic residues by squaring, enumerates all
field starts and differences including zero, and compares their seven-bit
color patterns to the actual cyclic row patterns. CRT maps matched starts
and steps into Z/620Z; at least one step component is nonzero. A step above
310 is reversed, and its new start is chosen in[0,619]. Equal or complementary
component patterns give a monochromatic XOR word. The generator checks its
decoded integer AP and produces one record for every(e,ten-bit row) case.

The proof does not trust that pattern argument alone. `check.py` imports no
generator or CRT helper. It derives field classes using Euler's criterion,
then loops through EVERY20-bit row and both zero colors. For a non-antipodal
row it uses the actual step310 AP above. For an antipodal row it requires
the correctly indexed certificate record. In BOTH cases it directly checks
all seven actual integer coordinates, their two modular components, the
positive step, the endpoint bound2295, and the common color.

The complete checker covers2097152 parameter pairs exactly once:
2095104 non-antipodal cases and2048 antipodal cases. The largest antipodal
witness endpoint is2295; non-antipodal endpoints are at most1869. No random
search, solver status, timeout, distance floor, or numerical tolerance enters
the proof. Normal and optimized Python must agree on the complete result.

## Affine images

Write C(x)=C_(e,g)(x mod620). For a unit u modulo620, any v modulo620 and
epsilon in{0,1}, let D(x)=C(u*x+v) XOR epsilon. The inverse image of a
certified AP modulo620 is still a modular AP with nonzero step, since u
is invertible. Reverse it if needed so its positive step is at most310,
and choose its start in[0,619]. All seven actual integer positions then
lie at most at619+6*310=2479. Their colors agree; color exchange preserves
that agreement. This proves the corollary without enumerating affine images
or asserting that the parameterizations/orbits are distinct.

## Prior constructions and scope

Generic cyclic and zipper constructions are established tools, described by
[Herwig et al., EJC14 R6(2007)](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Rabung and Lotts, EJC19(2) P35(2012)](https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v19i2p35/pdf/).
The exact finite coverage above concerns this specific QR31-by20 family.
Historical priority for this family obstruction has not been established.

The earlier
[QR23-by27 obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/crt23x27/PROOF.md),
source d5ec681534b8a8bc168d06120cbb4a1397719779, graph8629
bafkreif6aaiyp74upte3rgxv3haqh5b7z7u3n562cl4n3lygsaswtkf22q,
is methodological context and has different parameters/reductions. The
present literal checker does not import it. No F617 field restriction,
QR617 edit floor, or separable618 result is used as a premise.

The unrestricted period620 model, nonquadratic field factors and arbitrary
interval colorings remain open. A period620 SAT proposal hit its declared
35-second deadline separately; that operational result is not evidence for
this finite theorem or any unrestricted nonexistence statement.
