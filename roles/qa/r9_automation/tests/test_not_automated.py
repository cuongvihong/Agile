"""Mỗi case của R9_Test_Cases.xlsx chưa có test tự động hiện ở đây dưới dạng test bị bỏ qua kèm lý do,
để báo cáo liệt kê đủ 162 case. data/not_automated.py do tools/build_coverage.py tạo ra."""
from __future__ import annotations

import pytest

from data.not_automated import NOT_AUTOMATED

pytestmark = pytest.mark.not_automated


if NOT_AUTOMATED:
    @pytest.mark.parametrize("case_id", sorted(NOT_AUTOMATED))
    def test_not_automated(case_id):
        pytest.skip(f"{case_id}: {NOT_AUTOMATED[case_id]}")
