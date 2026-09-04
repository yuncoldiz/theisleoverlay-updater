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
