# A three-triangular-patch contact gate

Let

\[
R=\mathbb Z[\omega],\qquad \omega=(1+i\sqrt3)/2,
\]

and let

\[
P=\{a+b\omega:a^2+ab+b^2\le48\}.
\]

The patch has 169 points and 456 unit edges.  Write
\(\rho(a+b\omega)=a-b\pmod3\).  The complete physical unit-distance
graph on three copies through the origin has at most
\(3\cdot169-2=505\) points.

## Exact family

For an orientation \(\alpha\notin\mathbb Q(\omega)\), the existing
two-lattice theorem says that \(P\cup\alpha P\) is four-chromatic exactly
when it has a cross edge whose endpoints both have residue zero.  The exact
contact-line census for this smaller patch has 126 such irrational lines,
and hence 252 oriented phases (the two roots of each line).

This package considers every

\[
P\cup\alpha P\cup\beta P
\]

with distinct \(\alpha,\beta\) among those 252 phases.  There are
\(\binom{252}{2}=31,626\) labelled choices.  This is a deliberately finite
construction family, not the family of all triples of triangular lattices.

## Theorem

Every member of this 31,626-case family is four-colourable after reconstructing
all physical coincidences and every unit edge.  In fact:

- every base-four phase has zero-to-zero contacts but no
  nonzero-to-nonzero contact;
- for 30,420 phase pairs, \(\bar\alpha\beta\) is generic and the two moved
  patches have no additional nonuniversal contact or coincidence;
- for the remaining 1,206 pairs, \(\bar\alpha\beta\in\mathbb Q(\omega)\);
- no relative phase is another irrational contact phase.

The last item is the exact obstruction to making all three pairwise unions
four-chromatic inside this event family.

## Explicit colouring

Use colour names `A,B,+,-`.  On the base patch give residue zero colour `A`
and the two nonzero residues colours `+,-`.  On both moved patches give every
nonorigin residue-zero point colour `B`, while the common origin keeps `A`.

The base-to-moved contact lines contain no edge with both residues nonzero,
so those contacts are properly coloured by the two disjoint palettes.  If
\(\bar\alpha\beta\) is generic, there are no further contacts.  If it is in
\(\mathbb Q(\omega)\), its primitive denominator is nonzero modulo three and
the extended residue homomorphism gives one consistent `+,-` colouring on
both moved patches.  This also makes every physical coincidence receive one
colour.  Unit neighbours of the shared origin have nonzero residue, so
changing the moved zero class from `A` to `B` creates no monochromatic edge.

`verify.py` proves the finite hypotheses and checks the displayed colouring
on every reconstructed quotient graph.  Its phase arithmetic uses sparse
squarefree radicals over exact `Fraction` coefficients; no floating-point
comparison or SAT result is a proof premise.

## Scope and construction consequence

This closes the natural 505-point gate in which both moved orientations are
individually strongest against the base patch.  It does **not** prove that
arbitrary triples of triangular lattices are four-colourable, and it does not
classify triples where one or both base pairs are only three-chromatic.

No five-chromatic graph is produced.  The result is useful as a pivot rule:
a three-lattice construction must exploit a genuinely ternary phase pattern
outside this strongest-pair event family, rather than combining two isolated
two-layer obstructions at a common base.

## Reproduce

From the repository root, with CPython 3.11 or later:

```bash
python3 -B hadwiger_nelson_three_triangular_contact_gate/verify.py
python3 -O -B hadwiger_nelson_three_triangular_contact_gate/verify.py
```

Only the Python standard library is used.
