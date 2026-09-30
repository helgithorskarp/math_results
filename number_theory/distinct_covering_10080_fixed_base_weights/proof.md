# Exact weight certificate and a necessary base-phase inequality

Actual author: **six-covering-1**, role **researcher**.

Put N = 10080 = 7B, with B = 1440. Let D be the divisors of N that are
at least 8. A distinct covering with moduli in D may use at most one
congruence for each label. There are 30 labels in D not divisible by 7,
which divide B, and 35 labels of the form 7k, where k is a divisor of B
other than 1. Missing labels may be adjoined arbitrarily without creating
holes, but the estimates below also apply directly to subsets.

The fixture lists one phase for every label in D. Its minimum is exactly
8 and its actual LCM is N. Direct evaluation of the congruence predicates
leaves 87 residues uncovered. Its base consists of the 30 specified
congruences with labels not divisible by 7. That base leaves 223 residues
of Z/BZ uncovered.

Let f : Z/BZ -> {0,1,2,3,4} be the vector in `certificate.json`, zero at
unlisted points. It has 76 nonzero entries. Direct integer calculation gives

    sum_z f(z) = 232,       max_z f(z) = 4.

Every point with positive weight is missed by the specified base. Lift
the vector to physical residues by F(x) = f(x mod B). Its total weight
on Z/NZ is 7*232 = 1624.

For k | B, k > 1, define

    K_k = max_{0 <= b < k} sum_{z mod B, z = b mod k} f(z).

A congruence x = a mod 7k contributes exactly the sum in this definition
with b = a mod k. Indeed, each z = b mod k has seven physical lifts
modulo N; because gcd(B,7) = 1, exactly one has the required residue
modulo 7. Hence every phase of label 7k contributes at most K_k,
regardless of its septary allocation. Exact calculation gives

    sum_{k | B, k > 1} K_k = 1463.

The checker verifies this total from ordinary physical predicates: for
each eligible tail label m, it sums F(x) into buckets x mod m and takes
the largest bucket. Thus it checks all 34391 physical tail phases without
relying on the preceding CRT derivation or an optimizer.

If the base phases are fixed at the fixture, they cover weight zero.
The weighted union of all tail congruences is at most 1463, even when
all 35 full phases are free. Consequently the uncovered weighted mass is
at least 1624 - 1463 = 161. Since an uncovered physical residue has weight
at most 4, the number of uncovered residues is at least

    ceil(161/4) = 41.

Omitting tail or specified base labels cannot invalidate this lower bound.
The fixture supplies an upper bound of 87 on this conditional minimum.
Neither endpoint is asserted to be the exact optimum.

More generally, allow the non7 phases to change as well. For a selected
base congruence x = a mod m, m | B, define its coefficient

    r_m(a) = sum_{z mod B, z = a mod m} f(z).

Let R be the sum of these coefficients over the selected base labels.
Their physical weighted union is at most 7R. The tails still contribute
at most 1463. Therefore every such assignment has at least

    ceil(max(0,161 - 7R)/4)

uncovered physical residues. In particular, any covering must have
7R >= 161 and thus R >= 23. The checker calculates all 4893 base-phase
coefficients by ordinary physical buckets and verifies their seven-fold
multiplicity. At the specified base every selected coefficient is zero.

This necessary inequality applies to distinct coverings whose moduli
are divisors of N and are at least 8; it does not require that their actual
LCM be exactly N. The fixture itself has minimum exactly 8 and actual
LCM N. The conditional obstruction and phase inequality do not exclude
all assignments at N, exclude period 15120, or determine L_min(8).

The certificate was discovered using a small floating LP and simplified
to integer weights 1 through 4. Only the resulting integer vector and
literal checker are proof inputs; no floating optimum, solver status, or
bounded search failure is a premise. Ordinary nonnegative weighted union
counting is established methodology, including in six-covering-2's work
on weighted residual resources. This is an explicit construction-family
certificate, not a new general counting principle.
