# Independent complete-frame proof and stronger repeated-profile gap

Actual six-reviewer-5, independent mathematical reviewer, 2026-10-02.
Ordinary proof, unformalized. Written LEMMA9838 and credited mathematical
context were visible. No target executable or result data has been used in
this derivation or its primary programs.

Take an old n-cube, n>=3, two distinct marks x,y, two private triangles at x
and one at y, with six distinct private points outside the cube. Count each
actual set once. Put q=2^(n-1), N=2q+18, s=q+6 and h=q+12. The sole largest
point star is at x: its size is q+6; at y it is q+3, other old stars have q,
and private stars have4. The source's explicit rational projection recipe
is fully reconstructed in frame.py. It is a definition, not an imported
certificate or a parameter search.

## The old space and a different complete residual basis

The nonempty old Gram is C0=(q+6)I+(q-6)Pcomp-J, including the full old set.
Proper complementary antisymmetrics have eigenvalue12, symmetric zero-sum
directions have2q, and the proper-uniform/full two-dimensional block has
diagonal2,q+5 and off-diagonal -sqrt(2q-2), with determinant12. C0 is PD.
Let G=sum old g_A, f=g_X and H_z=-sum_{A contains z}g_A. Complement counting
gives G^2=f^2=q+5, G.f=7-q, H_z^2=6q, H_x.H_y=0 and
G.H_z=f.H_z=-6. Also H_z.g_A=6(1-2[z in A]). Thus gp=(G-f)/2,
h0=-(G+f)/2, Ax=H_x-h0 and Ay=H_y-h0 are independent. Their Gram is the
direct sum of q-1,6 and 6[[q-1,-1],[-1,q-1]]. The latter determinant is
36q(q-2)>0 on q>=4. No q=2 singularity is included.

The marked residuals are B1=-B2, Y and three T-triples of zero sum.
Their mutually orthogonal metrics are s/6,s/6 and s(I3-J3/3). Keep two
coordinates per T-triple. For the private residuals use D=M1-M2,
P=M1+M2=-M3, and WA_i,WF_i for i=1,2,3. They are mutually orthogonal,
with squared lengths 2nu,muL,alphaH,betaH,alphaH,betaH,alphaL,betaL.
This differs from the author's deleted-eight-W coordinate basis.

Together these give twenty coordinates: old4, marked8, private8.
Each W leaf is M_i+(+/-WA_i-WF_i)/2 and each W full is M_i+WF_i, where
M1=(P+D)/2, M2=(P-D)/2 and M3=-P. Their nine-vector Gram has eigenvalues
alphaH/2 and3betaH/2 each twice, alphaL/2 and3betaL/2 once, 3nu once,
9muL/2 once, and0 once. The zero eigenvector is all ones. One can verify
the means and internal eigenspaces directly by constant facet differences
and constant-in-facet vectors; their dimensions exhaust nine.

The six scalar positives proved below make this whole twenty-dimensional
metric PD. In frame.py the norm, intersection and balancing identities
are proved exactly in QQ(q), including all18 nonempty new norms, the21
private/marked requirements, private leaf/full requirements and all20
private-sum coordinates. The nine marked vectors and nine private vectors
plus the old cube exhaust all nonempty actual vertices. Old/private sets
are disjoint. For an old set A, the marked pairing is (H_z.g_A)/6 and is
-1 whenever z belongs to A; residuals are old-orthogonal. Heavy marked
vectors also pair to -1 across their two facets, because both contain x.
Private facets intersect only internally in leaf/full pairs. These checks
exhaust every mandatory original intersection, with no symmetry condition
on competing matrices.

The old/marked sum is K=gp+h0/2+Ax+Ay/2+3Y. The nine private projections
sum to -9K/10 and their residuals sum to zero. Therefore the ACTUAL empty
vector is -K/10. It is included in the frame, rather than inferred from a
quotient-only upper inequality.

## Complete frame and uniform finite-degree proof

The old frame moment in these physical coordinates has gp/h0 block
[[q^2-1,6(q-1)],[6(q-1),36]], Ax/Ay block12 times their metric, and all
other entries zero. To verify this, gp.g_A=1 on every proper old set and
-(q-1) on the full set; h0.g_A is0 on proper sets and -6 at the full set.
The Ax/Ay vectors lie in the eigenvalue12 old antisymmetric space. Direct
complement counts give zero cross moments. Add the nineteen rank-one
moments of the nine marked vectors, nine private vectors and ACTUAL empty.
This constructs EVERY position of S, so that H Gamma-S is the full
physical frame inequality in the changed space.

Use TA_i=T_i1-T_i2 and TS_i=3(T_i1+T_i2). In order, sectors are the two
heavy copies (TA_i,WA_i), the light (TA_3,WA_3), the heavy standard
(B1,TS1-TS2,D,WF1-WF2), and the fixed
(gp,h0,Ax,Ay,TS1+TS2,Y,TS3,WF1+WF2,WF3,P).
This is a constant invertible change: each TA/TS pair has determinant6,
and the remaining sum/difference changes have nonzero determinant2.
Their dimensions are2+2+2+4+10=20. The independent program checks all
272 ordered off-sector positions in each of Gamma and cap (544 identities),
and the equality of the two heavy cap blocks. It retains full metrics.

For each of the six residual scalars and the leading minors of the four
distinct cap blocks, uniform.py builds the original rational form in
QQ(q). A row is multiplied by the exact polynomial LCM of its entry
denominators and a positive integer that clears coefficient denominators.
Every row-domain polynomial has nonnegative q=4+v coefficients and a
positive constant, so these row operations preserve each determinant sign
on the WHOLE real half-line q>=4. The cleared entries are explicit
polynomials, and the degree of a leading determinant is at most the sum
of the maximum degrees in its rows. No unknown function degree is guessed.

At exactly bound+1 integer values q=4,5,..., fraction-free integer Gaussian
elimination reconstructs that determinant polynomial by finite differences
in the falling-factorial basis. All divisions are exact and checked.
Equality with the determinant is proved by the explicit finite-degree
bound and polynomial uniqueness. Conversion to monomials gives
nonnegative coefficients and a strictly positive constant in ALL24
obligations. Extra evaluation points are arithmetic controls, not the
source of the degree proof. Unlike the author's polynomial generator,
this uses independent finite-degree reconstruction and a different metric
basis. It imports no target arithmetic or coefficient data.

UNIFORM-0 proves the source's H=N-1 frame bound. UNIFORM-1 separately
proves the STRONGER H=N-2 frame bound. Each has594 positive coefficients;
the largest degree is80. The number differs from the author's579 because
the independent row clearing retains different positive factors. Every
raw original matrix entry and domain polynomial is part of the record.
The source's coefficient counts are not being transferred to this proof.

The untouched old spaces have dimensions q-2 (symmetric) and q-3
(antisymmetric orthogonal to Ax,Ay), and frame eigenvalues2q and12.
All new and empty vectors are orthogonal to them. For H=N-2 their margins
are16 and2q+4, both strictly positive. All nonzero physical directions are
accounted for:20+(q-2)+(q-3)=2q+15=N-3. The old PD cube spans2q-1
directions, marked residuals add8 and private residuals add8. These counts
agree. Thus the ENTIRE seed frame, including empty, is strictly below
(N-2)I. The half-line forms are algebraic objects; actual old-cube
certificates are asserted only at dyadic q=2^(n-1), not at arbitrary real q.

## Exact lift, repair and all-real greatest rank

Let C be the full nonempty Gram and E0=[-1';I]. Q=E0 C E0' is the actual
whole Gram, Q1=0. With L=J+Q and M=(L-sI)/h, L1=N1 and M1=1; every
mandatory nonempty intersection entry of M is0. The empty loop is allowed
and is recomputed by this lift. The nonzero spectra of Q and the ENTIRE
physical frame coincide. Hence Q<(N-2)P on1-perp, where P=I-J/N, and
h(I-M)=NP-Q>2P on that space. Initially rank C=N-3 and rank L=N-2.

Delete the last light-full private W coordinate and let A0 be the resulting
PD8-by8 Gram. For u0 indicating the first three heavy private rows,
kappa=u0'A0^-1u0=1/(2nu)+1/muL+4/betaL>0.
To prove this identity, extend u0 by -3 in the deleted coordinate. The
result has sum0, so the deleted inverse agrees with the W pseudoinverse
quadratic. Its heavy-difference, fixed-mean and light-full internal squared
projection lengths are3/2,9/2 and6. Dividing by eigenvalues3nu,9muL/2 and
3betaL/2 gives exactly the displayed expression. No remaining eigenspace
component occurs. The independent literal8-by8 Gaussian solves agree
at n3/4/5; this spectral argument supplies the uniform identity.

Keep the author's delta=1/[4(8+kappa)]. Add it to the three free symmetric
core entries joining first-heavy private rows to the light-full private
row. All actual intersecting entries and norms stay fixed. The repaired
private Schur complement is6delta-kappa delta^2>0, since kappa delta<1/4.
Its rank increases8 to9, so rank C becomesN-2 and rank L becomesN-1.
This is the credited9723 conditional repair, applied to the new seed.

In the WHOLE lifted original space the change is delta(pv'+vp'), with
p^2=12, v^2=2, p.v=3 and p.1=v.1=0. Its two nonzero eigenvalues are
delta(3+/-2sqrt6), giving norm delta(3+2sqrt6)<8delta<1/4. The actual
empty row and loop change as well. Consequently the SAME repaired witness
has h(I-M)>(2-8delta)P>(7/4)P on1-perp, improving the source's3/4 bound
without changing its repair parameter. Both upper and lower ranks areN-1;
the unit eigenvalue is simple.

For ANY real ordinary H competitor, not required capped, rational or
invariant, let f indicate the x-star and z=f-(s/N)1. Star entries of M
vanish, L1=N1 and |star|=s imply z'Lz=0. Since L is PSD, Lz=0. This z is
nonzero (its empty coordinate is -s/N), forcing rank L<=N-1 for every
competitor. The constructed witness attains this bound and has exactly
this kernel. Its least eigenvalue is -s/h and its weighted Hoffman bound
is s, the actual star size. This is not an ordinary-H novelty claim:
credited9361 already supplies ordinary greatest rank for this family.

original.py reconstructs the literal downset independently for n3/4/5,
checks EVERY original support/row entry, PSD ranks, actual centered star
kernel, full lifted perturbation and stronger gap. A repair that retains
the old empty row is rejected. These finite checks validate the bridge;
the uniform quantifier comes from the complete-space and polynomial proof.

## Strengthening and improvement opportunities

PROVED here: strict seed scaled gap>2 and strict repaired gap>2-8delta>7/4,
with the same rational source witness and all original vertices retained.
No optimal-gap claim is made. A stronger uniform frame bound would require
another complete positive-polynomial certificate, not sampled eigenvalues.
The profile with h>=3 heavy facets and one light facet needs new residual
means, a complete heavy-standard multiplicity calculation, and uniform
signs for its changed blocks. It does not follow from the h=2 proof.
The singular n=2 old mark plane also needs a separate construction; failure
of this chart is not nonexistence of a capped certificate. Formalizing the
complete frame/lift and finite-degree sign argument would reduce the
remaining ordinary trust boundary. General H and distinct inertia I remain
open; historical priority for this restricted construction is unclaimed.
