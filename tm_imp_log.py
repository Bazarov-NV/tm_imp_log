import requests
import re


TELEGRAM_BOT_TOKEN = "8341323223:AAFiBauHL7nmn6CWPh4MQ6opkvxMTwGSXT0"  # !заменить! Telegrам bot's token 
TELEGRAM_CHAT_ID = "7290071868"    # !заменить! Telegram chat ID
ERROR_FILE_PATH = ".\\teammaster_imp.exe.log"       # Путь к файлу лога
POSITION_ERROR_FILE = 'pos_err.txt' # Файл, где запоминаем последнюю обработанную строку лога, чтобы не дублировать сообщения 

def send_telegram_message(message):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            print("Message sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

def get_line_pos_errors(file_pos):     
  try:  
     pos_err = ""
     try:
          f = open(file_pos) 
     except FileNotFoundError:
          f = open(file_pos, "w") 
          f.write("0")
          f.close()
          f = open(file_pos) 

     s1 = f.read()
     try:
       pos_err = s1.strip()      
     except:
       pos_err = ""
  finally:     
     f.close()  
  return pos_err
     

def write_line_pos_errors(file_pos, pos_err):     
     with open(file_pos, "w") as f:
       f.write(str(pos_err))
     f.close()  
  
def analyze_and_send_errors(file_path):
        errors = []     
        pos_err = get_line_pos_errors (POSITION_ERROR_FILE)
        try:
            f = open(file_path, 'r')                                                
            list_errors = f.readlines()
            f.close
            num_lines = len(list_errors)   

            try:
              k2 = list_errors.index(pos_err+"\n") + 2
            except:
              k2 = 0 

            if k2 > num_lines: k2 = num_lines
            while k2 != num_lines: 
                if re.search("^ERR [2-9][0-9].*$",list_errors[k2]):
                    errors.append(list_errors[k2].strip())                    
                k2 = k2 + 1            
            if errors:
                error_summary = "Найдены ошибки:\n" + "\n".join(errors)
                send_telegram_message(error_summary)                
            else:
                send_telegram_message("В log файле нет новых ошибок.")
            if list_errors[k2-1].strip() != "":
                write_line_pos_errors(POSITION_ERROR_FILE, list_errors[num_lines-1].strip())
            else: write_line_pos_errors(POSITION_ERROR_FILE, list_errors[num_lines-2].strip())   
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        f.close()  
if __name__ == "__main__":
        analyze_and_send_errors(ERROR_FILE_PATH)