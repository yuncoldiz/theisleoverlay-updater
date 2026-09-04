"""
Script khôi phục dự phòng an toàn (Rollback) cho gói nâng cấp v2
Dùng để hoàn tác lại toàn bộ các file về trạng thái trước khi nâng cấp UI, Auto-Updater và FPS.
"""
import os
import shutil

backup_dir = "backup_full_upgrade_v2"

file_map = {
    os.path.join(backup_dir, "main.cjs"): os.path.join("src_extracted", "electron", "main.cjs"),
    os.path.join(backup_dir, "preload.cjs"): os.path.join("src_extracted", "electron", "preload.cjs"),
    os.path.join(backup_dir, "index.html"): os.path.join("src_extracted", "dist", "index.html"),
    os.path.join(backup_dir, "index-hNLmMOku.css"): os.path.join("src_extracted", "dist", "assets", "index-hNLmMOku.css"),
    os.path.join(backup_dir, "TheIsleVn-BanhMi.exe"): "TheIsleVn-BanhMi.exe",
    os.path.join(backup_dir, "setup.iss"): "setup.iss",
    os.path.join(backup_dir, "pack_secure_app.py"): "pack_secure_app.py",
    os.path.join(backup_dir, "app.asar"): os.path.join("resources", "app.asar"),
}

print("=== BẮT ĐẦU HOÀN TÁC TỪ BẢN SAO LƯU V2 ===")
success = True
for src, dst in file_map.items():
    if os.path.exists(src):
        try:
            shutil.copy2(src, dst)
            print(f"[OK] Đã khôi phục: {dst}")
        except Exception as e:
            print(f"[LỖI] Không thể khôi phục {dst}: {e}")
            success = False
    else:
        print(f"[CẢNH BÁO] Không tìm thấy file: {src}")
        success = False

if success:
    print("\n=== HOÀN TẤT KHÔI PHỤC THÀNH CÔNG! ===")
else:
    print("\n=== CÓ LỖI XẢY RA TRONG QUÁ TRÌNH KHÔI PHỤC ===")
