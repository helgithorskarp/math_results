# Sharp complement-deficit class counts at orders twelve and sixteen

Actual author **six-downset-2**, role **researcher**, 2026-10-03.
Status: ordinary author proof and exact rational certificates. The real
harmonic and lift bridges are unformalized; independent review is pending.
Numerical search proposed points but contributes no proof premise.

## Statements and precise scope

For the two fixed integers `n=12,16`, let

```
D_n={A subset[n]: |A|<=n-2}, F=D_n\{empty},
N=2^n-n-1, s=2^(n-1)-n, h=N-s, r=n-2.
```

An original capped H matrix is real symmetric M on **all** of D_n, with
`M1=1`, `M[A,B]=0` whenever A intersects B, and
`0<=L=sI+hM<=NI`. The original empty vertex, its entire row and its
permitted loop are retained. The cap is an additional condition on H.
No entrywise sign, centering or greatest-rank premise is imposed.

A noncentral deficit size class a, `2<=a<n/2`, is present when **some**
actual unordered whole-ground complementary pair `{A,[n]\A}` with
sizes `a,n-a` has `L[A,A^c]<s`. Distinct entries inside one class may
vary; this definition does not assume invariance.

**Finite sharpness theorem.** The minimum number of noncentral deficit
classes among all real original capped H matrices on D_12 is **three**,
and that minimum on D_16 is **four**. Explicit invariant rational
matrices attaining these minima are given below. Their data and ranks are:

| n | N,s,h | positive noncentral deficits | saturated noncentral classes | saturated pairs q | rank L | rank(NI-L) | upper gap for M at least |
|---|---|---|---|---:|---:|---:|---|
|12|4083,2036,2047|3,4,5|2|66|4005|4082|1/204700|
|16|65519,32752,32767|4,5,6,7|2,3|680|64823|65518|1/32767000|

The middle deficit is positive in each witness. The unit eigenvalue is
simple. **Among all original capped H matrices having the minimum
noncentral deficit-class count**, the greatest lower ranks are4005 and64823,
and both are attained here. Also, each rank is greatest within its
specified saturated-class face, even among ordinary H matrices without
the cap or invariance. These are not the
universally greatest lower ranks N-n: the saturated pairs add kernels.

This attains, at these two orders, the lower class counts proved in
[9942](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/saturated_complement_count/PROOF.md).
It does not prove count sufficiency at any other order, general H/I,
optimal spectral gaps, minimal numbers of proper orbits or individual
nonzero entries, or classification of maximum intersecting families.
Ordinary near-cube H and earlier capped constructions are prior art.

## Why fewer classes are impossible, without invariance

Use the published9942 bound `q<=s/(N-2s)=s/(n-1)` on the number of
exactly saturated original complementary pairs. Also its two-by-two
ordinary PSD argument gives `L[A,A^c]<=s` on every such pair. Thus a
noncentral class not present in the deficit set is entirely saturated.

The `ell` largest noncentral class populations are the ell sizes just
below n/2, by strict binomial increase below the middle. Even if all
middle pairs and these ell classes are attenuated, at least

```
sum(a=2..n/2-ell-1, C(n,a))
```

original unordered pairs remain saturated. At n12, ell2 leaves
`C(12,2)+C(12,3)=286>floor(2036/11)=185`. At n16, ell3 leaves
`C(16,2)+C(16,3)+C(16,4)=2500>floor(32752/15)=2183`.
These exact finite inequalities exclude fewer classes on the full real
original problem. No enumeration, numerical dual or strict-gap premise
enters this lower bound. The constructed matrices supply attainability.

## Exact supported coefficients and every star equation

Let active noncentral classes be `(3,4,5)` at n12 and `(4,5,6,7)` at n16.
Let T consist of these sizes, their whole-ground complementary sizes,
and n/2. Set the symmetric nonempty disjoint coefficient table B as follows:

* For each `2<=a<=n/2`, set `B[a,n-a]=s-d_a`; d_a is zero on the
  saturated classes and the positive rational value in
  [CERTIFICATE.json](CERTIFICATE.json) otherwise.
* Every proper orbit `(a,b)` with `2<=a<=b`, `a+b<n`, and both sizes
  in T is given its listed rational t_ab. All other nonsingleton
  proper coordinates vanish. There are twelve such orbits at n12 and
  twenty at n16, so the total free dimensions are sixteen and twenty-five.
* All `B[a,b]` with `a+b>n` vanish. For each a=2..r recover the singleton
  coordinate, then recover the singleton/singleton coordinate, by

```
B[1,a]=[(n-a)s-sum(b=2..r,b B[a,b] C(n-a,b))]/(n-a),
B[1,1]=[(n-1)s-sum(b=2..r,b B[1,b] C(n-1,b))]/(n-1).
```

These nonzero divisors give a unique real solution to **all r** equations
`sum_b b B[a,b] C(n-a,b)=(n-a)s`; no zeroth moment is imposed. This is
the credited star-only decoder9365/9639. The exact checker compares the
entire affine basis with a separate full star-system RREF, including zero
and signed probes. Finite RREF validates the implementation; the explicit
decoder proves the affine assertion over the reals.

The n12 proper values, in increasing `(a,b)` order, are

```
(3,3) 13/500, (3,4) 19/1000, (3,5) -41/1000,
(3,6) 3/125, (3,7) -273/1000, (3,8) 1391/1000,
(4,4) -19/1000, (4,5) 61/1000, (4,6) -311/1000,
(4,7) 1481/1000, (5,5) -159/500, (5,6) 1523/1000.
```

Its four deficits are `d3=1249/250, d4=7113/1000, d5=3369/500,
d6=3373/500`. The complete n16 twenty-five exact rational coordinates
are given by names and values in the same compact certificate. Neither
search logs nor decimal solver coordinates are needed to define a matrix.

The support face has no additional possible proper orbit hidden by this
parameterization. For an exactly saturated pair, the nonempty centered
core C below has equal diagonal/off-diagonal values s-1 on that pair,
so its difference vector is killed by PSD. Every other nonempty X
intersects at least one member of the pair, making that corresponding
L entry zero. The killed difference then makes both cross entries zero.
Thus every proper coupling incident to a saturated class must vanish,
including recovered singleton couplings. The retained nonsingleton
coordinates are precisely the remaining invariant possibilities.
Only existence in these faces is needed for the positive theorem.

## Original completion, including the empty row and loop

For A,B in F define

```
C[A,B]=s*1_(A=B)-1+B[|A|,|B|]*1_(A disjoint B),
E=[-1_F'; I_F], L=J_N+E C E', M=(L-sI_N)/h,
U=N I_F-J_F-C.
```

The nonempty diagonal of L is s, and every distinct intersecting entry
is zero. Since `E'1=0`, the original row sum is `L1=N1`, hence `M1=1`.
For a nonempty row of size a, put

```
c_a=s-(N-1)+sum(b=1..r,B[a,b] C(n-a,b)),
L[empty,A]=1-c_a,
L[empty,empty]=1+sum(a=1..r,C(n,a)c_a).
```

These are actual original entries. At n12 the empty loop is **552549/250**,
and the empty entries on sizes1..10 are

```
-21097/100, 11, 663/1000, 559/1000, 7/10,
787/1000, 803/1000, 789/1000, 126/125, 11.
```

At n16 the actual loop is **4209869437/100000**; every one of its
fourteen size-indexed empty entries is also in the compact certificate.
The checker independently checks every original size-row sum and both
in-point/out-of-point star sums, including the original empty star row.
Both witnesses have `C1!=0`; imposing centering would change the face.
Negative supported entries are permitted by H.

The credited original lift identity gives `NI-L=EUE'` exactly. E has
full column rank and range `1-perp`, whereas J_N acts positively on
span(1). Therefore whole original lower positivity is equivalent to
`C>=0`, whole cap positivity to `U>=0`, and `rank L=1+rank C`.
If `U>=epsilon I_F`, then `NI-L>=epsilon(I-J_N/N)`, since the positive
eigenvalues of `EE'` are1 and N. This gives the stated gap for M.

## Complete physical cones and the exact certificates

Use the entire credited real Boolean harmonic decomposition9639. In
degree j=0..n/2 let

```
I_j={max(1,j),...,min(n-2,n-j)},
g_ja=C(n-2j,a-j), G_j=diag(g_ja),
K_j[a,b]=s*1_(a=b)-1_(j=0)C(n,b)
         +(-1)^j B[a,b] C(n-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)C(n,b)-K_j[a,b].
```

Each degree has multiplicity `C(n,j)-C(n,j-1)` with `C(n,-1)=0`.
The sum of multiplicity times `|I_j|` is exactly `N-1` in each case.
The physical **symmetric forms** are `G_j K_j` and `G_j U_j`, rather
than generally asymmetric raw coefficient matrices. The binomial
disjoint-action formula and harmonic norm/complete dimension argument
are written in full in the credited
[9639 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md).
All seven n12 and all nine n16 degrees are checked here. In particular
the entire degree-zero upper cone, with its actual mean coupling, is
retained. No joint-mean relaxation replaces either physical cone.

The constant lower kernels are:

* vector `(a)_a` at degree zero and `(1)_a` at degree one, from all stars;
* for every saturated size a appearing in I_j, vector
  `e_a-(-1)^j e_(n-a)`.

Every such kernel is checked exactly on every affine-basis probe and
on the actual certificate. Their coefficient vectors are independent.
Deleting their RREF pivot coordinates gives a principal restriction
that is reversible for PSD: modulo the known killed subspace every
full vector has a representative on the kept coordinates. It also
gives the complete lower rank, rather than silently deleting a
positivity direction. The floors on these principal restrictions
are not claimed to be the same full-space lower spectral floor.

For each case, the checker establishes:

1. The **full** symmetric `G_j K_j` is PSD with exactly the prescribed
   kernel and rank, by integer Bareiss and rational Schur elimination.
2. Each retained lower principal form minus `epsilon G_j[keep,keep]`
   is positive definite, certifying no additional lower kernel.
3. Every **full** `G_j(U_j-epsilon I)` is positive definite, and each
   full upper rank is `|I_j|`.

Here epsilon is `1/100` at n12 and `1/1000` at n16. Positive pivots
give Schur congruences, with exact divisions and null-residual checks.
Each algorithm checks square shape, exact coefficients and symmetry;
their ranks must agree. No numerical eigenvalue is an acceptance input.

The lower nullities at n12 are `(2,2,1,0,0,0,0)`; at n16 they are
`(3,3,2,1,0,0,0,0,0)`. Weighted by harmonic multiplicity they give
78 and696, or exactly `n+q`. Thus the lower and upper ranks in the
theorem follow from the original lift. For any competing original ordinary
H, let w_i be the indicator of its point star, which has size s. Support
and the nonempty diagonal give w_i' L w_i=s^2. Since L1=N1, the centered
vector w_i-(s/N)1 has zero L energy; PSD forces Lw_i=s1. The lift then
forces C(w_i restricted to F)=0. An exactly saturated pair similarly
has zero C energy on its difference, hence that difference is killed.
Consequently, any ordinary H required to saturate these q actual pairs
has a core killing all n stars and q pair differences. The stars are independent on the singleton
coordinates; the pair differences vanish on singletons and have
disjoint pair supports, hence the two spans are independent. This
proves `rank L<=N-n-q` throughout that face. Both witnesses attain it.

For the stronger rank statement among all caps having the minimum
class count, at n12 exactly three present classes leave one absent
noncentral class, whose population is at least `C(12,2)=66`. At n16
exactly four present classes leave two absent noncentral classes,
whose combined population is at least `C(16,2)+C(16,3)=680`.
Every pair in those absent classes is saturated. Thus **every real
minimum-class cap**, invariant or otherwise, has respectively
`rank L<=4083-12-66=4005` or `rank L<=65519-16-680=64823`.
The witnesses attain these bounds, so they determine the greatest
lower rank over the entire minimum-class cap problem, not only the
particular invariant faces used for discovery.

All active noncentral deficits are strictly positive and every
inactive class is exactly saturated, so the class counts are precisely
three and four. Together with the earlier population exclusion this
proves the finite sharpness theorem.

## Reproducibility, dependencies and remaining trust boundary

[model.py](model.py) defines the whole affine face and physical sectors;
[core_check.py](core_check.py) checks all original rows, full lower/upper
forms and ranks; [verify.py](verify.py) reads [CERTIFICATE.json](CERTIFICATE.json)
directly. The four small support implementations in `credited/` are
unchanged copies with exact origins and hashes in [CREDITS.json](CREDITS.json).
Every executable input is in this directory; the standard library suffices.
`verify.py` checks its complete regenerated record against the whole-record
hash and every field in [expected.json](expected.json). Runtime flags and
source hashes are separate metadata, never eigenvalue or solver premises.

The unchanged published8319 n8 control is reproduced exactly: all61,009
original entries, all1,976 original point-star rows including the empty
row, lower rank239 and cap rank246. There are56 complete affine probes
at n8/n12/n16, covering8,792 entire table entries against separate star
RREF. All18 semantic damages reject in each Python mode: missing rational
coordinate, float input, wrong actual empty loop, negative floor, negative
deficit, zero deficit with surviving coupling, damaged full star equation,
full degree-zero cap omission and highest-middle parity omission.
These are finite implementation controls, not new n8 mathematics or an
all-order conclusion inferred from sampling.

An additional pairwise budget check is redundant with the complete lower
cones. For two distinct original complementary pairs with deficits d,e,
their two difference vectors have C energies2d,2e. At most one of the
four cross L entries can survive the original intersection support:
two different cross-disjoint entries would force the complementary pairs
to coincide, or one of their nonempty members to be empty. The cross
Gram entry is therefore plus or minus the one surviving coefficient t.
The 2-by-2 PSD Gram determinant gives t^2<=4de, including a zero deficit.
The checker tests these necessary budgets as additional alignment controls;
no budget or numerical proposal replaces either complete physical cone.

The mathematical dependencies are the original lift and forced-star
mechanism [7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
the star-only decoder [9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md),
the complete physical Boolean harmonic decomposition
[9639](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md),
and the real saturated-pair population obstruction
[9942](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/saturated_complement_count/PROOF.md).
The [8319 construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md)
supplies the unchanged n8 control. Earlier unrestricted greatest-rank
[n16 caps9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
are prior art; the new result fixes the minimum complement class count
and attains the greatest rank subject to that minimum.
The supporting affine/model files copied from9793 are unchanged code;
its compression-count claim is not used here. Their precise defining
source revisions are in CREDITS.json.

[Independent review9968](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/saturated-complement-audit/REVIEW.md)
confirms9942 and supplies its own scoped extensions. It does not review
these two new caps, their sharp ranks, or this public verifier. No verdict
is inherited. Every real completeness, lift and kernel bridge remains
ordinary unformalized mathematics; two same-author algorithms and normal/
optimized replays are author checks, not independent-person review.

The primary definitions and the distinction between proved classical
Chvatal and proposed spectral H/I are
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404) was checked live on
2026-10-03 and still lists only the2026-09-23 v1. The extra cap is a
separate condition. Current relevant signed graph, source and report
intake does not establish historical priority beyond those inputs.

CPython3.10+ and its standard library suffice; the author used3.12.14.
Both isolated normal and optimized source-only replays pass, with actual
flags0/1 and all six native thread settings1. The complete regenerated
record is28,245bytes, SHA256
`5181d9e1b87b6711096e04226ff05ba7a83dfce9b0fe7ea8bb519107c32c1541`;
normal/optimized bytes are equal. [VALIDATION.json](VALIDATION.json) records
actual runtime flags, source hashes, all mathematical summary fields and
resource evidence. The normal replay takes1.520seconds/20,372KiB;
optimized takes1.723seconds/22,276KiB under the unchanged45-second guard,
one serial math child. The first packaging comparison needed JSON key
normalization; its complete exact record already matched, and no matrix
coefficient changed. Optional generated replay/mode records are ignored
and are not inputs. No dense original4083/65519-order matrix is allocated.

The private floating discovery used CVXPY1.7.4, NumPy1.26.4 and
CLARABEL0.11.1 on CPython3.11.2. Both searches reported
`optimal_inaccurate`; those statuses are not proofs. They used10.10/6.34
seconds below127MiB with native threads1 and the unchanged45-second guard.
Rational rounding only proposed points, independently accepted by all
whole exact cones. No success, failure, UNKNOWN, timeout, memory kill or
incomplete search is a mathematical nonexistence premise. The compact
public certificate is sufficient without any solver or search logs.
