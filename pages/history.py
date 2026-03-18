import dash
from dash import html, dcc, Input, Output, callback, State, ALL, callback_context
import dash_bootstrap_components as dbc
from init_database import get_session, TriangleDomain

dash.register_page(__name__, path="/history")



layout = dbc.Container([
    dcc.Store(id="current-page-store", data=1),


    html.H2("📜 Tra cứu tam giác", className="text-light mb-4"),
    html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),

    dbc.Card([
        dbc.CardHeader(
            html.H5("🔎 Bộ lọc tra cứu", className="mb-0")
        ),
        dbc.CardBody([
            dbc.Col([
                html.Label("Trạng thái", className="small text-muted"),
                dcc.Dropdown(
                    id="valid-filter",
                    options=[
                        {"label": "Tất cả", "value": "all"},
                        {"label": "Hợp lệ", "value": "true"},
                        {"label": "Không hợp lệ", "value": "false"}
                    ],
                    value="all",
                    clearable=False,
                    className="dark-dropdown"
                )
            ], md=3),

            # ===== ROW 1 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Theo cạnh", className="small text-muted"),
                    dcc.Dropdown(
                        id="edge-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác đều","value":"Tam giác đều"},
                            {"label":"Tam giác cân","value":"Tam giác cân"},
                            {"label":"Tam giác thường","value":"Tam giác thường"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown" # Thêm class này
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Theo góc", className="small text-muted"),
                    dcc.Dropdown(
                        id="angle-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác nhọn","value":"Tam giác nhọn"},
                            {"label":"Tam giác vuông","value":"Tam giác vuông"},
                            {"label":"Tam giác tù","value":"Tam giác tù"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown"
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Nguồn", className="small text-muted"),
                    dcc.Dropdown(
                        id="by-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Web","value":"web"},
                            {"label":"API","value":"api"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown"
                    )
                ], md=4)
            ], className="mb-3"),

            # ===== ROW 2 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Khoảng ngày", className="small text-muted d-block"),
                    dcc.DatePickerRange(
                        id="date-filter",
                        className="dark-date-picker" # Thêm class này
                    )
                ], md=9),

                dbc.Col([
                    html.Br(),
                    dbc.ButtonGroup([
                        dbc.Button(
                            "🔎 Tra cứu",
                            id="btn-search",
                            color="primary",
                            className="shadow-sm"
                        ),
                        dbc.Button(
                            "🔄 Reset",
                            id="btn-reset",
                            color="secondary",
                            outline=True,
                            className="shadow-sm"
                        ),
                    ], className="w-100")
                ], md=6, lg=3, className="ms-auto")
            ])
        ])
    ], className="main-card mb-4 border-0", style={"backgroundColor": "#1a1d2b", "color": "#e2e4e9"}),

    dcc.Loading(
        html.Div([
            html.Div(id="table-container"),
            html.Div(id="pagination-container", className="d-flex justify-content-center mt-3")
        ]),
        type="circle",
        color="#4a90e2"
    )


], className="main-content g-4")



@callback(
    [Output("valid-filter", "value"),
     Output("edge-filter", "value"),
     Output("angle-filter", "value"),
     Output("by-filter", "value"),
     Output("date-filter", "start_date"),
     Output("date-filter", "end_date"),
     Output("edge-filter", "disabled"),
     Output("angle-filter", "disabled")],
    [Input("btn-reset", "n_clicks"),
     Input("valid-filter", "value")],
    prevent_initial_call=True
)
def handle_filter_logic(n_reset, valid_val):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "btn-reset":
        return "all", "", "", "", None, None, False, False

    if trigger_id == "valid-filter":
        if valid_val == "false":
            return (dash.no_update, "", "", dash.no_update, 
                    dash.no_update, dash.no_update, True, True)
        else:
            return (dash.no_update, dash.no_update, dash.no_update, 
                    dash.no_update, dash.no_update, dash.no_update, False, False)

    return [dash.no_update] * 8



def get_angle_badge(angle_type):
    # Ánh xạ loại góc sang màu sắc Badge
    color_map = {
        "Tam giác nhọn": "success", 
        "Tam giác vuông": "warning", 
        "Tam giác tù": "danger", 
    }
    
    color = color_map.get(angle_type, None)
    return dbc.Badge(angle_type, color=color, pill=True)



def get_edge_badge(edge_type):
    # Ánh xạ loại cạnh
    color_map = {
        "Tam giác đều": "info",  
        "Tam giác cân": "primary",
        "Tam giác thường": "dark", 
    }
    color = color_map.get(edge_type, None)
    return dbc.Badge(edge_type, color=color, pill=True, className="border border-light")



@callback(
    [Output("table-container", "children"),
     Output("pagination-container", "children")],
    [Input("btn-search", "n_clicks"),
     # Dùng Pattern-Matching ID ở đây để tránh lỗi "nonexistent object"
     Input({'type': 'history-pagination', 'index': ALL}, "active_page")],
    [State("valid-filter", "value"),
     State("edge-filter", "value"),
     State("angle-filter", "value"),
     State("by-filter", "value"),
     State("date-filter", "start_date"),
     State("date-filter", "end_date")],
    prevent_initial_call=True
)
def search(n, active_page_list, is_valid_v, edge_v, angle_v, by_v, start, end):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update

    # Xác định ID nào vừa kích hoạt Callback
    trigger_id = ctx.triggered[0]['prop_id']
    
    if "btn-search" in trigger_id:
        active_page = 1
    else:
        active_page = active_page_list[0] if active_page_list else 1

    page_size = 20
    session = get_session()
    
    try:
        query = session.query(TriangleDomain)
        
        # 1. Áp dụng các bộ lọc (Filter)
        if is_valid_v != "all":
            query = query.filter(TriangleDomain.is_valid == (is_valid_v == "true"))
        if edge_v: query = query.filter(TriangleDomain.edge_type == edge_v)
        if angle_v: query = query.filter(TriangleDomain.angle_type == angle_v)
        if by_v: query = query.filter(TriangleDomain.by == by_v)
        if start: query = query.filter(TriangleDomain.created_at >= start)
        if end: query = query.filter(TriangleDomain.created_at <= end)

        # 2. Tính toán phân trang
        total_records = query.count()
        total_pages = (total_records + page_size - 1) // page_size

        results = query.order_by(TriangleDomain.created_at.desc()) \
                       .limit(page_size) \
                       .offset((active_page - 1) * page_size) \
                       .all()

        if not results:
            return dbc.Alert("Không có dữ liệu phù hợp.", color="info", className="mt-3"), ""

        # 3. Tạo Rows cho Table (Tính STT chuẩn theo trang)
        start_stt = (active_page - 1) * page_size + 1
        rows = []
        for i, t in enumerate(results, start=start_stt):
            if t.is_valid:
                edge_display = get_edge_badge(t.edge_type)
                angle_display = get_angle_badge(t.angle_type)
                status_badge = dbc.Badge("Valid", color="success")
            else:
                edge_display = html.Span("---", className="text-muted")
                angle_display = html.Span("---", className="text-muted")
                status_badge = dbc.Badge("Invalid", color="danger")

            rows.append(html.Tr([
                html.Td(i, className="align-middle"),
                html.Td(edge_display, className="align-middle"),   
                html.Td(angle_display, className="align-middle"),  
                html.Td(status_badge, className="align-middle"),  
                html.Td(t.by.upper(), className="align-middle font-weight-bold"),
                html.Td(t.created_at.strftime("%H:%M %d/%m"), className="align-middle small"),
                html.Td(f"({t.x1:.2f}, {t.y1:.2f})", className="font-monospace small align-middle text-info"),
                html.Td(f"({t.x2:.2f}, {t.y2:.2f})", className="font-monospace small align-middle text-info"),
                html.Td(f"({t.x3:.2f}, {t.y3:.2f})", className="font-monospace small align-middle text-info"),
            ]))

        # 4. Tạo Table & Pagination UI
        table = dbc.Table([
            html.Thead(html.Tr([
                html.Th("STT"), html.Th("Loại cạnh"), html.Th("Loại góc"), 
                html.Th("Trạng thái"), html.Th("Nguồn"), html.Th("Thời gian"), 
                html.Th("Tọa độ A"), html.Th("Tọa độ B"), html.Th("Tọa độ C")
            ])),
            html.Tbody(rows)
        ], striped=True, hover=True, bordered=True, className="mt-3")

        pagination_ui = dbc.Pagination(
            id={'type': 'history-pagination', 'index': 'main'},
            active_page=active_page,
            max_value=total_pages,
            fully_expanded=False, 
            first_last=True,
            previous_next=True,
            size="sm",
            className="mt-3"
        ) if total_pages > 1 else ""

        return table, pagination_ui

    except Exception as e:
        return dbc.Alert(f"Lỗi truy vấn: {str(e)}", color="danger"), ""
    finally:
        session.close()