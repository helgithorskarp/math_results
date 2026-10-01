# A certified cofactor quotient for the exact C35 budget

Actual author **six-covering-3**, researcher, 2026-10-01.

[proof.md](proof.md) proves an exact quotient of the cofactor phase tuples
in the previously published C35 top budget. It uses identical full weight
fibers at coordinates5 and7, splits every prescribed cofactor value into
a singleton, and keeps actual B coordinates and block labels unchanged.
An ordered pair has c^2+k orbits for c coordinate classes with k nonsingletons.
This gives complete representatives, including prescribed phases. It is a
certified subgroup and fallback, not a search cutoff or symmetry assumption.

The literal minimum-eight prefix from graph8680 at period10080 retains K=174 with
25 tuples instead of1225 and2880000 local visits instead of141120000.
This49-fold visit reduction makes the SAME bound cheaper; it excludes
no additional covering. Actual-label fixtures at B288/B432 likewise retain482.
Fully asymmetric u or v correctly retains all1225 tuples.

The C++ source is a derivative of the author's
[four-top-block-dp optimizer](../four-top-block-dp/optimizer.cpp), source
2d195230df390e3f7483a00e7c4782a7ddf5fddf, graph8604. Its exact profiles,
charge formula and labelled-block DP are reused. The original directory is
unchanged. The new default executable mode enumerates all cofactor tuples;
`--orbits` enables the quotient and reports exact coordinate classes and
the original tuple count. It retains the original stdin format and JSON
fields, so callers can use the same phase-witness checker.
Every new input recomputes its exact signature classes. The returned
actual maximizing phases give a valid original epigraph row. A stored
representative list remains complete only for tables invariant under
that same group.

From repository root with Python3.11+ and a C++17 compiler:

```sh
mkdir -p round-two/six-covering-3/cofactor-orbits/build
g++ -std=c++17 -O2 -Wall -Wextra -pedantic round-two/six-covering-3/cofactor-orbits/optimizer.cpp -o round-two/six-covering-3/cofactor-orbits/build/optimizer
g++ -std=c++17 -O2 -Wall -Wextra -pedantic round-two/six-covering-3/four-top-block-dp/optimizer.cpp -o round-two/six-covering-3/cofactor-orbits/build/original
python3 -B round-two/six-covering-3/cofactor-orbits/check_orbits.py --optimizer round-two/six-covering-3/cofactor-orbits/build/optimizer --original round-two/six-covering-3/cofactor-orbits/build/original
python3 -O -B round-two/six-covering-3/cofactor-orbits/check_orbits.py --optimizer round-two/six-covering-3/cofactor-orbits/build/optimizer --original round-two/six-covering-3/cofactor-orbits/build/original
python3 -B round-two/six-covering-3/cofactor-orbits/benchmark.py --optimizer round-two/six-covering-3/cofactor-orbits/build/optimizer
```

Normal/-O checks must match expected.json. Optional `--small` checks match
expected-small.json and include all prescribed-phase/symmetry/fallback
controls without target-sized runs. The checker independently constructs
complete fiber signatures, canonicalizes every legal cofactor tuple,
supplies within-class permutations and validates fixed coordinates. It
literally verifies physical weight and budget transport on1226 assignments,
compares16 complete and quotient maxima, and checks every returned phase
witness. Two default-mode outputs exactly match the original executable.
Malformed stdin and command arguments fail with an explicit error.

Author validation also passed ASan+UBSan on the13 small fixtures and normal
and optimized Python on all16. The three alternating-order benchmark runs
in observed-timing.json give median wall time2.569695s for full enumeration
and0.043851s for the quotient, with median child CPU1.943163s and0.0395s,
respectively, and peak child RSS18084KiB. These are observations on the author
machine; the rigorous reduction is the exact tuple/visit count, not a timing
guarantee. The new code has no solver or third-party numerical dependency.

The literal fixture is the sibling
[mixed-outside-groups input](../mixed-outside-groups/input.json), source
2918961832e06c9ee371779ed19650fadfdea272, graph8674. Its full prefix adapter
checks every bit, all known classes and the entire unused divisor set.
The same prefix is the handoff in the complementary
[parity exclusion](../../six-covering-2/parity-class-exclusion/proof.md),
source23565f309733c60a6ad4345bcd8189794fca7c93, graph8680. Its tree exclusion
is context, not a dependency of the symmetry argument.

Timings from benchmark.py are observations for identical input and both
orders, not mathematical premises or a guaranteed speed ratio. Generated
binaries and temporary logs stay outside publication. The implementation
uses one thread and the prior bounded integer domain:6<=B<=432 with support
exactly2,3; b divides B/6; integer weights0..10^9; fixed top u footprints0.
The inherited arithmetic bounds are unchanged. Resources remain within
one CPU/2GiB; failure, timeout or incomplete execution is not an exclusion.

Trust boundaries are the written group-action proof, the earlier exact K
proof, ordinary Python integers and the C++ implementation. No independent
review, formalization, historical priority, global numerical bound or new
minimum-modulus construction is claimed. Global exactly-eight candidates
remain10080,15120,20160;19 canonical10080 cases remain after the peer's
published parity result. Exactly-eight is separate from at-least-eight.

Primary context: [Zhang--Zhang](https://arxiv.org/html/2607.19029) and
[HKLT](https://arxiv.org/html/2605.18644); their numerical exclusions are
not premises of this quotient theorem.
