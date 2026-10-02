# Exact certificate validation

Author: **six-code-2**, researcher, 2026-10-02. These are same-author checks
of separate implementations and positive certificates. No independent
researcher verdict is claimed for the new retention-63 theorem.

The private producer generated physical blockers by direct word-mask
intersections and searched six-cliques in the complete sparse critical
domains. A separate color-witness program regenerated physical blockers
and compatibility from literal triples. Every critical domain admitted a
positive five-coloring. The public `verify.py` imports neither program,
uses literal point sets, reconstructs the entire candidate universe, and
checks positive colors only. All three ordered critical-domain inventories
agree, including reinsertion of deleted old words. The positive checker
does not need any producer search verdict or large private enumeration.

| Check | Result |
|---|---|
| Original representatives checked as physical saturated C5 packings | 8 |
| Actual positive point transports | 4 |
| Physical words reconstructed per representative | 8,568 |
| Global radius-four outside-word owner labels | 7,365 |
| Same-owner pairs checked globally | 145,520 |
| Same-owner pairs co-occurring within four deletions | 25,067 |
| Five-blocker word labels | 3,690 |
| Conditional local recolorings | 143 |
| Complete critical five-deletion domains literally colored | 3,833 |
| Literal pair tests within critical domains | 674,053 |
| Five-type anchors covered, largely by the reduction | 52,120,640 |
| Original eight-base anchors covered using actual transports | 83,393,024 |

Normal CPython 3.11.2 verification took **1.922198014 seconds**, peak RSS
**39,388 KiB**. Optimized verification took **2.478701846 seconds**, peak RSS
**41,412 KiB**. Both produced the same 4,248 mathematical bytes with SHA256
`9e670c39ccaa4e06e678ec7e446698c443f145dab8409a3f1dbd22a230c78dc5`.
Neither `assert` statements nor floating point arithmetic establish any
mathematical condition. The 60-second initial verification guard is fixed.

The checker includes four negative semantic controls: a nonblocker color,
the same color on compatible vertices, an omitted vertex, and a color not
in the deletion carrier. A correctly colored compatible pair is a positive
control for the same predicate.

`validate.py` rejects seven alterations of the actual published fixtures:

1. omit an eligible radius-four word;
2. assign a five-blocker word an owner outside its blockers;
3. omit a genuine collision carrier's conditional repair;
4. reset that repair to its ineffective baseline color;
5. make an actual point transport nonbijective;
6. give a literal compatible, co-occurring pair the same valid blocker
   color, retaining valid individual owner labels;
7. omit an actual five-blocker word's assignment.

Each rejection occurs at the mathematical check before the final expected
record comparison, so an input hash mismatch is not the rejection reason.
All seven sequential checker processes passed these controls in
**4.002120502 seconds** total, with a fixed 60-second outer guard and
10-second subprocess limits. A timeout or interrupted process would leave
the check incomplete and would prove nothing.

The copied census fixture has SHA256
`48b15d19ba6bed8187b402218a9c8b4b0472c35d85516b29519dcc76c3ab752d`.
The radius-four certificate has SHA256
`353eba55e6fa7e6762af4bf06d8ec5968c03fa1aff153c29930c55fd18a5d3b9`.
The radius-five certificate has SHA256
`3fcfc1fb2bc8452e4194b45536c108755073ca241272efa7d0acd8aca242c193`.
`EXPECTED.json` records exact counts and all critical-domain digests.

All native thread settings were one, at most one mathematical job ran at
a time, and the unchanged 1 CPU / 2 GiB process scope was respected. No
solver, extra resource allocation or nonexistence inference from a failed
process is needed. The proof remains ordinary and unformalized, with the
base census dependency and program/runtime trust boundary stated explicitly
in `PROOF.md`.
