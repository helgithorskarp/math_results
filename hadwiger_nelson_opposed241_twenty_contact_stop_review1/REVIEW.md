# Review verdict and limitations

## Explicit verdict

`ACCEPT_AND_STRENGTHEN_OPPOSED241_TWENTY_CONTACT_STOP`

The target's exact theorem is supported. One fixed shared-origin rotation of
two congruent copies of the reviewed 241-point opposed-B214 core gives 481
distinct plane points whose complete strict unit-distance graph has 2,002
edges and chromatic number exactly four.

The review strengthens the target in two ways. It supplies a fresh proper
four-colouring found without the submitted word, and it classifies the
cross-contact graph as the disjoint union of seven `P3` components and six
`K2` components.

## Checks passed

- Eleven public target, dependency, and prior-review files pinned by SHA-256.
- The 241-point source rebuilt from the original B214 fixture and retained
  label list, with the prior independent source-review hashes reproduced.
- A flat eight-element exact field implementation used instead of the
  target's nested `K+Kt` and normalized-y representation.
- Faithfulness of the flat basis justified over `K=Q(sqrt(33))` using the
  negative norms of both `T` and `T/3`.
- The displayed rotation checked to have unit norm and to realize its stated
  source-45/rotated-source-65 contact.
- Collision merging checked to identify only the common origin.
- All 115,440 final unordered pairs tested exactly; 1,982 inherited and 20
  cross edges recovered, with both canonical hashes reproduced.
- Submitted four-word checked on all 2,002 edges.
- A distinct proper four-word generated in 7,054 direct-search nodes.
- The 18-edge Golomb subgraph reconstructed and all 2,187 normalized
  three-colour assignments exhausted.
- Connectivity, articulation, bridge, degree, and four-core claims replayed.
- Cross contacts classified component by component; matching size 13 checked
  by augmenting paths.
- Normal, assertion-disabled, and adversarial-control runs agree.

## Limitations

- Only this one rotation branch, defining contact, shared origin, and pair of
  complete 241-point copies is decided.
- No neighbouring angle, alternative contact, reflected branch, second
  placement, fragment, or larger composition is classified.
- The linear-forest classification concerns only the twenty cross edges; it
  is not a theorem about the full conditional relation of the source core.
- The 481-point graph is four-chromatic. Its order being below 509 is not
  record progress because a record candidate must be non-four-colourable.
- The source core's conditional nonextension theorem is not needed for this
  verdict; only its exact point selection and the prior independent geometry
  alignment are used.
- The proof is computer-assisted. Residual trust is in the pinned bytes,
  exact `Fraction` semantics, the documented field-basis argument, SHA-256,
  CPython, the operating system, and correct hardware. It is not a
  proof-assistant formalization.

