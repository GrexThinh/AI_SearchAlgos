			HƯỚNG DẪN KIỂM THỬ CHƯƠNG TRÌNH CỦA ĐỒ ÁN 1

NOTE: Theo yêu cầu của thầy thì các bản đồ kiểm thử được để trong thư mục kiểm thử
      Nhưng em để thêm ở thư mục source nữa, mục đích là phục vụ việc chạy chương trình

1. Kiểm thử chương trình ứng với bản đồ không có điểm thưởng
B1: run code thì màn hình console sẽ xuất hiện 1 menu có tên "MENU-MAZE-MAP-NO-BONUS-POINTS" sẽ xuất hiện.
B2: _ Nhập 1 số từ 1 đến 5 như trong menu đã thông báo
      để lựa chọn bản đồ trong 5 bản đồ không có điểm thưởng ở thư mục kiểm thử, và đi đến bước 3.
    _ Nếu không muốn kiểm thử nữa thì nhập 1 số không thuộc 1 đến 5
      lúc đó CHƯƠNG TRÌNH SẼ KẾT THÚC!
B3: _ Khi đã chọn bản đồ thì xuất hiện 1 menu có tên "MENU-SEARCH-ALGORITHMS"
    _ Lúc này sẽ nhập 1 số từ 1 đến 4 để chọn thuật toán tìm kiếm tương ứng theo thứ tự:
      Breadth-First Search, Depth-First Search, Greedy Best-First Search, A* algorithm
B4: _ Với thuật toán Breadth-First Search và Depth-First Search thì sẽ đến bước 5.
    _ Còn với thuật toán Greedy Best-First Search, A* algorithm thì sẽ xuất hiện 1 màn hình menu
      có tên "MENU-HEURISTIC-DISTANCE". Sau đó thì nhập 1 hoặc 2 để chọn heuristic tính khoảng cách để phục vụ cho việc di chuyển
      các heuristic lần lượt là: distance Euclid và distance Manhattan.
B5: _ Kết quả xuất hiện ở màn hình là chi phí thực hiện đường đi, lộ trình đường đi, và bản đồ minh họa đường đi
    _ Khi tắt bản đồ minh họa đi thì sẽ quay lại bước 1.


2. Kiểm thử chương trình ứng với bản đồ có điểm thưởng (lưu ý ở trường hợp này chỉ dùng thuật toán tìm kiếm A*)
B1: run code thì màn hình console sẽ xuất hiện 1 menu có tên "MENU-MAZE-MAP-HAVE-BONUS-POINTS" sẽ xuất hiện.
B2: _ Nhập 1 số từ 1 đến 3 như trong menu đã thông báo
      để lựa chọn bản đồ trong 3 bản đồ có điểm thưởng ở thư mục kiểm thử, và đi đến bước 3.
    _ Nếu không muốn kiểm thử nữa thì nhập 1 số không thuộc 1 đến 3
      lúc đó CHƯƠNG TRÌNH SẼ KẾT THÚC!
B3: _ Khi đã chọn bản đồ thì xuất hiện 1 menu có tên "MENU-HEURISTIC-DISTANCE".
    _ Lúc này sẽ nhập số 1 hoặc 2 để lựa chọn heuristic phục vụ việc chọn và đi đến điểm thưởng gần nhất.
      2 heuristic lần lượt là: distance Euclid và distance Manhattan.
B4: _ Kết quả xuất hiện ở màn hình là chi phí thực hiện đường đi, lộ trình đường đi, và bản đồ minh họa đường đi
    _ Khi tắt bản đồ minh họa đi thì sẽ quay lại bước 1.
