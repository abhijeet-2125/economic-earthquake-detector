import plotly.graph_objects as go


def create_eei_chart(df, crisis_df=None):
    # Smooth signal
    df["eei_smooth"] = (df["economic_earthquake_index"].rolling(14, min_periods=1).mean())
    fig = go.Figure()

    # Main EEI Line
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["eei_smooth"],
            mode="lines",
            name="EEI",
            line=dict(
                width=4,
                color="#6C7BFF"
            ),
            hovertemplate=
            "<b>Date:</b> %{x}<br>"
            "<b>EEI:</b> %{y:.2f}<extra></extra>"))

    # Risk Zones
    fig.add_hrect(
        y0=1,
        y1=2,
        fillcolor="#22C55E",
        opacity=0.10,
        line_width=0,
        annotation_text="ELEVATED",
        annotation_position="top left"
    )

    fig.add_hrect(
        y0=2,
        y1=3,
        fillcolor="#FACC15",
        opacity=0.12,
        line_width=0,
        annotation_text="HIGH",
        annotation_position="top left"
    )

    fig.add_hrect(
        y0=3,
        y1=10,
        fillcolor="#EF4444",
        opacity=0.15,
        line_width=0,
        annotation_text="CRISIS",
        annotation_position="top left"
    )

    # Crisis Markers
    if crisis_df is not None and len(crisis_df) > 0:
        fig.add_trace(
            go.Scatter(
                x=crisis_df["date"],
                y=crisis_df["economic_earthquake_index"],
                mode="markers",
                name="Crisis Events",
                marker=dict(
                    size=10,
                    color="red"
                ),
                hovertemplate=
                "<b>Crisis Event</b><br>"
                "Date: %{x}<br>"
                "EEI: %{y:.2f}<extra></extra>"
            )
        )

        # Major Event Labels
        important_events = {
            "2020-03-12": "COVID Crash",
            "2020-03-16": "Pandemic Panic",
            "2020-04-20": "Oil Crash",
            "2022-06-13": "Inflation Shock",
            "2021-11-26": "Omicron Fear",
            "2019-08-14": "China Slowdown",
            "2018-02-05": "Volatility Crash",
            "2020-02-24": "COVID Selloff"
        }

        for event_date, label in important_events.items():
            event_row = crisis_df[
                crisis_df["date"] == event_date
            ]
            if not event_row.empty:
                fig.add_annotation(
                    x=event_date,
                    y=float(
                        event_row[
                            "economic_earthquake_index"
                        ].iloc[0]
                    ),
                    text=label,
                    showarrow=True,
                    arrowhead=2,
                    arrowwidth=1,
                    arrowsize=1,
                    ax=0,
                    ay=-40,
                    font=dict(
                        size=11,
                        color="white"
                    )
                )

    fig.update_layout(
        title=dict(
            text="Economic Earthquake Index Timeline",
            x=0.02
        ),
        template="plotly_dark",
        height=700,
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(
            color="white"
        ),
        xaxis=dict(
            showgrid=False,
            title=""
        ),
        yaxis=dict(
            title="EEI",
            gridcolor="rgba(255,255,255,0.08)",
            range=[-1.5, 4]
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )
    return fig


def create_risk_gauge(eei):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=max(0, eei),
            title={
                "text": "Current Risk"
            },
            gauge={
                "axis": {
                    "range": [0, 8]
                },
                "steps": [
                    {"range": [0, 1], "color": "#22C55E"},
                    {"range": [1, 2], "color": "#FACC15"},
                    {"range": [2, 3], "color": "#FB923C"},
                    {"range": [3, 8], "color": "#EF4444"},
                ],
                "bar": {
                    "color": "white"
                }
            }
        )
    )
    fig.update_layout(
        height=350,
        paper_bgcolor="#0B1220",
        font={"color": "white"}
    )
    return fig