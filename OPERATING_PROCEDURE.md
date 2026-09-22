# SỔ TAY QUY TRÌNH VẬN HÀNH TỪ XA (REMOTE OPERATING PLAYBOOK)
## TheIsleOverlay - Bánh Mì Biết Chơi

> **Mục đích:** Tài liệu này ghi lại toàn bộ cấu trúc dữ liệu và quy trình chuẩn để thay đổi mọi thông tin của ứng dụng từ xa qua mạng (Online) **MÀ KHÔNG CẦN** phải build lại app hay gửi file `Setup.exe` mới cho người chơi.
> Khi Admin cần đổi bất kỳ nội dung nào, chỉ cần nhắn 1 câu, AI Assistant sẽ tự động thực hiện và đồng bộ lên hệ thống trong 30 giây.

---

## 1. File Cấu Hình Online Trung Tâm (`remote_config.json`)
- **Kho lưu trữ (Repository):** `https://github.com/yuncoldiz/theisleoverlay-updater`
- **Đường dẫn file trực tuyến (Raw URL):**
  `https://raw.githubusercontent.com/yuncoldiz/theisleoverlay-updater/main/remote_config.json`
- **File cục bộ dự phòng:** `resources/remote_config.json`

---

## 2. Cấu Trúc Toàn Bộ Các Tham Số Có Thể Thay Đổi Online

```json
{
  "gateSeason": 1,
  "adminKey": "BANHMI-ADMIN-KEY1",
  "youtube": "https://www.youtube.com/@BanhMiBietChoi",
  "facebook": "https://www.facebook.com/ngocdocbanhmi",
  "tiktok": "https://www.tiktok.com/@contentwithbanhmi",
  "discord": "https://discord.gg/banhmibietchoi",
  "announcement": "Chào mừng anh em đến với TheIsleVN - YTB BanhMi!",
  "bank": {
    "bankName": "TPBank",
    "accountNumber": "0888888888",
    "accountName": "YTB BANHMI"
  },
  "qrImageUrl": ""
}
```

---

## 3. Danh Mục Các Tình Huống Vận Hành Chuẩn

### Tình huống 1: Đổi Link Mạng Xã Hội hoặc Kéo View Video Mới
- **Khi nào dùng:** Khi bạn ra video YouTube mới, clip TikTok mới, đổi link mời Discord bị hết hạn, hoặc đổi link bài viết Fanpage cần đẩy tương tác.
- **Cách Admin yêu cầu:**
  > *"Đổi link YouTube sang video mới này: https://youtu.be/..."*
  > hoặc *"Cập nhật link Discord mới: https://discord.gg/..."*
- **Quy trình xử lý của AI:**
  1. Cập nhật trường `youtube`, `tiktok`, `facebook`, hoặc `discord` trong `remote_config.json`.
  2. Commit và đẩy lên GitHub: `git commit -m "Update social links" && git push origin main`.
  3. Xong ngay trong 30 giây! Người chơi mở app bấm nút sẽ dẫn thẳng đến link mới.

---

### Tình huống 2: Bắt Đầu Mùa Mới (Reset Bắt Mọi Người Làm Lại Nhiệm Vụ)
- **Khi nào dùng:** Sau khoảng 1 - 2 tháng, hoặc khi bạn mở sự kiện mới, muốn toàn bộ cộng đồng bấm ủng hộ lại 1 lần để duy trì tương tác.
- **Cách Admin yêu cầu:**
  > *"Reset mùa nhiệm vụ mới cho tôi"* hoặc *"Tăng season nhiệm vụ lên mùa 2"*
- **Quy trình xử lý của AI:**
  1. Tăng số `gateSeason` trong `remote_config.json` từ `1` lên `2` (hoặc `3`, `4`...).
  2. Có thể kết hợp đổi kèm link video mới nhất.
  3. Đẩy lên GitHub `git push origin main`.
  4. Toàn bộ người chơi khi bật app sẽ thấy bảng nhiệm vụ kích hoạt lại.
  5. **Lưu ý an toàn:** Máy của Admin (đã kích hoạt Key Admin) sẽ tự động miễn trừ, không bao giờ bị dính reset.

---

### Tình huống 3: Đổi Mã Key Admin / VIP
- **Khi nào dùng:** Khi bạn muốn đổi sang một mã bí mật mới hoặc không muốn người khác dùng mã cũ nữa.
- **Cách Admin yêu cầu:**
  > *"Đổi key admin thành: BANHMI-VIP-2026"*
- **Quy trình xử lý của AI:**
  1. Đổi giá trị `"adminKey"` trong `remote_config.json`.
  2. Đẩy lên GitHub. Mã mới có hiệu lực ngay lập tức với tất cả các máy.

---

### Tình huống 4: Thay Đổi Thông Tin Donate (Ngân hàng / STK / QR)
- **Khi nào dùng:** Khi bạn đổi số tài khoản ngân hàng nhận donate hoặc đổi mã VietQR.
- **Cách Admin yêu cầu:**
  > *"Đổi STK nhận donate sang MBBank STK: 123456789 chủ TK: NGUYEN VAN A"*
- **Quy trình xử lý của AI:**
  1. Cập nhật object `"bank"` trong `remote_config.json`.
  2. Đẩy lên GitHub. Mọi widget Donate trên app (Thẻ ID khủng long, Tab Cài Đặt) sẽ tự động hiển thị STK mới.

---

### Tình huống 5: Phát Thông Báo Khẩn / Lời Nhắn Toàn App (Broadcast Announcement)
- **Khi nào dùng:** Khi cần thông báo lịch livestream tối nay, thông báo game The Isle đang bảo trì, hoặc chúc mừng lễ/Tết.
- **Cách Admin yêu cầu:**
  > *"Gửi thông báo toàn app: Tối nay 20h Bánh Mì live stream The Isle trên kênh nhé anh em!"*
- **Quy trình xử lý của AI:**
  1. Đổi nội dung trường `"announcement"` trong `remote_config.json`.
  2. Đẩy lên GitHub. Banner thông báo trên app của tất cả người chơi sẽ tự cập nhật.

---

## 4. Cam Kết & Bảo Đảm Vận Hành
1. **Không can thiệp file cài:** Người dùng cuối không cần tải lại file `Setup.exe`.
2. **Khả năng dự phòng mất mạng (Offline Fallback):** Nếu mạng của người chơi bị rớt hoặc GitHub gặp sự cố, app sẽ tự động dùng cấu hình lưu cục bộ gần nhất, đảm bảo app không bao giờ bị crash hay đơ màn hình.
3. **Tốc độ phản hồi:** Mọi yêu cầu đổi cấu hình từ Admin chỉ mất dưới 1 phút để cập nhật trực tiếp.
