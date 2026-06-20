"""Gradio theme and glassmorphic CSS."""

import gradio as gr


def get_theme():
    return gr.themes.Soft(
        primary_hue="cyan",
        secondary_hue="emerald",
        neutral_hue="slate",
        font=["Inter", "Segoe UI", "sans-serif"],
        font_mono=["JetBrains Mono", "Consolas", "monospace"],
    )


def get_css() -> str:
    return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
    --bg: #090b10;
    --panel: rgba(255, 255, 255, 0.075);
    --panel-strong: rgba(255, 255, 255, 0.12);
    --stroke: rgba(255, 255, 255, 0.16);
    --stroke-hot: rgba(74, 222, 128, 0.42);
    --text: #f8fafc;
    --muted: rgba(248, 250, 252, 0.66);
    --faint: rgba(248, 250, 252, 0.42);
    --cyan: #22d3ee;
    --green: #4ade80;
    --yellow: #facc15;
    --red: #fb7185;
    --shadow: 0 24px 80px rgba(0, 0, 0, 0.42);
}

* { box-sizing: border-box; }

body,
.gradio-container {
    min-height: 100vh;
    color: var(--text) !important;
    font-family: Inter, Segoe UI, sans-serif !important;
    background:
        linear-gradient(120deg, rgba(34, 211, 238, 0.16), transparent 34%),
        linear-gradient(250deg, rgba(74, 222, 128, 0.12), transparent 38%),
        linear-gradient(180deg, #111827 0%, #090b10 54%, #050609 100%) !important;
}

.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 18px !important;
}

footer, #footer { display: none !important; }

.hero-shell {
    position: relative;
    padding: 48px 20px 26px;
    text-align: center;
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 9px 16px;
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 999px;
    background: rgba(34, 211, 238, 0.08);
    color: #b7f7ff;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 0 6px rgba(74, 222, 128, 0.14);
}

.hero-shell h1 {
    margin: 18px auto 12px;
    font-size: clamp(2.2rem, 5vw, 4.2rem);
    line-height: 1;
    font-weight: 900;
    color: var(--text);
}

.hero-shell p {
    max-width: 760px;
    margin: 0 auto;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.7;
}

.hero-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(120px, 1fr));
    gap: 12px;
    max-width: 820px;
    margin: 28px auto 0;
}

.hero-stats div,
.glass-panel,
.result-shell,
.plot-container,
.gradio-plot,
.gr-markdown,
.file-preview {
    background: var(--panel) !important;
    border: 1px solid var(--stroke) !important;
    box-shadow: var(--shadow);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
}

.hero-stats div {
    border-radius: 8px;
    padding: 16px 14px;
}

.hero-stats strong {
    display: block;
    font-size: 22px;
    font-weight: 900;
    color: var(--text);
}

.hero-stats span {
    display: block;
    margin-top: 4px;
    color: var(--faint);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.section-title {
    display: flex;
    gap: 12px;
    align-items: center;
    margin: 22px 0 12px;
}

.section-title > span {
    display: grid;
    place-items: center;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.22), rgba(74, 222, 128, 0.14));
    border: 1px solid rgba(255, 255, 255, 0.14);
    font-weight: 900;
}

.section-title h2 {
    margin: 0;
    font-size: 16px;
    line-height: 1.2;
}

.section-title p {
    margin: 3px 0 0;
    color: var(--faint);
    font-size: 12px;
}

.glass-panel {
    border-radius: 8px !important;
    padding: 16px !important;
}

.glass-panel:hover,
.result-shell:hover {
    border-color: var(--stroke-hot) !important;
}

label, .wrap label {
    color: var(--muted) !important;
    font-weight: 700 !important;
}

input, textarea, select,
.gr-text-input, .gr-number-input,
.gr-dropdown, .gr-form {
    color: var(--text) !important;
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
}

input[type="range"] { accent-color: var(--cyan); }

.predict-btn {
    width: 100% !important;
    border: 0 !important;
    border-radius: 8px !important;
    min-height: 52px !important;
    font-weight: 900 !important;
    letter-spacing: 0.03em !important;
    color: #041014 !important;
    background: linear-gradient(135deg, #67e8f9, #86efac) !important;
    box-shadow: 0 18px 42px rgba(34, 211, 238, 0.22) !important;
}

.reset-btn {
    width: 100% !important;
    border-radius: 8px !important;
    min-height: 52px !important;
    font-weight: 800 !important;
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid var(--stroke) !important;
    color: var(--text) !important;
}

.predict-btn:hover,
.reset-btn:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

.empty-state {
    min-height: 360px;
    display: grid;
    place-items: center;
    text-align: center;
    padding: 30px;
    color: var(--muted);
}

.empty-icon {
    display: grid;
    place-items: center;
    width: 86px;
    height: 86px;
    margin: 0 auto 18px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.24), rgba(74, 222, 128, 0.18));
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #cffafe;
    font-weight: 900;
    font-family: JetBrains Mono, monospace;
}

.empty-state h3 { margin: 0 0 8px; color: var(--text); }
.empty-state p { max-width: 360px; margin: 0; line-height: 1.6; }

.result-shell {
    border-radius: 8px;
    padding: 18px;
}

.score-card {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 18px;
    align-items: center;
}

.score-ring {
    --score: 0;
    --score-color: var(--green);
    width: 190px;
    aspect-ratio: 1;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background:
        radial-gradient(circle at center, rgba(9, 11, 16, 0.92) 0 58%, transparent 59%),
        conic-gradient(var(--score-color) calc(var(--score) * 1%), rgba(255,255,255,0.09) 0);
}

.score-ring div {
    text-align: center;
}

.score-ring strong {
    display: block;
    font-size: 46px;
    line-height: 1;
    font-weight: 900;
    color: var(--text);
}

.score-ring span,
.score-copy p,
.meter-head span {
    color: var(--faint);
}

.score-copy h3 {
    margin: 12px 0 6px;
    font-size: 22px;
}

.status-pill {
    display: inline-flex;
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 12px;
}

.meter-card,
.recommendation-card,
.summary-card {
    margin-top: 14px;
    padding: 16px;
    border-radius: 8px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
}

.meter-head,
.summary-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: center;
}

.meter-head strong,
.summary-row strong {
    font-family: JetBrains Mono, Consolas, monospace;
}

.meter-head.confidence { margin-top: 14px; }

.meter-track {
    height: 10px;
    overflow: hidden;
    margin-top: 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
}

.meter-track span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--cyan), var(--green));
}

.mini-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(80px, 1fr));
    gap: 10px;
    margin-top: 14px;
}

.mini-card {
    padding: 14px 10px;
    border-radius: 8px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.11);
    text-align: center;
}

.mini-card span {
    display: block;
    color: var(--faint);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.mini-card strong {
    display: block;
    margin-top: 6px;
    color: var(--text);
    font-size: 18px;
}

.recommendation-card h4,
.summary-card h4 {
    margin: 0 0 10px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #b7f7ff;
}

.recommendation-card ul {
    margin: 0;
    padding-left: 18px;
    color: var(--muted);
    line-height: 1.8;
}

.alert-list {
    margin-bottom: 14px;
}

.alert-list div {
    margin-top: 8px;
    padding: 10px 12px;
    border-radius: 8px;
    color: #fecdd3;
    background: rgba(251, 113, 133, 0.11);
    border: 1px solid rgba(251, 113, 133, 0.2);
}

.summary-row {
    padding: 10px 0;
    border-top: 1px solid rgba(255,255,255,0.08);
}

.summary-row span { color: var(--faint); }

.notice {
    display: grid;
    gap: 3px;
    padding: 13px 15px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.08);
}

.notice span { color: var(--muted); }
.notice-success { border-color: rgba(74,222,128,0.35); }
.notice-info { border-color: rgba(34,211,238,0.35); }
.notice-warning { border-color: rgba(250,204,21,0.35); }
.notice-error, .notice-critical { border-color: rgba(251,113,133,0.38); }

.app-footer {
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    padding: 28px 12px;
    color: var(--faint);
    font-size: 13px;
}

.js-plotly-plot .plotly .modebar {
    background: rgba(9,11,16,0.62) !important;
    border-radius: 8px !important;
}

@media (max-width: 900px) {
    .hero-stats { grid-template-columns: repeat(2, 1fr); }
    .score-card { grid-template-columns: 1fr; justify-items: center; text-align: center; }
    .mini-grid { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
}

@media (max-width: 520px) {
    .gradio-container { padding: 10px !important; }
    .hero-shell { padding-top: 30px; }
    .hero-stats { grid-template-columns: 1fr; }
    .mini-grid { grid-template-columns: 1fr; }
    .score-ring { width: 168px; }
}
"""
