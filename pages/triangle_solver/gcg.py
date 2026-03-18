from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import math
from __hidden.__solve import _solve_ccc_common
from __hidden.__draw import _draw_default
from __hidden.__safe import _safe_extract_to_real_num


input_style = {"width": "80px", "textAlign": "center"}
res_style = {"width": "120px", "fontWeight": "bold", "color": "#4a90e2", "fontSize": "1.1rem"}

layout = html.Div([
    dbc.Container([
        # Góc 1
        dbc.Row([
            dbc.Col("Góc 1", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="gcg_angle1", type="number", value=45, min=0.1, max=179.8, style={"maxWidth": "150px"}),
                    dbc.InputGroupText("độ (°)"),
                ]), width=10
            ),
        ], className="mb-3"),

        # Cạnh giữa
        dbc.Row([
            dbc.Col("Cạnh giữa", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="gcg_c_a", type="number", value=0, style=input_style),
                    dbc.InputGroupText("+", className="bg-transparent border-0"),
                    dbc.Input(id="gcg_c_b", type="number", value=1, style=input_style),
                    dbc.InputGroupText("√", className="bg-transparent border-0"),
                    dbc.Input(id="gcg_c_c", type="number", value=0, min=0, style=input_style),
                    dbc.InputGroupText("=", className="bg-transparent border-0"),
                    dbc.InputGroupText("≈", className="bg-transparent border-0"),
                    dbc.Input(id="gcg_c_val", type="number", readonly=True, plaintext=True, style=res_style),
                ]), width=10
            )
        ], className="mb-3"),

        # Góc 2
        dbc.Row([
            dbc.Col("Góc 2", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="gcg_angle2", type="number", value=45, min=0.1, max=179.8, style={"maxWidth": "150px"}),
                    dbc.InputGroupText("độ (°)"),
                ]), width=10
            ),
        ], className="mb-4"),

    ], fluid=True),

    dbc.Row(
        dbc.Col(
            dcc.Loading(
                children=dbc.Button("Giải tam giác", id="btn_gcg", color="primary", size="lg", disabled=True, className="px-5")
            ), className="text-center"
        )
    ),

    dbc.Row([
        dbc.Col(html.Div(id="o_gcg"), width=12, lg=4),
        dbc.Col(dcc.Graph(id="output_gcg", figure=_draw_default()), width=12, lg=8)
    ], className="mt-4")
], id="gcg", className="p-3")



@callback(
    [Output("gcg_c_val", "value"), Output("btn_gcg", "disabled")],
    [
        Input("gcg_c_a", "value"), Input("gcg_c_b", "value"), Input("gcg_c_c", "value"),
        Input("gcg_angle1", "value"), Input("gcg_angle2", "value")
    ]
)
def update_gcg_real_time(a, b, c, g1, g2):
    val_c = _safe_extract_to_real_num(a, b, c)
    
    is_valid = all([
        val_c is not None and val_c > 0,
        g1 is not None and g2 is not None,
        g1 and g2 and (g1 + g2) < 180
    ])
    
    return val_c, not is_valid



@callback(
    [Output("o_gcg", "children"), Output("output_gcg", "figure")],
    Input("btn_gcg", "n_clicks"),
    [
        State("gcg_c_val", "value"),
        State("gcg_angle1", "value"),
        State("gcg_angle2", "value")
    ],
    prevent_initial_call=True
)
def solve_gcg_final(n, base_c, g1, g2):
    g3 = 180 - g1 - g2
    
    A = math.radians(g1)
    B = math.radians(g2)
    C = math.radians(g3)
    
    side_a = base_c * math.sin(A) / math.sin(C)
    side_b = base_c * math.sin(B) / math.sin(C)

    table, graph = _solve_ccc_common(side_a, side_b, base_c)
    
    return table, graph