#!/usr/bin/env python3
"""
部署前檢查清單 - Zeabur 部署驗證工具

用法:
  python scripts/deploy_check.py
"""

import os
import sys
import subprocess
from pathlib import Path


def check_file_exists(path: str, description: str) -> bool:
    """檢查文件是否存在"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    if not exists:
        print(f"   期望位置: {path}")
    return exists


def check_file_content(path: str, keyword: str, description: str) -> bool:
    """檢查文件是否包含特定內容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            found = keyword in content
            status = "✅" if found else "❌"
            print(f"{status} {description}")
            if not found:
                print(f"   未找到: '{keyword}'")
            return found
    except Exception as e:
        print(f"❌ {description} - 讀取失敗: {e}")
        return False


def check_command(cmd: str, description: str) -> bool:
    """檢查命令是否可用"""
    result = subprocess.run(f"which {cmd}", shell=True, capture_output=True)
    exists = result.returncode == 0
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    if not exists:
        print(f"   無法找到命令: {cmd}")
    return exists


def main():
    print("\n" + "=" * 60)
    print("🏥 Taiwan Health MCP - 部署前檢查")
    print("=" * 60 + "\n")

    base_dir = Path(__file__).parent.parent
    os.chdir(base_dir)

    all_passed = True

    # 1. 檢查基本文件
    print("📋 基本文件檢查:")
    all_passed &= check_file_exists("requirements.txt", "requirements.txt 存在")
    all_passed &= check_file_exists("Dockerfile", "Dockerfile 存在")
    all_passed &= check_file_exists("docker-compose.yml", "docker-compose.yml 存在")
    all_passed &= check_file_exists("zeabur.json", "zeabur.json 存在")
    all_passed &= check_file_exists("src/server.py", "src/server.py 存在")
    all_passed &= check_file_exists("src/run_with_http.py", "src/run_with_http.py 存在")

    # 2. 檢查依賴包
    print("\n📦 依賴包檢查:")
    all_passed &= check_file_content("requirements.txt", "mcp", "MCP 框架")
    all_passed &= check_file_content("requirements.txt", "fastapi", "FastAPI")
    all_passed &= check_file_content("requirements.txt", "starlette", "Starlette")
    all_passed &= check_file_content("requirements.txt", "httpx", "HTTPX")
    all_passed &= check_file_content("requirements.txt", "uvicorn", "Uvicorn")

    # 3. 檢查 Dockerfile 配置
    print("\n🐳 Docker 配置檢查:")
    all_passed &= check_file_content("Dockerfile", "FROM python:3.10", "Python 3.10 基礎映像")
    all_passed &= check_file_content("Dockerfile", "MCP_TRANSPORT=http", "MCP_TRANSPORT 環境變數")
    all_passed &= check_file_content("Dockerfile", "HEALTHCHECK", "健康檢查配置")

    # 4. 檢查啟動腳本
    print("\n🚀 啟動腳本檢查:")
    all_passed &= check_file_content("src/run_with_http.py", "streamable-http", "使用 HTTP 傳輸")
    all_passed &= check_file_content("src/run_with_http.py", "logging", "日誌配置")
    all_passed &= check_file_content("src/run_with_http.py", "error handling", "錯誤處理")

    # 5. 檢查 Zeabur 配置
    print("\n☁️  Zeabur 配置檢查:")
    all_passed &= check_file_content("zeabur.json", "8000", "埠號 8000")
    all_passed &= check_file_content("zeabur.json", "healthcheck", "健康檢查")

    # 6. 檢查系統命令
    print("\n🛠️  系統命令檢查:")
    all_passed &= check_command("docker", "Docker 已安裝")
    all_passed &= check_command("git", "Git 已安裝")

    # 7. 檢查數據文件
    print("\n📊 數據文件檢查:")
    data_dir = Path("data")
    if data_dir.exists():
        xlsx_files = list(data_dir.glob("*.xlsx"))
        if xlsx_files:
            print(f"✅ 找到 ICD-10 Excel 文件: {xlsx_files[0].name}")
        else:
            print("❌ 未找到 ICD-10 Excel 文件")
            all_passed = False
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            print(f"✅ 找到實驗室參考值 CSV 文件: {len(csv_files)} 個")
        else:
            print("⚠️  未找到 CSV 文件 (可選)")
    else:
        print("❌ 找不到 data 目錄")
        all_passed = False

    # 8. 檢查 Git 狀態
    print("\n📝 Git 狀態檢查:")
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    if result.stdout:
        print("⚠️  有未提交的更改:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
        print("\n   建議: 在部署前提交這些更改")
    else:
        print("✅ 工作目錄乾淨 (全部已提交)")

    # 最終結果
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有檢查通過！")
        print("\n後續步驟:")
        print("  1. git push origin main")
        print("  2. 在 Zeabur 部署控制台檢查構建狀態")
        print("  3. 驗證服務在線:")
        print("     curl https://mauricemedmcp.zeabur.app/mcp")
    else:
        print("❌ 存在未通過的檢查項目")
        print("\n請修復上述問題後重新運行此檢查")
        return 1

    print("=" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())