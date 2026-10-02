# Six integer orders suffice for the general deletion frontier

Actual author **six-downset-3**, role **researcher**, 2026-10-02.
Status: ordinary author proof with exact algebra and one original-matrix
baseline. The real PSD, monotonicity, root-branch, counting and imported
infinite arguments are unformalized. Independent review of this extension
is pending. The common signing identity and the prior finite reviews do
not establish a new verdict.

## Exact quantified theorem

Let a,b,c be core points and W a disjoint set of integer size q>=4. Include
the empty set, every singleton and pair, and every triple containing at
least two core points. Delete bcx for all x in an arbitrary Z subset W of
integer size k, where 3<=k<=q. Write this downset as D(q,Z). Put

```
N = (q²+13q+16)/2-k,    s = 3q+4,
DB = 28k²-36k+17,
b(k) = floor((6k-7+sqrt(DB))/2)
     = (6k-7+isqrt(DB))//2.
```

Use the explicit affine table and scalar four-edge repair of the credited
9434/9195 construction, defined below. Then:

* For every admissible q<=b(k)-6 and every Z, **no real parameter pair
  kappa,t gives a capped H matrix in this specified ansatz**.
* For every q>=b(k)+1 and every Z, the credited9195 adaptive construction
  gives such a matrix with rational entries, greatest lower/cap ranksN-1
  and a simple unit eigenvalue.

Consequently at most the SIX integers `b(k)-5,...,b(k)` remain between
these two threshold criteria, for every integer k>=3. Some of these can
already be excluded by the stronger necessary test or resolved by known
small-k classifications. We do not claim that a corridor member passes
the necessary test, is feasible, or that all six values actually remain
open. No existence or nonexistence assertion for arbitrary H follows from
failure of this ansatz.

The new unbounded deduction uses a positive cubic for ALL k>=5, a short
rational margin for k=4, and only the single original case k=3,q=5.
Neither an all-k sweep nor an extrapolation from the small cases is used.

The defining current problem is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), rechecked live
2026-10-02, still lists the September23 v1 with H/I as conjectures.
The classical [rank-three work](https://arxiv.org/abs/1703.00494) is prior
art; no historical priority or general H/I resolution is asserted.

## Explicit ansatz and retained premises

Identify a,b,c with bits1,2,4. For a nonempty original member A, its type
is `((A&7).bit_count(),(A>>3).bit_count())`. The two coefficients of every
disjoint type-table entry are explicitly expanded in the credited
[literal.py](https://github.com/helgithorskarp/math_results/blob/41a580c695e0b0d38858af543a8fabcf880631ae/round-two/six-downset-3/small-deletion-boundary/literal.py),
SHA256 `46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39`.
That table function is defined for every integer q>=4; its original-matrix
builder retains its separate published finite guard. Denote the affine
entry by `Q_kappa(A,B)=a(A,B)+kappa*d(A,B)`.

On surviving nonempty original members, set C_kappa,t to have diagonal
s-1, entry-1 on distinct intersecting pairs and entry Q_kappa(A,B)-1 on
disjoint pairs, plus tR. The only nonzero entries of the symmetric R are

```
R[a,b]=R[a,c]=1,
R[b,ac]=R[c,ab]=-1.
```

Let E have first row minus the nonempty all-1 row, followed by the identity,
and let J denote an all-1 matrix of the required order. Define

```
L_kappa,t = J_N + E C_kappa,t E',
M_kappa,t = (L_kappa,t-sI_N)/(N-s),
U_kappa,t = N I_(N-1)-J_(N-1)-C_kappa,t.
```

The actual empty member and its allowed loop are retained. The ansatz
has the regularity and intersecting-support equations of H. The additional
cap is M<=I. Since E has full column rank with range1-perp,
`L>=0 iff C>=0`. Also `NI-L=E U E'`, so `M<=I iff U>=0`.
These are ordinary real congruence arguments, not matrix symmetry
assumptions. The star sizes are s at a, s-k at b,c, q+5 at each x in Z
and q+6 at every other outside point, so s is the largest star size.

The all-real necessary condition is imported precisely from
[LEMMA9434](https://github.com/helgithorskarp/math_results/blob/6e029f9f88a784f54c562dc3e8c28536bfb1e08c/round-two/six-downset-3/five-deletion-boundary/PROOF.md),
source `6e029f9f88a784f54c562dc3e8c28536bfb1e08c`,
`bafkreifw5zt43azq7w225ttypnia2bvrwgdovedwic73irlsxtknftmss4`.
For every q>=4,1<=k<=q and every Z, its original lower dual forces
kappa>=0. Its four-coordinate original upper Gram gives

```
Q(kappa) = Q0-kappa*D4
             -kappa²*h²*[q/gap+4q/d] >= 0,
D4 > 0,
h = 1/(3q+5),   r = 3+2/q,
gap = N-s = [q²+7q+8-2k]/2,
d = N-2s+r = q(q+1)/2-k+r,
ww = (s-r)/(q-1),
e = [q²+(13-6k)q+2k²-10k+14]/2,
a0 = (2k+1)q+k-2k/q,
Q0 = e-a0²/(q*gap)
        -k(q-k)*ww²/(q*gap)-4q(k-1)²/d.
```

The coordinates are1, indicators of pairs ax inside and outside Z, and
the indicator of bx,cx,abx,acx for every x in W. The lower3x3 block is
exactly diagonal and parameter independent. The zero outside-Z coordinate
is dropped at k=q. Every denominator is positive on the WHOLE domain:
gap>0 and `N-2s>=q(q-1)/2>0`. The repair pairing vanishes. Since Q is
strictly decreasing on kappa>=0, any feasible parameters require Q0>=0.
In particular e>0, because a0>2kq>0 and the other subtractions are
nonnegative. These statements are imported universal lemmas, not inferred
from our one finite baseline. The underlying8757/9145 spectral premises
are retained through9434 and9195; no new verdict on them is supplied here.

The constructive premise is
[LEMMA9195](https://github.com/helgithorskarp/math_results/blob/6df5f969a5140ec9a7b70973a34cf10257ec5f74/round-two/six-downset-3/adaptive-deletions/PROOF.md),
source `6df5f969a5140ec9a7b70973a34cf10257ec5f74`,
`bafkreihheqg5ispobqtthf6b4kucvyrgcllkg7lxxfuveveio7l26m3evm`.
It constructs the stated capped greatest-rank matrices when

```
B0 = [q²+(7-6k)q+2k²-12k+8]/2 > 0.
```

We import its adaptive parameters and infinite proof; we do not
re-prove or independently audit that tail in this source packet.

## The universal obstruction for k>=5

Suppose capped real parameters existed at q<=b(k)-6. Write
`rB=(6k-7+sqrt(DB))/2`. Then q<=rB-6 and rB<6k, the latter because

```
(6k+7)²-DB = 8k²+120k+32 > 0.
```

The upward quadratic e has `e(k,k)=(-3k²+3k+14)/2<0` for k>=3.
Its upper root is

```
rE = (6k-13+sqrt(28k²-116k+113))/2.
```

Since q>=k and feasibility requires e>0, we have q>rE, where e is
increasing. In particular rB-6>=q>rE, so this monotonicity gives

```
e(q,k) <= e(rB-6,k)
        = 10k-15/2-(3/2)sqrt(DB).
```

The root substitution is exact: for an indeterminate R,
`2e(R-6,k)-2(19k-18-3R)=2B0(R,k)`. Substituting R=rB yields the displayed
formula. The coefficient-12k in B0 is essential; e-B0=3q+k+3.

For every k>=5,

```
DB-(5k-2)² = (3k-13)(k-1) > 0,
sqrt(DB)>5k-2,
e(q,k)<(5k-9)/2.
```

On the other hand k>=4,q>=4 give

```
gap <= q(q+7)/2,
d < q(q+1)/2,
a0 > 2kq.
```

For d, the difference from q(q+1)/2 is `-k+3+2/q<=-1/2`.
Since q<6k, the two actual Schur losses satisfy

```
a0²/(q*gap)+4q(k-1)²/d
 > 8k²/(6k+7)+8(k-1)²/(6k+1) = L(k).
```

The exact identity

```
2(6k+7)(6k+1)[L(k)-(5k-9)/2]
 = 12k³+20k²+269k+175 > 0
```

holds for every positive k. Thus the two losses alone exceed e, and
Q0<0. This contradicts the necessary Q0>=0 and excludes every real
kappa,t at every stated q for every k>=5. No finite sampling is used
in this unbounded step. Its analytic completeness bridge is the explicit
root-branch and sign argument above.

## The k=4 margin and sole k=3 exception

At k=4, DB=321>17². The same hypothetical feasibility and root-branch
argument give

```
e(q,4) <= e(rB-6,4)<40-15/2-(3/2)*17=7.
L(4)=128/31+72/25=7+7/775>7.
```

The same two-loss contradiction therefore excludes every admissible
q<=b(4)-6. This is not a new classification of k4; the sharp q13 result
is already [LEMMA9379](https://github.com/helgithorskarp/math_results/blob/0b68f6cf5044feffbb02b397364a7b3149b1f684/round-two/six-downset-3/four-deletion-boundary/PROOF.md),
`bafkreibmitgnbsrhey3sbrfwxpiss653aahaw74iegvit2vtjaul4zgh4q`.

At k=3, b(3)=11, so only q4,5 are admissible below b(3)-5.
At q4, e=-1 contradicts e>0. At q5,N50,s19, reproduce the ORIGINAL
49-coordinate C0,Delta,R,U0 from the SHA-pinned literal table. Let yZ
and yW indicate the3 and2 pairs ax in and outside Z, and let v indicate
the20 members bx,cx,abx,acx. The rational vector

```
w = 1-(29/155)yZ-(97/310)yW+(10/77)v
```

has exact original pairings

```
w' U0 w = -322737/23870,
w' Delta w = 939346/59675 > 0,
w' R w = 0.
```

The original lower vector `z=1-S_b-S_c+F_triangle` has C0z=Rz=0 and
`z'Delta z=159/10>0`. It forces kappa>=0. Thus
`w'U_kappa,t w=w'U0w-kappa*w'Delta w<0` for EVERY real t and kappa>=0,
contradicting the cap. These are whole original nonempty-coordinate
pairings, not merely a compressed-matrix sign. Complete original
family generation, all four Gram forms and the affine orientation are
reproduced in [baseline.py](baseline.py). The q5 result is already implied
by the credited [9259 small-k boundary](https://github.com/helgithorskarp/math_results/blob/41a580c695e0b0d38858af543a8fabcf880631ae/round-two/six-downset-3/small-deletion-boundary/PROOF.md),
`bafkreifbeem3terc2paxr43rs3lsr6gkdgufl3av5gobbwdqcffw46kqoi`.
Its reproduction is validation, not new finite mathematics.

Every Z of size k is covered by permutation of W. The analytic formulas
depend only on k; the reproduced finite case is transported by the same
permutation, without an incomplete list of labeled cases.

## Strict tail and the six-integer conclusion

For every k>=3, `B0(k,k)=-(k-1)(3k+8)/2<0`. Therefore the upward
quadratic B0 is positive on q>=k exactly when q>rB. Its strict integer
cutoff is b(k)+1, supplied by9195. Replacing sqrt(DB) by isqrt(DB) does
not change the floor after addition of an integer and division by2:
the removed fraction is less than1/2 and the retained number is an
integer or half-integer. The branch and strict endpoint are important;
at k8,q40, DB=1521 and B0=0, so9195 does not certify that endpoint.

Combining the new all-real obstruction q<=b(k)-6 with this credited
construction q>=b(k)+1 leaves at most the six integers b(k)-5,...,b(k).
No monotonicity of actual ansatz feasibility is assumed, and there is
no claim that the scalar Q condition is sufficient.

This is an unbounded constant-width reduction. The prior k3,q8;
k4,q13; k5,q19 sharp boundaries are retained as distinct earlier
results9259/9379/9434. They do not imply an arbitrary-k cutoff formula.
No new k6 certificate, uniform corridor construction, optimal width,
maximum kappa, full parameter face, or general H/I result is asserted.

## Exact evidence and trust boundary

[verify.py](verify.py) checks exact coefficient identities, the positive
cubic, the k4 rational margin, strict root endpoints and one49-coordinate
original dual. It imports only the one SHA-pinned standalone literal
input, with its existing finite guard unchanged. No proof corpus, dense
input matrix, inverse expansion, solver output or numerical PSD result
is needed. The full [frozen record](EXPECTED.json) includes9604 original
input positions, the complete finite family comparison, actual four-vector
Grams, matrix digest and12 semantic damage rejections. Seven endpoint
calibrations are labeled as such; they do not prove the unbounded theorem.

Normal and optimized execution must agree with the ENTIRE frozen record.
Every condition uses exceptions and remains active under-O; there are
no assertions or child processes. [RESULTS.json](RESULTS.json) records
the measured serial replay and [SHA256SUMS](SHA256SUMS) covers all source
and the external pinned input. Standard-library exact integer/Fraction
arithmetic is the computational trust boundary. There is one bounded
mathematical process, native threads1, fixed45s and unchanged1CPU2GiB.

The universal necessary premise9434 and constructive infinite premise9195
remain explicit imports with their ordinary unformalized bridges. This
extension has no independent review yet. Earlier reviews of different
finite or near-cube claims confer no verdict here. The useful increment is
the universal six-order frontier and the short all-k proof, not baseline
replay, source packaging or numerical search.
