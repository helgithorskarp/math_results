"""Fetch only four small, fixed public certificate inputs into a new directory."""
import argparse,hashlib,json,pathlib,urllib.request

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=pathlib.Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('require a new input directory')
    root=pathlib.Path(__file__).resolve().parent
    manifest=json.loads((root/'INPUTS.json').read_text())
    args.output.mkdir(parents=True)
    for row in manifest['inputs']:
        with urllib.request.urlopen(row['url'],timeout=20) as response:data=response.read()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('public input bytes differ: '+row['name'])
        (args.output/row['name']).write_bytes(data)
    print('Four exact public positive inputs fetched; no author executable.')

if __name__=='__main__':main()
