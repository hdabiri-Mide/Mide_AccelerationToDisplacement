# # ####################################################################################### Works V
import endaq
import numpy as np
import streamlit as st

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# CONSTANTS
# ============================================================
ACCEL_40G = 80
G_TO_M2S = 9.81

axis_dict = {"X": 0, "Y": 1, "Z": 2}


# ============================================================
# PREVIEW SIGNAL
# ============================================================
def preview_signal(ide_path, axis):

    axis_number = axis_dict[axis]

    doc = endaq.ide.get_doc(ide_path)

    df = endaq.ide.to_pandas(
        doc.channels[ACCEL_40G].subchannels[axis_number],
        time_mode="seconds",
    )

    df = df * G_TO_M2S
    df = df.copy()
    df.columns = ["acceleration"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["acceleration"]))

    fig.update_layout(
        title="Raw Acceleration Signal",
        xaxis_title="Time [s]",
        yaxis_title="Acceleration [m/s²]",
        hovermode="x unified"
    )

    return fig


# ============================================================
# PROCESS SIGNAL
# ============================================================
@st.cache_data(show_spinner=False)
# def process_signal(ide_path, axis, start_time, end_time):
def process_signal(
    ide_path,
    axis,
    start_time,
    end_time,
    highpass_cutoff=1.0,
    tukey_percent=0.05,
):

    axis_number = axis_dict[axis]

    doc = endaq.ide.get_doc(ide_path)

    df_accel = endaq.ide.to_pandas(
        doc.channels[ACCEL_40G].subchannels[axis_number],
        time_mode="seconds",
    )

    if df_accel is None or len(df_accel) == 0:
        raise ValueError("No acceleration data found.")

    # unit conversion
    df_accel = df_accel * G_TO_M2S
    df_accel = df_accel.copy()
    df_accel.columns = ["acceleration"]

    # time filter
    df_accel = df_accel.loc[
        (df_accel.index >= float(start_time)) &
        (df_accel.index <= float(end_time))
    ]

    if len(df_accel) == 0:
        raise ValueError("No data in selected time range.")

    # integration
    # integrals = endaq.calc.integrate.integrals(
    #     df_accel,
    #     n=2,
    #     highpass_cutoff=1.0,
    #     tukey_percent=0.05
    # )
    integrals = endaq.calc.integrate.integrals(
        df_accel,
        n=2,
        highpass_cutoff=highpass_cutoff,
        tukey_percent=tukey_percent,
    )

    df_velocity = integrals[1].copy()
    df_displacement = integrals[2].copy()

    df_velocity.columns = ["velocity"]
    df_displacement.columns = ["displacement"]

    # scaling
    df_velocity *= 1e3
    df_displacement *= 1e3

    df = df_accel.join(df_velocity)
    df = df.join(df_displacement)

    return df


# ============================================================
# PLOT: 3 SUBPLOTS (FINAL OUTPUT)
# ============================================================
def create_result_plot(df):

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=[
            "Acceleration (m/s²)",
            "Velocity (mm/s)",
            "Displacement (mm)"
        ]
    )

    fig.add_trace(go.Scatter(x=df.index, y=df["acceleration"]), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["velocity"]), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["displacement"]), row=3, col=1)

    fig.update_layout(
        height=800,
        hovermode="x unified",
        showlegend=False,
        # title="Acceleration / Velocity / Displacement"
    )

    fig.update_xaxes(title_text="Time [s]", row=3, col=1)

    return fig

################################################################################### TEST

