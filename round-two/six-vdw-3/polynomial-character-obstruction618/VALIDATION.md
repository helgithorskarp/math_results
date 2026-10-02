# Validation and trust

Actual author: **six-vdw-3, researcher**. Same-author independent
algorithms; no independent-person review of this new census or
proof-assistant formalization is claimed. Arithmetic is exact CPython
integer/set arithmetic, tested with CPython3.11.2, standard library only.
One serial child at a time; numerical thread variables are one. Fixed
20s child guards are unchanged. No solver or native finite verdict enters
the proof. Ordinary normalization/transport/masking arguments remain
unformalized.

`generate.py` evaluates characters by Euler's criterion and polynomials
by Horner's method. It intersects cyclic integer bit masks and tries
four deterministic greedy orders, stopping on eight positive witnesses
per polynomial. Failure to find eight is incomplete evidence, not a
counterexample or exclusion. Its search need not be exhaustive: only
the complete list of positively checked witnesses is used.

`check.py` imports no generator code. It builds the nonzero square set,
evaluates explicit polynomial powers and checks all317 canonical rows,
2536 actual APs/17752 terms, every root, all56 distinct used columns
per row, every color and positive integer lift. Root histogram is
106/157/4/50 for0/1/2/3 roots. Field zero is regular in312 cases.
Actual nonunit steps with gcd2,3,6 are included. The whole literal
geometry transcript is hashed, not published as a corpus.

Independent finite controls:

- all10404 nonzero character multiplicativity inputs;
- square class size51 and three disjoint cube classes of size34;
- all10712 depressed monic quadratic/cubic normalizations, including
 1092727 cubic point/root equalities;
- all10506 linear normalizations,126072 affine-basis values and63036
 CRT field-affine/phase parameter sets;
- all1920 phase-cycle inputs and5974 actual singleton-column witnesses
 on every103 field labels for58 illegal rows, with positive lifts<=2163;
- all3030 integer distances in30 root/hole/intersection classes, proving
 the stated distance/correlation formulas agree for0..3 holes;
- thirteen semantic certificate damages, including the missing third
 cube class, zero polynomial, root inclusion, overlap and nonmono AP.

The numerical normalization controls do not enumerate every original
polynomial or every orientation. The ordinary coefficient, CRT and
cardinality proofs supply those bridges. Four basis identities extend
to arbitrary coefficients by linearity. The group representatives,
nonzero-polynomial restriction, root-freedom convention, character
sign, modular repetition convention and unrestricted edit geometry are
all explicit.

All checks use explicit exceptions and survive Python-O. The reproduction
wrapper compares the entire CSV bytes and entire JSON records in both
modes, and verifies all source pins before helper execution. Runtime
records and hashes are in [verification.json](verification.json),
[expected.json](expected.json), and [SOURCE_PINS.json](SOURCE_PINS.json).
Hashes identify data; they do not replace finite checks or written proof.

Primary literature: Daniel Monroe,
[New lower bounds for Van der Waerden numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Table1 gives length7/two colors>3703; Table2 gives prime617. Its
length-first W(7,2) equals our color-first W(2,7). Herwig et al.'s
[primary manuscript](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides power-residue/zipping context. These primary sources and narrowly
targeted103/618 polynomial-character searches were refreshed2026-10-02;
they do not establish exhaustive later-record absence or priority.

Prior graph7950's F311 degree<=3 character repair is credited construction
context; its20-column number and single cube-class normalization are not
premises. Prior graph9637's phase/transport and graph9659's stronger linear
repair16 are credited separately. Reviewer4's graph9693 confirms/refines
the earlier linear theorem, not this polynomial census. No earlier
UNKNOWN, timeout, native proof, nonlinear transfer of16, or graph review
verdict is a premise of the new bound8.
