# hh-optimize

## Goal

Compare liquid-sleeve allocation research objectives.

## Procedure and controls

Read methodology and the confirmed household policy first. Require a separate JSON file declaring `universe_type=liquid_proxy_research`, uniquely named instruments, complete decimal simple returns, frequency, dates and constraints. Never insert private property, businesses or locked pension positions as liquid observations. Use `python scripts/hh.py optimize <file> --engine <scipy|skfolio|pypfopt> --method <method>`. Check doctor before native engines; reject unsupported combinations. Black–Litterman requires explicit annual prior returns, views and confidences; never invent them. Review solver status, finite weights, constraints, sample window and assumptions. Present side-by-side research, not recommendations or trades. Use outside-repo `--out` for approved output.

## Completion

Return the actual calculation/output location, the methods executed and their limitations. Do not claim installation, live connection or host validation merely because source code exists.
