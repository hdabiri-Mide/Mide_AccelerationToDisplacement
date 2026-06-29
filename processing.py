import os
import tempfile

import endaq
import plotly.express as px

from plotting import create_result_plot


############################################################
# USER CONSTANTS
############################################################

ACCEL_40G = 80

X = 0
Y = 1
Z = 2

G_TO_M2S = 9.81


############################################################
# PREVIEW SIGNAL
############################################################

def preview_signal(
        ide_path,
        axis
):

    axis_dict = {
        "X": X,
        "Y": Y,
        "Z": Z
    }

    axis_number = axis_dict[axis]

    ########################################################

    doc_full = endaq.ide.get_doc(ide_path)

    df_preview = endaq.ide.to_pandas(
        doc_full.channels[ACCEL_40G].subchannels[axis_number],
        time_mode="seconds"
    ) * G_TO_M2S

    df_preview.columns = ["acceleration"]

    fig_preview = px.line(
        df_preview,
        x=df_preview.index,
        y="acceleration",
        labels={
            "index": "Time [s]",
            "acceleration": "Acceleration [m/s²]"
        },
        title="Raw Acceleration Signal"
    )

    fig_preview.update_layout(
        hovermode="x unified"
    )

    return fig_preview


############################################################
# PROCESS SIGNAL
############################################################

def process_signal(
        ide_path,
        axis,
        start_time,
        end_time
):

    axis_dict = {
        "X": X,
        "Y": Y,
        "Z": Z
    }

    axis_number = axis_dict[axis]

    ########################################################
    # CREATE TEMP EXTRACTED IDE
    ########################################################

    temp_folder = tempfile.gettempdir()

    extracted_ide_path = os.path.join(
        temp_folder,
        "Extracted.ide"
    )

    ########################################################
    # EXTRACT TIME RANGE
    ########################################################

    endaq.ide.extract_time(

        ide_path,

        extracted_ide_path,

        start=str(start_time),

        end=str(end_time)

    )

    ########################################################
    # LOAD ACCELERATION
    ########################################################

    doc = endaq.ide.get_doc(
        extracted_ide_path
    )

    df_accel = endaq.ide.to_pandas(

        doc.channels[ACCEL_40G].subchannels[axis_number],

        time_mode="seconds"

    ) * G_TO_M2S

    ########################################################
    # CALCULATE VELOCITY / DISPLACEMENT
    ########################################################

    integrals = endaq.calc.integrate.integrals(

        df_accel,

        n=2,

        highpass_cutoff=1.0,

        tukey_percent=0.05

    )

    df_velocity = integrals[1]

    df_displacement = integrals[2]

    ########################################################
    # RENAME
    ########################################################

    df_accel.columns = ["acceleration"]

    df_velocity.columns = ["velocity"]

    df_displacement.columns = ["displacement"]

    ########################################################
    # CONVERT UNITS
    ########################################################

    df_velocity = df_velocity * 1000

    df_displacement = df_displacement * 1000

    ########################################################
    # JOIN
    ########################################################

    df = df_accel.join(
        df_velocity,
        how="left"
    )

    df = df.join(
        df_displacement,
        how="left"
    )

    ########################################################
    # FIGURE
    ########################################################

    fig = create_result_plot(df)

    ########################################################

    return df, fig
