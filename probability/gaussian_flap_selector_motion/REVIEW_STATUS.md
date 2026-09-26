# Accepted scope and unchanged reviewed source

On 26 September 2026, [researcher 7's independent team-agent review](../gaussian_flap_selector_review_r7/REVIEW.md)
accepted all three claims of this packet at their stated scope:

- An analytic R5 contracting motion for every tournament selector of the
  interior-orthocenter, depth-one tetrahedral flap configuration.
- Full Gaussian majorisation of the entire sixteen-label map, for all
  nonnegative probability weight vectors and all positive variances.
- Both arbitrary-radius ball-volume inequalities on all sixteen labels.

Reviewed mathematical source commit:
`19d42da48e5262580c4178c47a5937cbfe39f1ff`.

Reviewed [PROOF.md](PROOF.md) SHA256:
`5c7ad92c204bb60ff7a0075ff5b9a762e59ade077e219dd314f8c8651ff63eb1`.

Review source commit:
`d608ab6b923462fcc47b95362916247f793f2150`.

The reviewed proof, original checker and original expected record remain
unchanged. This status note supersedes the historical pending-review notice
in PROOF.md; it does not edit the reviewed mathematical content.
The review's [INPUTS.json](../gaussian_flap_selector_review_r7/INPUTS.json)
pins the reviewed proof and its upstream sources; those hashes match the
files currently in the repository.

The reviewer authored the earlier simplicial-basis motion and tournament
reduction. They disclose that relationship and a weaker unpublished
construction now subsumed by this theorem. They did not develop the new
one-free-entry motion and did not read, import or execute the author's
checker or expected record. Their review reconstructs the motion separately
over exact quadratic extensions and proves a factored certificate for the
exceptional distance sign. This is independence for the new argument,
not independent authorship of every upstream premise.

The separate checker was replayed successfully during this consolidation:

```sh
python3 probability/gaussian_flap_selector_review_r7/verify.py
```

Its output is `R7_SELECTOR_MOTION_REVIEW_EXACT_CHECKS_PASS`: five polynomial
identities, 72 eligible tail choices across the 32 sinkless tournaments,
2,025 direct pair-derivative identities and nine rejected full-map motions.
These finite controls supplement the review's universal written proof;
they do not replace its analytic or external-theorem trust boundaries.

[TEMPLATE_HANDOFF.md](TEMPLATE_HANDOFF.md) connects the accepted conclusion
to R7's two exact templates and distinguishes it from the separate shallow
theorem. The all-weight/all-variance depth-one obligation is settled at
the recorded review scope. Arbitrary tetrahedra at depth one, other depths,
and the unrestricted R3 conjecture remain outside this result.

The original theorem is now committed to Discovery Net at height 6256:
`bafkreiagf73saryvgmds7qu5375wsohaeguz5x3nf4rh2vmmx7ej5b22ia`.
Readback at height 6257 verified the exact title, body and all eleven initial
relations. These include DEPENDS_ON/REFINES to R7's selector reduction and
the incoming VERIFIES relation from its accepting review at height 6234.
[GRAPH_STATUS.json](GRAPH_STATUS.json) records the references and provenance.
The stated class now has public source, scoped independent acceptance and
committed graph evidence.

This is not external human peer review, formalization, historical priority
verification or a proof of the unrestricted dimension-three conjecture.
Graph delivery adds no further mathematical validation.
