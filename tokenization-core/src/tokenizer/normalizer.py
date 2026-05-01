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
    
class Normalier2:
    def __init__(self):
        self.whitespace = re.compile(r'\s+')
    def read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raw = path.read_bytes()
            encoding = chardet.detect(raw)['encoding'] or 'utf-8'
            return raw.decode(
                encoding,
                errors='replace'
            )
    def clean_text(self, text: str)->str:
        text = normalize('NFC', text)
        text = self.whitespace.sub(' ', text)
        return text
    def validate_text(self, text: str):
        if not text:
            raise ValueError("Empty text")
        if not is_normalized("NFC", text):
            raise ValueError("Text not NFC normalized")
    def process_file(self, path: Path):
        text = self.read_text(path)
        text = self.clean_text(text)
        self.validate_text(text)
        try:
            lang = detect(text)
        except:
            lang = "unknown"
        return {
            "path": str(path),
            "text": text,
            "language": lang,
        }
    def process_directory(self, directory):
        for path in Path(directory).rglob("*.txt"):
            try:
                yield self.process_file(path)

            except Exception as e:
                print(f"[ERROR] {path}: {e}")
        
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