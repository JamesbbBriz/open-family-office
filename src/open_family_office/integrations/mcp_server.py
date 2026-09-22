"""Read-only stdio MCP adapter. Scope is a user-selected workspace, never a broad filesystem."""
import json, os
from pathlib import Path
from ..core import InputError, snapshot, cashflow, stress
from ..io import read_json, outside_repo

def confined(root:Path,relative:str)->Path:
    target=(root/relative).resolve()
    if target!=root and root not in target.parents:raise InputError('Path outside explicit MCP workspace')
    if not target.is_file() or target.suffix.lower()!='.json':raise InputError('MCP reads JSON files only')
    return target

def main():
    try:from mcp.server.fastmcp import FastMCP
    except ImportError:raise InputError('Install mcp extra to start the server') from None
    value=os.environ.get('OFO_WORKSPACE')
    if not value:raise InputError('Set OFO_WORKSPACE to the explicit PRIVATE folder you authorize this agent to read')
    root=outside_repo(value)
    if not root.is_dir():raise InputError('Workspace does not exist')
    server=FastMCP('Open Family Office - read-only')
    hints={'readOnlyHint':True,'destructiveHint':False,'openWorldHint':False}
    @server.tool(annotations=hints)
    def household_snapshot(file:str='household.json')->dict:
        """Read a balance sheet within the authorized workspace; never edits files."""
        return snapshot(read_json(confined(root,file)))
    @server.tool(annotations=hints)
    def household_cashflow(file:str='household.json',months:int=24)->dict:
        """Calculate dated monthly cash budget; not a return forecast."""
        return cashflow(read_json(confined(root,file)),months)
    @server.tool(annotations=hints)
    def household_stress(scenario_file:str,file:str='household.json',months:int=24)->dict:
        """Evaluate explicit local scenario assumptions."""
        return stress(read_json(confined(root,file)),read_json(confined(root,scenario_file)),months)
    @server.tool(annotations=hints)
    def research_optimize(file:str,engine:str='scipy',method:str='min_variance')->dict:
        """Research liquid-sleeve weights; no recommendations or order placement."""
        from ..quant.allocation import optimize
        return optimize(read_json(confined(root,file)),engine,method)
    @server.tool(annotations=hints)
    def research_simulate(file:str)->dict:
        """Simulate explicit liquid-sleeve assumptions, not a probability of investment success."""
        from ..quant.simulation import simulate
        return simulate(read_json(confined(root,file)))
    @server.tool(annotations=hints)
    def ownership_lookthrough(file:str)->dict:
        """Consolidate explicit ownership graph without double-counting parents and leaves."""
        from ..quant.ownership import consolidate
        return consolidate(read_json(confined(root,file)))
    @server.tool(annotations=hints)
    def provider_status()->dict:
        """Inspect required credentials without returning any values; does not contact providers."""
        from .registry import providers
        return {'providers':providers()}
    server.run(transport='stdio')
