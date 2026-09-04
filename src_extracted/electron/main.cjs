const { app, BrowserWindow, ipcMain, net, shell, screen, Tray, Menu, safeStorage } = require("electron");
const { autoUpdater } = require("electron-updater");
const path = require("path");
const fs = require("fs");

app.setPath("userData", path.join(app.getPath("appData"), "theisleinformation-bybanhmibietchoi"));

let uio = null;
try {
  uio = require("uiohook-napi");
} catch {
  uio = null;
}
let cursorOn = false;
let cursorKeyHeld = false;
let dashKeyHeld = false;
let dashOn = true;
let recordTarget = "cursorKey";
let uioStarted = false;
let recordResolve = null;

const SETTINGS_FILE = () =>
    path.join(app.getPath("userData"), "theisleinformation-bybanhmibietchoi.settings.json");

const logInfo = (msg) => {
  try {
    fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `[INFO ${new Date().toISOString()}] ${msg}\n`, "utf8");
  } catch {}
};

const defaultTheme = {
  accent: "#7cf2a6",
  stat: { health: "#ff5a5a", stamina: "#ffcf4a", food: "#79f2a6", water: "#5ab6ff" },
};

const defaultSettings = {
  apiBaseUrl: "https://islepilot.eu",
  steamId: null,
  overlayToken: null,
  opacity: 1,
  layout: null,
  panels: { stats: true, prime: true, radar: true, heart: false },
  theme: defaultTheme,
  radarBounds: null,
  radarSize: 320,
  radarRange: 1,
  radarLabels: false,
  radarOpen: true,
  cursorEnabled: false,
  cursorKey: "Insert",
  cursorMode: "toggle",
  dashKey: "F8",
  statsKey: "Ctrl+K",
  primeKey: "Ctrl+P",
  radarKey: "Ctrl+M",
  reloadKey: "Ctrl+Shift+R",
  resetLayoutKey: "Ctrl+Shift+L",
  streamerMode: false,
  compatMode: false,
  dismissedUpdateVersion: null,
};

const isHex = (v) => typeof v === "string" && /^#[0-9a-fA-F]{6}$/.test(v);
const normalizeTheme = (t) => {
  const src = t && typeof t === "object" ? t : {};
  const st = src.stat && typeof src.stat === "object" ? src.stat : {};
  return {
    accent: isHex(src.accent) ? src.accent : defaultTheme.accent,
    stat: {
      health: isHex(st.health) ? st.health : defaultTheme.stat.health,
      stamina: isHex(st.stamina) ? st.stamina : defaultTheme.stat.stamina,
      food: isHex(st.food) ? st.food : defaultTheme.stat.food,
      water: isHex(st.water) ? st.water : defaultTheme.stat.water,
    },
  };
};

const asStringOrNull = (v) => (typeof v === "string" && v.length > 0 ? v : null);
const asString = (v, fallback) =>
  typeof v === "string" && v.trim() ? v.trim() : fallback;

const normalizeSettings = (raw) => {
  const s = raw && typeof raw === "object" ? raw : {};
  const steamIdRaw = typeof s.steamId === "string" ? s.steamId.trim() : "";
  return {
    apiBaseUrl: asString(s.apiBaseUrl, defaultSettings.apiBaseUrl),
    steamId: /^\d{17}$/.test(steamIdRaw) ? steamIdRaw : null,
    overlayToken: asStringOrNull(s.overlayToken),
    opacity:
      typeof s.opacity === "number" && Number.isFinite(s.opacity)
        ? Math.max(0.3, Math.min(1, s.opacity))
        : 1,
    layout: (() => {
      if (!s.layout || typeof s.layout !== "object") return null;
      const lay = { ...s.layout };
      if (lay.w_stats && (lay.w_stats.x === 18 || lay.w_stats.x === 443 || lay.w_stats.y === 240 || lay.w_stats.y === 818 || lay.w_stats.y === 1035 || lay.w_stats.y === 990 || lay.w_stats.y === 780)) {
        delete lay.w_stats;
      }
      if (lay.w_prime && (lay.w_prime.x === 18 || lay.w_prime.x === 381 || lay.w_prime.x === 853 || lay.w_prime.y === 470)) {
        delete lay.w_prime;
      }
      if (lay.main && (lay.main.x === 140 || lay.main.x === 506 || lay.main.y === 70 || lay.main.y === 87)) {
        delete lay.main;
      }
      return lay;
    })(),
    panels: s.panels && typeof s.panels === "object" ? s.panels : null,
    serverHistory: Array.isArray(s.serverHistory) ? s.serverHistory : ["https://islepilot.eu"],
    theme: normalizeTheme(s.theme),
    radarBounds: s.radarBounds && typeof s.radarBounds === "object" ? s.radarBounds : null,
    radarSize:
      typeof s.radarSize === "number" && Number.isFinite(s.radarSize)
        ? Math.max(180, Math.min(560, Math.round(s.radarSize)))
        : 320,
    radarRange:
      typeof s.radarRange === "number" && s.radarRange >= 0 && s.radarRange <= 3
        ? Math.round(s.radarRange)
        : 1,
    radarLabels: Boolean(s.radarLabels),
    radarOpen: Boolean(s.radarOpen),
    cursorEnabled: Boolean(s.cursorEnabled),
    cursorKey: typeof s.cursorKey === "string" && s.cursorKey ? s.cursorKey : "Insert",
    cursorMode: s.cursorMode === "hold" ? "hold" : "toggle",
    dashKey: typeof s.dashKey === "string" ? s.dashKey : "F8",
    statsKey: typeof s.statsKey === "string" ? s.statsKey : "Ctrl+K",
    primeKey: typeof s.primeKey === "string" ? s.primeKey : "Ctrl+P",
    radarKey: typeof s.radarKey === "string" ? s.radarKey : "Ctrl+M",
    reloadKey: typeof s.reloadKey === "string" && s.reloadKey ? s.reloadKey : "Ctrl+Shift+R",
    resetLayoutKey: typeof s.resetLayoutKey === "string" && s.resetLayoutKey ? s.resetLayoutKey : "Ctrl+Shift+L",
    streamerMode: Boolean(s.streamerMode),
    compatMode: Boolean(s.compatMode),
    dismissedUpdateVersion: typeof s.dismissedUpdateVersion === "string" ? s.dismissedUpdateVersion : null,
    savedSteamId: asStringOrNull(s.savedSteamId),
    savedOverlayToken: asStringOrNull(s.savedOverlayToken),
  };
};

const encryptToken = (plain) => {
  if (!plain) return null;
  try {
    if (safeStorage.isEncryptionAvailable()) {
      return "enc1:" + safeStorage.encryptString(plain).toString("base64");
    }
  } catch {}
  return plain;
};
const decryptToken = (stored) => {
  if (!stored) return null;
  if (typeof stored === "string" && stored.startsWith("enc1:")) {
    try {
      return safeStorage.decryptString(Buffer.from(stored.slice(5), "base64"));
    } catch {
      return null;
    }
  }
  return stored;
};

const readSettings = () => {
  try {
    const s = normalizeSettings(JSON.parse(fs.readFileSync(SETTINGS_FILE(), "utf8")));
    s.overlayToken = decryptToken(s.overlayToken);
    return s;
  } catch {
    return { ...defaultSettings };
  }
};

const writeSettings = (patch) => {
  const merged = normalizeSettings({
    ...readSettings(),
    ...(patch && typeof patch === "object" ? patch : {}),
  });
  const onDisk = { ...merged, overlayToken: encryptToken(merged.overlayToken) };
  fs.mkdirSync(path.dirname(SETTINGS_FILE()), { recursive: true });
  fs.writeFileSync(SETTINGS_FILE(), JSON.stringify(onDisk, null, 2), "utf8");
  return merged;
};

// Performance Optimizations
app.commandLine.appendSwitch("js-flags", "--max-old-space-size=128");
app.commandLine.appendSwitch("force_high_performance_gpu");
app.commandLine.appendSwitch("enable-gpu-rasterization");
app.commandLine.appendSwitch("enable-accelerated-2d-canvas");
app.commandLine.appendSwitch("disable-software-rasterizer");
app.commandLine.appendSwitch("enable-zero-copy");
app.commandLine.appendSwitch("disable-background-timer-throttling");
app.commandLine.appendSwitch("disable-renderer-backgrounding");
app.commandLine.appendSwitch("disable-features", "CalculateNativeWinOcclusion");

if (readSettings().compatMode) {
  app.commandLine.appendSwitch("disable-direct-composition");
}

function baseApi() {
  return (readSettings().apiBaseUrl || defaultSettings.apiBaseUrl).replace(/\/+$/, "");
}

let mainWindow = null;
let gameBounds = null;
let overlayFocusActive = false;
let lastUpdaterState = { state: "idle" };
const bootGraceUntil = Date.now() + 4000;
let streamerModeActive = false;
let lastShowTs = 0;
let lastTopmostTs = 0;

const createWindow = () => {
  logInfo("createWindow called.");
  streamerModeActive = readSettings().streamerMode;
  const primary = screen.getPrimaryDisplay();
  logInfo(`primary screen bounds: ${JSON.stringify(primary.bounds)}`);
  mainWindow = new BrowserWindow({
    x: primary.bounds.x,
    y: primary.bounds.y,
    width: primary.bounds.width,
    height: primary.bounds.height,
        title: "TheIsleVN - YTB BanhMi",
    icon: path.join(__dirname, "tray.ico"),
    frame: false,
    transparent: true,
    backgroundColor: "#00000000",
    resizable: false,
    movable: false,
    minimizable: false,
    maximizable: false,
    skipTaskbar: !readSettings().streamerMode,
    hasShadow: false,
    fullscreenable: false,
    focusable: true,
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      devTools: true,
      backgroundThrottling: false,
      preload: path.join(__dirname, "preload.cjs"),
    },
  });

  // mainWindow.webContents.openDevTools({ mode: "detach" });
  mainWindow.setAlwaysOnTop(true, "screen-saver");
  mainWindow.setIgnoreMouseEvents(true, { forward: true });
  mainWindow.setMenuBarVisibility(false);

  const distIndex = path.join(__dirname, "..", "dist", "index.html");
  const devUrl = process.env.VITE_DEV_SERVER_URL;
  if (!app.isPackaged && devUrl) void mainWindow.loadURL(devUrl);
  else void mainWindow.loadFile(distIndex);

  mainWindow.webContents.on("console-message", (_e, level, msg, line, src) => {
    if (level >= 3) {
      fs.appendFile(path.join(app.getPath("userData"), "renderer.log"), `[L${level}] ${src}:${line} ${msg}\n`, "utf8", () => {});
    }
  });

  mainWindow.once("ready-to-show", () => {
    logInfo("mainWindow ready-to-show fired.");
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.showInactive();
      logInfo("mainWindow showInactive called.");
    }
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
};

let radarWindow = null;

function openRadar() {
  if (radarWindow && !radarWindow.isDestroyed()) {
    radarWindow.show();
    radarWindow.focus();
    return;
  }
  const s = readSettings();
  if (!s.overlayToken) {
    return;
  }
  const b = s.radarBounds || null;
    const sz = s.radarSize || 220;
    const primary = screen.getPrimaryDisplay();
    const defaultX = primary.bounds.x + 20;
    const defaultY = primary.bounds.y + 150;
    radarWindow = new BrowserWindow({
    title: "TheIsleVN - Radar Overlay",
    width: b?.width ?? sz,
    height: b?.height ?? sz,
    icon: path.join(__dirname, "tray.ico"),
    x: b?.x ?? defaultX,
    y: b?.y ?? defaultY,
    minWidth: 160,
    minHeight: 160,
    frame: false,
    transparent: true,
    backgroundColor: "#00000000",
    resizable: false,
    movable: true,
    minimizable: false,
    maximizable: false,
    skipTaskbar: true,
    hasShadow: false,
    fullscreenable: false,
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      backgroundThrottling: false,
      devTools: false,
      preload: path.join(__dirname, "preload.cjs"),
    },
  });
  radarWindow.setAlwaysOnTop(true, "screen-saver", 2);
  radarWindow.setMenuBarVisibility(false);

  const distIndex = path.join(__dirname, "..", "dist", "index.html");
  const devUrl = process.env.VITE_DEV_SERVER_URL;
  if (!app.isPackaged && devUrl) void radarWindow.loadURL(`${devUrl}#radar`);
  else void radarWindow.loadFile(distIndex, { hash: "radar" });

  radarWindow.once("ready-to-show", () => {
    if (radarWindow && !radarWindow.isDestroyed()) radarWindow.show();
  });
  let radarSaveTimer = null;
  const saveBounds = () => {
    if (radarSaveTimer) clearTimeout(radarSaveTimer);
    radarSaveTimer = setTimeout(() => {
      if (radarWindow && !radarWindow.isDestroyed()) writeSettings({ radarBounds: radarWindow.getBounds() });
    }, 200);
  };
  radarWindow.on("resize", saveBounds);
  radarWindow.on("move", saveBounds);
  radarWindow.on("closed", () => {
    radarWindow = null;
    if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("radar:changed", { open: false });
  });
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("radar:changed", { open: true });
}

function closeRadar() {
  if (radarWindow && !radarWindow.isDestroyed()) radarWindow.close();
}

function radarSend(channel, data) {
  if (radarWindow && !radarWindow.isDestroyed()) radarWindow.webContents.send(channel, data);
}

function setCursor(on) {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  cursorOn = on;
  mainWindow.setIgnoreMouseEvents(true, { forward: true });
  if (on) {
    if (!mainWindow.isVisible()) mainWindow.showInactive();
    mainWindow.setAlwaysOnTop(true, "screen-saver");
    mainWindow.focus();
    try { app.focus({ steal: true }); } catch {}
    if (radarWindow && !radarWindow.isDestroyed()) {
      radarWindow.setAlwaysOnTop(true, "screen-saver", 2);
      radarWindow.moveTop();
    }
  } else {
    try { mainWindow.blur(); } catch {}
  }
  mainWindow.webContents.send("overlay:cursor", on);
}

function toggleDash() {
  dashOn = !dashOn;
  setCursor(dashOn);
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("overlay:dash", dashOn);
  void trackGame();
}

let tray = null;

let serverPromptWindow = null;
function promptChangeServer() {
  if (serverPromptWindow && !serverPromptWindow.isDestroyed()) {
    serverPromptWindow.focus();
    return;
  }
  
  serverPromptWindow = new BrowserWindow({
    width: 420,
    height: 240,
    title: "Thay đổi Server",
    frame: true,
    resizable: false,
    minimizable: false,
    maximizable: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  serverPromptWindow.setMenuBarVisibility(false);
  
  const currentSettings = readSettings();
  const currentUrl = currentSettings.apiBaseUrl || "https://islepilot.eu";
  
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Thay đổi Server (Change Server)</title>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          padding: 20px;
          background-color: #030208;
          color: #ffffff;
          margin: 0;
          overflow: hidden;
        }
        h3 {
          margin-top: 0;
          color: #00f0ff;
          font-size: 16px;
          letter-spacing: 0.05em;
          text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
        }
        .desc {
          font-size: 12px;
          color: #a09cb0;
          margin-bottom: 12px;
        }
        input {
          width: 100%;
          padding: 8px 12px;
          margin: 5px 0 15px 0;
          box-sizing: border-box;
          border: 1px solid #201335;
          border-radius: 6px;
          background-color: #0c0714;
          color: #ffffff;
          font-size: 13px;
          transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus {
          border-color: #e97ca5;
          outline: none;
          box-shadow: 0 0 8px rgba(233, 124, 165, 0.3);
        }
        .buttons {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
        }
        button {
          padding: 8px 16px;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 600;
          font-size: 12px;
          transition: all 0.2s;
        }
        .btn-save {
          background-color: #00f0ff;
          color: #030208;
          box-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
        }
        .btn-save:hover {
          background-color: #33f3ff;
          box-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
        }
        .btn-cancel {
          background-color: #201335;
          color: #a09cb0;
        }
        .btn-cancel:hover {
          background-color: #311e50;
          color: #ffffff;
        }
      </style>
    </head>
    <body>
      <h3>Thay đổi Server URL</h3>
      <div class="desc">Nhập URL Server mới cho HUD của bạn:</div>
      <input type="text" id="serverUrl" value="${currentUrl}" placeholder="https://...">
      <div class="buttons">
        <button class="btn-cancel" onclick="cancel()">Hủy</button>
        <button class="btn-save" onclick="save()">Lưu</button>
      </div>
      <script>
        const { ipcRenderer } = require('electron');
        function cancel() {
          window.close();
        }
        function save() {
          const url = document.getElementById('serverUrl').value.trim();
          if (url) {
            ipcRenderer.send('server:change', url);
          }
          window.close();
        }
      </script>
    </body>
    </html>
  `;
  
  serverPromptWindow.loadURL("data:text/html;charset=utf-8," + encodeURIComponent(htmlContent));
}

ipcMain.on("server:change", (e, newUrl) => {
  writeSettings({ apiBaseUrl: newUrl });
  stopLive();
  connectLive();
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("settings:changed", readSettings());
    mainWindow.reload();
  }
});

function createTray() {
  try {
    tray = new Tray(path.join(__dirname, "tray.ico"));
        tray.setToolTip("TheIsleInformation-byBanhmibietchoi");
    tray.setContextMenu(
      Menu.buildFromTemplate([
        { label: "Show / hide dashboard", click: () => toggleDash() },
        { label: "Thay đổi Server (Change Server)", click: () => promptChangeServer() },
        { type: "separator" },
        { label: "Quit TheIsleInformation-byBanhmibietchoi", click: () => app.quit() },
      ]),
    );
    tray.on("double-click", () => toggleDash());
  } catch {
    tray = null;
  }
}

function keyNameForCode(code) {
  if (!uio) return String(code);
  for (const name of Object.keys(uio.UiohookKey)) {
    if (uio.UiohookKey[name] === code) return name;
  }
  return String(code);
}

function cursorCodeFrom(cursorKey) {
  if (!uio || !cursorKey) return null;
  const named = uio.UiohookKey[cursorKey];
  if (typeof named === "number") return named;
  const n = Number(cursorKey);
  return Number.isFinite(n) ? n : null;
}

function currentCursorCode() {
  const s = readSettings();
  if (!s.cursorEnabled) return null;
  return cursorCodeFrom(s.cursorKey);
}

function matchCombo(e, comboStr) {
  if (!comboStr || typeof comboStr !== "string") return false;
  const parts = comboStr.split("+");
  const keyName = parts[parts.length - 1];
  const targetCode = cursorCodeFrom(keyName);
  if (targetCode == null || e.keycode !== targetCode) return false;
  
  const wantCtrl = parts.includes("Ctrl");
  const wantShift = parts.includes("Shift");
  const wantAlt = parts.includes("Alt");
  
  const hasCtrl = !!(e.ctrlKey || (e.mask & 2));
  const hasShift = !!(e.shiftKey || (e.mask & 1));
  const hasAlt = !!(e.altKey || (e.mask & 4));
  
  return wantCtrl === hasCtrl && wantShift === hasShift && wantAlt === hasAlt;
}

function startCursorHook() {
  if (!uio || uioStarted) return;
  uioStarted = true;
  uio.uIOhook.on("keydown", (e) => {
    if (recordResolve) {
      const name = keyNameForCode(e.keycode);
      const hasCtrl = e.ctrlKey || (e.mask & 2);
      const hasShift = e.shiftKey || (e.mask & 1);
      const hasAlt = e.altKey || (e.mask & 4);
      let comboName = "";
      if (hasCtrl) comboName += "Ctrl+";
      if (hasShift) comboName += "Shift+";
      if (hasAlt) comboName += "Alt+";
      comboName += name;
      writeSettings({ [recordTarget]: comboName });
      const r = recordResolve;
      recordResolve = null;
      r(comboName);
      return;
    }
    if (licenseBlocked) return;

    // Dash toggle hotkey (e.g. F8) MUST always be allowed to toggle the dashboard,
    // even when the overlay is currently hidden or focus is outside the game.
    const dashCode = cursorCodeFrom(readSettings().dashKey);
    if (dashCode != null && e.keycode === dashCode) {
      if (!dashKeyHeld) {
        dashKeyHeld = true;
        toggleDash();
      }
      return;
    }

    if (!overlayFocusActive) return;

    // Custom panel toggles (Stats, Prime, Radar)
    if (matchCombo(e, readSettings().statsKey)) {
      togglePanel("stats");
      return;
    }
    if (matchCombo(e, readSettings().primeKey)) {
      togglePanel("prime");
      return;
    }
    if (matchCombo(e, readSettings().radarKey)) {
      toggleRadar();
      return;
    }
    if (matchCombo(e, readSettings().reloadKey)) {
      reloadApp();
      return;
    }
    if (matchCombo(e, readSettings().resetLayoutKey)) {
      resetLayout();
      return;
    }

    const code = currentCursorCode();
    if (code == null || e.keycode !== code) return;
    if (cursorKeyHeld) return;
    cursorKeyHeld = true;
    if (readSettings().cursorMode === "hold") setCursor(true);
    else setCursor(!cursorOn);
  });
  uio.uIOhook.on("keyup", (e) => {
    const dashCode = cursorCodeFrom(readSettings().dashKey);
    if (dashCode != null && e.keycode === dashCode) dashKeyHeld = false;
    const code = currentCursorCode();
    if (code != null && e.keycode === code) {
      cursorKeyHeld = false;
      if (readSettings().cursorMode === "hold") setCursor(false);
    }
  });
  try {
    uio.uIOhook.start();
  } catch {}
}

function displayForBounds(b) {
  if (!b) return screen.getPrimaryDisplay();
  return screen.getDisplayNearestPoint({
    x: Math.round(b.x + b.width / 2),
    y: Math.round(b.y + b.height / 2),
  });
}

function positionOverlay() {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  const wa = displayForBounds(gameBounds).bounds;
  const cur = mainWindow.getBounds();
  if (cur.x !== wa.x || cur.y !== wa.y || cur.width !== wa.width || cur.height !== wa.height) {
    mainWindow.setBounds(wa);
  }
}

let nw = null;
function loadNw() {
  if (nw === null) {
    try {
      nw = require("./native-windows.cjs");
    } catch {
      nw = false;
    }
  }
  return nw || null;
}

const GAME_WINDOW_RE = /theisle|isle-win64/i;
let gameHwnd = null;
let lastGameScanTs = 0;

function trackGame() {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  const n = loadNw();
  if (!n) return;

  let activeIsGame = false;
  let activeIsOverlay = false;
  try {
    if (gameHwnd && !n.IsWindow(gameHwnd)) gameHwnd = null;
    if (!gameHwnd && Date.now() - lastGameScanTs > 3000) {
      lastGameScanTs = Date.now();
      gameHwnd = n.findWindow((_title, imagePath, pid) => {
        if (pid === process.pid) return false;
        return GAME_WINDOW_RE.test(imagePath);
      });
    }

    const fg = n.GetForegroundWindow();
    let fgIsGame = false;
    let fgPid = 0;
    if (fg) {
      fgPid = n.windowPid(fg);
      if (fgPid && fgPid !== process.pid) {
        const fgPath = n.processImagePath(fgPid);
        if (fgPath && GAME_WINDOW_RE.test(fgPath)) {
          fgIsGame = true;
          if (!gameHwnd || !n.IsWindow(gameHwnd)) {
            gameHwnd = fg;
          }
        }
      }
    }

    if (gameHwnd) {
      const b = n.windowBounds(gameHwnd);
      if (b && b.width > 0 && b.height > 0) gameBounds = b;
    }

    activeIsGame = Boolean(fgIsGame || (gameHwnd && fg && n.isSameWindow(fg, gameHwnd)));
    activeIsOverlay = Boolean(fg && !activeIsGame && fgPid === process.pid);
  } catch {
  }
  const shouldShow =
    activeIsGame || activeIsOverlay || Date.now() < bootGraceUntil || dashOn || streamerModeActive;
  overlayFocusActive = shouldShow;

  if (shouldShow) {
    lastShowTs = Date.now();
    positionOverlay();
    const justShown = !mainWindow.isVisible();
    if (justShown) mainWindow.showInactive();
    if (justShown || Date.now() - lastTopmostTs > 2000) {
      mainWindow.setAlwaysOnTop(true, "screen-saver");
      lastTopmostTs = Date.now();
      if (radarWindow && !radarWindow.isDestroyed()) {
        radarWindow.setAlwaysOnTop(true, "screen-saver", 2);
        radarWindow.moveTop();
      }
    }
    if (radarWindow && !radarWindow.isDestroyed() && !radarWindow.isVisible() && readSettings().radarOpen) {
      radarWindow.showInactive();
    }
  } else {
    if (mainWindow && !mainWindow.isDestroyed() && mainWindow.isVisible()) {
      mainWindow.hide();
    }
    if (radarWindow && !radarWindow.isDestroyed() && radarWindow.isVisible()) {
      radarWindow.hide();
    }
  }
  const hasFocus = activeIsGame || activeIsOverlay;
  if (!hasFocus && cursorOn) {
    mainWindow.setIgnoreMouseEvents(true, { forward: true });
  } else if (hasFocus && cursorOn) {
    // Let the preload script manage mouseIgnore dynamically based on hover state.
  }
  mainWindow.webContents.send("overlay:state", {
    gameDetected: gameBounds != null,
    active: shouldShow,
    focused: activeIsGame || activeIsOverlay,
  });
}

async function apiFetch(method, pathname, body) {
  const s = readSettings();
  const headers = { Accept: "application/json", "X-Overlay-Version": "2" };
  if (s.overlayToken) headers.Authorization = `Bearer ${s.overlayToken}`;
  const init = { method, headers };
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }
  try {
    const res = await net.fetch(`${baseApi()}${pathname}`, init);
    const json = await res.json().catch(() => ({}));
    if (!res.ok) return { error: `HTTP ${res.status}`, status: res.status, ...json };
    return json;
  } catch (err) {
    return { error: String(err && err.message ? err.message : err) };
  }
}

async function apiGetFile(pathname) {
  const s = readSettings();
  const headers = {};
  if (s.overlayToken) headers.Authorization = `Bearer ${s.overlayToken}`;
  try {
    const res = await net.fetch(`${baseApi()}${pathname}`, { method: "GET", headers });
    if (!res.ok) return { error: `HTTP ${res.status}`, status: res.status };
    const mime = res.headers.get("content-type") || "application/octet-stream";
    const buf = Buffer.from(await res.arrayBuffer());
    return { dataUrl: `data:${mime};base64,${buf.toString("base64")}` };
  } catch (err) {
    return { error: String(err && err.message ? err.message : err) };
  }
}

const WebSocket = require("ws");
let liveWs = null;
let liveBackoff = 1000;
let liveTimer = null;
let liveStopped = false;
let lastLiveSendTs = 0;
let pendingLiveFrame = null;
let liveSendTimeout = null;

function baseWs() {
  return baseApi().replace(/^http/i, "ws");
}

function scheduleLiveReconnect() {
  if (liveStopped || liveTimer) return;
  if (!readSettings().overlayToken) return;
  liveTimer = setTimeout(() => {
    liveTimer = null;
    connectLive();
  }, liveBackoff);
  liveBackoff = Math.min(liveBackoff * 2, 15000);
}

async function sendOverlayHello(ws, token) {
  let name = "";
  try {
    const res = await fetch(`${baseApi()}/api/overlay/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const me = await res.json();
      name = typeof me?.personaName === "string" ? me.personaName : typeof me?.name === "string" ? me.name : "";
    }
  } catch {}
  try {
    if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ t: "hello", name }));
  } catch {}
}

let fallbackTimer = null;

function startHttpFallbackPolling() {
  if (fallbackTimer) return;
  fallbackTimer = setInterval(async () => {
    const wsConnected = liveWs && liveWs.readyState === WebSocket.OPEN;
    if (wsConnected) return;
    const token = readSettings().overlayToken;
    if (!token) return;
    try {
      const res = await fetch(`${baseApi()}/api/overlay/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const me = await res.json();
        if (me && me.position && me.steamId) {
          const livePayload = {
            steamId: me.steamId,
            position: me.position,
            skin: me.skin || null
          };
          if (mainWindow && !mainWindow.isDestroyed()) {
            mainWindow.webContents.send("overlay:live", livePayload);
          }
          radarSend("overlay:live", livePayload);
        }
      }
    } catch (err) {
      // Ignore network errors
    }
  }, 3000);
}

function connectLive() {
  liveStopped = false;
  const token = readSettings().overlayToken;
  try {
    fs.appendFileSync(path.join(app.getPath("userData"), "connect_live.log"), `connectLive called. Has token: ${!!token}\n`, "utf8");
  } catch {}
  if (!token) return;
  try {
    fetch(`${baseApi()}/api/overlay/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => res.text().then(text => {
         fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `HTTP test /api/overlay/me: status=${res.status} body=${text}\n`, "utf8");
      }))
      .catch(err => {
         fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `HTTP test failed: ${err.message}\n`, "utf8");
      });
  } catch (e) {
     fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `HTTP test catch error: ${e.message}\n`, "utf8");
  }
    if (liveWs) {
    try {
      liveWs.on("error", () => {});
      liveWs.terminate();
    } catch {}
    liveWs = null;
  }
  let ws;
  try {
    ws = new WebSocket(`${baseWs()}/ows`, { headers: { Authorization: `Bearer ${token}` } });
  } catch {
    scheduleLiveReconnect();
    return;
  }
  liveWs = ws;
    ws.on("open", () => {
    try {
      fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `WS Open success\n`, "utf8");
    } catch {}
    liveBackoff = 1000;
    sendOverlayHello(ws, token);
  });
  ws.on("message", (raw, isBinary) => {
    if (isBinary) {
      if (mainWindow && !mainWindow.isDestroyed()) {
        const buf = Buffer.isBuffer(raw) ? raw : Buffer.from(raw);
        mainWindow.webContents.send("overlay:troll-audio", buf);
      }
      return;
    }
    let frame;
    try {
      frame = JSON.parse(raw.toString());
    } catch {
      return;
    }
        if (frame && frame.t === "live" && frame.d) {
      const now = Date.now();
      if (now - lastLiveSendTs >= 33) {
        lastLiveSendTs = now;
        if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("overlay:live", frame.d);
        radarSend("overlay:live", frame.d);
        if (liveSendTimeout) {
          clearTimeout(liveSendTimeout);
          liveSendTimeout = null;
        }
      } else {
        pendingLiveFrame = frame.d;
        if (!liveSendTimeout) {
          liveSendTimeout = setTimeout(() => {
            lastLiveSendTs = Date.now();
            if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("overlay:live", pendingLiveFrame);
            radarSend("overlay:live", pendingLiveFrame);
            liveSendTimeout = null;
          }, 33 - (now - lastLiveSendTs));
        }
      }
    } else if (frame && frame.t === "troll") {
      if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("overlay:troll", frame);
    } else if (frame && frame.type === "ticket") {
      if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("overlay:ticket", frame);
    }
  });
    ws.on("close", (code, reason) => {
    try {
      fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `WS Closed: code=${code}, reason=${reason}\n`, "utf8");
    } catch {}
    if (liveWs === ws) liveWs = null;
    scheduleLiveReconnect();
  });
  ws.on("error", (err) => {
    try {
      fs.appendFileSync(path.join(app.getPath("userData"), "ws_error.log"), `WS Error: ${err && err.message ? err.message : err}\n`, "utf8");
    } catch {}
    try {
      ws.terminate();
    } catch {}
  });
}

function stopLive() {
  liveStopped = true;
  if (liveTimer) {
    clearTimeout(liveTimer);
    liveTimer = null;
  }
  if (liveSendTimeout) {
    clearTimeout(liveSendTimeout);
    liveSendTimeout = null;
  }
  pendingLiveFrame = null;
    if (liveWs) {
    try {
      liveWs.on("error", () => {});
      liveWs.terminate();
    } catch {}
    liveWs = null;
  }
}

ipcMain.handle("overlay:openUrl", (_e, url) => {
  if (typeof url === "string" && (url.startsWith("http://") || url.startsWith("https://"))) {
    shell.openExternal(url).catch(() => {});
    return true;
  }
  return false;
});


function toggleRadar() {
  const s = readSettings();
  const nextRadar = !(radarWindow && !radarWindow.isDestroyed());
  if (nextRadar) {
    openRadar();
    writeSettings({ radarOpen: true, panels: { ...s.panels || {}, radar: true } });
  } else {
    closeRadar();
    writeSettings({ radarOpen: false, panels: { ...s.panels || {}, radar: false } });
  }
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("settings:changed", readSettings());
  }
}

function togglePanel(panelKey) {
  const settings = readSettings();
  const panels = settings.panels || { stats: true, prime: true, heart: false, radar: false };
  panels[panelKey] = !panels[panelKey];
  const merged = writeSettings({ panels });
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("settings:changed", merged);
  }
}

function resetLayout() {
  const rSize = readSettings().radarSize || 320;
  const defaultRadarBounds = { x: 10, y: 10, width: rSize, height: rSize };
  const defaultLayout = {
    w_stats: { x: 513, y: 822 },
    w_prime: { x: 378, y: 2 },
    main: { x: 700, y: 200 }
  };
  const merged = writeSettings({
    layout: defaultLayout,
    radarBounds: defaultRadarBounds,
  });
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("settings:changed", merged);
  }
  if (radarWindow && !radarWindow.isDestroyed()) {
    radarWindow.setBounds(defaultRadarBounds);
    radarWindow.webContents.send("settings:changed", merged);
  }
  return merged;
}

function reloadApp() {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.reload();
  }
  if (radarWindow && !radarWindow.isDestroyed()) {
    radarWindow.reload();
  }
  stopLive();
  connectLive();
  return { success: true };
}

ipcMain.handle("app:openUrl", (_e, url) => {
  if (typeof url === "string" && (url.startsWith("http://") || url.startsWith("https://"))) {
    shell.openExternal(url);
  }
});

ipcMain.handle("overlay:getSettings", () => {
  const s = readSettings();
  return { ...s, apiBaseUrl: baseApi() };
});
ipcMain.handle("overlay:setSettings", (_e, next) => {
  const prev = readSettings();
  const merged = writeSettings(next);
  if (next && next.panels && typeof next.panels.radar === "boolean" && next.panels.radar !== prev.panels?.radar) {
    if (next.panels.radar) {
      openRadar();
      writeSettings({ radarOpen: true });
    } else {
      closeRadar();
      writeSettings({ radarOpen: false });
    }
  }
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.setOpacity(merged.opacity);
    if (typeof next?.streamerMode === "boolean" && merged.streamerMode !== prev.streamerMode) {
      streamerModeActive = merged.streamerMode;
      mainWindow.setSkipTaskbar(!merged.streamerMode);
      if (merged.streamerMode && !mainWindow.isVisible()) mainWindow.showInactive();
    }
    mainWindow.webContents.send("settings:changed", merged);
  }
  if (radarWindow && !radarWindow.isDestroyed()) {
    radarWindow.webContents.send("settings:changed", merged);
    if (typeof next?.radarSize === "number") {
      const bounds = radarWindow.getBounds();
      radarWindow.setBounds({
        x: bounds.x,
        y: bounds.y,
        width: next.radarSize,
        height: next.radarSize
      });
    }
  }
  return merged;
});
ipcMain.handle("overlay:getState", () => ({ gameDetected: gameBounds != null }));
ipcMain.handle("overlay:mouseIgnore", (_e, ignore) => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.setIgnoreMouseEvents(Boolean(ignore), { forward: true });
  }
});
ipcMain.handle("overlay:quit", () => app.quit());

ipcMain.handle("radar:toggle", () => {
  toggleRadar();
  return radarWindow != null && !radarWindow.isDestroyed();
});
ipcMain.handle("radar:close", () => {
  closeRadar();
  writeSettings({ radarOpen: false });
});
ipcMain.handle("radar:isOpen", () => radarWindow != null && !radarWindow.isDestroyed());
ipcMain.handle("radar:getBounds", () =>
  radarWindow && !radarWindow.isDestroyed() ? radarWindow.getBounds() : null,
);
ipcMain.handle("radar:setBounds", (_e, b) => {
  if (radarWindow && !radarWindow.isDestroyed() && b) {
    radarWindow.setBounds({
      x: Math.round(b.x),
      y: Math.round(b.y),
      width: Math.max(160, Math.round(b.width)),
      height: Math.max(160, Math.round(b.height)),
    });
    saveBounds();
  }
});

ipcMain.handle("skin:send", (_e, state) => {
  if (liveWs && liveWs.readyState === WebSocket.OPEN && state && typeof state === "object") {
    try {
      liveWs.send(JSON.stringify({ t: "liveskin", d: state }));
    } catch {}
  }
});

function recordKey(target) {
  if (!uio) return Promise.resolve(null);
  startCursorHook();
  recordTarget = target;
  return new Promise((resolve) => {
    if (recordResolve) recordResolve(null);
    recordResolve = resolve;
    setTimeout(() => {
      if (recordResolve === resolve) {
        recordResolve = null;
        resolve(null);
      }
    }, 10000);
  });
}

ipcMain.handle("cursor:recordKey", () => recordKey("cursorKey"));
ipcMain.handle("dash:recordKey", () => recordKey("dashKey"));
ipcMain.handle("map:recordKey", () => recordKey("radarKey"));
ipcMain.handle("prime:recordKey", () => recordKey("primeKey"));
ipcMain.handle("stats:recordKey", () => recordKey("statsKey"));
ipcMain.handle("reload:recordKey", () => recordKey("reloadKey"));
ipcMain.handle("resetLayout:recordKey", () => recordKey("resetLayoutKey"));
ipcMain.handle("app:reload", () => reloadApp());
ipcMain.handle("layout:reset", () => resetLayout());

ipcMain.handle("overlay:dashOpen", (_e, open) => {
  dashOn = !!open;
  setCursor(!!open);
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("overlay:dash", dashOn);
  }
  void trackGame();
});

ipcMain.handle("auth:steamLogin", () => {
  const s = readSettings();
  if (s.savedOverlayToken && s.savedSteamId) {
    logInfo("Quick login: using saved credentials.");
    const saved = writeSettings({
      steamId: s.savedSteamId,
      overlayToken: s.savedOverlayToken
    });
    connectLive();
    if (saved.radarOpen || (saved.panels && saved.panels.radar)) {
      try { openRadar(); } catch {}
    }
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("auth:changed", { steamId: saved.steamId });
    }
    return { success: true };
  } else {
    logInfo("Normal login: opening browser.");
    void shell.openExternal(`${baseApi()}/api/overlay/auth/steam`);
    return { pending: true };
  }
});
ipcMain.handle("auth:getAuth", () => {
  const s = readSettings();
  return { steamId: s.steamId, authed: Boolean(s.overlayToken) };
});
ipcMain.handle("auth:logout", () => {
  writeSettings({ 
    steamId: null, 
    overlayToken: null, 
    savedSteamId: null, 
    savedOverlayToken: null 
  });
  stopLive();
  try { closeRadar(); } catch {}
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send("auth:changed", { steamId: null });
});

ipcMain.handle("api:get", (_e, pathname) => apiFetch("GET", String(pathname)));
ipcMain.handle("api:post", (_e, pathname, body) => apiFetch("POST", String(pathname), body ?? {}));
ipcMain.handle("api:getfile", (_e, pathname) => apiGetFile(String(pathname)));

let mapCatalogCache = null;

function readJsonArray(fileName) {
  const dirs = [
    process.resourcesPath ? path.join(process.resourcesPath, "resources") : null,
    path.join(app.getAppPath(), "resources"),
    path.join(process.cwd(), "resources"),
    path.join(__dirname, "..", "resources"),
  ].filter(Boolean);
  for (const dir of dirs) {
    const file = path.join(dir, fileName);
    try {
      if (fs.existsSync(file)) {
        const parsed = JSON.parse(fs.readFileSync(file, "utf8"));
        if (Array.isArray(parsed)) return parsed;
      }
    } catch {
    }
  }
  return [];
}

ipcMain.handle("mapedit:getCatalog", () => {
  if (mapCatalogCache) return mapCatalogCache;
  const meshes = readJsonArray("sm_files.json")
    .map((x) => ({
      path: typeof x?.path === "string" ? x.path : "",
      name: typeof x?.name === "string" ? x.name : "",
    }))
    .filter((x) => x.path && x.name);
  const blueprints = readJsonArray("bp_files.json")
    .map((x) => ({
      path: typeof x?.path === "string" ? x.path : "",
      name: typeof x?.name === "string" ? x.name : "",
      category: typeof x?.category === "string" && x.category ? x.category : "Uncategorized",
    }))
    .filter((x) => x.path && x.name);
  mapCatalogCache = { meshes, blueprints };
  return mapCatalogCache;
});

function isNewerVersion(remote, current) {
  if (!remote || !current) return false;
  const parse = (v) => String(v).replace(/^v/i, "").split(".").map((x) => parseInt(x, 10) || 0);
  const r = parse(remote);
  const c = parse(current);
  for (let i = 0; i < Math.max(r.length, c.length); i++) {
    const rNum = r[i] || 0;
    const cNum = c[i] || 0;
    if (rNum > cNum) return true;
    if (rNum < cNum) return false;
  }
  return false;
}

ipcMain.handle("updater:restart", () => {
  if (!app.isPackaged) return false;
  try {
    autoUpdater.quitAndInstall(false, true);
    return true;
  } catch {
    return false;
  }
});
ipcMain.handle("updater:check", () => {
  if (!app.isPackaged) return false;
  autoUpdater.checkForUpdates().catch(() => {});
  return true;
});
ipcMain.handle("updater:startDownload", async () => {
  logInfo("User initiated update download via modal.");
  if (!app.isPackaged) {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:error", { message: "Không thể cập nhật trên môi trường dev (chưa đóng gói)." });
    }
    return false;
  }
  try {
    await autoUpdater.downloadUpdate();
    return true;
  } catch (err) {
    logInfo(`Download update error: ${err.message}`);
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:error", { message: err.message || "Không thể tải gói cập nhật." });
    }
    return false;
  }
});
ipcMain.handle("updater:dismiss", (_e, version) => {
  logInfo(`User dismissed update version: ${version}`);
  writeSettings({ dismissedUpdateVersion: String(version) });
  return true;
});
ipcMain.handle("updater:checkManual", async () => {
  logInfo("User triggered manual update check from settings.");
  if (!app.isPackaged) {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:status", { status: "not-packaged", message: "Đang chạy bản phát triển (chưa đóng gói)." });
    }
    return { success: false, reason: "not-packaged" };
  }
  try {
    const res = await autoUpdater.checkForUpdates();
    const currentVersion = app.getVersion();
    const remoteVersion = res?.updateInfo?.version;

    if (!remoteVersion || !isNewerVersion(remoteVersion, currentVersion)) {
      logInfo(`Manual check: App is already on latest version (v${currentVersion}). Remote version was: ${remoteVersion || "unknown"}`);
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send("updater:status", {
          status: "latest",
          version: currentVersion,
          message: `Bạn đang sử dụng phiên bản TheIsleVN mới nhất (v${currentVersion})!`
        });
      }
      return { success: true, latest: true, version: currentVersion };
    }

    logInfo(`Manual check: New version found! v${remoteVersion} > v${currentVersion}`);
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:prompt", {
        version: res.updateInfo.version,
        releaseName: res.updateInfo.releaseName || `Phiên bản ${res.updateInfo.version}`,
        releaseNotes: res.updateInfo.releaseNotes || ""
      });
    }
    return { success: true, version: res.updateInfo.version };
  } catch (err) {
    logInfo(`Manual check error: ${err.message}`);
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:status", { status: "error", message: `Không thể kiểm tra cập nhật: ${err.message}` });
    }
    return { success: false, error: err.message };
  }
});
ipcMain.handle("updater:getState", () => lastUpdaterState);

const AUTH_PROTOCOL = "isle-overlay";
if (process.defaultApp && process.argv.length >= 2) {
  app.setAsDefaultProtocolClient(AUTH_PROTOCOL, process.execPath, [path.resolve(process.argv[1])]);
} else {
  app.setAsDefaultProtocolClient(AUTH_PROTOCOL);
}

function handleDeepLink(rawUrl) {
  try {
    fs.appendFileSync(path.join(app.getPath("userData"), "deep_link.log"), `handleDeepLink called with: ${rawUrl}\n`, "utf8");
  } catch {}
  if (typeof rawUrl !== "string" || rawUrl.indexOf(`${AUTH_PROTOCOL}://`) !== 0) return;
  let parsed;
  try {
    parsed = new URL(rawUrl);
  } catch {
    return;
  }
  const sid = parsed.searchParams.get("sid");
  const token = parsed.searchParams.get("token");
  if (!sid || !/^\d{17}$/.test(sid)) return;
  const saved = writeSettings({ 
    steamId: sid, 
    overlayToken: token || null,
    savedSteamId: sid,
    savedOverlayToken: token || null
  });
  connectLive();
  if (saved.radarOpen || (saved.panels && saved.panels.radar)) {
    openRadar();
  }
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("auth:changed", { steamId: saved.steamId });
    if (!mainWindow.isVisible()) mainWindow.showInactive();
  }
}

let licenseBlocked = false;

function applyLicense() {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("overlay:blocked", licenseBlocked);
    if (licenseBlocked && !mainWindow.isVisible()) mainWindow.showInactive();
  }
  if (licenseBlocked) {
    try { closeRadar(); } catch {}
    try { setCursor(false); } catch {}
  }
}

async function checkLicense() {
  // Always bypass license check
  licenseBlocked = false;
  applyLicense();
}

let setupWindow = null;
let setupDone = false;

function showServerSetup() {
  const currentSettings = readSettings();
  const currentUrl = currentSettings.apiBaseUrl || "https://islepilot.eu";

      setupWindow = new BrowserWindow({
    width: 440,
    height: 330,
    title: "Cấu hình Server",
    icon: path.join(__dirname, "tray.ico"),
    frame: true,
    resizable: false,
    minimizable: false,
    maximizable: false,
    alwaysOnTop: true,
    center: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  setupWindow.setMenuBarVisibility(false);

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Cấu hình Server</title>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          padding: 24px;
          background-color: #060a08;
          color: #dcf1e2;
          margin: 0;
          display: flex;
          flex-direction: column;
          height: 100vh;
          box-sizing: border-box;
          justify-content: center;
        }
        .container {
          background: linear-gradient(180deg, #131b15, #0a0f0c);
          border: 1px solid #1b2a1f;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 12px 40px rgba(0,0,0,0.6);
          text-align: center;
        }
        .logo {
          font-family: monospace;
          font-size: 16px;
          font-weight: bold;
          color: #7cf2a6;
          letter-spacing: 0.1em;
          margin-bottom: 8px;
          text-transform: uppercase;
        }
        .desc {
          font-size: 13px;
          color: #82997f;
          margin-bottom: 20px;
          line-height: 1.4;
        }
        input {
          width: 100%;
          padding: 10px 14px;
          box-sizing: border-box;
          border: 1px solid #1b2a1f;
          border-radius: 8px;
          background-color: #0c130d;
          color: #dcf1e2;
          font-size: 14px;
          margin-bottom: 20px;
          text-align: center;
        }
        input:focus {
          border-color: #7cf2a6;
          outline: none;
          box-shadow: 0 0 10px rgba(124, 242, 166, 0.15);
        }
        button {
          width: 100%;
          padding: 11px;
          border: 1px solid #7cf2a62e;
          background-color: #7cf2a61f;
          color: #7cf2a6;
          font-family: monospace;
          font-size: 13px;
          font-weight: 600;
          letter-spacing: 0.05em;
          border-radius: 8px;
          cursor: pointer;
          transition: background 0.18s, box-shadow 0.18s;
        }
        button:hover {
          background-color: #7cf2a633;
          box-shadow: 0 0 15px -4px rgba(124, 242, 166, 0.3);
        }
      </style>
    </head>
    <body>
            <div class="container">
                <div class="logo" style="display: flex; align-items: center; justify-content: center; gap: 8px;">
          <svg viewBox="0 0 24 24" width="20" height="20" style="vertical-align: middle;">
            <path d="M23.498 6.163a3.003 3.003 0 0 0-2.11-2.11C19.518 3.545 12 3.545 12 3.545s-7.518 0-9.388.508a3.003 3.003 0 0 0-2.11 2.11C0 8.033 0 12 0 12s0 3.967.502 5.837a3.003 3.003 0 0 0 2.11 2.11c1.87.508 9.388.508 9.388.508s7.518 0 9.388-.508a3.003 3.003 0 0 0 2.11-2.11C24 15.967 24 12 24 12s0-3.967-.502-5.837z" fill="#ff0000"/>
            <path d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="#ffffff"/>
          </svg>
          THE ISLE INFORMATION
        </div>
        <div class="desc">Vui lòng cấu hình URL Server của bạn để tiếp tục:</div>
        <input type="text" id="serverUrl" value="${currentUrl}" placeholder="https://...">
        <button onclick="save()">Xác nhận (Confirm)</button>
        <div style="margin-top: 15px; display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 12px; color: #82997f;">
          <span style="display: inline-flex; align-items: center; gap: 5px; cursor: pointer; color: #7cf2a6; text-decoration: none;" onclick="openYoutube()">
            <svg viewBox="0 0 24 24" width="14" height="14" style="vertical-align: middle;">
              <path d="M23.498 6.163a3.003 3.003 0 0 0-2.11-2.11C19.518 3.545 12 3.545 12 3.545s-7.518 0-9.388.508a3.003 3.003 0 0 0-2.11 2.11C0 8.033 0 12 0 12s0 3.967.502 5.837a3.003 3.003 0 0 0 2.11 2.11c1.87.508 9.388.508 9.388.508s7.518 0 9.388-.508a3.003 3.003 0 0 0 2.11-2.11C24 15.967 24 12 24 12s0-3.967-.502-5.837z" fill="#ff0000"/>
              <path d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="#ffffff"/>
            </svg>
            YouTube: Bánh Mì Biết Chơi
          </span>
        </div>
      </div>
            <script>
        const { ipcRenderer, shell } = require('electron');
        let saving = false;
        document.getElementById('serverUrl').addEventListener('keydown', (e) => {
          if (e.key === 'Enter') save();
        });
        function save() {
          if (saving) return;
          const url = document.getElementById('serverUrl').value.trim();
          if (url) {
            saving = true;
            const btn = document.querySelector('button');
            btn.disabled = true;
            btn.innerText = 'Đang kết nối...';
            setTimeout(() => {
              ipcRenderer.send('server:setup-done', url);
            }, 5000);
          }
        }
        function openYoutube() {
          shell.openExternal('https://www.youtube.com/@BanhMiBietChoi');
        }
      </script>
    </body>
    </html>
  `;
  
  setupWindow.loadURL("data:text/html;charset=utf-8," + encodeURIComponent(htmlContent));

  setupWindow.on("closed", () => {
    setupWindow = null;
    if (!setupDone) {
      app.quit();
    }
  });
}

ipcMain.on("server:setup-done", (e, newUrl) => {
  setupDone = true;
  writeSettings({ apiBaseUrl: newUrl });
  
  if (setupWindow && !setupWindow.isDestroyed()) {
    setupWindow.close();
  }
  
  createWindow();
  createTray();
  const boot = readSettings();
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.setOpacity(boot.opacity);
  }
  connectLive();
  startCursorHook();
  initAutoUpdate();
  void trackGame();
  setInterval(() => {
    void trackGame();
  }, 700);
  void checkLicense();
  setInterval(() => {
    void checkLicense();
  }, 5 * 60 * 1000);
  
  const startUrl = process.argv.find((a) => typeof a === "string" && a.indexOf(`${AUTH_PROTOCOL}://`) === 0);
  if (startUrl) handleDeepLink(startUrl);
});

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
    app.on("second-instance", (_e, argv) => {
    try {
      fs.appendFileSync(path.join(app.getPath("userData"), "deep_link.log"), `second-instance called. Argv: ${JSON.stringify(argv)}\n`, "utf8");
    } catch {}
    const url = argv.find((a) => typeof a === "string" && a.includes(`${AUTH_PROTOCOL}://`));
    if (url) {
      let cleanUrl = url.trim();
      if (cleanUrl.startsWith('"') && cleanUrl.endsWith('"')) {
        cleanUrl = cleanUrl.slice(1, -1);
      }
      handleDeepLink(cleanUrl);
    }
    if (mainWindow && !mainWindow.isDestroyed()) {
      if (!dashOn) {
        toggleDash();
      } else {
        mainWindow.showInactive();
        mainWindow.setAlwaysOnTop(true, "screen-saver");
      }
    }
  });
  app.on("open-url", (_e, url) => {
    try {
      fs.appendFileSync(path.join(app.getPath("userData"), "deep_link.log"), `open-url called. Url: ${url}\n`, "utf8");
    } catch {}
    if (url) {
      let cleanUrl = url.trim();
      if (cleanUrl.startsWith('"') && cleanUrl.endsWith('"')) {
        cleanUrl = cleanUrl.slice(1, -1);
      }
      handleDeepLink(cleanUrl);
    }
  });

   app.whenReady().then(() => {
    logInfo("app.whenReady fired.");
    const current = readSettings();
    writeSettings({
      steamId: null,
      overlayToken: null,
      panels: current.panels || { heart: false, stats: true, prime: true, radar: true },
      radarOpen: typeof current.radarOpen === "boolean" ? current.radarOpen : true,
      radarBounds: current.radarBounds || { x: 10, y: 10, width: 320, height: 320 },
      layout: {
        ...current.layout || {},
        w_prime: (current.layout && current.layout.w_prime) || { x: 240, y: 10 }
      }
    });
    createWindow();
    createTray();
    const boot = readSettings();
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.setOpacity(boot.opacity);
    }
    connectLive();
    startHttpFallbackPolling();
    if (boot.panels && boot.panels.radar) {
      openRadar();
    }
    startCursorHook();
    initAutoUpdate();
    void trackGame();
    setInterval(() => {
      void trackGame();
    }, 700);
    void checkLicense();
    setInterval(() => {
      void checkLicense();
    }, 5 * 60 * 1000);

    const startUrl = process.argv.find((a) => typeof a === "string" && a.includes(`${AUTH_PROTOCOL}://`));
    if (startUrl) {
      let cleanUrl = startUrl.trim();
      if (cleanUrl.startsWith('"') && cleanUrl.endsWith('"')) {
        cleanUrl = cleanUrl.slice(1, -1);
      }
      handleDeepLink(cleanUrl);
    }
  });
}

app.on("before-quit", () => {
  try {
    if (uio && uioStarted) uio.uIOhook.stop();
  } catch {}
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

function initAutoUpdate() {
  if (!app.isPackaged) return;

  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = false;

  autoUpdater.on("checking-for-update", () => {
    lastUpdaterState = { state: "checking" };
    logInfo("AutoUpdater: Checking for update...");
  });

  autoUpdater.on("update-available", (info) => {
    const currentVersion = app.getVersion();
    if (!info?.version || !isNewerVersion(info.version, currentVersion)) {
      logInfo(`AutoUpdater: Ignored update-available event for ${info?.version} because current is ${currentVersion}`);
      lastUpdaterState = { state: "idle" };
      return;
    }
    lastUpdaterState = { state: "available", version: info.version };
    logInfo(`AutoUpdater: Update available: ${info.version} (current is ${currentVersion})`);
    const s = readSettings();
    if (s.dismissedUpdateVersion === info.version) {
      logInfo(`AutoUpdater: Version ${info.version} was previously dismissed by user. Skipping dialog.`);
      return;
    }
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:prompt", {
        version: info.version,
        releaseName: info.releaseName || `Phiên bản ${info.version}`,
        releaseNotes: info.releaseNotes || ""
      });
    }
  });

  autoUpdater.on("update-not-available", () => {
    lastUpdaterState = { state: "idle" };
    logInfo("AutoUpdater: Update not available.");
  });

  autoUpdater.on("error", (err) => {
    lastUpdaterState = { state: "error", error: err ? err.message : "Unknown error" };
    logInfo(`AutoUpdater error: ${err ? err.stack : "Unknown"}`);
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:error", { message: err ? err.message : "Lỗi cập nhật không xác định" });
    }
  });

  autoUpdater.on("download-progress", (progressObj) => {
    lastUpdaterState = { 
      state: "downloading", 
      percent: progressObj.percent, 
      bytesPerSecond: progressObj.bytesPerSecond,
      transferred: progressObj.transferred,
      total: progressObj.total
    };
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:progress", {
        percent: Math.round(progressObj.percent || 0),
        bytesPerSecond: Math.round(progressObj.bytesPerSecond || 0),
        transferred: progressObj.transferred || 0,
        total: progressObj.total || 0
      });
    }
  });

  autoUpdater.on("update-downloaded", (info) => {
    lastUpdaterState = { state: "downloaded", version: info.version };
    logInfo("AutoUpdater: Update downloaded, ready to install.");
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("updater:downloaded", { version: info.version });
    }
    setTimeout(() => {
      autoUpdater.quitAndInstall(false, true);
    }, 2500);
  });

  setTimeout(() => {
    autoUpdater.checkForUpdates().catch((err) => {
      logInfo(`AutoUpdater check failed: ${err.message}`);
    });
  }, 4000);
}
