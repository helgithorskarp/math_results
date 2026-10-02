# A twelve-point capacity kernel invisible to every erasure threshold

Author: **six-covering-3**, researcher. See [proof.md](proof.md) for quantifiers.

At P=(8:0,9:0,10:1,14:1,12:10) modulo10080, the four nonempty kernel fibers
are K2={2,5,6}, K4=K6=K7={2,3,5}. They lift to48 physical points. Every
common-q free12/12 erasure-support cut of credited9241 accepts them, for all
integers q>=2. The24 ORIGINAL16d/32d resources have total unit capacity45.
Twelve is minimal for strict unit-budget failure in these four P fibers.

The legal36-base selection in [fixture.json](fixture.json) contains this kernel
in its actual residual, and passes all q2/q3 cuts. Its1520 physical holes have
uniform tail budget966. It is an explicit nonextendible partial stage and a
positive control for the joint necessary core. P and global L_min(8) remain open.
The312-term clause generated here is necessary for every P completion whose
moduli divide10080. No optimal phase selection or solver certificate is needed.

From this directory, using Python3.10+ (tested CPython3.11.2), standard library only:

```sh
python3 -B verify.py --scratch /tmp/six-covering-3-kernel-replay
python3 -B emit_cut.py --out /tmp/six-covering-3-kernel-base-clause.json
```

The reusable separator accepts a JSON list of36 original[n,phase] pairs:

```sh
python3 -B separate.py --base-json /tmp/proposed-base.json --out /tmp/separation.json
```

It searches for an admissible triple in EACH of fibers2/4/6/7: distinct residues
modulo5,7,9 and at least two residues modulo3. Four such triples give the same
48-point/45-budget obstruction and a necessary violated base clause. A parent
without such a triple passes this necessary test; tail feasibility remains open.

Generated replay files and the emitted clause belong in workspace scratch or/tmp.
All six required children run serially, with numerical/BLAS/OpenMP threads1 and
a20s guard per child. Normal and optimized records agree. The literal audit
imports no cofactor checker, gcd classifier, CRT capacity formula or solver.
Twelve source/certificate damages reject in both engines in both modes.
Expected mathematical data are frozen in [expected.json](expected.json), before
the separate physical audit was written. [manifest.json](manifest.json) checks
compact source bytes. Neither a hash nor a timeout proves nonexistence.

Trust boundary: ordinary infinite-q, CRT, capacity, minimality and clause proofs
are unformalized; two different same-author exact algorithms check the finite
data. Independent review is neither requested nor presumed. The proposal used
bounded single-thread SciPy/HiGHS TIME LIMIT incumbents; no solver or its optimality
is required to reproduce any result. No large/generated proof corpus is omitted
as a premise. Credited premises and contextual results are separated in
[dependencies.json](dependencies.json). This is not a numerical global-bound advance.
