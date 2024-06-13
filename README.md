TÓM TẮT CHƯƠNG TRÌNH:
•  remove_comments_and_empty_lines: Hàm này loại bỏ các dòng trống và các bình luận trong mã hợp ngữ. Nó duyệt qua từng dòng mã, loại bỏ tất cả các ký tự sau dấu # (đánh dấu bình luận) và xóa các khoảng trắng thừa. Nếu dòng kết quả không trống, nó sẽ thêm dòng đó vào danh sách các dòng đã làm sạch.
•  calculate_label_addresses: Hàm này xác định các nhãn (labels) và tính toán địa chỉ của chúng. Nó duyệt qua từng dòng mã đã làm sạch, kiểm tra xem có dấu : (đánh dấu nhãn) hay không. Nếu có, nó lưu lại địa chỉ của nhãn (được tính bằng cách lấy giá trị hiện tại chia cho 4) và lọc bỏ định nghĩa nhãn khỏi danh sách lệnh. Nếu có lệnh trong cùng một dòng với nhãn, nó sẽ giữ lại lệnh đó.
•  replace_labels: Hàm này thay thế các nhãn trong lệnh bằng địa chỉ tương ứng của chúng. Nó duyệt qua từng dòng lệnh đã lọc và thay thế tất cả các nhãn bằng địa chỉ đã tính toán trước đó.
•  parse_instruction: Hàm này phân tích một lệnh thành các phần thành phần (operation, các thanh ghi, các giá trị immediate, v.v.). Nó sử dụng biểu thức chính quy để tách lệnh bằng dấu phẩy, khoảng trắng và dấu ngoặc đơn, sau đó loại bỏ các chuỗi rỗng.
•  assemble_instruction: Hàm này dịch một lệnh thành mã nhị phân tương ứng. Nó lấy opcode của lệnh và tùy thuộc vào loại lệnh (R-type, J-type hoặc I-type), nó dịch lệnh bằng cách sử dụng các mã nhị phân tương ứng cho các thanh ghi, các giá trị immediate, và các mã chức năng (funct).
•  assemble_program: Hàm này dịch toàn bộ chương trình từ danh sách các lệnh. Nó duyệt qua từng lệnh, cố gắng dịch nó thành mã máy và xử lý bất kỳ lỗi nào xảy ra trong quá trình dịch.
•  main: Hàm chính để đọc file đầu vào, xử lý mã hợp ngữ và ghi file đầu ra. Nó đọc file đầu vào, xử lý mã hợp ngữ để loại bỏ các bình luận, tính toán địa chỉ nhãn, thay thế các nhãn, và dịch các lệnh. Cuối cùng, nó ghi mã máy kết
HƯỚNG DẪN SỬ DỤNG:
Bước 1: Tạo file với tên “input.asm” với các mã muốn dịch và file “output.bin” trong cùng 1 folder với file .py này
Bước 2: Chạy chương trình
Bước 3: Mở file output.bin để thấy kết quả.
LƯU Ý:
Chương trình này chỉ dịch được những lệnh đã được định nghĩa sẵn trong code muốn dịch thêm thì tự định nghĩa thêm :3
