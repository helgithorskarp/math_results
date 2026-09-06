#!/usr/bin/env python3
"""Bounded disjoint-parent execution; the older sequential runner is retained."""
import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from hashlib import sha256
import json
import multiprocessing
from pathlib import Path
import signal
import time
from batch import save, run, model
from fast_check import check
from physical import catalog, require

stop_requested = False


def request_stop(signum, frame):
    global stop_requested
    stop_requested = True


def decide(index, record, args):
    # Each worker owns exactly one parent directory at a time. No retries.
    folder = args.folder/f"parent{index:03d}"
    folder.mkdir(exist_ok=True)
    checkpoint = folder/"result.json"
    require(not checkpoint.exists() and not (folder/"solver.log").exists(), "Previously started parent")
    result = {"parent": index, "seed": record, "status": "STARTED"}
    if not (folder/"family.cnf").exists():
        result["generation"] = run([args.generator, args.catalog, index, folder/"family.cnf"],
                                    folder/"generation.log", 60)
        require(result["generation"]["exit_code"] == 0, "Generation failed")
    result["cnf_sha256"] = sha256((folder/"family.cnf").read_bytes()).hexdigest()
    result["solver"] = run([args.kissat, "--time=30", "--no-binary", folder/"family.cnf", folder/"proof.drat"],
                            folder/"solver.log", 45)
    code = result["solver"]["exit_code"]
    if code == 10 and not result["solver"]["wall_timeout"]:
        save(folder/"target.json", model(record, folder/"solver.log"))
        result["status"] = "DIRECTLY_CHECKED_TARGET"
    elif code == 20 and not result["solver"]["wall_timeout"]:
        require("s UNSATISFIABLE" in (folder/"solver.log").read_text(), "Missing UNSAT status")
        result["status"] = "UNSAT_PROOF_PENDING"
        save(checkpoint, result)
        result["proof_check"] = run([args.drat_trim, folder/"family.cnf", folder/"proof.drat",
                                      "-c", folder/"core.cnf", "-l", folder/"trimmed.drat"],
                                     folder/"proof_check.log", 300)
        require(result["proof_check"]["exit_code"] == 0 and
                "s VERIFIED" in (folder/"proof_check.log").read_text(), "Unverified proof")
        start = time.monotonic()
        result["certificate"] = check(record, folder/"core.cnf", folder/"trimmed.drat", args.checker)
        result["direct_check_seconds"] = time.monotonic()-start
        result["status"] = "CHECKED_SWITCH_EXTENSION_EXCLUSION"
    else:
        result["status"] = "NO_CONCLUSION"
    result["files"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p.read_bytes()).hexdigest()}
                       for p in sorted(folder.iterdir()) if p.is_file() and p.name != "result.json"}
    save(checkpoint, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path(__file__).with_name("r55_42some.g6"))
    for name in ["generator", "kissat", "drat-trim", "checker"]:
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    require(1 <= args.jobs <= 4, "Worker bound")
    for name in ["folder", "catalog", "generator", "kissat", "drat_trim", "checker"]:
        setattr(args, name, getattr(args, name).resolve())
    records = catalog(args.catalog)
    args.folder.mkdir(parents=True, exist_ok=True)
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    start = time.monotonic()
    completed, pending, errors = {}, [], []
    # Existing cases are replayed and never solved a second time.
    for index, record in enumerate(records):
        if stop_requested or (args.folder/"STOP").exists():
            save(args.folder/"parallel_stopped.json", {"status": "STOPPED_DURING_PREFLIGHT", "parent": index})
            return
        folder = args.folder/f"parent{index:03d}"
        checkpoint = folder/"result.json"
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_text())
            require(saved["parent"] == index and saved["seed"] == record, "Saved input mismatch")
            require(saved["status"] == "CHECKED_SWITCH_EXTENSION_EXCLUSION", "Unresolved prior case; no retry")
            require(check(record, folder/"core.cnf", folder/"trimmed.drat", args.checker) == saved["certificate"],
                    "Saved certificate mismatch")
            completed[index] = saved
        else:
            require(not (folder/"solver.log").exists(), "Interrupted prior solver; no retry")
            pending.append(index)
    print(json.dumps({"status": "PREFLIGHT_CHECKED", "parents": sorted(completed), "remaining": len(pending)}), flush=True)
    cursor, halted = 0, False
    # Spawned processes avoid inheriting the controller's signal handler.
    with ProcessPoolExecutor(max_workers=args.jobs, mp_context=multiprocessing.get_context("spawn")) as pool:
        active = {}
        while active or (cursor < len(pending) and not halted):
            halted = halted or stop_requested or (args.folder/"STOP").exists()
            while not halted and len(active) < args.jobs and cursor < len(pending):
                index = pending[cursor]
                cursor += 1
                active[pool.submit(decide, index, records[index], args)] = index
            if not active:
                break
            ready, _ = wait(active, timeout=1, return_when=FIRST_COMPLETED)
            for future in sorted(ready, key=lambda f: active[f]):
                index = active.pop(future)
                try:
                    result = future.result()
                    completed[index] = result
                    if result["status"] != "CHECKED_SWITCH_EXTENSION_EXCLUSION":
                        halted = True
                    print(json.dumps({"parent": index, "status": result["status"],
                                      "solver_seconds": result["solver"]["wall_seconds"]}), flush=True)
                except Exception as error:
                    errors.append({"parent": index, "error": repr(error)})
                    halted = True
                save(args.folder/"parallel_progress.json", {
                    "checked": sum(r["status"] == "CHECKED_SWITCH_EXTENSION_EXCLUSION" for r in completed.values()),
                    "completed_parents": sorted(completed), "active_parents": sorted(active.values()),
                    "not_dispatched": pending[cursor:], "errors": errors,
                    "elapsed_seconds": time.monotonic()-start})
    successful = sorted(i for i, r in completed.items() if r["status"] == "CHECKED_SWITCH_EXTENSION_EXCLUSION")
    if successful == list(range(328)) and not errors:
        save(args.folder/"completed.json", {"status": "CHECKED_ENTIRE_CATALOG_SWITCH_EXTENSION_UNION", "parents": 328,
                                           "jobs": args.jobs, "elapsed_seconds": time.monotonic()-start})
        print("CHECKED_ENTIRE_CATALOG_SWITCH_EXTENSION_UNION", flush=True)
    else:
        save(args.folder/"parallel_stopped.json", {"status": "STOPPED_WITH_CHECKPOINTS", "checked_parents": successful,
                    "not_dispatched": pending[cursor:], "errors": errors, "active_parents": []})


if __name__ == "__main__":
    main()
