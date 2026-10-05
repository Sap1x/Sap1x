#!/usr/bin/env python3
"""Render the animated 53-week contribution heatmap from the local snapshot."""
import datetime as dt, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILE=json.loads((ROOT/'config/profile.json').read_text())
SRC=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'data/contributions.json'
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'contrib-heatmap.svg'
data=json.loads(SRC.read_text()); contribs=data['days']; total=data['total_contributions']
if not contribs: raise SystemExit('No contribution data. Run fetch_contributions.py first.')
CELL,GAP,RAD,LEFT,TOP=13,3,2.5,34,24; COLORS=['#161b22','#0e4429','#006d32','#26a641','#39d353']; GRAY='#7d8590'; MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; n=len(contribs); NW=(n+6)//7; W=LEFT+NW*(CELL+GAP)+6; H=TOP+7*(CELL+GAP)+22
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif"><style>.lbl{{fill:{GRAY};font-size:13px;font-weight:600}}.total{{fill:#e6edf3;font-size:15px;font-weight:700}}.c{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pop .55s ease-out both}}@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}60%{{opacity:1;transform:scale(1.1)}}100%{{opacity:1;transform:scale(1)}}}}@media (prefers-reduced-motion:reduce){{.c{{opacity:1!important;animation:none!important}}}}</style>']
sd=dt.date.fromisoformat(contribs[0]['date']); last=None
for wk in range(NW):
    d=sd+dt.timedelta(days=wk*7)
    if d.month!=last: last=d.month; parts.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-8}">{MONTHS[d.month-1]}</text>')
for name,row in [('Mon',1),('Wed',3),('Fri',5)]: parts.append(f'<text class="lbl" x="2" y="{TOP+row*(CELL+GAP)+CELL-2}">{name}</text>')
for i,c in enumerate(contribs):
    wk,row,lvl=i//7,i%7,c['level']; x=LEFT+wk*(CELL+GAP); y=TOP+row*(CELL+GAP); delay=(wk+row*.55)/max((NW-1)+6*.55,1)*3.6
    parts.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" fill="{COLORS[min(lvl,4)]}" style="animation-delay:{delay:.3f}s"/>')
parts.append(f'<text class="total" x="{LEFT}" y="{H-6}">{total:,} contributions in the last year</text></svg>'); OUT.write_text(''.join(parts)); print(f'wrote {OUT}')
