# Mide_AccelerationToDisplacement

AccelerationApp/

│
├── app.py                  # Streamlit interface
├── processing.py           # endaq functions
├── requirements.txt
└── temp/

app.py:

app.py implements the Streamlit user interface. It allows users to upload an IDE file, preview the raw acceleration signal, select the axis and time interval, and trigger signal processing. After processing, it displays synchronized acceleration, velocity, and displacement plots and provides a downloadable CSV containing the processed data.

processing.py:

processing.py contains the core data processing pipeline. It loads the uploaded IDE file using the EnDAQ library, extracts the selected acceleration channel, converts acceleration from g to m/s², filters the user-selected time window, computes velocity and displacement through numerical integration, and returns the processed data for visualization and export.

requirements.txt

requirements.txt lists all Python packages required to run the application. When the app is deployed (e.g., on Streamlit Community Cloud), these dependencies are installed automatically on the hosting server. Users accessing the application through the shared web link do not need to install Python or any libraries locally; all computations are performed on the server, and only a web browser is required.
