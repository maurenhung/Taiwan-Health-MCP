# 貢獻指南

感謝您對 Taiwan Health MCP 的興趣！本指南將幫助您了解如何對本專案做出貢獻。

## 📋 目錄

- [行為準則](#行為準則)
- [開始貢獻](#開始貢獻)
- [開發流程](#開發流程)
- [提交 Pull Request](#提交-pull-request)
- [提交問題](#提交問題)
- [代碼規範](#代碼規範)
- [提交訊息規範](#提交訊息規範)

---

## 行為準則

### 我們的承諾

為建立開放友好的社區，我們承諾：

- 尊重所有參與者，無論身份、經驗水平、種族、民族、性別或其他特徵
- 營造包容的環境，歡迎各種不同的觀點
- 接受建設性批評，並共同進步

### ❌ 不可接受的行為

- 性化語言或意象的使用及不受歡迎的性關注
- 人身攻擊、侮辱性評論或仇恨言論
- 公開或私下騷擾
- 發佈他人私密信息而未得明確許可
- 其他在專業環境中不適當的行為

### 執行與報告

不當行為將由社區領導者審查。報告方式：

- 📧 [support@healthymind-tech.com](mailto:support@healthymind-tech.com)
- 🐛 [GitHub Issue](https://github.com/audi0417/Taiwan-Health-MCP/issues)

所有投訴將被審查和調查，維護者有義務對報告人保密。

---

## 開始貢獻

### 前置需求

確保您已安裝：

- Python 3.8 或更高版本
- Git
- Docker（推薦用於測試）

### 環境設置

```bash
# 1. Fork 本倉庫到您的 GitHub 帳戶
# 2. Clone 您的 Fork
git clone https://github.com/YOUR_USERNAME/Taiwan-Health-MCP.git
cd Taiwan-Health-MCP

# 3. 創建開發分支
git checkout -b feature/your-feature-name

# 4. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 5. 安裝開發依賴
pip install -r requirements.txt
pip install -r requirements-docs.txt

# 6. 安裝 pre-commit hooks（可選）
pip install pre-commit
pre-commit install
```

---

## 開發流程

### 1. 選擇一個任務

查看 [GitHub Issues](https://github.com/audi0417/Taiwan-Health-MCP/issues) 找尋待解決的問題。您也可以：

- 新增功能
- 修復 Bug
- 改進文檔
- 優化性能

### 2. 建立功能分支

```bash
git checkout -b feature/descriptive-name
```

分支命名規範：

- `feature/new-feature` - 新功能
- `bugfix/bug-description` - 錯誤修復
- `docs/documentation-update` - 文檔更新
- `refactor/code-improvement` - 代碼重構

### 3. 開發與測試

進行您的更改，並確保：

```bash
# 運行現有測試
python -m pytest

# 檢查代碼質量
python -m pylint src/

# 格式化代碼
python -m black src/
```

### 4. 提交變更

遵循提交訊息規範（見下方）：

```bash
git add .
git commit -m "feat: Add new feature description"
git push origin feature/your-feature-name
```

---

## 提交 Pull Request

### PR 檢查清單

提交 PR 前，請確保：

- [ ] 代碼基於最新的 `main` 分支
- [ ] 已運行所有測試且通過
- [ ] 添加了新功能的測試用例
- [ ] 更新了相關文檔
- [ ] 遵循代碼規範
- [ ] 提交訊息清晰描述了變更

### PR 描述模板

```markdown
## 描述
簡要描述您的變更。

## 相關 Issue
關閉 #（issue number）

## 變更類型
- [ ] 新功能
- [ ] 錯誤修復
- [ ] 文檔更新
- [ ] 性能改進
- [ ] 代碼重構

## 測試
描述您進行的測試。

## 截圖（如適用）
添加相關截圖。
```

### 審查流程

1. 至少一名維護者審查 PR
2. 根據反饋進行修改
3. 獲得批准後合併至 `main` 分支

---

## 提交問題

### Bug 報告

提交 Bug 前，請檢查是否已存在類似問題。

提供以下信息：

- 環境詳情（OS、Python 版本、Docker 版本等）
- 詳細的重現步驟
- 預期行為
- 實際行為
- 相關日誌或錯誤信息

### 功能請求

提交功能請求時，請包括：

- 功能的清晰描述
- 為什麼您認為此功能有用
- 可能的實現方案

---

## 代碼規範

### Python 代碼風格

我們遵循 [PEP 8](https://pep8.org/) 標準：

```python
# 好的
def calculate_icd_codes(condition: str, max_results: int = 10) -> dict:
    """Calculate ICD codes for a given condition.

    Args:
        condition: Medical condition name
        max_results: Maximum number of results

    Returns:
        Dictionary containing ICD codes
    """
    results = []
    # Implementation here
    return {"codes": results}


# 不好
def calc(c,m=10):
    r = []
    #implement
    return r
```

### 文檔字符串

使用 Google 風格的文檔字符串：

```python
def search_drug(keyword: str) -> list:
    """搜尋藥品。

    Args:
        keyword: 藥品名稱或 ID

    Returns:
        符合搜尋條件的藥品列表

    Raises:
        ValueError: 若關鍵字為空

    Example:
        >>> results = search_drug("普拿疼")
        >>> print(results[0]['name'])
    """
    pass
```

### 類型提示

使用類型提示提高代碼可讀性：

```python
from typing import Dict, List, Optional

def process_data(
    data: List[Dict[str, str]],
    filter_key: Optional[str] = None
) -> Dict[str, List]:
    """Process medical data."""
    pass
```

---

## 提交訊息規範

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 類型

- `feat` - 新功能
- `fix` - 錯誤修復
- `docs` - 文檔更新
- `style` - 代碼風格（不影響功能）
- `refactor` - 代碼重構
- `perf` - 性能改進
- `test` - 添加或修改測試
- `chore` - 構建過程、依賴更新等

### 例子

```
feat(icd-service): Add ICD-10-CM code validation

- Implement validation logic for ICD-10-CM codes
- Add unit tests for validation
- Update documentation

Closes #123
```

```
fix(drug-service): Handle missing drug metadata

Previous implementation would crash when drug metadata was unavailable.
Now returns graceful error message and logs warning.

Fixes #456
```

---

## 文檔貢獻

### 編輯文檔

文檔使用 Markdown 和 MkDocs：

```bash
# 安裝 MkDocs 依賴
pip install -r requirements-docs.txt

# 本地預覽文檔
mkdocs serve

# 開啟 http://localhost:8000
```

### 文檔結構

```
docs/
├── index.md                 # 首頁
├── getting-started.md       # 快速開始
├── architecture/            # 架構文檔
├── modules/                 # 模組文檔
├── guides/                  # 使用指南
├── api/                     # API 參考
└── faq/                     # 常見問題
```

### 文檔規範

- 使用繁體中文
- 標題層級清晰
- 包含代碼示例
- 添加相關連結

---

## 獲得幫助

- 📖 查看 [文檔](https://github.com/audi0417/Taiwan-Health-MCP)
- 💬 開啟 [GitHub Discussion](https://github.com/audi0417/Taiwan-Health-MCP/discussions)
- 📧 聯絡維護者: [support@healthymind-tech.com](mailto:support@healthymind-tech.com)

---

## 許可

對本專案的貢獻表示您同意在 MIT 許可證下發佈您的貢獻。

### 行為準則歸屬

本行為準則改編自 [Contributor Covenant][homepage]，版本 2.0：
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html

社區影響準則受 [Mozilla 行為準則執行階梯](https://github.com/mozilla/diversity) 啟發。

有關本行為準則常見問題的答案，請參閱 [Contributor Covenant FAQ](https://www.contributor-covenant.org/faq)。

[homepage]: https://www.contributor-covenant.org

---

感謝您的貢獻！ 🎉
