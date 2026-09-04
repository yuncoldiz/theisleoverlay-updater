"""
Script khôi phục dự phòng an toàn (Rollback) từ bản sao lưu v1.0.2
Dùng để hoàn tác toàn bộ các file về trạng thái trước khi nâng cấp lên v1.0.3.
"""
import os
import shutil

backup_dir = "backup_v1.0.2"

file_map = {
    os.path.join(backup_dir, "main.cjs"): os.path.join("src_extracted", "electron", "main.cjs"),
    os.path.join(backup_dir, "preload.cjs"): os.path.join("src_extracted", "electron", "preload.cjs"),
    os.path.join(backup_dir, "index.html"): os.path.join("src_extracted", "dist", "index.html"),
    os.path.join(backup_dir, "index-CealnApy.js"): os.path.join("src_extracted", "dist", "assets", "index-CealnApy.js"),
    os.path.join(backup_dir, "package.json"): os.path.join("src_extracted", "package.json"),
    os.path.join(backup_dir, "setup.iss"): "setup.iss",
    os.path.join(backup_dir, "app.asar"): os.path.join("resources", "app.asar"),
}

print("=== BẮT ĐẦU HOÀN TÁC TỪ BẢN SAO LƯU v1.0.2 ===")
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
        print(f"[CẢNH BÁO] Không tìm thấy file nguồn: {src}")
        success = False

if success:
    print("\n=== HOÀN TẤT KHÔI PHỤC v1.0.2 THÀNH CÔNG! ===")
else:
    print("\n=== CÓ MỘT SỐ CẢNH BÁO HOẶC LỖI TRONG QUÁ TRÌNH KHÔI PHỤC ===")
