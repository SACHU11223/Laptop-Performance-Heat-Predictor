"""Reusable Gradio components for the laptop health dashboard."""

import gradio as gr

from prediction import DEVICE_MODEL_MAP, GRAPHICS_MAP, PROCESSOR_MAP


def render_hero() -> gr.HTML:
    return gr.HTML(
        """
        <section class="hero-shell">
            <div class="hero-kicker">
                <span class="live-dot"></span>
                AI laptop diagnostics
            </div>
            <h1>Laptop Health Prediction</h1>
            <p>
                Enter real system metrics, run the trained Random Forest model,
                and get a clean health score with risks, charts, and maintenance actions.
            </p>
            <div class="hero-stats">
                <div><strong>Accuracy</strong><span>94.4%</span></div>
                <div><strong>10</strong><span>input features</span></div>
                <div><strong>Predicted</strong><span>health score</span></div>
                <div><strong>live</strong><span>report export</span></div>
            </div>
        </section>
        """
    )


def section_header(icon: str, title: str, subtitle: str = "") -> gr.HTML:
    return gr.HTML(
        f"""
        <div class="section-title">
            <span>{icon}</span>
            <div>
                <h2>{title}</h2>
                <p>{subtitle}</p>
            </div>
        </div>
        """
    )


def build_basic_inputs():
    with gr.Column(elem_classes=["glass-panel", "input-panel"]):
        cpu = gr.Slider(0, 100, value=45, step=1, label="CPU utilization (%)", info="Current processor load")
        ram = gr.Slider(0, 100, value=60, step=1, label="Memory utilization (%)", info="Current RAM pressure")
        disk = gr.Slider(0, 100, value=40, step=1, label="Disk I/O utilization (%)", info="Read/write load")
    return cpu, ram, disk


def build_advanced_inputs():
    with gr.Column(elem_classes=["glass-panel", "input-panel"]):
        device_age = gr.Slider(0, 15, value=2, step=0.5, label="Device age (years)", info="Laptop age")
        cores = gr.Slider(1, 32, value=4, step=1, label="CPU cores", info="Logical cores")
        running_apps = gr.Slider(0, 80, value=8, step=1, label="Running applications", info="Active apps/process groups")
        crashed_apps = gr.Slider(0, 20, value=0, step=1, label="Crashed applications", info="Crashes in last 24 hours")
    return device_age, cores, running_apps, crashed_apps


def build_hardware_selectors():
    with gr.Column(elem_classes=["glass-panel", "input-panel"]):
        device_model = gr.Dropdown(
            choices=list(DEVICE_MODEL_MAP.keys()),
            value="Other",
            label="Device model",
            info="Laptop family",
            interactive=True,
        )
        processor = gr.Dropdown(
            choices=list(PROCESSOR_MAP.keys()),
            value="Other",
            label="Processor",
            info="CPU family",
            interactive=True,
        )
        graphics = gr.Dropdown(
            choices=list(GRAPHICS_MAP.keys()),
            value="Other",
            label="Graphics",
            info="GPU family",
            interactive=True,
        )
    return device_model, processor, graphics


def build_predict_button() -> gr.Button:
    return gr.Button("Analyze Health", variant="primary", size="lg", elem_classes=["predict-btn"])


def build_clear_button() -> gr.Button:
    return gr.Button("Reset", variant="secondary", size="lg", elem_classes=["reset-btn"])


def build_result_html_output() -> gr.HTML:
    return gr.HTML(
        """
        <div class="empty-state">
            <div class="empty-icon">AI</div>
            <h3>Ready for analysis</h3>
            <p>Set your laptop metrics and run the model to generate the full health dashboard.</p>
        </div>
        """
    )


def build_history_output() -> gr.Markdown:
    return gr.Markdown(value="No predictions yet. Run your first analysis.", label="Prediction history")


def build_report_download() -> gr.File:
    return gr.File(label="Download health report", interactive=False, visible=False)


def build_notification_bar() -> gr.HTML:
    return gr.HTML(value="", visible=True)


def render_notification(ntype: str, title: str, message: str) -> str:
    return f"""
    <div class="notice notice-{ntype}">
        <strong>{title}</strong>
        <span>{message}</span>
    </div>
    """


def render_footer() -> gr.HTML:
    return gr.HTML(
        """
        <footer class="app-footer">
            <span>LaptopHealthPrediction</span>
            <span>Python + Gradio + scikit-learn + Plotly</span>
        </footer>
        """
    )


def render_about_tab() -> gr.HTML:
    return gr.HTML("")


def render_global_injections() -> list:
    return []
