# Provenance and reproduction boundary

Prepared 2026-09-16 by researcher 1 in the Hadwiger--Nelson construction
campaign. The supplied opportunity was one fixed unit-distance conversion of
Exoo--Ismailescu's 13-point `{1,sqrt(2)}` carrier. `ARCHITECTURE.json` was
frozen before the physical four-colour decision. The first complete graph
returned a proper four-word, and construction changes stopped there.

Primary mathematical input:
[Exoo and Ismailescu, The Hadwiger--Nelson problem with two forbidden
distances, arXiv:1805.06055v1, second proof of Theorem 3.1](https://arxiv.org/html/1805.06055v1).
The coordinate and pair lists are small mathematical fixtures transcribed
in both programs; the verifier checks their complete geometric interpretation
and the source's five-chromaticity directly.

The exact 334-point support and its chromatic decision are new author-side
work. The two arithmetic implementations and corruption checks are not a
separate peer review. No teammate's executable or generated graph is needed
for reproduction. The committed Discovery Exoo--Ismailescu interface/core
results concern a different construction and are not used as proof premises.

The source package contains deterministic coordinate generators, compact
colour certificates, proof notes, expected results and checks. Generated
point/edge streams and run logs are kept outside version control. They can be
recreated exactly using `verify.py --write-graph DIR`; the literal four-word
is tied to their canonical order and hashes.

The supported unrestricted record remains Parts's 509-point/2442-edge graph:
[Parts](https://arxiv.org/abs/2010.12665), also explicitly described as current
by [Haugland v4](https://arxiv.org/html/2608.04542v4).
This construction does not improve that record. No claim is made about all
conversions of EI13, all attachments or all plane unit-distance supports.

Publication uses a new directory and an ordinary non-force push to the
authorized repository. Discovery broadcast acceptance, if recorded later,
will remain pending until visible in the committed ledger. Existing pending
receipts and historical evidence are preserved without resubmission.
