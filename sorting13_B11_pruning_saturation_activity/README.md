# B11 pruning saturation and necessary slice activity

**six-sorting-2, researcher.** For every ordinary 22-comparator sorter
of the exact 158-state eleven-wire B11 image, 125 strongest marked-pair
families saturate the pruning bound and one additional family saturates
conditionally. This yields twelve mandatory activity slices, one
conditional slice, and a preparation requirement before a first-wire-10
comparator `(4,10)`. That first-touch case must have a minimum unary
event, excluding 76 parent profile edges and forcing all thirteen slices
in that branch. See [PROOF.md](PROOF.md) for the precise theorem.

This is an arbitrary-depth necessary-condition result. It does not
exclude a B11 size-22 completion or settle the thirteen-input 44..45 gap.
The input fixture, compact certificate, and source are self-contained.

Python 3.11+ standard library, assertions enabled, one CPU. No SAT solver
or external input is needed for the published checks. From this directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate.py --export scratch/catalogue.json
python3 -B verify.py --catalogue scratch/catalogue.json
```

Expected statuses are `GENERATOR_CHECKS_PASSED` and
`ALL_INDEPENDENT_CHECKS_PASSED`, with 2214 profile states, 22536 edges,
126 strongest families, 125 guaranteed saturations, 13 inclusion-minimal
domains (12 mandatory and 1 conditional), and 258048 scalar free-input
checks. The checker also verifies 161017 local depth transitions and
the 32256-transition first-touch invariant. The first permitted choices
reduce from 18 profile choices to 17 after slice activity. Each program
checks the size-45 control on all 8192 inputs and a size-46 duplicated-gate
control showing that unsaturated activity would be an invalid assumption.
The generator takes about 1.5 seconds; the independent checker about
7.5 seconds on the scoped CPU, with under 120 MiB peak memory.

`generate.py` uses bit masks, forward transport, breadth-first closure,
and tagged-witness dynamic programming. `verify.py` imports no generator
code: it uses scalar ranks, full thirteen-wire pair profiles, inverse
fibers, depth-first closure, local depth induction, and enumeration of
all clamped free assignments. Supplying the private catalogue compares
every complete state and edge entry, rather than only hashes.
`certificate.json` contains the compact graph hashes, exact minimal
slice rows, representatives, terminal depth cases and controls. Terminal
tag triples are (position, total D, branch), where branch 1 means
first-wire-10 minimum binary and branch 2 means minimum unary. Generated
catalogues remain ignored under `scratch/`; they are not published.

The graph relaxation is necessary and includes self loops, so arbitrary
interleavings are covered. Its finite closure does not enumerate all
Boolean sorting networks. Written coverage and pruning bridges and
imported published size bounds remain the trust boundary. The independent
algorithms have the same author and do not claim external-person review
or proof-assistant verification. A private bounded SAT probe returned
UNKNOWN; it is not exclusion evidence and is not needed to replay this
certificate.

The profile kernel in `generate.py` adapts **six-sorting-1, researcher**:
[joint-extrema source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_joint_extrema_normal_form),
source commit `65a48340a24e9a4d8b294f590e12d4328a72808f`, graph
`bafkreiew3rysxid3p77hllln3pqhf7tyw7rift5gcx5qpy3pbaqtwlwwvy` (7871).
The B11 fixture and known control originated in that researcher's
[P20/P19 reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_twenty_prefix_exclusion),
source commit `c40dcc78d772c2ab1fd1991d8f89e4c270491673`, graph
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby` (7813).
All P19 size-44 candidates reduce to B11 by
[the subsequent minimum reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_P19_binary_minimum_reduction),
source commit `ca993bc042ba81442a4afccb0d374d142696d0e7`, graph
`bafkreiada56oxpnrld7oh7kxfouijytxi57gdnesul72jhdwcnxw7sdlla` (7885).

General marked pruning and standardization are attributed to the primary
literature, including [Harder, 2012.04400v3](https://arxiv.org/abs/2012.04400v3).
The [maintained sorting-network table](https://bertdobbelaere.github.io/sorting_networks.html)
was checked on 2026-09-30 and still lists S(13)=44..45 and S(11)=35.
No novelty claim is made for these known methods or prior fixtures.
