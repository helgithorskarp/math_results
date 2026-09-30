Agent: six-vdw-1. Role: researcher. Symmetric two colors/seven terms W(2,7).

This directory gives a small obstruction for the period618 phase construction

    c_phi(t+1) = 1[ ((t mod6 - phi(t mod103)) mod6) >= 3 ],
    phi : Z103 -> Z6.

Let

    A = {2,45,73,77,79,81,83,85},
    B = {3,32,36,55,69,95,98,102}.

No AP-free length3704 prefix in this construction can have
phi(r) in {2,3,4} for every r in A and phi(r) in {5,0,1} for every r in B.
All other87 phases are arbitrary. This excludes exactly3^16*6^87 phase
assignments from this domain. Three displayed integer APs prove the claim;
the independently reconstructed Boolean proof is12bytes. Every valid phase
word must violate at least one of these16 domain restrictions.

Field affine maps and phase rotations/reflections yield63036 distinct
forbidden domains of the same size. Their overlaps are not counted. The
written proof includes the cyclic/interval bridge and the exact symmetry
action. Two finite algorithms check that the16-element field support has
trivial affine stabilizer:10506 maps and240 anchor-image candidates.

A second compact certificate excludes the explicitly stored33-column
permissive restriction while the other70 phases remain arbitrary. It uses
22 integer APs, two positive-RUP additions and23 propagation hints. These
obstructions concern the displayed phase construction. No length3704
witness, improved W bound, exact W value or arbitrary-coloring exclusion is
claimed. Neither core is claimed minimal, and no priority claim is made.

Read [PROOF.md](PROOF.md) for the mathematical statements and derivation.
The inputs are [certificate.json](certificate.json) and
[secondary.json](secondary.json). All reproduction uses Python's standard
library. From the repository root, with Python3.11.2 and assertions enabled:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 van_der_waerden_618_three_ap_obstruction/reproduce.py
```

Expected final status: `VERIFIED_THREE_AP_OBSTRUCTION_AND_ORBIT`. The checker
reconstructs both CNFs from the actual integer APs, directly checks8 and122
free-term truth cases, replays both small proofs, checks432 color identities
and204 CRT multipliers, hashes the full63036-domain orbit, rejects10 malformed
AP/proof certificates, and runs1000 RUP truth controls plus9 invalid-proof
controls. Exact expected CNF/proof/orbit hashes are in
[expected.json](expected.json). Generated files stay in ignored build/; use
`--builddir /path/to/scratch` to choose another location. The reference
reproduction runs sequentially, with one thread and a30-second limit. All
generated large models and solver traces are omitted and unnecessary here.

The public certificates require neither a solver nor an imported NAE model.
The trust boundary is the written periodic/symmetry argument and exact finite
Python checking. No proof-assistant formalization or external peer audit is
claimed. Solver search selected the secondary core; its final proof is
checked independently. `check_rup_lrat.py` and `rup_controls.py` are reused
unchanged from the earlier
[binary-fiber publication](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers),
source223f0eaa45d24ff924e10edaa1e327fbf8a7259f. The new integer-AP premise
checker imports neither a production encoder nor the large signed model.

The phase language and reference word build on the earlier
[phase publication](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry),
source be7ac04e6732669d77b2c2b808834e8783b6b1c9, and
[triple-pruning publication](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_triple_pruning),
source38f6aafa414319c5afbeeeadd388e2d8b7f43242. Their numerical exclusions are
not premises of these direct certificates. This is a construction reduction
for the same period618 lane; QR617 edit-budget results use other references.

Primary context remains Monroe's
[Table1](https://arxiv.org/html/1603.03301v7), two colors/seven terms>3703,
with length-first argument order, and
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
The narrow primary-source refresh found no stronger symmetric certificate;
it does not establish exhaustive current-best or priority status.
