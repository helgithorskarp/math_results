# The original singleton-to-bc fifth repair fails for every k>=5

Actual author: **six-downset-3**, role **researcher**. This is a complete
ordinary author proof with exact finite certificates; its analytic and
original-coordinate bridges are unformalized and the new leaf is
independently unreviewed.

## Original space and the quantified conclusion

Let the distinguished points be a,b,c and let W contain q outside points.
Let Z be ANY k-subset of W. The downset D contains the actual empty set,
every set of size at most two, and each triple containing at least two
distinguished points, except the k triples bcx with x in Z. Set

    N=(q²+13q+16)/2-k,   s=3q+4.

The maximum star is the a-star, with s members. The b/c stars have s-k
members and an outside star has q+6-indicator(x in Z) members. Below,
**k is any integer at least5 and q=2k**. Thus s is indeed the maximum and
N>s. Relabelling W sends any k-subset Z to the first k outside points, so
the canonical computations represent every Z, with no group-orbit omission.

Nonempty members form the original coordinate space of dimension N-1.
C0 has diagonal s-1, entry -1 on distinct intersecting members and entry
base(type(A),type(B))-1 on disjoint members. Delta is zero on diagonal and
intersecting pairs, and equals the corresponding slope on disjoint pairs.
The complete exact original base/slope table is the credited whole
[literal.py](credited-original/literal.py), not a Schur residual.

The symmetric proper repairs have entries

    R_b(a,b)=1, R_b(b,ac)=-1;
    R_c(a,c)=1, R_c(c,ab)=-1;
    B(b,c)=1;
    T(x,bc)=1 for EACH outside singleton x.

Their reversals have the same entries; all unlisted entries are zero.
Define, for unrestricted independent real parameters,

    C_rho=C0+kappa Delta+t_b R_b+t_c R_c+sigma B+rho T,
    U_rho=N I_(N-1)-J_(N-1)-C_rho.

**Claim. There is no real parameter tuple for which BOTH C_rho and U_rho
are positive semidefinite.** No greatest-rank, positive-kappa range or
equal-trade assumption is imposed. This is entire prescribed-face
nonexistence, not nonexistence for arbitrary H or uncapped H.

For the exact relationship with capped H, let E have first row -one'
and remaining rows I_(N-1), and put

    L=J_N+E C_rho E',   M=(L-s I_N)/(N-s).

E has full column rank, its range is one-perp, and E'one=0. Moreover

    N I_N-J_N=E(N I_(N-1)-J_(N-1))E'.

Consequently C_rho>=0 is equivalent to L>=0, and U_rho>=0 to N I_N-L>=0.
The support rule on intersecting proper members and their zero diagonals
follows from the original entries; the actual empty row completes all row
sums to one. The empty-set loop is retained. Thus the two inequalities are
exactly H plus the ADDITIONAL spectral cap M<=I in this affine face. This
decoding does not assume a fixed-space positivity or spectral-completeness
theorem, and no converse about arbitrary matrices is being claimed.

The fifth repair has rank2 and original eigenvalues +/-sqrt(q): it is
u e_bc'+e_bc u', where u indicates all q outside singletons. These vectors
are orthogonal, with norms sqrt(q),1. It is supported on proper disjoint
pairs, preserves proper diagonals, and kills the original maximum a-star.
It is therefore a legitimate additional repair, despite the obstruction.

## The original constant dual and the two-dimensional determinant

The credited original scalar dual from10222 uses member values:

* zeta is1 on outside-only members, -1 at abc, zero elsewhere.
* y is0 on outside-only members and bc/bcx; it is0 at a,ab,ac;1 at b,c;
  1/2 at ax and abc;3/4 at bx,cx; -1/4 at abx,acx.
* v=2one-e_b-e_c, so its values are1 at b,c and2 elsewhere.

These are values at EACH original member, not coordinates of orthonormal
orbit vectors. On q=2k, the exact original energies are

    zeta'C_rho zeta=kappa alpha,
    y'C_rho y+v'U_rho v=A-kappa d-8q rho,

where

    H=6k+5, h=1/H,
    alpha=q(q+1)/2+3(q+1)/(3q+5)
         =(12k³+16k²+11k+3)/H >0,
    d=2q(q+1)+4(3q+1-2k)/(3q+5)
     =(48k³+64k²+36k+4)/H >0,
    A=-8k²+55k+121/4.

Both independent trades and sigma cancel separately. For the new repair,
y'Ty=0, v'Tv=8q and zeta'Tzeta=0, by direct singleton counts. Therefore
C_rho>=0 forces kappa>=0 even after adding rho T.

Let e=e_bc, the proper original unit coordinate. Direct table counts give

    zeta'C_rho e=kappa h+q rho,   e'C_rho e=s-1.

For clarity, zeta'C0 e=0 because all q outside singletons contribute -1
in total, outside pairs contribute0, and the abc term contributes+1.
For Delta, the outside singleton slope is0; the outside-pair slope is
2/[q(q-1)(3q+5)], and there are q(q-1)/2 pairs. The result is h. Both
trades and B have zero cross terms and zero bc diagonal. The T cross is q
and its diagonal zero. These are all-variable original-member identities.

For k>=8, A<0: four times A translated by8 has coefficients
[-167,-292,-32]. Put b0=-A/8>0 and beta=d/8-h. Its numerator is

    beta=(12k³+16k²+9k-1)/(2H)>0.

At k=8+x this numerator has coefficients [7239,2569,304,12]. If kappa=0,
the zeta/e determinant forces rho=0, contradicting A<0. For kappa>0, the
original two-plane inequality and lower determinant imply

    q rho <= -b0-kappa d/8,
    (kappa h+q rho)² <= kappa alpha(s-1).

The cross term is at most -b0-kappa beta<0, so

    (b0+kappa beta)² <= kappa alpha(s-1).

Since (b0-kappa beta)²>=0, a necessary consequence is

    4b0 beta <= alpha(s-1).

This is an exact two-dimensional PSD/AMGM argument, not a numerical
condition or an assumption that a necessary condition is sufficient.

Set eta=alpha(s-1)+(A/2)beta. Its positive clearing gives the full identity

    16(6k+5)eta=
    23+1685k+5772k²+6796k³+3280k⁴-384k⁵.

The ENTIRE coefficient list at k=11+x is

    [-4058658,-8052383,-2499720,-313524,-17840,-384].

Every coefficient is negative, hence eta<0 for all real k>=11. The
necessary condition is impossible. This proves the claimed absence for
every integer k>=11, without bounded enumeration or an asymptotic gap.

## Exact original certificates at k=5,...,10

[CERTIFICATE.json](CERTIFICATE.json) supplies, for each of these six
points, two complete rational physical vectors l,u with positive endpoint
weights1,1. Their exact identity is

    l'C_rho l+u'U_rho u = a_k+b_k kappa,

with a_k<0 and b_k<0. Each t_b, t_c, sigma and rho coefficient is exactly
zero. Since orientation requires kappa>=0, both positive semidefinite
forms would have nonnegative left side and negative right side, a
contradiction. Values of the negative coefficients are:

|k|a_k|b_k|
|--|--|--|
|5|-47704168872089/2267321204736|-631743589/8413511680|
|6|-9700247939325/197940740096|-3973796047/61950918656|
|7|-427606970604961/5146459242496|-619356421/71016906752|
|8|-172202989268317/1403579793408|-260308329639/946434211840|
|9|-102345373459375/611816833024|-14939199755/17221943296|
|10|-628803011664919/2906129956864|-453730519123/288394575872|

The independent checker enumerates the complete actual original carrier,
including empty, at every finite point, and all ordered nonempty-member
pairs. It reconstructs all seven physical forms by integer pair counts and
the complete literal table. An independent binomial-count representation
must match every one of 6*7*23² positions. No matching aggregate count is
substituted for full coefficient comparison. All original maximum-star
sizes, T support and T star action are checked. It then checks BOTH entire
affine endpoint planes and their sum, not merely a scalar value of a
numerically proposed parameter tuple.

Combining this finite proof with the uniform determinant proof yields
every integer k>=5. Failure of the reused certificate search at k2..4
has no mathematical implication about that face.

## Evidence, ordinary bridges and credit

The symbolic polynomial check reconstructs alpha,d,beta from their
original formulas, expands eta independently and uses a separate Horner
translation to check every coefficient. Ten exact binomial-count controls
at k8..17 bind all original scalar components, with positive clearing
4q(q-1)(q-2)(q-3)(3q+5). Original cleared table entries have degree<=5;
full physical entries have degree<=9 by the explicit size-at-most-two
binomial factors. These controls validate the ordinary all-variable
counts; the direct cross-term counts and polynomial signs above constitute
the universal argument. No old q>=3k positivity/Schur bridge is applied on
q=2k, and no full positivity premise is needed for a necessary-vector dual.

The defining input is credited9826's original affine table, available in
[the original definition source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-six-cutoff/PROOF.md),
source commit d2d8a094e389a51668026b7646d046c50c91eff0. The entire copied
literal executable is pinned by SHA256
46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39;
its historical finite-domain helper is unused. The original constant scalar
dual is credited10222,
[the all-count four-repair proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/all-count-repair-classification/PROOF.md),
source commit f0a7e23f66884531a65f97cf4368ad0873f1cbc9. We extend its affine
face; neither its classification nor its review status answers this new
five-parameter question. The new finite vector certificates and determinant
obstruction are the current mathematical contribution.

During the prepublication refresh, independent REVIEW10228 became committed:
[the low-count audit and spectral separation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/low-count-original-dual-audit/REVIEW.md),
source commit dcf7428c31d4d585dcc334152da700d80fd0e9ea. It confirms the
credited four-repair low-count scalar leaf relative to its original table,
retaining the k7 and q>=3k positive classification as explicit premises.
Its quantitative separation does not exclude an extra repair. The present
five-parameter leaf is new and independently UNREVIEWED; that earlier
verdict and margin are not transported to it.

The problem source is Ellis--Filmus--Friedgut,
[Spectral Chvatal Conjecture H, Section4](https://arxiv.org/html/2609.28404v1#S4).
The arXiv primary version was live rechecked on2026-10-04: v1 remains the
listed version. General H/I, arbitrary support-changing repairs, uncapped
H and unrestricted cap-face classification are not resolved here. No
historical priority claim is made from a targeted literature refresh.

The complete source manifest is checked before importing mathematical
modules. Supplied/generated certificates remain untrusted until fully
decoded. Correct mathematical interpretation of original counts, empty
lift and the real PSD determinant argument is ordinary and unformalized;
the code is not a proof-assistant theorem. A single floating discovery
pilot was useful to find small rational finite duals; it contributes no
certificate soundness premise. No independent-person verdict is claimed.
