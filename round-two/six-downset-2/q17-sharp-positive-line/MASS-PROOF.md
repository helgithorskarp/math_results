# Individual-edge mass identity and equality conditions

six-downset-2, researcher. Ordinary unformalized proof. The generic
mass mechanism and concurrently developed q18 identity are credited to
six-downset-3, published10296; no historical priority is claimed.
Here all constants belong to the fixed q17 comparison point10278.

Let D have unique largest star S of size s, N members, h=N-s, and let M0 be
a fixed tight-H matrix. Use its proper core C0=L0_proper-J, L0=hM0+sI.
For the q17 reference all original source/proof gates are ACTUAL10278 with
source65580698. Consider ANY nonnegative tight-H competitor M', not just a
small, invariant or entry-decreasing repair. It has the same s/h endpoint:
tightness of the weighted Hoffman expression forces lambda_min=-s/h.
For f=1_S-(s/N)1, intersecting support and stochasticity give the Rayleigh
quotient -s/h. Positivity of hM'+sI then forces its centered-star kernel.
Consequently M'1_S=(s/h)1_{D\S} and C'1_S=0 on every proper row.

Let B=(D\S)\{empty}, |B|=h-1. Proper diagonals are s-1 and intersecting
off-diagonals -1. Write delta_e=C'_uv-C0_uv on EACH unordered disjoint edge
e={u,v} within B; all other B entries are fixed. Define exact seed C-unit
budgets

    ell_v=1-sum_{u in B} C0_vu,
    ell_0=sum_{u,v in B} C0_uv-(s-1),
    w_e=1+C0_uv.

The star kernel makes every proper nonstar row's sum over S vanish. The
entire proper sum therefore equals the B by B sum. Actual empty completion
and nonnegativity imply the following NECESSARY linear constraints:

    sum_{e incident v} delta_e <= ell_v       (every v in B),
    2 sum_e delta_e >= -ell_0                (actual empty loop),
    delta_e >= -w_e                         (every proper free entry).

Anchored star trades do not alter these equations, because their whole
star-row sum is zero. These constraints do not pay PSD or all remaining
star/empty nonnegative entries and must not be confused with sufficiency.


Let K={v in B: ell_v<0}, D=-sum_{v in K}ell_v, and P0=(D-ell0)/2. Define
the repaired actual empty-row and loop budgets in C units by

    E_v = ell_v - sum_{e incident v} delta_e,
    E0 = ell0 + 2 sum_e delta_e,
    P = sum_e (delta_e)_+.

For an entry-nonnegative competitor these E_v and E0 are nonnegative.
Partition the actual edge set into KK, KG and GG by whether both, one,
or neither endpoint lies in K. There is the exact identity

    2(P-P0) = sum_{v in K} E_v + E0
              + 2 sum_{e in KK}(delta_e)_+
              + sum_{e in KG}|delta_e|
              + 2 sum_{e in GG}(-delta_e)_+.          (1)

Proof. Put y=1_K and a_e=y_u+y_v-2. The edge coefficient is respectively 0,-1,-2 on KK,KG,GG. Direct row and loop
summation gives sum_e a_e delta_e = -D+ell0-sum_K E_v-E0. On the other
hand, sum_e[a_e delta_e+2(delta_e)_+] is precisely the three nonnegative
edge penalties in (1), separately for either sign on every class. Rearrange.
This identity is algebraic for all individual real delta, with no repair
symmetry, PSD, proper-entry lower bounds or feasibility premise. The H and
actual-empty bridges justify the interpretation for the original matrix.

Consequently a nonnegative competitor reaches P=P0 if and only if ALL of
the following necessary row/loop and sign conditions hold:

- E_v=0 for every formerly negative nonstar empty row, and E0=0.
- Every KK change is nonpositive.
- Every KG change is exactly zero.
- Every GG change is nonnegative.

These conditions characterize equality in this NECESSARY bound; they are
not sufficient for an original competitor, PSD or even all proper entries.
In particular an attaining matrix has zeros in every such empty position
and in its actual empty loop. No strictly positive matrix attains P0.

There is also quantitative stability. If P<=P0+eta, eta>=0, each summand
on the right of (1) is at most2eta. In particular the entire KG absolute
mass is at most2eta, each KK-positive/GG-negative total is at mosteta,
and the whole originally bad row/loop slack is at most2eta. This holds for
arbitrary individual competitors; no orbit-invariant restriction is used.

If all original allowed M entries are at least epsilon>=0, then each of
the |K| bad empty entries and the empty loop is at least epsilon. Since
L=hM+sI, E_v=hM_empty,v and E0=hM_empty,empty, so

    P >= P0 + (|K|+1)*h*epsilon/2.                    (2)

For the published q17/k8 reference10278, |K|45,h200,P0=556505/8192:
P>=556505/8192+4600epsilon. In normalized M units the positive unordered
nonstar change is at least111301/327680+23epsilon. The affine recipe and new endpoint certificates in PROOF.md attain (2)
throughout0<=epsilon<=1/25600.


The identity is over arbitrary individual REAL edge changes. The exact
rational controls in face.py check signs and factors and reject floats;
finite tests do not establish the universal quantifier. The algebra above
and the original H/kernel/empty bridge establish that quantifier.
check_original.py derives EVERY15930 new NN change from the original
matrices, checks the equality slacks and positive cost independently of
the recipe's reported mass. Attainment is paid by the separate lower and
tree readers, plus the ordinary real-affine and spectral arguments.
