"""Explicit acyclic ownership graph. Only leaf economic assets are consolidated."""
from decimal import Decimal
from ..core import InputError, number, fraction, money

def consolidate(graph):
    nodes={n['id']:n for n in graph['nodes']}
    if len(nodes)!=len(graph['nodes']):raise InputError('Duplicate entity/asset id')
    root=graph['root']
    if root not in nodes:raise InputError('Unknown root')
    children={k:[] for k in nodes};inbound={k:Decimal(0) for k in nodes}
    seen=set()
    for e in graph['edges']:
        parent,child=e['owner'],e['owned']
        if parent not in nodes or child not in nodes or (parent,child) in seen:raise InputError('Unknown or duplicate ownership edge')
        seen.add((parent,child));pct=fraction(e['share'],'ownership share')
        children[parent].append((child,pct));inbound[child]+=pct
        if inbound[child]>1:raise InputError('Total ownership of an entity exceeds 100%')
    if inbound[root]>0:raise InputError('Consolidation root cannot be owned in this graph')
    def check_cycles(k,path):
        if k in path:raise InputError('Ownership graph must be acyclic')
        for c,p in children[k]:check_cycles(c,path|{k})
    for node in nodes:check_cycles(node,set())
    totals={};paths={}
    def visit(k,share,path):
        n=nodes[k]
        if children[k]:
            if 'value_base' in n:raise InputError('Do not count an intermediate entity valuation and its underlying assets together')
            for c,p in children[k]:visit(c,share*p,path+[c])
        elif n.get('kind') in ('asset','liability'):
            value=number(n['value_base'])
            if value<0:raise InputError('Leaf values must be nonnegative; specify liability kind for debts')
            totals[k]=totals.get(k,Decimal(0))+share*value*(-1 if n['kind']=='liability' else 1)
            paths.setdefault(k,[]).append({'path':path,'attributable_share':str(share)})
    visit(root,Decimal(1),[root])
    return {'root':root,'currency':graph['base_currency'],'net_value_base':money(sum(totals.values(),Decimal(0))),
      'leaves':[{'id':k,'value_base':money(v),'ownership_paths':paths[k]} for k,v in totals.items()],
      'warnings':['Only explicit ownership is modeled. Control, legal beneficial rights, guarantees and tax are not inferred.','Values must already be converted into the stated base currency.']}

def exposures(positions):
    totals={};gross=Decimal(0)
    for p in positions:
        value=number(p['value_base']);gross+=value
        if value<0:raise InputError('Exposure view requires positive gross asset values')
        for dimension,weights in p.get('exposures',{}).items():
            subtotal=sum((fraction(w,k) for k,w in weights.items()),Decimal(0))
            if subtotal>1:raise InputError('Exposure weights cannot exceed 100% within a dimension')
            bucket=totals.setdefault(dimension,{})
            for label,weight in weights.items():bucket[label]=bucket.get(label,Decimal(0))+value*fraction(weight,label)
    if gross<=0:raise InputError('Need positive gross assets')
    for dimension,bucket in totals.items():
        bucket['unknown']=gross-sum(bucket.values(),Decimal(0))
    return {'gross_assets':money(gross),'dimensions':{d:{k:{'amount':money(v),'share':str(v/gross)} for k,v in b.items()} for d,b in totals.items()},
      'warnings':['Dimensions overlap: never add geographic, currency and sector totals together.','Exposure weights are explicit inputs, not inferred betas or guaranteed correlations. Unknown is retained.']}
