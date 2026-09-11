# Unequal-core AHT templates: exact criterion and rigidity

The [general theorem](proof.md) characterizes non-two-colorability for AHT templates with arbitrary, possibly different core families and arbitrary transversal families, at every uniformity and on any finite core ground set.

When the core has size `2r-3`, it gives a counting lower bound, an equality characterization by intersecting Steiner systems, and a quantitative bound on how much the cores can differ near equality. For odd `r`, equality also forces the transversal family to be a parity class.

For `r=5`, every non-two-colorable subhypergraph of the entire 207-edge template on 17 vertices has at least **51 edges**, and every equality example is the classical Fano/parity construction up to isomorphism. The global Property B bounds remain **35 ≤ m(5) ≤ 51**.

Reproduce the compact evidence with Python 3.11+ and only its standard library:

```sh
python3 verify.py
```

Run without `-O`. The verifier checks the exact criterion against all 131,072 small subtemplates, regenerates all 60 labeled equality templates at uniformity five, and checks the classical 51-edge control against every coloring modulo color reversal. It also checks counting and stability identities and explicit proper-coloring witnesses. `expected.json` records the output; `reproducibility.json` records the run and hashes.

The arbitrary-parameter result has a written proof. Computations are controls and finite equality enumeration, not its sole justification. No solver, external catalogue, or omitted large certificate is required. The 51-edge witness is classical; no improved construction or unrestricted endpoint is claimed. The proof has not been independently reviewed or formally verified.
