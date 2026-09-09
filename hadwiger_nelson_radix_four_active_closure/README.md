# No four-active counterexample in the five-digit complex radix architecture

For `A5(z)=T+zT+z²T+z³T+z⁴T`, `T={0,1,(1+i√3)/2}`, this exact computation
closes the complete off-circle, injective branch with at most four active
distance curves. Together with the previous collision and unit-circle
closures, any non-four-colourable physical member must have **at least five
active curves**. No graph improving the 509-vertex record is established.

All 960,768 eligible four-curve combinations from HN3 h4135 are classified:
934,632 have explicit linear three-colourings, and 26,136 contain a K4 that
is impossible at unit distance in the plane. The export gives 3,006 reusable
forbidden incidence sets with exact four-label witnesses.

Read [PROOF.md](PROOF.md) for the complete reduction and trust boundary,
and [HANDOFF.md](HANDOFF.md) for the complementary HN3 parameter interface.
This is an author-checked computer-assisted result, not an independent
reviewer verdict or a closure of the whole architecture.

From the repository root, using standard-library CPython 3.11.2:

```sh
python3 -B hadwiger_nelson_radix_four_active_closure/verify.py
python3 -O -B hadwiger_nelson_radix_four_active_closure/verify.py
python3 -B hadwiger_nelson_radix_four_active_closure/controls.py
python3 -B hadwiger_nelson_radix_four_active_closure/produce.py --out /tmp/hn-four-active-certificate.json --export-interface /tmp/hn-four-active-incidences.json
python3 -B hadwiger_nelson_radix_four_active_closure/verify.py --certificate /tmp/hn-four-active-certificate.json
```

Output paths for generation must not already exist. The verifier imports
no producer or ancestor code and reconstructs every finite witness. The
producer uses the existing sibling `hadwiger_nelson_complex_radix_architecture`
geometry module. Neither needs a solver, CAS, network connection, raw input
dataset or floating-point arithmetic. Runtime is on the order of tens of
seconds per replay on the research host.

The checked expected result is [certificate.json](certificate.json), with
SHA-256 `1b9ed319a9765ed67fa2ed09a5a94d2e626b6d2028b9b4032a1bec23b8a55d55`.
The canonical transcript hash covers every quartet's selected F3 word
index or K4 label tuple. Full transcripts and raw incidence exports are
kept outside the repository and regenerated as needed.
