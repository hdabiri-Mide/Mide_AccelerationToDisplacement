# import os
# import tempfile

# import endaq
# import plotly.express as px

# from plotting import create_result_plot


# ############################################################
# # USER CONSTANTS
# ############################################################

# ACCEL_40G = 80

# X = 0
# Y = 1
# Z = 2

# G_TO_M2S = 9.81


# ############################################################
# # PREVIEW SIGNAL
# ############################################################

# def preview_signal(
#         ide_path,
#         axis
# ):

#     axis_dict = {
#         "X": X,
#         "Y": Y,
#         "Z": Z
#     }

#     axis_number = axis_dict[axis]

#     ########################################################

#     doc_full = endaq.ide.get_doc(ide_path)

#     df_preview = endaq.ide.to_pandas(
#         doc_full.channels[ACCEL_40G].subchannels[axis_number],
#         time_mode="seconds"
#     ) * G_TO_M2S

#     df_preview.columns = ["acceleration"]

#     fig_preview = px.line(
#         df_preview,
#         x=df_preview.index,
#         y="acceleration",
#         labels={
#             "index": "Time [s]",
#             "acceleration": "Acceleration [m/s²]"
#         },
#         title="Raw Acceleration Signal"
#     )

#     fig_preview.update_layout(
#         hovermode="x unified"
#     )

#     return fig_preview


# ############################################################
# # PROCESS SIGNAL
# ############################################################

# def process_signal(
#         ide_path,
#         axis,
#         start_time,
#         end_time
# ):

#     axis_dict = {
#         "X": X,
#         "Y": Y,
#         "Z": Z
#     }

#     axis_number = axis_dict[axis]

#     ########################################################
#     # CREATE TEMP EXTRACTED IDE
#     ########################################################

#     temp_folder = tempfile.gettempdir()

#     extracted_ide_path = os.path.join(
#         temp_folder,
#         "Extracted.ide"
#     )

#     ########################################################
#     # EXTRACT TIME RANGE
#     ########################################################

#     # endaq.ide.extract_time(

#     #     ide_path,

#     #     extracted_ide_path,

#     #     start=str(start_time),

#     #     end=str(end_time)

#     # )

#     df_accel = df_accel[
#             (df_accel.index >= start_time) &
#             (df_accel.index <= end_time)
#     ]

#     ########################################################
#     # LOAD ACCELERATION
#     ########################################################

#     # doc = endaq.ide.get_doc(
#     #     extracted_ide_path
#     # )
#     doc = endaq.ide.get_doc(ide_path)

#     df_accel = endaq.ide.to_pandas(

#         doc.channels[ACCEL_40G].subchannels[axis_number],

#         time_mode="seconds"

#     ) * G_TO_M2S

#     df_accel = df_accel.copy()
#     df_accel.columns = ['acceleration']

#     # ⭐ NORMALIZE TIME (IMPORTANT FIX)
#     df_accel.index = df_accel.index - df_accel.index.min()

#     df_accel = df_accel[
#             (df_accel.index >= start_time) &
#             (df_accel.index <= end_time)
#     ]

#     ########################################################
#     # CALCULATE VELOCITY / DISPLACEMENT
#     ########################################################

#     integrals = endaq.calc.integrate.integrals(

#         df_accel,

#         n=2,

#         highpass_cutoff=1.0,

#         tukey_percent=0.05

#     )

#     df_velocity = integrals[1]

#     df_displacement = integrals[2]

#     ########################################################
#     # RENAME
#     ########################################################

#     df_accel.columns = ["acceleration"]

#     df_velocity.columns = ["velocity"]

#     df_displacement.columns = ["displacement"]

#     ########################################################
#     # CONVERT UNITS
#     ########################################################

#     df_velocity = df_velocity * 1000

#     df_displacement = df_displacement * 1000

#     ########################################################
#     # JOIN
#     ########################################################

#     df = df_accel.join(
#         df_velocity,
#         how="left"
#     )

#     df = df.join(
#         df_displacement,
#         how="left"
#     )

#     ########################################################
#     # FIGURE
#     ########################################################

#     fig = create_result_plot(df)

#     ########################################################
import endaq
import numpy as np
from plotting import create_result_plot


# ============================================================
# MAIN PROCESS FUNCTION
# ============================================================

def process_signal(ide_path, axis, start_time, end_time):
    """
    Pipeline:
    IDE → acceleration → time filter → integration →
    velocity/displacement → plot
    """

    # -----------------------------
    # CONSTANTS
    # -----------------------------
    ACCEL_40G = 80
    G_TO_M2S = 9.81

    axis_dict = {"X": 0, "Y": 1, "Z": 2}

    if axis not in axis_dict:
        raise ValueError(f"Invalid axis '{axis}'. Must be one of X, Y, Z.")

    axis_number = axis_dict[axis]

    # ============================================================
    # LOAD IDE FILE
    # ============================================================
    doc = endaq.ide.get_doc(ide_path)

    # ============================================================
    # EXTRACT ACCELERATION SIGNAL
    # ============================================================
    raw_accel = endaq.ide.to_pandas(
        doc.channels[ACCEL_40G].subchannels[axis_number],
        time_mode="seconds",
    )

    if raw_accel is None or len(raw_accel) == 0:
        raise ValueError("No acceleration data found in IDE file.")

    # convert to m/s²
    raw_accel = raw_accel * G_TO_M2S

    # rename + clean
    df_accel = raw_accel.copy()
    df_accel.columns = ["acceleration"]

    # ============================================================
    # NORMALIZE TIME
    # ============================================================
    df_accel.index = df_accel.index - df_accel.index.min()

    # ============================================================
    # FILTER TIME WINDOW
    # ============================================================
    df_accel = df_accel[
        (df_accel.index >= start_time) &
        (df_accel.index <= end_time)
    ]

    if df_accel.empty:
        raise ValueError(
            "Selected time range returned no data. "
            "Check start_time and end_time."
        )

    # ============================================================
    # INTEGRATION (VELOCITY + DISPLACEMENT)
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

    # ============================================================
    # UNIT CONVERSION
    # ============================================================
    df_velocity *= 1e3       # m/s → mm/s
    df_displacement *= 1e3   # m → mm

    # ============================================================
    # ALIGN & COMBINE DATA
    # ============================================================
    df = df_accel.join(df_velocity, how="left")
    df = df.join(df_displacement, how="left")

    # ============================================================
    # PLOT
    # ============================================================
    fig = create_result_plot(df)

    return df, fig
#     return df, fig



