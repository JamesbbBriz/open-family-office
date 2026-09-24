#!/usr/bin/env python3
"""Best-effort release hygiene; NOT comprehensive PII/security certification."""
from pathlib import Path
import json
import re
import sys
import zipfile
ROOT=Path(__file__).resolve().parents[1]
DIRECTORIES={'.agents','.claude','.github','agent','assets','config','docs','examples','src','scripts','web','tests','requirements','vendor','public'}
FILES={'README.md','README.zh-CN.md','AGENTS.md','CLAUDE.md','GEMINI.md','LICENSE','THIRD_PARTY.md','SECURITY.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md','ROADMAP.md','CHANGELOG.md','pyproject.toml','.gitignore','.gitattributes','package.json','package-lock.json','THIRD_PARTY_NOTICES.txt','MANIFEST.in','setup.py','server.json'}
IGNORE={'.git','__pycache__','.pytest_cache','.venv','.venv-openbb','node_modules','.DS_Store','build','dist','.eggs'}

def release_files(root:Path=ROOT)->list[Path]:
    result=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if any(part in IGNORE or part.endswith('.egg-info') for part in rel.parts):continue
        if p.is_symlink():raise ValueError(f'Symlinks are not allowed in release: {rel}')
        if not p.is_file():continue
        if p.suffix in {'.pyc','.pyo'}:continue
        if (len(rel.parts)==1 and rel.name in FILES) or (len(rel.parts)>1 and rel.parts[0] in DIRECTORIES):result.append(p)
        else:raise ValueError(f'Unexpected release file: {rel}; review it, do not silently publish')
    return sorted(result)

def check(root:Path=ROOT)->list[str]:
    errors=[]
    try:paths=release_files(root)
    except ValueError as e:return [str(e)]
    for p in paths:
        rel=p.relative_to(root)
        if any(part.lower() in {'private','workspace','workspaces','statements','secrets','credentials'} for part in rel.parts):errors.append(f'Private-looking path: {rel}')
        if p.name.startswith('.env') or p.suffix in {'.pem','.key','.p12','.pfx'}:errors.append(f'Secret-looking file: {rel}')
        if p.suffix in {'.png','.jpg','.gif','.ico'}:continue
        if rel.as_posix()=='public/downloads/open-family-office-kit.zip':
            try:
                with zipfile.ZipFile(p) as z:
                    for member in z.infolist():
                        bits=Path(member.filename).parts
                        if not bits or bits[0]!='open-family-office' or '..' in bits or any(b in IGNORE for b in bits) or member.filename.endswith('.zip'):
                            errors.append(f'Unsafe source archive entry: {member.filename}')
                        if any(b.lower() in {'private','workspace','workspaces','statements','secrets','credentials'} for b in bits):
                            errors.append(f'Private-looking source archive entry: {member.filename}')
                    if z.testzip():errors.append('Corrupt source download archive')
            except zipfile.BadZipFile:errors.append('Invalid source download archive')
            continue
        try:text=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:errors.append(f'Unexpected binary file: {rel}');continue
        patterns=[r'ghp_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{50,}',r'sk-[A-Za-z0-9_-]{32,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
        if any(re.search(pattern,text) for pattern in patterns):errors.append(f'Possible credential in {rel}')
        if p.suffix=='.json':
            try:data=json.loads(text)
            except json.JSONDecodeError:errors.append(f'Invalid JSON: {rel}');continue
            if isinstance(data,dict) and 'synthetic' in data and 'assets' in data and data.get('synthetic') is not True and rel.as_posix()!='agent/templates/household.json':errors.append(f'Non-synthetic household in release: {rel}')
        if p.suffix=='.md':
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                target=link.split(' ')[0].split('#')[0]
                if not target or re.match(r'^[a-zA-Z][\w+.-]*:',target):continue
                if not (p.parent/target).resolve().exists():errors.append(f'Broken local link in {rel}: {target}')
    return errors

if __name__=='__main__':
    errors=check()
    if errors:
        print('\n'.join(errors),file=sys.stderr);raise SystemExit(1)
    print(f'Release hygiene passed for {len(release_files())} allowlisted files. Human privacy review still required.')
