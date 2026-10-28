"""Metadata for all 261 test cases from R5_Test_Cases.xlsx."""
from __future__ import annotations

CASES = {'TC-001': {'id': 'TC-001',
            'scenario_id': 'TS-001',
            'title': 'Màn Upload applications hiện đúng thành phần ở trạng thái gốc',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Mở menu Financial assistance, Upload applications.\n'
                     '2. Đọc tiêu đề, phụ đề, nút, ba thẻ, ô Search, ba bộ lọc, các cột của bảng và chân bảng.',
            'expected': '1. Tiêu đề Upload applications, nhãn FUNCTION 5 · PAPER APPLICATIONS, phụ đề "Scan the signed '
                        'paper form, check what the system read, then submit it for assessment. One form is one '
                        'student."\n'
                        '2. Nút Upload scans ở góc phải.\n'
                        '3. Ba thẻ PENDING (Waiting for assessment), MOEFAS (Approved automatically), SBFAS (Decided '
                        'by school), các số đúng với hình của FS: 1, 1, 2.\n'
                        '4. Ô Search có placeholder "Search Application ID, uploaded by or EA number". Bộ lọc Status: '
                        'All, Tier: All, Uploaded: Last 7 days.\n'
                        '5. Bảng có các cột File, Uploaded by, Uploaded at, Student, Application ID, Status. Cột Tier '
                        'không có.\n'
                        '6. Chân bảng "Showing 1 to 3 of 3".',
            'review': 'Approve'},
 'TC-002': {'id': 'TC-002',
            'scenario_id': 'TS-001',
            'title': 'Ghi chú cuối trang đúng nguyên văn',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Cuộn đến cuối màn Upload applications.\n2. Đọc ghi chú dưới bảng.',
            'expected': '1. Ghi chú đọc đúng: "Student is matched by NRIC/FIN against the school\'s enrolment '
                        '(Function 3). Applications can be submitted only while a FAS application form is open. A '
                        'student who already has an application this year is blocked at submit. Drafts appear in the '
                        'list with status Draft until they are submitted."',
            'review': 'Approve'},
 'TC-003': {'id': 'TC-003',
            'scenario_id': 'TS-002',
            'title': 'Thẻ đếm đơn đã nộp của trường và không đếm bản Draft',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đọc số trên ba thẻ PENDING, MOEFAS, SBFAS.\n'
                     '2. Đếm số dòng Draft, Pending, Approved trong danh sách và trong chế độ Uploaded: Any time.',
            'expected': '1. PENDING 1, MOEFAS 1, SBFAS 2 như hình của FS.\n'
                        '2. Dòng Draft không được tính vào thẻ nào: tổng ba thẻ không đổi khi thêm hoặc bỏ một Draft.\n'
                        '3. Các thẻ không đổi khi đổi bộ lọc Uploaded.',
            'review': 'Draft'},
 'TC-004': {'id': 'TC-004',
            'scenario_id': 'TS-002',
            'title': 'Bấm thẻ PENDING lọc danh sách, bấm lần nữa bỏ lọc',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Bấm thẻ PENDING.\n2. Đọc các dòng của bảng.\n3. Bấm thẻ PENDING lần nữa.',
            'expected': '1. Sau lần bấm đầu thẻ ở trạng thái chọn và bảng chỉ có các dòng có trạng thái Pending, ở '
                        'trạng thái gốc là APP-2026-00412 Aisha Rahman.\n'
                        '2. Sau lần bấm thứ hai thẻ hết trạng thái chọn và bảng quay về 3 dòng như ban đầu.',
            'review': 'Approve'},
 'TC-005': {'id': 'TC-005',
            'scenario_id': 'TS-002',
            'title': 'Bấm thẻ SBFAS lọc các đơn SBFAS và hiện cột Tier',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Bấm thẻ SBFAS.\n2. Đọc các dòng và các cột của bảng.\n3. Bấm thẻ SBFAS lần nữa.',
            'expected': '1. Bảng chỉ có các dòng Approved · SBFAS, ở trạng thái gốc là APP-2026-00386 Lucas Teo, '
                        'Status ghi Approved SBFAS · Tier 3.\n'
                        '2. Cột Tier xuất hiện trong bảng khi lọc SBFAS và biến mất khi bỏ lọc.',
            'review': 'Approve'},
 'TC-006': {'id': 'TC-006',
            'scenario_id': 'TS-002',
            'title': 'Bấm thẻ MOEFAS lọc các đơn MOEFAS đã duyệt tự động',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đổi bộ lọc Uploaded sang Any time.\n2. Bấm thẻ MOEFAS.\n3. Đọc các dòng của bảng.',
            'expected': '1. Bảng chỉ có các đơn có Status Approved · MOEFAS, số dòng bằng số trên thẻ MOEFAS (1).\n'
                        '2. Mọi dòng hiển thị Approved MOEFAS và Application ID.',
            'review': 'Draft'},
 'TC-007': {'id': 'TC-007',
            'scenario_id': 'TS-002',
            'title': 'Thẻ không đổi khi gõ ô Search',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Gõ "Lucas" vào ô Search.\n2. Đọc ba thẻ và các dòng của bảng.',
            'expected': '1. Bảng chỉ còn dòng của Lucas Teo.\n2. Ba thẻ giữ nguyên PENDING 1, MOEFAS 1, SBFAS 2.',
            'review': 'Draft'},
 'TC-008': {'id': 'TC-008',
            'scenario_id': 'TS-003',
            'title': 'Tìm theo Application ID đầy đủ',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: APP-2026-00412',
            'steps': '1. Mở màn Upload applications.\n'
                     '2. Nhập vào ô Search: APP-2026-00412.\n'
                     '3. Đọc bảng.\n'
                     '4. Xoá ô Search.',
            'expected': '1. Bảng chỉ có APP-2026-00412 Aisha Rahman.\n2. Xoá ô Search thì bảng quay về 3 dòng.',
            'review': 'Approve'},
 'TC-009': {'id': 'TC-009',
            'scenario_id': 'TS-003',
            'title': 'Tìm theo một phần Application ID',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: 00386',
            'steps': '1. Mở màn Upload applications.\n2. Nhập vào ô Search: 00386.\n3. Đọc bảng.\n4. Xoá ô Search.',
            'expected': '1. Bảng chỉ có APP-2026-00386 Lucas Teo.',
            'review': 'Approve'},
 'TC-010': {'id': 'TC-010',
            'scenario_id': 'TS-003',
            'title': 'Tìm theo tên người tải lên',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: lan',
            'steps': '1. Mở màn Upload applications.\n2. Nhập vào ô Search: lan.\n3. Đọc bảng.\n4. Xoá ô Search.',
            'expected': '1. Cả 3 dòng hiện, vì cả ba do Lan Nguyen tải lên.',
            'review': 'Approve'},
 'TC-011': {'id': 'TC-011',
            'scenario_id': 'TS-003',
            'title': 'Tìm theo tên học sinh trong dòng Draft',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: Mei Ling',
            'steps': '1. Mở màn Upload applications.\n2. Nhập vào ô Search: Mei Ling.\n3. Đọc bảng.\n4. Xoá ô Search.',
            'expected': '1. Bảng chỉ có dòng Draft của Tan Mei Ling, Application ID là Not submitted.',
            'review': 'Approve'},
 'TC-012': {'id': 'TC-012',
            'scenario_id': 'TS-003',
            'title': 'Tìm theo số EA của học sinh',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: số EA nhìn thấy dưới tên Aisha Rahman',
            'steps': '1. Mở màn Upload applications.\n'
                     '2. Nhập vào ô Search: EA của Aisha Rahman đọc trong cột Student.\n'
                     '3. Đọc bảng.\n'
                     '4. Xoá ô Search.',
            'expected': '1. Bảng chỉ có APP-2026-00412 Aisha Rahman.',
            'review': 'Approve'},
 'TC-013': {'id': 'TC-013',
            'scenario_id': 'TS-003',
            'title': 'Tìm không có kết quả hiện thông báo trống',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: zzzz',
            'steps': '1. Nhập "zzzz" vào ô Search.\n2. Đọc bảng.',
            'expected': '1. Bảng không có dòng nào và hiện "No applications found."\n2. Không có lỗi nào khác.',
            'review': 'Draft'},
 'TC-014': {'id': 'TC-014',
            'scenario_id': 'TS-003',
            'title': 'Tìm không phân biệt chữ hoa chữ thường và cắt khoảng trắng đầu cuối',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: "  AISHA  " rồi "aisha"',
            'steps': '1. Nhập "  AISHA  " (có hai khoảng trắng mỗi đầu) vào ô Search.\n2. Đọc bảng.\n3. Nhập "aisha".',
            'expected': '1. Cả hai cách nhập đều cho cùng một kết quả: dòng APP-2026-00412 Aisha Rahman.',
            'review': 'Draft'},
 'TC-015': {'id': 'TC-015',
            'scenario_id': 'TS-003',
            'title': 'Ký tự % và _ trong Search là văn bản thường',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Search: %, _, a%o',
            'steps': '1. Nhập "%" vào ô Search và đọc bảng.\n2. Nhập "_" và đọc bảng.\n3. Nhập "a%o" và đọc bảng.',
            'expected': '1. Mỗi lần bảng không có dòng nào khớp (không phải ký tự đại diện) và hiện "No applications '
                        'found."\n'
                        '2. Không có lỗi nào.',
            'review': 'Draft'},
 'TC-016': {'id': 'TC-016',
            'scenario_id': 'TS-003',
            'title': 'Search giới hạn 100 ký tự',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Chuỗi 100 và 101 ký tự a',
            'steps': '1. Dán chuỗi 100 ký tự a vào ô Search.\n'
                     '2. Đọc ô Search và bảng.\n'
                     '3. Dán chuỗi 101 ký tự a.\n'
                     '4. Đọc ô Search và thông báo.',
            'expected': '1. Chuỗi 100 ký tự được giữ nguyên và bảng không có dòng nào khớp.\n'
                        '2. Chuỗi 101 ký tự bị cắt còn 100 ký tự và hiện "Search is limited to 100 characters."',
            'review': 'Draft'},
 'TC-017': {'id': 'TC-017',
            'scenario_id': 'TS-003',
            'title': 'Search xử lý SQL và script như văn bản',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Chuỗi SQL, script, img onerror',
            'steps': '1. Nhập "\' OR \'1\'=\'1" vào ô Search và đọc bảng.\n'
                     '2. Nhập "<script>alert(1)</script>" và đọc bảng.\n'
                     '3. Nhập "<img src=x onerror=alert(1)>" và đọc bảng.',
            'expected': '1. Mỗi lần bảng không có dòng nào (hoặc chỉ có dòng khớp đúng chuỗi) và hiện "No applications '
                        'found."\n'
                        '2. Không có hộp thoại alert, không dòng nào bị thêm hoặc xoá, không có lỗi hệ thống.\n'
                        '3. Chuỗi hiển thị trong ô Search như văn bản thường.',
            'review': 'Draft'},
 'TC-018': {'id': 'TC-018',
            'scenario_id': 'TS-004',
            'title': 'Bộ lọc Status có đủ sáu giá trị theo FS',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Mở danh sách bộ lọc Status.\n2. Đọc các giá trị và giá trị đang chọn.',
            'expected': '1. Sáu giá trị theo thứ tự: All, Draft, Pending, Approved · MOEFAS, Approved · SBFAS, '
                        'Rejected.\n'
                        '2. Giá trị mặc định là All.',
            'review': 'Approve'},
 'TC-019': {'id': 'TC-019',
            'scenario_id': 'TS-004',
            'title': 'Lọc Status Draft và Pending',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Chọn Status Draft và đọc bảng.\n2. Chọn Status Pending và đọc bảng.',
            'expected': '1. Draft chỉ cho dòng của Tan Mei Ling, Application ID Not submitted.\n'
                        '2. Pending chỉ cho APP-2026-00412 Aisha Rahman.',
            'review': 'Approve'},
 'TC-020': {'id': 'TC-020',
            'scenario_id': 'TS-004',
            'title': 'Lọc Status Approved SBFAS, Approved MOEFAS và Rejected',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Chọn Status Approved · SBFAS và đọc bảng.\n'
                     '2. Chọn Status Approved · MOEFAS và đọc bảng.\n'
                     '3. Chọn Status Rejected và đọc bảng.',
            'expected': '1. Approved · SBFAS cho APP-2026-00386 Lucas Teo và hiện cột Tier với giá trị Tier 3.\n'
                        '2. Approved · MOEFAS và Rejected không có dòng nào trong Last 7 days và hiện "No applications '
                        'found."',
            'review': 'Draft'},
 'TC-021': {'id': 'TC-021',
            'scenario_id': 'TS-004',
            'title': 'Bộ lọc Tier liệt kê tier SBFAS của trường và lọc đúng',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Mở bộ lọc Tier và đọc các giá trị.\n2. Chọn Tier 3 và đọc bảng.',
            'expected': '1. Các giá trị gồm All và các tier SBFAS của Bukit View Primary.\n'
                        '2. Với Tier 3 bảng chỉ có APP-2026-00386 Lucas Teo và cột Tier hiện với giá trị Tier 3.',
            'review': 'Approve'},
 'TC-022': {'id': 'TC-022',
            'scenario_id': 'TS-004',
            'title': 'Bộ lọc Uploaded có ba giá trị và mặc định Last 7 days',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Mở màn Upload applications.\n2. Đọc giá trị của bộ lọc Uploaded và mở danh sách giá trị.',
            'expected': '1. Giá trị mặc định là Last 7 days.\n2. Ba giá trị: Last 7 days, Last 30 days, Any time.',
            'review': 'Approve'},
 'TC-023': {'id': 'TC-023',
            'scenario_id': 'TS-004',
            'title': 'Search, Status, Tier và Uploaded kết hợp bằng AND',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Status Approved · SBFAS, Search Teo rồi Aisha',
            'steps': '1. Chọn Status Approved · SBFAS và nhập "Teo" vào Search.\n'
                     '2. Đọc bảng.\n'
                     '3. Đổi Search thành "Aisha" giữ Status.\n'
                     '4. Đọc bảng.',
            'expected': '1. Bước 2: có dòng của Lucas Teo.\n'
                        '2. Bước 4: không có dòng nào, hiện "No applications found."',
            'review': 'Draft'},
 'TC-024': {'id': 'TC-024',
            'scenario_id': 'TS-004',
            'title': 'Uploaded Any time hiện thêm các đơn cũ',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Chọn Uploaded Any time.\n2. Đếm số dòng đã nộp theo từng trạng thái.',
            'expected': '1. Số dòng Approved · MOEFAS và Approved · SBFAS bằng số trên thẻ MOEFAS và SBFAS (1 và 2).\n'
                        '2. Dòng Pending vẫn là 1 và có đúng 1 dòng Draft.',
            'review': 'Draft'},
 'TC-025': {'id': 'TC-025',
            'scenario_id': 'TS-005',
            'title': 'Dòng Draft đứng đầu danh sách với Application ID Not submitted',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đọc dòng đầu của bảng ở Status All.',
            'expected': '1. Dòng Draft của Tan Mei Ling đứng trước các dòng đã nộp.\n'
                        '2. Application ID là Not submitted, Status là Draft (nhãn vàng), Student là tên con kèm NRIC '
                        'T1412345B.',
            'review': 'Approve'},
 'TC-026': {'id': 'TC-026',
            'scenario_id': 'TS-005',
            'title': 'Dòng Draft có nút Continue và Delete',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đọc dòng Draft và tìm hai nút.',
            'expected': '1. Dòng Draft có nút Continue và nút Delete.',
            'review': 'Draft'},
 'TC-027': {'id': 'TC-027',
            'scenario_id': 'TS-005',
            'title': 'Bấm vào dòng Draft tiếp tục bản nháp',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Bấm vào dòng Draft (không bấm vào nút).',
            'expected': '1. Màn Review application mở với mẫu đơn của bản nháp, các giá trị đã lưu có mặt.',
            'review': 'Approve'},
 'TC-028': {'id': 'TC-028',
            'scenario_id': 'TS-005',
            'title': 'Bấm dòng đã nộp mở View application chỉ đọc có nút Back to list',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Bấm dòng APP-2026-00412 Aisha Rahman.\n'
                     '2. Đọc màn hình, thử gõ vào một ô.\n'
                     '3. Bấm Back to list.',
            'expected': '1. View application mở, cùng mẫu đơn nhưng mọi ô chỉ đọc.\n'
                        '2. Có nút Back to list và nút Edit vì đơn đang Pending.\n'
                        '3. Back to list quay về danh sách Upload applications.',
            'review': 'Approve'},
 'TC-029': {'id': 'TC-029',
            'scenario_id': 'TS-006',
            'title': 'Last 7 days gồm đúng đơn tải lên 7 ngày trước, loại đơn tải lên 8 ngày trước',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Có hai đơn tải lên 11/10/2026 và 10/10/2026.',
            'test_data': 'SEED-R5-30: hai đơn của trường Bukit View Primary tải lên 11/10/2026 và 10/10/2026',
            'steps': '1. Với Uploaded Last 7 days, tìm hai dòng thử.\n2. Chọn Last 30 days và đọc bảng.',
            'expected': '1. Dòng tải lên ngày 11/10/2026 (7 ngày trước 18/10/2026) có trong Last 7 days.\n'
                        '2. Dòng tải lên ngày 10/10/2026 không có trong Last 7 days và có trong Last 30 days.',
            'review': 'Draft'},
 'TC-030': {'id': 'TC-030',
            'scenario_id': 'TS-006',
            'title': 'Draft đứng đầu, dòng đã nộp mới nhất trước và 10 dòng mỗi trang',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Trường có 11 đơn đã nộp và 1 Draft.',
            'test_data': 'SEED-R5-31: 11 đơn đã nộp của Bukit View Primary',
            'steps': '1. Mở danh sách với Uploaded Any time.\n'
                     '2. Đọc thứ tự và số dòng của trang 1.\n'
                     '3. Sang trang 2 và đọc.',
            'expected': '1. Draft đứng đầu, các dòng đã nộp theo Uploaded at mới nhất trước.\n'
                        '2. Trang 1 có 10 dòng, trang 2 có 1 dòng, chân bảng ghi Showing 11 to 11 of 11.',
            'review': 'Draft'},
 'TC-031': {'id': 'TC-031',
            'scenario_id': 'TS-006',
            'title': 'Đổi bộ lọc về trang 1',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Trường có 11 đơn đã nộp và đang ở trang 2.',
            'test_data': 'SEED-R5-31',
            'steps': '1. Ở trang 2 chọn Status Pending.',
            'expected': '1. Bảng quay về trang 1 với các dòng khớp bộ lọc.',
            'review': 'Draft'},
 'TC-032': {'id': 'TC-032',
            'scenario_id': 'TS-006',
            'title': 'Uploaded at hiển thị DD/MM/YYYY HH:mm giờ Singapore',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đọc cột Uploaded at của các dòng.',
            'expected': '1. Mỗi giá trị theo dạng DD/MM/YYYY HH:mm, giờ Singapore, ví dụ 17/10/2026 09:12.',
            'review': 'Draft'},
 'TC-033': {'id': 'TC-033',
            'scenario_id': 'TS-007',
            'title': 'School user chỉ thấy đơn của học sinh trường mình',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đăng xuất, đăng nhập School user MRS-0012 Farah Tan.\n'
                     '2. Mở Upload applications với Uploaded Any time.\n'
                     '3. Đọc các dòng và ba thẻ.',
            'expected': '1. Không có dòng nào của Aisha Rahman, Lucas Teo, Tan Mei Ling hay bất kỳ học sinh nào của '
                        'Bukit View Primary.\n'
                        '2. Các thẻ phản ánh đơn của Meridian Secondary.',
            'review': 'Approve'},
 'TC-034': {'id': 'TC-034',
            'scenario_id': 'TS-007',
            'title': 'MOE HQ không truy cập được Upload applications',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n2. Đăng nhập MOE HQ Mei Lin Tan.',
            'test_data': 'Trạng thái gốc của prototype: 1 Draft, 1 Pending APP-2026-00412 Aisha Rahman, 1 Approved '
                         'SBFAS Tier 3 APP-2026-00386 Lucas Teo',
            'steps': '1. Đăng nhập MOE HQ Mei Lin Tan.\n'
                     '2. Tìm mục Upload applications trong menu.\n'
                     '3. Mở địa chỉ của màn Upload applications bằng cách gõ trực tiếp.',
            'expected': '1. Menu của MOE HQ không có mục Upload applications.\n'
                        '2. Mở trực tiếp bị từ chối, không có dữ liệu nào hiển thị.',
            'review': 'Approve'},
 'TC-035': {'id': 'TC-035',
            'scenario_id': 'TS-007',
            'title': 'Đơn của con học trường khác hiện ở danh sách của trường con',
            'suite': 'F5.1 Upload applications list',
            'page': 'Upload applications (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'SEED-R5: Tan Mei Ling T1412345B (P6, BVP), Tan Jun Kai T1012345A (S4, MRS)',
            'steps': '1. Với BVP-0012 nộp mẫu có hai con Tan Mei Ling (Bukit View Primary) và Tan Jun Kai (Meridian '
                     'Secondary).\n'
                     '2. Mở Upload applications của Bukit View Primary với Uploaded Any time.\n'
                     '3. Đăng xuất, đăng nhập MRS-0012 Farah Tan và mở Upload applications.',
            'expected': '1. Bukit View Primary thấy đơn của Tan Mei Ling và không thấy đơn của Tan Jun Kai.\n'
                        '2. Meridian Secondary thấy đơn của Tan Jun Kai và không thấy đơn của Tan Mei Ling.',
            'review': 'Draft'},
 'TC-036': {'id': 'TC-036',
            'scenario_id': 'TS-008',
            'title': 'Hộp thoại mở với danh sách file trống và Upload and read tắt',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Bấm Upload scans.\n2. Đọc hộp thoại.',
            'expected': '1. Hộp thoại Upload scans mở, danh sách file trống.\n'
                        '2. Nút Upload and read tắt, nút Cancel bật.',
            'review': 'Approve'},
 'TC-037': {'id': 'TC-037',
            'scenario_id': 'TS-008',
            'title': 'Cancel đóng hộp thoại và không tải gì',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'File: scan_bvp_0667.pdf 812 KB',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm file scan_bvp_0667.pdf.\n'
                     '3. Bấm Cancel.\n'
                     '4. Đọc danh sách Upload applications.\n'
                     '5. Bấm Upload scans lần nữa.',
            'expected': '1. Hộp thoại đóng, danh sách đơn không đổi và không có dòng Draft mới.\n'
                        '2. Hộp thoại mở lại với danh sách file trống.',
            'review': 'Approve'},
 'TC-038': {'id': 'TC-038',
            'scenario_id': 'TS-008',
            'title': 'Bấm đúp Upload scans chỉ mở một hộp thoại',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Bấm đúp nhanh vào Upload scans.\n2. Đọc màn hình.',
            'expected': '1. Chỉ có một hộp thoại Upload scans.',
            'review': 'Approve'},
 'TC-039': {'id': 'TC-039',
            'scenario_id': 'TS-009',
            'title': 'PDF, JPG và PNG đều được nhận',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'a.pdf 812 KB, b.jpg 600 KB, c.png 300 KB',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm lần lượt a.pdf, b.jpg, c.png.\n'
                     '3. Đọc danh sách file và nút Upload and read.',
            'expected': '1. Cả ba file nằm trong danh sách, mỗi dòng có tên file, dung lượng và nút Remove.\n'
                        '2. Nút Upload and read bật.\n'
                        '3. Không có thông báo lỗi.',
            'review': 'Approve'},
 'TC-040': {'id': 'TC-040',
            'scenario_id': 'TS-009',
            'title': 'File .docx bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'File: form.docx',
            'steps': '1. Bấm Upload scans.\n2. Thêm file form.docx.\n3. Đọc danh sách file và thông báo.',
            'expected': '1. File không vào danh sách.\n'
                        '2. Thông báo "form.docx: only PDF, JPG or PNG files."\n'
                        '3. Nút Upload and read vẫn tắt.',
            'review': 'Approve'},
 'TC-041': {'id': 'TC-041',
            'scenario_id': 'TS-009',
            'title': 'Các loại file khác bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'photo.gif, scan.tiff, notes.txt, run.exe, pic.heic',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm lần lượt photo.gif, scan.tiff, notes.txt, run.exe, pic.heic.\n'
                     '3. Đọc thông báo sau mỗi lần thêm.',
            'expected': '1. Mỗi file bị từ chối với "{tên file}: only PDF, JPG or PNG files." và không vào danh sách.\n'
                        '2. Nút Upload and read vẫn tắt.',
            'review': 'Approve'},
 'TC-042': {'id': 'TC-042',
            'scenario_id': 'TS-009',
            'title': 'Phần mở rộng viết hoa vẫn được nhận',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'FORM.PDF, PHOTO.JPG, SCAN.PNG',
            'steps': '1. Bấm Upload scans.\n2. Thêm FORM.PDF, PHOTO.JPG, SCAN.PNG.\n3. Đọc danh sách.',
            'expected': '1. Cả ba file vào danh sách, không có thông báo lỗi.',
            'review': 'Draft'},
 'TC-043': {'id': 'TC-043',
            'scenario_id': 'TS-009',
            'title': 'Phần mở rộng jpeg được coi là JPG',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'photo.jpeg',
            'steps': '1. Bấm Upload scans.\n2. Thêm photo.jpeg.\n3. Đọc danh sách.',
            'expected': '1. File vào danh sách, không có thông báo lỗi.',
            'review': 'Draft'},
 'TC-044': {'id': 'TC-044',
            'scenario_id': 'TS-009',
            'title': 'File đổi tên phần mở rộng bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'payload.pdf (exe), form.pdf.exe, notes.pdf (text)',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm payload.pdf (thực ra là file .exe đã đổi tên).\n'
                     '3. Thêm form.pdf.exe.\n'
                     '4. Thêm notes.txt đổi tên thành notes.pdf.\n'
                     '5. Đọc thông báo sau mỗi lần thêm.',
            'expected': '1. Cả ba file bị từ chối với "{tên file}: only PDF, JPG or PNG files." và không vào danh '
                        'sách.',
            'review': 'Draft'},
 'TC-045': {'id': 'TC-045',
            'scenario_id': 'TS-010',
            'title': 'File 5 MB được nhận',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'big5.pdf, 5 MB',
            'steps': '1. Bấm Upload scans.\n2. Thêm file big5.pdf dung lượng 5 MB.',
            'expected': '1. File vào danh sách và dòng hiện dung lượng khoảng 5 MB.\n2. Không có thông báo lỗi.',
            'review': 'Approve'},
 'TC-046': {'id': 'TC-046',
            'scenario_id': 'TS-010',
            'title': 'File 11 MB bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'big11.pdf, 11 MB',
            'steps': '1. Bấm Upload scans.\n2. Thêm file big11.pdf dung lượng 11 MB.',
            'expected': '1. File không vào danh sách.\n2. Thông báo "big11.pdf is larger than 10 MB."',
            'review': 'Approve'},
 'TC-047': {'id': 'TC-047',
            'scenario_id': 'TS-010',
            'title': 'Biên 10 MB: đúng 10 MB được nhận, 10 MB cộng 1 byte bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'exact10.pdf 10.485.760 byte, over10.pdf 10.485.761 byte',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm file exact10.pdf dung lượng 10.485.760 byte.\n'
                     '3. Thêm file over10.pdf dung lượng 10.485.761 byte.\n'
                     '4. Đọc danh sách và thông báo.',
            'expected': '1. exact10.pdf vào danh sách.\n'
                        '2. over10.pdf bị từ chối với "over10.pdf is larger than 10 MB."',
            'review': 'Draft'},
 'TC-048': {'id': 'TC-048',
            'scenario_id': 'TS-010',
            'title': 'File 0 byte bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'empty.pdf, 0 byte',
            'steps': '1. Bấm Upload scans.\n2. Thêm file empty.pdf dung lượng 0 byte.',
            'expected': '1. File không vào danh sách và hiện "empty.pdf: the file is empty."',
            'review': 'Draft'},
 'TC-049': {'id': 'TC-049',
            'scenario_id': 'TS-011',
            'title': 'Thêm đủ 5 file được nhận',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf đến p5.pdf, mỗi file 1 MB',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm lần lượt p1.pdf, p2.pdf, p3.pdf, p4.pdf, p5.pdf.\n'
                     '3. Đọc danh sách.',
            'expected': '1. Cả 5 file nằm trong danh sách.\n2. Nút Upload and read bật, không có thông báo lỗi.',
            'review': 'Approve'},
 'TC-050': {'id': 'TC-050',
            'scenario_id': 'TS-011',
            'title': 'File thứ 6 bị từ chối',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf đến p6.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm p1.pdf đến p5.pdf.\n'
                     '3. Thêm p6.pdf.\n'
                     '4. Đọc danh sách và thông báo.',
            'expected': '1. p6.pdf không vào danh sách, danh sách vẫn có 5 file.\n'
                        '2. Thông báo "Up to 5 files per application."',
            'review': 'Approve'},
 'TC-051': {'id': 'TC-051',
            'scenario_id': 'TS-011',
            'title': 'Chọn 6 file một lần chỉ nhận 5 file đầu',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf đến p6.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Chọn đồng thời p1.pdf đến p6.pdf trong hộp chọn file.\n'
                     '3. Đọc danh sách và thông báo.',
            'expected': '1. 5 file đầu vào danh sách, file thứ 6 bị từ chối.\n'
                        '2. Thông báo "Up to 5 files per application."',
            'review': 'Draft'},
 'TC-052': {'id': 'TC-052',
            'scenario_id': 'TS-011',
            'title': 'Bỏ một file bằng Remove rồi thêm file khác',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf đến p6.pdf',
            'steps': '1. Bấm Upload scans.\n2. Thêm p1.pdf đến p5.pdf.\n3. Bấm Remove ở dòng p3.pdf.\n4. Thêm p6.pdf.',
            'expected': '1. Sau Remove danh sách còn 4 file, không còn p3.pdf.\n'
                        '2. p6.pdf vào danh sách, tổng 5 file và không có thông báo lỗi.',
            'review': 'Approve'},
 'TC-053': {'id': 'TC-053',
            'scenario_id': 'TS-011',
            'title': 'Bỏ file cuối cùng thì Upload and read tắt',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf',
            'steps': '1. Bấm Upload scans.\n2. Thêm p1.pdf.\n3. Bấm Remove ở dòng p1.pdf.',
            'expected': '1. Danh sách trống và nút Upload and read tắt.',
            'review': 'Approve'},
 'TC-054': {'id': 'TC-054',
            'scenario_id': 'TS-011',
            'title': 'File hợp lệ và file lỗi trong cùng một lần chọn',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'a.pdf, b.docx, c.png',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Chọn đồng thời a.pdf, b.docx, c.png trong hộp chọn file.\n'
                     '3. Đọc danh sách và thông báo.',
            'expected': '1. a.pdf và c.png vào danh sách.\n'
                        '2. b.docx bị từ chối với "b.docx: only PDF, JPG or PNG files."\n'
                        '3. Nút Upload and read bật.',
            'review': 'Draft'},
 'TC-055': {'id': 'TC-055',
            'scenario_id': 'TS-011',
            'title': 'Thêm cùng một file hai lần',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'a.pdf',
            'steps': '1. Bấm Upload scans.\n2. Thêm a.pdf.\n3. Thêm lại đúng file a.pdf.',
            'expected': '1. Danh sách vẫn có một file a.pdf.\n2. Thông báo "a.pdf is already added."',
            'review': 'Draft'},
 'TC-056': {'id': 'TC-056',
            'scenario_id': 'TS-012',
            'title': 'Upload and read mở màn Review application với các giá trị đọc được',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'scan_bvp_0667.pdf 812 KB',
            'steps': '1. Bấm Upload scans.\n2. Thêm scan_bvp_0667.pdf.\n3. Bấm Upload and read.\n4. Đọc màn hình.',
            'expected': '1. Màn Review application mở, khung bên trái hiển thị bản scan, bên phải có Part 1 đến Part '
                        '5.\n'
                        '2. Các trường mà trình đọc không chắc chắn được tô vàng.\n'
                        '3. Các nút Discard, Save draft, Review and submit hiện ở đầu trang.',
            'review': 'Approve'},
 'TC-057': {'id': 'TC-057',
            'scenario_id': 'TS-012',
            'title': 'Bấm đúp Upload and read chỉ tải và đọc một lần',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'scan_bvp_0667.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm scan_bvp_0667.pdf.\n'
                     '3. Bấm đúp nhanh vào Upload and read.\n'
                     '4. Đóng màn Review application bằng Discard.\n'
                     '5. Đọc danh sách.',
            'expected': '1. Chỉ có một màn Review application.\n2. Sau Discard danh sách đơn không có dòng thừa.',
            'review': 'Draft'},
 'TC-058': {'id': 'TC-058',
            'scenario_id': 'TS-012',
            'title': 'Tải đủ 5 file là một mẫu đơn',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'p1.pdf đến p5.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm p1.pdf đến p5.pdf.\n'
                     '3. Bấm Upload and read.\n'
                     '4. Đọc khung bản scan.',
            'expected': '1. Khung bên trái cho xem đủ 5 trang scan của một mẫu.\n'
                        '2. Chỉ có một màn Review application, không có nhiều mẫu.',
            'review': 'Draft'},
 'TC-059': {'id': 'TC-059',
            'scenario_id': 'TS-012',
            'title': 'Lời nhắc trong hộp thoại phù hợp với mẫu nhiều con',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Bấm Upload scans.\n2. Đọc dòng nhắc trong hộp thoại.',
            'expected': '1. Dòng nhắc không nói mỗi lần tải chỉ cho một học sinh, vì một mẫu có thể có nhiều con.',
            'review': 'Draft'},
 'TC-060': {'id': 'TC-060',
            'scenario_id': 'TS-012',
            'title': 'Đọc scan lỗi: file mã hoá mật khẩu',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-06',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'locked.pdf (mã hoá mật khẩu)',
            'steps': '1. Bấm Upload scans.\n2. Thêm locked.pdf.\n3. Bấm Upload and read.\n4. Đọc màn hình.',
            'expected': '1. Hộp thoại giữ mở và file giữ nguyên trong danh sách.\n'
                        '2. Hiện "Something went wrong. Please try again."\n'
                        '3. Không mở màn Review application, không có dòng Draft.',
            'review': 'Draft'},
 'TC-061': {'id': 'TC-061',
            'scenario_id': 'TS-012',
            'title': 'Đọc scan lỗi: file hỏng và trang trắng',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-06',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'corrupt.pdf, blank.png',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm corrupt.pdf (hỏng) và bấm Upload and read.\n'
                     '3. Đọc màn hình.\n'
                     '4. Bỏ file, thêm blank.png (trang trắng) và bấm Upload and read.\n'
                     '5. Đọc màn hình.',
            'expected': '1. Cả hai lần: hộp thoại giữ mở, hiện "Something went wrong. Please try again."\n'
                        '2. Không có dòng Draft và không có màn Review application chứa dữ liệu sai.',
            'review': 'Draft'},
 'TC-062': {'id': 'TC-062',
            'scenario_id': 'TS-012',
            'title': 'Lỗi máy chủ khi đọc scan',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'scan_bvp_0667.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm scan_bvp_0667.pdf.\n'
                     '3. Cho dịch vụ đọc scan trả lỗi rồi bấm Upload and read.',
            'expected': '1. Hộp thoại giữ mở, file giữ nguyên.\n'
                        '2. Hiện "Something went wrong. Please try again."\n'
                        '3. Không tạo Draft hay đơn nào.',
            'review': 'Draft'},
 'TC-063': {'id': 'TC-063',
            'scenario_id': 'TS-012',
            'title': 'Đóng hộp thoại khi đang đọc scan',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'scan_bvp_0667.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm scan_bvp_0667.pdf.\n'
                     '3. Bấm Upload and read.\n'
                     '4. Bấm Cancel hoặc Esc ngay khi đang đọc.\n'
                     '5. Đọc danh sách.',
            'expected': '1. Hộp thoại đóng và không có màn Review application hiện sau đó.\n'
                        '2. Không có dòng Draft hay đơn nào được tạo.',
            'review': 'Draft'},
 'TC-064': {'id': 'TC-064',
            'scenario_id': 'TS-013',
            'title': 'Tên file Unicode, có khoảng trắng và dài 255 ký tự',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '"đơn xin trợ cấp 2026.pdf", tên 255 ký tự',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm file "đơn xin trợ cấp 2026.pdf".\n'
                     '3. Thêm file có tên 251 ký tự a cộng ".pdf" (255 ký tự).\n'
                     '4. Đọc danh sách.',
            'expected': '1. Cả hai file vào danh sách, tên hiển thị đúng như văn bản.',
            'review': 'Draft'},
 'TC-065': {'id': 'TC-065',
            'scenario_id': 'TS-013',
            'title': 'Tên file chứa mã hiển thị như văn bản',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01, ENV-R5-06',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '<img src=x onerror=alert(1)>.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm file có tên "<img src=x onerror=alert(1)>.pdf".\n'
                     '3. Đọc danh sách và bấm Upload and read.',
            'expected': '1. Tên hiển thị đúng như văn bản trong danh sách, không có alert và không dựng thành thẻ.\n'
                        '2. Tên được mã hoá an toàn ở màn Review application.',
            'review': 'Draft'},
 'TC-066': {'id': 'TC-066',
            'scenario_id': 'TS-013',
            'title': 'Đường dẫn trong tên file bị loại bỏ khi lưu',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-06',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': '../../etc/passwd.pdf',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm file có tên "../../etc/passwd.pdf".\n'
                     '3. Bấm Upload and read và hoàn tất lưu nháp.\n'
                     '4. Kiểm tra tên file lưu trên máy chủ.',
            'expected': '1. File không ghi ra ngoài thư mục lưu trữ của F5.\n'
                        '2. Tên lưu do máy chủ đặt, phần ../ không có tác dụng.',
            'review': 'Draft'},
 'TC-067': {'id': 'TC-067',
            'scenario_id': 'TS-013',
            'title': 'PDF có JavaScript không chạy khi đọc và khi xem',
            'suite': 'F5.2 Upload scans dialog',
            'page': 'Upload scans dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-06',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'active.pdf (JavaScript, OpenAction)',
            'steps': '1. Bấm Upload scans.\n'
                     '2. Thêm active.pdf có JavaScript và hành động mở khi tải.\n'
                     '3. Bấm Upload and read và xem bản scan ở khung bên trái.',
            'expected': '1. Không có mã nào chạy, không hộp thoại, không mở tài nguyên ngoài.\n'
                        '2. Bản scan hiển thị như hình tĩnh.',
            'review': 'Draft'},
 'TC-068': {'id': 'TC-068',
            'scenario_id': 'TS-014',
            'title': 'Nhập NRIC người khai thì tự điền các trường của Part 1',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Gõ S7612345A vào ô NRIC của Part 1.\n'
                     '2. Rời ô NRIC (bấm Tab) hoặc bấm Enter.\n'
                     '3. Đọc các trường của Part 1.',
            'expected': '1. Full name Tan Wei Ming, Date of birth theo hồ sơ dạng DD/MM/YYYY, Gender Male, Category '
                        'Singapore Citizen, Nationality Chinese.\n'
                        '2. Phone number, Email wm.tan@example.com và Address (bắt đầu Blk 123 Bukit Batok St 21) được '
                        'điền từ hồ sơ.\n'
                        '3. Các ô tự điền chuyển sang nền xám (khoá).\n'
                        '4. Relationship to child giữ giá trị đọc từ mẫu đơn (Father), School-based FAS giữ mặc định '
                        'Yes.',
            'review': 'Approve'},
 'TC-069': {'id': 'TC-069',
            'scenario_id': 'TS-014',
            'title': 'Nhập NRIC bằng chữ thường được đổi thành chữ hoa và vẫn tự điền',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'NRIC gõ: s7612345a',
            'steps': '1. Gõ s7612345a vào ô NRIC.\n2. Rời ô NRIC.',
            'expected': '1. Ô NRIC hiển thị S7612345A.\n2. Part 1 được tự điền như với S7612345A.',
            'review': 'Draft'},
 'TC-070': {'id': 'TC-070',
            'scenario_id': 'TS-014',
            'title': 'Khoảng trắng đầu cuối quanh NRIC bị cắt',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'NRIC gõ: "  S7612345A  "',
            'steps': '1. Gõ "  S7612345A  " (hai khoảng trắng mỗi đầu) vào ô NRIC.\n2. Rời ô NRIC.',
            'expected': '1. Ô NRIC là S7612345A và Part 1 được tự điền.',
            'review': 'Draft'},
 'TC-071': {'id': 'TC-071',
            'scenario_id': 'TS-014',
            'title': 'Category Singapore PR, International ASEAN và non ASEAN tự điền đúng',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'SEED-R5-01 Priya Nair S7403219B\n'
                         'SEED-R5-02 Nguyen Thi Hoa F2214680R\n'
                         'SEED-R5-03 Daniel Okoro F3358024W',
            'steps': '1. Gõ lần lượt ba NRIC người khai vào ô NRIC, mỗi lần rời ô và đọc Category.',
            'expected': '1. Priya Nair cho Singapore PR.\n'
                        '2. Nguyen Thi Hoa cho International ASEAN.\n'
                        '3. Daniel Okoro cho International non ASEAN.\n'
                        '4. Mỗi lần các ô tự điền chuyển sang nền xám.',
            'review': 'Approve'},
 'TC-072': {'id': 'TC-072',
            'scenario_id': 'TS-014',
            'title': 'Nationality hiện đủ năm giá trị theo hồ sơ',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'SEED-R5-04 Siti Noor S8205501J Malay\n'
                         'SEED-R5-05 Grace Pereira S7706633J Eurasian\n'
                         'SEED-R5-06 Ravi Kumar S7907712G Indian\n'
                         'SEED-R5-07 Karen Lee S8001126A Others\n'
                         'Tan Wei Ming S7612345A Chinese',
            'steps': '1. Gõ lần lượt năm NRIC người khai vào ô NRIC và đọc Nationality.',
            'expected': '1. Nationality hiện lần lượt Malay, Eurasian, Indian, Others, Chinese đúng theo hồ sơ.',
            'review': 'Approve'},
 'TC-073': {'id': 'TC-073',
            'scenario_id': 'TS-014',
            'title': 'Đổi NRIC sau khi đã tự điền thay toàn bộ giá trị tự điền',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'S7612345A rồi S8205501J',
            'steps': '1. Gõ S7612345A, rời ô, đổi Relationship thành Mother và bỏ chọn School-based FAS.\n'
                     '2. Đổi NRIC người khai sang S8205501J.\n'
                     '3. Đọc Part 1.',
            'expected': '1. Họ tên, ngày sinh, giới tính, category, nationality, điện thoại, email, địa chỉ chuyển '
                        'sang giá trị của NRIC mới.\n'
                        '2. Relationship to child giữ Mother và School-based FAS giữ trạng thái đã bỏ chọn.',
            'review': 'Draft'},
 'TC-074': {'id': 'TC-074',
            'scenario_id': 'TS-014',
            'title': 'NRIC người khai không có trong hồ sơ',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'NRIC S8700111C không có trong hồ sơ',
            'steps': '1. Gõ NRIC S8700111C (cấu trúc đúng, không có trong hồ sơ phụ huynh và dữ liệu Chính phủ).\n'
                     '2. Rời ô NRIC.\n'
                     '3. Đọc Part 1.',
            'expected': '1. Không có kết quả xác định trong FS.',
            'review': 'Block'},
 'TC-075': {'id': 'TC-075',
            'scenario_id': 'TS-014',
            'title': 'Hồ sơ phụ huynh lỗi thì không tự điền',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Cho hồ sơ phụ huynh trả lỗi.\n2. Gõ S7612345A và rời ô.',
            'expected': '1. Hiện "Something went wrong. Please try again."\n'
                        '2. Các trường của Part 1 không bị điền giá trị nửa chừng.\n'
                        '3. Màn Review application và dữ liệu đã nhập khác không mất.',
            'review': 'Draft'},
 'TC-076': {'id': 'TC-076',
            'scenario_id': 'TS-015',
            'title': 'Các ô tự điền khoá không sửa được',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Bấm vào từng ô Full name, Date of birth, Gender, Category, Nationality.\n'
                     '2. Thử gõ và dán giá trị khác vào từng ô.\n'
                     '3. Thử mở danh sách chọn của Gender, Category, Nationality.',
            'expected': '1. Không ô nào nhận thay đổi, nền ô vẫn xám và giá trị giữ nguyên.\n'
                        '2. Danh sách chọn không mở.',
            'review': 'Approve'},
 'TC-077': {'id': 'TC-077',
            'scenario_id': 'TS-015',
            'title': 'Phone, Email và Address khoá sau khi tự điền',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Bấm vào Phone number, Email, Address.\n2. Thử gõ giá trị khác vào từng ô.',
            'expected': '1. Cả ba ô không nhận thay đổi và nền ô xám.',
            'review': 'Draft'},
 'TC-078': {'id': 'TC-078',
            'scenario_id': 'TS-015',
            'title': 'Relationship to child và School-based FAS luôn sửa được',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Đổi Relationship to child từ Father sang Mother.\n2. Bỏ chọn School-based FAS rồi chọn lại.',
            'expected': '1. Hai ô nhận thay đổi, nền trắng.\n2. Giá trị mới được giữ khi bấm Save draft rồi Continue.',
            'review': 'Draft'},
 'TC-079': {'id': 'TC-079',
            'scenario_id': 'TS-016',
            'title': 'NRIC người khai sai độ dài bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'Dưới 9 ký tự: S761234A\nTrên 9 ký tự: S7612345AB\nChỉ 1 chữ cái: S',
            'steps': '1. Gõ lần lượt từng giá trị trong Test Data vào ô NRIC người khai.\n'
                     '2. Rời ô NRIC rồi bấm Review and submit.\n'
                     '3. Đọc các ghi chú đỏ và màn hình, xoá ô NRIC trước khi thử giá trị kế tiếp.',
            'expected': '1. Mỗi lần hộp thoại Review before submitting không mở.\n'
                        '2. Ô NRIC báo hoặc ghi chú đỏ ở đầu trang có "Enter a valid NRIC/FIN."\n'
                        '3. Part 1 không được tự điền.',
            'review': 'Draft'},
 'TC-080': {'id': 'TC-080',
            'scenario_id': 'TS-016',
            'title': 'NRIC người khai sai cấu trúc bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'A7612345A (chữ cái đầu không phải S, T, F, G)\n'
                         'S76123456 (số ở vị trí chữ cái cuối)\n'
                         'S76A2345A (chữ cái trong phần chữ số)\n'
                         'M1234567K (chữ cái đầu M)',
            'steps': '1. Gõ lần lượt từng giá trị trong Test Data vào ô NRIC người khai.\n'
                     '2. Rời ô NRIC rồi bấm Review and submit.\n'
                     '3. Đọc các ghi chú đỏ và màn hình, xoá ô NRIC trước khi thử giá trị kế tiếp.',
            'expected': '1. Mỗi lần không mở hộp thoại Review before submitting.\n'
                        '2. Hiện "Enter a valid NRIC/FIN." và Part 1 không được tự điền.',
            'review': 'Draft'},
 'TC-081': {'id': 'TC-081',
            'scenario_id': 'TS-016',
            'title': 'NRIC người khai có khoảng trắng ở giữa bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'S761 2345A\nS7612 345A',
            'steps': '1. Gõ lần lượt từng giá trị trong Test Data vào ô NRIC người khai.\n'
                     '2. Rời ô NRIC rồi bấm Review and submit.\n'
                     '3. Đọc các ghi chú đỏ và màn hình, xoá ô NRIC trước khi thử giá trị kế tiếp.',
            'expected': '1. Mỗi lần hiện "Enter a valid NRIC/FIN." và hộp thoại Review before submitting không mở.',
            'review': 'Draft'},
 'TC-082': {'id': 'TC-082',
            'scenario_id': 'TS-016',
            'title': 'NRIC người khai có SQL, script và ký tự đặc biệt bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': "S7612345A' OR '1'='1\n"
                         '<script>alert(1)</script>\n'
                         '{"a":1}\n'
                         '../../etc/passwd\n'
                         'S7612345A;DROP TABLE x',
            'steps': '1. Gõ lần lượt từng giá trị trong Test Data vào ô NRIC người khai.\n'
                     '2. Rời ô NRIC rồi bấm Review and submit.\n'
                     '3. Đọc các ghi chú đỏ và màn hình, xoá ô NRIC trước khi thử giá trị kế tiếp.',
            'expected': '1. Mỗi lần hiện "Enter a valid NRIC/FIN." và không alert, không lỗi hệ thống.\n'
                        '2. Giá trị hiển thị như văn bản thường và không bao giờ tới câu truy vấn.',
            'review': 'Draft'},
 'TC-083': {'id': 'TC-083',
            'scenario_id': 'TS-016',
            'title': 'Chữ cái kiểm tra cuối sai vẫn được nhận',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'NRIC gõ: S7612345Z',
            'steps': '1. Gõ S7612345Z (chữ cái đúng theo thuật toán công khai là D) vào ô NRIC.\n2. Rời ô NRIC.',
            'expected': '1. Máy chủ chỉ kiểm cấu trúc nên giá trị được nhận và tra hồ sơ như bình thường (không có '
                        'thông báo định dạng).',
            'review': 'Draft'},
 'TC-084': {'id': 'TC-084',
            'scenario_id': 'TS-017',
            'title': 'Số điện thoại chỉ nhận chữ số',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': 'Gõ: ab12-34 5+6',
            'steps': '1. Xoá ô Phone number rồi gõ "ab12-34 5+6".\n2. Đọc giá trị trong ô.',
            'expected': '1. Chỉ còn các chữ số 123456; chữ cái, dấu gạch, khoảng trắng và dấu cộng không vào ô.',
            'review': 'Draft'},
 'TC-085': {'id': 'TC-085',
            'scenario_id': 'TS-017',
            'title': 'Dán số điện thoại có dấu cộng và khoảng trắng',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': 'Dán: +65 9123 4567',
            'steps': '1. Dán "+65 9123 4567" vào ô Phone number.',
            'expected': '1. Ô hiển thị 6591234567 (10 chữ số).\n2. Review and submit không báo lỗi điện thoại.',
            'review': 'Draft'},
 'TC-086': {'id': 'TC-086',
            'scenario_id': 'TS-017',
            'title': 'Số điện thoại 10 chữ số được nhận, chữ số thứ 11 không vào ô',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': '6591234567 rồi gõ 8',
            'steps': '1. Nhập 6591234567.\n2. Gõ thêm chữ số 8.\n3. Đọc giá trị trong ô và bấm Review and submit.',
            'expected': '1. Ô vẫn là 6591234567, chữ số 8 không vào.\n2. Không có ghi chú về điện thoại.',
            'review': 'Draft'},
 'TC-087': {'id': 'TC-087',
            'scenario_id': 'TS-017',
            'title': 'Dán 11 chữ số bị cắt hoặc bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': 'Dán: 65912345678',
            'steps': '1. Dán 65912345678 vào ô Phone number.\n2. Bấm Review and submit.',
            'expected': '1. Ô không giữ 11 chữ số: hoặc bị cắt còn 10 chữ số, hoặc hiện "Complete: Phone number (up to '
                        '10 digits)." và hộp thoại không mở.',
            'review': 'Draft'},
 'TC-088': {'id': 'TC-088',
            'scenario_id': 'TS-017',
            'title': 'Số điện thoại 8 chữ số được nhận, 7 chữ số bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': '91234567 và 9123456',
            'steps': '1. Nhập 91234567 và bấm Review and submit.\n2. Nhập 9123456 và bấm Review and submit.',
            'expected': '1. 8 chữ số: không có ghi chú về điện thoại.\n'
                        '2. 7 chữ số: hiện "Complete: Phone number (up to 10 digits)."',
            'review': 'Draft'},
 'TC-089': {'id': 'TC-089',
            'scenario_id': 'TS-017',
            'title': 'Số điện thoại để trống bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': 'Phone number để trống',
            'steps': '1. Xoá ô Phone number.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Phone number (up to 10 digits)."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Draft'},
 'TC-090': {'id': 'TC-090',
            'scenario_id': 'TS-017',
            'title': 'Số điện thoại chứa SQL và script chỉ giữ chữ số',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Phone number sửa được (ô đang tô vàng).',
            'test_data': 'Dán hai chuỗi SQL và script',
            'steps': '1. Dán "9123\' OR 1=1--" vào ô.\n2. Dán "<script>alert(1)</script>".',
            'expected': '1. Chỉ còn các chữ số (9123 và 1 1 cho lần đầu), không alert, không lỗi hệ thống.\n'
                        '2. Không có chữ cái hay ký tự đặc biệt nào được lưu.',
            'review': 'Draft'},
 'TC-091': {'id': 'TC-091',
            'scenario_id': 'TS-018',
            'title': 'Email đúng cấu trúc được nhận',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Email sửa được (ô đang tô vàng).',
            'test_data': 'wm.tan@example.com\na.b+c@mail.example.sg\nTAN@EXAMPLE.COM',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Email.\n'
                     '2. Bấm Review and submit và đọc ghi chú, xoá ô Email trước giá trị kế tiếp.',
            'expected': '1. Không có ghi chú về email với cả ba giá trị.\n'
                        '2. Email chữ hoa được giữ và so sánh không phân biệt hoa thường.',
            'review': 'Draft'},
 'TC-092': {'id': 'TC-092',
            'scenario_id': 'TS-018',
            'title': 'Email sai cấu trúc bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Email sửa được (ô đang tô vàng).',
            'test_data': 'wm.tan@\n'
                         '@example.com\n'
                         'wm tan@example.com\n'
                         'wm.tan@@example.com\n'
                         'wm.tan@example\n'
                         '.wm@example.com\n'
                         'wm..tan@example.com',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Email.\n'
                     '2. Bấm Review and submit và đọc ghi chú, xoá ô Email trước giá trị kế tiếp.',
            'expected': '1. Mỗi lần hiện "Enter a valid email address." và hộp thoại Review before submitting không '
                        'mở.',
            'review': 'Draft'},
 'TC-093': {'id': 'TC-093',
            'scenario_id': 'TS-018',
            'title': 'Email để trống bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Email sửa được (ô đang tô vàng).',
            'test_data': '(để trống)',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Email.\n'
                     '2. Bấm Review and submit và đọc ghi chú, xoá ô Email trước giá trị kế tiếp.',
            'expected': '1. Hiện "Complete: Email." và hộp thoại không mở.',
            'review': 'Draft'},
 'TC-094': {'id': 'TC-094',
            'scenario_id': 'TS-018',
            'title': 'Giới hạn độ dài email',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Email sửa được (ô đang tô vàng).',
            'test_data': '64 ký tự trước @ cộng @example.com\n65 ký tự trước @\nTổng 254 ký tự\nTổng 255 ký tự',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Email.\n'
                     '2. Bấm Review and submit và đọc ghi chú, xoá ô Email trước giá trị kế tiếp.',
            'expected': '1. 64 ký tự trước @ và tổng 254: được nhận.\n'
                        '2. 65 ký tự trước @ và tổng 255: hiện "Enter a valid email address."',
            'review': 'Draft'},
 'TC-095': {'id': 'TC-095',
            'scenario_id': 'TS-018',
            'title': 'Email có xuống dòng bị chặn, chống chèn tiêu đề thư',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Email sửa được (ô đang tô vàng).',
            'test_data': "wm.tan@example.com%0ABcc: x@y.com (xuống dòng thật trong giá trị)\n'><script>@x.com",
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Email.\n'
                     '2. Bấm Review and submit và đọc ghi chú, xoá ô Email trước giá trị kế tiếp.',
            'expected': '1. Hiện "Enter a valid email address."\n2. Không alert, không chèn thêm người nhận.',
            'review': 'Draft'},
 'TC-096': {'id': 'TC-096',
            'scenario_id': 'TS-019',
            'title': 'Address để trống bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Address sửa được (ô đang tô vàng).',
            'test_data': 'Address để trống',
            'steps': '1. Xoá ô Address.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Address."\n2. Hộp thoại không mở.',
            'review': 'Draft'},
 'TC-097': {'id': 'TC-097',
            'scenario_id': 'TS-019',
            'title': 'Address 255 ký tự được nhận, 256 ký tự bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Address sửa được (ô đang tô vàng).',
            'test_data': 'Chuỗi 255 ký tự\nChuỗi 256 ký tự',
            'steps': '1. Dán chuỗi 255 ký tự rồi bấm Review and submit.\n'
                     '2. Dán chuỗi 256 ký tự rồi bấm Review and submit.',
            'expected': '1. 255 ký tự: không có ghi chú về địa chỉ.\n'
                        '2. 256 ký tự: hiện "Address must be 255 characters or fewer."',
            'review': 'Draft'},
 'TC-098': {'id': 'TC-098',
            'scenario_id': 'TS-019',
            'title': 'Address có ký tự đặc biệt, SQL và script lưu như văn bản',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Ô Address sửa được (ô đang tô vàng).',
            'test_data': 'Blk 123 Bukit Batok St 21, #05-12, Singapore 650123\n'
                         'O\'Brien & Sons "Unit" <b>5</b>\n'
                         "' OR '1'='1\n"
                         '<script>alert(1)</script>',
            'steps': '1. Nhập lần lượt từng giá trị và bấm Review and submit.\n'
                     '2. Mở hộp thoại Review before submitting (nếu mở được) và danh sách.',
            'expected': '1. Giá trị được lưu đúng như đã nhập.\n'
                        '2. Hiển thị như văn bản thường ở mọi nơi, không alert, không dựng HTML.',
            'review': 'Draft'},
 'TC-099': {'id': 'TC-099',
            'scenario_id': 'TS-020',
            'title': 'Relationship to child có đủ mười giá trị theo FS',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Mở danh sách Relationship to child và đọc các giá trị.\n2. Chọn lần lượt từng giá trị.',
            'expected': '1. Mười giá trị: Father, Mother, Legal guardian, Grandfather, Grandmother, Sibling, Uncle, '
                        'Aunt, Cousin, Other.\n'
                        '2. Mỗi giá trị chọn được và hiển thị đúng trong hộp thoại Review before submitting.',
            'review': 'Approve'},
 'TC-100': {'id': 'TC-100',
            'scenario_id': 'TS-020',
            'title': 'School-based FAS mặc định chọn Yes và đổi được sang No',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Đọc ô School-based FAS ngay sau khi nhập NRIC người khai.\n'
                     '2. Bỏ chọn ô.\n'
                     '3. Bấm Review and submit (các phần khác hợp lệ) và đọc dòng School-based FAS của hộp thoại.\n'
                     '4. Bấm Back to edit và chọn lại ô.',
            'expected': '1. Ô mặc định được chọn, nhãn "Also consider for SBFAS" kèm lời giải thích.\n'
                        '2. Sau khi bỏ chọn hộp thoại hiển thị School-based FAS: No.\n'
                        '3. Sau khi chọn lại hộp thoại hiển thị Yes.',
            'review': 'Approve'},
 'TC-101': {'id': 'TC-101',
            'scenario_id': 'TS-020',
            'title': 'Relationship to child để trống bị chặn',
            'suite': 'F5.3 Review application, Part 1 Applicant',
            'page': 'Review application, Part 1 Applicant',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Người khai: Tan Wei Ming S7612345A',
            'steps': '1. Cho Relationship to child chưa chọn (xoá giá trị đọc từ mẫu đơn).\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Relationship to child."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-102': {'id': 'TC-102',
            'scenario_id': 'TS-021',
            'title': 'Nhập NRIC con tự điền thông tin con từ hồ sơ MOE',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Con 1: Tan Mei Ling T1412345B',
            'steps': '1. Gõ T1412345B vào ô NRIC của con 1.\n2. Rời ô NRIC.\n3. Đọc dòng con.',
            'expected': '1. Full name Tan Mei Ling, Date of birth dạng DD/MM/YYYY, Gender F, School Bukit View '
                        'Primary, Level Primary, Grade P6, Class P6 Integrity.\n'
                        '2. Các ô tự điền chuyển sang nền xám.',
            'review': 'Approve'},
 'TC-103': {'id': 'TC-103',
            'scenario_id': 'TS-021',
            'title': 'Nhập thêm con học trường khác tự điền đúng trường và khối',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Con 2: Tan Jun Kai T1012345A',
            'steps': '1. Gõ T1412345B vào dòng con 1.\n2. Bấm Add child.\n3. Gõ T1012345A vào dòng con 2.',
            'expected': '1. Dòng con 2: Tan Jun Kai, Gender M, School Meridian Secondary, Level Secondary, Grade S4, '
                        'Class S4 Excellence.\n'
                        '2. Dòng con 1 không đổi.',
            'review': 'Draft'},
 'TC-104': {'id': 'TC-104',
            'scenario_id': 'TS-021',
            'title': 'Các ô thông tin con khoá không sửa được',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1: T1412345B',
            'steps': '1. Sau khi tự điền, bấm và thử gõ vào Full name, Date of birth, Gender, School, Level, Grade, '
                     'Class của con 1.',
            'expected': '1. Không ô nào nhận thay đổi, giá trị giữ nguyên.',
            'review': 'Approve'},
 'TC-105': {'id': 'TC-105',
            'scenario_id': 'TS-021',
            'title': 'Đổi NRIC con thay toàn bộ dữ liệu con',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'T1412345B rồi T1711010H',
            'steps': '1. Gõ T1412345B vào con 1.\n2. Đổi NRIC con 1 thành T1711010H.\n3. Đọc dòng con.',
            'expected': '1. Dòng con chuyển sang dữ liệu của NRIC mới, không còn giá trị của Tan Mei Ling.',
            'review': 'Draft'},
 'TC-106': {'id': 'TC-106',
            'scenario_id': 'TS-021',
            'title': 'NRIC con sai cấu trúc bị chặn',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Bốn giá trị sai cấu trúc',
            'steps': '1. Gõ lần lượt vào NRIC con 1: T141234B, T1412345BC, B1412345T, T14A2345B.\n'
                     '2. Bấm Review and submit sau mỗi giá trị.',
            'expected': '1. Mỗi lần hiện "Enter a valid NRIC/FIN." và hộp thoại không mở.\n'
                        '2. Dòng con không được tự điền.',
            'review': 'Draft'},
 'TC-107': {'id': 'TC-107',
            'scenario_id': 'TS-021',
            'title': 'Hồ sơ MOE lỗi thì không tự điền thông tin con',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở, Part 1 đã tự điền.',
            'test_data': '',
            'steps': '1. Cho hồ sơ MOE trả lỗi.\n2. Gõ T1412345B vào con 1.',
            'expected': '1. Hiện "Something went wrong. Please try again."\n'
                        '2. Dòng con không bị điền nửa chừng và phần Part 1 không mất.',
            'review': 'Draft'},
 'TC-108': {'id': 'TC-108',
            'scenario_id': 'TS-022',
            'title': 'Level suy ra đúng từ Grade ở các biên P1, P6, S1, S5, PU1, PU3',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'P1: T2010808D (Level Primary)\n'
                         'P6: T1412345B (Level Primary)\n'
                         'S1: T1380707D (Level Secondary)\n'
                         'S5: T0990505C (Level Secondary)\n'
                         'PU1: T0890101A (Level Pre-University)\n'
                         'PU3: T0690202I (Level Pre-University)',
            'steps': '1. Gõ lần lượt từng NRIC trong Test Data vào dòng con 1.\n2. Đọc Grade và Level sau mỗi lần.',
            'expected': '1. P1 và P6 cho Primary.\n2. S1 và S5 cho Secondary.\n3. PU1 và PU3 cho Pre-University.',
            'review': 'Approve'},
 'TC-109': {'id': 'TC-109',
            'scenario_id': 'TS-022',
            'title': 'Grade ngoài danh sách thì Level hiển thị thế nào',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'SEED-R5-20 Grade SP1',
            'steps': '1. Gõ NRIC T1511212Z (Grade SP1) vào dòng con 1.\n2. Đọc Level.',
            'expected': '1. Không có kết quả xác định trong FS.',
            'review': 'Block'},
 'TC-110': {'id': 'TC-110',
            'scenario_id': 'TS-023',
            'title': 'Add child thêm một dòng con trống và giữ dòng đã nhập',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'T1412345B',
            'steps': '1. Nhập con 1 T1412345B.\n2. Bấm Add child.\n3. Đọc các dòng con.',
            'expected': '1. Có hai dòng con, dòng 1 giữ dữ liệu, dòng 2 có NRIC trống và các cột còn lại trống.',
            'review': 'Approve'},
 'TC-111': {'id': 'TC-111',
            'scenario_id': 'TS-023',
            'title': 'Mẫu có hai con: một con ở trường người dùng, một con ở trường khác',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Con 1 T1412345B (BVP P6), con 2 T1012345A (MRS S4)',
            'steps': '1. Nhập con 1 T1412345B và con 2 T1012345A.\n'
                     '2. Hoàn tất các phần khác với dữ liệu hợp lệ.\n'
                     '3. Bấm Review and submit.',
            'expected': '1. Không có ghi chú chặn về trường của con.\n'
                        '2. Hộp thoại Review before submitting mở và liệt kê Children (2): Tan Mei Ling (Bukit View '
                        'Primary) và Tan Jun Kai (Meridian Secondary).',
            'review': 'Draft'},
 'TC-112': {'id': 'TC-112',
            'scenario_id': 'TS-023',
            'title': 'Thêm đến 5 dòng con và 5 dòng thành viên không lỗi',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Không nhập NRIC',
            'steps': '1. Bấm Add child bốn lần và Add member bốn lần.\n2. Đọc màn hình.',
            'expected': '1. Có 5 dòng con và 5 dòng thành viên, không có lỗi và bố cục không vỡ.',
            'review': 'Draft'},
 'TC-113': {'id': 'TC-113',
            'scenario_id': 'TS-023',
            'title': 'Dòng con để trống NRIC bị bỏ qua hay bị chặn',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.',
            'test_data': 'Con 1 T1412345B, con 2 trống',
            'steps': '1. Nhập con 1 T1412345B và bấm Add child, để con 2 trống.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Child 2: enter the NRIC/FIN."\n2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-114': {'id': 'TC-114',
            'scenario_id': 'TS-024',
            'title': 'Tên con khác dữ liệu Chính phủ hiện cảnh báo và vẫn nộp được',
            'suite': 'F5.4 Review application, Part 2 Children',
            'page': 'Review application, Part 2 Children',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'SEED-R5-21 con có tên MOE khác dữ liệu Chính phủ',
            'steps': '1. Nhập con có tên trong hồ sơ MOE khác dữ liệu Chính phủ.\n'
                     '2. Đọc dòng con và ghi chú.\n'
                     '3. Hoàn tất các phần khác và bấm Review and submit.',
            'expected': '1. Có ghi chú cho biết MOE sẽ thấy cảnh báo sai lệch dữ liệu của con đó.\n'
                        '2. Review and submit không bị chặn, hộp thoại Review before submitting mở.',
            'review': 'Draft'},
 'TC-115': {'id': 'TC-115',
            'scenario_id': 'TS-025',
            'title': 'Add member thêm một dòng thành viên trống',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1 T1412345B (Tan Mei Ling, Bukit View Primary P6)',
            'steps': '1. Bấm Add member.\n2. Đọc Part 3.',
            'expected': '1. Có một dòng thành viên mới với Full name, NRIC, Gender trống.\n'
                        '2. Part 1 và Part 2 không đổi.',
            'review': 'Approve'},
 'TC-116': {'id': 'TC-116',
            'scenario_id': 'TS-025',
            'title': 'Part 3 tuỳ chọn: mẫu không có thành viên vẫn nộp được',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1 T1412345B (Tan Mei Ling, Bukit View Primary P6), không có thành viên',
            'steps': '1. Không thêm thành viên nào.\n2. Hoàn tất các phần khác hợp lệ.\n3. Bấm Review and submit.',
            'expected': '1. Không có ghi chú về Part 3.\n'
                        '2. Hộp thoại Review before submitting mở với Household size 3 (người khai và hai con) hoặc 2 '
                        'nếu chỉ một con.',
            'review': 'Approve'},
 'TC-117': {'id': 'TC-117',
            'scenario_id': 'TS-025',
            'title': 'Dòng thành viên có tên mà thiếu NRIC bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Lim Hui Min, NRIC trống',
            'steps': '1. Bấm Add member, nhập Full name "Lim Hui Min" và để NRIC trống.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Family members (name and NRIC)."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-118': {'id': 'TC-118',
            'scenario_id': 'TS-025',
            'title': 'Dòng thành viên có NRIC mà thiếu tên bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'NRIC S8512301G, tên trống',
            'steps': '1. Bấm Add member, nhập NRIC S8512301G và để Full name trống.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Family members (name and NRIC)."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-119': {'id': 'TC-119',
            'scenario_id': 'TS-025',
            'title': 'Dòng thành viên trống hoàn toàn không chặn nộp',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Một dòng thành viên trống',
            'steps': '1. Bấm Add member và để trống cả dòng.\n2. Bấm Review and submit.',
            'expected': '1. Dòng trống bị bỏ qua, không có ghi chú Family members, Household size không tính dòng '
                        'trống.',
            'review': 'Draft'},
 'TC-120': {'id': 'TC-120',
            'scenario_id': 'TS-025',
            'title': 'Thêm tới 5 thành viên',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở, Part 1 và con 1 đã tự điền.',
            'test_data': 'S8512301G\nS5811122H\nT0211133G\nG1555566T\nS6611144Z',
            'steps': '1. Bấm Add member bốn lần và nhập đủ 5 thành viên hợp lệ.\n2. Bấm Review and submit.',
            'expected': '1. Hộp thoại mở, Household size bằng 1 cộng số con cộng 5, mọi thành viên được liệt kê.',
            'review': 'Draft'},
 'TC-121': {'id': 'TC-121',
            'scenario_id': 'TS-026',
            'title': 'Thành viên trùng NRIC người khai (T7) bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Thành viên S7612345A',
            'steps': '1. Bấm Add member, nhập Full name và NRIC S7612345A (trùng người khai).\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. The applicant, each child and each family member '
                        'must have a different NRIC/FIN."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-122': {'id': 'TC-122',
            'scenario_id': 'TS-026',
            'title': 'Con trùng NRIC người khai bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 2 S7612345A',
            'steps': '1. Bấm Add child và nhập NRIC con 2 là S7612345A.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. The applicant, each child and each family member '
                        'must have a different NRIC/FIN."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-123': {'id': 'TC-123',
            'scenario_id': 'TS-026',
            'title': 'Hai thành viên trùng NRIC nhau bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Hai thành viên S8512301G',
            'steps': '1. Thêm hai thành viên cùng NRIC S8512301G.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. The applicant, each child and each family member '
                        'must have a different NRIC/FIN."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-124': {'id': 'TC-124',
            'scenario_id': 'TS-026',
            'title': 'Thành viên trùng NRIC của con bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Thành viên T1412345B',
            'steps': '1. Bấm Add member, nhập NRIC T1412345B (trùng con 1).\n2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. The applicant, each child and each family member '
                        'must have a different NRIC/FIN."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-125': {'id': 'TC-125',
            'scenario_id': 'TS-026',
            'title': 'Con 2 trùng NRIC con 1 bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 2 T1412345B',
            'steps': '1. Bấm Add child và nhập NRIC con 2 là T1412345B.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. The applicant, each child and each family member '
                        'must have a different NRIC/FIN."\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-126': {'id': 'TC-126',
            'scenario_id': 'TS-026',
            'title': 'NRIC trùng khác chữ hoa chữ thường và khoảng trắng vẫn bị coi là trùng',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Thành viên " s7612345a "',
            'steps': '1. Thêm thành viên với NRIC " s7612345a ".\n2. Bấm Review and submit.',
            'expected': '1. Hiện "The same NRIC/FIN appears twice. ..." vì sau khi chuẩn hoá là S7612345A.',
            'review': 'Draft'},
 'TC-127': {'id': 'TC-127',
            'scenario_id': 'TS-027',
            'title': 'Full name thành viên 100 ký tự được nhận, 101 ký tự bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Full name 100 và 101 ký tự a, NRIC S8512301G',
            'steps': '1. Thêm thành viên với Full name 100 ký tự chữ và NRIC S8512301G, bấm Review and submit.\n'
                     '2. Đổi Full name thành 101 ký tự và bấm Review and submit.',
            'expected': '1. 100 ký tự: không có ghi chú.\n'
                        '2. 101 ký tự: hiện "Full name must be 100 characters or fewer."',
            'review': 'Draft'},
 'TC-128': {'id': 'TC-128',
            'scenario_id': 'TS-027',
            'title': 'Full name nhận chữ mọi hệ chữ viết và dấu câu cho phép',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': "Lim Hui Min\nNguyễn Thị Hoa\nO'Brien-Tan\n李慧敏\nAli bin Abdullah",
            'steps': '1. Nhập lần lượt các tên trong Test Data vào dòng thành viên (NRIC S8512301G) và bấm Review and '
                     'submit.',
            'expected': '1. Mọi tên được nhận, không có thông báo ký tự không hợp lệ.',
            'review': 'Draft'},
 'TC-129': {'id': 'TC-129',
            'scenario_id': 'TS-027',
            'title': 'Full name có chữ số hoặc ký tự đặc biệt bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Lim 123\nLim<Hui>\nLim;Hui\nLim{Hui}',
            'steps': '1. Nhập lần lượt các tên trong Test Data vào dòng thành viên (NRIC S8512301G) và bấm Review and '
                     'submit.',
            'expected': '1. Mỗi lần hiện "Full name contains invalid characters." và hộp thoại không mở.',
            'review': 'Draft'},
 'TC-130': {'id': 'TC-130',
            'scenario_id': 'TS-027',
            'title': 'Full name chứa script và SQL bị từ chối và không chạy',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': "<script>alert(1)</script>\n' OR '1'='1\n${jndi:ldap://x}\n{{7*7}}",
            'steps': '1. Nhập lần lượt các chuỗi trong Test Data vào Full name thành viên và bấm Review and submit.',
            'expected': '1. Mỗi lần hiện "Full name contains invalid characters.", không alert, không lỗi hệ thống.\n'
                        '2. Không dữ liệu nào bị đổi.',
            'review': 'Draft'},
 'TC-131': {'id': 'TC-131',
            'scenario_id': 'TS-027',
            'title': 'NRIC thành viên sai cấu trúc bị chặn',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'S761234A\nS7612345AB\nA7612345B\nS76A2345B',
            'steps': '1. Nhập lần lượt các NRIC trong Test Data vào dòng thành viên (Full name Lim Hui Min) và bấm '
                     'Review and submit.',
            'expected': '1. Mỗi lần hiện "Enter a valid NRIC/FIN." và hộp thoại không mở.\n'
                        '2. NRIC thành viên không bị khoá và không tra hồ sơ MOE.',
            'review': 'Draft'},
 'TC-132': {'id': 'TC-132',
            'scenario_id': 'TS-027',
            'title': 'Gender của thành viên có Male, Female, Other',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Dòng thành viên Lim Hui Min',
            'steps': '1. Mở danh sách Gender của dòng thành viên và đọc các giá trị.\n2. Chọn từng giá trị.',
            'expected': '1. Ba giá trị Male, Female, Other, chọn được từng giá trị.\n'
                        '2. Để trống Gender không chặn nộp.',
            'review': 'Draft'},
 'TC-133': {'id': 'TC-133',
            'scenario_id': 'TS-028',
            'title': 'Household summary theo hình FS: GHI 4,300.00, 4 người, PCI 1,075.00',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Người khai S7612345A, con T1412345B và T1012345A, thành viên Lim Hui Min',
            'steps': '1. Nhập con 2 T1012345A (Add child).\n'
                     '2. Thêm thành viên Lim Hui Min với NRIC theo FS.\n'
                     '3. Đọc phần tóm tắt hộ gia đình ở Part 3.',
            'expected': '1. Household size 4 (1 người khai, 2 con, 1 thành viên).\n'
                        '2. Gross household income S$ 4,300.00 mỗi tháng.\n'
                        '3. Per capita income S$ 1,075.00.',
            'review': 'Approve'},
 'TC-134': {'id': 'TC-134',
            'scenario_id': 'TS-028',
            'title': 'Part 3 không có ô nhập thu nhập',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '',
            'steps': '1. Đọc các ô của dòng thành viên và của phần tóm tắt.',
            'expected': '1. Chỉ có Full name, NRIC, Gender cho mỗi thành viên.\n'
                        '2. GHI, Household size, PCI chỉ hiển thị, không gõ được.',
            'review': 'Approve'},
 'TC-135': {'id': 'TC-135',
            'scenario_id': 'TS-028',
            'title': 'Household size đổi khi thêm con hoặc thành viên',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1 T1412345B (Tan Mei Ling, Bukit View Primary P6); con 2 T1012345A; thành viên S8512301G',
            'steps': '1. Đọc Household size với 1 con và không thành viên.\n'
                     '2. Thêm con 2 T1012345A, đọc.\n'
                     '3. Thêm thành viên S8512301G, đọc.',
            'expected': '1. Household size lần lượt 2, 3, 4.',
            'review': 'Draft'},
 'TC-136': {'id': 'TC-136',
            'scenario_id': 'TS-028',
            'title': 'Thu nhập của thành viên lấy từ dữ liệu Chính phủ và tính lại khi đổi NRIC',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở, Part 1 và con 1 đã tự điền.',
            'test_data': 'S8512301G: S$ 2,000.00 mỗi tháng\n'
                         'S5811122H: S$ 3,000.00 mỗi tháng\n'
                         'Thu nhập người khai: giá trị tại SEED-R5-22',
            'steps': '1. Thêm thành viên với NRIC S8512301G và đọc GHI.\n'
                     '2. Đổi NRIC thành viên sang S5811122H và đọc GHI.',
            'expected': '1. GHI bằng thu nhập của người khai cộng thu nhập của thành viên theo dữ liệu Chính phủ.\n'
                        '2. Sau khi đổi NRIC GHI được tính lại theo thành viên mới.',
            'review': 'Draft'},
 'TC-137': {'id': 'TC-137',
            'scenario_id': 'TS-028',
            'title': 'Thu nhập của các con không tính vào GHI',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1 T1412345B (Tan Mei Ling, Bukit View Primary P6); con 2 T1012345A',
            'steps': '1. Đọc GHI với 1 con.\n2. Thêm con 2 và đọc lại GHI.',
            'expected': '1. GHI không đổi khi thêm con, chỉ Household size và PCI đổi.',
            'review': 'Draft'},
 'TC-138': {'id': 'TC-138',
            'scenario_id': 'TS-028',
            'title': 'PCI hiển thị S$ hai chữ số thập phân theo giá trị chính xác',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'SEED-R5-22: các tổ hợp thu nhập cho hai mẫu',
            'steps': '1. Dựng mẫu có GHI 4,350.00 và Household size 4.\n'
                     '2. Đọc PCI.\n'
                     '3. Dựng mẫu có GHI 1,000.00 và Household size 3.\n'
                     '4. Đọc PCI.',
            'expected': '1. GHI 4,350.00 chia 4 cho PCI S$ 1,087.50.\n2. GHI 1,000.00 chia 3 cho PCI S$ 333.33.',
            'review': 'Draft'},
 'TC-139': {'id': 'TC-139',
            'scenario_id': 'TS-028',
            'title': 'Thành viên không có dữ liệu thu nhập',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở.',
            'test_data': 'Thành viên S6611144Z không có dữ liệu thu nhập',
            'steps': '1. Thêm thành viên với NRIC không có dữ liệu thu nhập trong dữ liệu Chính phủ.\n'
                     '2. Đọc GHI và bấm Review and submit.',
            'expected': '1. Thu nhập của thành viên đó tính 0, GHI bằng tổng thu nhập của những người còn lại.\n'
                        '2. Household size vẫn tính thành viên đó và PCI chia cho số người đã tính.\n'
                        '3. Review and submit không bị chặn vì thiếu dữ liệu thu nhập của thành viên.',
            'review': 'Draft'},
 'TC-140': {'id': 'TC-140',
            'scenario_id': 'TS-028',
            'title': 'API thu nhập Chính phủ lỗi thì không nộp được',
            'suite': 'F5.5 Review application, Part 3 Family and household',
            'page': 'Review application, Part 3 Family members',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở, Part 1 và con 1 đã tự điền.',
            'test_data': '',
            'steps': '1. Cho API thu nhập Chính phủ trả lỗi.\n2. Thêm thành viên S8512301G.\n3. Bấm Review and submit.',
            'expected': '1. Hiện "Something went wrong. Please try again."\n'
                        '2. Hộp thoại Review before submitting không mở, không tạo đơn nào.',
            'review': 'Draft'},
 'TC-141': {'id': 'TC-141',
            'scenario_id': 'TS-029',
            'title': 'Context để trống vẫn nộp được',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Context trống',
            'steps': '1. Để trống Context.\n2. Hoàn tất các phần khác hợp lệ và bấm Review and submit.',
            'expected': '1. Không có ghi chú về Context, hộp thoại Review before submitting mở.',
            'review': 'Approve'},
 'TC-142': {'id': 'TC-142',
            'scenario_id': 'TS-029',
            'title': 'Context hiện đúng ở hộp thoại Review before submitting',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Context: Father works shifts; the family hopes for help with transport.',
            'steps': '1. Nhập Context "Father works shifts; the family hopes for help with transport.".\n'
                     '2. Hoàn tất các phần khác hợp lệ, bấm Review and submit.\n'
                     '3. Đọc Part 4 của hộp thoại.',
            'expected': '1. Part 4 · Context hiện đúng nội dung "Father works shifts; the family hopes for help with '
                        'transport.".',
            'review': 'Approve'},
 'TC-143': {'id': 'TC-143',
            'scenario_id': 'TS-029',
            'title': 'Context lưu cùng đơn và hiện ở drawer của F4',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Review application đang mở, mẫu hợp lệ.',
            'test_data': 'Context: Father works shifts; the family hopes for help with transport.',
            'steps': '1. Nộp mẫu có Context "Father works shifts; the family hopes for help with transport.".\n'
                     '2. Mở drawer của đơn vừa nộp trong F4 (FAS applications).\n'
                     '3. Đọc phần Context.',
            'expected': '1. Context hiện đúng, nguyên văn, trong drawer cho người xét đơn.',
            'review': 'Approve'},
 'TC-144': {'id': 'TC-144',
            'scenario_id': 'TS-029',
            'title': 'Context đúng 2000 ký tự được nhận, 2001 ký tự bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Chuỗi 2000 và 2001 ký tự a',
            'steps': '1. Dán chuỗi 2000 ký tự vào Context, bấm Review and submit.\n'
                     '2. Dán chuỗi 2001 ký tự, bấm Review and submit.',
            'expected': '1. 2000 ký tự: không có ghi chú về Context.\n'
                        '2. 2001 ký tự: hiện "Context must be 2000 characters or fewer." và hộp thoại không mở.',
            'review': 'Draft'},
 'TC-145': {'id': 'TC-145',
            'scenario_id': 'TS-029',
            'title': 'Xuống dòng trong Context được giữ và tính một ký tự',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '1998 ký tự a, xuống dòng, 1 ký tự a',
            'steps': '1. Nhập 1998 ký tự, xuống dòng, 1 ký tự (tổng 2000 tính cả xuống dòng).\n'
                     '2. Bấm Review and submit.\n'
                     '3. Thêm một xuống dòng nữa (tổng 2001).\n'
                     '4. Bấm Review and submit.',
            'expected': '1. Tổng 2000: nhận, hộp thoại giữ ngắt dòng.\n'
                        '2. Tổng 2001: hiện "Context must be 2000 characters or fewer."',
            'review': 'Draft'},
 'TC-146': {'id': 'TC-146',
            'scenario_id': 'TS-029',
            'title': 'Context chứa HTML và script hiển thị như văn bản',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Context HTML và SQL',
            'steps': '1. Nhập Context "<b>ok</b> <script>alert(1)</script> \' OR \'1\'=\'1".\n'
                     '2. Bấm Review and submit và đọc hộp thoại.\n'
                     '3. Nộp và mở drawer ở F4.',
            'expected': '1. Hiển thị đúng như chuỗi đã nhập, không in đậm, không alert.\n'
                        '2. Lưu và hiển thị như văn bản thuần ở mọi nơi (BR5).',
            'review': 'Approve'},
 'TC-147': {'id': 'TC-147',
            'scenario_id': 'TS-029',
            'title': 'Context chứa tiếng Việt, emoji và nhiều hệ chữ',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Context đa ngôn ngữ',
            'steps': '1. Nhập Context "Gia đình khó khăn 🙏 家庭 உதவி".\n2. Bấm Review and submit và đọc hộp thoại.',
            'expected': '1. Hộp thoại hiển thị đúng chuỗi, không lỗi hiển thị.',
            'review': 'Approve'},
 'TC-148': {'id': 'TC-148',
            'scenario_id': 'TS-030',
            'title': 'Chưa tick Declaration bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Declaration ticked: không, signature checked: có',
            'steps': '1. Bỏ tick "The applicant ticked the declaration".\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Declaration."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-149': {'id': 'TC-149',
            'scenario_id': 'TS-030',
            'title': 'Chưa kiểm tra chữ ký bị chặn (T8)',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Declaration ticked: có, signature checked: không',
            'steps': '1. Bỏ tick "Applicant\'s signature checked".\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Applicant signature checked."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-150': {'id': 'TC-150',
            'scenario_id': 'TS-030',
            'title': 'Hai ô cam kết và Date signed cùng thiếu: một ghi chú liệt kê đủ',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Cả ba để trống',
            'steps': '1. Bỏ tick Declaration và Signature checked, xoá Date signed.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Declaration, Applicant signature checked, Date signed." theo thứ tự trong '
                        'FS 6.',
            'review': 'Draft'},
 'TC-151': {'id': 'TC-151',
            'scenario_id': 'TS-030',
            'title': 'Hai ô cam kết có thể tick và bỏ tick',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '',
            'steps': '1. Tick rồi bỏ tick từng ô hai lần.',
            'expected': '1. Ô đổi trạng thái đúng sau mỗi lần bấm, mặc định bỏ tick khi mở một mẫu mới.',
            'review': 'Draft'},
 'TC-152': {'id': 'TC-152',
            'scenario_id': 'TS-031',
            'title': 'Received by hiển thị School user đang đăng nhập và chỉ đọc',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Lan Nguyen BVP-0012; Farah Tan MRS-0012',
            'steps': '1. Đọc Received by (trường).\n2. Thử gõ vào ô.\n3. Đăng nhập Farah Tan và mở một mẫu mới.',
            'expected': '1. Với Lan Nguyen ô ghi Lan Nguyen, không sửa được.\n2. Với Farah Tan ô ghi Farah Tan.',
            'review': 'Approve'},
 'TC-153': {'id': 'TC-153',
            'scenario_id': 'TS-031',
            'title': 'Date received là hôm nay và chỉ đọc',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Ngày mẫu 18/10/2026',
            'steps': '1. Đọc Date received.\n2. Thử gõ vào ô.',
            'expected': '1. Hiển thị 18/10/2026 (ngày hôm nay của prototype), định dạng DD/MM/YYYY, không sửa được.',
            'review': 'Approve'},
 'TC-154': {'id': 'TC-154',
            'scenario_id': 'TS-031',
            'title': 'Date received đổi sang ngày hôm nay khi tiếp tục bản nháp ở ngày khác',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã có một bản nháp lưu 18/10/2026.',
            'test_data': 'Draft lưu 18/10/2026',
            'steps': '1. Save draft ngày 18/10/2026.\n'
                     '2. Đổi đồng hồ sang 19/10/2026.\n'
                     '3. Bấm Continue và đọc Date received.',
            'expected': '1. Date received là 19/10/2026.',
            'review': 'Draft'},
 'TC-155': {'id': 'TC-155',
            'scenario_id': 'TS-032',
            'title': 'Date signed để trống bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '(để trống)',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Hiện "Complete: Date signed."',
            'review': 'Draft'},
 'TC-156': {'id': 'TC-156',
            'scenario_id': 'TS-032',
            'title': 'Date signed đúng định dạng và ngày có thật được nhận',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '15/10/2026, 18/10/2026, 29/02/2024',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Mỗi giá trị không có ghi chú về Date signed.',
            'review': 'Draft'},
 'TC-157': {'id': 'TC-157',
            'scenario_id': 'TS-032',
            'title': 'Date signed sai định dạng bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '15-10-2026, 15/10/26, 2026/10/15, 15.10.2026',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Mỗi giá trị hiện "Enter a valid date (DD/MM/YYYY)."',
            'review': 'Draft'},
 'TC-158': {'id': 'TC-158',
            'scenario_id': 'TS-032',
            'title': 'Date signed không có thật bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '31/04/2026, 29/02/2027, 00/10/2026, 15/13/2026',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Mỗi giá trị hiện "Enter a valid date (DD/MM/YYYY)."',
            'review': 'Draft'},
 'TC-159': {'id': 'TC-159',
            'scenario_id': 'TS-032',
            'title': 'Date signed sau Date received bị chặn, đúng ngày nhận được nhận',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '18/10/2026 và 19/10/2026',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. 18/10/2026: không có ghi chú.\n'
                        '2. 19/10/2026: hiện "Date signed cannot be after the date received."',
            'review': 'Draft'},
 'TC-160': {'id': 'TC-160',
            'scenario_id': 'TS-032',
            'title': 'Date signed rất cũ không bị giới hạn dưới',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '01/01/1990',
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Không có ghi chú về Date signed.',
            'review': 'Draft'},
 'TC-161': {'id': 'TC-161',
            'scenario_id': 'TS-032',
            'title': 'Date signed chứa chữ, SQL và script bị chặn',
            'suite': 'F5.6 Review application, Part 4 Context and Part 5 Declaration',
            'page': 'Review application, Part 4 and Part 5',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': "abc, ' OR '1'='1, <script>alert(1)</script>",
            'steps': '1. Nhập lần lượt từng giá trị trong Test Data vào ô Date signed.\n'
                     '2. Bấm Review and submit sau mỗi giá trị và đọc ghi chú.',
            'expected': '1. Mỗi giá trị hiện "Enter a valid date (DD/MM/YYYY)." và không alert.',
            'review': 'Draft'},
 'TC-162': {'id': 'TC-162',
            'scenario_id': 'TS-033',
            'title': 'Save draft rồi Continue khôi phục đúng mẫu đơn (T9)',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Con 1 T1412345B (Tan Mei Ling, Bukit View Primary P6); Lim Hui Min; Context Father works '
                         'shifts; the family hopes for help with transport.',
            'steps': '1. Nhập con 1 T1412345B, thành viên Lim Hui Min, Context "Father works shifts; the family hopes '
                     'for help with transport.", đổi Relationship thành Mother.\n'
                     '2. Bấm Save draft.\n'
                     '3. Đọc danh sách Upload applications.\n'
                     '4. Bấm Continue ở dòng Draft.\n'
                     '5. So sánh các trường với lúc lưu.',
            'expected': '1. Danh sách có một dòng Draft với tên Tan Mei Ling, Application ID Not submitted.\n'
                        '2. Mẫu khôi phục đúng: NRIC người khai, con, thành viên, Context, Relationship Mother, '
                        'School-based FAS và các ô cam kết.',
            'review': 'Approve'},
 'TC-163': {'id': 'TC-163',
            'scenario_id': 'TS-033',
            'title': 'Save draft với mẫu chưa đầy đủ vẫn lưu được',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Chỉ có NRIC người khai',
            'steps': '1. Chỉ nhập NRIC người khai S7612345A.\n2. Bấm Save draft.\n3. Mở lại bằng Continue.',
            'expected': '1. Không có ghi chú Complete nào khi lưu nháp.\n'
                        '2. Dòng Draft xuất hiện, mẫu khôi phục chỉ với NRIC người khai và phần tự điền.',
            'review': 'Draft'},
 'TC-164': {'id': 'TC-164',
            'scenario_id': 'TS-033',
            'title': 'Save draft với dữ liệu sai vẫn lưu nguyên giá trị đã nhập',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Context 2100 ký tự; Date signed 31/04/2026',
            'steps': '1. Nhập Context 2100 ký tự và Date signed "31/04/2026".\n2. Bấm Save draft rồi Continue.',
            'expected': '1. Draft được lưu, hai giá trị khôi phục đúng như đã nhập.\n'
                        '2. Chặn xảy ra ở Review and submit, không ở Save draft.',
            'review': 'Draft'},
 'TC-165': {'id': 'TC-165',
            'scenario_id': 'TS-033',
            'title': 'Save draft hai lần cập nhật cùng một bản nháp',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'Hai lần lưu',
            'steps': '1. Bấm Save draft, đổi Context, bấm Save draft lần nữa.\n2. Đọc danh sách.',
            'expected': '1. Danh sách vẫn một dòng Draft, Continue mở ra Context mới.',
            'review': 'Draft'},
 'TC-166': {'id': 'TC-166',
            'scenario_id': 'TS-033',
            'title': 'Bấm đúp Save draft chỉ tạo một bản nháp',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '',
            'steps': '1. Bấm đúp nhanh Save draft.\n2. Đọc danh sách.',
            'expected': '1. Chỉ có một dòng Draft.',
            'review': 'Draft'},
 'TC-167': {'id': 'TC-167',
            'scenario_id': 'TS-033',
            'title': 'Bản nháp ghi người lưu và thời gian lưu',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': '',
            'steps': '1. Bấm Save draft.\n2. Đọc dòng Draft: cột Uploaded by và Uploaded at.',
            'expected': '1. Uploaded by là Lan Nguyen, Uploaded at là thời điểm lưu theo DD/MM/YYYY HH:mm giờ '
                        'Singapore.',
            'review': 'Draft'},
 'TC-168': {'id': 'TC-168',
            'scenario_id': 'TS-033',
            'title': 'Bản nháp còn nguyên sau khi đăng xuất và đăng nhập lại',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đang ở màn Review application với dữ liệu hợp lệ.',
            'test_data': '',
            'steps': '1. Bấm Save draft.\n2. Đăng xuất rồi đăng nhập lại BVP-0012.\n3. Mở Upload applications.',
            'expected': '1. Dòng Draft vẫn còn và Continue khôi phục đúng mẫu.',
            'review': 'Approve'},
 'TC-169': {'id': 'TC-169',
            'scenario_id': 'TS-034',
            'title': 'Discard trên bản scan vừa tải xoá scan và không tạo bản nháp',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. NRIC người khai S7612345A đã nhập, Part 1 đã tự điền và khoá.\n'
                             '5. Con 1 T1412345B đã nhập và tự điền.',
            'test_data': 'scan_bvp_0667.pdf chưa lưu nháp',
            'steps': '1. Bấm Discard.\n2. Đọc danh sách.',
            'expected': '1. Về danh sách Upload applications.\n2. Không có dòng Draft mới và scan bị bỏ.',
            'review': 'Draft'},
 'TC-170': {'id': 'TC-170',
            'scenario_id': 'TS-034',
            'title': 'Discard trên bản nháp đã mở xoá bản nháp',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Bấm Continue ở dòng Draft.\n2. Bấm Discard (xác nhận nếu có hộp thoại).\n3. Đọc danh sách.',
            'expected': '1. Dòng Draft biến mất khỏi danh sách và không khôi phục được.',
            'review': 'Draft'},
 'TC-171': {'id': 'TC-171',
            'scenario_id': 'TS-034',
            'title': 'Delete trên dòng Draft xoá bản nháp và scan',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Bấm Delete ở dòng Draft (xác nhận nếu có hộp thoại).\n2. Đọc danh sách và các thẻ.',
            'expected': '1. Dòng Draft biến mất, tổng các thẻ không đổi.\n2. Bản nháp và scan đi kèm không còn.',
            'review': 'Draft'},
 'TC-172': {'id': 'TC-172',
            'scenario_id': 'TS-035',
            'title': 'Bản nháp bị xoá khi nộp thành công',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Draft của Tan Mei Ling',
            'steps': '1. Bấm Continue ở dòng Draft và hoàn tất các phần thiếu.\n'
                     '2. Bấm Review and submit rồi Confirm and submit.\n'
                     '3. Đọc danh sách.',
            'expected': '1. Dòng Draft biến mất, xuất hiện đơn đã nộp với Application ID thật.',
            'review': 'Approve'},
 'TC-173': {'id': 'TC-173',
            'scenario_id': 'TS-035',
            'title': 'Draft chỉ thuộc trường của người tạo',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'Draft của BVP-0012',
            'steps': '1. Đăng nhập Farah Tan (Meridian Secondary) và mở Upload applications với Uploaded Any time.',
            'expected': '1. Dòng Draft của Tan Mei Ling không có trong danh sách của Meridian Secondary.',
            'review': 'Approve'},
 'TC-174': {'id': 'TC-174',
            'scenario_id': 'TS-035',
            'title': 'Hai người cùng mở một bản nháp, lần lưu sau ghi đè',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-05',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Có một bản nháp.',
            'test_data': '',
            'steps': '1. Phiên A và phiên B cùng Continue bản nháp.\n'
                     '2. Phiên A đổi Context và Save draft.\n'
                     '3. Phiên B đổi Relationship và Save draft.\n'
                     '4. Mở lại bản nháp.',
            'expected': '1. Bản nháp có nội dung của lần lưu sau (phiên B) và không lỗi hệ thống.',
            'review': 'Draft'},
 'TC-175': {'id': 'TC-175',
            'scenario_id': 'TS-035',
            'title': 'Con đã có đơn khi bản nháp được nộp bị chặn lúc nộp',
            'suite': 'F5.7 Drafts',
            'page': 'Upload applications and Review application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-05',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Hai phiên đăng nhập BVP-0012.',
            'test_data': 'Con T1711010H (SEED-R5-23)',
            'steps': '1. Phiên A lưu bản nháp có con T1711010H.\n'
                     '2. Phiên B nộp một mẫu hợp lệ cho cùng con đó.\n'
                     '3. Phiên A Continue bản nháp và bấm Review and submit.',
            'expected': '1. Phiên A hiện "{tên} already has an application this year ({id}, {status})." với mã đơn do '
                        'phiên B tạo.\n'
                        '2. Hộp thoại Review before submitting không mở.',
            'review': 'Approve'},
 'TC-176': {'id': 'TC-176',
            'scenario_id': 'TS-036',
            'title': 'Mẫu hợp lệ mở hộp thoại Review before submitting',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Bấm Review and submit.',
            'expected': '1. Không có ghi chú đỏ nào.\n2. Hộp thoại Review before submitting mở.',
            'review': 'Approve'},
 'TC-177': {'id': 'TC-177',
            'scenario_id': 'TS-036',
            'title': 'Mẫu trống hoàn toàn liệt kê mọi trường bắt buộc theo thứ tự FS',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.',
            'test_data': 'Mẫu trống',
            'steps': '1. Mở một mẫu mới chưa nhập gì (Upload and read file không đọc được giá trị nào).\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Một ghi chú đỏ: "Complete: Applicant NRIC, Applicant full name, Applicant date of birth, '
                        'Gender, Category, Nationality, Relationship to child, Phone number (up to 10 digits), Email, '
                        'Address, At least one child, Declaration, Applicant signature checked, Date signed."\n'
                        '2. Mục Family members không có vì Part 3 trống và tuỳ chọn.\n'
                        '3. Hộp thoại không mở.',
            'review': 'Draft'},
 'TC-178': {'id': 'TC-178',
            'scenario_id': 'TS-036',
            'title': 'Thiếu đúng một trường: Date signed',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Xoá Date signed.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Date signed."',
            'review': 'Approve'},
 'TC-179': {'id': 'TC-179',
            'scenario_id': 'TS-036',
            'title': 'Thiếu hai trường: chữ ký và Date signed',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Bỏ tick Applicant signature checked, xoá Date signed.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Complete: Applicant signature checked, Date signed."',
            'review': 'Draft'},
 'TC-180': {'id': 'TC-180',
            'scenario_id': 'TS-036',
            'title': 'Con chưa nhập NRIC',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Con 1 để trống',
            'steps': '1. Xoá NRIC của con 1.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Child 1: enter the NRIC/FIN."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-181': {'id': 'TC-181',
            'scenario_id': 'TS-037',
            'title': 'NRIC của con không có trong hồ sơ MOE (T4)',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'NRIC T2300001B không có trong hồ sơ MOE',
            'steps': '1. Nhập NRIC T2300001B vào con 1.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Child 1: no student with NRIC/FIN T2300001B in MOE records."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-182': {'id': 'TC-182',
            'scenario_id': 'TS-037',
            'title': 'Con 17 tuổi bị chặn (T5)',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user MRS-0012 Farah Tan, trường Meridian Secondary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ khác như Test Data của F5.8.',
            'test_data': 'SEED-R5-12 Teo Jun Hao T0990505C, sinh 18/10/2009, MRS S5',
            'steps': '1. Đăng nhập Farah Tan, nhập NRIC T0990505C vào con 1.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Teo Jun Hao must be 7 to 16 years old (now 17)."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-183': {'id': 'TC-183',
            'scenario_id': 'TS-037',
            'title': 'Con đã có đơn Pending trong năm nay bị chặn',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Aisha Rahman T1801177H có APP-2026-00412 Pending',
            'steps': '1. Nhập NRIC T1801177H (Aisha Rahman) vào con 1.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Aisha Rahman already has an application this year (APP-2026-00412, Pending)."\n'
                        '2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-184': {'id': 'TC-184',
            'scenario_id': 'TS-037',
            'title': 'Con đã có đơn đã duyệt trong năm nay bị chặn',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Lucas Teo T1780445K có APP-2026-00386 Approved SBFAS Tier 3',
            'steps': '1. Nhập NRIC T1780445K (Lucas Teo) vào con 1.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Lucas Teo already has an application this year (APP-2026-00386, {status})." với '
                        'status của đơn như danh sách hiển thị.\n'
                        '2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-185': {'id': 'TC-185',
            'scenario_id': 'TS-037',
            'title': 'Đơn của năm trước có chặn hay không',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Chen Xin Yi T1775532J có APP-2026-00390 nộp 14/11/2025 cho MOEFAS 2026',
            'steps': '1. Nhập NRIC T1775532J (Chen Xin Yi) vào con 1.\n2. Bấm Review and submit.',
            'expected': '1. Không có kết quả xác định trong FS.',
            'review': 'Block'},
 'TC-186': {'id': 'TC-186',
            'scenario_id': 'TS-037',
            'title': 'Không con nào học tại trường của người dùng (T6)',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ khác như Test Data của F5.8.',
            'test_data': 'SEED-R5-14 Yap Shu Ting T1380707D, MRS S1',
            'steps': '1. Đăng nhập Lan Nguyen (Bukit View Primary), nhập NRIC T1380707D (học Meridian Secondary) vào '
                     'con 1.\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Hiện "At least one child must be enrolled at Bukit View Primary."\n2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-187': {'id': 'TC-187',
            'scenario_id': 'TS-038',
            'title': 'Con đúng 7 tuổi hôm nay được nhận, con 6 tuổi 364 ngày bị chặn',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ khác như Test Data của F5.8.',
            'test_data': 'SEED-R5-08 Lim Zhi Wei T1990101C, sinh 18/10/2019, BVP P2\n'
                         'SEED-R5-09 Ng Kai Xin T1990202H, sinh 19/10/2019, BVP P1',
            'steps': '1. Nhập NRIC T1990101C vào con 1 và bấm Review and submit.\n'
                     '2. Đổi sang NRIC T1990202H và bấm Review and submit.',
            'expected': '1. Lim Zhi Wei (sinh 18/10/2019) được nhận, không có ghi chú tuổi.\n'
                        '2. Ng Kai Xin (sinh 19/10/2019) bị chặn: "Ng Kai Xin must be 7 to 16 years old (now 6)."',
            'review': 'Draft'},
 'TC-188': {'id': 'TC-188',
            'scenario_id': 'TS-038',
            'title': 'Con đúng 16 tuổi và 16 tuổi 364 ngày được nhận, con 17 tuổi bị chặn',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user MRS-0012 Farah Tan, trường Meridian Secondary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ khác như Test Data của F5.8.',
            'test_data': 'SEED-R5-10 Wong Jia Hui T1090303Z\n'
                         'SEED-R5-11 Ong Mei Xuan T0990404I\n'
                         'SEED-R5-12 Teo Jun Hao T0990505C',
            'steps': '1. Đăng nhập Farah Tan.\n'
                     '2. Nhập NRIC T1090303Z vào con 1, bấm Review and submit.\n'
                     '3. Đổi sang T0990404I và bấm Review and submit.\n'
                     '4. Đổi sang T0990505C và bấm Review and submit.',
            'expected': '1. Wong Jia Hui (sinh 18/10/2010, đúng 16 tuổi) được nhận.\n'
                        '2. Ong Mei Xuan (sinh 19/10/2009, 16 tuổi 364 ngày) được nhận.\n'
                        '3. Teo Jun Hao (sinh 18/10/2009, đúng 17 tuổi) bị chặn: "Teo Jun Hao must be 7 to 16 years '
                        'old (now 17)."',
            'review': 'Draft'},
 'TC-189': {'id': 'TC-189',
            'scenario_id': 'TS-038',
            'title': 'Tuổi tính tại ngày nộp, không tính tại ngày lưu nháp',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã có bản nháp lưu 17/10/2026 với con SEED-R5-08.',
            'test_data': 'SEED-R5-08',
            'steps': '1. Đặt ngày 17/10/2026 và Save draft mẫu có con T1990101C (6 tuổi 364 ngày).\n'
                     '2. Đặt ngày 18/10/2026 (sinh nhật thứ 7).\n'
                     '3. Bấm Continue rồi Review and submit.',
            'expected': '1. Review and submit không báo lỗi tuổi vì ngày nộp con đúng 7 tuổi.',
            'review': 'Draft'},
 'TC-190': {'id': 'TC-190',
            'scenario_id': 'TS-039',
            'title': 'Không có form FAS nào đang mở bị chặn, có ngày form kế tiếp (T13)',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'SEED-R5-33: MOEFAS 2028 có Form opens 01/08/2027 đến 31/12/2027, đã publish',
            'steps': '1. Đặt ngày 01/01/2027 (sau Form closes 31/12/2026 của MOEFAS 2027 và Tier 2027).\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Hiện "Tan Mei Ling: the FAS application form is closed (next opens 01/08/2027)."\n'
                        '2. Hộp thoại không mở.',
            'review': 'Approve'},
 'TC-191': {'id': 'TC-191',
            'scenario_id': 'TS-039',
            'title': 'Không có form nào đang mở và chưa có form kế tiếp: bỏ phần ngày',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Không có form kế tiếp được publish',
            'steps': '1. Đặt ngày 01/01/2027 khi chưa có scheme MOEFAS hay SBFAS nào publish cho năm sau.\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Hiện "Tan Mei Ling: the FAS application form is closed." (không có phần "next opens").',
            'review': 'Approve'},
 'TC-192': {'id': 'TC-192',
            'scenario_id': 'TS-039',
            'title': 'Biên đầu: 01/08/2026 mở, 31/07/2026 đóng',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Form opens 01/08/2026',
            'steps': '1. Đặt ngày 31/07/2026 và bấm Review and submit.\n'
                     '2. Đặt ngày 01/08/2026 và bấm Review and submit.',
            'expected': '1. 31/07/2026: hiện "Tan Mei Ling: the FAS application form is closed (next opens '
                        '01/08/2026)."\n'
                        '2. 01/08/2026: không có ghi chú về form.',
            'review': 'Draft'},
 'TC-193': {'id': 'TC-193',
            'scenario_id': 'TS-039',
            'title': 'Biên cuối: 31/12/2026 mở, 01/01/2027 đóng',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Form closes 31/12/2026',
            'steps': '1. Đặt ngày 31/12/2026 và bấm Review and submit.\n'
                     '2. Đặt ngày 01/01/2027 và bấm Review and submit.',
            'expected': '1. 31/12/2026: không có ghi chú về form.\n'
                        '2. 01/01/2027: hiện "Tan Mei Ling: the FAS application form is closed ..."',
            'review': 'Draft'},
 'TC-194': {'id': 'TC-194',
            'scenario_id': 'TS-039',
            'title': 'Chỉ form SBFAS của trường con đang mở thì vẫn nộp được',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'MOEFAS 2027 đóng, Tier (2027) của BVP còn mở',
            'steps': '1. Đặt khoảng form MOEFAS đã đóng và Tier SBFAS của Bukit View Primary còn mở.\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Không có ghi chú về form, hộp thoại mở.',
            'review': 'Approve'},
 'TC-195': {'id': 'TC-195',
            'scenario_id': 'TS-039',
            'title': 'Chỉ form MOEFAS đang mở thì vẫn nộp được',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'MOEFAS 2027 mở, SBFAS của BVP đóng',
            'steps': '1. Đặt khoảng form MOEFAS còn mở và các Tier SBFAS của Bukit View Primary đã đóng.\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Không có ghi chú về form, hộp thoại mở.',
            'review': 'Approve'},
 'TC-196': {'id': 'TC-196',
            'scenario_id': 'TS-039',
            'title': 'Con không phải công dân chỉ xét form SBFAS của trường con',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'SEED-R5-15 Ismail Hakim T1610707C',
            'steps': '1. Nhập con T1610707C (Singapore PR) khi form MOEFAS còn mở nhưng Tier SBFAS của Bukit View '
                     'Primary đã đóng.\n'
                     '2. Bấm Review and submit.',
            'expected': '1. Hiện "Ismail Hakim: the FAS application form is closed ..." vì chỉ form SBFAS của trường '
                        'con được xét.',
            'review': 'Draft'},
 'TC-197': {'id': 'TC-197',
            'scenario_id': 'TS-039',
            'title': 'Mẫu hai con, form của một con đóng thì chặn cả mẫu',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Con 1 T1412345B, con 2 T1610707C',
            'steps': '1. Nhập con 1 T1412345B (công dân) và con 2 T1610707C (PR, trường BVP).\n'
                     '2. Đặt Tier SBFAS của Bukit View Primary đã đóng, MOEFAS còn mở.\n'
                     '3. Bấm Review and submit.',
            'expected': '1. Hiện ghi chú form đóng cho Ismail Hakim, không có ghi chú cho Tan Mei Ling.\n'
                        '2. Hộp thoại không mở và không tạo đơn nào.',
            'review': 'Draft'},
 'TC-198': {'id': 'TC-198',
            'scenario_id': 'TS-040',
            'title': 'Hai ghi chú cùng lúc: thiếu trường bắt buộc và form đã đóng',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Đặt ngày 01/01/2027, xoá Date signed.\n2. Bấm Review and submit.',
            'expected': '1. Hiện hai ghi chú đỏ ở đầu trang: "Complete: Date signed." và "Tan Mei Ling: the FAS '
                        'application form is closed ..."',
            'review': 'Approve'},
 'TC-199': {'id': 'TC-199',
            'scenario_id': 'TS-040',
            'title': 'Sửa lỗi rồi bấm lại thì ghi chú cũ biến mất',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Xoá Date signed và bấm Review and submit.\n'
                     '2. Nhập Date signed 15/10/2026 và bấm Review and submit.',
            'expected': '1. Lần đầu có "Complete: Date signed."\n2. Lần hai không còn ghi chú nào và hộp thoại mở.',
            'review': 'Draft'},
 'TC-200': {'id': 'TC-200',
            'scenario_id': 'TS-040',
            'title': 'Nhiều con có ghi chú riêng cho từng con',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Con 2 trống, con 3 T2300001B',
            'steps': '1. Thêm con 2 có NRIC trống và con 3 NRIC T2300001B.\n2. Bấm Review and submit.',
            'expected': '1. Hiện "Child 2: enter the NRIC/FIN." và "Child 3: no student with NRIC/FIN T2300001B in MOE '
                        'records."',
            'review': 'Draft'},
 'TC-201': {'id': 'TC-201',
            'scenario_id': 'TS-040',
            'title': 'Trang cuộn lên đầu để thấy ghi chú',
            'suite': 'F5.8 Review and submit validation',
            'page': 'Review application (kiểm tra khi Review and submit)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Cuộn xuống Part 5 và bấm Review and submit khi thiếu Date signed.',
            'expected': '1. Trang cuộn lên đầu, ghi chú đỏ nằm trong vùng nhìn thấy.',
            'review': 'Draft'},
 'TC-202': {'id': 'TC-202',
            'scenario_id': 'TS-041',
            'title': 'Hộp thoại hiện đủ Part 1 đến Part 4 như hình của FS',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Thêm con 2, thành viên và Context như Test Data.',
            'test_data': 'Con 2 T1012345A đã thêm\n'
                         'Thành viên Lim Hui Min đã thêm\n'
                         'Context "Father works shifts; the family hopes for help with transport."',
            'steps': '1. Dựng mẫu theo Test Data rồi bấm Review and submit.\n2. Đọc từng phần của hộp thoại.',
            'expected': '1. Tiêu đề "Review before submitting", dòng nhãn FUNCTION 5 kèm tên file scan_bvp_0667.pdf, '
                        'phụ đề "One application per child. MOEFAS is assessed automatically after the application '
                        'form closes."\n'
                        '2. Part 1: Applicant Tan Wei Ming · S7612345A (Father); Category · Nationality Singapore '
                        'Citizen · Chinese; Contact +65 9123 4567 · wm.tan@example.com; School-based FAS Yes.\n'
                        '3. Part 2 Children (2): Tan Mei Ling · T1412345B, Bukit View Primary · P6 · P6 Integrity · EA '
                        'EA-2021-03318; Tan Jun Kai · T1012345A, Meridian Secondary · S4 · S4 Excellence · EA '
                        'EA-2017-00412.\n'
                        '4. Part 3: Other family members Lim Hui Min; Household size 4; Gross household income S$ '
                        '4,300.00 / month (Government records); Per capita income S$ 1,075.00.\n'
                        '5. Part 4: nội dung Context. Hai nút Back to edit và Confirm and submit.',
            'review': 'Approve'},
 'TC-203': {'id': 'TC-203',
            'scenario_id': 'TS-041',
            'title': 'Hộp thoại với một con hiện Children (1) và Household size đúng',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Con 1 T1412345B, không thành viên',
            'steps': '1. Bấm Review and submit với mẫu một con, không thành viên.',
            'expected': '1. Part 2 ghi Children (1) với một dòng Tan Mei Ling.\n'
                        '2. Household size 2, PCI bằng GHI chia 2.',
            'review': 'Approve'},
 'TC-204': {'id': 'TC-204',
            'scenario_id': 'TS-041',
            'title': 'Địa chỉ người khai không hiện trong hộp thoại',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Bấm Review and submit và tìm địa chỉ trong hộp thoại.',
            'expected': '1. Hộp thoại không hiển thị Address.',
            'review': 'Draft'},
 'TC-205': {'id': 'TC-205',
            'scenario_id': 'TS-041',
            'title': 'Con chưa có EA hiển thị dấu gạch ngang ở số EA',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'SEED-R5-17 Rao Anika T2010808D chưa có EA',
            'steps': '1. Dựng mẫu có con Rao Anika T2010808D và bấm Review and submit.',
            'expected': '1. Dòng của Rao Anika ghi trường, khối, lớp và số EA hiển thị dấu gạch ngang, không lỗi.',
            'review': 'Draft'},
 'TC-206': {'id': 'TC-206',
            'scenario_id': 'TS-041',
            'title': 'Context trống thì Part 4 trống hoặc ẩn',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Context trống',
            'steps': '1. Để trống Context và bấm Review and submit.',
            'expected': '1. Part 4 không hiển thị nội dung, không lỗi hiển thị.',
            'review': 'Draft'},
 'TC-207': {'id': 'TC-207',
            'scenario_id': 'TS-041',
            'title': 'Context hiển thị như văn bản thuần trong hộp thoại',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Context HTML',
            'steps': '1. Nhập Context "<b>x</b><script>alert(1)</script>" và bấm Review and submit.',
            'expected': '1. Hộp thoại hiện đúng chuỗi, không in đậm, không alert.',
            'review': 'Approve'},
 'TC-208': {'id': 'TC-208',
            'scenario_id': 'TS-042',
            'title': 'Back to edit đóng hộp thoại, giữ nguyên mẫu và không tạo gì',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': '',
            'steps': '1. Bấm Review and submit.\n2. Bấm Back to edit.\n3. Đọc màn Review application và danh sách.',
            'expected': '1. Hộp thoại đóng, mọi giá trị đã nhập còn nguyên.\n'
                        '2. Không có đơn mới và không có dòng Draft mới trong danh sách.',
            'review': 'Approve'},
 'TC-209': {'id': 'TC-209',
            'scenario_id': 'TS-042',
            'title': 'Sửa rồi mở lại hộp thoại thì hiện giá trị mới',
            'suite': 'F5.9 Review before submitting dialog',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.',
            'test_data': 'Relationship Mother, School-based FAS No',
            'steps': '1. Bấm Review and submit rồi Back to edit.\n'
                     '2. Đổi Relationship thành Mother, bỏ chọn School-based FAS, đổi Context.\n'
                     '3. Bấm Review and submit.',
            'expected': '1. Hộp thoại hiện Mother, School-based FAS No và Context mới.',
            'review': 'Approve'},
 'TC-210': {'id': 'TC-210',
            'scenario_id': 'TS-043',
            'title': 'Mẫu hai con tạo hai đơn dùng chung mã gia đình, MOEFAS Pending (T10)',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)\n'
                         'Con 2 Tan Jun Kai T1012345A (Meridian Secondary, Singapore Citizen)\n'
                         'School-based FAS Yes',
            'steps': '1. Bấm Confirm and submit.\n'
                     '2. Đọc toast và danh sách.\n'
                     '3. Mở hai đơn mới, đọc Application ID, mã gia đình, nguồn, trạng thái và System check.',
            'expected': '1. Toast "Applications submitted."\n'
                        '2. Hai đơn mới: mỗi con một đơn, nguồn Paper, cùng một mã gia đình.\n'
                        '3. Cả hai là MOEFAS, trạng thái Pending, System check Waiting, chưa có quyết định.',
            'review': 'Draft'},
 'TC-211': {'id': 'TC-211',
            'scenario_id': 'TS-043',
            'title': 'Mẫu một con tạo một đơn và toast số ít',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B',
            'steps': '1. Bấm Confirm and submit.\n2. Đọc toast và danh sách.',
            'expected': '1. Toast "Application submitted for assessment."\n'
                        '2. Một đơn mới của Tan Mei Ling, nguồn Paper, MOEFAS Pending, System check Waiting.',
            'review': 'Draft'},
 'TC-212': {'id': 'TC-212',
            'scenario_id': 'TS-043',
            'title': 'Sau khi nộp về danh sách, bản nháp biến mất và đơn mới hiện',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)',
            'steps': '1. Bấm Confirm and submit.\n2. Đọc danh sách với Uploaded Last 7 days.',
            'expected': '1. Hộp thoại đóng, màn danh sách hiện.\n'
                        '2. Có đơn mới với Application ID thật, không còn dòng Draft của mẫu này, các thẻ tăng đúng.',
            'review': 'Draft'},
 'TC-213': {'id': 'TC-213',
            'scenario_id': 'TS-043',
            'title': 'Application ID có định dạng APP, năm, số thứ tự và không trùng',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Hai mẫu một con',
            'steps': '1. Nộp hai mẫu liên tiếp.\n2. Đọc các Application ID.',
            'expected': '1. Mỗi ID có dạng APP-2026-nnnnn, các ID khác nhau.',
            'review': 'Draft'},
 'TC-214': {'id': 'TC-214',
            'scenario_id': 'TS-043',
            'title': 'Đơn tạo ra có nguồn Paper trong F4',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B',
            'steps': '1. Nộp mẫu một con.\n'
                     '2. Đăng nhập MOE HQ, mở FAS applications và đơn vừa nộp.\n'
                     '3. Đọc nguồn và Context.',
            'expected': '1. Nguồn là Paper, Context đúng như đã nhập, trạng thái Pending và System check Waiting.',
            'review': 'Approve'},
 'TC-215': {'id': 'TC-215',
            'scenario_id': 'TS-043',
            'title': 'School-based FAS được lưu cùng đơn',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'School-based FAS No',
            'steps': '1. Bỏ chọn School-based FAS trước khi nộp.\n2. Nộp, mở View application của đơn.',
            'expected': '1. Đơn hiển thị School-based FAS: No và mở lại cho thấy đúng giá trị.',
            'review': 'Approve'},
 'TC-216': {'id': 'TC-216',
            'scenario_id': 'TS-043',
            'title': 'Scan gắn với đơn của từng con',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)\n'
                         'Con 2 Tan Jun Kai T1012345A (Meridian Secondary, Singapore Citizen)\n'
                         'School-based FAS Yes',
            'steps': '1. Nộp mẫu hai con từ một scan.\n2. Mở View application của từng đơn và đọc file scan.',
            'expected': '1. Mỗi đơn có file scan_bvp_0667.pdf để xem.',
            'review': 'Draft'},
 'TC-217': {'id': 'TC-217',
            'scenario_id': 'TS-043',
            'title': 'Nộp lại cho con đã có đơn bị chặn',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan Mei Ling T1412345B',
            'steps': '1. Nộp mẫu một con Tan Mei Ling.\n'
                     '2. Upload một mẫu mới cho cùng Tan Mei Ling và bấm Review and submit.',
            'expected': '1. Hiện "Tan Mei Ling already has an application this year ({id}, Pending)." với mã đơn vừa '
                        'tạo.',
            'review': 'Approve'},
 'TC-218': {'id': 'TC-218',
            'scenario_id': 'TS-044',
            'title': 'Con công dân với School-based FAS Yes là MOEFAS Pending',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan Mei Ling, Yes',
            'steps': '1. Nộp mẫu một con công dân với Yes.\n2. Đọc đơn.',
            'expected': '1. MOEFAS Pending, System check Waiting, chưa xếp hạng.',
            'review': 'Approve'},
 'TC-219': {'id': 'TC-219',
            'scenario_id': 'TS-044',
            'title': 'Con công dân với School-based FAS No vẫn là MOEFAS Pending',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan Mei Ling, No',
            'steps': '1. Bỏ chọn School-based FAS rồi nộp mẫu một con công dân.\n2. Đọc đơn.',
            'expected': '1. MOEFAS Pending, System check Waiting. Không bị Rejected lúc nộp.',
            'review': 'Approve'},
 'TC-220': {'id': 'TC-220',
            'scenario_id': 'TS-044',
            'title': 'Con Singapore PR là SBFAS Pending gửi trường của con',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'SEED-R5-15 Ismail Hakim T1610707C',
            'steps': '1. Nộp mẫu có con Ismail Hakim (PR, Bukit View Primary) với Yes.\n'
                     '2. Đọc đơn và đăng nhập Lan Nguyen xem FAS applications.',
            'expected': '1. Đơn là SBFAS Pending ngay lúc nộp, gửi Bukit View Primary.\n'
                        '2. Không có bước chờ form MOEFAS đóng.',
            'review': 'Approve'},
 'TC-221': {'id': 'TC-221',
            'scenario_id': 'TS-044',
            'title': 'Con International ASEAN là SBFAS Pending gửi trường của con',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'SEED-R5-16 Pham Minh Chau T1580909J',
            'steps': '1. Nộp mẫu có con Pham Minh Chau (International ASEAN, Bukit View Primary) với Yes.\n2. Đọc đơn.',
            'expected': '1. SBFAS Pending, gửi Bukit View Primary.',
            'review': 'Approve'},
 'TC-222': {'id': 'TC-222',
            'scenario_id': 'TS-044',
            'title': 'Con không đủ điều kiện quốc tịch với School-based FAS No',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'SEED-R5-15, School-based FAS No',
            'steps': '1. Bỏ chọn School-based FAS và nộp mẫu có con Ismail Hakim (PR).',
            'expected': '1. Không có kết quả xác định trong FS.',
            'review': 'Block'},
 'TC-223': {'id': 'TC-223',
            'scenario_id': 'TS-044',
            'title': 'Mẫu có con công dân và con PR được phân luồng riêng từng con',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan Mei Ling T1412345B; Ismail Hakim T1610707C',
            'steps': '1. Nộp mẫu có con Tan Mei Ling (công dân) và Ismail Hakim (PR).\n2. Đọc hai đơn.',
            'expected': '1. Đơn Tan Mei Ling là MOEFAS Pending, đơn Ismail Hakim là SBFAS Pending.\n'
                        '2. Hai đơn dùng chung một mã gia đình.',
            'review': 'Approve'},
 'TC-224': {'id': 'TC-224',
            'scenario_id': 'TS-044',
            'title': 'Đơn của con học trường khác vào hàng SBFAS của trường con',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con PR học MRS (SEED-R5)',
            'steps': '1. Nộp mẫu có con PR học Meridian Secondary.\n2. Đăng nhập Farah Tan và mở FAS applications.',
            'expected': '1. Đơn SBFAS Pending hiện ở Meridian Secondary, không hiện ở Bukit View Primary.',
            'review': 'Draft'},
 'TC-225': {'id': 'TC-225',
            'scenario_id': 'TS-044',
            'title': 'Sau khi form MOEFAS đóng, đơn không đủ điều kiện sang SBFAS khi chọn Yes',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan family, MOEFAS 2027 giới hạn GHI 4,200.00 hoặc PCI 1,050.00',
            'steps': '1. Nộp mẫu một con công dân với GHI 4,300.00 và PCI 1,075.00, School-based FAS Yes.\n'
                     '2. Đăng nhập MOE HQ, bấm Close form now (demo) ở MOEFAS 2027.\n'
                     '3. Đọc đơn.',
            'expected': '1. Đơn vượt giới hạn GHI 4,200.00 và PCI 1,050.00 của MOEFAS 2027, chuyển thành SBFAS Pending '
                        'gửi Bukit View Primary.',
            'review': 'Approve'},
 'TC-226': {'id': 'TC-226',
            'scenario_id': 'TS-044',
            'title': 'Sau khi form MOEFAS đóng, đơn không đủ điều kiện bị Rejected khi chọn No',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Tan family, School-based FAS No',
            'steps': '1. Nộp mẫu một con công dân với GHI 4,300.00 và PCI 1,075.00, School-based FAS No.\n'
                     '2. Đăng nhập MOE HQ, bấm Close form now (demo).\n'
                     '3. Đọc đơn.',
            'expected': '1. Đơn không đủ điều kiện và Rejected (BR8, không có SBFAS).',
            'review': 'Approve'},
 'TC-227': {'id': 'TC-227',
            'scenario_id': 'TS-044',
            'title': 'Sau khi form MOEFAS đóng, đơn đủ điều kiện được duyệt tự động',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'SEED-R5-22 hộ GHI 3,000.00, PCI 750.00',
            'steps': '1. Nộp mẫu một con công dân với GHI 3,000.00 và PCI 750.00.\n'
                     '2. Đăng nhập MOE HQ, bấm Close form now (demo).\n'
                     '3. Đọc đơn.',
            'expected': '1. Đơn Approved bởi System (auto-approved) với priority theo F4.',
            'review': 'Approve'},
 'TC-228': {'id': 'TC-228',
            'scenario_id': 'TS-045',
            'title': 'Bấm đúp Confirm and submit chỉ tạo một bộ đơn',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)',
            'steps': '1. Bấm đúp nhanh Confirm and submit.\n2. Đọc danh sách.',
            'expected': '1. Chỉ có một bộ đơn, không có đơn trùng.',
            'review': 'Draft'},
 'TC-229': {'id': 'TC-229',
            'scenario_id': 'TS-045',
            'title': 'Hai người nộp cùng một con: chỉ một đơn được tạo',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-05',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Hai phiên đăng nhập BVP-0012, mỗi phiên có hộp thoại Review before submitting mở cho '
                             'cùng con.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)',
            'steps': '1. Phiên A và phiên B cùng mở hộp thoại cho cùng con Tan Mei Ling.\n'
                     '2. Phiên A bấm Confirm and submit.\n'
                     '3. Phiên B bấm Confirm and submit.',
            'expected': '1. Phiên A tạo đơn thành công.\n'
                        '2. Phiên B hiện "Tan Mei Ling already has an application this year ({id}, Pending)." và không '
                        'tạo đơn.',
            'review': 'Draft'},
 'TC-230': {'id': 'TC-230',
            'scenario_id': 'TS-045',
            'title': 'Form đóng giữa lúc mở hộp thoại và lúc xác nhận thì không tạo đơn',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)',
            'steps': '1. Mở hộp thoại Review before submitting khi form đang mở.\n'
                     '2. Đặt đồng hồ sau Form closes.\n'
                     '3. Bấm Confirm and submit.',
            'expected': '1. Không tạo đơn nào, hiện "Tan Mei Ling: the FAS application form is closed ..." và bản nháp '
                        'giữ nguyên.',
            'review': 'Draft'},
 'TC-231': {'id': 'TC-231',
            'scenario_id': 'TS-045',
            'title': 'Một con vừa có đơn: mẫu hai con không tạo đơn nào',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-05',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Hai phiên đăng nhập, phiên A có hộp thoại Review before submitting mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)\n'
                         'Con 2 Tan Jun Kai T1012345A (Meridian Secondary, Singapore Citizen)\n'
                         'School-based FAS Yes',
            'steps': '1. Phiên A mở hộp thoại cho hai con.\n'
                     '2. Phiên B nộp mẫu riêng cho con 2.\n'
                     '3. Phiên A bấm Confirm and submit.',
            'expected': '1. Phiên A không tạo đơn nào cho cả hai con.\n'
                        '2. Hiện thông báo already has an application cho con 2.',
            'review': 'Draft'},
 'TC-232': {'id': 'TC-232',
            'scenario_id': 'TS-045',
            'title': 'Lỗi lưu khi xác nhận: không tạo đơn, bản nháp giữ nguyên',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'Con 1 Tan Mei Ling T1412345B (Bukit View Primary, Singapore Citizen)',
            'steps': '1. Cho dịch vụ lưu đơn trả lỗi.\n2. Bấm Confirm and submit.',
            'expected': '1. Hiện "Something went wrong. Please try again."\n'
                        '2. Không có đơn nào được tạo, hộp thoại giữ mở, dữ liệu đã nhập giữ nguyên.',
            'review': 'Draft'},
 'TC-233': {'id': 'TC-233',
            'scenario_id': 'TS-045',
            'title': 'Cảnh báo sai lệch tên con hiện cho MOE sau khi nộp',
            'suite': 'F5.10 Confirm and submit and routing',
            'page': 'Review before submitting dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đã bấm Upload scans, thêm scan_bvp_0667.pdf và bấm Upload and read. Màn Review '
                             'application đang mở.\n'
                             '4. Mẫu hợp lệ: người khai S7612345A đã tự điền, con 1 T1412345B đã tự điền, Declaration '
                             'và Signature checked đã tick, Date signed 15/10/2026.\n'
                             '5. Hộp thoại Review before submitting đang mở.',
            'test_data': 'SEED-R5-21',
            'steps': '1. Nộp mẫu có con tên MOE khác dữ liệu Chính phủ.\n2. Đăng nhập MOE HQ và mở drawer của đơn.',
            'expected': '1. Drawer hiện cảnh báo sai lệch dữ liệu của con.',
            'review': 'Draft'},
 'TC-234': {'id': 'TC-234',
            'scenario_id': 'TS-046',
            'title': 'View application hiện đủ năm phần chỉ đọc và nút Back to list',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00386 Approved SBFAS Tier 3',
            'steps': '1. Bấm dòng APP-2026-00386 Lucas Teo.\n2. Đọc màn hình và thử sửa từng ô.\n3. Bấm Back to list.',
            'expected': '1. Mẫu đơn hiện Part 1 đến Part 5 với giá trị đã nộp.\n'
                        '2. Mọi ô chỉ đọc, không có Edit và Save changes vì đơn đã Approved SBFAS.\n'
                        '3. Back to list về danh sách.',
            'review': 'Approve'},
 'TC-235': {'id': 'TC-235',
            'scenario_id': 'TS-047',
            'title': 'Đơn Pending có nút Edit',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412 Aisha Rahman (Pending)',
            'steps': '1. Mở APP-2026-00412 Aisha Rahman (Pending) từ danh sách.\n'
                     '2. Đọc các nút ở đầu màn View application.',
            'expected': '1. Có nút Edit.',
            'review': 'Approve'},
 'TC-236': {'id': 'TC-236',
            'scenario_id': 'TS-047',
            'title': 'Đơn Approved SBFAS không có nút Edit',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00386 Lucas Teo (Approved SBFAS Tier 3)',
            'steps': '1. Mở APP-2026-00386 Lucas Teo (Approved SBFAS Tier 3) từ danh sách.\n'
                     '2. Đọc các nút ở đầu màn View application.',
            'expected': '1. Không có nút Edit, mọi ô chỉ đọc.',
            'review': 'Approve'},
 'TC-237': {'id': 'TC-237',
            'scenario_id': 'TS-047',
            'title': 'Đơn Approved MOEFAS không có nút Edit',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'một đơn Approved MOEFAS (chọn Uploaded Any time)',
            'steps': '1. Mở một đơn Approved MOEFAS (chọn Uploaded Any time) từ danh sách.\n'
                     '2. Đọc các nút ở đầu màn View application.',
            'expected': '1. Không có nút Edit, mọi ô chỉ đọc.',
            'review': 'Approve'},
 'TC-238': {'id': 'TC-238',
            'scenario_id': 'TS-047',
            'title': 'Đơn Rejected không có nút Edit',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'một đơn Rejected (chọn Uploaded Any time)',
            'steps': '1. Mở một đơn Rejected (chọn Uploaded Any time) từ danh sách.\n'
                     '2. Đọc các nút ở đầu màn View application.',
            'expected': '1. Không có nút Edit, mọi ô chỉ đọc.',
            'review': 'Approve'},
 'TC-239': {'id': 'TC-239',
            'scenario_id': 'TS-048',
            'title': 'Sửa đơn Pending và Save changes, History ghi Paper application edited (T12)',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Mở APP-2026-00412 Aisha Rahman và bấm Edit.\n'
                     '2. Đổi Relationship thành Mother, đổi Context và bỏ chọn School-based FAS.\n'
                     '3. Bấm Save changes.\n'
                     '4. Mở lại đơn và mở History của đơn.',
            'expected': '1. Đơn lưu các giá trị mới, trạng thái vẫn Pending.\n'
                        '2. History có một dòng "Paper application edited" mới nhất.',
            'review': 'Approve'},
 'TC-240': {'id': 'TC-240',
            'scenario_id': 'TS-048',
            'title': 'Save changes cập nhật thành viên gia đình và thu nhập của đơn',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đang mở View application của một đơn Pending.',
            'test_data': 'APP-2026-00412, thêm thành viên S8512301G',
            'steps': '1. Bấm Edit ở đơn Pending và thêm một thành viên.\n'
                     '2. Bấm Save changes và đọc GHI, Household size, PCI.',
            'expected': '1. Household size tăng 1, GHI và PCI tính lại theo dữ liệu Chính phủ.\n'
                        '2. History có "Paper application edited".',
            'review': 'Draft'},
 'TC-241': {'id': 'TC-241',
            'scenario_id': 'TS-048',
            'title': 'Sửa đơn không chạy lại luồng quyết định',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Sửa Context của đơn MOEFAS Pending và Save changes.\n'
                     '2. Đọc trạng thái, System check và priority của đơn.',
            'expected': '1. Đơn vẫn Pending, System check vẫn Waiting, không có quyết định hay xếp hạng mới.',
            'review': 'Approve'},
 'TC-242': {'id': 'TC-242',
            'scenario_id': 'TS-048',
            'title': 'Sau khi form đóng vẫn sửa được đơn Pending (BR9)',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Có một đơn Pending, đang mở View application.',
            'test_data': 'Đơn Pending khi form đã đóng',
            'steps': '1. Đặt ngày 01/01/2027.\n2. Mở đơn Pending, bấm Edit, đổi Context và Save changes.',
            'expected': '1. Save changes thành công, không có ghi chú "form is closed".',
            'review': 'Approve'},
 'TC-243': {'id': 'TC-243',
            'scenario_id': 'TS-049',
            'title': 'Save changes chạy lại kiểm tra bắt buộc',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Bấm Edit, bỏ tick Applicant signature checked và Save changes.',
            'expected': '1. Hiện "Complete: Applicant signature checked." và không lưu gì, không có History mới.',
            'review': 'Draft'},
 'TC-244': {'id': 'TC-244',
            'scenario_id': 'TS-049',
            'title': 'Khi sửa, NRIC người khai và NRIC con bị khoá',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Bấm Edit và thử đổi NRIC người khai và NRIC của con.',
            'expected': '1. Hai NRIC không sửa được, các ô tự điền giữ nguyên.',
            'review': 'Draft'},
 'TC-245': {'id': 'TC-245',
            'scenario_id': 'TS-049',
            'title': 'Đơn đang sửa không bị coi là trùng với chính nó',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Bấm Edit và Save changes mà không đổi gì.',
            'expected': '1. Save changes thành công, không hiện "already has an application this year".',
            'review': 'Draft'},
 'TC-246': {'id': 'TC-246',
            'scenario_id': 'TS-049',
            'title': 'Đơn đổi trạng thái trong lúc sửa thì không lưu',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-05',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Hai phiên đăng nhập: School user và MOE HQ, đơn Pending đang mở ở chế độ sửa.',
            'test_data': 'Đơn MOEFAS Pending',
            'steps': '1. Phiên A mở Edit của đơn Pending.\n'
                     '2. Phiên MOE HQ đóng form MOEFAS và đơn được quyết định.\n'
                     '3. Phiên A bấm Save changes.',
            'expected': '1. Không lưu gì và hiện "This application was already decided by {user} on {DD/MM/YYYY}."',
            'review': 'Draft'},
 'TC-247': {'id': 'TC-247',
            'scenario_id': 'TS-049',
            'title': 'Bấm đúp Save changes chỉ ghi một mục History',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Bấm đúp nhanh Save changes sau khi sửa Context.\n2. Đọc History.',
            'expected': '1. Chỉ một dòng "Paper application edited" mới.',
            'review': 'Draft'},
 'TC-248': {'id': 'TC-248',
            'scenario_id': 'TS-049',
            'title': 'Lỗi lưu khi Save changes không thêm History',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Đơn Pending đang ở chế độ sửa.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Cho dịch vụ lưu trả lỗi và bấm Save changes.',
            'expected': '1. Hiện "Something went wrong. Please try again.", đơn giữ giá trị cũ và không có History '
                        'mới.',
            'review': 'Draft'},
 'TC-249': {'id': 'TC-249',
            'scenario_id': 'TS-049',
            'title': 'API sửa đơn đã quyết định bị từ chối',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'APP-2026-00386',
            'steps': '1. Gửi yêu cầu sửa đơn APP-2026-00386 (Approved SBFAS) và đơn Rejected qua API.',
            'expected': '1. Yêu cầu bị từ chối, không đổi dữ liệu và không có History mới.',
            'review': 'Approve'},
 'TC-250': {'id': 'TC-250',
            'scenario_id': 'TS-049',
            'title': 'School user không mở được đơn của trường khác bằng địa chỉ',
            'suite': 'F5.11 View and edit submitted application',
            'page': 'View application',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy.\n'
                             '2. Đã đăng nhập School user MRS-0012 Farah Tan, trường Meridian Secondary.',
            'test_data': 'APP-2026-00412',
            'steps': '1. Đăng nhập Farah Tan.\n'
                     '2. Mở trực tiếp địa chỉ View application của APP-2026-00412 (Bukit View Primary).',
            'expected': '1. Không hiện dữ liệu của đơn, thông báo "You do not have access to this application."',
            'review': 'Draft'},
 'TC-251': {'id': 'TC-251',
            'scenario_id': 'TS-050',
            'title': 'MOE HQ gọi API của F5 bị từ chối',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy.\n2. Có token của MOE HQ.',
            'test_data': '',
            'steps': '1. Đăng nhập MOE HQ Mei Lin Tan và lấy token.\n'
                     '2. Gọi API danh sách, mở đơn, lưu nháp và nộp của F5.',
            'expected': '1. Mọi yêu cầu bị từ chối (403), không trả dữ liệu, không đổi gì.',
            'review': 'Approve'},
 'TC-252': {'id': 'TC-252',
            'scenario_id': 'TS-050',
            'title': 'School user không đọc được đơn của trường khác qua API',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy.\n2. Có token của Farah Tan.',
            'test_data': '',
            'steps': '1. Dùng token của Farah Tan gọi API lấy APP-2026-00412 và danh sách của Bukit View Primary.',
            'expected': '1. 403 và "You do not have access to this application.", không trả dữ liệu, danh sách chỉ '
                        'chứa dữ liệu của Meridian Secondary.',
            'review': 'Draft'},
 'TC-253': {'id': 'TC-253',
            'scenario_id': 'TS-050',
            'title': 'School user không đọc được bản nháp của trường khác qua API',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy.\n2. Có token của Farah Tan.',
            'test_data': '',
            'steps': '1. Dùng token của Farah Tan gọi API lấy bản nháp của Tan Mei Ling.',
            'expected': '1. 403 hoặc không tìm thấy, không trả dữ liệu của bản nháp.',
            'review': 'Draft'},
 'TC-254': {'id': 'TC-254',
            'scenario_id': 'TS-050',
            'title': 'Tải file scan của trường khác bị từ chối',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy.\n2. Có token của hai School user.',
            'test_data': '',
            'steps': '1. Dùng token của Farah Tan mở địa chỉ file scan của đơn APP-2026-00412.\n'
                     '2. Dùng token của Lan Nguyen mở cùng file.',
            'expected': '1. Farah Tan bị từ chối.\n'
                        '2. Lan Nguyen tải được, tên file gửi đúng loại nội dung và tiêu đề tải xuống.',
            'review': 'Draft'},
 'TC-255': {'id': 'TC-255',
            'scenario_id': 'TS-051',
            'title': 'Máy chủ không nhận giá trị tự điền gửi từ trình duyệt',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'Full name đổi thành "Hacker", School đổi sang trường khác',
            'steps': '1. Gửi yêu cầu nộp với tên người khai và trường của con bị sửa so với hồ sơ.\n2. Đọc đơn đã tạo.',
            'expected': '1. Đơn dùng giá trị từ hồ sơ, không dùng giá trị gửi lên.',
            'review': 'Draft'},
 'TC-256': {'id': 'TC-256',
            'scenario_id': 'TS-051',
            'title': 'Yêu cầu nộp bỏ qua giao diện vẫn bị chạy lại mọi kiểm tra',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Bản F5 có API (chưa có)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-02, ENV-R5-03, ENV-R5-04',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'Con SEED-R5-12, ngày 01/01/2027, NRIC trùng',
            'steps': '1. Gửi trực tiếp yêu cầu nộp với con 17 tuổi.\n'
                     '2. Gửi yêu cầu nộp khi form đóng.\n'
                     '3. Gửi yêu cầu nộp với NRIC trùng và thiếu chữ ký.',
            'expected': '1. Mỗi yêu cầu bị từ chối với thông báo của quy tắc tương ứng, không tạo đơn nào.',
            'review': 'Draft'},
 'TC-257': {'id': 'TC-257',
            'scenario_id': 'TS-051',
            'title': 'Mã gia đình: nhiều con dùng chung, mẫu một con có mã riêng',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-03',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'Mẫu hai con Tan Mei Ling và Tan Jun Kai; mẫu một con T1711010H',
            'steps': '1. Nộp một mẫu hai con và một mẫu một con.\n2. Đọc mã gia đình của các đơn.',
            'expected': '1. Hai đơn của mẫu hai con có cùng mã gia đình.\n'
                        '2. Đơn của mẫu một con có mã gia đình riêng, khác hai mã kia.',
            'review': 'Draft'},
 'TC-258': {'id': 'TC-258',
            'scenario_id': 'TS-051',
            'title': 'Nguồn dữ liệu ngoài lỗi khi nộp thì không nộp',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02, ENV-R5-07',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': '',
            'steps': '1. Cho hồ sơ MOE lỗi rồi gọi nộp.\n2. Cho API thu nhập Chính phủ lỗi rồi gọi nộp.',
            'expected': '1. Cả hai lần hiện "Something went wrong. Please try again.", không tạo đơn, không dùng thu '
                        'nhập 0 thay thế.',
            'review': 'Draft'},
 'TC-259': {'id': 'TC-259',
            'scenario_id': 'TS-051',
            'title': 'Context 2 MB gửi qua API bị từ chối',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'Context 2 MB',
            'steps': '1. Gửi yêu cầu lưu nháp với Context 2 MB.',
            'expected': '1. Yêu cầu bị từ chối vì vượt 2000 ký tự, máy chủ không lỗi và không treo.',
            'review': 'Draft'},
 'TC-260': {'id': 'TC-260',
            'scenario_id': 'TS-051',
            'title': 'File scan lưu ngoài thư mục web, tên do máy chủ đặt',
            'suite': 'F5.12 Access, API and data',
            'page': 'F5 API (School user)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Bản F5 có API (chưa có)\nChrome (latest)\nBuild: ghi khi chạy\nCần: ENV-R5-02',
            'preconditions': '1. Bản F5 có API chạy, dữ liệu SEED-R5 đã nạp.\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.',
            'test_data': 'scan_bvp_0667.pdf',
            'steps': '1. Tải một scan rồi kiểm tra vị trí lưu và tên lưu.\n2. Thử mở file bằng địa chỉ đoán trước.',
            'expected': '1. File lưu ngoài thư mục web, tên lưu do máy chủ sinh.\n'
                        '2. Địa chỉ đoán trước không tải được.',
            'review': 'Draft'},
 'TC-261': {'id': 'TC-261',
            'scenario_id': 'TS-052',
            'title': 'Ngày, giờ và tiền theo DD/MM/YYYY, HH:mm giờ Singapore, S$ #,##0.00',
            'suite': 'F5.12 Access, API and data',
            'page': 'Nhiều màn của F5',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (ngày mẫu 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: ghi khi chạy\n'
                   'Cần: ENV-R5-01',
            'preconditions': '1. Prototype ở trạng thái gốc (dùng Reset data).\n'
                             '2. Đã đăng nhập School user BVP-0012 Lan Nguyen, trường Bukit View Primary.\n'
                             '3. Màn Upload applications đang mở.',
            'test_data': '',
            'steps': '1. Đọc Uploaded at, Date of birth, Date signed, Date received, GHI và PCI ở danh sách, màn '
                     'Review, hộp thoại và View application.',
            'expected': '1. Ngày dạng DD/MM/YYYY, giờ HH:mm theo giờ Singapore, tiền dạng S$ 4,300.00.',
            'review': 'Draft'}}
