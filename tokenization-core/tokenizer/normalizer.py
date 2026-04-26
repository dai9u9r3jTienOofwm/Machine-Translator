#Chuẩn hóa text trước khi tokenize
#Input không phải string thì báo lỗi rõ ràng.
#Normalize được tiếng Việt.
#Normalize được chữ có dấu.
#Không làm mất emoji.
#Có unit test cho composed/decomposed Unicode.
#Cùng một text sau normalize phải cho output ổn định.