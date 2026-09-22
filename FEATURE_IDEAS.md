# Danh sách Ý tưởng & Tính năng Chờ Triển Khai (Pending Features)

Tài liệu này lưu lại các ý tưởng và giải pháp kỹ thuật đã thống nhất với người dùng. Khi người dùng yêu cầu triển khai, sẽ thực hiện theo kế hoạch chi tiết dưới đây.

---

## 1. Phím tắt Reset & Reload Giao diện Trong Game (In-Game Reset & Reload Hotkey)

### Mục đích & Nhu cầu:
- Trong khi đang chơi The Isle, người dùng đôi khi gặp tình trạng HUD bị lag, mất kết nối WebSocket, đứng hiển thị chỉ số, hoặc vô tình kéo các panel (Stats, Prime, Radar) bay lệch ra khỏi tầm nhìn màn hình.
- Cần một cơ chế nhanh gọn bằng phím tắt toàn cục (Global Hotkey) để làm mới (Reload) hoặc khôi phục vị trí mặc định (Reset Layout) ngay lập tức mà không cần thoát game hay mở file cấu hình.

---

### Kế hoạch Triển khai Kỹ thuật:

#### 1. Cấu hình Cài đặt (`main.cjs`)
- Thêm các thuộc tính vào `defaultSettings` và `normalizeSettings`:
  - `reloadKey`: Phím tắt reload giao diện (Mặc định: `"Ctrl+Shift+R"` hoặc `"F9"`).
  - `resetLayoutKey`: Phím tắt khôi phục vị trí HUD (Mặc định: `"Ctrl+Shift+L"` hoặc phím do người dùng chọn).

#### 2. Xử lý Phím tắt Toàn cục với `uiohook-napi` (`main.cjs` -> `startCursorHook`)
- Lắng nghe combo phím tương ứng:
  ```javascript
  // 1. Phím tắt Reload toàn bộ Overlay
  if (matchCombo(e, readSettings().reloadKey)) {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.reload();
    }
    if (radarWindow && !radarWindow.isDestroyed()) {
      radarWindow.reload();
    }
    stopLive();
    connectLive();
    return;
  }

  // 2. Phím tắt Reset vị trí các widget (Layout)
  if (matchCombo(e, readSettings().resetLayoutKey)) {
    const defaultRadarBounds = { x: 10, y: 10, width: 320, height: 320 };
    const defaultLayout = { w_prime: { x: 240, y: 10 } };
    const nextSettings = writeSettings({
      layout: defaultLayout,
      radarBounds: defaultRadarBounds,
    });
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("settings:changed", nextSettings);
    }
    if (radarWindow && !radarWindow.isDestroyed()) {
      radarWindow.setBounds(defaultRadarBounds);
    }
    return;
  }
  ```

#### 3. Bổ sung IPC và Ghi nhận Phím trong Settings (`preload.cjs` & Dashboard UI)
- Thêm IPC handler:
  - `ipcMain.handle("reload:recordKey", () => recordKey("reloadKey"));`
  - `ipcMain.handle("layout:reset", () => { ... });`
- Expose qua `contextBridge` trong `preload.cjs`.
- Trong giao diện Settings (Tab *Điều Khiển* / *Controls*):
  - Cho phép người dùng bấm để đổi phím tắt `reloadKey` và `resetLayoutKey`.
  - Bổ sung nút **"Đặt lại vị trí mặc định (Reset Layout)"** trực tiếp trên thanh Dashboard hoặc trong cài đặt Widgets để người dùng có thể click chuột khi cần.

#### 4. Quy trình Đóng gói (Packaging)
- Tuân thủ quy định tại [GEMINI.md](file:///c:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/GEMINI.md):
  1. Đảm bảo tiến trình `TheIsleVn-BanhMi.exe` đã tắt hoàn toàn.
  2. Sử dụng `python pack_secure_app.py` để làm rối mã nguồn và đóng gói an toàn.

---

## 2. Cấu hình Thông tin Mạng Xã Hội & Thông Báo Từ Xa (Remote Config qua GitHub Gist / JSON)

### Mục đích & Nhu cầu:
- Tránh việc phải sửa code và đóng gói (pack) lại app mỗi khi muốn cập nhật link Facebook, TikTok, YouTube, Discord hoặc câu thông báo/banner.
- Quản trị viên có thể cập nhật thông tin bất cứ lúc nào ngay trên điện thoại hoặc trình duyệt web.

### Giải pháp Kỹ thuật (Đề xuất khuyên dùng: GitHub Gist):
1. **Lưu trữ từ xa:** Tạo file cấu hình `remote_config.json` trên GitHub Gist chứa danh sách link mạng xã hội và thông báo.
2. **Cơ chế trong App:**
   - Khi khởi động, app tải ngầm file JSON từ CDN GitHub.
   - **Local Cache & Fallback:** Luôn có link mặc định và lưu cache trên máy; nếu người chơi mất mạng thì app vẫn chạy mượt mà, không bao giờ bị lỗi hay crash.

---

## 3. Hệ thống Cổng Mở Khóa Nhiệm Vụ Mạng Xã Hội (Social Checklist Gate - Tinh gọn, Không cần nhập mã)

### Mục đích & Nhu cầu:
- Ứng dụng cung cấp miễn phí cho cộng đồng, đổi lại người chơi ủng hộ tác giả bằng cách ghé thăm và theo dõi các kênh mạng xã hội.
- Tối ưu hóa trải nghiệm người dùng (UX): Quy trình diễn ra nhanh gọn, mượt mà, **không cần copy/paste hay nhập mã phức tạp** tránh gây khó khăn hay nản lòng cho game thủ.

### Kế hoạch Triển khai (Quy trình 1 Chạm Tinh Gọn):
1. **Giao diện khi mở app lần đầu:**
   - App hiển thị bảng nhiệm vụ mở khóa đẹp mắt và chuyên nghiệp với 4 nền tảng:
     - 🔴 **Bước 1:** Đăng ký kênh YouTube (Bấm nút ➔ Mở YouTube ➔ Đếm ngược 5s ➔ Hiện tích xanh ✅).
     - ⚫ **Bước 2:** Follow kênh TikTok (Bấm nút ➔ Mở TikTok ➔ Đếm ngược 5s ➔ Hiện tích xanh ✅).
     - 🔵 **Bước 3:** Like/Follow Fanpage Facebook (Bấm nút ➔ Mở Facebook ➔ Đếm ngược 5s ➔ Hiện tích xanh ✅).
     - 🟣 **Bước 4:** Tham gia Server Discord Bánh Mì (Bấm nút ➔ Mở Discord ➔ Đếm ngược 5s ➔ Hiện tích xanh ✅).
2. **Kích hoạt tức thì:**
   - Sau khi bấm đủ 4 nút và nhận đủ 4 tích xanh ✅ ➔ Nút to màu xanh **`[ MỞ KHÓA VÀO APP ]`** sẽ sáng lên rực rỡ.
   - Người chơi chỉ cần bấm 1 click là app mở khóa ngay lập tức và chuyển thẳng vào giao diện game/dashboard.
   - Lưu trạng thái đã mở khóa vào máy vĩnh viễn (các lần khởi động tiếp theo vào thẳng app, không bao giờ phải làm lại).
3. **Ưu điểm vượt trội:**
   - **Cực kỳ thân thiện & nhanh chóng:** Người chơi chỉ mất tầm 20-30 giây là xong toàn bộ, ai cũng làm được.
   - **Nhàn cho bạn:** Bạn không cần phải túc trực trong Discord để hỗ trợ phát mã, không lo người chơi gõ sai mã hay quên mã.
   - Các đường link nhiệm vụ vẫn liên kết với **Remote Config (Mục 2)** để bạn tùy chỉnh dễ dàng từ xa.


---

## 4. Sửa Lỗi Nút "Đăng Xuất" Không Làm Mới Giao Diện Ngay (Instant Logout UI Refresh Fix)

### Hiện trạng & Nguyên nhân:
- **Hiện tượng:** Khi bấm nút `[đăng xuất]` trong tab Tài Khoản (Settings), app không đăng xuất ngay lập tức. Người dùng phải tắt hẳn app và bật lại thì mới thấy đã đăng xuất.
- **Nguyên nhân:** Lệnh backend `auth:logout` trong `main.cjs` đã xóa token thành công vào file cấu hình, nhưng giao diện không tự đóng modal Settings và không gọi `mainWindow.reload()`, khiến React UI vẫn giữ trạng thái cũ trên màn hình.

### Giải pháp Kỹ thuật:
- Trong `src_extracted/electron/main.cjs` tại IPC handler `auth:logout`:
  ```javascript
  ipcMain.handle("auth:logout", () => {
    writeSettings({ 
      steamId: null, 
      overlayToken: null, 
      savedSteamId: null, 
      savedOverlayToken: null 
    });
    stopLive();
    try { closeRadar(); } catch {}
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("auth:changed", { steamId: null });
      mainWindow.reload(); // 🌟 Tự động reset toàn bộ giao diện về màn hình đăng nhập ngay lập tức
    }
  });
  ```

---

## 5. Tinh Chỉnh Giao Diện Donate & Bổ Sung Kênh Discord Hỗ Trợ

### Mục đích & Nhu cầu:
- Tinh chỉnh màn hình hiển thị mã QR VietQR TPBank cho gần gũi, rõ ràng mục đích và chuyên nghiệp hơn.
- Chuyển hàng nút mạng xã hội thành kênh liên hệ hỗ trợ chính thức và bổ sung thêm nút **Discord**.

### Nội dung Thay đổi Cụ thể:
1. **Tiêu đề:** 
   - Đổi từ `SUPPORT YTB BANHMI` ➔ **`Donate ủng hộ ở đây ạ <3 !`** (Gần gũi, ấm áp, đúng tính chất ủng hộ cốc cafe/trà đá).
2. **Đoạn chữ mô tả dưới mã QR:**
   - Thay đổi câu xin sub/follow ➔ **`Nếu có vấn đề gì về app, xin vui lòng liên hệ các mạng xã hội ở đây nha!`** (Vì người chơi đã hoàn thành follow ở cổng mở khóa, chuyển sang câu này để làm kênh hỗ trợ khi gặp lỗi).
3. **Bổ sung Nút Discord (Trọn bộ 4 Kênh Mạng Xã Hội):**
   - Hàng nút bên dưới gồm:
     - 🔴 **YouTube** (Tông đỏ)
     - 🔵 **Facebook** (Tông xanh dương)
     - ⚫ **TikTok** (Tông đen)
     - 🟣 **Discord** (Tông tím Blurple `#5865F2` đặc trưng kèm logo Discord).
   - Khi bấm vào nút Discord: Tự động mở link mời vào server Discord của Bánh Mì trên trình duyệt hoặc trực tiếp trong app Discord của máy.
   - Toàn bộ 4 đường link này đều được kết nối với **Remote Config (Mục 2)** để bạn có thể đổi link mời bất kỳ lúc nào nếu link cũ hết hạn.

---

## 6. Tích Hợp Mini Widget Donate QR & 4 Kênh Mạng Xã Hội Vào Thẻ Profile (`.idCard`)

### Mục đích & Khảo sát giao diện:
- **Khảo sát thực tế:** Phần bên phải của thẻ thông tin khủng long (`.idCard`) trong tab Profile hiện tại **hoàn toàn trống 100%** (chỉ có avatar và 3 dòng Stage/Server/SteamID lệch bên trái).
- **Ý tưởng:** Tận dụng tối đa khoảng trống này để đặt một khối Mini Widget gồm mã QR Donate và 4 kênh mạng xã hội, giúp giao diện cân đối, sang trọng và thu hút người chơi ủng hộ ngay trên màn hình chính Dashboard.

### Kế hoạch Thiết kế & Triển khai:
1. **Bố cục bên phải `.idCard` (`margin-left: auto`):**
   - Thiết kế ưu tiên **Mã QR to rõ tối đa để quét nhanh bằng điện thoại**:
     - **Kích thước mã QR:** Mở rộng tối đa theo chiều cao của thẻ (khoảng **85px - 95px**, chiếm trọn chiều cao của `.idCard`).
     - **Nền trắng chuẩn độ tương phản (High-Contrast White Base):** Giữ khung nền trắng tinh khiết với padding chuẩn để camera các app ngân hàng (MB, Vietcombank, Momo, TPBank...) có thể **bắt nét và nhận diện mã tức thì chỉ trong 0.5 giây**, không bị lóa hay khó quét trong phòng tối.
     - **Hiệu ứng tiện ích (Tùy chọn):** Khi bấm vào mã QR có thể phóng to nhẹ hoặc mở ảnh gốc để quét siêu dễ.
   - **Cụm 4 Icon Mạng Xã Hội được xếp gọn bên cạnh QR:**
     - Xếp gọn gàng theo dạng cột 2x2 hoặc 1 hàng dọc bên cạnh QR để nhường toàn bộ diện tích cho mã QR to nhất có thể.
     - Gồm: 🔴 YouTube, 🔵 Facebook, ⚫ TikTok, 🟣 Discord với hiệu ứng hover phát sáng neon, click vào mở kênh trong 1 nốt nhạc.
2. **Ưu điểm nổi bật:**
   - **Dễ quét 100%:** Game thủ chỉ cần giơ điện thoại lên trước màn hình máy tính là app ngân hàng nhận diện ngay, không cần căn chỉnh hay phóng to.
   - **Tối ưu không gian:** Biến khoảng trống thừa thãi thành khu vực truyền thông và nhận donate hiệu quả nhất.

---

## 7. Bổ Sung Tab "Ủng Hộ Coder" Lên Vị Trí Top 1 Trong Bảng Cài Đặt (Settings)

### Mục đích & Nhu cầu:
- Đặt khu vực Donate & Kênh liên hệ vào vị trí danh giá, dễ thấy nhất trong bảng Cài Đặt.
- Người dùng khi mở Cài Đặt sẽ nhìn thấy ngay tab tri ân tác giả Bánh Mì.

### Kế hoạch Thiết kế & Triển khai:
1. **Vị trí Tab Menu:**
   - Nằm ở **vị trí số 1 trên cùng** của thanh danh mục bên trái (đứng trên cả `HUD Tiện Ích`).
   - Tên tab: **`Ủng Hộ Coder`** (hoặc `Ủng Hộ Bánh Mì ❤️`) với icon trái tim hoặc tách cafe phát sáng neon nổi bật.
2. **Bố cục nội dung bên trong Tab:**
   - **Tiêu đề:** `Donate ủng hộ ở đây ạ <3 !`
   - **Mã VietQR TPBank to rõ tối đa:** Khung nền trắng tương phản cao chuẩn quét ngân hàng tức thì.
   - **Thông tin chuyển khoản dạng chữ & Nút Copy:**
     - Ngân hàng: TPBank
     - Số tài khoản + Nút `[Sao Chép STK]`
     - Chủ tài khoản: Tên của bạn
   - **Lời nhắn hỗ trợ kỹ thuật:** `Nếu có vấn đề gì về app, xin vui lòng liên hệ các mạng xã hội ở đây nha!`
   - **Cụm 4 nút mạng xã hội chính thức:**
     - 🔴 YouTube | 🔵 Facebook | ⚫ TikTok | 🟣 Discord (click mở trực tiếp trình duyệt, link đồng bộ qua Remote Config).

---

## 8. Sửa Lỗi "Kẹt Xuyên Chuột" Click Không Ăn (Mouse Click-Through Desync Fix)

### Hiện trạng & Triệu chứng:
- **Triệu chứng:** Đôi khi người dùng rê chuột vào app bấm nút không ăn, bấm vào bất kỳ đâu trên bảng điều khiển cũng không có phản hồi. Chỉ khi bấm phím `F8` bật/tắt lại hoặc bấm `Alt+Tab` vài lần thì mới click được bình thường.
- **Tên kỹ thuật:** Lỗi lệch pha trạng thái xuyên chuột (*Mouse Click-Through Desync / WS_EX_TRANSPARENT Lock*) trong Electron Overlay.

### Phân tích Nguyên nhân Cốt lõi:
1. **Cơ chế xuyên chuột của Overlay:**
   - Khi người chơi điều khiển game: App kích hoạt `setIgnoreMouseEvents(true, { forward: true })` để chuột xuyên qua app vào game.
   - Khi người chơi rê chuột vào các nút/dashboard: `preload.cjs` phát hiện hover và gọi `overlay:mouseIgnore(false)` để đón nhận click chuột.
2. **Nguyên nhân gây nghẽn (Desync):**
   - Trong `main.cjs`, hàm `trackGame()` chạy nền mỗi 700ms. Khi phát hiện cửa sổ game bị mất focus nhẹ hoặc Windows tráo đổi tiến trình, `trackGame()` tự động gọi cưỡng chế:
     `mainWindow.setIgnoreMouseEvents(true, { forward: true });`
   - Tuy nhiên, lệnh này **không đồng bộ biến cờ** với `currentIgnoreMouse` trong `main.cjs` và `lastSentIgnore` trong `preload.cjs`.
   - Kết quả: `preload.cjs` vẫn tưởng trạng thái là `false`, nên các sự kiện di chuột tiếp theo bị bỏ qua (`if (lastSentIgnore === targetIgnore) return;`). App bị kẹt cứng ở trạng thái "xuyên chuột", mọi cú click đều xuyên thẳng ra ngoài.
   - Khi bấm **F8**: Hàm `toggleDash()` cưỡng chế reset lại toàn bộ trạng thái chuột nên click lại được.
   - Khi bấm **Alt+Tab**: Windows phát lại sự kiện `GetForegroundWindow()`, ép `trackGame()` nhận diện lại.

### Giải pháp Kỹ thuật Triệt để:
1. **Đồng bộ hóa 1 chiều tuyệt đối:** Khi `main.cjs` cưỡng chế đổi `setIgnoreMouseEvents`, phải cập nhật lại biến `currentIgnoreMouse` và gửi thông báo cho `preload.cjs` cập nhật `lastSentIgnore`.
2. **Khắc phục tại `trackGame()`:** Chỉ cưỡng chế `setIgnoreMouseEvents(true)` khi Dashboard thực sự đang tắt (`!dashOn`). Nếu Dashboard đang mở (`dashOn === true`) hoặc đang mở bảng Settings, tuyệt đối không được tự ý ghi đè trạng thái xuyên chuột của người dùng.

---

## 9. Hệ Thống Tùy Biến Giao Diện Cá Nhân Hóa (Custom HUD Skins & Appearance)

### Mục đích & Nhu cầu:
- Thay vì giao diện mặc định cố định, người chơi có thể tự do tùy biến màu sắc, kích thước và hình dáng của 3 thành phần chính:
  1. **Bản đồ Radar**
  2. **Bảng chỉ số (Stats HUD - Máu, Thể lực, Thức ăn, Nước)**
  3. **Bảng trạng thái tăng trưởng (Prime / Growth Bar)**
- Mang lại trải nghiệm độc đáo, chuyên nghiệp tương tự các công cụ HUD quốc tế và phù hợp với nhiều kích thước màn hình khác nhau (FullHD, 2K, 4K).

### Kế hoạch Thiết kế & Triển khai (Tích hợp trong Tab "Giao Diện"):
> [!IMPORTANT]
> **NGUYÊN TẮC BẤT DI BẤT DỊCH (CORE PRINCIPLE):**
> - **Giao diện hiện tại LUÔN LUÔN là Giao diện Mặc Định (Default 100%):** Bảng chỉ số thanh ngang truyền thống, bảng Prime hiện tại, hình dáng radar và bảng màu hiện tại sẽ là cấu hình chuẩn ban đầu khi cài đặt app.
> - Người dùng mới tải app về sẽ thấy giao diện quen thuộc y hệt như trước giờ, không bị bỡ ngỡ.
> - Các kiểu dáng (Dọc, Hộp vuông 2x2, Vòng tròn) và các Theme màu sắc khác chỉ là **tùy chọn bổ sung (Options)** cho ai muốn đổi.
> - Bổ sung nút **"Khôi Phục Mặc Định (Reset to Default)"** để người chơi bấm 1 click là đưa mọi tùy biến về lại đúng giao diện nguyên bản hiện tại.

1. **Bộ Theme Làm Sẵn (Preset Themes - 1 Click đổi ngay):**
   - 🌟 **Mặc Định Ban Đầu (Classic Default):** Giữ nguyên vẹn 100% toàn bộ màu sắc và kiểu dáng hiện tại của app.
   - 🟣 **Cyberpunk Neon:** Tím dạ quang & Hồng phát sáng.
   - 🟢 **Emerald Jungle:** Xanh lục ngọc bích phong cách tự nhiên.
   - 🔴 **Blood Crimson:** Đỏ huyết chiến đấu mạnh mẽ.
   - 🍞 **Bánh Mì Signature:** Tông vàng cam ấm áp mang thương hiệu Bánh Mì Biết Chơi.
   - ⚪ **Minimalist Dark:** Xám khói tinh tế, chống rối mắt.
2. **Tùy biến Hình dáng Bố cục (Layout Shapes):**
   - ➖ **Thanh Ngang Cổ Điển (Mặc định):** Giữ nguyên thiết kế thanh ngang như hiện tại.
   - 🟦 **Khối Chữ Nhật / Hộp Vuông Mini (2x2):** Gom 4 chỉ số thành thẻ hộp nhỏ gọn ở góc màn hình.
   - 📱 **Cột Dọc (Vertical):** Xếp dọc theo mép màn hình.
   - ⭕ **Đồng Hồ Tròn (Circular Gauges):** Vòng tròn sinh tồn bao quanh icon.
3. **Tùy biến Màu sắc Chi tiết (Custom Color Pickers):**
   - Bộ chọn màu (Color Picker) độc lập cho từng thanh: Máu, Thể lực, Thức ăn, Nước, Thanh tăng trưởng Prime (kèm nút hoàn tác màu gốc).
4. **Tùy biến Kích thước & Hình dáng (Shape & Scale):**
   - **Radar:** Chọn kiểu dáng Tròn (Mặc định) hoặc Bo vuông (Rounded Square); Thanh trượt kích thước Zoom & Size.
   - **Stats & Prime HUD:** Thanh trượt co giãn tỷ lệ (Scale: 80% - 130%); Tùy chọn ẩn/hiện số phần trăm chi tiết.
5. **Lưu trữ & Hiệu năng:**
   - Cấu hình lưu trữ trực tiếp vào file settings máy người dùng (không mất khi tắt máy).
   - Áp dụng màu sắc thông qua CSS Variables (GPU accelerated), đảm bảo 0ms độ trễ và không ảnh hưởng đến FPS của game.

---

## 5. Quản lý Chu kỳ Nhiệm vụ Mạng Xã Hội từ xa theo Mùa (Remote Season Social Gate)

### Mục đích & Nhu cầu:
- Định kỳ (khoảng 1 - 2 tháng một lần, hoặc mỗi khi Bánh Mì có video/chiến dịch mới), Admin muốn kích hoạt lại bảng nhiệm vụ mạng xã hội để người chơi làm lại 1 lần nhằm duy trì tương tác, kéo follow/sub cho các kênh mới.
- Admin không muốn phải build lại file cài đặt hay gửi file Setup mới mỗi lần muốn reset nhiệm vụ.

### Giải pháp Kỹ thuật:
1. **Quản lý qua Remote Config trực tuyến:**
   - Trong file cấu hình online `remote_config.json`, thêm trường phiên bản mùa:
     ```json
     "gateSeason": 1
     ```
2. **Logic so khớp trên ứng dụng người dùng:**
   - Khi người chơi mở khóa thành công, app lưu: `localStorage.setItem("banhmi_gate_season", currentSeason)`.
   - Mỗi lần mở app, app tải config từ xa và so sánh:
     - Nếu `localSeason < remoteSeason`: Bảng nhiệm vụ tự động kích hoạt lại để người dùng ủng hộ mùa mới.
     - Nếu `localSeason >= remoteSeason`: Ứng dụng tự động bỏ qua và vào thẳng game.
3. **Đặc quyền Admin Vĩnh viễn (Bypass):**
   - Khi đã nhập Key `BANHMI-ADMIN-KEY1`, cờ `localStorage.getItem("banhmi_is_admin_v1") === "true"` được thiết lập vĩnh viễn.
   - Dù Admin có nâng `gateSeason` lên bao nhiêu (Season 2, 3, 4...), máy của Admin vẫn luôn được miễn trừ 100%, không bao giờ bị hỏi lại.








