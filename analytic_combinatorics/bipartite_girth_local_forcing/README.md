# Sharp local cut forcing for every bipartite girth

For every finite simple bipartite graph `H` containing a cycle, this
package determines the optimal cut-norm exponent, its leading constant,
and all asymptotically sharp profiles near a fixed constant graphon.

Let `m=e(H)`, let `g` be its girth, and let `c_g` be its number of shortest
cycles, each counted once. Fix `0<p<1`. Among all nonconstant symmetric
graphons `W` of density `p` with `||W-p||_infinity <= rp`,

\[
\lim_{r\downarrow0}\sup_W
\frac{\|W-p\|_\square}{[t(H,W)-p^m]^{1/g}}
=\frac{1}{4[c_g p^{m-g}]^{1/g}}.
\]

The [proof](PROOF.md) includes an explicit finite-radius bound and the
positivity of the deficit on sufficiently small such neighborhoods.
The exponent `1/g` cannot be increased. Disconnected graphs, pendant
trees, and bridges are included.

Sharp sequences have negligible degree variance relative to the
regular shortest-cycle moment, and their normalized regular operators
approach signed balanced rank-one operators in Schatten `g` norm. Both
conditions are necessary: a two-scale example shows that the profile
condition alone does not suffice.

This extends the graph's earlier complete-bipartite sharp-constant and
rigidity results to every bipartite girth. Qualitative local Sidorenko
and local forcing are known results. The proof uses Lovász's signed
density inequalities; the precise new scope and the limits of the
novelty search are in [LITERATURE.md](LITERATURE.md).

The neighborhood is in `L^infinity` and `p` is fixed. This package does
not prove global Sidorenko, new global forcing cases, a sharp statement
in cut-norm neighborhoods, or a kernel-`L^2` rigidity theorem.

## Reproduce the compact audit

From this directory:

```sh
python3 verify.py
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2; Python 3.11+ and the standard library suffice.
The verifier uses integers and `fractions.Fraction`, explicit error
checks, and no randomness. Assertions need not be enabled. To print
regenerated evidence without comparing it with the saved file:

```sh
python3 verify.py --emit
```

The recorded clean replay took 4.35 seconds and used about 17.2 MiB of
maximum resident memory on the development machine; these are observations,
not reproducibility requirements.

The expected status is `PASS`, with record SHA-256
`bdab48c6591134130a31cae97770ccf0be6e66a458caef68f4fa8b01a08c3126`.
The audit covers:

* All 49 nonempty edge subsets of a labelled `K_3,3` with minimum positive
  degree at least two, against four signed rational kernels: 196 checks.
* Independent operator-trace and literal vertex-assignment cycle counts,
  plus exact centered cut bounds, at girths 4, 6, 8, and 10: 12 checks.
* Thirteen named graphs, including unequal theta graphs, a cube, the
  subdivision of `K_4`, a cycle with a pendant edge, a disconnected
  example, and two six-cycles joined by a bridge.
* Seventy definition-level two-scale perturbation polynomials and
  seventy exact finite-radius remainder checks, including unequal atom
  masses and irregular kernels.
* Thirteen exact sharpness polynomials, compared with an independent
  Eulerian-edge-subset enumeration, and six rejected invalid inputs.

No large artifact, hidden catalogue, solver, network access, or external
runtime input is required. These are normalization and boundary audits;
the universal theorem rests on the written proof and its stated
external mathematical inputs. No independent peer review is claimed.
