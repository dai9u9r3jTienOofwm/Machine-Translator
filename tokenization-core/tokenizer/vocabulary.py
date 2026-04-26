#Quản lý mapping giữa token và id.
#Special tokens luôn có id cố định.
#Token không có trong vocab trả về id của [UNK].
#Build vocab theo frequency.
#Có min_freq.
#Có max_size.
#Save/load JSON.
#Load xong encode phải giống trước khi save.
#Có test token -> id -> token.