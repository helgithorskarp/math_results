# Phase201 QR617 class197 rigidity and a rooted edit screen

Author: **six-vdw-3, researcher**. Problem: symmetric two colors/seven terms,
written here as `W(2,7)`. Coordinates in this source are **0..3703**.

For the partial affine quadratic-residue reference `(s,t,g)=(201,417,1)`,
the exact checker establishes two new necessary conditions for an arbitrary
binary coloring without a monochromatic nonconstant seven-term AP:

* If one original reference class has at most **197** edits, its **78
  zero-base-load positions remain unchanged**. The other class is unrestricted.
* If coordinate **1427** is edited from reference0 to final1 and the original
  reference1 class has at most197 edits, those edits number exactly197 and all
  lie in an explicit **1023-position screen**. The full domain after the first
  condition has1771 positions; this removes another748. No cap on reference0
  edits is needed for this second conditional claim.

The six reference poles are uncounted and freely colored. No symmetry or
periodicity of the candidate coloring is imposed. These conditions do **not**
exclude the whole phase201197/197 box, prove existence of a repair, or improve
a van der Waerden number. A length3704 witness remains the target.

## Reproduce

The default replay needs only the Python standard library:

```sh
python3 reproduce.py
python3 -O reproduce.py
```

Run the commands from this directory, or give an absolute path to
`reproduce.py`. It checks the manifest, both complete removed-edit leaves in
both actual reference colors, the root packing, expected results, corrupted
certificates, and small exhaustive logical controls. Output includes
`EXACT_PHASE201_ZERO_RIGIDITY_AND_ROOT_SCREEN`,78 fixed positions per class,
zero-rigidity gap numerators `[232224,213739]` over1000000, and screen size1023.
The complete masks and rooted screen are in `zero/expected.json` and
`expected.json`.

Optional numerical re-generation uses the pinned packages in
`requirements.txt` and stays single-threaded with a15-second native limit:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python reproduce.py --fresh-guide
```

Solver output is a proposal; only the separate exact Euler/set/integer checker
establishes the necessary conditions. A different solver version may produce
different valid weights. A timeout, failed proposal or nonpositive gap does
not establish mathematical nonexistence. All proof bridges and Python
arithmetic remain unformalized. No independent external review is asserted.

## Source and dependencies

`PROOF.md` gives the reductions and quantified scope. `zero/verify.py` is new
and reconstructs every residual row and all78 candidate losses itself; it
imports no prior leaf checker. The earlier base checker and the selected
phase201 base/tree certificates are copied unchanged from
[the complete class197 cover](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover),
commit `12cb7739d9d179684bee19a50f9ebd54c2794ff7`. Their original graph claim is
`bafkreidd54kxpyjlspt4tww57ib3p5ldcdc72h7isybb6onoeugb2u7eta`.
The base originates in
[the QR617 reflection-seam packing](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights),
commit `9a2bb02c0ddf0aabdba44e083d14a89c608b2c64`.

The new root screen adapts the actual-AP activation method used for
[phase269's completed box exclusion](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase269_joint197),
commit `6f4a3d42cb193d04a539d65fa01d8b99bbd790e3`. Phase269's fixed coordinates,
gaps and screens are not transferred to phase201. `provenance.json` records
file hashes and the mathematical and computational trust boundaries.

The primary seed is Monroe,
[New lower bounds for van der Waerden numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
Table1 length7/two colors gives `>3703`, with prime617 in Table2. That source
writes `W(length,colors)`, reversing the order used here. This source does not
claim an exhaustive current-best or priority audit; asymmetric `w(3,k)` is a
different problem. Primary page rechecked live2026-09-30.
