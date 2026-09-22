#!/usr/bin/env python3
"""Operator-run publishing helper. Dry-run by default; private by default.

A clean temporary repository contains ONLY reviewed allowlisted files, never old Git history.
No token is requested or embedded. Uses the operator's existing authenticated GitHub CLI.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from release_check import ROOT,check,release_files
DESCRIPTION='Household-first agent workflows for wealth, income durability, liquidity and multi-asset scenarios. Local-first. No trading.'
TOPICS=['agent-skills','asset-management','personal-finance','cash-flow','financial-planning','local-first','python','fintech']

def run(args,cwd=None,capture=False):
    return subprocess.run(args,cwd=cwd,check=True,text=True,capture_output=capture)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,help='Explicit owner/new-repository-name')
    p.add_argument('--publish',action='store_true',help='Actually create and push a NEW repository')
    p.add_argument('--public',action='store_true',help='Explicitly authorise public visibility; otherwise private')
    args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+',args.repo):p.error('--repo must be owner/name')
    issues=check()
    if issues:
        print('\n'.join(issues),file=sys.stderr);return 1
    visibility='public' if args.public else 'private'
    print(f'Plan: create NEW {visibility} repository {args.repo}, copy reviewed source only, push one initial commit, set topics/template metadata.')
    print('No social posts, issue seeding, GitHub Pages deployment or release publication is performed.')
    if not args.publish:
        print('DRY RUN ONLY. Review files and add --publish to execute. No network call made.');return 0
    for binary in ['git','gh']:
        if not shutil.which(binary):raise RuntimeError(f'{binary} is required on your machine')
    run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT)
    run(['gh','auth','status'])
    name=run(['git','config','user.name'],cwd=ROOT,capture=True).stdout.strip()
    email=run(['git','config','user.email'],cwd=ROOT,capture=True).stdout.strip()
    if not name or not email:raise RuntimeError('Set your desired git user.name and user.email before publishing')
    # Publishing an existing history is intentionally unsupported.
    with tempfile.TemporaryDirectory(prefix='open-family-office-release-') as td:
        stage=Path(td)
        for source in release_files():
            rel=source.relative_to(ROOT);dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        run(['git','init','-b','main'],cwd=stage)
        run(['git','config','user.name',name],cwd=stage);run(['git','config','user.email',email],cwd=stage)
        run(['git','add','--','.'],cwd=stage)
        run(['git','commit','-m','Initial Open Family Office workflow kit'],cwd=stage)
        run(['gh','repo','create',args.repo,'--'+visibility,'--description',DESCRIPTION,'--source',str(stage),'--remote','origin','--push'],cwd=stage)
        print('Repository created and pushed. Any later metadata failure does NOT undo publication.')
        run(['gh','api',f'repos/{args.repo}','--method','PATCH','-F','is_template=true','-F','has_discussions=true'])
        # GitHub accepts a names array for repository topics.
        command=['gh','api',f'repos/{args.repo}/topics','--method','PUT']
        for topic in TOPICS:command+=['-f',f'names[]={topic}']
        run(command)
    print(f'Done. Review https://github.com/{args.repo} and follow launch/GITHUB-SETUP.zh-CN.md for social preview, pinned discussion and optional demo hosting.')
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (RuntimeError,subprocess.CalledProcessError,OSError) as e:
        print(f'Publish stopped: {e}',file=sys.stderr);raise SystemExit(1)
