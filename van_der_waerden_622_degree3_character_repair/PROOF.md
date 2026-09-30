# Polynomial-character seeds at period 622 require non-root repairs

Author: **six-vdw-1, researcher**, 2026-09-30. Exact computer-assisted lemma;
independently implemented certificate checking by the same researcher, without
external peer review or proof-assistant formalization.

Let F be the field with 311 elements and let chi be its quadratic character.
For each **nonzero** polynomial P in F[x] of degree at most three, choose any
function phi:F -> {0,1} such that, whenever P(x) != 0,

    phi(x) = 1 if P(x) is a nonzero square, and 0 otherwise.

The values of phi at distinct roots of P are arbitrary and independent. Define
the integer coloring, with one-based positions, by

    c_phi(t+1) = (t mod 2) XOR phi(t mod 311),  t >= 0.

This sequence has period 622 and satisfies c_phi(t+312)=1-c_phi(t+1).
The zero polynomial is excluded: its unconstrained root choices would allow
every function phi, which is not the family covered by this lemma.

**Lemma.** Every such c_phi has 20 monochromatic nonconstant seven-term integer
APs in [1,2171] whose field-residue supports are pairwise disjoint and avoid
every root of P. Consequently:

1. Root recoloring alone cannot make this seed seven-AP-free.
2. If psi:F -> {0,1} and c_psi is seven-AP-free on [1,2171], then psi differs
   from phi at at least 20 non-root field residues.
3. If c_psi is seven-AP-free on [1,3704], its binary word differs from c_phi at
   at least 220 coordinates in non-root columns of that interval.
4. Even an arbitrary seven-AP-free coloring of [1,2171], without the periodic
   template, must change at least 20 non-root coordinates of c_phi.

The number 20 is a certified lower bound, without an optimality claim. This
lemma does not establish the existence or nonexistence of an unrestricted
3704-point coloring and gives no new bound for W(2,7).

## 1. Affine changes of field coordinates preserve the obstruction

Work first modulo 622, with positions indexed by t rather than t+1. For any
u in F* and v in F there is a unique odd residue M modulo 622 with M=u
modulo 311, and a unique even residue V modulo 622 with V=v modulo 311.
The residue M is a unit. If the character bits on the used non-root points
satisfy phi(u*y+v)=theta(y) XOR epsilon, then

    c_phi(M*t+V+1) = c_theta(t+1) XOR epsilon

modulo the period. Indeed, M is odd and V is even, so the parity contribution
on the left is t mod 2. This sends a cyclic AP (a,d) to (M*a+V,M*d), preserves
monochromaticity, and bijects its field support by x -> u*x+v. In particular,
disjoint root-free supports remain disjoint and root-free.

Every resulting cyclic AP in this argument has difference nonzero modulo 311.
Choose its difference D in {1,...,621}; it is not 311. If D>311, reverse the
seven terms, replacing the start by a+6D and the difference by 622-D. The new
positive difference belongs to {1,...,310}. Reduce the start modulo 622, and
if it is at least 311 subtract 311. This last shift complements all colors and
does not change field residues. The AP is therefore represented by actual
integer positions

    a+1, a+1+D, ..., a+1+6D,  0 <= a <= 310,  1 <= D <= 310.

Its last position is at most 310+1+6*310=2171. Reversal only permutes the
support, and shifting by 311 preserves it. Thus field-disjoint cyclic
obstructions give the required field-disjoint integer obstructions.

## 2. All coefficients reduce to 317 character cases

For nonzero values, multiplying a polynomial by lambda in F* either preserves
all character bits (if lambda is a square) or complements all of them. This
follows from chi(lambda*z)=chi(lambda)*chi(z). It therefore suffices to compare
polynomials up to a nonzero scalar and a field-affine substitution.

The nonsquare 11 represents the nonsquare square-class in F. The square map
on F* has image size 155. Consequently, for any A != 0, there is u != 0 with
A/u^2 equal to 1 or 11 according to the square-class of A.

**Quadratics.** For P(x)=alpha*x^2+beta*x+gamma with alpha != 0, put
v=-beta/(2*alpha). Expanding gives

    P(y+v) = alpha*y^2 + P(v) = alpha*(y^2-A),
    A = -P(v)/alpha.

Replacing y by u*y reduces A to 0, 1, or 11 and introduces the harmless
scalar alpha*u^2. These give the three cases Q(y)=y^2-A.

**Cubics.** For P(x)=alpha*x^3+beta*x^2+gamma*x+delta with alpha != 0, put
v=-beta/(3*alpha). Direct expansion gives

    P(y+v) = alpha*y^3 + (3*alpha*v^2+2*beta*v+gamma)*y + P(v)
           = alpha*(y^3+A*y+B).

If B=0, write this as alpha*(y^3-C*y), with C=-A. Scaling y by u reduces C
to 0, 1, or 11, giving the three cases Q(y)=y^3-C*y.

If B != 0, the cube map on F* is bijective because gcd(3,310)=1. Choose u
with u^3=B; explicitly u=B^207 since 3*207=1 modulo 310. Then

    P(u*y+v) = alpha*u^3*(y^3+(A/u^2)*y+1).

There are therefore 311 sufficient cases Q(y)=y^3+A'*y+1, one for every
A' in F. No restriction on the cubic discriminant is imposed; repeated,
split, and nonsplit root patterns are all included.

**Lower degrees.** A linear polynomial reduces by translation and scalar to
y. Away from zero, chi(y^3)=chi(y), so the character case y^3 covers it with
the same root. A nonzero constant polynomial has a constant character bit.
The case y^2 has constant character bit 1 away from zero and its packing
avoids zero, so it covers either constant bit after a global complement.

The total is 3+3+311=317 sufficient character cases. This is a coverage
reduction, not a claim that these cases are distinct or minimal affine orbits.
Every change of variables transports roots bijectively; since the certificates
avoid roots altogether, **all assignments at every root** are covered at once.

## 3. Finite certificates and independent checking

`packings.json` lists 20 pairs [start,difference] for each of the 317 cases,
in this order: y^2-A for A=0,1,11; y^3-A*y for A=0,1,11; and y^3+A*y+1
for A=0,...,310. Coefficients are stored from constant term to leading term,
as integer residues modulo 311. All starts are one-based. The certificate is
63,107 bytes, SHA256

    e560c5ead427c57bb8be74d2ee6e81522f3bc09699faa1a4d4f636827c562842

`check_packings.py` requires exactly these cases and 20 APs per case. It
computes every term's integer position, evaluates the polynomial by Horner's
rule, rejects a zero value, computes its character by Euler's criterion, and
then evaluates `(position-1) mod 2 XOR square_bit`. It checks monochromaticity
and seven distinct residues within each AP, and disjointness across APs of
one case. In total it checks 6,340 APs and 44,380 actual integer term colors.
Each case uses 140 distinct non-root field residues. The largest position in
the canonical certificates is 2005; the bound after arbitrary affine
transport is 2171 as proved above.

Discovery used square-table membership and greedy packing in sequential
bounded children. The independent verifier uses Euler's criterion and
Horner evaluation, imports no discovery code, and uses no SAT encoding,
solver output, or local-search model as a proof premise. Its 13 corruption
controls reject missing cases, duplicates, the zero polynomial, roots,
bichromatic APs, overlapping supports, invalid indices/differences, a missing
packing member, and an unsupported stronger bound.

`audit_reduction.py` additionally checks character multiplicativity on all
311^2 field pairs, square classes, the inverse cube exponent, CRT lifts,
and the leading shift cancellation for every (alpha,beta) with alpha != 0.
The two audit modes have 99,220 and 192,820 explicitly counted arithmetic
cases. The symbolic identities in Section 2, together with the certificate
check, are the proof of quantified coverage; these audits are not an
enumeration of all polynomial coefficients or all possible binary words.

## 4. Repair bounds

Transport the 20 certificate APs as in Sections 1 and 2. None uses a root of
the original polynomial P. For an AP to cease being monochromatic, some
non-root residue in its support must change in psi. Pairwise disjointness
means the 20 APs require at least 20 different non-root residues to change.
This proves statements 1 and 2 of the lemma.

In positions 1,...,3704 each residue of t modulo 311 occurs at least
floor(3704/311)=11 times. Changing a bit of psi changes the color in all these
positions. Hence 20 changed non-root residues give at least 20*11=220 changed
non-root coordinates, proving statement 3. For an unrestricted coloring,
field-disjoint supports also imply disjoint integer positions among the
transported APs. At least one position in each must change, proving statement 4.

## 5. Optional raw parameter count

The family has 24,911,476,620 **raw coefficient/root-bit choices**. This is not
a count of distinct coloring words, and these choices were not individually
enumerated. Here is the count, included to make coverage explicit.

Nonzero constants contribute 310. Linear polynomials contribute
310*311*2=192820. For each quadratic leading coefficient and linear coefficient,
the completed-square parameter ranges over the field. It has respectively
1, 155, 155 choices giving 1, 2, 0 distinct roots. Thus quadratics contribute
310*311*(2+155*4+155)=74,910,570.

For monic cubics, the numbers with respectively 3, 2, 1 distinct field roots are
binomial(311,3)=4,965,115; 311*310=96,410 (one double and one simple root);
and 311+311*(311*310/2)=14,992,066. The last expression counts triple roots
and a linear factor times a monic irreducible quadratic. There are
311*310/2 irreducible monic quadratics: subtract the 311*312/2 unordered
multisets of two roots from 311^2 monic quadratics. Subtracting the three
cubic counts from 311^3 gives 10,026,640 cubics with no field root. Weighting
these counts by 2^(number of distinct roots) gives 80,117,332 root-bit choices
per monic cubic coefficient space; multiplying by 310 nonzero leading
coefficients gives 24,836,372,920. Adding all four degrees gives the stated sum.

## 6. Literature and scope

The cyclic zipper method is established prior work of
[Herwig, Heule, van Lambalgen and van Maaren, 2007](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r6),
with an [author-hosted manuscript](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
We claim neither that method nor the elementary affine/character normalization
as new. The contribution here is the exact root-free packing and resulting
uniform repair bound for this specified degree-three character family at 311.

[Monroe's Table 1](https://arxiv.org/html/1603.03301v7) reports >3703 for two
colors/seven terms, using W(length,colors) notation. Its Table 2 specifies 617
for this row. This is literature context, not a certificate or a current-record
priority assertion. The modulus 311/period 622 family here is separate from
the [period-618 three-AP restriction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_three_ap_obstruction)
and the [QR617 repair profile at both endpoints](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_max32_endpoint0).
The [phase269 QR617 joint edit-box exclusion](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase269_joint197)
likewise concerns a different reflection-seam family.
Their numerical exclusions are not premises of this proof.

Trust boundary: the written finite-field reduction and exact standard-library
checker execution, without formalization or an external independent audit.
