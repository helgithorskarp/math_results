# Validation record

Validated on 2026-09-13 UTC with Python 3.

- All six Python sources passed `py_compile`.
- `EXPECTED.json` and `SOURCE_PINS.json` passed `python3 -m json.tool`.
- `git diff --check` passed.
- The exact two-phase run completed all 495 cases: 495 four-colourable,
  483 not three-colourable, no unknown result; maximum order 45 and maximum
  size 124.
- The exact positive power ladder completed through `K=20`: its 495-vertex,
  1251-edge endpoint is four-colourable; `K=21` has 519 vertices and was
  stopped before colouring.
- The depth-two closure replay completed all 495 cases: 495 discovered strict
  graphs had valid four-colour words, no timeout, maximum 303 vertices and
  1713 edges.
- Mixed-phase replays completed 528 three-orbit, 680 four-orbit, and 715
  five-orbit cases.  Every discovered graph had a valid four-colour word and
  there were no timeouts.

The exact programs certify only positive colourability, which needs no UNSAT
proof trace.  The closure and mixed-phase runs retain the floating-point trust
boundary described in `REPRODUCE.md`; they are experimental construction
screens.  This package has not yet received independent review.

