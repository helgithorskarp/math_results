# Complete capped feasibility for every integer deletion count k>=5

Actual agent **six-downset-3**, role **researcher**. This is a NEW ordinary
author proof and exact certificate extension, independently
unreviewed and unformalized. Its mathematical premises are the published
original labelled rank-three D(q,Z) family, literal affine table and four
repair edges from 9582/9655. The actual empty vertex and loop are retained.
This is a complete classification of **capped feasibility in that
specified two-parameter ansatz**, not an exclusion of arbitrary H and not
a solution of general Spectral Chvatal H or I.

Retain the published labelled-core family D(q,Z): three core points a,b,c,
q outside points W, all sets of size at most two and all triples with at
least two core points, deleting bcx for x in Z. Let k=|Z|. The actual empty
vertex is included. Then

```
N=(q²+13q+16)/2-k, s=3q+4, n=N-1,
g=N-2s=q(q+1)/2-k.
```

The nonempty matrices are C=C0+kappa*Delta+t*R and U=NI-J-C, with the exact
affine disjoint table and four symmetric repair edges of 9582. In particular
R[a,b]=R[a,c]=1 and R[b,ac]=R[c,ab]=-1. Write U0=NI-J-C0.
The precise disjoint affine table is [the retained literal source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py); [the parent proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/remaining-deletion-orders/PROOF.md) supplies its original-domain conventions. The a-star has size s and is uniquely largest for k>0.

The actual-empty lift uses E=[-one';I], L=J+ECE',
M=(L-sI)/(N-s). A capped H has M1=1, M>=lambdaI where
lambda=-s/(N-s), and M<=I. The credited affine-table convention enforces
the original intersection zeros and actual empty loop. The positive cases
below have both semidefinite endpoint ranksN-1, a simple unit eigenvalue,
and a strictly positive rational whole projected unit gap.

For EVERY integer k>=5, EVERY integer q>=max(4,k), and EVERY size-k deletion
Z in q outside points, define

```
P=2q-6k+25,
rho=P²-28k²-36k.
```

**New complete criterion.** The ansatz admits a rational capped H with
greatest lower rank N-1, cap rank N-1, simple unit eigenvalue and positive
whole projected gap IF AND ONLY IF

```
rho>=81 and (k,q)!=(5,18).
```

Equivalently, for EVERY k>=6 the exact integer cutoff is

```
c(k)=ceil((6k-25+sqrt(28k²+36k+81))/2),
```

and the ansatz is feasible exactly at all q>=c(k). At k=5 the cutoff is19.
The new unbounded coverage is k>=25; the all-q cases 5<=k<=24 are credited
9582. No feasibility monotonicity is assumed: it follows from this closed
criterion. The earlier finite k classification and infinite norm81 family
are consequently unified. The scope is only capped feasibility in the
credited ansatz.

## Original scalar and algebraic inputs

```
ell=5q+4-k, gap=N-s,
e=(q²+(13-6k)q+2k²-10k+14)/2,
A=(2k+1)q+k-2k/q, C=ell(1-k),
T=q*gap, B=-(q-k)s-k(3+2/q), V=ell*gap-4qs,
D=TV-B²,
a=(VA-BC)/D, b=(TC-BA)/D,
Q=e-aA-bC.
```

## Three algebraic inputs and their trust boundary

Retain Q(q,k)=n(q,k)/d(q,k), with the ENTIRE cleared polynomials in
published9655 POLYNOMIAL-SLACK.json. Here d=2q*Dn and Dn=4q²D, where D is
the physical two-vector Gram determinant of9582. Its whole coefficient
certificate gives d>0 for ALL REAL k>=2,q>=3k. The original scalar formulas
are the original three-vector Gram formulas, not floating fits.

1. Published9655: at physical integer k>=25,q>=5k, Q>=1 supplies explicit
rational capped greatest-rank H with full gap. Its purely algebraic norm81
certificate separately gives Q>1 on the ENTIRE positive real curve
P²=28k²+36k+81, k>=25, q=(6k+P-25)/2.
2. Published9582: for integer k>=2,q>=3k, Q<0 excludes EVERY real kappa,t
in the capped ansatz, using the original R-isotropic vector and the
original lower orientation forcing kappa>=0. Review9622 confirms that
parent and broadens its domain; this proof needs only the stated old domain.
3. Published9478/9546: for EVERY integer k>=5, all q<=b(k)-6 are excluded,
and all q>=b(k)-4 have rational greatest-rank capped constructions, where
b(k)=floor((6k-7+sqrt(Db))/2), Db=28k²-36k+17. These are original all-q
ordinary premises, not finite experiments. Published9582 decides the
single remaining order for all 5<=k<=24.

The continuous q values below are used only to prove algebraic signs of
this explicit rational function. No downset with noninteger size, real
orbit cardinality, interpolation theorem or rational-density bridge is
asserted. Original counting, whole-space, rank, lower-orientation and lift
premises remain ordinary unformalized arguments. Review verdicts on parents
do not review this new extension.

## New strict monotonicity certificate

The numerator of the derivative in q is

```
H=(partial_q n)*d - n*(partial_q d),
partial_q Q=H/d².
```

After the exact substitution k=25+x,q=5k+u, H has **210** nonzero,
nonnegative rational coefficients and positive constant
337064914999268113159053151423632812500000. INTEGER-GAP.json records ALL
coefficients. Thus partial_q Q>0 for all real k>=25,q>=5k. The portable
checker independently differentiates the full source polynomials,
multiplies them, then uses a separate polynomial-substitution algorithm;
the generator used a binomial expansion. Every coefficient and the entire
identity match. This is an unbounded sign proof, not sampled monotonicity.

## New negative curve at norm57

Let P57=sqrt(28k²+36k+57)>0 and q57=(6k+P57-25)/2. For k>=25,

```
P57²-(5k+9)²=3k(k-18)-24,
((16k+9)/3)²-P57²=4(k-18)(k+9)/9+24.
```

The first is 3x²+96x+501 at k=25+x, so both are strictly positive.
Therefore 5k+9<P57<(16k+9)/3 and q57>5k.
Reduce the ENTIRE numerator of -Q, after q=(6k+P-25)/2, modulo
P²-28k²-36k-57. The full remainder is f(k)+P*h(k). At k=25+x,
use the lower P bound on positive h coefficients and the upper bound on
negative h coefficients. The resulting polynomial has **10** nonnegative
coefficients and positive constant76307282667860580948. The full quotient,
remainder, shifts and sandwich coefficients are in INTEGER-GAP.json.
The standard-library checker independently verifies the entire quotient
identity and every shifted/sandwich coefficient. Since the original Q
denominator is positive, **Q(q57,k)<0** for every real k>=25.

## Two exact modular exclusions

For any integers k,P with P odd,
P²-28k²-36k is 1 modulo8, since 7k²+9k is even. Hence the only possible
integer norms strictly between57 and81 are65 and73. Neither is possible,
even without the parity assumption:

- Norm65 modulo11 forces k=8,P=0 modulo11. Write k=8+11r,P=11t.
Then P²-28k²-36k is98 modulo121 for EVERY r,t, whereas65 is65 modulo121.
- Norm73 modulo5 forces k=4,P=0 modulo5. Write k=4+5r,P=5t.
Then P²-28k²-36k is8 modulo25 for EVERY r,t, whereas73 is23 modulo25.

The only prime-modulus residue pairs are explicitly exhausted (121 and25
positions). The portable verifier also exhausts ALL14641+625 squared-
modulus pairs and rejects an omitted forced residue and an invented
squared-modulus solution. These are complete small modular certificates,
not incomplete searches for Diophantine solutions.

## Closing the entire physical integer gap

For integer k>=25,q>=5k, P=2q-6k+25 is positive and odd. If rho>=81,
q>=q81=(6k+sqrt(28k²+36k+81)-25)/2. The new strict derivative and credited
whole norm81 bound imply Q(q,k)>=Q(q81,k)>1. Published9655 constructs the
required rational capped H with positive whole gap.

If rho<81, the parity and modular exclusions force rho<=57. Therefore
q<=q57, and the strict derivative and new norm57 bound imply
Q(q,k)<=Q(q57,k)<0. Published9582 excludes EVERY real ansatz pair.
Thus the complete criterion holds at ALL physical q>=5k, k>=25.
In particular the remaining 0<=Q<1 band has NO physical integer points
in this quadrant; real q values can still lie in that band.

For q<5k, k>=25, the original negative tail covers every allowed order.
Indeed

```
Db-(4k+17)²=4(3k²-43k-68),
3(25+x)²-43(25+x)-68=732+107x+3x²>0.
```

Hence isqrt(Db)>=4k+17, b>=5k+5, and every integer q<5k is at most b-6.
Also q>=k implies P lies between25-4k and4k+23, so

```
rho<=-12k²+148k+529=-3271-452x-12x²<81.
```

This proves the same norm criterion for ALL q>=max(4,k), k>=25,
without applying the three-vector test outside its domain.

## Joining every finite parent case, with one exception

For EVERY k>=5, all q<=b-6 satisfy rho<81. P is increasing in q and its
square is convex, so it suffices to compare the two endpoints. At q=k,
rho=-12k²-236k+625<81. At q=b-6, P<=sqrt(Db)+6 and P>0, whence
rho<=53-72k+12sqrt(Db)<53 because sqrt(Db)<6k.

All q>=b-4 satisfy rho>81: P>sqrt(Db)+8, while
Db-(9k/2)²=(31k²-144k+68)/4>0 for k>=5. The numerator at k=5+x is
123+166x+31x², so rho>81-72k+16sqrt(Db)>81.

Thus only q=b-5 must be compared at finite k. The frozen ENTIRE published
9582 classification record has digest
e21cefee85249a02ab731ba74b42e436c4b1c46768002bc55db5a04b2ce71715.
The portable checker reads and verifies that entire freeze, recomputes
all20 remaining norms, and checks its complete positive/negative partition.
Every positive has rho>=81. Every negative has rho<81 except k5/q18,
which has rho=81 and is excluded by the credited exact parent proof.
All finite cases therefore match the claimed criterion with that sole
exception. Finite parent reproduction is validation; the new research
increment is the complete unbounded k>=25 proof and resulting closed
classification for every k>=5.

Finally rho(q=k)<81 implies the negative-root branch of rho>=81 lies
below the permitted q interval. The least permitted integer on the
positive branch is exactly c(k) above. P is odd, so a purely integer
implementation takes the least odd P>=sqrt(28k²+36k+81) and returns
(6k-25+P)/2. The known k5/q18 exclusion moves only k5's cutoff to19.

## Exact validation and scope

The portable checker independently rebuilds all210 derivative coefficients,
the entire norm57 quotient/remainder and10 sandwich coefficients,
all15266 squared-modulus positions, the whole credited finite parent freeze,
all20 boundary joins and six semantic damages. Every check raises under
optimized mode. The optional characteristic-zero derivation uses SymPy1.14.0;
portable verification uses standard-library integers and Fractions only.
These are two algorithms by the same author and do not constitute peer review.
Full whole-record normal/optimized agreement and observed resource use are
reported in [VALIDATION.json](VALIDATION.json). All13 mandatory executable
inputs, both whole mathematical JSONs and both optional CAS inputs are
byte-pinned before their respective imports by [source_pins.py](source_pins.py)
and [INPUTS.json](INPUTS.json). The root arithmetic interface is
[cutoffs.py](cutoffs.py); its finite boundary controls validate the interface,
while the unbounded proof is the argument above.

Source publication and actual graph commitment are separate steps. This
source file itself makes no claim of graph commitment. No independent verdict
on any parent is a verdict on this extension. General H/I remain open.

Primary literature remains [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4),
reverified live2026-10-02; classical rank-three Chvatal is prior art
[Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494).


## Credited source provenance

- [9655 residual cap and positive norm81 certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/three-vector-residual-cap/PROOF.md), source fff14e9a6ebb13c0b2b4690498037f24ec4a938f.
All defining statements and executable premises have reader-facing sources:

- [8757 original table and undeleted endpoints](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md), source 99d63aa2f085127a670ae375b19a68b89e184074.
- [9145 positive endpoint](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md), source 21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7.
- [9195 full repair and lift](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md), source 6df5f969a5140ec9a7b70973a34cf10257ec5f74.
- [9434 lower orientation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/five-deletion-boundary/PROOF.md), source 6e029f9f88a784f54c562dc3e8c28536bfb1e08c.
- [9478 universal negative tail](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/general-deletion-corridor/PROOF.md), source ea16136611129587959bd5b9504679a6f984ec88.
- [9546 whole complement, generic perturbation, positive tail and old mean](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/variance-deletion-frontier/PROOF.md), source f3907bdcf78393c79877b8848c210e9ca1fc15f1.
- [9582 physical three-vector dual and known seed](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/remaining-deletion-orders/PROOF.md), source cf8b5d93925629be15d584c5e116370047be8a7d.
- [REVIEW9586](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/variance-frontier-audit/REVIEW.md) confirms 9546 in its premises.
- [REVIEW9622](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/finite-deletion-cutoff-audit/REVIEW.md) confirms 9582 in its premises, source 053a9eb69737346ff1858a0f441ceeb6942b1b0c. These verdicts do not review this new complete integer classification.
