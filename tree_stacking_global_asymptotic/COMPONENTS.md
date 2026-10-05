# Frozen components and logical interfaces

Prepared by Atlas / `studio-researcher-1`, researcher, 2026-10-05.
The exact assembly is `PROOF.md`; full source sizes and SHA256 values are
in [MANIFEST.json](MANIFEST.json). The four checks below are distinct
other-researcher internal checks of the actual listed versions.

| Component | Author | Internal checker | Frozen proof | Actual report |
| --- | --- | --- | --- | --- |
| Inherited classification | Iris | Atlas | [Proof](components/iris_classification_v1/PROOF.md) | [Report](internal_checks/atlas_classification_v1/REVIEW.md) |
| Universal tree budget | Atlas | Nova | [Proof](components/atlas_structural_v1/PROOF.md) | [Report](internal_checks/nova_structural_v1/REVIEW.md) |
| Uniform analytic upper | Rowan | Iris | [Proof](components/rowan_upper_v1/PROOF.md) | [Report](components/rowan_upper_v1/internal_checks/iris_full_v1/REVIEW.md) |
| Eventual all-order lower | Nova | Rowan | [Proof](components/nova_lower_v1/PROOF.md) | [Report](internal_checks/rowan_lower_v1/REVIEW.md) |

The author files and reports keep the exact accepted bytes. Component
`ACCEPTED_SCOPE.md` files record later scoped acceptance without editing
historical preparation/pending language. Final assembly checking is a
separate responsibility assigned to Nova. Nova's lower result is checked
by Rowan, and its acceptance is not inferred from Nova's assembly check.

## Counting and normalization

Iris's accepted proof SHA256 is
`e49e654abe3ae31e360033541aae4a58d93119a91f6ab400095f17d92e00427f`.
Atlas's report SHA256 is
`8ede8dcfdcc300f88233e434e6fa8ec4e7b326a381f283135a3ceee0efea7caa`.
The accepted scope is Sections 1--7, at Fairfax-Ball2609.31811v1
Theorems 3.3 and 1.1. It supplies the prior exact all-critical
classification and its count, not merely sufficient configurations.
See its [acceptance metadata](components/iris_classification_v1/ACCEPTED_SCOPE.md).

For n>=3, all degrees are full-tree degrees, and all distances are ambient
tree distances. The nonleaf core is connected and has the same distances.
P is the graph-leaf-parent set, Xp=F(p), and P* includes every tie for
the largest Xp. The exact individual-function count is

    N(T) = sum_{p in P*} binom(Xp+dp-1,dp-1).

The audited equality argument exhausts the convex branch majorant and
proves the all-target-zero converse. EMPTY remains distinct from an
occupied zero message. Positive Xp makes different sibling families
disjoint. The single-leaf-parent-size term dp=1 contributes one. Stars
and K2 are explicitly accounted for. This is an inherited theorem audit;
predecessor code/censuses are source provenance rather than correctness
inputs to this assembly.

## Universal structural budget

Atlas's accepted proof SHA256 is
`8f57991e5d268f38cc0d0fd7a525accd04e7aa07dce135621d9b620e822ded77`.
Nova's report SHA256 is
`0e5475225e16e34a55c523c53ec6ffeda4582371569144363c9680ad8f30cfcb`.
The accepted scope is structural equations 1--13. Its inherited counting
equation14 is supplied by Iris's separate accepted classification.
See its [acceptance metadata](components/atlas_structural_v1/ACCEPTED_SCOPE.md).

For p in P*, hp is the eccentricity within the nonleaf core. It is not
a directed structural deficit. The full eccentricity to graph leaves
is H=hp+1. In nonstars H>=2; in stars hp=0. The universally consumed
budget and potential estimate are

    n >= hp+1+(9/5)dp-(4/5)dp*2^(-hp),
    0 < Xp <= 2(n-1)*2^hp.

The stronger nonstar budget adds positive slack and is not applied to
stars. The edge pairing works without a core-endpoint characterization
and includes tied maximizing parents and dp=1.

The author finite controls have 594 input cases, with repeated parameter
controls acknowledged, 16106 directed-deficit identities, 2243 edge
certificates, 1933 heavy-edge pairings and 1145 maximizing-parent budgets.
Nova reproduced the same source once with byte-identical expected JSON
in CPU0.556336s and peak15820KiB, and separately reconstructed the
ordinary proof. This is neither an independent finite enumerator nor
a universal exhaustive tree census.

## Analytic upper

Rowan's accepted proof SHA256 is
`89cb5a4a3fef9e32c48a6de6b605cb4ecabdf3cd803493d979a7519142b3e8bc`.
Iris's report SHA256 is
`160777ca6247b2a2b7b2c0be1ccef1cca71e328d430acd14fad3afe845093e0c`.
The accepted scope is Sections 1--5 under their displayed parameter
hypotheses. See its [acceptance metadata](components/rowan_upper_v1/ACCEPTED_SCOPE.md).

The parameter lemma uses the preceding count, potential estimate, weak
budget and at most n maximizing parents. It preserves the factorial
in the binomial bound, so its remainder is linear uniformly in the
height and dp. The assembly discharges both mathematical imports and
gives C_plus=6 for every n>=2, with K2 handled separately. Stars have
hp=0 and need no cutoff. This ordinary analytic check required no
new computation and has no lower or classification acceptance scope.

## All-order lower

Nova's accepted proof SHA256 is
`b7198174579fe7c275218c9e087b1ba0a350d28e1dad63e69e1bd0f051e37da8`.
Rowan's report SHA256 is
`2ebf638b27df6d5f14e95727fdd34c7a9c2fb6ccc9bde179b3ed5bbeaa26a1c8`.
See its [acceptance metadata](components/nova_lower_v1/ACCEPTED_SCOPE.md).

The literal prior family R(d,e,t) has order d+2e+t+1. For n=18m+1+s,
m>=2 and 0<=s<=17, take d=5m+3, e=2m+2, t=9m-7+s. These cover every
integer n>=37 and have a strictly unique maximizing large leaf class.
The sufficient configurations give

    log2 N(T_n) > 5n^2/36 - 5n/4.

The standalone lower uses primary identity(4) and Theorems 1.1, 3.3,
4.1; it needs sufficiency rather than converse classification. The
assembly can obtain sufficiency from the accepted classification and
does not need an additional external4.1 import for its own proof.

Rowan independently checked the ordinary proof and reproduced one
bounded run: 90 witness trees across all eighteen residues, six extra
controls and 378 rooted-score checks. Its deterministic record digest
is `67c620281ebb8fe9deb170fb7bba5d30ce5ea1fb651b1244e3806aace47731a1`;
resource receipt: CPU2.569607512s, peak16040KiB. This is a replay of the
author algorithm, not an arbitrary-move oracle or proof of the infinite
range by sampling.

The public lower `INPUTS.json` is Nova's metadata derivative SHA256
`a0ba7082f72e86a8d471f39dae9bad3bdcf5cfeb404231aa45b270555cb6452e`.
The original checked metadata SHA256
`bc52c70df893dca7134fa602e3b4d7ee86d7c52b4e061986dd7d523a8d5e2483`
remains preserved privately. Only eight cache/extracted-file path fields
were removed and one publication annotation added. A reversible field
comparison leaves all mathematical inputs unchanged. The final assembly
checker must inspect this incorporated derivative as provenance metadata;
the proof, code, result and report files themselves are unchanged.

## Assembly range and limits

The common asymptotic range is n>=37, with C_minus=5/4 and C_plus=6.
The upper alone holds for n>=2. No restricted-family exact optimizer,
onset91 assertion, optimal linear coefficient, formal build, external
review or priority verdict is an input to this argument. Source-byte
integrity and named votes do not establish mathematical correctness.
