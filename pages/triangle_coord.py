import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from __hidden.__table import _create_table
import models.triangle as triangle
import init_database
from __hidden.__draw import _draw_triangle, _draw_default

dash.register_page(__name__, path="/calc/coord")

input_form = dbc.Table(
    [
        html.Thead(
            html.Tr([
                html.Th(""),
                html.Th("Theo trục x"),
                html.Th("Theo trục y"),
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td("Cạnh 1"),
                html.Td(dbc.Input(id="x1", type="number", value=0)),
                html.Td(dbc.Input(id="y1", type="number", value=0)),
            ]),
            html.Tr([
                html.Td("Cạnh 2"),
                html.Td(dbc.Input(id="x2", type="number", value=0)),
                html.Td(dbc.Input(id="y2", type="number", value=0)),
            ]),
            html.Tr([
                html.Td("Cạnh 3"),
                html.Td(dbc.Input(id="x3", type="number", value=0)),
                html.Td(dbc.Input(id="y3", type="number", value=0)),
            ]),
        ])
    ],
    bordered=True,
)



layout = html.Div([
    input_form, 
    
    dbc.Row(
        dbc.Col(
            dbc.Button(
                "Tính toán",
                id="btn-calc",
                color="primary",
                size="lg",
                className="mt-3 w-100",
            ),
            width=4
        ),
        justify="center"
    ),

    dbc.Alert(
        id="alert",
        is_open=False,
        color="danger",
        dismissable=True
    ),

    dbc.Spinner(
        dbc.Row([
            dbc.Col(html.Div(id="output"), width=3),
            dbc.Col(dcc.Graph(id="triangle-graph", figure=_draw_default()), width=9)
        ]),
        color="primary",
        type="border",
        fullscreen=False
    )
])



@callback(
    Output("output", "children"),
    Output("triangle-graph", "figure"),
    Output("alert", "children"),
    Output("alert", "is_open"),
    Input("btn-calc", "n_clicks"),
    State("x1", "value"), State("y1", "value"),
    State("x2", "value"), State("y2", "value"),
    State("x3", "value"), State("y3", "value"),
)
def calculate_triangle(n_clicks, x1, y1, x2, y2, x3, y3):
    if any(v is None for v in [x1, y1, x2, y2, x3, y3]):
        return None, _draw_default(), "Nhập thiếu tọa độ", True

    record = init_database.TriangleDomain(
        x1=x1, y1=y1,
        x2=x2, y2=y2,
        x3=x3, y3=y3,
        by="web"
    )

    with init_database.get_session() as session:
        try:
            session.add(record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Lỗi DB: {e}")

    A = triangle.Point(x1, y1)
    B = triangle.Point(x2, y2)
    C = triangle.Point(x3, y3)

    AB = A.distance_to_other(B)
    AC = A.distance_to_other(C)
    BC = B.distance_to_other(C)
    tri = triangle.Triangle(AB, AC, BC)

    if not tri.is_exist():
        return None, _draw_default(), "Ba điểm không tạo thành tam giác", True

    fig = _draw_triangle(x1, y1, x2, y2, x3, y3)
    table = _create_table(x1, y1, x2, y2, x3, y3)

    return table, fig, None, False