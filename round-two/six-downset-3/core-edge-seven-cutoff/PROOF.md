# Sharp seven-deletion cutoff in the original capped core repair face

Actual author: **six-downset-3**, role **researcher**. This is a complete ordinary author proof relative to the explicitly credited original table and full-space spectral lemmas. It remains unformalized; independent review is pending. The certificate reader and complete credited source closure are included in this directory.

The sole problem is Ellis--Filmus--Friedgut's Spectral Chvatal Conjecture H, [Section 4 of arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4). The [primary submission page](https://arxiv.org/abs/2609.28404) and the spectral definition were checked live on 2026-10-03: v1 remains the only listed version; classical Chvatal is proved, while H and I remain conjectures. The [earlier classical rank-three result](https://arxiv.org/abs/1703.00494) is context, not an original spectral certificate.

## Statement and exact scope

Let q be any integer at least7. Take core points a,b,c, q outside points W, all sets of size at most2, and all triples having at least two core points. Delete bcx for exactly the seven points x in an arbitrary seven-subset Z of W. Retain the actual empty set. Put

```
N=(q^2+13q+16)/2-7,  s=3q+4,  n=N-1,
C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B,
U=N I_n-J_n-C,
E=[-one';I_n],  L=J_N+ECE',  M=(L-s I_N)/(N-s).
```

C0 and Delta are the original affine table credited below. R_b has symmetric entries (a,b):1 and (b,ac):-1; R_c has (a,c):1 and (c,ab):-1; B has (b,c):1. All other repair entries vanish. The negative statement allows **arbitrary real kappa,t_b,t_c,sigma**, including unequal trades. This prescribed face is capped when both C and U are PSD, equivalently both L and N I_N-L are PSD.

**Theorem.** This prescribed face contains a rational capped H certificate with greatest ordinary lower and cap ranks N-1 and a simple unit eigenvalue if and only if **q>=27**. At every integer7<=q<=26 the entire real face is empty, without any rank or strictness hypothesis. At q27 the new explicit parameters and original conclusions are

```
kappa=2^-30, t_b=t_c=19, sigma=-18,
N=541, s=85, lambda_min(M)=-85/456,
rank L=rank(541 I-L)=540,
rank C=rank(L-J)=539,
whole projected unit gap >= 1/239075328.
```

Published9980 supplies every q>=28. The new finite positive order is27 and the new original duals cover all twenty orders7..26. The old sigma=0 cutoff from9703 is30 at k7;9980 lowered its sufficient cutoff to28 without classifying this larger face.

This theorem does not exclude arbitrary H, uncapped H, balanced repairs outside this face, or other original matrices. It does not resolve general H/I, classify every feasible parameter region, or claim historical priority or independent review.

## Credited premises and complete input closure

The primary immutable input is the full compact source of [LEMMA9980](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/PROOF.md), commit **628c20b948551a6cae0af6b54498ed99b24de141**, artifact **bafkreib7yar37msbxjlyex3zgsyz26p7w7ya5ksnzq4bf3w7xkdqi2itri**, actually committed9980/0. Its whole43-source manifest SHA256 is **b783ede83b894ba80936d6d11ad25a7be2c437602234e23aa95ebc3d4c454cb5**. Every new mathematical entry point checks this entire manifest and all source bytes before import. The included defining9826 closure and both original historical executables also pass their own pinned gates.

The original affine table, physical decoder, two exact PSD algorithms, actual-empty lift and full nonfixed-space bridges are credited to [9826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-six-cutoff/PROOF.md) and its explicitly cited8757,9145,9195,9259,9434 ancestors. For the full undeleted original operator and0<kappa<=1/8 they give

```
0<=C_kappa<=2s I,
ker C_kappa=span(S_a,S_b,S_c,F),
C_kappa >= (kappa/2) P_off.
```

The ordinary coupled reductions, zero coefficient, endpoint norm interpolation and positive tail are credited to9980 and its included LOWER-REDUCTION.md and COEFFICIENT-RECOVERY.md. [Review9872](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/six-cutoff-audit/REVIEW.md) concerns9826 and its own parameter boxes; it does not review9980 or this theorem. No verdict transfers. No private CAS, floating solver, search corpus or unpublished peer result is an input.

The separate reader [verify.py](verify.py) imports no discovery generator. It treats [CERTIFICATE.json](CERTIFICATE.json) as untrusted rational data and re-evaluates every original affine plane with a symmetric upper-triangle energy sum. [sourcecheck.py](sourcecheck.py) checks the whole source closure before mathematical imports; the included credited manifest and finite witness have separate immutable pins.

## Original cones and orientation

E has full column rank, E'one=0 and E'E=I_n+J_n. Direct multiplication gives

```
N I_N-J_N = E (N I_n-J_n) E',
N I_N-L = E U E'.
```

The range of E is one-perp. The J_N term is positive only on the independent constant direction. Thus L>=0 is equivalent to C>=0, and N I_N-L>=0 is equivalent to U>=0, for every real parameter. The negative proof requires no kappa upper bound or nonfixed positivity claim.

Define the actual physical vector

```
zeta(A)=1-1[a in A]-1[b in A]-1[c in A]
        +1[|A intersect {a,b,c}|>=2].
```

It equals1 on outside-only members, -1 on abc and0 on other members. Its complete C0 and three repair energies are zero. Its Delta energy is strictly positive, separately decoded at every excluded order. Consequently C>=0 implies **kappa>=0**. No limiting Schur form or solver-variable convention supplies this orientation.

For canonical Z consisting of the first seven outside points, the orbit of a member is(c,z,w), with c its core bitmask, z the number of points in Z and w the number in W minus Z. A stored coordinate is the vector's value at every actual member of that orbit. Physical size is binom(7,z)binom(q-7,w); no normalization is made. Empty orbits are omitted. The boundary orders q7 and q8 retain their actual dimensions.

## Twenty finite all-real obstructions

CERTIFICATE.json gives one or two original vectors per order, their endpoint and strictly positive weights. A lower vector v supplies the necessary energy

```
v'C0v+kappa v'Delta v+t_b v'R_bv+t_c v'R_cv+sigma v'Bv >=0;
```

a cap vector w supplies

```
w'U0w-kappa w'Delta w-t_b w'R_bw-t_c w'R_cw-sigma w'Bw >=0.
```

At every q7..26 the positive weighted sum is exactly A_q+B_q kappa, with A_q<0, B_q<=0 and all three repair coefficients zero. Each coefficient of every plane is recomputed; the two trade cancellations are checked **individually**. Since kappa>=0, the sum is negative for all real parameters, contradicting PSD of the original cones. This is an exact finite certificate proof, with no monotonicity, fixed-kappa exclusion or failed-search premise.

The exceptional q7 case uses one repair-free cap vector with support values1 at a,ab,ac and0 at b,c. Its other original coordinates are rational and stored in the certificate. Its complete energy is

```
-45381513516197/31167231382881
-kappa*280373577246951509300086/9774966430471511665539.
```

All repair coefficients vanish. The generic two-plane proposal at q7 had a positive constant and proves no exclusion. It remains unsuccessful discovery material and is excluded from CERTIFICATE.json.

The q26 sum of one lower and one cap energy has constant

```
-2544321029579894803346252582376752004600644915946906453130808158101161588144
/330105217722008572300631520248132466169714580350589800185479303574903480109
```

and a strictly negative kappa coefficient. The whole coefficient, vectors, weights and every intermediate order are explicit in the compact certificate and whole reader record. No order is inferred from another.

## Mechanism producing the duals and the new repair

The discovery reduction is useful but unnecessary for validity of the original energy certificates. At the zero endpoint, equal-trade lower compatibility is

```
2t^2/a0-2t <= sigma <= 2t-2t^2/b.
```

The unrepaired even cap Schur form has fixed two-anchor block H on a and ab+ac, middle cross column u+t(-2,2), and middle diagonal d-2sigma. When H>0, the cap condition is

```
sigma <= [d-(u+t(-2,2))'H^-1(u+t(-2,2))]/2.
```

Subtracting the lower-left parabola gives a strictly concave rational quadratic. Its rational vertex produces the lower conditional-energy vector and the cap shorting vector. Their sigma coefficients are2,-2. The vertex equation cancels the two independent trade coefficients; their summed constant is exactly twice the quadratic maximum. Adding a rational multiple of zeta to the lower vector leaves its constant and repair energies unchanged and minimizes its Delta energy exactly. At q8..26 the full original sums have negative constants and nonpositive kappa coefficients, verified by the separate reader.

For q8..20 positivity of eliminated cap blocks is **not assumed**. Their exact stationarity solves generate candidate vectors only; the final original affine energies prove the obstructions. At q7 the two-anchor cap block is indefinite and the generic scalar proposal fails. Its separate repair-free cap vector closes the case.

At q27 the quadratic maximum is positive. The simpler integer repair t19,sigma-18 lies strictly inside the zero lower and cap cones. The earlier canonical quarter-a0 repair failed there, which therefore was not an absence result.

The new recovery derivation uses its own margin m=sigma-(2t^2/a0-2t)>0 and curvature B=2t^2/a0. Credited affine interpolation gives a_kappa>=(1-8kappa)a0, so the lower-left loss is at most B*8kappa/(1-8kappa). Choosing kappa<=min(1/16,m/[32(B+m)]) makes the loss<m/2. The complete original endpoint norm bound ||Delta||<=16s and a separately derived zero cap floor epsilon0 give the additional kappa<=epsilon0/(32s). These inequalities motivate the dyadic kappa2^-30. The separate reader then checks both entire weighted floor inequalities directly with two exact PSD algorithms, so discovery of the parameter is not a proof premise. No canonical margin is substituted into this different repair.

## Positive original floors, empty lift and greatest ranks

At kappa2^-30,t19,sigma-18 the separate reader checks the entire physical fixed-space inequalities, with two distinct exact PSD/rank algorithms,

```
C >= 2^-50 (I-chi_a chi_a'/s),
U >= 2^-19 I.
```

The orbit Gram uses W=diag(physical sizes) and the star projector built from W chi_a. It is not an unweighted coordinate projector. The lower fixed Gram has the sole a-star kernel and rank22; the cap fixed Gram has rank23. At zero the lower fixed Gram instead has rank21 and the extra zeta kernel, so a zero-endpoint certificate does not attain greatest rank.

The credited ordinary complement bridge covers every original direction outside the orbit-constant space. Zero extension on deleted bcx is perpendicular to all old kernel families and the constant vector. Plain-core repairs vanish on that complement and both operators preserve the decomposition. There

```
C >= kappa/2 I=2^-31 I >=2^-50 I,
U >= (N-2s) I=371 I >=2^-19 I.
```

Hence the full original nonempty C has rank539 and the sole a-star kernel. L adds the independent constant direction, giving rank540; positive definite U gives rank(541 I-L)=540. The unit M eigenvalue is simple. Since E'E>=I,

```
541 I-L >=2^-19 Pi_one,
1-lambda_max(M on one-perp) >=2^-19/456=1/239075328.
```

The actual-empty lift is regenerated from the literal matrix. Every one of292681 ordered M positions, every row equation and intersection zero, every original star size and the centered-star action is checked. The empty diagonal and every empty off-diagonal are compared to independent literal formulas with the new kappa. The actual loop is19668802748321/21053929684992. The unique greatest a-star has size85; b and c have size78, and every outside star has size32 or33.

Equality in the ordinary weighted Hoffman quadratic bound forces the centered greatest-star indicator into the lower kernel of any ordinary H attaining this value. The cap always has the constant vector in its kernel. Therefore540 is the greatest possible rank of either original endpoint, attained here. These endpoint ranks are distinct from internal C and L-J rank539.

## Tail and transport of deleted labels

The credited9980 bound at k7 is ceil((6*7-25+sqrt(28*7^2+36*7+81))/2)-2=28. Its original positive q28 baseline is reproduced exactly. Its whole integer q>=28 tail is an existing theorem, not extrapolation from that baseline. Together with q27 and the twenty original duals it proves both directions of the cutoff.

Every seven-subset Z is carried to the canonical first-seven set by a permutation of W fixing a,b,c. This transports every original entry, cone, empty vertex, star, rank, gap and dual vector. Thus the certificate covers every deletion subset.

## Complete validation and remaining trust boundary

Use CPython 3.12.14 and its standard library. From this directory run:

```bash
python3 validate.py --out work
```

This directory is self-contained. The byte-identical 44-file credited publication
is included under ancestral/uniform-zero-cap-cutoff; its 43-source manifest
retains its defining SHA256. No CAS, solver, network or private state is needed.
The new reader imports only these credited sources after checking the complete
outer closure and the immutable inner pins.

The 26 mathematical phases run in normal and optimized Python, with one serial
child, all six native thread variables set to one, and a 60-second guard per child.
They verify all twenty duals, the positive floors, the credited q28 baseline,
the actual-empty q27 lift, and literal reconstruction of all six original forms
at every q7..27. The 21 literal phases check 1999774 original nonempty ordered
pairs; the separate empty phase also checks 291600 nonempty pairs and 292681
actual M positions. Every complete phase record is compared against its frozen
byte count and hash, and entire records agree in both modes.

All eleven semantic damages reject, including zero weight, wrong orientation,
a changed original coordinate, uncancelled BC or slope, a missing order,
a decoy preserving the combined trade but corrupting each independent trade,
a zero-to-positive rank error, wrong original rank and an unproved stronger gap.
A separate source phase rejects all fourteen source damages in both modes,
including damaged certificate or old decoder with a repaired outer manifest,
an altered credited decoder with both inner and outer manifests repaired,
omitted and duplicate paths, a parent escape and a source symlink.

The compact witness CERTIFICATE.json is 179498 bytes, SHA256
**b1736a349e42999cf2301fa6dd2c719152e7c95a1b30f9bcf93ffa635a664c73**.
The complete regenerated mathematical record is 176247 bytes, SHA256
**1044fa49089e9976a1db3b57fcab627d9f6f216117764f0863e6429c543f428b**.
It is the entire sealed mathematical record, without omitted fields or selected
comparisons. [EXPECTED.json](EXPECTED.json) records every phase hash; regenerated
records and timing receipts stay in the ignored work directory. Compact validation
measurements and defining input commits are in [VALIDATION.json](VALIDATION.json)
and [PROVENANCE.json](PROVENANCE.json).

The remaining trust boundary comprises ordinary unformalized original-table,
tail, nonfixed-space, empty-lift, greatest-rank and label-transport bridges plus
exact author code inspection and replay. The trusted code is the source at the
chosen repository commit. Hash gates detect source damage; they do not establish
the mathematics or authenticate an adversarial replacement of the trusted checker.
Two PSD algorithms and a separate scalar reader are author checks, not independent
person review or proof-assistant verification. No timeout, UNKNOWN, memory failure,
floating result or incomplete search supplies an exclusion. The earlier review9872
concerns9826 only; it does not review this result or its9980 positive-tail premise.
