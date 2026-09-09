#!/usr/bin/env python3
"""Compile, regenerate, compare, and independently verify both switch censuses."""
from __future__ import annotations
import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path

INPUT_SHA256="4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"

def need(ok: bool, message: str) -> None:
    if not ok: raise SystemExit(message)

def run(command: list[str], cwd: Path) -> str:
    result=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    need(result.returncode==0,"command failed: "+" ".join(command)+"\n"+result.stdout)
    return result.stdout

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("work",type=Path)
    args=ap.parse_args()
    package=Path(__file__).resolve().parent
    source=package.parent/"ramsey_r55_cyclic43_q13_boundary_certificate"/"objective-twelve-component-fast.json"
    need(hashlib.sha256(source.read_bytes()).hexdigest()==INPUT_SHA256,"input hash mismatch")
    args.work.mkdir(parents=True,exist_ok=True)
    programs={
      "analyze_switches":"analyze_switches.cpp",
      "verify_switches":"verify_switches.cpp",
      "analyze_two":"analyze_minimum_two_switches.cpp",
      "verify_two":"verify_minimum_two_switches.cpp",
    }
    for binary,src in programs.items():
        run(["g++","-std=c++20","-O3","-DNDEBUG","-pthread","-Wall","-Wextra","-Wpedantic",str(package/src),"-o",str(args.work/binary)],args.work)
    generated_one=args.work/"SWITCH_CENSUS.tsv"
    output=[]
    output.append(run([str(args.work/"analyze_switches"),str(source),str(generated_one),"12"],args.work))
    need(generated_one.read_bytes()==(package/"SWITCH_CENSUS.tsv").read_bytes(),"first census differs")
    output.append(run([str(args.work/"verify_switches"),str(source),str(generated_one)],args.work))
    generated_two=args.work/"MINIMUM_TWO_SWITCH_CENSUS.tsv"
    output.append(run([str(args.work/"analyze_two"),str(source),str(generated_one),str(generated_two)],args.work))
    need(generated_two.read_bytes()==(package/"MINIMUM_TWO_SWITCH_CENSUS.tsv").read_bytes(),"two-level census differs")
    output.append(run([str(args.work/"verify_two"),str(source),str(generated_one),str(generated_two)],args.work))
    # A numerical corruption of either certificate must be rejected.
    corrupt=args.work/"CORRUPT.tsv"
    text=generated_one.read_text();corrupt.write_text(text.replace("\t17\t1\t","\t16\t1\t",1))
    bad=subprocess.run([str(args.work/"verify_switches"),str(source),str(corrupt)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    need(bad.returncode!=0,"corrupt first census accepted")
    observed="".join(output)
    need(observed==(package/"EXPECTED_OUTPUT.txt").read_text(),"headline output differs\n"+observed)
    print(observed,end="")
    print("PASS byte-identical regeneration and corruption control")

if __name__=="__main__":main()
