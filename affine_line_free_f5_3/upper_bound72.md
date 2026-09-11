# No 73-point line-free set in F_5^3

**Theorem.** Every subset of F_5^3 containing no complete affine line has at
most 72 points. Consequently

\[
70\le r_5(\mathbb F_5^3)\le72.
\]

Equivalently, every point set meeting every affine line in AG(3,5) has at
least 53 points. The known 55-point blocking set is the complement of the
known 70-point line-free set.

We use the published bound r_5(F_5^3)<=73 of Elsholtz et al., Theorem 1.5,
and the classification and support theorems of Kurz–Landjev–Rousseva [KLR].
Precise sources and replay instructions are in the README. Our small exact
checks do not re-prove the imported classification.

## 1. Reduction and spectrum identities

Assume S is a line-free 73-set. Write a_j for the number of affine planes
meeting S in j points. Every plane has size at most 16; its four parallel
companions imply size at least 9. There is no 12-plane: a 12-set in AG(2,5)
contains a line with at least four points, whose six-plane pencil would
give 73+5*4<=12+5*16, or 93<=92. The two planar facts used here are checked
by complete labelled enumeration in `plane_caps.cpp`.

The following identities and reduction were established in [proof.md](proof.md).
They are recalled to specify the complete scope used below. Counting pairs
in all affine planes gives

\[
\sum_j\binom j2a_j=6\binom{73}{2}=15768.\tag{1}
\]

For the counts a=a_9 and b=a_10 of parallel profiles (9,16,16,16,16) and
(10,15,16,16,16), the complete integer profile list gives 5a+2b>=41.
In particular a+b>=9.

Complete to PG(3,5) with empty plane H_infinity. On dual points (primal
planes) put

\[
K(H)=(16-|S\cap H|)\bmod5\in\{0,1,2,3\}.
\]

The plane-pencil identity
\(\sum_{H\supset\ell}|S\cap H|=73+5|S\cap\ell|\)
shows that K is a strong (3 mod 5)-arc: every line has total multiplicity
congruent to 3 modulo 5. The point Q_infinity dual to H_infinity has
multiplicity one. Put u=a_9, v=a_10, w=a_11 and L=u+v+w. Summing deficits
over all 156 projective planes gives

\[
|K|=218-5L\le173.\tag{2}
\]

Let lambda_i count dual points of multiplicity i. Then

\[
a_{16}=\lambda_0-w,\quad a_{15}=\lambda_1-1-v,\quad
a_{14}=\lambda_2-u,\quad a_{13}=\lambda_3.\tag{3}
\]

The minus one removes Q_infinity. With

\[
B=120\lambda_0+105(\lambda_1-1)+91\lambda_2+78\lambda_3,
\]

(1) becomes B-55u-60v-65w=15768. Therefore

\[
2u+v=13L-\frac{B-15768}{5}.\tag{4}
\]

A dual line of type A2 has point multiplicities (2,1,0,0,0,0).
Every 9-plane belongs to a distinct parallel class with four 16-planes.
Together with H_infinity, that class becomes an A2 line through Q_infinity.
Thus

\[
u\le\#\{\text{A2 lines through }Q_\infty\}.\tag{5}
\]

The low-cardinality classification [KLR, Theorem 5.2] says that K is lifted,
has a full plane in its support, or is one of the exceptional arcs of sizes
128,143,168. The latter two have no multiplicity-two points. Then u=0,
5a+2b>=41 forces v>=21, and (2) gives |K|<=113, excluding both.
We now close every remaining alternative.

## 2. The exceptional 128 arc is impossible

Its multiplicity spectrum is (lambda_0,lambda_1,lambda_2,lambda_3)
=(80,40,20,16), and (2) gives L=18. Equation (4) gives 2u+v=35.
Nonnegativity of v and w=18-u-v forces

\[
(u,v,w)=(17,1,0),\qquad
(a_9,a_{10},a_{11},a_{13},a_{14},a_{15},a_{16})
=(17,1,0,16,3,38,80).\tag{6}
\]

But every multiplicity-one point of this exceptional arc is on exactly
six A2 lines [KLR, Theorem 5.2]. This contradicts (5), which requires
at least seventeen.

`exceptional128.json` transcribes the matrix displayed in that theorem.
The checker constructs the 156 projective points and 806 lines directly,
verifies the strong-arc condition, the full point and plane spectra, and
the absence of a full plane in its support. Cardinality modulo 25 rules
out lifting. Hence the published uniqueness theorem identifies the checked
configuration with the required exceptional type. All forty possible
choices of Q_infinity are checked separately: each has six A2 lines. No
transitivity or unproved automorphism reduction is used.

## 3. Every lifted possibility is impossible or has full-plane support

In a lifted arc K, the lifting vertex has multiplicity three and each base
point is replaced by five points of its multiplicity. If the base has size m
and multiplicity spectrum (n_0,n_1,n_2,n_3), then

\[
|K|=5m+3,\quad \lambda=(5n_0,5n_1,5n_2,5n_3+1),\quad L=43-m.\tag{7}
\]

The base is a strong planar (3 mod 5)-arc. Its 31 lines have weights at
least three, giving 6m>=93. Its size is 3 modulo 5, and (2) gives m<=34.
Thus m is 18,23,28 or 33. We use the complete spectra in [KLR, Tables 4–7].

**Size 18.** Each of the four base types contains a full line in its support.
Table 4 lists, respectively, a B8, B5, B5 or D1 line, with patterns
(2,2,1,1,1,1), (3,1,1,1,1,1), or (3,3,3,3,3,3).
The plane joining that line to the lifting vertex is fully supported.
These cases belong to Section 4 below.

**Size 23.** The unique base type has spectrum (18,6,4,3). Its possible line
types are A1, A2, A3, B2, B3. At a multiplicity-one point only A2, A3, B2,
B3 occur; their patterns are

\[
(2,1,0,0,0,0),\ (1,1,1,0,0,0),\
(3,3,1,1,0,0),\ (3,2,2,1,0,0).
\]

Let their counts there be x,y,z,t. Count all multiplicity-three points,
all multiplicity-two points, all other multiplicity-one points, and the
six lines through the point:

\[
2z+t=3,\quad x+2t=4,\quad2y+z=5,\quad x+y+z+t=6.
\]

The unique nonnegative solution is (x,y,z,t)=(2,2,1,1).
For any multiplicity-one point Q in the lift, the line joining it to the
lifting vertex has type B5. Each base line through its projection gives
five other lines through Q, with the same type as that base line. Hence Q
is on exactly 5*2=10 A2 lines.

On the other hand, (7) gives lambda=(90,30,20,16), L=20, and (4) gives
2u+v=31. Since u+v+w=20, we have u>=11. This contradicts (5) at every
possible Q_infinity, excluding the whole size-23 base case.

**Size 28.** The base spectrum is (15,10,0,6). There is no multiplicity-two
point in its lift, which has size 143; the bound |K|<=113 established in
Section 1 rules it out. Equivalently, (4) gives 2u+v=36 while L=15.

**Size 33.** Table 7 has ten isomorphism types and the following six distinct
point spectra. In each case L=10 and 2u+v<=2L=20, contradicting (4):

| Base spectrum (n_0,n_1,n_2,n_3) | Isomorphism types | Required 2u+v |
| --- | ---: | ---: |
| (10,15,0,6) | 1 | 46 |
| (11,12,3,5) | 1 | 46 |
| (12,9,6,4) | 4 | 46 |
| (13,6,9,3) | 1 | 46 |
| (15,5,5,6) | 2 | 41 |
| (18,1,4,8) | 1 | 36 |

`check_lifted.py` checks every spectrum and every small integer identity.
The completeness of the listed types remains an explicit dependency on
the published classification, rather than on these arithmetic checks.

## 4. Full-plane support is impossible

It remains to exclude K with a full dual plane in its support. Let P be the
corresponding primal point. Every primal plane through P has size at most 15,
because a 16-plane would have K=0. The six-plane pencil identity forces
every line through P to contain at most three points of S.
If P is affine and belongs to S, the 31 lines through P give
73<=1+31*2=63, a contradiction. If P is affine and outside S, adjoining it
gives a line-free 74-set, contrary to the published upper bound 73.
Thus P lies on H_infinity.

The 25 parallel affine lines in direction P have sizes at most three and
total 73. Their deficits from three sum to two. Every affine plane parallel
to P is a union of five such lines, so its intersection with S has size
13,14 or 15.

Adjoin P to obtain a projective set A=S union {P} of size 74. Every plane
still contains at most 16 points, and H_infinity contains exactly P.
The planes through P other than H_infinity have sizes 14,15 or 16.
The other planes have S-section sizes 9 through 16, excluding 12. Size 13
is also impossible for these planes: a four-point line in such a section
would have an A-pencil sum at least 74+5*4=94 but at most 13+5*16=93.
The existence of a four-point line follows from the same planar 12-subset
bound. Therefore the complete list of plane sizes in A is contained in

\[
\{1,9,10,11,14,15,16\}.\tag{8}
\]

Define another dual multiplicity

\[
J(H)=(16-|A\cap H|)\bmod5\in\{0,1,2\}.
\]

For every dual line its sum is 96-74=2 modulo 5, by the pencil identity.
Thus J is a strong (2 mod 5)-arc in PG(3,5). Theorem 3.9 of [KLR] implies
that **J has a full plane in its support**. Let Q be the corresponding primal
point. Since J(H_infinity)=(16-1) mod5=0, that supported plane cannot contain
the dual point H_infinity. Equivalently, **Q is affine**.

Every primal plane through Q contains at most 15 points of A. The point Q
cannot already belong to A: if it did, summing the 31 plane sizes through Q
would give 6*74+25=469, greater than 31*15=465. Thus adjoining Q produces
a projective 75-set A union {Q} whose plane sizes remain at most 16.

Its affine subset T=S union {Q} has size 74 and also has every affine plane
of size at most 16. If T contained a full affine line, its six-plane pencil
would give 74+5*5=99<=6*16=96, a contradiction. Hence T is a line-free 74-set,
contrary to the known bound. This excludes full-plane support.

All alternatives for S have now been excluded. There is no line-free
73-set, and the published upper bound 73 implies r_5(F_5^3)<=72. The
published, directly checked 70-point set supplies the lower bound. QED.

## Scope and evidence

The argument is global and uses no restriction on a seed, automorphism
group, repair radius or coordinate profile. No solver result is a premise.
The sparse-fiber CNF probes were stopped when the argument in Section 4
made them unnecessary; their incomplete traces prove nothing.

The exact finite checks cover the planar facts, the projective incidence
identities, all forty exceptional marked points, all lifted spectra and
the displayed integer obstructions. The remaining mathematical trust
boundary consists of the written reductions, ordinary finite geometry,
the cited classification and support theorem, and the existing bound 73.
This is not a proof-assistant formalization or an independent re-proof of
the imported classification.

The existence questions at 71 and 72 are still open in this work. No
73-point profile or dual classification is automatically valid at 72.
