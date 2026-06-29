from plotly.subplots import make_subplots
import plotly.graph_objects as go


def create_result_plot(df):

    ############################################################
    # CREATE SUBPLOTS
    ############################################################

    fig = make_subplots(

        rows=3,

        cols=1,

        shared_xaxes=True,

        vertical_spacing=0.05,

        subplot_titles=(

            "Acceleration",

            "Velocity",

            "Displacement"

        )

    )

    ############################################################
    # ACCELERATION
    ############################################################

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["acceleration"],

            name="Acceleration"

        ),

        row=1,

        col=1

    )

    ############################################################
    # VELOCITY
    ############################################################

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["velocity"],

            name="Velocity"

        ),

        row=2,

        col=1

    )

    ############################################################
    # DISPLACEMENT
    ############################################################

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["displacement"],

            name="Displacement"

        ),

        row=3,

        col=1

    )

    ############################################################
    # LABELS
    ############################################################

    fig.update_yaxes(

        title_text="m/s²",

        row=1,

        col=1

    )

    fig.update_yaxes(

        title_text="mm/s",

        row=2,

        col=1

    )

    fig.update_yaxes(

        title_text="mm",

        row=3,

        col=1

    )

    fig.update_xaxes(

        title_text="Time [s]",

        row=3,

        col=1

    )

    ############################################################
    # LAYOUT
    ############################################################

    fig.update_layout(

        height=900,

        hovermode="x unified",

        showlegend=False,

        title="Acceleration, Velocity and Displacement"

    )

    return fig
