# Proof audit

## 1. Claim under review

Let `E=Z[omega]`, where `omega=(1+i sqrt(3))/2`, and let the six units of
`E` be the sixth roots of unity.  Fix distinct nonnegative exponents
`p<q<r`.  Take five rows in `({0} union E^units)^3`, each with at least two
nonzero coefficients, whose distinct projective reductions modulo two form
the five sections of a full projective F4 pencil without a coordinate
direction.

The claim is that no physical complex number `z` makes all five forms in
`z^p,z^q,z^r` have modulus one.

## 2. Complete normalization

The independent finite audit first enumerates the unit-coefficient rows
directly.  It quotients row scaling by taking the least of all six unit
multiples.  Reduction modulo two gives 18 realized projective normals in
`F4^3`.  Exact masks on all 64 points of `F4^3` show that precisely nine
five-normal subsets cover the space; every one has lift-bucket sizes
`2,2,2,4,4`.  Their product gives 1,152 distinct lifted systems.

Diagonal multiplication of the second and third variables by units gives a
36-element action.  Direct orbit canonicalization partitions the 1,152
systems into exactly 32 orbits, all of size 36.  Independently constructed
templates show that these are exactly the sign systems

    U+V,
    U+W,
    V+epsilon W,
    U+sigma omega V+tau omega^2 W,
    U+kappa omega^2 V+lambda omega W,

where all five displayed signs range independently over `{-1,+1}`.  This is
an exhaustive quotient, not a sample or an inference from matching totals.

The first form has modulus one, so division of all three variables by `U+V`
is a rotation and permits `U+V=1`.  Write

    U=a+i sqrt(3)b,
    V=1-a-i sqrt(3)b,
    W=c+i sqrt(3)d.

For each sign system, the remaining four unit-norm conditions are four
quadratics over `Q` in the monomial order `d,c,b,a`.

## 3. Independent radius certificate

Put

    u=|U|^2,  v=|V|^2,  w=|W|^2,
    Delta=(u-v)(u-w)(v-w).

The clean-room checker implements sparse polynomials over Python `Fraction`
and executes Buchberger's algorithm in pure lexicographic order `d>c>b>a`.
It uses no critical-pair shortcut: every initial pair and every pair created
by a new remainder is processed.  A representation vector is carried through
every S-polynomial and reduction.  The checker confirms that every remainder
is exactly the represented combination of the four original quadratics;
therefore every generated basis element belongs to their ideal.  Completion
of all created pairs is Buchberger's criterion.

For 20 sign systems, exact division by the resulting basis gives remainder
zero for `Delta`.  For each of the other 12 systems, it gives remainder zero
for all three polynomials

    Delta (4u-1)(4u-3)(4u-7),
    Delta (4v-1)(4v-3)(4v-7),
    Delta (4w-1)(4w-3)(4w-7).

There are 2,431 processed S-pairs.  The ordered case classification has
SHA-256
`923de5887d8fa08b20a3f294106798d94add46e689041c8c6af9412d9a7cf549`.
A separately written SymPy script reconstructs the equations and reduced lex
bases and obtains the identical entry-level classification hash.  The SymPy
calculation is corroboration, not a dependency of the portable proof.

At a common zero, either `Delta=0`, giving two equal squared radii, or all
three radii are distinct roots of `(4t-1)(4t-3)(4t-7)`.  In the latter case
their unordered set is exactly `{1/4,3/4,7/4}`.

The controls retain exact solutions realizing both free-vector alternatives:
`U=V=W=1/2`, and
`U=i sqrt(3)/2`, `V=1-i sqrt(3)/2`, `W=1/2`.  Hence the proof does not
silently strengthen radius rigidity into free-vector nonconcurrence.

## 4. The all-unit boundary

If `u=v=w=1` and `U+V=1`, elementary unit-circle geometry makes `U,V` the
two unit vectors at angles plus or minus `pi/3`.  The equation `|U+W|=1`
then makes `W/U` a primitive cube root.  Thus `U,V,W` are Eisenstein units.

If all five displayed forms also had modulus one, each would be an
Eisenstein unit and therefore nonzero modulo two.  But the five hyperplanes
of a full F4 pencil cover `F4^3`, so one form must vanish modulo two.  This is
a contradiction.  The audit also exhausts all 384 sign/unit triples with
`U+V=1` and obtains zero survivors.

## 5. Return to distinct powers

The normalizing coefficient changes and the division by `U+V` have unit
modulus.  Therefore, with `rho=|z|^2`, the three squared radii are

    u=rho^p,  v=rho^q,  w=rho^r.

For `rho=0`, at least two positive-exponent terms vanish, forcing one of the
three binomial forms to vanish; this includes the `p=0` boundary.  For
`rho=1`, all radii are one, already excluded.  If `rho>0` and `rho!=1`, the
radii are distinct.  When `p=0`, one equals one and hence the exceptional set
is impossible.  When `p>0`, all three radii lie below one if `rho<1`, or all
lie above one if `rho>1`, whereas `{1/4,3/4,7/4}` straddles one.  This
exhausts physical `z` and proves the theorem.

## 6. Exact A5 interface

Embedding each of the nine three-variable pencils on each three-subset of
the four nonconstant A5 positions gives `9*C(4,3)=36` distinct pencils and
`36*128=4,608` lifts.  The h4195 residual was regenerated through the public
dependency chain and has canonical JSON hash
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
Definition-level filtering finds exactly 24 homogeneous three-position
pencils, all among the 36 derived pencils, hence 3,072 residual lifts.

This comparison uses the literal residual only.  It does not import the
conditional global orbit-allowance accounting at h4117/h4175/h4177.

## 7. Scope and trust

The main checker uses CPython integers and `Fraction`; it imports no target
artifact.  Correctness additionally requires inspection of the written
normalization, Buchberger implementation, ideal-to-radius interpretation,
all-unit argument, and common-radix deduction.  The secondary CAS check uses
SymPy 1.14.0 over `QQ` in lex order.  The target package's own 93,468-byte
certificate regenerated byte for byte and its portable normal and optimized
replays passed, but those checks are author-path validation rather than the
independent proof.

The optional target claim excluding the 24 residual pencils over independently
complexified coordinate variables was not independently audited here and is
not part of the verdict.  It is stronger on a smaller class and unnecessary
for physical nonconcurrence.  Four-position pencils, extra arbitrary common
dilations, and the remaining A5 frontier are open within this review scope.
