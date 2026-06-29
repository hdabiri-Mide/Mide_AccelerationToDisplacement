# import streamlit as st
# import tempfile

# from processing import preview_signal, process_signal

# st.set_page_config(
#     page_title="IDE Signal Converter",
#     layout="wide"
# )

# st.title("IDE Signal Converter")

# st.write(
#     """
# Upload an IDE file, preview the acceleration,
# choose a time range, convert to velocity/displacement,
# and export the desired signal.
# """
# )

# ############################################################
# # Upload IDE
# ############################################################

# uploaded_file = st.file_uploader(
#     "Upload IDE File",
#     type=["ide", "IDE"]
# )

# if uploaded_file is not None:

#     temp_file = tempfile.NamedTemporaryFile(
#         delete=False,
#         suffix=".IDE"
#     )

#     temp_file.write(uploaded_file.read())

#     ide_path = temp_file.name

#     ########################################################
#     # Axis selection
#     ########################################################

#     axis = st.selectbox(
#         "Axis",
#         ["X", "Y", "Z"]
#     )

#     ########################################################
#     # Preview
#     ########################################################

#     st.subheader("Raw Acceleration")

#     fig_preview = preview_signal(
#         ide_path,
#         axis
#     )

#     st.plotly_chart(
#         fig_preview,
#         use_container_width=True
#     )

#     ########################################################
#     # Time selection
#     ########################################################

#     col1, col2 = st.columns(2)

#     with col1:
#         start_time = st.number_input(
#             "Start Time (s)",
#             value=0.0,
#             step=1.0
#         )

#     with col2:
#         end_time = st.number_input(
#             "End Time (s)",
#             value=10.0,
#             step=1.0
#         )

#     ########################################################
#     # Process
#     ########################################################

#     if st.button("Process Signal"):

#         with st.spinner("Processing..."):

#             df, fig = process_signal(
#                 ide_path,
#                 axis,
#                 start_time,
#                 end_time
#             )

#         st.success("Done!")

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         ####################################################
#         # Export
#         ####################################################

#         st.subheader("Export CSV")

#         signal = st.radio(
#             "Choose Signal",
#             [
#                 "Acceleration",
#                 "Velocity",
#                 "Displacement"
#             ]
#         )

#         if signal == "Acceleration":
#             export_df = df[["acceleration"]]

#         elif signal == "Velocity":
#             export_df = df[["velocity"]]

#         else:
#             export_df = df[["displacement"]]

#         csv = export_df.to_csv().encode("utf-8")

#         st.download_button(
#             label="Download CSV",
#             data=csv,
#             file_name=f"{signal}.csv",
#             mime="text/csv"
#         )


########################################################################## Test
import streamlit as st
import tempfile
import plotly.express as px

from processing import preview_signal, process_signal


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="IDE Signal Converter",
    layout="wide"
)

st.title("IDE Signal Converter")

st.write(
    """
Upload an IDE file, preview acceleration,
select a time range, process into velocity/displacement,
and download the result.
"""
)


# ============================================================
# SESSION STATE INIT
# ============================================================
if "df" not in st.session_state:
    st.session_state["df"] = None

if "ide_path" not in st.session_state:
    st.session_state["ide_path"] = None


# ============================================================
# FILE UPLOAD
# ============================================================
uploaded_file = st.file_uploader(
    "Upload IDE File",
    type=["ide", "IDE"]
)

if uploaded_file is not None:

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".IDE"
    )

    temp_file.write(uploaded_file.read())
    ide_path = temp_file.name

    st.session_state["ide_path"] = ide_path


# ============================================================
# MAIN APP (ONLY IF FILE EXISTS)
# ============================================================
if st.session_state["ide_path"] is not None:

    ide_path = st.session_state["ide_path"]

    # --------------------------------------------------------
    # AXIS SELECTION
    # --------------------------------------------------------
    axis = st.selectbox(
        "Axis",
        ["X", "Y", "Z"]
    )

    # --------------------------------------------------------
    # PREVIEW SIGNAL (ALWAYS SAFE)
    # --------------------------------------------------------
    st.subheader("Raw Acceleration")

    fig_preview = preview_signal(
        ide_path,
        axis
    )

    st.plotly_chart(
        fig_preview,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TIME RANGE INPUT
    # --------------------------------------------------------
    st.subheader("Time Selection")

    col1, col2 = st.columns(2)

    with col1:
        start_time = st.number_input(
            "Start Time (s)",
            value=0.0,
            step=1.0
        )

    with col2:
        end_time = st.number_input(
            "End Time (s)",
            value=10.0,
            step=1.0
        )

    # --------------------------------------------------------
    # PROCESS BUTTON (ONLY TRIGGERS COMPUTATION)
    # --------------------------------------------------------
    if st.button("Process Signal"):

        with st.spinner("Processing..."):

            df = process_signal(
                ide_path,
                axis,
                start_time,
                end_time
            )

            st.session_state["df"] = df

        st.success("Processing complete!")

    # --------------------------------------------------------
    # RESULTS (PERSISTENT UI)
    # --------------------------------------------------------
    if st.session_state["df"] is not None:

        df = st.session_state["df"]

        st.subheader("Processed Signal")

        # ----------------------------------------------------
        # SIGNAL VIEW SELECTOR (NO RECOMPUTATION)
        # ----------------------------------------------------
        signal = st.radio(
            "Choose Signal",
            ["Acceleration", "Velocity", "Displacement"],
            key="signal_view"
        )

        if signal == "Acceleration":
            y = df["acceleration"]
        elif signal == "Velocity":
            y = df["velocity"]
        else:
            y = df["displacement"]

        fig = px.line(
            x=y.index,
            y=y.values,
            labels={"x": "Time [s]", "y": signal},
            title=f"{signal} Signal"
        )

        fig.update_layout(hovermode="x unified")

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------------------------
        # DOWNLOAD SECTION
        # ----------------------------------------------------
        st.subheader("Export Data")

        csv = df.to_csv(index=True).encode("utf-8")

        st.download_button(
            label="Download Full CSV (Accel + Vel + Disp)",
            data=csv,
            file_name="processed_signal.csv",
            mime="text/csv"
        )
