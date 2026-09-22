#!/usr/bin/env python3
"""One command, fail-fast setup; no broker login, API calls, uploads or deployment."""
import argparse, os, subprocess, sys, venv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args,**kwargs):
    print('+',' '.join(map(str,args)),flush=True);return subprocess.run(list(map(str,args)),check=True,**kwargs)
def interpreter(folder):return folder/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');p.add_argument('--without-openbb',action='store_true');p.add_argument('--without-ui-build',action='store_true');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    if sys.version_info<(3,11):p.error('Python 3.11+ is required; 3.12 recommended for full provider stack')
    print('Create project-local environments, install dependencies, build dashboard, test. Private data stays outside repo.')
    extra='all' if a.all else 'analytics'
    commands=[['<.venv python>','-m','pip','install','-e',f'.[{extra}]']]
    if a.all and not a.without_openbb:commands.append(['<.venv-openbb python>','-m','pip','install','-r','requirements/openbb.txt'])
    if not a.without_ui_build:commands.extend([['npm','install','--ignore-scripts'],['npm','run','build:css']])
    commands.extend([['<.venv python>','scripts/build_site.py'],['<.venv python>','-m','unittest','discover','-s','tests','-v'],['<.venv python>','scripts/hh.py','doctor'],['<.venv python>','scripts/package_web.py']])
    if a.dry_run:
        for c in commands:print(' '.join(c))
        return
    folder=ROOT/'.venv';venv.EnvBuilder(with_pip=True).create(folder);python=interpreter(folder)
    run([python,'-m','pip','install','--upgrade','pip'],cwd=ROOT)
    install_dir=Path.home()/'.open-family-office';install_dir.mkdir(mode=0o700,exist_ok=True)
    env=os.environ.copy()
    for c in commands:
        if c[0]=='<.venv-openbb python>':
            other=ROOT/'.venv-openbb';venv.EnvBuilder(with_pip=True).create(other);op=interpreter(other);env['OPENBB_PYTHON']=str(op)
            c[0]=str(op)
        elif c[0]=='<.venv python>':c[0]=str(python)
        run(c,cwd=ROOT,env=env)
    resolved=run([python,'-m','pip','freeze'],capture_output=True,text=True,cwd=ROOT)
    (install_dir/'install-core.txt').write_text(resolved.stdout)
    if env.get('OPENBB_PYTHON'):
        resolved=run([env['OPENBB_PYTHON'],'-m','pip','freeze'],capture_output=True,text=True,cwd=ROOT)
        (install_dir/'install-openbb.txt').write_text(resolved.stdout)
        print('Set OPENBB_PYTHON='+env['OPENBB_PYTHON']+' in your shell/agent environment.')
    print('Installed. Open public/index.html or public/demo.html. Keys are supplied by you; no paid provider has been contacted.')
if __name__=='__main__':
    try:main()
    except (subprocess.CalledProcessError,OSError) as e:
        print('Setup stopped at a failed step; later steps are NOT marked successful: '+str(e),file=sys.stderr);raise SystemExit(1)
