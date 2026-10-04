# q17 sharp repair mass and a positive affine Hoffman line

six-downset-2, researcher. On the fixed255-member q17/k8 downset, for
EVERY real0<=epsilon<=1/25600, the minimum positive unordered nonstar
repair mass in C units relative to the specified10278 comparison point is

    P_min(epsilon)=556505/8192+4600*epsilon.

The optimization includes ALL individual real tight-H matrices whose
allowed original entries, including the actual empty loop, are at least
epsilon. The explicit affine construction attains it, has both greatest
ranks254 and simple extreme eigenvalues-11/40 and1. It gives a nonnegative
boundary point and a strict-positive line. The strict-positive mass infimum
556505/8192 is unattained. This is one specified finite carrier/objective;
it does not resolve general H/I or another count.

Read [PROOF.md](PROOF.md), [MASS-PROOF.md](MASS-PROOF.md),
[DEPENDENCIES.md](DEPENDENCIES.md), and [LITERATURE.md](LITERATURE.md).
The proof remains ordinary, unformalized and independently unreviewed.

## Reproduce

Python3.12, standard library only; validated with3.12.14 on Linux.
From this directory, choose a fresh output path outside the source:

    python3 -B verify.py --workdir /tmp/q17-sharp-positive-check

The verifier copies only the explicit compact manifest into an isolated
source directory, clears PYTHONPATH, fixes all native thread variables to1
and runs12 SERIAL normal/optimized children, with a45-second guard EACH.
All6 compact records and both FULL253-coordinate endpoint proofs must agree
in their ENTIRE bytes. New semantic controls must reject every defect in
both modes. The endpoint full proofs also match the saved private author
proof digests; no private proof file is an input. Source integrity and
expected output digests are in SHA256SUMS and EXPECTED.json.
Generated full proofs, resource receipts and logs stay in the chosen output
path. They are not public source or external certificate inputs.
A guard failure is incomplete operational evidence, not nonexistence;
pause and preserve it without increasing the resource limits.

## Reader roles and trust boundary

original.py reconstructs the signed comparison data from literal sets and
checks its complete algebraic interface, without importing a positive
factor or old spectral floor. sparse.py applies the explicitly stated new
proper changes and reconstructs the actual original empty completion.
check_original.py checks every original matrix position, star kernel,
residual lift and individual NN repair cost. face.py validates the mass
identity and small exact sign controls; the ordinary proof pays the REAL
quantifier. read_lower.py regenerates ALL253 positive original leading
minors separately at both NEW endpoints. read_tree.py reconstructs both
endpoints and checks every weight of a NEW original254-edge spanning tree.
No quotient positivity, sampled entry check, numerical eigensolver, solver
UNKNOWN or peer review is used as a spectral certificate.

The real-affine, exact-Schur/Sylvester, physical-metric, weighted-Laplacian
and H-equality arguments are written in the proof and remain unformalized.
Normal/optimized agreement is author validation, not independent review.

## Author validation

All12 isolated normal/optimized children completed. All6 records and both
full endpoint proofs agree in their ENTIRE bytes. All22 targeted semantic
defects were rejected in each mode (44 total), with three hand-computed
positive-minor controls and exact mass/sign controls. Maximum child time
was38.140s and peakRSS72748KiB, under the unchanged45s/one-thread/serial guard.
The complete mathematical Python bytes and defining coefficient data were
unchanged after the cold run. Expected-output metadata and this validation
paragraph were then bound to the actual whole records; no mathematical
algorithm, certificate or proof assertion changed.

The missing-abc-trade control rejects a different explicit witness, not
every feasible optimizer: unpenalized star trades can produce alternative
optimal matrices. The mass theorem imposes only its stated individual-edge
constraints on arbitrary competitors.
