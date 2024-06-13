import re

# Từ điển ánh xạ các lệnh hợp ngữ sang mã nhị phân tương ứng
opcodes = {
    'add': '000000', 'addu': '000000', 'and': '000000', 'jr': '000000',
    'addi': '001000', 'addiu': '001001', 'andi': '001100', 'beq': '000100',
    'bne': '000101', 'lbu': '100100', 'lhu': '100101', 'lui': '001111',
    'lw': '100011', 'sw': '101011', 'j': '000010', 'jal': '000011'
}

# Từ điển ánh xạ các lệnh R-type sang mã nhị phân tương ứng
functs = {
    'add': '100000', 'addu': '100001', 'and': '100100', 'jr': '001000'
}

# Từ điển ánh xạ tên các thanh ghi sang mã nhị phân tương ứng
registers = {
    '$zero': '00000', '$at': '00001', '$v0': '00010', '$v1': '00011',
    '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
    '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011',
    '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111',
    '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011',
    '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111',
    '$t8': '11000', '$t9': '11001', '$k0': '11010', '$k1': '11011',
    '$gp': '11100', '$sp': '11101', '$fp': '11110', '$ra': '11111'
}

# Hàm loại bỏ các dòng trống và các bình luận trong mã hợp ngữ
def remove_comments_and_empty_lines(assembly_lines):
    cleaned_lines = []
    for line in assembly_lines:
        line = re.sub(r'#.*', '', line).strip()  # Loại bỏ các bình luận (phần sau dấu #) và khoảng trắng
        if line:  # Nếu dòng không trống sau khi loại bỏ
            cleaned_lines.append(line)  # Thêm dòng đã làm sạch vào danh sách
    return cleaned_lines

# Hàm tính toán địa chỉ của các nhãn và lọc bỏ định nghĩa nhãn
def calculate_label_addresses(cleaned_lines):
    label_addresses = {}  # Từ điển để lưu địa chỉ của các nhãn
    address = 0  # Địa chỉ bắt đầu từ 0
    filtered_lines = []  # Danh sách để lưu các dòng lệnh đã lọc bỏ nhãn
    for line in cleaned_lines:
        if ':' in line:  # Kiểm tra xem dòng có chứa nhãn không
            label, instruction = line.split(':', 1)  # Tách nhãn và lệnh
            label_addresses[label.strip()] = address // 4  # Lưu địa chỉ của nhãn (chia cho 4 để chuyển từ byte sang từ)
            if instruction.strip():  # Nếu có lệnh trong cùng một dòng với nhãn
                filtered_lines.append(instruction.strip())  # Thêm lệnh vào danh sách đã lọc
                address += 4  # Tăng địa chỉ lên 4 byte (1 từ)
        else:
            filtered_lines.append(line)  # Thêm dòng không có nhãn vào danh sách đã lọc
            address += 4  # Tăng địa chỉ lên 4 byte (1 từ)
    return label_addresses, filtered_lines

# Hàm thay thế các nhãn bằng địa chỉ tương ứng trong các lệnh
def replace_labels(filtered_lines, label_addresses):
    replaced_lines = []  # Danh sách để lưu các dòng lệnh đã thay thế nhãn
    for line in filtered_lines:
        for label, address in label_addresses.items():  # Duyệt qua từng nhãn và địa chỉ tương ứng
            if label in line:  # Kiểm tra xem dòng lệnh có chứa nhãn không
                line = line.replace(label, str(address))  # Thay thế nhãn bằng địa chỉ của nó
        replaced_lines.append(line)  # Thêm dòng lệnh đã thay thế vào danh sách
    return replaced_lines

# Hàm phân tích một lệnh thành các phần thành phần
def parse_instruction(instruction):
    parts = re.split(r'[,\s()]+', instruction)  # Tách bằng dấu phẩy, khoảng trắng và dấu ngoặc đơn
    return [part for part in parts if part]  # Loại bỏ các chuỗi rỗng

# Hàm dịch một lệnh thành mã nhị phân tương ứng
def assemble_instruction(instruction):
    parts = parse_instruction(instruction)  # Phân tích lệnh thành các phần thành phần
    if not parts:  # Nếu lệnh rỗng, báo lỗi
        raise ValueError(f"Lệnh rỗng: {instruction}")
    if parts[0] not in opcodes:  # Nếu lệnh không hợp lệ, báo lỗi
        raise ValueError(f"Lệnh không hợp lệ: {parts[0]}")
    opcode = opcodes[parts[0]]  # Lấy opcode của lệnh

    # Kiểm tra nếu lệnh thuộc loại R-type
    if parts[0] in functs:  
        funct = functs[parts[0]]  # Lấy mã chức năng (funct) của lệnh
        if parts[0] == 'jr':  # Nếu là lệnh 'jr'
            rs = registers[parts[1]]  # Lấy mã nhị phân của thanh ghi rs
            return f"{opcode}{rs}000000000000000{funct}"  # Kết hợp thành mã nhị phân hoàn chỉnh
        else:  # Nếu là các lệnh R-type khác
            rd = registers[parts[1]]  # Lấy mã nhị phân của thanh ghi đích (rd)
            rs = registers[parts[2]]  # Lấy mã nhị phân của thanh ghi nguồn (rs)
            rt = registers[parts[3]]  # Lấy mã nhị phân của thanh ghi nguồn (rt)
            return f"{opcode}{rs}{rt}{rd}00000{funct}"  # Kết hợp thành mã nhị phân hoàn chỉnh

    # Kiểm tra nếu lệnh thuộc loại J-type (nhảy tới địa chỉ)
    elif parts[0] in ['j', 'jal']:  
        address = format(int(parts[1]), '026b')  # Chuyển đổi địa chỉ thành chuỗi nhị phân 26 bit
        return f"{opcode}{address}"  # Kết hợp thành mã nhị phân hoàn chỉnh

    # Nếu là lệnh I-type (có giá trị immediate)
    else:  
        rt = registers[parts[1]]  # Lấy mã nhị phân của thanh ghi đích (rt)
        if parts[0] in ['lw', 'sw']:  # Nếu là lệnh tải/lưu (load/store)
            immediate = parts[2]  # Lấy giá trị immediate
            rs = registers[parts[3]]  # Lấy mã nhị phân của thanh ghi cơ sở (rs)
        else:  # Các lệnh I-type khác
            rs = registers[parts[2]]  # Lấy mã nhị phân của thanh ghi nguồn (rs)
            immediate = parts[3]  # Lấy giá trị immediate
        immediate = format(int(immediate) & 0xffff, '016b')  # Chuyển đổi immediate thành chuỗi nhị phân 16 bit
        return f"{opcode}{rs}{rt}{immediate}"  # Kết hợp thành mã nhị phân hoàn chỉnh

# Hàm dịch toàn bộ chương trình từ danh sách các lệnh
def assemble_program(replaced_lines):
    machine_code_lines = []  # Danh sách để lưu các dòng mã máy đã dịch
    for line in replaced_lines:  # Duyệt qua từng dòng lệnh đã thay thế nhãn
        try:
            machine_code_lines.append(assemble_instruction(line))  # Thử dịch từng lệnh thành mã máy
        except Exception as e:
            print(f"Lỗi khi dịch lệnh '{line}': {e}")  # Nếu có lỗi, in ra thông báo lỗi
    return machine_code_lines  # Trả về danh sách các dòng mã máy

# Hàm chính để đọc file đầu vào, xử lý mã hợp ngữ và ghi file đầu ra
def main(input_file, output_file):
    with open(input_file, 'r') as f:
        assembly_lines = f.readlines()  # Đọc các dòng từ file đầu vào

    cleaned_lines = remove_comments_and_empty_lines(assembly_lines)  # Loại bỏ các bình luận và dòng trống
    label_addresses, filtered_lines = calculate_label_addresses(cleaned_lines)  # Tính toán địa chỉ nhãn và lọc bỏ định nghĩa nhãn
    replaced_lines = replace_labels(filtered_lines, label_addresses)  # Thay thế nhãn bằng địa chỉ tương ứng
    machine_code_lines = assemble_program(replaced_lines)  # Dịch chương trình thành mã máy

    with open(output_file, 'w') as f:
        for line in machine_code_lines:
            f.write(line + '\n')  # Ghi các dòng mã máy vào file đầu ra

if __name__ == "__main__":
    main('input.asm', 'output.bin')

