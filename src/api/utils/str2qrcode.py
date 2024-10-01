from pathlib import Path
import pyqrcode
import datetime

work_dir = Path.cwd()

def str2qrcode(text:str) -> Path:
    qr_code = pyqrcode.create(text)
    prefix_file_name = int(datetime.datetime.now().timestamp())
    qr_code_file = work_dir.joinpath(f'{prefix_file_name}-qrcode.png')
    qr_code.png(qr_code_file,scale=5)
    return qr_code_file