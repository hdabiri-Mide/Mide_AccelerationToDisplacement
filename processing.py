

# # ####################################################################################### Works V

# import endaq
# import numpy as np
# import plotly.express as px
# import streamlit as st

# from plotting import create_result_plot


# # ============================================================
# # CONSTANTS
# # ============================================================
# ACCEL_40G = 80
# G_TO_M2S = 9.81

# axis_dict = {"X": 0, "Y": 1, "Z": 2}


# # ============================================================
# # PREVIEW SIGNAL
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
# # MAIN PROCESS FUNCTION (CACHE-OPTIMIZED)
# # ============================================================
# @st.cache_data(show_spinner=False)
# def process_signal(ide_path, axis, start_time, end_time):

#     axis_number = axis_dict[axis]

#     # --------------------------------------------------------
#     # SAFETY CAST (from UI selection)
#     # --------------------------------------------------------
#     start_time = float(start_time)
#     end_time = float(end_time)

#     # ============================================================
#     # LOAD IDE FILE (NO extract_time = stable)
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
#     # UI-BASED SLICING (THIS IS YOUR CORE FIX)
#     # ------------------------------------------------------------
#     # start/end come from Plotly preview selection
#     # ============================================================
#     df_accel = df_accel.loc[
#         (df_accel.index >= start_time) &
#         (df_accel.index <= end_time)
#     ]

#     if len(df_accel) == 0:
#         raise ValueError(
#             "No data in selected window. Adjust selection range."
#         )

#     # ============================================================
#     # INTEGRATION (IDENTICAL TO YOUR LOCAL SCRIPT)
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
#     # FINAL COMBINATION
#     # ============================================================
#     df = df_accel.join(df_velocity, how="left")
#     df = df.join(df_displacement, how="left")

#     # ============================================================
#     # PLOT
#     # ============================================================
#     fig = create_result_plot(df)

#     return df, fig

############################################################################################### test 
# import endaq
# import numpy as np
# import streamlit as st
# import plotly.express as px

# from plotting import create_result_plot


# # ============================================================
# # CONSTANTS
# # ============================================================
# ACCEL_40G = 80
# G_TO_M2S = 9.81

# axis_dict = {"X": 0, "Y": 1, "Z": 2}


# # ============================================================
# # PREVIEW SIGNAL
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
# # PROCESS SIGNAL (CACHED)
# # ============================================================
# @st.cache_data(show_spinner=False)
# def process_signal(ide_path, axis, start_time, end_time):

#     axis_number = axis_dict[axis]

#     start_time = float(start_time)
#     end_time = float(end_time)

#     # --------------------------------------------------------
#     # LOAD DATA
#     # --------------------------------------------------------
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

#     # --------------------------------------------------------
#     # TIME FILTER
#     # --------------------------------------------------------
#     df_accel = df_accel.loc[
#         (df_accel.index >= start_time) &
#         (df_accel.index <= end_time)
#     ]

#     if len(df_accel) == 0:
#         raise ValueError("No data in selected time window.")

#     # --------------------------------------------------------
#     # INTEGRATION
#     # --------------------------------------------------------
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
#     # UNIT SCALING
#     # --------------------------------------------------------
#     df_velocity *= 1e3
#     df_displacement *= 1e3

#     # --------------------------------------------------------
#     # MERGE ALL SIGNALS
#     # --------------------------------------------------------
#     df = df_accel.join(df_velocity, how="left")
#     df = df.join(df_displacement, how="left")

#     return df


# # ============================================================
# # STREAMLIT UI WRAPPER (STATE SAFE)
# # ============================================================
# def run_processing_ui():

#     st.title("Signal Processing Dashboard")

#     # --------------------------------------------------------
#     # INPUT FORM (prevents rerun issues)
#     # --------------------------------------------------------
#     with st.form("input_form"):

#         ide_path = st.text_input("IDE File Path")

#         axis = st.selectbox("Axis", ["X", "Y", "Z"])

#         start_time = st.number_input("Start time (s)", value=0.0)
#         end_time = st.number_input("End time (s)", value=10.0)

#         submitted = st.form_submit_button("Process Signal")

#     # --------------------------------------------------------
#     # PROCESS ONLY ON SUBMIT
#     # --------------------------------------------------------
#     if submitted:

#         df = process_signal(ide_path, axis, start_time, end_time)

#         st.session_state["df"] = df

#     # --------------------------------------------------------
#     # DISPLAY RESULTS (PERSISTENT)
#     # --------------------------------------------------------
#     if "df" in st.session_state:

#         df = st.session_state["df"]

#         st.success("Processing complete")

#         # ----------------------------------------------------
#         # SIGNAL SELECTION (NO RECOMPUTE)
#         # ----------------------------------------------------
#         # view = st.radio(
#         #     "Select signal to view",
#         #     ["Acceleration", "Velocity", "Displacement"],
#         #     key="signal_view"
#         # )

#         # if view == "Acceleration":
#         #     y = df["acceleration"]
#         # elif view == "Velocity":
#         #     y = df["velocity"]
#         # else:
#         #     y = df["displacement"]

#         # fig = px.line(
#         #     y,
#         #     x=y.index,
#         #     y=y.values,
#         #     labels={"x": "Time [s]", "y": view},
#         #     title=f"{view} Signal"
#         # )

#         # fig.update_layout(hovermode="x unified")

#         # st.plotly_chart(fig, use_container_width=True)

#         st.subheader("Acceleration / Velocity / Displacement")

#         fig_acc = px.line(
#             x=df.index,
#             y=df["acceleration"],
#             labels={"x": "Time [s]", "y": "Acceleration"},
#             title="Acceleration"
#         )
        
#         fig_vel = px.line(
#             x=df.index,
#             y=df["velocity"],
#             labels={"x": "Time [s]", "y": "Velocity"},
#             title="Velocity"
#         )
        
#         fig_disp = px.line(
#             x=df.index,
#             y=df["displacement"],
#             labels={"x": "Time [s]", "y": "Displacement"},
#             title="Displacement"
#         )
        
#         st.plotly_chart(fig_acc, use_container_width=True)
#         st.plotly_chart(fig_vel, use_container_width=True)
#         st.plotly_chart(fig_disp, use_container_width=True)


#         # ----------------------------------------------------
#         # DOWNLOAD BUTTON (STABLE)
#         # ----------------------------------------------------
#         csv = df.to_csv(index=True).encode("utf-8")

#         st.download_button(
#             "Download CSV (Accel + Vel + Disp)",
#             data=csv,
#             file_name="processed_signal.csv",
#             mime="text/csv"
#         )

import endaq
import numpy as np
import streamlit as st
import plotly.express as px


# ============================================================
# CONSTANTS
# ============================================================
ACCEL_40G = 80
G_TO_M2S = 9.81

axis_dict = {"X": 0, "Y": 1, "Z": 2}


# ============================================================
# PREVIEW SIGNAL (RAW ACCEL ONLY)
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
# PROCESS SIGNAL (PURE DATA FUNCTION)
# ============================================================
@st.cache_data(show_spinner=False)
def process_signal(ide_path, axis, start_time, end_time):

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

    # scale
    df_velocity *= 1e3
    df_displacement *= 1e3

    df = df_accel.join(df_velocity)
    df = df.join(df_displacement)

    return df


# ============================================================
# UI FUNCTION (FORCE 3 PLOTS)
# ============================================================
def show_results(df):

    st.subheader("Acceleration / Velocity / Displacement")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Acceleration")
        fig1 = px.line(
            x=df.index,
            y=df["acceleration"],
            labels={"x": "Time [s]", "y": "Acceleration"},
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Velocity")
        fig2 = px.line(
            x=df.index,
            y=df["velocity"],
            labels={"x": "Time [s]", "y": "Velocity"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown("### Displacement")
        fig3 = px.line(
            x=df.index,
            y=df["displacement"],
            labels={"x": "Time [s]", "y": "Displacement"},
        )
        st.plotly_chart(fig3, use_container_width=True)
