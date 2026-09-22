# A planar LP obstruction for line-free sets in F_5^3

An exact certificate shows that a specific strong planar relaxation admits
total mass **exactly71**, even after fixing a maximum16-point section and
a parallel small section. The certificate rules out this relaxation as a
proof of the bound70. It is a limitation of a method; no new bound on the
actual line-free extremum is proved.

For each of all155 affine planes, the71-mass point vector is the marginal
of a probability distribution on line-free subsets of that plane of sizes
7–16. All these distributions respect the same fixed16-point grid in z=0
and missing point(0,0,1). On z=1, the subsets have size7–10 and no four
collinear points. The distributions agree on individual point marginals;
joint distributions on shared lines are not imposed.

Thus adding **any linear inequalities valid for those planar families**
cannot exclude this fractional point. Constraints linking higher-order
marginals, further geometric restrictions, or integrality may still help.
The certificate does not represent a71-point set.

The [proof](PROOF.md) defines the relaxation precisely, proves the
maximum/parallel-small normalization for actual71-point candidates, and
explains how bounded random deletion converts the compact certificate to
exact local distributions. The distinguished maximum section in this
certificate is a grid; we do not assert that every candidate has a grid
section.

## Replay

Requires Python3.10+; no dependencies, solver, network, or large catalogue.

```sh
python3 verify.py
python3 -O verify.py
```

Both outputs match [EXPECTED.json](EXPECTED.json). The integer certificate
has125 point weights and1996 mixture terms covering all155 planes.
Six malformed controls are rejected. The verifier also checks the exact
bounded-deletion condition that preserves at least seven points in every
local subset.

An optional independent replay of the standard planar cap16 is:

```sh
g++ -O2 -std=c++20 -Wall -Wextra -Wconversion -Werror planar_cap.cpp -o /tmp/line_free_planar_cap
/tmp/line_free_planar_cap
```

It checks all1081575 seventeen-subsets and finds none line-free. The main
fractional certificate verifier does not need this program or assume an
optimizer verdict. Ordinary mathematics, exact integer code and the compact
input certificate are the trust boundary; independent review and formal
verification are not claimed.

Background and attribution are in [SOURCES.md](SOURCES.md). The campaign's
separate70–72 interval remains unchanged. The public paper gives70–73;
the campaign's72 bound is a separate earlier contribution.
