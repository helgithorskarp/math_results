# Original twelve-core, three arbitrary additions: bounded polynomial reduction

Actual author **six-tammes-2**, role **researcher**.

[PROOF.md](PROOF.md) proves a lossless conditional feasibility reduction
on t in [14/25,593/1000]. It uses nine real variables, one positive radical
equation, six bounded stereographic coordinates, and no added-point unit
equations. [SYSTEM.json](SYSTEM.json) specifies the full original core,
every required pair and all bounds. The ring-only `constraints` function
in [model.py](model.py) generates94 defining integral polynomials.
`strict_improvement=True` adds precisely -F(t)>0, yielding95, exactly
equivalent to t<tau on the entire band. This preserves the critical strip.

The three added points are arbitrary. There is no actual fixed point13,
support/degree assumption, symmetry restriction or initial proximity
condition. This is a complete reduction using prior frame9774, rather
than an UNSAT certificate. Whole-domain arbitrary-three capacity, core
occurrence and global optimality remain open. Independent review and
formalization of this reduction are pending. The small local gate9866
is optional future context and is not a model constraint.

From a checkout of the repository, with Python3.11+ and only its standard
library, run these sequentially:

```sh
cd round-two/six-tammes-2/twelve-core-polynomial-model
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
python3 check.py --output /tmp/tammes-polynomial-model-normal.json
python3 -O check.py --output /tmp/tammes-polynomial-model-optimized.json
python3 controls.py
python3 -O controls.py
```

Each entrypoint has a50-second guard. One mathematical child at a time
was used in an unchanged1CPU2GiB scope. A timeout or incomplete check
establishes no infeasibility. Full normal/O results match the compact
[EXPECTED.json](EXPECTED.json) and [CONTROLS.json](CONTROLS.json).
[VALIDATION.json](VALIDATION.json) records actual complete execution
and measured cost; [RUNTIME_PINS.json](RUNTIME_PINS.json) binds all nine
runtime files. No external solver, executable, private input or floating
point decision is needed.

The checker verifies76 generic integral-polynomial identities, exact
whole-domain scalar bounds, and all four credited feasible completions.
All376 base-model polynomial predicates and all four exact equality
controls for strict improvement are executed. The controls reject27
scope damages and5 invalid polynomial inputs, detect two corrupted
coordinate identities, and accept3 harmless scope changes and3 finite
chart controls. Both Python modes perform all mathematical checks without
`assert`. These are same-author checks and do not supply independent review.

The local sparse polynomial class uses three slots for generic core
(t,z,w) identities, and fresh slots for universal chart(t,u,v) identities.
It does not identify the six distinct addition variables. The full
`constraints` generator accepts any compatible exact ring elements for
all nine distinct variables and uses integral ring operations only.

[DEPENDENCIES.json](DEPENDENCIES.json) gives exact source commits,
hashes, graph references and logical scopes. [LITERATURE.md](LITERATURE.md)
records current primary context. [INPUT.json](INPUT.json) and
[field.py](field.py) are unchanged credited incumbent fixtures/kernel;
archived heuristic metadata is not used as a certificate. No new
configuration or numerical separation improvement is claimed.
