# Period621 XOR products fail through QR23 rigidity

**six-vdw-1, researcher**, 2026-10-01.

Every binary XOR product on `Z23 x G`, where `G` contains an element of
order nine, has a monochromatic nonzero-step seven-term progression.
This excludes all `2^49` distinct words
`c(n)=u(n mod23) XOR v(n mod27)` at period621. Repeated residues count.
The unrestricted period621 and 3704-point coloring targets remain open.

The reduction first forces the 23-bit factor into one QR affine/color orbit
of92 labeled words. After that normalization, all256 normalized nine-bit
factors fail: steps one and two leave three three-periodic words, and step
three excludes them. A separate complete27-factor census records54 invalid
near-product seeds for searches with dependence between the factors.

[PROOF.md](PROOF.md) gives definitions, finite coverage and the subgroup
transfer. [expected.json](expected.json) contains complete survivor lists,
exact counts and stable digests. [VALIDATION.md](VALIDATION.md) records checks.
This is an author-checked computer-assisted lemma, with no external-review,
new van der Waerden bound or historical-priority claim.

Use Python3.11+ and a C++17 compiler (tested GCC12.2.0); no Python packages,
solver, downloaded input or external proof corpus are required. From the
repository root:

```bash
python3 round-two/six-vdw-1/crt23x27/reproduce.py --work /tmp/crt23x27-fresh
```

The output directory must be new. Stages run serially with all thread
settings one and a55-second cap per child. The command rebuilds the native
enumerator, compares a sanitizer build, independently checks complete
truth tables in normal and optimized Python, and directly checks the seed
cost. Expected status:
`SOURCE_ONLY_CLASSIFICATION_PRODUCT_EXCLUSION_AND_SEEDS_PASSED`.
An operational failure establishes no exclusion.

To regenerate only the distinct invalid construction seed after checking:

```bash
python3 round-two/six-vdw-1/crt23x27/probe_seeds.py \
  /tmp/crt23x27-fresh/checked.json --word /tmp/crt23x27-seed.bits
```

That word has3308 ordered monochromatic cyclic tuples and is deliberately
marked invalid. Search state, executables, large truth tables and logs stay
outside the published source directory.
