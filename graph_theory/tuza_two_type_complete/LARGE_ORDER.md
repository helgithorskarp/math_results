# The large-order bridge, with attribution

This appendix restates the mathematical argument of Discovery Net h5548,
`bafkreihudoilzxemequeeqi5k3bcgefhszofzmew24ddiu6pus62q74zgq`,
*A uniform Tuza gap for two-neighborhood split graphs: all clique orders at
least 113*. Its [original proof](../tuza_two_type_uniform_gap/PROOF.md) is
prior work in this repository. This bridge is not claimed as new here.
The rederivation below makes the all-order dependency explicit and does not
require the original code or its regression data.

Use the capped notation of the main proof. Put `x=m/s`, `y=n/t`, interpreting
a ratio for an empty type as zero, and define

    H=(x s^2+y t^2-xy c^2)/2, delta=2H/k^2,
    E=ms+nt, alpha=u/k, r=E/(uk) when u>0.

In a clique on `z` labeled vertices, the edges of each color `i+j mod z`
form a matching. Independent choices of `m` and `n` such colors yield a
centered packing of size at least

    x binomial(s,2)+y binomial(t,2)-xy binomial(c,2)
      = H-(xs+yt-xyc)/2 >= H-k/2.                          (A1)

For the last step the subtracted expression increases with `x,y` in
`[0,1]`, and at `(1,1)` is `s+t-c=u<=k`.

Every graph `R` on `k` vertices has a triangle packing of size at least
`t(R)/k`: triangles with the same sum of labels modulo `k` are edge-disjoint.
Apply (8) of the main proof after removing the base edges of a centered
packing of size `h0`. The resulting total packing bound is

    h0+e(4e-k^2)/(3k^2)
      = k^2/6-k/2+1/3+4h0/(3k)+4h0^2/(3k^2),
    e=binomial(k,2)-h0.

This quadratic increases for `h0>=-k/2`. Substitute (A1) and also use the
centered packing alone to get

    2nu(G) >= k^2 p0(delta)-k,
    p0(delta)=max(delta,1/3+2delta^2/3).                    (A2)

For a cover, put `ell` of the union's vertices on one side of a clique cut,
all outside vertices on the other, and all centers opposite the first side.
A uniform `ell`-subset of the union deletes `E(1-ell/u)` spokes on average.
If `ell>=u`, include the entire union and fill from outside, losing no
spokes. If `alpha<=1/2` the union fits on a balanced side. Otherwise minimize
the real normalized cost over `1/2<=z=ell/k<=alpha`. This yields

    F=1/4                                     if alpha<=1/2;
    F=1/4+r(alpha-1/2)-r^2/4                   if r<=2alpha-1;
    F=alpha^2-alpha+1/2                        otherwise.

Rounding an interior minimizer of a quadratic of leading coefficient one
costs at most `1/4`; the union endpoint is already integral. Therefore

    tau(G) <= k^2 F-k/2+1/4.                               (A3)

The two-set relation `st-cu=(s-c)(t-c)>=0` and
`E^2>=(2sqrt(mn st))^2` imply

    mn c^2/(st) <= E^2/(4u^2),
    delta >= alpha r-r^2/4,    0<=r<=2alpha,
    0<=delta<=alpha^2<=1.                                 (A4)

Zero denominators correspond to absent terms. To see the first inequality,
use `st>=cu`, so `E^2/(4u^2)>=mn st/u^2>=mn c^2/(st)`.
The upper bound on delta follows by increasing `x,y` to one and using
`u^2-(s^2+t^2-c^2)=2(s-c)(t-c)>=0`.

For `delta<=3/4`, these inequalities give the envelope

    F <= g(delta)=delta+sqrt(1-delta)-3/4.                 (A5)

For completeness, if `alpha<=1/2`, this follows from
`sqrt(1-delta)>=1-delta`. Otherwise first suppose
`delta<=alpha^2-1/4`. Solving (A4) on `r<=2alpha` gives
`r<=2alpha-2sqrt(alpha^2-delta)<=2alpha-1`. Substitute this in the increasing
first branch of `F` and then increase `alpha` to one:

    F<=1/4+delta-alpha+sqrt(alpha^2-delta)<=g(delta).

The last expression is nondecreasing in `alpha` on its domain, as follows
by differentiation or rationalization. In the other case,
`delta>=alpha^2-1/4`, use

    F<=alpha^2-alpha+1/2<=delta+3/4-sqrt(delta+1/4)<=g(delta).

For the last inequality,
`(delta+1/4)(1-delta)=1/4+delta(3/4-delta)>=1/4` implies
`sqrt(delta+1/4)+sqrt(1-delta)>=3/2`. Also `F<=1/2` throughout.

If `0<=delta<=1/2`, then
`sqrt(1-delta)<=1-delta/2-delta^2/8`: both sides are nonnegative, and the
square of the right side minus `1-delta` is `delta^3(8+delta)/64`.
Consequently

    p0(delta)-F >= 1/12-delta/2+19delta^2/24
                = (19/24)(delta-6/19)^2+1/228.

For `1/2<=delta<=3/4`, `p0(delta)=delta` and (A5) give a gap at least
`3/4-sqrt(1/2)>1/24>1/228`; the strict inequality follows from
`sqrt(1/2)<17/24`. For `3/4<=delta<=1`, use `p0(delta)=delta` and `F<=1/2`
to get a gap at least `1/4`. Combining (A2) and (A3) proves

    2nu(G)-tau(G) >= k^2/228-k/2-1/4.

Its value at `k=113` is `-85/114`; its derivative is positive for all
`k>=113`. Since the left side is integral, this proves the required
large-order branch. The cap lifts the cover and embeds the packing in the
original graph, so arbitrary original multiplicities are covered.
