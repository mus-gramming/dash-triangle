from __hidden.__draw import _draw_triangle, _draw_default
from __hidden.__table import _create_table
from init_database import TriangleDomain, get_session
import dash_bootstrap_components as dbc
import math



def _solve_ccc_common(a, b, c):
    
    # 1. Tính toán tọa độ an toàn (Vệ sĩ tránh chia cho 0)
    x, y = 0.0, 0.0
    if c != 0:
        try:
            x = (b**2 + c**2 - a**2) / (2*c)
            y = math.sqrt(max(b**2 - x**2, 0))
        except ZeroDivisionError:
            x, y = 0.0, 0.0
    else:
        # Nếu c=0, mặc định tọa độ là (0,0), (0,0), (0,0)
        x, y = 0.0, 0.0

    # 2. Khởi tạo và Lưu DB (Bất kể tam giác có xịn hay không)
    domain = TriangleDomain(
        x1 = 0, y1 = 0,
        x2 = c, y2 = 0,
        x3 = x, y3 = y,
        by = "web"
    )

    with get_session() as session:
        try:
            session.add(domain)
            session.commit()
        except Exception as e:
            session.rollback()

    # 3. Logic hiển thị giao diện (Chỗ này mới chặn người dùng xem)
    if a + b <= c or a + c <= b or b + c <= a:
        return dbc.Alert("Theo bất đẳng thức tam giác, tổng hai cạnh phải lớn hơn cạnh còn lại.", color="danger"), _draw_default()

    graph = _draw_triangle(0, 0, c, 0, x, y)
    table = _create_table(0, 0, c, 0, x, y)

    return table, graph
