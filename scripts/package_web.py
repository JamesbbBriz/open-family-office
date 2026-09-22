#!/usr/bin/env python3
"""Create the public source download without secrets, environments or recursion."""
from pathlib import Path
import hashlib,sys,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from release_check import release_files,check
ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=check()
    if errors:raise ValueError('\n'.join(errors))
    files=[p for p in release_files() if 'downloads' not in p.relative_to(ROOT).parts and p.name!='MANIFEST.sha256']
    output=ROOT/'public/downloads/open-family-office-kit.zip';output.parent.mkdir(parents=True,exist_ok=True)
    entries={f'open-family-office/{p.relative_to(ROOT).as_posix()}':p.read_bytes() for p in files}
    entries['open-family-office/MANIFEST.sha256']=(''.join(hashlib.sha256(content).hexdigest()+'  '+name.removeprefix('open-family-office/')+'\n' for name,content in sorted(entries.items()))).encode()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for name,content in sorted(entries.items()):
            info=zipfile.ZipInfo(name,(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,content)
    print('Built source kit:',output,'bytes',output.stat().st_size)
if __name__=='__main__':main()
