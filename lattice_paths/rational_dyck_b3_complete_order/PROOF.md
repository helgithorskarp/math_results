# Complete matching order at height three

Let `a>3`, `gcd(a,3)=1`, and write `a=3m+epsilon`, with
`epsilon in {1,2}`. A triple `(r,s,t)` denotes the path

    R^r U R^s U R^t U.

It belongs to `D(a,3)` precisely when

    r+s+t=a,  r,s,t>=0,  3r>=a,  3(r+s)>=2a.             (1)

The matching score `M` is the numerator of the continued fraction obtained
by replacing every equal adjacent step pair by `1,1`, and every unequal
pair by `2`. A matching cover `u <_M v` means there is no realized matching
score strictly between their scores. Ranks throughout this note start at
zero at the **greatest** score.

## 1. The complete chain

For `0<=z<=m` and `z<=y<=h_z=floor((a-z)/2)`, set

    x=a-y-z,
    C_y=(x,y,z),  P_y=(x,z,y),  N_y=(y,x,z).

The subscript notation is local to the fixed layer `z`. Put `n=m-z`.
The entire layer with minimum run `z`, in strictly decreasing matching
order, is the following list:

    C_z=P_z,
    P_(z+1), P_(z+2), ..., P_m,
    C_(z+1), C_(z+2), ..., C_m,
    N_(m+1), C_(m+1), N_(m+2), C_(m+2), ..., N_(h_z), C_(h_z).    (2)

An empty index range contributes nothing. If `a-z` is even, the last two
displayed paths coincide (`x=y=h_z`), and that path is listed only once.
The layers themselves occur in order `z=0,1,...,m`, still from greatest
matching score to least.

Consequently all matching scores on `D(a,3)` are distinct. Reversing (2)
and the layer order gives its complete Hasse chain. This is a uniform
classification for every admissible `a`, not a procedure that evaluates
and sorts continued fractions.

### The carrier and the size of a layer

For a decreasing rearrangement `(x,y,z)`, condition (1) permits starting
with `x`, and the canonical order `C_y` always works. Its other possible
order is `P_y` exactly when `y<=m`, since the last run must be at most
`a/3`. Starting with `y` is possible exactly when `y>=m+1`, and then the
only possible last run is `z`, giving `N_y`. Starting with `z` is
impossible unless all parts are equal, excluded by coprimality. Repeated
parts give exactly the duplicates suppressed in (2).

The layer therefore has

    1+2(m-z)+2(h_z-m)-1_(a-z even) = a-3z             (3)

paths. Summing gives

    N=|D(a,3)|=(a+1)(a+2)/6.

## 2. Continuants and the five local comparisons

Let `F_j` and `L_j` be the Fibonacci and Lucas numbers, with
`F_0=0,F_1=1,F_(-1)=1` and `L_0=2,L_1=1`. Write

    K_j = [[F_(2j+3), F_(2j+1)],
           [F_(2j+1), F_(2j-1)]],
    Q(r,s,t)=(K_r K_s K_t)_(2,1).                    (4)

Then `M(r,s,t)=Q(r,s,t)`. To see the bridge directly, put

    D=[[2,1],[1,0]], E=[[2,1],[1,1]].

The finite digit matrix has top-left entry `M`; prepend `D` to close the
period, so its bottom-left entry is still `M`. Factoring the closed step
word into its three runs gives `K_r K_s K_t`, since
`K_j=D E^(j-1) D` for positive `j`, and `K_0=E` also handles consecutive
up-steps. Thus zero runs require no limiting argument.

The following exact identities hold, with the usual signed extension of
Fibonacci numbers if one uses them outside the indicated applications:

    Q(y,x,z)-Q(x,y,z) = 2F_(2(x-y))F_(2z+3),
    Q(x,z,y)-Q(x,y,z) = 2F_(2(y-z))F_(2x-1).          (5)

For `d=x-y`, the three adjacent identities are

    Q(x,y,z)-Q(x-1,y+1,z)
      =2(F_(2d-4)F_(2z+3)+F_(2d-2)F_(2z+1)),

    Q(x,z,y)-Q(x-1,z,y+1)
      =6F_(2d-4)F_(2z+1),

    Q(x,y,z)-Q(y+1,x-1,z)
      =2F_(2d-2)F_(2z+1).                           (6)

These follow by multiplying (4) and applying Fibonacci addition, or by
substituting Binet's formula and comparing Laurent coefficients. The
included `identities.py` performs the latter comparison exactly over
`Q(phi)`, without a finite parameter cutoff or computer-algebra package.
The identities and their use as local comparisons are credited to the
earlier adjacent-fibre work in SOURCES.md.

The middle identity in (6) strictly orders the `P` block, including its
first member `P_z=C_z`: here consecutive parameters have `y<=m-1`, so
`d=a-z-2y>=4`. The first identity strictly orders the `C` block; `d>=2`
at each required step and its second summand is positive. The last
identity gives `C_y>N_(y+1)` whenever that next negative-chamber path
exists, including the interface `y=m`; here again `d>=2`. Finally, the
first identity in (5) gives `N_y>C_y` whenever these are distinct. If
`x=y`, they are the same path and it is the terminal duplicate.

## 3. The long internal bridge

The one comparison still needed inside a nontrivial layer is

    P_m >_M C_(z+1),  n=m-z>=1.                    (7)

The earlier nonlocal-cover theorem supplies the following exact identity;
we reproduce and verify it to expose the complete proof boundary:

    5(M(P_m)-M(C_(z+1)))
      =2F_(2z+1)(4L_(6n+2epsilon-5)+3L_(2n+2epsilon-2))
       +10F_(2z)F_(6n+2epsilon-4).                 (8)

All indices on the right are nonnegative; the first two Lucas indices
are at least 3 and 2 respectively. The first summand is strictly positive
and the second nonnegative. This proves (7), also when `n=1` and both
paths have the same sorted triple.

For an elementary derivation, sum the canonical drops in (6) from
`y=z+1` to `m-1`, then subtract them from the last-two-run swap gain in
(5) at `y=m`. The identities

    sum_(k=0)^(N-1) F_(r+4k)=(L_(r+4N-2)-L_(r-2))/5  (r even),
    5F_pF_q=L_(p+q)-(-1)^q L_(p-q)

give (8), with the standard negative-index convention when needed.
Alternatively the two cases `epsilon=1,2` of (8) are independently
checked as universal Laurent identities by `identities.py`.

Thus every successive comparison in (2) is strict. For `n=0` the two
middle ranges are empty, and `C_m=C_z` is followed by the negative block
if it exists; the last identity in (6) still applies.

## 4. A short positive certificate for the layer boundary

To complete the global proof without importing the prior Lagrange-chain
certificates, we give two explicit positive expressions for the boundary.
For `z<m`, write

    a-3z=2d+delta,  delta in {0,1},  d>=2.

The least path in layer `z` is `(z+d+delta,z+d,z)`. The greatest path in
layer `z+1` is `(z+2d+delta-2,z+1,z+1)`. Let `B_delta` be the first
matching score minus the second.

Put

    phi=(1+sqrt(5))/2, lambda=phi^2,
    X=lambda^z, Y=lambda^(d-2), U=X^2-1, V=Y^2-1.

Then

    (5 sqrt(5) X Y^2 / 2) B_delta = P_delta(U,V),    (9)

where the coefficients of `P_delta`, in the stated monomial order, are:

| delta | UV^2 | UV | U | V^2 | V | 1 |
|---|---|---|---|---|---|---|
| 0 | 23phi+15 | 54phi+33 | 25phi+15 | 17phi+24 | 50phi+40 | 25sqrt(5) |
| 1 | 61phi+38 | 129phi+78 | 65phi+40 | 58phi+41 | 130phi+75 | 65sqrt(5) |

Here `U,V>=0`; every displayed coefficient and the multiplier of `B_delta`
are positive. In particular the positive constant term proves strictness
even at `z=0,d=2`.

For direct verification of (9), Binet gives

    sqrt(5) K_j = lambda^j A + lambda^(-j) B,
    A=[[2phi+1,phi],[phi,phi-1]],
    B=[[2phi-3,phi-1],[phi-1,phi]].                 (10)

Substitute (10) in the two products defining `B_delta`, multiply by
`X Y^2`, and reduce `phi^2=phi+1`. Collecting in `U=X^2-1,V=Y^2-1`
gives the six coefficients above. `identities.py` reconstructs both
sides from (4), checks that every Laurent coefficient of their difference
vanishes, and checks each coefficient is positive using only `phi>1`.
SymPy helped discover these expressions; it is not used by the published
checker or needed to interpret this finite identity proof.

Sections 1-4 prove the entire matching chain without assuming the earlier
Lagrange classification or its computational certificates.

## 5. Closed rank and inverse rank

The number of paths preceding layer `z` is

    S_z=za-3z(z-1)/2.                              (11)

For a path whose sorted triple is `(x,y,z)`, its within-layer rank is

| Path / condition | Local rank |
|---|---:|
| `y=z` (the single path `C_z=P_z`) | `0` |
| `P_y`, `z<y<=m` | `y-z` |
| `C_y`, `z<y<=m` | `m+y-2z` |
| `N_y`, `y>=m+1` | `2(y-z)-1` |
| `C_y`, `y>=m+1`, `x>y` | `2(y-z)` |

At the terminal equality `x=y`, the common path has the `N_y` rank.
Adding (11) gives its global rank `R`. Thus `u <_M v` is a cover exactly
when `R(u)=R(v)+1`.

To invert, find the unique `z` with `S_z<=R<S_(z+1)` (the last endpoint
is `S_(m+1)=N`) from the quadratic formula and one integer square root.
The approximation obtained by replacing the real square root with its
floor can cross at most one integer boundary; the code corrects it by
direct integer comparisons. If `q=R-S_z` and `n=m-z`, the inverse is:

    q=0:          C_z;
    1<=q<=n:      P_(z+q);
    n<q<=2n:      C_(z+q-n);
    q>2n, q odd:  N_(z+(q+1)/2);
    q>2n, q even: C_(z+q/2).

This requires a bounded number of integer arithmetic operations and one
integer square root, independent of the number of paths. Bit complexity
still depends on the input length. No Fibonacci number needs to be formed.

## 6. Exact comparison with the Lagrange order

This section uses the previously proved and independently accepted
height-three Lagrange theorem: the score fibres are exactly sorted triples,
and their order from **greatest to least** is increasing `z`, then increasing
`y`. That prior theorem, rather than finite tests here, carries this
Lagrange-order premise. Its graph references and source are in SOURCES.md.

The descending fibre rank is

    ell(x,y,z)=floor(a^2/4)-floor((a-z)^2/4)
                -z(z-1)/2+z+(y-z).                (12)

Indeed the first four terms sum the numbers
`floor((a-t)/2)-t+1` of fibres over all `0<=t<z`.

Inspecting the complete matching list (2), every step to the next smaller
matching score has Lagrange-rank increment `+1` or `0`, except for the
single bridge `P_m -> C_(z+1)` in each layer with `n=m-z>=2`. That bridge
has increment `-(n-1)`. Therefore:

* For every distance `j=1,...,m-1`, there is exactly one matching cover
  whose Lagrange order is reversed, at fibre distance `j`.
* The **entire nonlocal family** (distance greater than one) is

      X_z=(a-1-2z,z+1,z),
      Y_z=(2m+epsilon-z,z,m),
      X_z <_M Y_z,    0<=z<=m-3.                  (13)

  It has `max(m-2,0)` members, with one at each distance `2,...,m-1`.
  An upper bound smaller than the lower bound means the family is empty.
* Every other matching cover with unequal Lagrange scores is a Lagrange
  cover in the same direction, except for the unique reversed adjacent
  Lagrange cover when `m>=2`.

The previous theorem proved existence of the family (13), together with
its distance-zero and distance-one boundaries. The new conclusion is
exhaustiveness, supplied by the complete chain.

### Counts and the full gap distribution

Set

    H=floor((m+epsilon-1)^2/4), T=1+H.

There are exactly `T` matching covers within a tied Lagrange fibre. To
count them, in layer `n=m-z` the negative chamber contributes
`floor((n+epsilon-1)/2)` such covers; the positive chamber contributes
one additional tied cover exactly when `n=1`. Summing uses
`sum_(n=0)^m floor(n/2)=floor(m^2/4)` and
`sum_(n=0)^m floor((n+1)/2)=floor((m+1)^2/4)`.

Thus the complete histogram of increments of (12) along the descending
matching chain is

| Increment | Multiplicity |
|---|---:|
| `+1` | `N-T-m` |
| `0` | `T` |
| `-j`, each `1<=j<=m-1` | `1` |

These multiplicities sum to `N-1`. In particular, the number of common
oriented covers is exactly `N-T-m`.

There are `m(m+1)/2+H` two-path Lagrange fibres, so their total number of
score levels is `N-m(m+1)/2-H`. The matching ranks of `P_y` and `C_y`
in a positive chamber differ by exactly `n=m-z`. There are `n` such
fibres in that layer. In the negative chamber their ranks differ by one.
Consequently the matching-rank gap among all two-path Lagrange fibres
has multiplicity `T` at gap one and multiplicity `j` at every gap
`j=2,...,m`.

Finally, an unordered pair with different Lagrange scores is ordered
oppositely by the two orders exactly when, in one layer,

    C_i and P_j,   z<i<j<=m.

There are `binom(n,2)` such pairs in layer `n`. Thus the **total** number
of discordant unequal-fibre pairs is

    sum_(n=1)^m binom(n,2)=binom(m+1,3).            (14)

This pair classification, the cover histogram, and (13) all follow from
the full chain; they are not inferred from an experimental fit.

## 7. Verification and scope

`identities.py` checks nine universal identities in the explicitly
implemented quadratic field and Laurent ring, including the twelve
positive boundary coefficients. `verify.py` independently generates
literal Dyck words from up-step positions, evaluates scalar continuants,
and compares the complete score sort with (2), (11), and the inverse.
For its smaller Lagrange range it examines every cyclic **digit** cut
(including both digits of each `1,1` block), using exact rational squares,
and checks every fibre, cover, within-fibre gap, and discordant pair.

The universal matching theorem rests on the written carrier argument and
finite identities, not on bounded enumeration. The Lagrange comparisons
add the explicitly cited prior theorem. The code is ordinary exact Python,
not a proof-assistant kernel. No solver, floating-point calculation,
random sample, external data, large certificate, or omitted exhaustive run
is used in the published verification. No conclusion for height four or
higher is asserted.
