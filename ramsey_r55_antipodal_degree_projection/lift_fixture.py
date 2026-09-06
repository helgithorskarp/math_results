"""Exercise reconstruction on the non-Ramsey G92 fixture; not a search."""
import argparse
import hashlib
import json
from pathlib import Path
from model import Model, write, need

HERE = Path(__file__).resolve().parent
G_SHA = '394aee401f7e9d6843affc05968b305bad2f92cd328035c65b5b8a0da9619a3e'


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    a = p.parse_args(); a.work.mkdir(exist_ok=False)
    path = HERE/'G92.json'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == G_SHA, 'fixture identity')
    red = {tuple(e) for e in json.loads(path.read_text())['red_edges']}
    model = Model(); values = [e in red for e in model.visible]
    write(a.work/'lifted.json',model.complete_degrees(values))
    write(a.work/'projected_fixture.json',model.evaluate(values))
    print(json.dumps({'scope':'degree lifting test only; not a six-neighborhood witness',
                      'evaluation':model.evaluate(values)}),flush=True)


if __name__ == '__main__':
    main()
