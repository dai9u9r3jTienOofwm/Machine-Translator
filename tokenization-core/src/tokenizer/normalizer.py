#Chuẩn hóa text trước khi tokenize
#Input không phải string thì báo lỗi rõ ràng.
#Normalize được tiếng Việt.
#Normalize được chữ có dấu.
#Không làm mất emoji.
#Có unit test cho composed/decomposed Unicode.
#Cùng một text sau normalize phải cho output ổn định.



from unicodedata import normalize, is_normalized
import re
import chardet
from pathlib import Path
import os
from datetime import datetime
from langdetect import detect

class Normalier:
    def __init__(self):
        self.texts = []
        self.cleaned_texts = []
        self.language = []
        self.whitespace_regex = r'[\t\r]'
    
    def normalize_encoding(self):
            for raw_data in Path("tokenization-core/Data/raw").rglob("*.txt"):
                try:
                    with open(raw_data,'r',encoding='utf-8') as file:
                        content = file.read()    
                
                except UnicodeDecodeError:
                    data = raw_data.read_bytes()
                    detector = chardet.detect(data)
                    encoding = detector['encoding']
                    
                    content = data.decode(encoding if encoding else 'utf-8', errors='ignore')
                    
                
                self.texts.append(content)    
                       
    def cleaning(self):
        for text in self.texts:
            text = normalize('NFC', text)
            cleaned_text = re.sub(self.whitespace_regex, ' ', text)
            
            self.cleaned_texts.append(cleaned_text)

    
    def validate_cleaned_texts(self):
        for i, text in enumerate(self.cleaned_texts):
            message_1 = ''
            words = text.split()
            is_sentence_ok = True
            
            for word in words:   
                c_len = len(word)
                b_len = len(word.encode('utf-8'))
                
                ratio = b_len / c_len if c_len > 0 else 0
                
                is_nfc = is_normalized('NFC', word)
                
                if not is_nfc:
                    is_sentence_ok = False
                    message_1 = f"Index {i}, NFD detect in word {words}, ratio {ratio}"
                    
            if is_sentence_ok and not text.isspace() and len(text) > 0:
                
                pass
            else:
                if not is_sentence_ok:
                   raise ValueError(message_1)
                if len(text) == 0 or text.isspace():
                    raise ValueError('Text contain no content!')   
                
            self.language.append(detect(text))          

a = Normalier()
a.normalize_encoding()
a.cleaning()
a.validate_cleaned_texts()


for i in range(len(a.cleaned_texts)):
    file_name = os.path.join(str(Path("tokenization-core/Data/interim")),f'text-{datetime.now()}.txt')
    with open(file_name,'w', encoding='utf-8') as file:
        if a.language[i] == 'en':
            file.write("Request: Translate this to Vietnamese\n")
        else:
            file.write("Request: Translate this to English\n")
               
        file.write("Raw text: \n")
        file.write(a.texts[i])
        
        file.write("\nCleaned text: \n")
        file.write(a.cleaned_texts[i])       
        
        
with open("tokenization-core/Data/interim/corpus.txt", 'w',encoding='utf-8') as file:
    for text in a.cleaned_texts:
        file.write(text + '\n')        