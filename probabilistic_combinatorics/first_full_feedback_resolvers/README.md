# When does a random graph first admit a resolving full-feedback probe?

Let `R` count vertices of `G(n,p)` whose full directional responses distinguish
every target in one initial round. Put `R=0` for disconnected graphs and
`L=log n`. We prove the exact sparse critical-window law

```
np^2 = L+s/L+o(1/L)
  ==> R converges to Poisson(2 exp(s-1)).
```

The counts of resolving probes of eccentricity two and three converge to
**independent** Poisson variables, each of mean `exp(s-1)`. All other
eccentricities disappear with high probability in the window. Allowing one
distance-three target is essential: keeping only the earlier two-hop
certificate misses half of the limiting intensity.

There is also a uniform law throughout every fixed band `|np^2-log n|<=C`.
With `lambda=np^2`, set

```
u=n exp(-lambda),  v=n lambda exp(-lambda),
theta=n(1+u) exp(-u-v).
```

Then `E R ~ theta` and `P(R>0)=1-exp(-theta)+o(1)`, uniformly in the band.
When `theta` diverges, `R/theta` tends to one in probability.

Read [the full proof](PROOF.md) and [prior-work alignment](LITERATURE.md).
The proof conditions on finitely many probe neighborhoods and controls
feedback errors relative to the rare success probability. It does not assume
that different probes are independent.

This is an existence theorem for a successful **initial single probe**.
It does not settle the adaptive multi-round localization problem, provide a
coupled-process hitting-time theorem, or assert monotonicity under adding
edges. It also differs from the previously proved requirement that *every*
vertex resolve in one round.

## Reproduce the finite audit

Python 3.11 or later; standard library only. Run from this directory:

```bash
python3 verify.py --check
sha256sum -c SHA256SUMS
```

To inspect the compact expected record:

```bash
python3 verify.py
```

The checker exhausts all 33,866 labelled graphs of orders two through six,
including disconnected graphs, and performs 202,012 probe checks with
independent breadth-first shortest-path responses. It checks 30 exact
rational degree-mixture probabilities, 120 conditional proxy sums,
165 overlapping-neighborhood identities, 720 marked coefficient identities,
and the additional collision, conditional-edge, and zero-target-path formulas.
Six fixtures include the three-cube, a disconnected proxy false positive,
and a connected repeated-code false positive. Eight malformed inputs are
rejected. The census through order six contains no eccentricity-three
resolver; the three-cube explicitly exercises that mechanism at order eight.

`EXPECTED.json` contains counts and SHA-256 digests; `SHA256SUMS` protects
all six other files. The expected terminal line begins
`PASS: exact BFS, rare-event proxy, overlap, and marked coefficients`.
The same output is checked with Python optimization enabled.

The universal result rests on the written proof. Finite enumeration checks
definitions and finite identities, not the asymptotic conclusion. There is
no solver, floating-point arithmetic, randomness, network dependency,
external dataset, large certificate, or proof-assistant claim in the audit.
The remaining computational trust boundary is readable Python, its standard
library and interpreter, the operating system, and hardware. Independent
mathematical review is pending; novelty is relative to the searched sources.
