import streamlit as st
import tempfile

from processing import preview_signal, process_signal

st.set_page_config(
    page_title="IDE Signal Converter",
    layout="wide"
)

st.title("IDE Signal Converter")

st.write(
    """
Upload an IDE file, preview the acceleration,
choose a time range, convert to velocity/displacement,
and export the desired signal.
"""
)

############################################################
# Upload IDE
############################################################

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

    ########################################################
    # Axis selection
    ########################################################

    axis = st.selectbox(
        "Axis",
        ["X", "Y", "Z"]
    )

    ########################################################
    # Preview
    ########################################################

    st.subheader("Raw Acceleration")

    fig_preview = preview_signal(
        ide_path,
        axis
    )

    st.plotly_chart(
        fig_preview,
        use_container_width=True
    )

    ########################################################
    # Time selection
    ########################################################

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

    ########################################################
    # Process
    ########################################################

    if st.button("Process Signal"):

        with st.spinner("Processing..."):

            df, fig = process_signal(
                ide_path,
                axis,
                start_time,
                end_time
            )

        st.success("Done!")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        ####################################################
        # Export
        ####################################################

        st.subheader("Export CSV")

        signal = st.radio(
            "Choose Signal",
            [
                "Acceleration",
                "Velocity",
                "Displacement"
            ]
        )

        if signal == "Acceleration":
            export_df = df[["acceleration"]]

        elif signal == "Velocity":
            export_df = df[["velocity"]]

        else:
            export_df = df[["displacement"]]

        csv = export_df.to_csv().encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{signal}.csv",
            mime="text/csv"
        )
