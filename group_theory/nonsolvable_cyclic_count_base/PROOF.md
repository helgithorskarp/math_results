# The radical-free base at normalized cyclic count six

Author: Nova, studio-researcher-3, researcher, Colloquium 2026-10-05.
Version 2. Corrected source attribution; the exact-version internal check
is recorded separately with source hashes.

All groups are finite. Let c(G) count cyclic subgroups, including 1,
r(G)=omega(|G|), and eta(G)=c(G)/2^r(G).

**B6.** If Rad(G)=1, G is nonsolvable, and eta(G)<=6, then G is A5.

This file gives a finite route to B6. It imports CFSG, standard simple
group orders, exceptional small isomorphisms, and outer automorphism
orders. It neither reproves CFSG nor treats a software catalogue as a
proof of its own completeness. Section 2 makes the parameter reduction
explicit. The exact finite computation has an additional GAP trust
boundary, documented in SOURCES.md.

## 1. A self-contained classical order bound

For a subgroup H of X put m(H)=|H||C_X(H)| and let M=max_H m(H).
For any subgroups A,B,

    m(A)m(B) <= m(A intersection B) m(<A,B>).              (1)

Indeed |A||B|=|A intersection B||AB| and
|C(A)||C(B)|=|C(A) intersection C(B)||C(A)C(B)|.
The first intersection of centralizers is C(<A,B>), whereas
C(A)C(B) is contained in C(A intersection B). Also AB is contained
in <A,B>. Multiplying these two inequalities proves (1).

If A,B have measure M, both their intersection and join therefore
have measure M. Let D be the intersection of all subgroups attaining
M. There are finitely many, so D itself attains M. It is characteristic
in X, since automorphisms preserve subgroup size and centralizers.
Furthermore C(D) has measure at least M because C(C(D)) contains D;
hence it also attains M. By definition D<=C(D), so D is abelian.
When Rad(X)=1, this characteristic abelian subgroup is trivial. Thus
M=m(1)=|X|, and

    |H||C_X(H)| <= |X| for every H<=X.                    (2)

This is the classical Chermak--Delgado/Lucchini estimate. The proof
above reproduces it; it is not new content claimed by this campaign.

For H cyclic of order e, H<=C_X(H), so e<=sqrt(|X|). Since

    c(X)=sum_(x in X) 1/phi(o(x)),

and phi(e)<=e, it follows that c(X)>=sqrt(|X|). For every integer n,

    16^omega(n)/n <= product_(prime p<16) 16/p
                    = 8388608/15015 = gamma.             (3)

Each prime-power factor 16/p^a is at most 16/p for p<16 and at most
1 for p>=16. Consequently

    eta(X)^4 >= |X|/gamma,
    eta(X)<=6 ==> |X|<=ceil(gamma*6^4)=724052.            (4)

The exact rational before rounding is 3623878656/5005. This order bound
and its use in normalized-count finiteness are prior repository work.

## 2. Complete finite parameter range and automorphism primes

Import CFSG's nonabelian families, their standard order formulae,
the sporadic order table and exceptional small isomorphisms. Applying
(4) leaves these types, with duplicate isomorphisms removed:

* PSL(2,q): prime powers 4<=q<=113; identify q=4,5 with A5,
  q=7 with L3(2), and q=9 with A6.
* A7,A8,A9, in addition to the preceding alternating isomorphisms.
* PSL(3,q) and PSU(3,q), q=3,4,5.
* PSp(4,3)=PSU(4,2), and Sz(8).
* M11,M12,J1,M22,J2.

These give 53 isomorphism types. Both types of order 20160 (A8 and
PSL(3,4)) are retained. The following cutoff audit explains why no
other rank or field parameter is omitted. Bounds are intentionally
conservative; they use division by an upper bound for the center.

| Family | Cutoff beyond the retained range |
|---|---|
| Alternating | |A10|=1814400 |
| PSL(2,q) | q>=114 gives q(q^2-1)/2>724052 |
| PSL(3,q) | q>=7 gives at least 7^3(7^2-1)(7^3-1)/3=1876896 |
| PSU(3,q) | q>=7 gives at least 7^3(7^2-1)(7^3+1)/3=1887872 |
| PSL(4,q) | q>=3 gives at least 3^6(3^2-1)(3^3-1)(3^4-1)/4=3032640; PSL(4,2)=A8 |
| PSU(4,q) | q>=3 gives at least 3^6(3^2-1)(3^3+1)(3^4-1)/4=3265920; PSU(4,2)=PSp(4,3) |
| PSL(n,q), n>=5 | at least 2^10 product_(i=2..5)(2^i-1)/5=1999872 |
| PSU(n,q), n>=5 | at least 2^10 product_(i=2..5)(2^i-(-1)^i)/5=2737152 |
| Symplectic rank>=3; odd orthogonal rank>=3 | at least 2^9(2^2-1)(2^4-1)(2^6-1)/2=725760 |
| Symplectic rank 2 | q=4 has order 979200; q>=5 gives at least 4680000; q=2 has derived A6 |
| Even orthogonal rank>=4 | at least 2^12(2^4-1)(2^2-1)(2^4-1)(2^6-1)/4=43545600 |
| G2(q) | q>=3 gives at least 3^6(3^6-1)(3^2-1)=4245696; G2(2)'=PSU(3,3) |
| 3D4(q) | q=2 has order 211341312, and orders increase with q |
| F4,E6,2E6,E7,E8 | their q-power factors, even after division by their center bounds, already exceed 724052 at q=2 |
| 2B2(q) | after q=8 the next allowed q is 32, of order 32537600 |
| 2G2(q) | q=3 has derived PSL(2,8); the next allowed q is 27, already too large |
| 2F4(q) | 2F4(2)' has order 17971200; q>=8 is too large already from q^12 |
| Sporadic | all remaining 21 orders are at least |M23|=10200960 |

The classical order products are increasing with q. For ranks beyond
the displayed threshold, their numerator ratios exceed the growth of
the dividing rank/center bound, so the lower bounds persist for every
higher rank. Low orthogonal isomorphisms return to the linear, unitary
or symplectic rows; PSL(3,2)=PSL(2,7) is already retained. The field
value 6 is not a prime power. PSU(3,2) and the exceptional undereived
small groups are not additional nonabelian simple types.

For q=p^f, the outer orders used by catalogue.py are:

    PSL2: f*gcd(2,q-1),
    PSL3: 2f*gcd(3,q-1),
    PSU3: 2f*gcd(3,q+1).

A7,A8,A9 and PSp(4,3) have outer order 2; Sz(8) has outer order 3.
The sporadic outer orders in the retained list are 1,2,1,2,2 respectively.
The A6 isomorphism has outer order 4, as also given by the q=9 formula.
These are standard structural imports, independently compared with the
primary CTblLib maintainer's Order/Out catalogue. The live table declares
coverage through 10^9 and version 1.3.8; the actual permutation-group
computation below uses GAP 4.12.1 / PrimGrp 3.4.3 / SmallGrp 1.5.1.

Set a(S)=omega(|Aut(S)|)=omega(|S|*|Out(S)|). Exactly two retained rows
acquire a new prime from Out: Sz(8) acquires 3, and PSL(2,32) acquires 5.
The program retains these primes in the denominator. It generates the
family parameters explicitly and compares its 53-order multiset with
GAP's AllSmallNonabelianSimpleGroups. That comparison is corroboration;
the completeness argument is the CFSG/order/cutoff reduction above.

## 3. Finite simple-group margin

Applying (2) to a simple S gives c(S)>=sqrt(|S|). Therefore

    |S|>36*4^a(S) ==> c(S)>6*2^a(S).                     (5)

Exactly 37 rows clear (5). The remaining 16 exact counts are:

| S | c(S) | c(S)/2^a(S) |
|---|---:|---:|
| A5 | 32 | 4 |
| PSL(2,7) | 79 | 79/8 |
| A6 | 167 | 167/8 |
| PSL(2,8) | 156 | 39/2 |
| PSL(2,11) | 244 | 61/4 |
| PSL(2,13) | 366 | 183/8 |
| A7 | 947 | 947/16 |
| PSL(2,19) | 914 | 457/8 |
| PSL(2,16) | 784 | 49 |
| PSL(2,23) | 1566 | 783/8 |
| PSL(2,25) | 2082 | 1041/8 |
| M11 | 2576 | 161 |
| PSL(2,29) | 2554 | 1277/16 |
| Sz(8) | 6372 | 1593/8 |
| PSL(2,32) | 3040 | 95 |
| PSL(2,41) | 6808 | 851/4 |

GAP computes conjugacy classes of stored permutation representations,
then sums |class|/phi(order(representative)). The compact evidence retains
every class order and size. It is checked for class coverage, identity,
element-order divisibility and integrality. An alternate structural
calculation reproduces the full element-order histogram of every PSL2
row and of A5,A6,A7, not just their aggregate cyclic counts. For PSL2,
the split/nonsplit cyclic torus numbers are q(q+1)/2 and q(q-1)/2;
the nonidentity unipotent count is q^2-1. In odd characteristic the
involutions are accounted for separately, equivalently by the unique
involution of the even torus type. The reference implementation uses
the resulting histogram formula and the alternating cycle-type formula.
The rank-one counting formula is prior literature, not new content.

Thus every simple S in the finite range satisfies c(S)>=4*2^a(S), and
every such S other than A5 satisfies c(S)>6*2^a(S). M11 and Sz(8)'s
class computations still require the independent team check. Atlas may
replace their exact counts with independently justified lower bounds;
only the strict margin is needed for B6.

## 4. Socles and almost-simple overgroups

For coprime or noncoprime groups X,Y,

    c(X x Y)>=c(X)c(Y),                                  (6)

because phi(lcm(u,v))<=phi(u)phi(v) prime by prime. No coprimality
is needed for this inequality. Counts increase on passage to an overgroup.

Let Rad(G)=1 and eta(G)<=6. Its socle L is a product of nonabelian
simple groups S_i^m_i, with distinct isomorphism types and m_i>=1.
C_G(L)=1: any nontrivial normal centralizer would contain a minimal
normal subgroup inside L, and hence inside the center of L, which is
trivial. Conjugation embeds G in Aut(L), a product of wreath products
Aut(S_i) wr Sym(m_i). Put a_i=omega(|Aut(S_i)|),
b_i=omega(m_i!), and M=sum_i m_i. Then

    r(G)<=sum_i(a_i+b_i), b_i<=m_i-1,
    sum_i m_i a_i >= r(G),

using a_i>=1. Every S_i has order <=|G|<=724052, so section 3 gives
c(S_i)>=4*2^a_i. Formula (6) therefore yields

    eta(G)>=4^M.                                         (7)

If M>=2, this is at least 16, contradicting eta(G)<=6. Consequently
L=S is simple and S<=G<=Aut(S). Hence

    eta(G)>=c(S)/2^omega(|Aut(S)|).

Section 3 excludes S other than A5. For S=A5, Aut(S)=S5, so the only
overgroups are A5 and S5. Cycle-type counting gives c(S5)=67 and
eta(S5)=67/8>6. Therefore G=A5, proving B6 with the stated finite
classification and computation premises.

For completeness Aut(A5)=S5 can be seen from the five Sylow-2
subgroups of A5. Their permutation action is faithful on inner
automorphisms. Its kernel in Aut(A5) centralizes all inner
automorphisms (the two normal subgroups have trivial intersection),
and is therefore trivial because Z(A5)=1. This embeds Aut(A5) in S5.
Conjugation by S5 gives the reverse inclusion. The five Sylow-2
subgroups are the Klein-four groups of double transpositions fixing
each one of the five letters. A5's simplicity is classical background;
it can also be checked from the class sizes 1,15,20,12,12, since no
proper nontrivial union containing the identity has size dividing 60.
Its trivial center follows from nonabelian simplicity. Iris's
central-boundary artifact supplies direct proofs of perfectness and
trivial center, and is not cited here as a proof of simplicity.

## 5. Scope

This closes only the proposed radical-free interface B6, conditional on
the recorded classical classification/automorphism premises and exact
finite evidence. It does not classify extensions with solvable radicals;
Rowan, Iris and Atlas own those remaining interfaces and their checks.
The proof uses no threshold-4 strictness extrapolation and needs no
unbounded stronger simple-group theorem: all simple factors encountered
already lie in the finite order range. The socle transfer, classical
order estimate and finite simple counts are not claimed as historically
new. No standalone priority claim or external peer review is implied.
