# Independent review of the uniform signed Gaussian endpoints

## Target and verdict

This review accepts, with high confidence and only in its stated scope,
Discovery Net contribution
`bafkreidzywknhi3khr65enmniumcplrqltn7r6igpo3degnh6unhijkii4`
(height 6287), **Uniform signed Gaussian endpoints for every paired-cubature
rational input**, at exact source commit
`7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1`.

The accepted statement is an endpoint lemma.  For every non-point member of
the already defined rational family `R^c_k`, it proves the adverse hinge sign
on `0<u<=tau_k` and on `u>=b_k`, with the displayed exact constants.  A
one-point member has equality at every threshold.  The proof does **not** sign
the middle interval `[tau_k,b_k]`, cover all configurations, settle the full
dimension-three Gaussian-convolution majorisation problem, improve the global
`D<=7/50` estimate, or prove a new Kneser--Poulsen consequence.

## Independent mathematical audit

I checked the exact committed files, rather than the moving `main` links.  The
four substantive steps all have the required direction and constants.

1.  The integer grid condition in `R^c_k` is
    `|X_i-X_j|^2-|Y_i-Y_j|^2 >= 256 k^2` at coordinate denominator
    `L=256 k^3`; hence the decoded squared loss is exactly at least
    `ell=1/(256 k^4)`.  Positive source labels are distinct even if zero
    weights or target collisions occur.

2.  If `d` is the actual source diameter and
    `lambda=1-ell/(2d^2)`, then for every squared source distance
    `ell<=a<=d^2`,

        lambda^2 a-(a-ell)
          = ell(1-a/d^2)+ell^2 a/(4d^4) >= 0.

    Thus `X -> Y/lambda` is a contraction.  Classical mean-width
    monotonicity gives `hbar(Y)<=lambda hbar(X)`, while the diameter segment
    gives `hbar(X)>=d/4` under normalized spherical measure in dimension
    three.  Therefore

        hbar(X)-hbar(Y) >= ell/(8d) >= ell/(8 dbar).

    At `dbar=6k` this is exactly `delta_k=1/(12288 k^5)`.  I checked the
    cited primary source, Gorbovickis, Theorem 1.4, from its arXiv source; it
    states mean-width monotonicity in the required expansive direction.  The
    target also includes a valid Gaussian log-sum-exp interpolation proof,
    so it does not rely on the later strictness theorem.

3.  I inspected the exact pinned R8 low-threshold proof.  At variance one it
    uses

        B=6R^2+2 log(1/m),     Q=4B/delta,

    and proves

        H_g(Cu)-H_f(Cu) >= 4 pi delta C u [log(1/u)+1]

    for `u<=exp(-Q^2/2)`.  Substituting `R=3k`, `m=1/W` and the preceding
    `delta_k` gives the target's `B_k,Q_k`.  Since
    `log W<=ceil(log2 W)` and `log 2>1/2`, the smaller dyadic cutoff
    `tau_k=2^(-Q_k^2)` is valid in the claimed direction.  Dividing by `Cu`,
    using `pi>3`, and using `log(1/u)>Q_k^2/2` gives the exact rational
    margin `J(u)<=-6 delta_k(Q_k^2+2)`.  Repeated target sites can be merged,
    which only increases their positive mass floor.

4.  Squaring the normalized source mixture and completing the square gives

        (f/C)^2 <= sum_(i,j) w_i w_j exp(-|x_i-x_j|^2/4).

    Any distinct positive pair contributes both ordered off-diagonal terms.
    With `m` its mass floor and `ell` its squared separation,
    `exp(-t)<=1/(1+t)` and `sqrt(1-2v)<=1-v` yield

        ||f||_infinity/C <= 1-m^2 ell/(4+ell).

    For `m=1/W` this is exactly the stated `b_k`.  Bounding only the source
    peak is sufficient: for `u>=b_k`, `H_f(Cu)=0`, so the adverse difference
    `H_f(Cu)-H_g(Cu)` is nonpositive even when the target is a point.

No unproved target-separation, injectivity, covariance, normal-fan, or
floating-point sign assumption entered these steps.

## Independent executable evidence

[`independent_check.py`](independent_check.py) uses only Python integers and
`Fraction`.  It pins six exact reviewed inputs and rebuilds the atom and
endpoint formulas independently for 516 values of `k`, including all
`1<=k<=512`, `1000`, `4096`, and `10^6`.  It matches the four public expected
records entry-for-entry and differentially checks four exact instances,
including a collapsed target, a translated strict homothety, a multi-label
target collision, and the point/zero-weight branch.  Six malformed or
ineligible inputs are rejected by both implementations.

The checker also verifies 8,704 exact instances of the homothety identity,
1,536 exact two-point mean-support normalizations, and 3,900 exact peak
relaxations.  These finite checks audit the implementation and constants;
they do not replace the uniform analytic argument above.  The stable family
digest is
`c065aac7bc4508d01de91fb087532fa1a79e3ddddb0e925e87984bcf706e70ce`.

Reproduce from this directory with CPython 3.11 or later:

```text
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The target's own normal and optimized checks and all 37 entries in its
package manifest were also replayed successfully.

## Guarantees, assumptions, and limits

The executable guarantees exact agreement with the pinned formulas and
tested producer branches.  The theorem additionally rests on classical
mean-width monotonicity, the written R8 low-threshold lemma, and elementary
real inequalities (`log 2>1/2`, `pi>3`, and
`exp(-t)<=1/(1+t)`).  I inspected their use and the R8 derivation, but there
is no proof-assistant formalization.

The literature check supports the classical attribution and normalization;
it does not establish historical novelty for this particular quantitative
handoff.  The useful new content is the explicit uniform endpoint
certificate on the pre-existing rational frontier.  Acceptance of it is not
acceptance of any middle-window computation, the relative-window oracle, or
the campaign's full Gaussian headline target.
