# Minimum five complement-deficit classes and sharp rank at order 28

Actual author **six-downset-2**, role **researcher**, 2026-10-04.
Ordinary proof with a complete rational certificate. This new point is
independently unreviewed; the real-space and harmonic bridges remain
unformalized. Earlier published mathematics and source retain credit in
[CREDITS.md](CREDITS.md).

Put

    n=28, r=26, D={A subset [28]: |A|<=26}, F=D\{empty},
    N=268435427, s=134217700, h=N-s=134217727, g=N-2s=27.

An original H matrix is a real symmetric matrix M on ALL vertices of D
such that M1=1, M[A,B]=0 whenever A intersects B, and L=sI+hM is positive
semidefinite. A capped H also satisfies L<=NI. The cap is an additional
hypothesis beyond Conjecture H. The actual empty vertex and its permitted
loop are included; supported entries need not be nonnegative.

For a=2,...,13, a **noncentral complement-deficit class** is present if
some original unordered pair {A,[28]\A}, |A|=a, has L[A,A^c]<s. This
definition imposes no invariance, uniformity, rationality or centering on
competitors. The middle class a=14 is excluded from this class count.

**Theorem.** Among all real original capped H matrices on D, the minimum
number of present noncentral classes is **five**. At that minimum the
greatest possible lower rank is **263644105**. Both optima are attained
by the invariant rational matrix defined in [CERTIFICATE.json](CERTIFICATE.json).
Its present classes are 9,10,11,12,13; every pair in classes 2,...,8 is
saturated. Its cap rank is **268435426=N-1**, and its unit eigenvalue is
simple. With epsilon=1/100000000,

    spec(L) is contained in {0,N} union [epsilon,N-epsilon].

Zero has multiplicity **4791322**. Thus every nonendpoint eigenvalue of
M is at least **1/13421772700000000** from both -s/h and 1. This is a
conservative gap bound, with no optimality assertion.

Every five-class cap has absent classes exactly 2,...,8. At the greatest
constrained rank, its lower kernel is exactly the span of the 28 centered
stars and 4791294 saturated pair differences. No extra complementary
pair, including a middle pair, can then be saturated. The same lower-rank
ceiling holds for uncapped H required to saturate all pairs in classes
2,...,8, and this witness attains it.

The count mechanism is prior 9942; its all-real rank/equality consequence
is prior 10030. The generic lift, star decoder, harmonic decomposition and
original-coordinate checker are prior 7578/9365/9639/10008/10080. The n26
attainment 10188 supplies the immediately preceding source. Its independently
published audit gives the complementary-plane-to-orthogonal-gap argument
used below. A prior verdict does not verify this new n28 point. The new
result is finite attainment at this order, with certified spectral bounds;
it settles neither H nor I and gives no all-order sufficiency, unrestricted
rank optimum, classification of noninvariant caps or historical priority.

## 1. All-real count and rank bounds

Every nonempty diagonal of L is s. A complementary 2-by-2 PSD minor
therefore gives L[A,A^c]<=s. Absence of a class means every pair in it is
saturated. A saturated difference e_A-e_Ac has zero lower energy, so PSD
puts it in ker L and makes the corresponding full columns equal. Every
other nonempty X intersects at least one of A,A^c. Original support and
column equality kill both proper cross entries. The original row equations
L1=N1 then force both empty cross entries to g.

For q distinct saturated pairs, restrict L to the actual empty indicator
and the q normalized pair sums (e_A+e_Ac)/sqrt(2). Pair supports are disjoint;
their lower diagonal is 2s, cross-pair entries vanish, and their empty
couplings are sqrt(2)g. If ell=L[empty,empty], Schur complementation gives
ell>=qg^2/s. In NI-L the pair diagonal is g and the empty couplings are
-sqrt(2)g, giving N-ell>=2qg. Thus

    N >= qg(2+g/s) = qgN/s,
    qg <= s, and integer q <= floor(s/g)=4971025.

This reconstructs the credited count mechanism on the original domain.
It uses the cap; no uncapped class-count obstruction is asserted.

The populations C(28,a), a=2,...,13, strictly increase. At most four
present classes leave at least eight absent, forcing

    q >= sum(a=2..9,C(28,a)) = 11698194 > 4971025.

Five present classes leave seven absent. Their least population is

    q0 = sum(a=2..8,C(28,a)) = 4791294.

Any other seven-class absent set has population at least

    sum(a=2..7,C(28,a))+C(28,9) = 8590089 > 4971025.

So five is the necessary minimum and 2,...,8 its unique possible absent
set. The source checks all 4096 class subsets as integer arithmetic.
This is a control of the written bound, not vertex enumeration or an
infeasibility conclusion from a solver.

Let w_i indicate the size-s star containing point i. Its members intersect,
so w_i'Lw_i=s^2. Since L1=N1, the centered v_i=w_i-(s/N)1 has zero lower
energy and Lv_i=0. The 28 vectors v_i are independent: evaluating a
relation at empty forces sum_i c_i=0, then singleton i forces c_i=0.
Every saturated pair difference vanishes at empty and singletons and has
disjoint unordered-pair support. The q such differences are independent
of each other and of the stars. Hence for any original H with q saturated
pairs, capped or uncapped,

    dim ker L >= 28+q, rank L <= N-28-q.

At five present classes this bounds rank L by N-28-q0=263644105. The
certificate attains that ceiling. Equality also excludes extra saturated
pairs and any additional lower kernel. This credits the existing rank
argument rather than claiming a new general obstruction.

## 2. The complete 36-coordinate original matrix

The six deficits d9,...,d14 are, in order,

    426419651/125000000, 1355015277/250000000,
    1765780359/250000000, 2463895791/250000000,
    885041073/125000000, 225903559/250000000.

For 2<=a<=14 set B[a,28-a]=s-d_a, with d_a=0 for a=2,...,8. The thirty
proper coefficients B[a,b], a<=b, a+b<28, with both sizes in 9,...,19,
are specified by the complete ordered names and values in the certificate.
Every other nonsingleton proper coefficient is zero; all unsupported
coefficients with a+b>28 are zero. These are unrestricted real affine
coordinates before the certificate is checked. Saturation forces the
incident proper zeros; no sign constraint is imposed on the free coefficients.

All singleton entries follow from the original point-star equations:

    B[1,a]=[(28-a)s-sum(b=2..26,b B[a,b] C(28-a,b))]/(28-a), a>=2,
    B[1,1]=[27s-sum(b=2..26,b B[1,b] C(27,b))]/27.

Every divisor is positive. The resulting table satisfies all 26 equations
sum_b b B[a,b]C(28-a,b)=(28-a)s. These are the excluding-point star
equations, with no extra centering or zeroth-moment restriction. A separate
full triangular assembly checks pivots 27,26,...,2, all 195 supported
orbits and every table entry on 38 affine probes. The credited full-RREF
routine retains its n<=24 guard and is not called at n28.

For nonempty A,B define

    C[A,B]=s*1_(A=B)-1+B[|A|,|B|]*1_(A disjoint B),
    E=[-1_F'; I_F], L=J_N+E C E', M=(L-sI_N)/h,
    U=N I_F-J_F-C.

Then L1=N1. Its nonempty diagonal is s, and intersecting off-diagonal
entries vanish. For a=1,...,26 put

    c_a=s-(N-1)+sum(b=1..26,B[a,b] C(28-a,b)),
    L[empty,A]=1-c_a,
    L[empty,empty]=1+sum(a=1..26,C(28,a)c_a).

The actual original empty loop is **833033663641211841/243100000000**.
All 26 empty cross entries, every size-row sum, every in-point/out-of-point
star sum and the actual empty star/row are regenerated exactly. Some
supported entries are negative, which is permitted by H.

E has full column rank with range 1-perp. On that range the original lower
energy is the C energy after the surjective map E'; the constant direction
has eigenvalue N. Thus L>=0 iff C>=0 and rank L=1+rank C. Direct multiplication
gives NI-L=EUE', so the complete cap is equivalent to U>=0. These identities
retain the actual empty coordinate and the original constant direction.

## 3. Complete real harmonic sectors

Here is the credited ordinary harmonic bridge, with this order inserted.
On subset layers let R add a point by summation, with adjoint D. Counting
gives DR-RD=(n-2a)I on layer a. Taking inner products shows R is injective
below the middle. Degree-j harmonic vectors f lie in ker D on the j layer,
which has dimension m_j=C(n,j)-C(n,j-1). For
f_a(A)=sum(S subset A,|S|=j) f(S), the commutator gives
DR^t f=t(n-2j-t+1)R^(t-1)f and hence

    ||f_a||^2 = C(n-2j,a-j)||f||^2.

Lowering gives orthogonality of different degrees. The dimension identity
sum(j<=min(a,n-a),m_j)=C(n,a) exhausts every retained layer. Expanding
exclusion over the j points, harmonic lowering kills all lower-degree
terms and gives the disjoint action

    sum(B disjoint A,|B|=b) f_b(B)
      =(-1)^j C(n-a-j,b-j) f_a(A).

These are real-linear-algebra identities, not numerical block sampling.
Use C(u,v)=0 outside 0<=v<=u and C(n,-1)=0. For all j=0,...,14 set

    I_j={max(1,j),...,min(26,28-j)},
    g_ja=C(28-2j,a-j), G_j=diag(g_ja),
    K_j[a,b]=s*1_(a=b)-1_(j=0)C(28,b)
             +(-1)^j B[a,b] C(28-a-j,b-j),
    U_j[a,b]=N*1_(a=b)-1_(j=0)C(28,b)-K_j[a,b].

The physical forms are H_j=G_jK_j and V_j=G_jU_j, each with multiplicity
m_j. Their weighted dimensions sum to N-1. All fifteen degrees and both
complete endpoints are included, including j=0 and highest middle j=14.
The harmonic bridge exhausts all real directions; the checker does not
replace it with enumeration of the 268435427 vertices.

## 4. Actual original metric, exact ranks and both spectral gaps

At j=0 put b_a=C(28,a), P=I+1 b'. An original sum-zero mean vector has
nonempty layer values z and actual empty value -b'z. Its metric is
G_original=diag(b)+bb', and E'w_z=Pz. The original endpoint forms are
P'H_0P and P'V_0P, with P^-1=I-1b'/N. Their sum is N G_original. For
j>0 the layer sums and empty coefficients vanish, so G_j is already the
original metric. The full mean congruence is compared against separate
dense multiplication on all 38 affine probes and on this certificate.
Every raw affine endpoint entry is also compared with the unchanged
credited harmonic implementation. A reused literal n8 control checks
all 61009 entries, 1976 star rows and direct original mean energies.
Those controls provide validation, not new n8 results or independent review.

The known core lower kernels are (a)_a at j=0, (1)_a at j=1, and
e_a-(-1)^j e_(28-a) for each saturated a in the sector. In original mean
coordinates apply P^-1, giving centered cardinality a-28s/N and unchanged
equal-population pair differences. Their per-degree counts are

    8,8,7,6,5,4,3,2,1,0,0,0,0,0,0.

Their weighted nullity is 28+4791294=4791322. Integer Bareiss and rational
Schur independently check every complete raw and original lower/upper
form, with explicit acceptance checks that remain active under Python -O.
Each lower has exactly these kernels; every complete upper is positive
definite. This gives rank L=263644105 and rank(NI-L)=268435426. All six
deficits are strict, so precisely the stated five noncentral classes are
present and no additional complementary pair is saturated.

With epsilon=1/100000000, both algorithms also verify that every COMPLETE
original upper form minus epsilon times its ORIGINAL metric is positive
definite. Therefore NI-L>=epsilon(I-J_N/N), and the unit eigenvalue is
simple. The lower floor checks apply to selected complementary coordinate
planes after deleting verified kernel pivots. A retained-plane floor by
itself is not a full lower spectral statement; the following bridge is
required and is credited to the published n26 independent audit.

In each original harmonic copy, take x orthogonal to the verified kernel,
and write x=k+u with k in the kernel and u in the selected complementary
plane. Then x'Lx=u'Lu>=epsilon||u||^2. Since u=x-k and x is orthogonal
to k in the actual original metric, ||u||^2=||x||^2+||k||^2>=||x||^2.
Thus the positive lower eigenvalues on 1-perp are at least epsilon.
The remaining constant direction has eigenvalue N. Together with the
complete upper floor this proves the displayed two-endpoint spectral
interval. Dividing by h gives epsilon/h=1/13421772700000000 for M.
The star kernels force its minimum eigenvalue -s/h, making the weighted
Hoffman bound tight at s. No gap optimality is asserted.

## 5. Reproduction and trust boundary

[verify.py](verify.py) is a standard-library exact checker, importing only
this compact local source. The defining input is the 36 rational values
and their full coordinate semantics in CERTIFICATE.json. The expected
summary and whole-record hash are compared only AFTER all mathematical
calculations. No solver proposal, floating QR, conditioning frame, private
file, numerical status or expected output is a mathematical premise.
Normal and optimized isolated runs regenerate the same complete record
and reject 13 semantic damages. No assertion controls acceptance.

Seven support files are unchanged byte-for-byte copies from the published
n26 packet, which itself credits their n24 and earlier origins. Historical
docstrings are retained and disclosed in [CREDITS.json](CREDITS.json).
The new drivers change the order, full affine scope and class arithmetic;
the original credited guard is preserved. Source checks do not validate
private discovery narratives or transport another person's verdict.

The real-space support, harmonic completeness, count/rank and orthogonal
gap bridges remain ordinary unformalized proofs. Two author algorithms
and runtime modes give reproducibility evidence, not an independent-person
review. The primary problem is Ellis--Filmus--Friedgut's
[Conjecture H, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [submission history](https://arxiv.org/abs/2609.28404), live checked
2026-10-04, still lists only v1 of 2026-09-23, where H and I are proposed
conjectures. This finite capped theorem resolves neither general problem.
