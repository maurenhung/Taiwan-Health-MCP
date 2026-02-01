# Taiwan Health MCP - 部署指南

## 快速修復清單

✅ **已修復的問題：**

1. **缺失依賴包** (requirements.txt)
   - 新增: `fastapi`, `starlette`, `httpx`, `pydantic`
   - 原因: HTTP/SSE 模式需要這些包

2. **改進啟動腳本** (run_with_http.py)
   - 使用 `streamable-http` 傳輸模式（更穩定）
   - 添加詳細日誌
   - 改進環境變數處理
   - 添加錯誤捕捉

3. **優化 Docker 配置** (Dockerfile)
   - 明確設置環境變數
   - 添加健康檢查
   - 安裝必要的系統依賴

4. **新增 Zeabur 配置** (zeabur.json)
   - 正確的埠號和協議
   - 健康檢查配置
   - 環境變數預設值

---

## 部署步驟 (Zeabur)

### 1. 推送更新到 GitHub

```bash
cd ~/GitHub/maurenhung/Taiwan-Health-MCP
git add requirements.txt Dockerfile src/run_with_http.py .dockerignore zeabur.json
git commit -m "修復: 添加缺失依賴、優化 HTTP 啟動配置、改進 Docker 部署"
git push origin main
```

### 2. Zeabur 部署設置

在 Zeabur 控制台：

**步驟 A: 連接 GitHub 倉庫**
- 選擇你的 Taiwan-Health-MCP 倉庫
- 授權 Zeabur 訪問

**步驟 B: 配置環境變數**
```
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_PATH=/mcp
PYTHONUNBUFFERED=1
```

**步驟 C: 構建和部署**
- Zeabur 會自動偵測 Dockerfile
- 使用 zeabur.json 的配置

### 3. 驗證部署

```bash
# 替換為你的實際域名
curl -v https://mauricemedmcp.zeabur.app/mcp

# 預期響應: 200 OK (MCP 伺服器就緒)
```

---

## 本地測試 (Docker)

### 構建並運行

```bash
cd ~/GitHub/maurenhung/Taiwan-Health-MCP

# 構建映像
docker build -t taiwan-health-mcp:latest .

# 運行容器
docker run -it \
  -p 8000:8000 \
  -e MCP_TRANSPORT=http \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=8000 \
  taiwan-health-mcp:latest
```

### 驗證本地運行

```bash
# 在另一個終端
curl http://localhost:8000/mcp

# 查看日誌
docker logs <container-id>
```

---

## 故障排除

### 問題 1: "Server disconnected"

**原因:** 依賴包缺失或啟動配置錯誤

**解決:**
```bash
# 檢查 requirements.txt 是否包含:
grep -E "fastapi|starlette|httpx|pydantic" requirements.txt

# 應該看到:
# fastapi~=0.104.1
# starlette~=0.27.0
# httpx~=0.25.0
# pydantic~=2.5.0
```

### 問題 2: "Data directory not found"

**原因:** Docker 未正確挂載數據目錄

**解決:**
```bash
# 確認 /app/data 存在
docker run -it taiwan-health-mcp ls -la /app/data

# 如果為空，檢查 Dockerfile COPY 命令
```

### 問題 3: 埠號衝突

**原因:** 埠 8000 已被占用

**解決:**
```bash
# 使用不同埠
docker run -p 9000:8000 taiwan-health-mcp:latest

# 或在環境變數中設置
-e MCP_PORT=9000
```

### 問題 4: 日誌中出現 ImportError

**原因:** Python 路徑配置錯誤

**檢查:**
```bash
# 進入容器
docker exec -it <container-id> bash

# 檢查 src 目錄
ls -la /app/src/

# 驗證 Python 路徑
python -c "import sys; print('\n'.join(sys.path))"
```

---

## 環境變數說明

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `MCP_TRANSPORT` | `http` | 傳輸模式 (http/sse/stdio) |
| `MCP_HOST` | `0.0.0.0` | 監聽 IP (0.0.0.0 允許外部連線) |
| `MCP_PORT` | `8000` | 監聽埠號 |
| `MCP_PATH` | `/mcp` | HTTP 端點路徑 |
| `PYTHONUNBUFFERED` | `1` | 禁用 Python 輸出緩衝 (改善日誌) |

---

## 在 Zeabur 上部署後的驗證

### 1. 檢查服務狀態

```bash
# 查看日誌
zeabur logs <service-name>

# 預期日誌輸出:
# ============================================================
# 🏥 Taiwan Health MCP Server - HTTP Mode
# ============================================================
# Starting server on http://0.0.0.0:8000
# MCP endpoint: http://0.0.0.0:8000/mcp
```

### 2. 測試 MCP 端點

```bash
# 替換為你的域名
curl -v https://mauricemedmcp.zeabur.app/mcp

# 健康檢查
curl https://mauricemedmcp.zeabur.app/mcp/health
```

### 3. 測試工具調用

```bash
# 測試搜索醫療代碼
curl -X POST https://mauricemedmcp.zeabur.app/mcp/tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_medical_codes",
    "args": {"keyword": "diabetes", "type": "diagnosis"}
  }'
```

---

## 性能優化建議

### 1. 資料庫快取

考慮在啟動時預加載常用數據：
```python
# src/server.py 初始化時
icd_service.preload_common_codes()
```

### 2. 記憶體管理

監控容器記憶體使用：
```bash
docker stats <container-id>
```

### 3. 日誌級別

生產環境使用 WARNING 級別：
```bash
# 環境變數
LOG_LEVEL=WARNING
```

---

## 連絡方式

如有問題，查看日誌：
```bash
zeabur logs <service-name> --follow
```

或本地測試：
```bash
docker run -it taiwan-health-mcp:latest
```

---

**更新時間**: 2026-02-01
**版本**: 1.1.0
**狀態**: ✅ 修復完成