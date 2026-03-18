from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from __hidden.__solve import _solve_ccc_common
from __hidden.__draw import _draw_default
from __hidden.__safe import _safe_extract_to_real_num



# Định nghĩa style chung cho các ô nhập liệu nhỏ
input_style = {"width": "80px", "textAlign": "center", "borderRadius": "5px"}
res_style = {"width": "120px", "fontWeight": "bold", "color": "#4a90e2", "fontSize": "1.1rem"}

layout = html.Div([
    dbc.Container([
        # Hàm tạo hàng nhập liệu cho gọn code
        *[dbc.Row([
            dbc.Col(f"Cạnh {i}", width=2, className="fw-bold align-self-center"),
            dbc.Col(
                dbc.InputGroup([
                    dbc.Input(id=f"c{i}_a", type="number", value=0, style=input_style),
                    dbc.InputGroupText("+", className="bg-transparent border-0"),
                    dbc.Input(id=f"c{i}_b", type="number", value=1, style=input_style),
                    dbc.InputGroupText("√", className="bg-transparent border-0"),
                    dbc.Input(id=f"c{i}_c", type="number", value=0, min=0, style=input_style),
                    dbc.InputGroupText("=", className="bg-transparent border-0"),
                    dbc.Input(id=f"c{i}", type="number", readonly=True, plaintext=True, style=res_style),
                ], className="mb-3")
            , width=10)
        ]) for i in range(1, 4)],

        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    children=dbc.Button("Tính toán", id="btn", color="primary", size="lg", disabled=True, className="px-5 mt-3")
                ), className="text-center"
            )
        ),

        dbc.Row([
            dbc.Col(html.Div(id="o1"), width=12, lg=4),
            dbc.Col(dcc.Graph(id="output1", figure=_draw_default()), width=12, lg=8)
        ], className="mt-4")
    ], fluid=True)
], id="ccc", className="p-3")



@callback(
    [
        Output("c1", "value"), Output("c2", "value"), Output("c3", "value"),
        Output("btn", "disabled")
    ], 
    [
        Input("c1_a", "value"), Input("c1_b", "value"), Input("c1_c", "value"),
        Input("c2_a", "value"), Input("c2_b", "value"), Input("c2_c", "value"),
        Input("c3_a", "value"), Input("c3_b", "value"), Input("c3_c", "value"),
    ]
)
def update_real_values(*vals):
    v1 = _safe_extract_to_real_num(vals[0], vals[1], vals[2])
    v2 = _safe_extract_to_real_num(vals[3], vals[4], vals[5])
    v3 = _safe_extract_to_real_num(vals[6], vals[7], vals[8])
    
    is_ready = all(v > 0 for v in [v1, v2, v3] if v is not None)
    
    return v1, v2, v3, not is_ready



@callback(
    [Output("o1", "children"), Output("output1", "figure")],
    Input("btn", "n_clicks"),
    [
        State("c1", "value"), 
        State("c2", "value"), 
        State("c3", "value")
    ],
    prevent_initial_call=True
)
def calc_ccc(n, c1, c2, c3):
    table, graph = _solve_ccc_common(c1, c2, c3)

    if c1 + c2 <= c3 or c1 + c3 <= c2 or c2 + c3 <= c1:
        return (
            dbc.Alert(
                "Không thỏa mãn bất đẳng thức tam giác: Tổng hai cạnh phải lớn hơn cạnh còn lại.",
                color="danger", className="mt-3"
            ),
            _draw_default()
        )

    return table, graph