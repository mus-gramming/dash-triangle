import numpy as np
import plotly.graph_objects as go
from models.triangle import TriangleWithCoords


def _draw_default():
    fig = go.Figure()
    
    fig.update_layout(
        # Thiết lập tọa độ mặc định (ví dụ từ -10 đến 10)
        xaxis=dict(
            range=[-10, 10],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color="#94a3b8"),
            scaleanchor="y",
        ),
        yaxis=dict(
            range=[-10, 10],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color="#94a3b8"),
        ),
        
        # Nhuộm đen tuyệt đối
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        
        # Chữ hiển thị khi chưa có dữ liệu
        annotations=[{
            "text": "Vui lòng nhập tọa độ để phân tích",
            "xref": "paper", "yref": "paper",
            "showarrow": False,
            "font": {"size": 16, "color": "#94a3b8"}
        }]
    )
    return fig



def _draw_triangle(x1, y1, x2, y2, x3, y3):

    tri = TriangleWithCoords(x1, y1, x2, y2, x3, y3)

    A, B, C = tri.A, tri.B, tri.C

    centroid = tri.centroid()
    orthocenter = tri.orthocenter()
    circum = tri.circumcircle()
    incircle = tri.incircle()

    G = centroid["intersect"]
    H = orthocenter["intersect"]
    O = circum["intersect"]
    I = incircle["intersect"]

    fig = go.Figure()


    # =================================
    # Helper: vẽ circle
    # =================================

    def draw_circle(center, r, name, group):

        theta = np.linspace(0, 2*np.pi, 200)

        fig.add_trace(go.Scatter(
            x=center.x + r*np.cos(theta),
            y=center.y + r*np.sin(theta),
            mode="lines",
            name=name,
            legendgroup=group,
            visible="legendonly"
        ))


    # =================================
    # 1 TRIANGLE
    # =================================

    fig.add_trace(go.Scatter(
        x=[A.x, B.x, C.x, A.x],
        y=[A.y, B.y, C.y, A.y],
        mode="lines+markers+text",
        text=["A","B","C",""],
        textposition="top center",
        line=dict(width=3),
        name="Tam giác",
        showlegend=False
    ))


    # =================================
    # 2 MEDIAN
    # =================================

    for v, f in [

        (A, centroid["feet"]["A_feet"]),
        (B, centroid["feet"]["B_feet"]),
        (C, centroid["feet"]["C_feet"])

    ]:

        fig.add_trace(go.Scatter(
            x=[v.x,f.x],
            y=[v.y,f.y],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="median",
            name="Trung tuyến",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[G.x],
        y=[G.y],
        mode="markers",
        marker=dict(size=10),
        legendgroup="median",
        name="Trọng tâm",
        visible="legendonly"
    ))


    # =================================
    # 3 ALTITUDE (SỬA CHỖ QUAN TRỌNG)
    # =================================

    for v,f in [

        (A, orthocenter["feet"]["A_feet"]),
        (B, orthocenter["feet"]["B_feet"]),
        (C, orthocenter["feet"]["C_feet"])

    ]:

        fig.add_trace(go.Scatter(
            x=[v.x,f.x],
            y=[v.y,f.y],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="altitude",
            name="Đường cao",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[H.x],
        y=[H.y],
        mode="markers",
        legendgroup="altitude",
        name="Trực tâm",
        visible="legendonly"
    ))


    # =================================
    # 4 BISECTOR
    # =================================

    for v,f in [

        (A, incircle["feet"]["A_feet"]),
        (B, incircle["feet"]["B_feet"]),
        (C, incircle["feet"]["C_feet"])

    ]:

        fig.add_trace(go.Scatter(
            x=[v.x,f.x],
            y=[v.y,f.y],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="bisector",
            name="Phân giác",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[I.x],
        y=[I.y],
        mode="markers",
        legendgroup="bisector",
        name="Tâm nội tiếp",
        visible="legendonly"
    ))

    draw_circle(I, incircle["radius"], "Nội tiếp", "bisector")


    # =================================
    # 5 PERP BISECTOR
    # =================================

    for line in circum["lines"]:

        fig.add_trace(go.Scatter(
            x=line["x"],
            y=line["y"],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="perp",
            name="Trung trực",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[O.x],
        y=[O.y],
        mode="markers",
        legendgroup="perp",
        name="Tâm ngoại tiếp",
        visible="legendonly"
    ))

    draw_circle(O, circum["radius"], "Ngoại tiếp", "perp")


    # =================================
    # 6 EULER LINE (GỌN HƠN)
    # =================================

    pts = [O,G,H]

    uniq=[]

    for p in pts:
        if not any(p==q for q in uniq):
            uniq.append(p)

    if len(uniq)>=2:

        P1,P2 = uniq[:2]

        dx=P2.x-P1.x
        dy=P2.y-P1.y

        L=np.hypot(dx,dy)

        if L>0:

            dx/=L
            dy/=L

            scale=50

            fig.add_trace(go.Scatter(

                x=[P1.x-dx*scale,P1.x+dx*scale],
                y=[P1.y-dy*scale,P1.y+dy*scale],

                mode="lines",

                name="Euler",
                legendgroup="euler",
                visible="legendonly"

            ))


    # =================================
    # 7 AUTO SCALE (ỔN ĐỊNH HƠN)
    # =================================

    pts=[A,B,C,O,I,G,H]

    xs=[p.x for p in pts]
    ys=[p.y for p in pts]

    minx,maxx=min(xs),max(xs)
    miny,maxy=min(ys),max(ys)

    size=max(maxx-minx,maxy-miny)+1

    cx=(minx+maxx)/2
    cy=(miny+maxy)/2


    fig.update_layout(

        xaxis=dict(
            range=[cx-size,cx+size],
            scaleanchor="y",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)', # Đường lưới siêu mờ
            zerolinecolor='rgba(255, 255, 255, 0.1)', # Trục 0 mờ
            tickfont=dict(color="#94a3b8") # Màu muted text cho tọa độ
        ),

        yaxis=dict(
            range=[cy-size,cy+size],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color="#94a3b8")
        ),

        height=600,
        margin=dict(l=20, r=20, t=40, b=20), # Giảm margin cho gọn

        legend=dict(
            orientation="h",
            y=-0.1,
            x=0.5,
            xanchor="center",
            bgcolor="rgba(0,0,0,0)", # Legend trong suốt
            bordercolor="rgba(255,255,255,0.05)", # Viền mờ
            font=dict(color="#e2e4e9") # Màu text chính
        ),

        template="plotly_dark", # Sử dụng theme tối mặc định của Plotly
        paper_bgcolor='rgba(0,0,0,0)', # Nền trong suốt để lộ nền web `#0f111a`
        plot_bgcolor='rgba(0,0,0,0)',  # Nền vùng vẽ trong suốt

        dragmode="pan", # Mặc định là chế độ kéo (Pan) cho dễ thao tác
    )

    return fig