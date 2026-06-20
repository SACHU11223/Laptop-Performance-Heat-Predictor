"""HTML builders for prediction results."""


def _risk_label(risk_percent: float) -> tuple[str, str]:
    if risk_percent < 15:
        return "Low risk", "#23d18b"
    if risk_percent < 35:
        return "Moderate risk", "#f6c343"
    if risk_percent < 60:
        return "High risk", "#ff8a4c"
    return "Critical risk", "#ff5c7a"


def build_metric_cards(inputs: dict) -> str:
    items = [
        ("CPU", inputs.get("CPU Usage", "0%")),
        ("RAM", inputs.get("RAM Usage", "0%")),
        ("Disk", inputs.get("Disk I/O", "0%")),
        ("Apps", inputs.get("Running Apps", "0")),
        ("Crashes", inputs.get("Crashed Apps", "0")),
    ]
    cards = "".join(
        f"""
        <div class="mini-card">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
        """
        for label, value in items
    )
    return f'<div class="mini-grid">{cards}</div>'


def build_recommendations(recommendations: list[str], alerts: list[str]) -> str:
    alert_html = ""
    if alerts:
        alert_html = '<div class="alert-list"><h4>Active alerts</h4>' + "".join(
            f"<div>{alert}</div>" for alert in alerts
        ) + "</div>"

    rec_html = "".join(f"<li>{rec}</li>" for rec in recommendations)
    return f"""
    <div class="recommendation-card">
        {alert_html}
        <h4>Recommended actions</h4>
        <ul>{rec_html}</ul>
    </div>
    """


def build_input_summary(inputs: dict) -> str:
    rows = "".join(
        f"""
        <div class="summary-row">
            <span>{key}</span>
            <strong>{value}</strong>
        </div>
        """
        for key, value in inputs.items()
    )
    return f'<div class="summary-card"><h4>Analysis inputs</h4>{rows}</div>'


def build_full_result_html(prediction_result: dict) -> str:
    score = float(prediction_result.get("health_score", 0))
    status = prediction_result.get("health_status", "Unknown")
    risk_percent = float(prediction_result.get("risk_percent", 0))
    confidence = float(prediction_result.get("confidence", 0))
    color = prediction_result.get("color", "#23d18b")
    timestamp = prediction_result.get("timestamp", "")
    inputs = prediction_result.get("input_summary", {})
    recommendations = prediction_result.get("recommendations", [])
    alerts = prediction_result.get("alerts", [])
    risk_label, risk_color = _risk_label(risk_percent)

    return f"""
    <div class="result-shell">
        <div class="score-card">
            <div class="score-ring" style="--score:{score}; --score-color:{color};">
                <div>
                    <strong>{score:.1f}</strong>
                    <span>/ 100</span>
                </div>
            </div>
            <div class="score-copy">
                <span class="status-pill" style="border-color:{color}; color:{color};">{status}</span>
                <h3>AI health analysis complete</h3>
                <p>Analyzed at {timestamp}</p>
            </div>
        </div>

        <div class="meter-card">
            <div class="meter-head">
                <span>Failure risk</span>
                <strong style="color:{risk_color};">{risk_percent:.1f}% - {risk_label}</strong>
            </div>
            <div class="meter-track"><span style="width:{risk_percent:.1f}%; background:{risk_color};"></span></div>
            <div class="meter-head confidence">
                <span>Model confidence</span>
                <strong>{confidence:.1f}%</strong>
            </div>
            <div class="meter-track"><span style="width:{confidence:.1f}%;"></span></div>
        </div>

        {build_metric_cards(inputs)}
        {build_recommendations(recommendations, alerts)}
        {build_input_summary(inputs)}
    </div>
    """
