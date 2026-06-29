import streamlit as st
import tempfile
import os 

from processing import preview_signal, process_signal, create_result_plot


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
select time range, and view acceleration/velocity/displacement together.
"""
)


# ============================================================
# SESSION STATE
# ============================================================
if "df" not in st.session_state:
    st.session_state["df"] = None

if "ide_path" not in st.session_state:
    st.session_state["ide_path"] = None


# ============================================================
# FILE UPLOAD
# ============================================================
uploaded_file = st.file_uploader("Upload IDE File", type=["ide", "IDE"])

if uploaded_file is not None:

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".IDE")
    temp_file.write(uploaded_file.read())

    st.session_state["ide_path"] = temp_file.name


# ============================================================
# MAIN APP
# ============================================================
if st.session_state["ide_path"] is not None:

    ide_path = st.session_state["ide_path"]

    # --------------------------------------------------------
    # AXIS
    # --------------------------------------------------------
    axis = st.selectbox("Axis", ["X", "Y", "Z"])

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------
    st.subheader("Raw Acceleration")
    st.plotly_chart(preview_signal(ide_path, axis), use_container_width=True)

    # --------------------------------------------------------
    # TIME RANGE
    # --------------------------------------------------------
    st.subheader("Time Selection")

    col1, col2 = st.columns(2)

    with col1:
        start_time = st.number_input("Start Time (s)", value=0.0)

    with col2:
        end_time = st.number_input("End Time (s)", value=10.0)

    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------
    if st.button("Process Signal"):

        df = process_signal(
            ide_path,
            axis,
            start_time,
            end_time
        )

        st.session_state["df"] = df

        st.success("Processing complete!")

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------
    if st.session_state["df"] is not None:

        df = st.session_state["df"]

        st.subheader("Results")

        fig = create_result_plot(df)

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------
        csv = df.to_csv(index=True).encode("utf-8")

        file_name = os.path.splitext(
            os.path.basename(st.session_state["ide_path"])
        )[0]

        st.download_button(
            "Download CSV (Accel + Vel + Disp)",
            csv,
            file_name=f"{file_name}_processed.csv",
            mime="text/csv"
        )
