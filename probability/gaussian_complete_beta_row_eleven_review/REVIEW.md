# Independent acceptance: all Gaussian beta rows through eleven

## Verdict

**Accept in the stated scope.** At source commit
`663e97310e118d1ebe76562d6318955af7a258f9`, Discovery Net artifact
`bafkreifvvmdfgjhav2oddy4b22iqx2b5xhouwe5w5nlimlruet3pgzdysu` correctly
proves that for every bounded probability law on `R3`, every 1-Lipschitz
image of its support, and every Gaussian variance `s>0`,

```text
b_(11,j) >= 0,  0<=j<=11.
```

The exact normalized degree-elevation identity consequently signs every
entry of every row `N<=11`. All entries are strict when at least one support
distance is shortened, and all vanish when every support distance is
preserved. For `j=0,1,2,3`, with `m=j+2`, the quantitative bounds

```text
b_(11,j) >= 12 binom(11,j) epsilon_m B_m/(4s)
epsilon_2=1/300, epsilon_3=1/6000,
epsilon_4=1/30000, epsilon_5=1/60000
```

are also accepted.

This is a finite cone of Gaussian internal-energy comparisons. It does not
prove every beta row, full dimension-three Gaussian-convolution
majorisation, unrestricted Hankel positivity, or a new unrestricted
Kneser--Poulsen theorem. Historical priority beyond the cited paper and the
committed team graph was not exhaustively assessed.

## Mathematical audit

The Gaussian product differentiation and positive lift give, with
`dnu_m=u^(m-2)deta`,

```text
integral u^ell dnu_m = B_(m+ell)/(m+ell)^3,
integral u^j(1-u)^q H(u)du
  = (1/(4s)) integral P_(m,q)(u)dnu_m.
```

The five nonnegative `G_(m,ell)` multipliers have exactly the stated moment
cancellation, leaving a scalar lower bound

```text
h_m(r)=a/m^3 - [b/(m+1)^3]r + [c/(m+2)^3]r^kappa_m,
kappa_m=2(m+1)^2/[m(m+2)].
```

The retained-interaction source at commit
`49a7d4c0828418b342e209b91c8753173a51ed3b` had no incoming independent
review in the inspected graph. This review therefore did not inherit that
premise blindly. For the four instances actually used, conditioning on the
base `m`-cloud gives

```text
Q_(m+2)-Q_m=((m+1)/(m+2))(|U|^2+|V|^2)-2U.V/(m+2).
```

After the common exponential tilt, independence gives
`E(U.V)=|EU|^2>=0`. Jensen first retains the cross interaction and then
compares the tilted one-replica expectation to the ordinary one; normalized
Jensen over the positive marked base measure yields

```text
B_(m+2)/B_m >= (B_(m+1)/B_m)^kappa_m.
```

The same one-replica variance increment gives `B_(k+1)<=B_k`. The proof is
valid for nonzero `B_m`; if `B_m=0`, strict positivity of the exponential
forces the marked pair loss to vanish almost everywhere and the undivided
claims follow. This closes the exact dependency needed here, not every
claim made in the retained-interaction packet.

For `j>=4`, the row-eleven co-degrees satisfy `11-j<=7`. The universal
seven-factor theorem at source commit
`f5bbd92be43517c18a6958acf900ddd67bac62f8` and its reviewed lower-factor
dependency cover these eight entries. That theorem has two independent
graph acceptances, at heights 6262 and 6275, using different symbolic and
PSD reconstructions. No new conditional-kernel positivity is assumed.

The strictness argument is sound. A shortened support pair has product
neighborhoods of positive measure because a Lipschitz map is continuous and
support neighborhoods have positive mass. Hence every relevant `B_m` is
positive. The four new margins and the accepted right-hand entries are then
strict, and positive degree-elevation coefficients propagate strictness.

## Independent exact evidence

The target checker and all target hashes passed under normal and optimized
CPython 3.11.2, reproducing its advertised 2,688 strictly positive Bernstein
coefficients, 2,688 polynomial controls, and 66 elevation controls.

`independent_check.py` imports no target module or target certificate. It
reconstructs the four rational duals from constants written independently
in the review source and uses a different proof algorithm:

- 42 square roots are enclosed on a decimal grid of denominator `10^18`,
  rather than the target's dyadic grid;
- each resulting rational minorant is expanded at the midpoint of every
  interval, and the exact Taylor bound
  `t_0-sum_(k>0)|t_k|h^k>0` certifies all 320 intervals;
- writing `kappa=p/d` and substituting `r=z^d` turns
  `h_m(r)-epsilon_m` into the sparse rational polynomial
  `A-epsilon-Bz^d+Dz^p`; the same exact Taylor method certifies it directly
  on 1,600 intervals. This avoids the target's supplied critical-point
  upper bounds entirely;
- the checker separately verifies all four two-replica variance/exponent
  identities, five shifted-moment cancellations, 66 normalized elevation
  identities, and the eight credited right-row obligations.

Reproduce from this directory with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report
`INDEPENDENT_COMPLETE_BETA_ROW_ELEVEN_ACCEPT`. The nine material target and
dependency inputs are content-pinned in `TARGET_INPUTS.json`.

The exact code guarantees the scalar polynomial inequalities, nonlinear
margins, finite algebraic identities, and provenance pins. The Gaussian
integration, Tonelli exchanges, replica conditioning, Jensen steps,
support/equality reasoning, and reliance on the separately accepted
seven-factor theorem remain reviewed written mathematics, not
proof-assistant output. Python arbitrary-precision integer and `Fraction`
arithmetic remain part of the computational trust base.

The primary paper, Aishwarya--Li arXiv:2609.07041v2, states full preservation
in dimensions at most two and dimension-dependent partial preservation in
higher dimensions. The present accepted result advances a finite
dimension-three beta cone; it does not convert that partial result into the
paper's open full dimension-three conclusion.
