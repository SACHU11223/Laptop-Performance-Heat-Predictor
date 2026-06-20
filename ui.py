"""Main Gradio UI for the laptop health prediction app."""

import gradio as gr
import plotly.graph_objects as go

from charts import build_all_charts
from components import (
    build_advanced_inputs,
    build_basic_inputs,
    build_clear_button,
    build_hardware_selectors,
    build_history_output,
    build_notification_bar,
    build_predict_button,
    build_report_download,
    build_result_html_output,
    render_footer,
    render_hero,
    render_notification,
    section_header,
)
from prediction import predict_health
from styles import build_full_result_html
from theme import get_css, get_theme
from utils import add_to_history, build_notification, get_history_display, save_report_to_file, validate_inputs


def _file_update(value=None, visible=False):
    return gr.update(value=value, visible=visible)


def _empty_chart(title: str = "Awaiting analysis") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=title,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color="rgba(248,250,252,0.42)"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20),
        height=260,
    )
    return fig


def _error_card(title: str, message: str) -> str:
    return f"""
    <div class="notice notice-error">
        <strong>{title}</strong>
        <span style="white-space:pre-wrap;">{message}</span>
    </div>
    """


def make_prediction(
    device_age: float,
    cores: int,
    cpu: float,
    ram: float,
    disk: float,
    running_apps: int,
    crashed_apps: int,
    device_model: str,
    processor: str,
    graphics: str,
):
    valid, error_message = validate_inputs(device_age, cores, cpu, ram, disk, running_apps, crashed_apps)
    if not valid:
        return (
            _error_card("Validation error", error_message),
            _empty_chart("Fix inputs to continue"),
            _empty_chart("Fix inputs to continue"),
            _empty_chart("Fix inputs to continue"),
            _empty_chart("Fix inputs to continue"),
            _empty_chart("Fix inputs to continue"),
            _empty_chart("Fix inputs to continue"),
            get_history_display(),
            render_notification("error", "Validation failed", error_message.replace("\n", " ")),
            _file_update(),
        )

    prediction_result = predict_health(
        device_age=device_age,
        cores=cores,
        cpu_utilization=cpu,
        memory_utilization=ram,
        disk_io_utilization=disk,
        running_apps=running_apps,
        crashed_apps=crashed_apps,
        device_model=device_model,
        processor=processor,
        graphics=graphics,
    )

    if prediction_result.get("error"):
        message = prediction_result["error"]
        return (
            _error_card("Prediction error", message),
            _empty_chart("Prediction failed"),
            _empty_chart("Prediction failed"),
            _empty_chart("Prediction failed"),
            _empty_chart("Prediction failed"),
            _empty_chart("Prediction failed"),
            _empty_chart("Prediction failed"),
            get_history_display(),
            render_notification("critical", "Model error", message),
            _file_update(),
        )

    history = add_to_history(prediction_result)
    charts = build_all_charts(cpu, ram, disk, device_age, running_apps, prediction_result.get("health_score", 0), history)
    report_path = save_report_to_file(prediction_result)
    notification = build_notification(prediction_result)

    return (
        build_full_result_html(prediction_result),
        *charts,
        get_history_display(),
        render_notification(notification["type"], notification["title"], notification["message"]),
        _file_update(value=report_path, visible=bool(report_path)),
    )


def clear_form():
    return (
        2.0,
        4,
        45,
        60,
        40,
        8,
        0,
        "Other",
        "Other",
        "Other",
        build_result_html_output().value,
        _empty_chart(),
        _empty_chart(),
        _empty_chart(),
        _empty_chart(),
        _empty_chart(),
        _empty_chart(),
        get_history_display(),
        "",
        _file_update(),
    )


def create_ui() -> gr.Blocks:
    with gr.Blocks(title="Laptop Health Prediction") as demo:
        render_hero()

        with gr.Row(equal_height=False):
            with gr.Column(scale=5, min_width=360):
                section_header("01", "System Inputs", "Core live metrics for model inference.")
                cpu, ram, disk = build_basic_inputs()

                section_header("02", "Advanced Metrics", "Hardware age and process stability.")
                device_age, cores, running_apps, crashed_apps = build_advanced_inputs()

                section_header("03", "Hardware Profile", "Encoded categorical features used by the model.")
                device_model, processor, graphics = build_hardware_selectors()

                with gr.Row():
                    with gr.Column(scale=7):
                        predict_btn = build_predict_button()
                    with gr.Column(scale=5):
                        clear_btn = build_clear_button()

                notification_bar = build_notification_bar()
                report_file = build_report_download()

            with gr.Column(scale=7, min_width=460):
                result_html = build_result_html_output()

                with gr.Row():
                    chart_gauge = gr.Plot(label="Health Gauge", value=_empty_chart())
                    chart_donut = gr.Plot(label="Risk Breakdown", value=_empty_chart())

                chart_area = gr.Plot(label="Resource Utilization", value=_empty_chart())

                with gr.Row():
                    chart_bar = gr.Plot(label="Metric Risk", value=_empty_chart())
                    chart_radar = gr.Plot(label="System Profile", value=_empty_chart())

                chart_timeline = gr.Plot(label="Health Timeline", value=_empty_chart())
                history_md = build_history_output()

        render_footer()

        predict_btn.click(
            fn=make_prediction,
            inputs=[
                device_age,
                cores,
                cpu,
                ram,
                disk,
                running_apps,
                crashed_apps,
                device_model,
                processor,
                graphics,
            ],
            outputs=[
                result_html,
                chart_gauge,
                chart_area,
                chart_bar,
                chart_donut,
                chart_radar,
                chart_timeline,
                history_md,
                notification_bar,
                report_file,
            ],
        )

        clear_btn.click(
            fn=clear_form,
            inputs=[],
            outputs=[
                device_age,
                cores,
                cpu,
                ram,
                disk,
                running_apps,
                crashed_apps,
                device_model,
                processor,
                graphics,
                result_html,
                chart_gauge,
                chart_area,
                chart_bar,
                chart_donut,
                chart_radar,
                chart_timeline,
                history_md,
                notification_bar,
                report_file,
            ],
        )

    return demo


if __name__ == "__main__":
    create_ui().launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        theme=get_theme(),
        css=get_css(),
    )
