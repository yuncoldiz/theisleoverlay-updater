import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path

def get_git_token():
    proc = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n",
        text=True,
        capture_output=True,
        check=True
    )
    for line in proc.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("Could not find GitHub password/token from git credential helper.")

def main():
    token = get_git_token()
    repo = "yuncoldiz/theisleoverlay-updater"
    tag = "v1.0.4"
    name = "TheIsleVN v1.0.4 - Bản Cập Nhật Hotfix F8 & Kéo Thả Map Radar"
    body = """## 🚀 Có gì mới trong phiên bản v1.0.4?

Bản cập nhật v1.0.4 tập trung sửa triệt để các lỗi liên quan đến phím tắt, nhận diện cửa sổ game và tính năng kéo thả bản đồ Radar:

### 🛠️ Các sửa lỗi & Cải tiến quan trọng:
* **Khắc phục lỗi phím F8**: 
  - Đưa phím F8 lên làm phím tắt toàn cục hoạt động độc lập mọi lúc.
  - Bạn có thể bật/tắt Dashboard F8 bất kỳ lúc nào, kể cả khi app đang ẩn hoặc khi đang tab ra ngoài Desktop, Chrome, Discord mà không lo bị liệt phím.
* **Nhận diện chính xác Game The Isle (Unreal Engine)**:
  - Tự động nhận diện tiến trình game ngay cả khi cửa sổ game không có tiêu đề.
  - Khi ở trong game và tắt bảng F8 đi, toàn bộ widget HUD (Máu, Thể lực, Đói, Khát, Radar map) vẫn hiển thị liên tục, sắc nét trên màn hình game.
* **Sửa triệt để lỗi Kéo thả Map Radar**:
  - Viết lại cơ chế kéo thả chuột đồng bộ, gắn sự kiện toàn màn hình giúp di chuyển vòng tròn map siêu mượt, không còn bị rớt chuột hay văng toạ độ.
  - Tích hợp bộ đệm Debounce khi lưu toạ độ vào ổ cứng, loại bỏ hoàn toàn hiện tượng giật đơ khung hình khi rê chuột.
  - Cố định lớp hiển thị trên cùng (Topmost) cho cửa sổ Radar.
* **Tối ưu hóa hiệu năng**:
  - Giảm tải thời gian phản hồi giao diện, các thao tác chuyển đổi diễn ra tức thì.

---
### 📦 Hướng dẫn cài đặt & Cập nhật:
* Tải file cài đặt **TheIsleVn-BanhMi-Setup.exe** bên dưới để cập nhật lên bản mới nhất.
* Hoặc người dùng đang sử dụng phiên bản cũ sẽ tự động nhận được thông báo cập nhật trực tiếp qua tính năng Auto-Update!
"""

    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "TheIsleOverlay-Publisher",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Check if release already exists
    print(f"Checking if release '{tag}' exists...")
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/tags/{tag}", headers=headers)
    release_data = None
    try:
        with urllib.request.urlopen(req) as resp:
            release_data = json.loads(resp.read().decode())
            print(f"Found existing release ID: {release_data['id']}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Release does not exist yet. Creating release...")
        else:
            raise

    # 2. Create release if not found
    if not release_data:
        payload = json.dumps({
            "tag_name": tag,
            "name": name,
            "body": body,
            "draft": False,
            "prerelease": False
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/releases",
            data=payload,
            headers={**headers, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            release_data = json.loads(resp.read().decode())
            print(f"Created release '{tag}' with ID: {release_data['id']}")

    upload_url_template = release_data["upload_url"].split("{")[0]

    # 3. Helper to upload asset
    def upload_asset(filepath: Path, content_type: str):
        asset_name = filepath.name
        print(f"Checking existing assets for '{asset_name}'...")
        for existing in release_data.get("assets", []):
            if existing["name"] == asset_name:
                print(f"Deleting older asset '{asset_name}' (ID: {existing['id']})...")
                del_req = urllib.request.Request(
                    f"https://api.github.com/repos/{repo}/releases/assets/{existing['id']}",
                    headers=headers,
                    method="DELETE"
                )
                urllib.request.urlopen(del_req)
                break

        print(f"Uploading '{asset_name}' ({filepath.stat().st_size / (1024*1024):.2f} MB)...")
        with open(filepath, "rb") as f:
            data = f.read()

        upload_url = f"{upload_url_template}?name={urllib.parse.quote(asset_name)}"
        upload_req = urllib.request.Request(
            upload_url,
            data=data,
            headers={
                **headers,
                "Content-Type": content_type,
                "Content-Length": str(len(data))
            }
        )
        with urllib.request.urlopen(upload_req) as resp:
            uploaded = json.loads(resp.read().decode())
            print(f"Uploaded '{asset_name}' successfully! ID: {uploaded['id']}")

    # 4. Upload latest.yml and Setup.exe
    upload_asset(Path("latest.yml"), "application/x-yaml")
    upload_asset(Path("TheIsleVn-BanhMi-Setup.exe"), "application/octet-stream")

    print("\n🎉 ALL ASSETS UPLOADED AND RELEASE PUBLISHED SUCCESSFULLY!")
    print(f"Release URL: {release_data['html_url']}")

if __name__ == "__main__":
    main()
