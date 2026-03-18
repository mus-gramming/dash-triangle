from dash import html
import dash_bootstrap_components as dbc
import numpy as np
from models.triangle import TriangleWithCoords


def _create_table(x1, y1, x2, y2, x3, y3):

    tri = TriangleWithCoords(x1, y1, x2, y2, x3, y3)

    edges = tri.triangle_edges
    angles = edges.angles()


    def row(name,value):

        return html.Tr(

            [
                html.Td(name,className="fw-semibold"),

                html.Td(
                    value,
                    style={
                        "textAlign":"right"
                    }
                )

            ]

        )


    table = dbc.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Thông số"),
                    html.Th("Giá trị")
                ]),
                className="dark-thead"
            ),

            html.Tbody([
                row("Cạnh a (BC)",f"{edges.a:.2f}"),
                row("Cạnh b (AC)",f"{edges.b:.2f}"),
                row("Cạnh c (AB)",f"{edges.c:.2f}"),
                row("Loại tam giác (theo góc)",edges.angle_type()),
                row("Loại tam giác (theo cạnh)",edges.edge_type()),
                row("Góc A",f"{np.degrees(angles['angle_a']):.2f}°"),
                row("Góc B",f"{np.degrees(angles['angle_b']):.2f}°"),
                row("Góc C",f"{np.degrees(angles['angle_c']):.2f}°"),
                row("Chu vi",f"{edges.perimeter():.2f}"),
                row("Diện tích",f"{edges.area():.2f}"),
                row("Bán kính nội tiếp",f"{edges.incircle_radius():.2f}"),
                row("Bán kính ngoại tiếp",f"{edges.circumcircle_radius():.2f}")
            ])
        ],
        striped=True,
        hover=True,
        responsive=True,
        bordered=False,
        className="align-middle"
    )


    return dbc.Card(
        [
            dbc.CardHeader(
                "Kết quả phân tích tam giác",
                className="fw-semibold border-0 bg-transparent text-info"
            ),
            dbc.CardBody(table)
        ],
        className="shadow-sm border-0",
        style={"backgroundColor": "#1a1d2b"}
    )