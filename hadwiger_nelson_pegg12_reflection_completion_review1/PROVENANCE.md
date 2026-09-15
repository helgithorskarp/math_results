# Provenance and source integrity

Target package: sibling directory
`hadwiger_nelson_pegg12_reflection_completion_stop`, mathematical commit
`beab314a6e106e524d6cbdcd26d26e785e0c5e7f`.

Pinned target inputs:

```text
certificate.json
0c8a7b2e2015f27adb69855a13768101ec2bf36166d1968c8b44d91b3628edea
expected.json
660590bc43073e81688164dec3b681eaacb013a928682edff111042db86acbb0
model.py
ba17b7bad40d2baf6fa0efb6c7064f211a008fa0dfd963d7225b90dcd352135e
verify.py
8af7692cd13245c94af8498b5b8620537a2005c0dcbfcc93fb98666627de53e5
```

The target checksum manifest passed, and normal and optimized target verifier
outputs were byte-identical. Corruption controls also passed.

Ed Pegg's original graph list is in the Math StackExchange question
<https://math.stackexchange.com/questions/3958839/are-4-chromatic-3-connected-unit-distance-graphs-always-rigid>.
Parcly Taxel's answer links the Shibuya implementation and lists
`{UnitDistance,{12,2}}` as rigid.

The coordinate producer was checked at Shibuya commit
`218097c9971db2b60ab94a0b8dae20d76741cc43`. The local detached clone and the
raw GitHub file agreed byte-for-byte:

```text
shibuya/graphs/pegg.py
2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1
shibuya/generators.py
f80d80994c712049aedfcac1c635a0f6691d9c296e2ac42cbe7981394359f500
```

As a source-integrity check rather than a proof premise, Shibuya's original
100-decimal `findroot` reconstruction gave parameters

```text
t = 1.801552330664620012499550152947576373031...
u = 1.340040322925173225963093230331926511166...
```

and its 12 numerical points agreed with the independently encoded exact
radical formulas to maximum absolute difference `2.18e-101`; both defining
residuals were below `1.43e-101`. The exact verification itself does not use
this numerical comparison or trust Shibuya's floating-point predicates.

Review host: CPython 3.11.2 on Linux. No third-party package is required for
the published checker. Mathematical review commit:
`MATHEMATICAL_COMMIT_TO_BE_RECORDED`.
