#!/usr/bin/env python3
"""Render a live-looking terminal stats card from contributions.json."""
import datetime as dt
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT/'config/profile.json').read_text())
SRC = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'data/contributions.json'
OUT = Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'stats.svg'
data = json.loads(SRC.read_text())
W,H=840,880; PAD=20; TITLE=30; TILE_W=(W-PAD*2-16)/2; TILE_H=150; GAP=16; TOP=TITLE+PAD+4; CHART_TOP=TOP+3*TILE_H+2*GAP+GAP
BG='#0d1117'; BG2='#111722'; TILE='#161b22'; FRAME='#30363d'; MUTED='#7d8590'; INK='#e6edf3'; GREEN='#39d353'; BAR='#26a641'

def short(s):
    return dt.date.fromisoformat(s).strftime('%b %-d') if s else '—'
def span(s): return f"{short(s['start'])} – {short(s['end'])}" if s['length'] else '—'
cur,lng,best=data['current_streak'],data['longest_streak'],data['best_day']; n=len(data['days'])
tiles=[('current streak',cur['length'],' days',span(cur),GREEN),('longest streak',lng['length'],' days',span(lng),INK),('contributions',data['total_contributions'],'','in the last year',INK),('active days',data['active_days'],f' / {n}',f'{data["active_days"]/n:.0%} of the year' if n else '0% of the year',INK),('best day',best['count'],'',short(best['date']),INK),('avg / active day',data['avg_per_active_day'],'','contributions',INK)]
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"><style>.t{{opacity:0;animation:in .45s ease-out both}}@keyframes in{{0%{{opacity:0;transform:translateY(14px)}}100%{{opacity:1;transform:translateY(0)}}}}.b{{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .6s ease-out both}}@keyframes grow{{to{{transform:scaleY(1)}}}}@media (prefers-reduced-motion:reduce){{.t,.b{{opacity:1!important;transform:none!important;animation:none!important}}}}</style><defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs><rect width="100%" height="100%" rx="12" fill="url(#bg)"/><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/><line x1="0" y1="{TITLE}" x2="{W}" y2="{TITLE}" stroke="{FRAME}"/>']
for i,c in enumerate(['#ff5f56','#ffbd2e','#27c93f']): parts.append(f'<circle cx="{PAD+i*16}" cy="{TITLE/2}" r="5" fill="{c}"/>')
parts.append(f'<text x="{W/2}" y="{TITLE/2+4}" fill="{MUTED}" font-size="12" text-anchor="middle">{PROFILE["github_username"]}@github: ~$ ./stats.sh</text>')
for i,(label,value,suffix,caption,accent) in enumerate(tiles):
    col,row=i%2,i//2; x=PAD+col*(TILE_W+GAP); y=TOP+row*(TILE_H+GAP)
    parts += [f'<g class="t" style="animation-delay:{i*.15:.2f}s"><rect x="{x:.1f}" y="{y}" width="{TILE_W:.1f}" height="{TILE_H}" rx="10" fill="{TILE}" stroke="{FRAME}"/><text x="{x+24:.1f}" y="{y+40}" fill="{MUTED}" font-size="22">$ {label}</text>', f'<text x="{x+24:.1f}" y="{y+100}" fill="{accent}" font-size="54" font-weight="700">{value:,.1f}' if isinstance(value,float) else f'<text x="{x+24:.1f}" y="{y+100}" fill="{accent}" font-size="54" font-weight="700">{int(value):,}', f'<tspan font-size="24" font-weight="400" fill="{MUTED}">{suffix}</tspan></text>', f'<text x="{x+24:.1f}" y="{y+132}" fill="{MUTED}" font-size="20">{caption}</text></g>']
monthly=data['monthly']; chart_h=H-PAD-CHART_TOP; chart_x=PAD; chart_w=W-PAD*2
parts += [f'<rect x="{chart_x}" y="{CHART_TOP}" width="{chart_w}" height="{chart_h}" rx="10" fill="{TILE}" stroke="{FRAME}"/><text x="{chart_x+24}" y="{CHART_TOP+40}" fill="{MUTED}" font-size="22">$ contributions / month</text>']
plot_top=CHART_TOP+64; plot_bot=CHART_TOP+chart_h-40; plot_l=chart_x+24; plot_r=chart_x+chart_w-24; slot=(plot_r-plot_l)/max(len(monthly),1); bar_w=slot*.62; peak=max(1, max([m['total'] for m in monthly] or [0]))
for i,m in enumerate(monthly):
    h=max(2,(plot_bot-plot_top)*m['total']/peak); bx=plot_l+i*slot+(slot-bar_w)/2
    parts.append(f'<rect class="b" x="{bx:.1f}" y="{plot_bot-h:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="3" fill="{GREEN if m["total"]==peak else BAR}" style="animation-delay:{i*.06:.2f}s"/><text x="{bx+bar_w/2:.1f}" y="{plot_bot+28}" fill="{MUTED}" font-size="18" text-anchor="middle">{dt.date.fromisoformat(m["month"]+"-01").strftime("%b")[0]}</text>')
parts.append('</svg>'); OUT.write_text(''.join(parts)); print(f'wrote {OUT}')
