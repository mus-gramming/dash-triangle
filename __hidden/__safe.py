import numpy as np



def _safe_acos(x):
    """
    Tính arc-cosine an toàn bằng cách ép giá trị đầu vào vào đoạn [-1, 1].
    Tránh lỗi NaN khi x bị sai số dấu phẩy động (ví dụ: 1.000000000001).
    """
    return np.arccos(np.clip(x, -1.0, 1.0))



def _safe_eq(a, b, eps=1e-6):
    """So sánh bằng giữa hai số thực với sai số cho phép (epsilon)."""
    return abs(a-b) < eps



def _safe_extract_to_real_num(a, b, c):
    """Biến đổi a, b, c thành số thực x = a + b*sqrt(c)"""
    return a + b * np.sqrt(c)