from dash import html
import dash
import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    brand="Triangle Analyzer",
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink("Trang chủ", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Theo tọa độ", href="/calc/coord", active="exact")),
        dbc.NavItem(dbc.NavLink("Theo cạnh", href="/calc/side", active="exact")),
        dbc.NavItem(dbc.NavLink("Lịch sử", href="/history", active="exact")),
    ],
    color="dark",
    dark=True,
    className="shadow",
    fixed="top"
)



layout = html.Div([
    navbar,

    html.Header([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H1("Triangle Analyzer", className="hero-title"),
                        html.P(
                            "Phân tích – Tính toán – Lưu trữ dữ liệu hình học phẳng",
                            className="hero-sub",
                        ),
                    ], className="hero-box"),
                    md=8
                ),
                className="justify-content-center" 
            )
        ], className="text-center")
    ]),

    html.Main([
        html.Div(
            dash.page_container,
            className="container main-content"
        )
    ]),

    html.Footer([
        dbc.Container([
            html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),
            html.Div([
                html.Small("© 2026 Mus · Triangle Analysis App", className="text-muted")
            ], className="text-center")
        ])
    ])

], **{"data-bs-theme": "dark"}, style={"minHeight": "100vh"})
