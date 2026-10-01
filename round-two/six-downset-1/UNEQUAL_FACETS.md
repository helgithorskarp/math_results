# Rational capped rank repair for any two Boolean facets

Actual author: **six-downset-1**, role **researcher**, 2026-10-01.
Complete author-checked ordinary proof, unformalized and independently
unreviewed. Exact full-matrix checks validate the construction.

## Quantified result and what is credited

Let a>b>=1 be integers, t=2^(a-1), u=2^(b-1), and let D be the union
of full a-point and b-point cubes on disjoint supports. Then

    t>=2u, N=2t+2u-1, s=t, B=N-t=t+2u-1.

There is an explicit rational capped H matrix with

    rank(BM+tI)=N-t, rank(I-M)=N-1.

The lower rank is maximal among **all real H matrices** on this family.
The unit endpoint is simple, and every nonunit eigenvalue is at most
1-beta/(2B), where

    beta=(2u-1)(t-2u+1)/(t-1)>0.

Combined with the equal-cube result and the elementary rank-one family,
this gives rational capped certificates of universally maximal lower
rank for every downset with **exactly two maximal members**, regardless
of their sizes or overlap. The complete formulas for that corollary
appear below. This is an explicit spectral-rank construction, not a
priority claim for ordinary H on two-facet families.

The core lift, ordinary shifted union, maximum-family forced kernel,
and capped tensor transport are credited prior mechanisms; see
[PROOF.md](PROOF.md), Sections 1,2,5,6 and their cited sources. The new
ingredients here are the aligned full vectors, a centered complementary
residual at a larger parameter, the exact strictly positive cap margin,
and a rational convex repair removing the excess lower kernel.

## A centered proper-cube residual

Consider the 2u-2 proper nonempty vertices of the smaller cube, u>=2,
split into u-1 complementary pairs. Define Z by

    diagonal t-2,
    complementary off-diagonal 2u-t-2,
    every other off-diagonal -1.

Its row sums vanish. Pair-constant centered vectors have eigenvalue
2u-2 with multiplicity u-2; pair-antisymmetric vectors have eigenvalue
2(t-u) with multiplicity u-1; the constant vector has eigenvalue zero.
These mutually orthogonal spaces have total dimension 2u-2. This proves
Z>=0 for every t>=u, including the stated range. When u=1 the proper
domain is empty and no residual space is needed.

This decomposition is literal two-by-two complementary-pair algebra:
the pair-constant block has diagonal 2u-4 and off-diagonal -2,
while each antisymmetric pair direction has eigenvalue
(t-2)-(2u-t-2)=2(t-u). Thus no harmonic-completeness assumption is hidden.

## An aligned capped core

Take one vector h with squared norm t-1. Give the full vertex of EACH
cube this same vector. For a proper nonempty vertex in a cube of star
size v (v=t for the larger cube, v=u for the smaller), take

    g_A=-h/(t-1)+w_A.

Choose the w_A perpendicular to h, with Gram t/(t-1) times the residual
Z just defined, using v in place of u. The two residual spans are
orthogonal to one another. Their sum vectors are zero because Z1=0.
This defines a PSD core C_cap with all diagonals t-1 and with entry -1
on every distinct intersecting pair. Its entries are rational:

* the large-cube block is its original complement core tP-J;
* the small-cube diagonal is t-1; full/proper off-diagonals are -1;
* small proper complementary off-diagonals are
  [1+t(2u-2-t)]/(t-1), with every other proper off-diagonal -1;
* between different cubes, full/full is t-1, full/proper is -1,
  and proper/proper is 1/(t-1).

All cross-cube pairs are disjoint, so none of these cross entries
violates the support prescription. Apply the credited empty lift to
obtain M_cap. The empty Gram vector is -sum_A g_A. The large cube's
nonempty sum is -h; the small cube's is (t-2u+1)h/(t-1). Thus the lifted
empty vector is 2(u-1)h/(t-1).

The full frame operator of Q_cap splits orthogonally into the two
residual spaces and the h direction. There are no mixed terms because
the sums of residual vectors vanish. The large residual has eigenvalue
2t, multiplicity t-2. The small residual has eigenvalues

    2t(u-1)/(t-1), multiplicity u-2,
    2t(t-u)/(t-1), multiplicity u-1,

when u>=2; both are at most 2t. At u=1 the small residual is absent.
The eigenvalue in the h direction, including the empty lift, is

    kappa=2t+2(u-1)(2u-1)/(t-1).

It is at least 2t and is the greatest eigenvalue of Q_cap. Consequently

    N-kappa=beta=(2u-1)(t-2u+1)/(t-1)>0,
    B(I-M_cap)=N I-J-Q_cap >= beta P_(1-perpendicular).       (1)

The equal-order case t=u is deliberately excluded from this construction;
its orthogonal-span capped union is supplied by PROOF.md. The power-of-two
gap ensures t>=2u, so the strict inequality in (1) holds for every
unequal pair of cube orders. The u=1 boundary has kappa=2t,beta=1.

## Removing the remaining lower kernel

Let C_shift be the ordinary union core from the larger complement core
and the smaller complement core plus (t-u)I. It is PSD. Its small block
is positive definite since t>u; its large block has nullity t. Therefore
C_shift has nullity exactly t. The corresponding M_shift is ordinary
H, with no cap assertion. Define

    q=(N-1)(t-1)+t+u-2+(t-u)(2u-1),
    epsilon=beta/[2(beta+q)],
    C=(1-epsilon)C_cap+epsilon C_shift,
    M=(1-epsilon)M_cap+epsilon M_shift.                        (2)

Here q=Tr(Q_shift)>0: the first term is Tr(C_shift), and the remaining
terms are 1^T C_shift1. Both certificates have the same N,t and prescribed
entries, so their lift and mixture agree exactly. All coefficients are
rational, and 0<epsilon<1.

Every maximum family of the larger cube has size t in D. Its indicator
must be annihilated by any H core, including C_cap. The credited
complementary exchanges span a t-dimensional space on that branch;
it is exactly ker C_shift. Hence ker C_shift is contained in
ker C_cap. A positive mixture of PSD matrices has the intersection of
their kernels, so the new core in (2) has nullity exactly t. The lower
rank is N-t, universally maximal by the same forced-span obstruction.

Since Q_shift>=0, Q_shift<=qI. On the constant-vector complement this
implies B(I-M_shift)>=-qI. Combine it with (1):

    B(I-M) >= [(1-epsilon)beta-epsilon q]I
            = (beta/2)I on 1-perpendicular.                  (3)

Thus the repaired matrix is capped with a simple unit eigenvalue and
the stated rational gap. No closeness heuristic, floating eigenvalue,
or unspecified choice of a sufficiently small perturbation is used.
The seed may have signed entries. Entrywise nonnegativity is not claimed.

## Every two-facet downset, and products

Let F,G be distinct incomparable nonempty sets, C=F intersect G,
A=F minus G and B=G minus F. Both petals are nonempty. Put
c=|C|, a=max(|A|,|B|), b=min(|A|,|B|), t=2^(a-1),u=2^(b-1).
Then

    2^F union 2^G = 2^C times (2^A union 2^B).

Let N0=2t+2u-1 be the petal-union size. When c=0 its largest star is t.
If a>b, (2) gives maximal lower rank N0-t. If a=b>=2, PROOF.md gives
maximal lower rank N0-2t. If a=b=1, the petal family is
{empty,{x},{y}}, with M=(J_3-I_3)/2 and maximal lower rank1=N0-2t.
This last elementary baseline is credited, not a new theorem.
In all cases the chosen petal matrix is capped, has a simple unit
eigenvalue, and has every other eigenvalue of absolute value strictly
less than one.

For c>=1 the full downset has N*=2^c N0 and largest star S=N*/2.
Tensor with the core-cube complement matrix. A tensor eigenvalue -1
must use a core eigenvalue -1 and the petal's simple +1, so the lower
nullity is precisely 2^(c-1). The full-cube maximum cylinder span forces
that same nullity in every real H certificate. Therefore the universally
maximal lower rank is

    N* - 2^(c-1).

The upper rank is also N*-2^(c-1). Every maximum intersecting family is
exactly a cylinder of a core-cube maximum family. This follows from
the factor-only lower kernel, with empty petals testing base intersection.
At c=1 both endpoints are simple, both slacks have rank N*-1, and the
common-point star is the unique maximum family. The cases c=0 have
maximum families in either branch if a=b and only in the larger branch
if a>b, with the classical complementary-selector descriptions.

The same product theorem as PROOF.md, Section 6 applies to arbitrary
finite products of the petal-union factors here and the equal Boolean-cube
unions in PROOF.md, Section 5. With factor sizes N_j, stars s_j and forced lower nullities
nu_j, the universal maximal lower rank is

    N_product - sum_(j:s_j/N_j=max_k s_k/N_k) nu_j.

All their unit endpoints are simple and negative endpoint ratios are
below one. Thus maximum families are exactly the eligible-factor
cylinders, by the credited tensor-kernel and Boolean-additivity mechanism.
For the new unequal-cube factor nu_j is its larger star t; for two equal
cubes it is 2t. The product mechanism and classical family description
are not reclaimed as new.

## Exact evidence and limits

The checker constructs every literal core entry, validates the full seed
and repaired matrices against the original H/support/row/cap definitions,
checks their full rational PSD ranks, verifies kappa P-Q_cap>=0, and
checks the repaired gap beta/2. It compares the full matrix mixture with
a separate mixed-core lift. Nine unequal pairs include the u=1 boundary,
adjacent cube orders, and widely separated orders, through a65-by65
matrix. Two unequal common-core products are checked literally.
Actual finite pairs and all exact coefficients/hashes are in RESULTS.json.

The quantified theorem rests on the written complete pair-space and
frame decompositions and the supplied exact kernel/trace argument.
It is unformalized and not independently reviewed. No general cap
closure under unequal-star unions is asserted; arbitrary downsets and
three unequal Boolean petals remain outside this construction.
