

# ####################################################################################### Works V
# import endaq
# import numpy as np
# import plotly.express as px
# import tempfile
# import os

# from plotting import create_result_plot


# # ============================================================
# # CONSTANTS
# # ============================================================
# ACCEL_40G = 80
# G_TO_M2S = 9.81

# axis_dict = {"X": 0, "Y": 1, "Z": 2}


# # ============================================================
# # PREVIEW SIGNAL (UNCHANGED)
# # ============================================================
# def preview_signal(ide_path, axis):

#     axis_number = axis_dict[axis]

#     doc = endaq.ide.get_doc(ide_path)

#     df = endaq.ide.to_pandas(
#         doc.channels[ACCEL_40G].subchannels[axis_number],
#         time_mode="seconds",
#     ) * G_TO_M2S

#     df = df.copy()
#     df.columns = ["acceleration"]

#     fig = px.line(
#         df,
#         x=df.index,
#         y="acceleration",
#         labels={
#             "index": "Time [s]",
#             "acceleration": "Acceleration [m/s²]"
#         },
#         title="Raw Acceleration Signal"
#     )

#     fig.update_layout(hovermode="x unified")

#     return fig


# # ============================================================
# # MAIN PROCESS FUNCTION (FINAL CLEAN VERSION)
# # ============================================================
# def process_signal(ide_path, axis, start_time, end_time):

#     axis_number = axis_dict[axis]

#     # --------------------------------------------------------
#     # SAFETY: convert UI inputs (from plot selection)
#     # --------------------------------------------------------
#     start_time = float(start_time)
#     end_time = float(end_time)

#     # ============================================================
#     # LOAD FULL IDE FILE (NO extract_time)
#     # ============================================================
#     doc = endaq.ide.get_doc(ide_path)

#     df_accel = endaq.ide.to_pandas(
#         doc.channels[ACCEL_40G].subchannels[axis_number],
#         time_mode="seconds",
#     )

#     if df_accel is None or len(df_accel) == 0:
#         raise ValueError("No acceleration data found in IDE file.")

#     # --------------------------------------------------------
#     # UNIT CONVERSION
#     # --------------------------------------------------------
#     df_accel = df_accel * G_TO_M2S
#     df_accel = df_accel.copy()
#     df_accel.columns = ["acceleration"]

#     # ============================================================
#     # IMPORTANT: UI-BASED SLICING (THIS FIXES YOUR WHOLE ISSUE)
#     # ------------------------------------------------------------
#     # start_time/end_time come from plot axis selection
#     # NOT from IDE global timestamps
#     # ============================================================
#     df_accel = df_accel.loc[
#         (df_accel.index >= start_time) &
#         (df_accel.index <= end_time)
#     ]

#     if len(df_accel) == 0:
#         raise ValueError(
#             "No data in selected time window. "
#             "Check your selection range on the preview plot."
#         )

#     # ============================================================
#     # INTEGRATION (SAME AS YOUR LOCAL SCRIPT)
#     # ============================================================
#     integrals = endaq.calc.integrate.integrals(
#         df_accel,
#         n=2,
#         highpass_cutoff=1.0,
#         tukey_percent=0.05
#     )

#     df_velocity = integrals[1].copy()
#     df_displacement = integrals[2].copy()

#     df_velocity.columns = ["velocity"]
#     df_displacement.columns = ["displacement"]

#     # --------------------------------------------------------
#     # UNIT CONVERSION
#     # --------------------------------------------------------
#     df_velocity *= 1e3
#     df_displacement *= 1e3

#     # ============================================================
#     # COMBINE DATA
#     # ============================================================
#     df = df_accel.join(df_velocity, how="left")
#     df = df.join(df_displacement, how="left")

#     # ============================================================
#     # PLOT (same structure as your working script)
#     # ============================================================
#     fig = create_result_plot(df)

#     return df, fig

# ############################################################################## TEST

import endaq
import numpy as np
import plotly.express as px
import streamlit as st

from plotting import create_result_plot


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
    ) * G_TO_M2S

    df = df.copy()
    df.columns = ["acceleration"]

    fig = px.line(
        df,
        x=df.index,
        y="acceleration",
        labels={
            "index": "Time [s]",
            "acceleration": "Acceleration [m/s²]"
        },
        title="Raw Acceleration Signal"
    )

    fig.update_layout(hovermode="x unified")

    return fig


# ============================================================
# MAIN PROCESS FUNCTION (CACHE-OPTIMIZED)
# ============================================================
@st.cache_data(show_spinner=False)
def process_signal(ide_path, axis, start_time, end_time):

    axis_number = axis_dict[axis]

    # --------------------------------------------------------
    # SAFETY CAST (from UI selection)
    # --------------------------------------------------------
    start_time = float(start_time)
    end_time = float(end_time)

    # ============================================================
    # LOAD IDE FILE (NO extract_time = stable)
    # ============================================================
    doc = endaq.ide.get_doc(ide_path)

    df_accel = endaq.ide.to_pandas(
        doc.channels[ACCEL_40G].subchannels[axis_number],
        time_mode="seconds",
    )

    if df_accel is None or len(df_accel) == 0:
        raise ValueError("No acceleration data found in IDE file.")

    # --------------------------------------------------------
    # UNIT CONVERSION
    # --------------------------------------------------------
    df_accel = df_accel * G_TO_M2S
    df_accel = df_accel.copy()
    df_accel.columns = ["acceleration"]

    # ============================================================
    # UI-BASED SLICING (THIS IS YOUR CORE FIX)
    # ------------------------------------------------------------
    # start/end come from Plotly preview selection
    # ============================================================
    df_accel = df_accel.loc[
        (df_accel.index >= start_time) &
        (df_accel.index <= end_time)
    ]

    if len(df_accel) == 0:
        raise ValueError(
            "No data in selected window. Adjust selection range."
        )

    # ============================================================
    # INTEGRATION (IDENTICAL TO YOUR LOCAL SCRIPT)
    # ============================================================
    integrals = endaq.calc.integrate.integrals(
        df_accel,
        n=2,
        highpass_cutoff=1.0,
        tukey_percent=0.05
    )

    df_velocity = integrals[1].copy()
    df_displacement = integrals[2].copy()

    df_velocity.columns = ["velocity"]
    df_displacement.columns = ["displacement"]

    # --------------------------------------------------------
    # UNIT CONVERSION
    # --------------------------------------------------------
    df_velocity *= 1e3
    df_displacement *= 1e3

    # ============================================================
    # FINAL COMBINATION
    # ============================================================
    df = df_accel.join(df_velocity, how="left")
    df = df.join(df_displacement, how="left")

    # ============================================================
    # PLOT
    # ============================================================
    fig = create_result_plot(df)

    return df, fig
