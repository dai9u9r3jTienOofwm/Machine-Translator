#Tách text thành các mảnh ban đầu trước khi đưa vào model tokenizer
#Tách được theo khoảng trắng.
#Tách được punctuation.
#Giữ được offset (start, end) trong text gốc.
#Không làm mất token.
#Không crash với tiếng Việt, emoji, URL, email.
#Có test offset.