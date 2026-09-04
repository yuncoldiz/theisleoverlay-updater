"""
Script khôi phục dự phòng an toàn (Rollback)
Dùng để hoàn tác lại toàn bộ các file về trạng thái trước khi loại bỏ Gacha-HUD
"""
import os
import shutil

backup_dir = "backup_gacha_cleanup"

file_map = {
    os.path.join(backup_dir, "TheIsleVn-BanhMi.exe"): "TheIsleVn-BanhMi.exe",
    os.path.join(backup_dir, "setup.iss"): "setup.iss",
    os.path.join(backup_dir, "pack_secure_app.py"): "pack_secure_app.py",
    os.path.join(backup_dir, "app.asar"): os.path.join("resources", "app.asar"),
}

print("=== BẮT ĐẦU HOÀN TÁC TỪ BẢN SAO LƯU ===")
success = True
for src, dst in file_map.items():
    if os.path.exists(src):
        try:
            shutil.copy2(src, dst)
            print(f"[OK] Đã khôi phục: {dst} ({os.path.getsize(dst)} bytes)")
        except Exception as e:
            print(f"[LỖI] Không thể khôi phục {dst}: {e}")
            success = False
    else:
        print(f"[CẢNH BÁO] Không tìm thấy file sao lưu: {src}")
        success = False

# Khôi phục file backup nếu có trong backup_dir
for extra in ["index-CealnApy.js.backup_pre_hotkey", "Uninstall TheIsleVn-BanhMi.exe"]:
    src = os.path.join(backup_dir, extra)
    if os.path.exists(src):
        if extra.startswith("index-"):
            dst = os.path.join("src_extracted", "dist", "assets", extra)
        else:
            dst = extra
        try:
            shutil.copy2(src, dst)
            print(f"[OK] Đã khôi phục file phụ: {dst}")
        except Exception as e:
            print(f"[LỖI] {e}")

if success:
    print("\n=== HOÀN TẤT KHÔI PHỤC THÀNH CÔNG! ===")
else:
    print("\n=== CÓ LỖI XẢY RA TRONG QUÁ TRÌNH KHÔI PHỤC ===")
