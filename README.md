# Flask 應用程式專案 (Port 19191)

本專案是一個精心架構、將程式碼與測試進行分離設計的 Python Flask 專案基礎範本。

## 📁 專案目錄結構

```
CKC_101/
├── src/                      # 核心開發與生產環境程式碼
│   ├── __init__.py           # Flask 應用程式工廠 (App Factory)
│   ├── config.py             # 專案環境配置 (預設設定為 Port 19191)
│   ├── routes.py             # 路由與 API 邏輯 (包含首頁及健康檢查 API)
│   └── templates/            # Jinja2 網頁模板
│       └── index.html        # 高度自訂、美觀且具備互動性的儀表板
├── test/                     # Pytest 單元測試程式碼
│   ├── __init__.py           # 單元測試套件初始化
│   ├── conftest.py           # 提供單元測試所需的 pytest fixtures (app, client)
│   └── test_routes.py        # 路由與功能自動化測試案例
├── requirements.txt          # Python 依賴套件清單 (Flask, pytest)
├── run.py                    # 專案啟動入口 (將服務啟動於 19191 連接埠)
└── README.md                 # 專案說明文件
```

---

## 🚀 快速開始指南

### 1. 安裝環境依賴

建議在虛擬環境 (Virtual Environment) 下執行：

```powershell
pip install -r requirements.txt
```

### 2. 執行自動化測試

我們使用 `pytest` 進行單元測試。測試程式碼被隔離在 `test/` 目錄中，您可以直接在終端機執行：

```powershell
python -m pytest
```

### 3. 啟動伺服器

執行主入口程式 `run.py` 以啟動 Flask 服務：

```powershell
python run.py
```

啟動後，開啟瀏覽器造訪以下網址：
- 🖥️ **精美儀表板首頁**: [http://127.0.0.1:19191](http://127.0.0.1:19191)
- 🔌 **API 健康狀態檢查**: [http://127.0.0.1:19191/api/health](http://127.0.0.1:19191/api/health)
