const { safeStorage, app } = require('electron');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const logPath = path.join(__dirname, "scratch", "diagnostic_run.log");
fs.mkdirSync(path.dirname(logPath), { recursive: true });
fs.writeFileSync(logPath, "=== Diagnostic Started ===\n", "utf8");

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(logPath, line, "utf8");
}

app.whenReady().then(() => {
  const settingsPath = path.join(app.getPath("userData"), "theisleinformation-bybanhmibietchoi.settings.json");
  log("Settings file path: " + settingsPath);
  
  if (!fs.existsSync(settingsPath)) {
    log("ERROR: Settings file not found!");
    app.quit();
    return;
  }
  
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  let token = settings.overlayToken;
  
  if (token && token.startsWith("enc1:")) {
    try {
      token = safeStorage.decryptString(Buffer.from(token.slice(5), "base64"));
      log("Decrypted Token successfully!");
    } catch (e) {
      log("ERROR: Failed to decrypt token: " + e.message);
      app.quit();
      return;
    }
  }
  
  const baseApi = (settings.apiBaseUrl || "https://sbtcisland.islepilot.eu/").replace(/\/+$/, "");
  const wsUrl = baseApi.replace(/^http/i, "ws") + "/ows";
  log(`Target WebSocket URL: ${wsUrl}`);
  
  log("Initiating WebSocket connection...");
  const ws = new WebSocket(wsUrl, {
    headers: { Authorization: `Bearer ${token}` }
  });
  
  ws.on('open', () => {
    log("SUCCESS: WebSocket connected!");
    ws.send(JSON.stringify({ t: 'hello', name: 'diagnostic' }));
  });
  
  ws.on('message', (data) => {
    log("Received message: " + data.toString());
  });
  
  ws.on('error', (err) => {
    log("ERROR: WebSocket Error: " + err.message);
  });
  
  ws.on('close', (code, reason) => {
    log(`CLOSED: WebSocket closed. Code: ${code}, Reason: ${reason}`);
    app.quit();
  });
  
  setTimeout(() => {
    log("Timeout reached. Closing test.");
    ws.terminate();
    app.quit();
  }, 10000);
});
