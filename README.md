# math_results

Source code behind mathematical results committed to the [Discovery Net](https://github.com/njallskarp/discovery_net)
knowledge graph, chain `discovery-net`.

## What lives here

The programs that *produce* results: search and enumeration code, SAT encodings,
certificate checkers, Lean formalisations, and the scripts used to reproduce a
published claim end to end.

## What does not live here

- **Proof logs and solver traces.** DRAT files, SAT solver output, and raw search
  logs are throwaway local artifacts. They are regenerable by rerunning the code
  in this repository and are often enormous — a single DRAT file from one run
  reached 57 GB. Nothing of that kind is committed.
- **The results themselves.** A claim, its statement, and its assessment live on
  chain as signed contributions, not as files here.
- **Keys, node state, or ledger databases.**

The division: the chain carries the description of a result, this repository
carries the code that generates it, and the logs stay on local disk.

## Reproducing a result

Each directory corresponds to one contribution on the chain and contains the
code, the exact commands, tool versions, and hashes needed to rerun it. Where a
result rests on a computation rather than a hand proof, the trust boundary is
stated explicitly — including any use of `native_decide` in Lean, or reliance on
an external solver's UNSAT answer.

## Layout

```
<area>/<result-slug>/
  README.md      what it computes, how to run it, what it establishes
  ...            solver input generators, checkers, Lean sources
```
