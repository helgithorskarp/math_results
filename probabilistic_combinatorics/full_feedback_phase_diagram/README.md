# Three transitions for full-feedback one-round resolution

For `G ~ G(n,p)`, let U mean that G is connected and **every vertex** can
identify every target with one full directional probe. This note proves
the uniform additive asymptotic formula

```
P(U) = exp[-n^3 p^2 exp(-np^2)/2
           -n^3 (1-p)^2 exp(-2n(1-p))/2] + o(1)
```

for `p >= log(n)/(2n)`; below that range the probability tends to zero.
This gives the complete phase diagram, including three critical windows:

| Scaling, q=1-p | Limiting probability |
|---|---|
| `np^2 = 2 log n + log log n + c` | `exp(-exp(-c))` |
| `nq = (log n)/2 + log log n + c` | `exp(-exp(-2c)/8)` |
| `n^(3/2)q -> a` | `exp(-a^2/2)` |

Increasing density first creates universal resolution, then destroys it,
then restores it near the complete graph. At the sparse boundary the
defects are nonedges with one common neighbor. At both dense boundaries
they are centers with two degree-one neighbors in the complement.
The number of failed probes converges respectively to twice a Poisson
variable, a Poisson variable, and a Poisson variable, with the corresponding
means appearing in the table.

The property concerns **all possible first probes**. Its failure does not
prove that an adaptive strategy needs more than one probe per round, and
the open question of a full-feedback localization number greater than
two remains untouched.

- [Complete written proof](PROOF.md), including all density regimes,
  dependence estimates, and exact moment identities.
- [Literature and attribution](LITERATURE.md).
- [Independent finite audit](verify.py) and [expected output](EXPECTED.json).

## Reproduce

Python 3.10+ and its standard library are sufficient. Tested with CPython
3.11.2. From this directory:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

The output must have `"status": "VERIFIED"` and record SHA-256
`f0f1158c7eca4dad8f98bc29253925664349c2687e37d71b9b793167abac763f`.

The audit exhausts all 33,866 labelled graphs on two through six vertices.
Breadth-first shortest-path responses are compared with the defect
reduction at every connected graph, including 164,030 probe checks.
Eighty rational first-moment checks and forty rational second-moment or
joint-event checks compare the formulas with weighted full enumeration.
The audit also checks all sixteen cross-edge patterns, 150 explicit
leaf-constraint counts, seven boundary fixtures, and seven rejection tests.
Fixtures include a diameter-three cube with universal resolution and a
complement triangle whose collisions are not leaf cherries.

The initial full audit took 2.66 seconds and 16,792 KiB peak resident
memory. No randomness, floating point, solver, external dataset, or large
certificate is used. Finite checks corroborate the written proof; the
uniform limits rest on its symbolic arguments. Independent mathematical
review is pending, and novelty is qualified relative to searched sources.
