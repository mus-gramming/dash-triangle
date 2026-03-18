from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import math
from __hidden.__solve import _solve_ccc_common
from __hidden.__draw import _draw_default
from __hidden.__safe import _safe_extract_to_real_num



# Style đồng nhất với file CCC
input_style = {"width": "80px", "textAlign": "center"}
res_style = {"width": "120px", "fontWeight": "bold", "color": "#4a90e2", "fontSize": "1.1rem"}

layout = html.Div([
    dbc.Container([
        # Cạnh 1
        dbc.Row([
            dbc.Col("Cạnh 1", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="cgc_c1_a", type="number", value=0, style=input_style),
                    dbc.InputGroupText("+", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c1_b", type="number", value=1, style=input_style),
                    dbc.InputGroupText("√", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c1_c", type="number", value=0, min=0, style=input_style),
                    dbc.InputGroupText("=", className="bg-transparent border-0"),
                    dbc.InputGroupText("≈", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c1_val", type="number", readonly=True, plaintext=True, style=res_style),
                ]), width=10
            )
        ], className="mb-3"),

        # Góc giữa
        dbc.Row([
            dbc.Col("Góc giữa", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="cgc_angle", type="number", value=60, min=0.1, max=179.9, style={"width": "100px"}),
                    dbc.InputGroupText("độ (°)"),
                ]), width=10
            )
        ], className="mb-3"),

        # Cạnh 2
        dbc.Row([
            dbc.Col("Cạnh 2", width=2, className="align-self-center fw-bold"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id="cgc_c2_a", type="number", value=0, style=input_style),
                    dbc.InputGroupText("+", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c2_b", type="number", value=1, style=input_style),
                    dbc.InputGroupText("√", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c2_c", type="number", value=0, min=0, style=input_style),
                    dbc.InputGroupText("=", className="bg-transparent border-0"),
                    dbc.InputGroupText("≈", className="bg-transparent border-0"),
                    dbc.Input(id="cgc_c2_val", type="number", readonly=True, plaintext=True, style=res_style),
                ]), width=10
            )
        ], className="mb-4"),

    ], fluid=True),

    dbc.Row(
        dbc.Col(
            dcc.Loading(
                children=dbc.Button("Tính toán", id="btn_cgc", color="primary", size="lg", disabled=True, className="px-5")
            ), className="text-center"
        )
    ),

    dbc.Row([
        dbc.Col(html.Div(id="o_cgc"), width=12, lg=4),
        dbc.Col(dcc.Graph(id="output_cgc", figure=_draw_default()), width=12, lg=8)
    ], className="mt-4")
], id="cgc", className="p-3")



@callback(
    [
        Output("cgc_c1_val", "value"),
        Output("cgc_c2_val", "value"),
        Output("btn_cgc", "disabled")
    ],
    [
        Input("cgc_c1_a", "value"), Input("cgc_c1_b", "value"), Input("cgc_c1_c", "value"),
        Input("cgc_c2_a", "value"), Input("cgc_c2_b", "value"), Input("cgc_c2_c", "value"),
        Input("cgc_angle", "value")
    ]
)
def update_cgc_inputs(c1a, c1b, c1c, c2a, c2b, c2c, angle):
    v1 = _safe_extract_to_real_num(c1a, c1b, c1c)
    v2 = _safe_extract_to_real_num(c2a, c2b, c2c)
    
    # Kiểm tra hợp lệ: cạnh > 0 và 0 < góc < 180
    is_valid = all([
        v1 is not None and v1 > 0,
        v2 is not None and v2 > 0,
        angle is not None and 0 < angle < 180
    ])
    
    # Trả về v1, v2 kiểu float (không cần f-string nữa)
    return v1, v2, not is_valid



@callback(
    [Output("o_cgc", "children"), Output("output_cgc", "figure")],
    Input("btn_cgc", "n_clicks"),
    [
        State("cgc_c1_val", "value"),
        State("cgc_c2_val", "value"),
        State("cgc_angle", "value")
    ],
    prevent_initial_call=True
)
def calc_cgc_final(n, c1, c2, angle_deg):
    angle_rad = math.radians(angle_deg)
    
    cos_val = c1**2 + c2**2 - 2*c1*c2*math.cos(angle_rad)
    c3 = math.sqrt(max(cos_val, 0))

    table, graph = _solve_ccc_common(c1, c3, c2)
    return table, graph