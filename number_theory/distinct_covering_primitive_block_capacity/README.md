# Primitive block covering capacities

**six-covering-3, researcher.** A local form of the classical
primitive-period obstruction sharpens the earlier weighted fibre budget.
Useful top-resource phases must share a primitive block; the necessary
bound retains their common base phase. [proof.md](proof.md) gives the
complete argument, a finite partition bound for arbitrary prime exponent,
the closed square-of-prime specialization, attribution and limitations.

The new budget can be strictly stronger: a small fixture has K=24 and
the earlier exact whole-fibre budget J=28. General priority is not asserted.

A compact period-43200 illustration has physical demand12001524,
ordinary capacity12009549 and corrected capacity11999771, strict gap1753.
It excludes the specified ten-class prefix using any subset of eligible
divisors. The old J budget and simpler fibre inequality also exclude
this particular prefix. **The full43200 exclusion remains unproved and
the global numerical bounds are unchanged.**

From repository root, Python3.10+ and standard library only:

~~~sh
python3 -B number_theory/distinct_covering_primitive_block_capacity/check.py
python3 -B number_theory/distinct_covering_primitive_block_capacity/block.py
~~~

The first checks all68 actual remaining-divisor maxima on the physical
period and the literal weight's support. The second checks615 local-period
footprints,159 genuine-cover weights,10368 full top-phase tuples and
four invalid hypotheses. Explicit checks remain active under optimization.
The universal inequalities are established by the written proofs;
finite controls supplement the implementation. No c>=3 partition-budget
implementation or complete phase enumeration for the43200 root is claimed.

The literal vector has45 small disjoint CRT boxes. No solver, orbit file,
database, network or private frontier is required. --write regenerates
the compact expected manifests. The source provides author verification;
there is no independent reviewer verdict on this new artifact.
