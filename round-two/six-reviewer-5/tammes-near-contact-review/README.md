# Independent near-contact review

Actual author: **six-reviewer-5**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the scoped Tammes thirteen-edge near-contact theorem h8524 and proves a 50% larger tolerance, **3/40000000**, throughout **[14/25,593/1000]**. All 877 changed Bernstein omissions and 30 affine transfers are independently reconstructed using exact evaluation/interpolation and de Casteljau restriction. Original cap/graph proofs and affine cancellations remain explicit pinned dependencies, replayed by their original checkers. No global Tammes bound or motif-occurrence theorem follows.

Use CPython >=3.11, standard library only, from the repository root:

```bash
python3 -B round-two/six-reviewer-5/tammes-near-contact-review/reproduce.py \
  --repository-root . --output-dir /tmp/tammes-near-contact-review-run
```

The output directory must be new. A sparse checkout must contain this directory and these three dependency directories:

- `round-two/six-tammes-2/robust-eight-core`
- `tammes15_octagon_model2_extension_exclusion`
- `tammes15_octagon_model2_lower_strip_exclusion`

[INPUTS.json](INPUTS.json) pins every input file used. The target source was published at commit `31b21dd53d0624dae19dc6215f0f4b2de7c636b5`; its old dependencies were inspected at snapshot `6dffbb940c10f415b71e275a45010a7141d1ee4e`. If current source differs, retrieve the pinned original version in a separate checkout; do not silently bypass the hash check.

The runner checks input hashes, replays two original proofs, runs the independent audit on both strips in ordinary and optimized Python, and runs exact geometry plus six corruption controls in both modes. Children run sequentially with one numerical thread and a 55-second timeout apiece. Any timeout or verification failure stops the runner without a mathematical verdict. Generated logs and original witness exports stay in the chosen output directory.

Expected final status: `SCOPED_REVIEW_AND_LARGER_TOLERANCE_VERIFIED`. Exact stable receipts are in [EXPECTED.json](EXPECTED.json), and a measured completed run is in [VALIDATION.json](VALIDATION.json). [audit.py](audit.py) imports no author or prerequisite algebra; [replay_parent.py](replay_parent.py) explicitly trusts and imports the original checkers in isolated processes. [controls.py](controls.py) proves polynomial geometry identities using full recovery grids and rejects actual altered certificates and unsupported relaxation values.

The recorded CPython 3.11.2 run took 70.89 seconds total and peaked at 22,076 KiB child RSS; the largest stage took 23.19 seconds. All eight stages completed under the stated limits.

The ordinary Python interpreter, exact Fraction arithmetic, unformalized geometric proof and original published cap/graph proof layer are the trust boundaries. Input and record hashes provide integrity, not a substitute for mathematical proof. No raw proof corpus, private ledger, credentials or solver installation is needed.
