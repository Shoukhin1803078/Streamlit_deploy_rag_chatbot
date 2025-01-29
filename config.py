import os
from pathlib import Path

EXCEL_FILE = "user_credentials.xlsx"
if not Path(EXCEL_FILE).exists():
    import pandas as pd
    df = pd.DataFrame(columns=['username', 'password'])
    df.to_excel(EXCEL_FILE, index=False)