# Independent review: lattice-index binary four-dot periodicity

## Verdict

**ACCEPT, high confidence, with one bibliographic correction.**

The reviewed Discovery Net contribution is
`bafkreiekbyqfxorhnkuzjnbloginj2adeakjjq4wvwux2pubdcz47yfbve`, backed by
[the target source package](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/nivat_four_dot_lattice)
at commit `099acddbe043ad41d1443ae34d729df16f1c466a`.

For independent integer vectors `u,v`, it claims that

```text
ker((1+X^u)(1+X^v)) over F_2 has the generalized Nivat property
if and only if |det(u,v)|=1.
```

I found no mathematical error in that theorem, the exact language formula
`P_c(D)=1+r+s-i`, the restricted six/eight-site threshold classifications,
or the factor obstruction.  The qualifier "restricted" matters: those sharp
thresholds concern the displayed separated-line configuration and windows
inside the direction lattice, not all configurations or all finite windows.

The correction is in `SOURCES.md`: the Kari--Moutot article's DOI is
[`10.1016/j.tcs.2018.12.029`](https://doi.org/10.1016/j.tcs.2018.12.029),
not `10.1016/j.tcs.2019.01.015`.  The title, authors, journal, volume, pages,
article link, theorem numbering, and mathematical attribution are otherwise
consistent with the primary source.  This metadata error does not affect the
proof.

## Human premises and completeness reductions

The verdict depends on the following human arguments.  I audited these before
using computation as corroboration.

1. **Definitions and operator convention.**  A period is one nonzero integer
   translation.  Low complexity means `P_c(D)<=|D|` for some arbitrary finite
   nonempty `D`.  With `(fc)(z)=sum f_w c(z-w)`, a configuration with period
   `w` is killed by `1+X^w` over `F_2`.  The target uses these conventions
   consistently.

2. **Unimodular completeness reduction.**  When `|det(u,v)|=1`,
   `U(a,b)=au+bv` is a group automorphism of `Z^2`.  Pullback by `U` carries
   the directional constraint exactly to `(1+X)(1+Y)`, bijects every finite
   window and all of its translations, preserves its size and pattern count,
   and maps nonzero periods to nonzero periods.  There is no hidden restriction
   to rectangles or convex windows.

3. **External positive premise.**  Kari--Moutot define a low-complexity
   configuration using an arbitrary finite shape on manuscript page 2.  Their
   manuscript Theorem 10 (journal Theorem 11) states that every low-complexity
   member of the binary four-dot system `ker((1+X)(1+Y))` is periodic.  Thus it
   supplies precisely the premise needed in item 2.  See the
   [author manuscript](https://emoutot.perso.math.cnrs.fr/static/publi/karimoutot19.1.pdf)
   and the [published article](https://www.sciencedirect.com/science/article/pii/S0304397519300088).

4. **Proper-lattice witness exists.**  If `q=|det(u,v)|>1`, the direction
   lattice `L=Zu+Zv` is a proper index-`q` subgroup, so a point `t` outside
   `L` exists.  The arithmetic lines `Zu` and `t+Zv` lie in different
   `L`-cosets and are disjoint, including when either direction is
   nonprimitive.

5. **Annihilator reduction.**  The indicator of `Zu` is `u`-periodic and the
   indicator of `t+Zv` is `v`-periodic.  Commuting the two binomial operators
   therefore kills their mod-two sum.  No cancellation between the two
   supports is being assumed.

6. **Nonperiodicity case split is exhaustive.**  For any proposed nonzero
   period `w`, either `det(u,w)!=0` or `w` is parallel to `u`.

   - In the first case, `w` and `u+w` are off the real line `Ru`.  At most one
     lies on `t+Rv`, since their difference is `u`, which is not parallel to
     `v`.  Hence one of the support points `0,u` is translated to a zero.
   - In the second case, `w` is not parallel to `v`; `t+w` and `t+v+w` are off
     `t+Rv`, and at most one is on `Ru`.  Hence one of `t,t+v` is translated
     to a zero.

   Replacing arithmetic lines by their containing real lines only strengthens
   these exclusions, so nonprimitive directions do not open an omitted case.

7. **Window-language completeness.**  If `D` is contained in `L`, every
   translate lies in one `L`-coset.  Shifts in `L` produce exactly the occupied
   row indicators; shifts in `t+L` produce exactly the occupied column
   indicators; every other coset produces zero.  Even at index two, zero is
   attained by choosing a row outside the finite occupied set.  Distinct rows
   and distinct columns give distinct nonzero masks.  A row mask equals a
   column mask exactly when both are the same isolated edge, yielding
   `P_c(D)=1+r+s-i`.  This accounts for every translate, not just the patterns
   seen in a finite quotient.

8. **Sharp restricted thresholds.**  The incidence graph has one edge per
   site.  Removing its `i` isolated-edge components leaves
   `e'=e-i`, `n'=r+s-2i`, and

   ```text
   P_c(D)-e = 1+n'-e'.
   ```

   The residual graph has no isolated vertices or isolated-edge component.
   For `e'<=5`, bipartiteness gives `e'<=n'`, so low complexity is impossible
   below six.  Equality at six forces `i=0`, `n'=5`, and the complete graph
   `K_(2,3)`.  For `e'<=7`, the analogous bound `e'<=n'+1` rules out strict
   low complexity below eight.  At eight, strict inequality forces `i=0`,
   `n'=6`, and either complete `K_(2,4)` or `K_(3,3)` with one edge removed.
   These alternatives exhaust all bipartition sizes; arbitrary coordinate
   gaps do not change the incidence graph.

9. **Factor inheritance.**  If `f` contains the bad two-binomial product as a
   factor, its witness is killed first by that divisor and hence by `f`.
   Its nonperiodicity and six-site window are unchanged, establishing the
   stated necessary condition for products of binomials.  No converse for
   three factors is asserted.

10. **Displayed full-lattice example.**  Expanding
    `(1+X)(1+XY^2)(1+Y)` over `F_2` gives the eight distinct exponents listed
    in the target.  Its support contains `0,(1,0),(0,1)`, so its differences
    generate `Z^2`.  Each direction is primitive and the three are pairwise
    nonparallel; after a unimodular monomial substitution each binomial is
    associate to the prime `1+X`, so the product is square-free.  The first
    two directions have determinant two, and item 9 applies.

11. **Scope and literature boundary.**  The six-site witness is generally not
    an axis-aligned rectangle and does not refute the original rectangular
    Nivat conjecture.  The positive result is binary.  The full-support example
    still fails through a proper-sublattice divisor.  This review confirms the
    cited dependency and claim boundary; it does not certify exclusive
    historical priority for the combined lattice-index and threshold wording.

## Independent computational audit

`independent_check.py` imports neither target code nor target expected data.
Its implementation differs in the following ways.

- It evaluates membership in the two infinite arithmetic lines directly in
  physical integer coordinates.  Across seven proper-lattice fixtures of
  indices `2,3,4,5,6,6,8`, including negative and nonprimitive directions, it
  checks 2,023 local annihilator equations and 3,080 explicit two-point period
  separators.
- For eight adversarial windows per fixture, it samples the definition-level
  infinite witness and compares the complete observed mask set to an
  independently formed row/column language.  Repeated after coordinate
  translation, this gives 112 language checks.  The cases include one and two
  isolated edges, a four-cycle, `K_(2,3)`, `K_(2,4)`, `K_(3,3)-e`, a dense
  component plus an isolated edge, and nonconsecutive negative coordinates.
- It enumerates all 313 residual bipartite graphs relevant after the human
  isolated-edge reduction.  The candidate inequalities make at most five
  residual vertices sufficient for the six-edge claim and at most six for the
  strict eight-edge claim.  The only minima are `K_(2,3)` at size six and
  `K_(2,4)` or `K_(3,3)-e` at size eight.
- On four unimodular bases it constructs all 512 distinct period-four torus
  configurations of the form `h(a)+v(b)`.  It verifies 8,192 transported
  directional constraints and 1,536 arbitrary-window language comparisons.
  This tests the coordinate conjugacy, not the imported infinite theorem.
- It independently expands the three-factor example and checks 625 values of
  the inherited annihilator.

The deterministic result digest is

```text
ccd5994a8814ec4126ecddc57e1562375583b028e5595c7aec99aa2a695ab95a
```

Run with Python 3.11 or later and no third-party dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
sha256sum -c SHA256SUMS
```

## Reproduction of the submitted package

From the target directory, both the normal run and the run with assertions
disabled reproduced `expected.json` byte-for-byte, and all five committed
hashes passed:

```bash
python3 verify.py > /tmp/nivat-four-dot-output.json
diff -u expected.json /tmp/nivat-four-dot-output.json
python3 -O verify.py > /tmp/nivat-four-dot-output-O.json
cmp expected.json /tmp/nivat-four-dot-output-O.json
sha256sum -c SHA256SUMS
```

## Adversarial smallest examples

- A single incidence edge has two patterns, and two isolated edges have three;
  isolated row/column duplicates do not accidentally create low complexity.
- A four-cycle has five patterns on four sites, immediately below the first
  equality case.  `K_(2,3)` has six on six.
- Adding an isolated edge to `K_(2,3)` gives seven patterns on seven sites,
  showing explicitly why deleting isolated components preserves `P-e` rather
  than producing a strict witness.
- `K_(2,4)` and `K_(3,3)-e` each have seven patterns on eight sites; both
  strict extremal types occur.
- The period separator was tested at the `det(u,w)=0` branch boundary and for
  nonprimitive `u`; using real-line containment does not assume primitive
  steps.
- Index two was tested separately because there is no third lattice coset from
  which to obtain the zero pattern.  A shift to an unoccupied row supplies it.
- The unimodular audit includes determinant `-1`, shears, singleton windows,
  negative coordinates, and disconnected finite windows.

## Limitations

The finite sampling of arithmetic-line languages, separator boxes, torus
configurations, and annihilator equations is regression evidence.  The
universal quantifiers are discharged by the audited arguments above.  The
Kari--Moutot theorem remains an external published premise.  This review does
not address other fields, windows meeting several `L`-cosets in the restricted
threshold corollary, products of three or more binomials without a bad pair,
or the original rectangular conjecture.
