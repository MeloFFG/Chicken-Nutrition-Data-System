# gsheet_utils.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========== Google Sheet 配置 ==========
GOOGLE_SHEET_ID = "1L0k6p3F13X_JXYXHvmTsnItt4ucFcv5aGvphbekkKBg"
GOOGLE_KEY_FILE = "data-collection-system-457718-176b52bb4b01.json"

# ========== 初始化 gspread 客户端 ==========
def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_KEY_FILE, scope)
    return gspread.authorize(creds)

# ========== 写入数据到 worksheet ==========
def append_record_to_worksheet(worksheet_name, record: dict):
    client = get_gsheet_client()
    worksheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(worksheet_name)

    # 读取 header 行
    headers = worksheet.row_values(1)
    if not headers:
        headers = list(record.keys())
        worksheet.append_row(headers)

    # 确保列顺序一致
    row = [record.get(col, "") for col in headers]
    worksheet.append_row(row)
