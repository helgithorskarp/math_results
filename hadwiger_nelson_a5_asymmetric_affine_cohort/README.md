# One asymmetric A5 cohort: exact physical graphs

For the 64 signed systems below, there are **340 distinct complex parameters**
with real Cartesian coordinates. Every resulting complete strict plane
unit-distance graph has chromatic number **exactly three**. This closes this
frozen cohort as a source of a sub-509 five-chromatic graph. It makes no claim
about the other A5 residual systems or the Hadwiger–Nelson problem globally.

Put `w=(1+i*sqrt(3))/2` and

```
A5(z) = {a0 + a1*z + a2*z^2 + a3*z^3 + a4*z^4 : aj in {0,1,w}}.
```

The cohort consists of all simultaneous solutions of

```
|z + a*w^2*z^2 + b*w*z^3 + c*z^4| = 1,
|1 + d*z^2 + e*z^3 + f*z^4| = 1,
a,b,c,d,e,f independently in {-1,+1}.
```

The 64 equation pairs were frozen before solving their roots. Each pair has
trivial stabilizer under the radix D3 action. Their canonical representatives
belong to the committed h4195 residual, and arise from two sections of its
pencil at zero-based index 2377. `COHORT.json` records provenance; the explicit equations above,
not pencil bookkeeping, define the theorem. Only this cohort is tested.

| Parameters | Distinct physical points | All unit edges | Chromatic number |
|---:|---:|---:|---:|
| 338 | 243 | 261 | 3 |
| 1 (`z=w^2`) | 21 | 45 | 3 |
| 1 (`z=conjugate(w)`) | 27 | 63 | 3 |

There are 66 rational-univariate charts: 46 of degree 32, 18 of degree 31,
and two rational charts. Charts with several real embeddings describe one
physical graph per embedding. Counts above are by distinct parameter, not
by nonisomorphic graph. Every graph contains the triangle `{0,1,w}`.

The certificate contains exact irreducible polynomials, rational isolating
intervals for every real embedding, complete pair-to-chart incidence, collision
and coordinate hashes, complete-edge hashes, and literal proper three-colour
words. The accompanying checker reconstructs exact coordinates and tests every
physical pair directly. No tolerance, omitted-unit-edge convention, list
colouring, or SAT UNSAT assertion enters the conclusion.

See [PROOF.md](PROOF.md) for the coverage and geometric argument,
[REPRODUCE.md](REPRODUCE.md) for commands, and [PROVENANCE.md](PROVENANCE.md)
for the committed frontier and reused source. `EXPECTED.json` is the checked
summary. This is author-side computer-assisted evidence, not independent
peer review or a proof-assistant formalization.

The campaign's one-cohort stop applies: bank this physical result and leave
A5 rather than enlarge this census. No record improvement is claimed.
