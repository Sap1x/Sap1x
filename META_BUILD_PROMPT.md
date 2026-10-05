# Senior Software Engineer / Meta-Style Build Prompt

You are a senior software engineer designing a production-quality GitHub profile README system for **Saptarshi Mondal**. Start from the supplied animated terminal-style GitHub profile project, but replace every identity-specific, visual, textual, and configuration-specific element with Saptarshi's resume-backed information. Do not retain the original author's name, username, shell prompt, social links, portrait filename, alt text, comments, default variables, output names, or stale contribution data.

## Source of truth
Use the attached Saptarshi Mondal resume as the authoritative source for personal, education, experience, project, technology, publication, and achievement claims. Use the supplied portrait as the source image. The GitHub username is `Sap1x`, confirmed by the resume's GitHub link. Preserve resume terminology and metrics exactly; never invent achievements, employers, performance numbers, repositories, certifications, or social accounts.

## Product goal
Build a polished GitHub profile README that feels like a single continuous terminal session:
- `saptarshi@github ~ $ ./contributions.sh` → animated real contribution heatmap.
- `saptarshi@github ~ $ whoami` → Saptarshi's supplied portrait rendered as animated monochrome ASCII.
- `saptarshi@github ~ $ ./stats.sh` → animated streak/statistics card.
- `saptarshi@github ~ $ ./links.sh` → resume-backed social/profile links.
- Follow with resume-backed education, skills, IIT Kharagpur research internship, CodeRL++, UrbanFlow OPS, publications, achievements, and current focus.

## Identity configuration
Centralize all identity-specific values in `config/profile.json`:
- Saptarshi Mondal
- Sap1x
- `saptarshi@github`
- Kolkata, India
- AI/ML Engineer · Software Systems Builder · Researcher
- resume-backed email, links, education, experience, projects, skills, publications, achievements

Scripts must load configuration instead of scattering identity strings throughout the codebase.

## Visual engineering
- Preserve the dark terminal aesthetic and macOS-style title bars.
- Use SVG + SMIL/CSS; do not rely on JavaScript because GitHub README content does not execute arbitrary scripts.
- Keep portrait/stats canvases aligned.
- Add `prefers-reduced-motion` support.
- Keep alt text Saptarshi-specific.
- Keep README runtime dependency-free.

## Contribution architecture
Implement:
`GitHub public contribution HTML → BeautifulSoup parser → data/contributions.json → heatmap SVG + stats SVG → README`

The Action must run daily, support manual dispatch, run on pushes to `main`, use least-privilege `contents: write`, install pinned dependencies, fetch `Sap1x`, regenerate generated assets, and commit only those generated artifacts. Use `[skip ci]` to prevent loops. Fail loudly if GitHub's calendar markup changes.

## Photo pipeline
Use `assets/saptarshi-source.jpg`. Preprocess the supplied white-background photo by isolating the subject, smoothing background noise, retaining facial/eyeglass/hair edges, normalizing grayscale contrast, and square-cropping to `assets/saptarshi-prepped.png`. Convert that to `saptarshi-ascii.svg` using a configurable density ramp and resolution.

## Resume-backed facts
### CodeRL++
OpenEnv-compliant RL environment; cross-episode memory; composite rewards; recall **+138%**; critical bug detection **+188%**; false positives **-57%**; **3K+ GRPO steps**; FastAPI + Redis + Docker; approximately **1.2s** inference; Python, FastAPI, PyTorch, Hugging Face, GRPO, Unsloth, Docker, Redis, Qwen2.5, Llama 3; GitHub `https://github.com/Sap1x/CodeRL-`.

### UrbanFlow OPS
**90K+** Bengaluru traffic records; XGBoost, Random Forest, SHAP; event-driven FastAPI/WebSockets microservices; Digital Twin; SciPy/NetworkX; **1000+** simultaneous incidents; **sub-100ms** ML inference; **94.3%** simulated cost savings; Flipkart GRiD 2.0 Semi-Finalist; GitHub `https://github.com/Sap1x/UrbanFlow-AI`.

### IIT Kharagpur Research Internship
Event-driven Edge–Cloud IoDT architecture; EventBus/Observer Pattern; IoT sensors, UAV missions, edge inference, cloud analytics, Digital Twin synchronization; LoRaWAN, MQTT, Wi-Fi, 5G, FANET; **100% field coverage**; **32.54 ms** average end-to-end latency; **97%** mission reliability.

## Engineering quality bar
Validate inputs; use `pathlib`; make scripts idempotent; fail explicitly rather than hiding stale data; pin dependencies; separate configuration from generated assets; keep local setup reproducible; use concise CI logs; avoid secrets; preserve resume facts exactly.

## Deliverables
```text
Saptarshi-Mondal-GitHub-Profile/
├── README.md
├── META_BUILD_PROMPT.md
├── SETUP.md
├── config/profile.json
├── assets/saptarshi-source.jpg
├── assets/saptarshi-prepped.png
├── data/contributions.json
├── scripts/fetch_contributions.py
├── scripts/prep_photo.py
├── scripts/make_ascii_svg.py
├── scripts/render_heatmap_svg.py
├── scripts/render_stats_svg.py
├── scripts/requirements.txt
├── .github/workflows/update-profile-art.yml
├── saptarshi-ascii.svg
├── contrib-heatmap.svg
└── stats.svg
```

Before finalizing, verify that no stale template references remain. Only Saptarshi Mondal / Sap1x and resume-backed facts should remain.
