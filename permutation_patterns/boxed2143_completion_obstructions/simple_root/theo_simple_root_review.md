# Lyra's separate check of Theo's simple-input root obstruction

Reviewer: literature-researcher-2 (Lyra). Author: literature-researcher-4
(Theo). Date: 2026-10-05. Verdict: **accept the entire finite certificate and
the stated conditional growth implication**, with precisely the exclusions
below. This is internal checking by a different researcher, not external peer
review or a novelty judgment. Full agreed target410 remains unsolved.

The frozen note `SIMPLE_INPUT_ROOT_OBSTRUCTION_V1.md` has SHA256
78140bbf310c7282d13e9952a16d80cc327ebc4f582fcb1df5814abc351201a0.
Its four-file author packet manifest has SHA256
2c76fd811aad930d2bd2eaa3683ad8b063fc1c82ec628845dbc2b212879c7ea8.
This acceptance is separate from review488 of arbitrary inflation and from
any earlier published or pending graph original.

## Exact finite scope and independent reconstruction

The input pi=(3,1,6,4,2,7,5) is simple: every proper contiguous segment of
length2 through6 has a nonconsecutive value set. My own `minimum_interval`
routine enumerates all such segments, rather than importing Theo's simplicity
test. Its maximum is at zero-based position5, so the full scaffold maximum6
would need position4 or5 to sit in an immediately adjacent old gap.

My checker filters all720 permutations of six labels by a direct classical132
triple test. Exactly132 remain, agreeing with C6. I impose only the full-root
position restriction; lower scaffold choices remain free. Exactly56 candidates
remain, with14 at position4 and42 at position5. The independent factorial
filter exhausts every possible scaffold, without calling the author's recursive
grammar. The Catalan split C4*C1 and C5*C0 independently explains these counts:
left values must all exceed right values at the maximum, and both sides must
avoid132. That characterization follows directly by excluding a triple with
left-small/right-large around the maximum.

I interleave old odd labels and scaffold even labels using a separate function.
For every one of the56 candidates, a literal four-index/strict-interior scan
finds a boxed2143. Every selected quadruple in the author's complete JSON list
is a genuine occurrence; the independently obtained ordered rejection list
agrees exactly. No rectangle scanner or author generator supplies the expected
answers. The shared `definition_checker.occurrences` is the explicitly pinned
direct target-definition generator; its output is materialized before testing
emptiness.

The unrestricted-root rho=(4,5,3,6,2,1) passes the independent classical132
test. Its interleaved word
(5,8,1,10,11,6,7,12,3,4,13,2,9) has no literal boxed2143. Its odd positions
recover precisely pi. Its maximum6 has position3, outside the two restricted
positions. This verifies that the failed mechanism concerns full-root adjacency,
and does not refute an unrestricted132 completion for this input.

I exhaustively repeated the smaller simple-input searches: all2,6,46 inputs
of lengths4,5,6 have an allowed witness. At length7 I reproduce the stopping
point at the73rd lexicographic simple input, namely pi above. The complete
success stream has SHA256
8934bd27ab88eb8beb8118dea1cf91a64c96f805e40f2e1a59e61a57814fe693,
with942 attempted scaffolds. This establishes length7 minimality among simple
inputs of length at least4. It does not exhaust length7 or8, and does not assert
minimality of a different mechanism.

## Conditional all-simple bridge

Here t_m counts **all** simple permutations, while s_m in the earlier inflation
reduction counts simple boxed avoiders. These quantities must stay distinct.
The primary author manuscript of Albert--Atkinson--Klazar, *The enumeration of
simple permutations*, https://cs.otago.ac.nz/research/publications/oucs-2003-05.pdf,
Theorem5 and Observation8, was checked live: t_m/m! tends to exp(-2).

If every simple input had such a completion, choose its lexicographically least
allowed scaffold. Odd-position recovery would make this an injection into
the boxed avoiders of length2m-1, hence a_(2m-1)>=t_m. The primary asymptotic
gives t_m>=c*m! for one positive c and all sufficiently large m. Since
m!>=(floor(m/2))^(ceil(m/2)), the (2m-1)-th roots are unbounded. Thus that
universal hypothesis really would imply the negative answer to target410.
The56-candidate certificate disproves the hypothesis; the conditional reasoning
does not establish a lower bound on actual a_n beyond the available inputs.

## Reproduction and trust boundary

From Lyra's research directory:

```sh
python3 -B check_theo_simple_root.py > /tmp/lyra-simple-root.json
```

Dependencies: the frozen author JSON and note in `received/theo_simple_root_v1`,
Lyra's direct `definition_checker.py`, and the independent `minimum_interval`
function in `check_theo_arbitrary_inflation.py`. The author code is not imported
or executed. `theo_simple_root_review_manifest.json` pins these dependencies,
the checker, this written review and `theo_simple_root_reproduction.json`.
Python3.11.2, one process/thread, runtime0.703seconds and16508KiB peak RSS.

## Exclusions

There is no full-target solution, arbitrary-input repair, failure of
unrestricted-root132 completion, factorial avoiding family, novelty or
external-review claim. No existing published or queued partial scope is
expanded. Theo owns publication of this newly checked finite certificate.
