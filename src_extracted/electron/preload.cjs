const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("isleOverlay", {
  getSettings: () => ipcRenderer.invoke("overlay:getSettings"),
  setSettings: (next) => ipcRenderer.invoke("overlay:setSettings", next),
  openUrl: (url) => ipcRenderer.invoke("overlay:openUrl", url),

  getState: () => ipcRenderer.invoke("overlay:getState"),
  setMouseIgnore: (ignore) => ipcRenderer.invoke("overlay:mouseIgnore", ignore),
  onState: (cb) => {
    const h = (_e, s) => cb(s);
    ipcRenderer.on("overlay:state", h);
    return () => ipcRenderer.removeListener("overlay:state", h);
  },
  quit: () => ipcRenderer.invoke("overlay:quit"),
  openUrl: (url) => ipcRenderer.invoke("app:openUrl", url),

  steamLogin: () => ipcRenderer.invoke("auth:steamLogin"),
  getAuth: () => ipcRenderer.invoke("auth:getAuth"),
  logout: () => ipcRenderer.invoke("auth:logout"),
  onAuthChanged: (cb) => {
    const h = (_e, s) => cb(s);
    ipcRenderer.on("auth:changed", h);
    return () => ipcRenderer.removeListener("auth:changed", h);
  },

  apiGet: (pathname) => ipcRenderer.invoke("api:get", pathname),
  apiPost: (pathname, body) => ipcRenderer.invoke("api:post", pathname, body),
  apiGetFile: (pathname) => ipcRenderer.invoke("api:getfile", pathname),

  getMapCatalog: () => ipcRenderer.invoke("mapedit:getCatalog"),

  onLive: (cb) => {
    const h = (_e, d) => cb(d);
    ipcRenderer.on("overlay:live", h);
    return () => ipcRenderer.removeListener("overlay:live", h);
  },

  onTicket: (cb) => {
    const h = (_e, frame) => cb(frame);
    ipcRenderer.on("overlay:ticket", h);
    return () => ipcRenderer.removeListener("overlay:ticket", h);
  },

  onTroll: (cb) => {
    const h = (_e, frame) => cb(frame);
    ipcRenderer.on("overlay:troll", h);
    return () => ipcRenderer.removeListener("overlay:troll", h);
  },
  onTrollAudio: (cb) => {
    const h = (_e, chunk) => cb(chunk);
    ipcRenderer.on("overlay:troll-audio", h);
    return () => ipcRenderer.removeListener("overlay:troll-audio", h);
  },

  sendLiveSkin: (state) => ipcRenderer.invoke("skin:send", state),
  recordCursorKey: () => ipcRenderer.invoke("cursor:recordKey"),
  recordDashKey: () => ipcRenderer.invoke("dash:recordKey"),
  setDashOpen: (open) => ipcRenderer.invoke("overlay:dashOpen", open),
  onDash: (cb) => {
    const h = (_e, on) => cb(on);
    ipcRenderer.on("overlay:dash", h);
    return () => ipcRenderer.removeListener("overlay:dash", h);
  },
  onCursor: (cb) => {
    const h = (_e, on) => cb(on);
    ipcRenderer.on("overlay:cursor", h);
    return () => ipcRenderer.removeListener("overlay:cursor", h);
  },
  onBlocked: (cb) => {
    const h = (_e, blocked) => cb(blocked);
    ipcRenderer.on("overlay:blocked", h);
    return () => ipcRenderer.removeListener("overlay:blocked", h);
  },

  onSettingsChanged: (cb) => {
    const h = (_e, s) => cb(s);
    ipcRenderer.on("settings:changed", h);
    return () => ipcRenderer.removeListener("settings:changed", h);
  },

  radarToggle: () => ipcRenderer.invoke("radar:toggle"),
  radarClose: () => ipcRenderer.invoke("radar:close"),
  radarIsOpen: () => ipcRenderer.invoke("radar:isOpen"),
  radarGetBounds: () => ipcRenderer.invoke("radar:getBounds"),
  radarSetBounds: (b) => ipcRenderer.invoke("radar:setBounds", b),
  onRadarChanged: (cb) => {
    const h = (_e, d) => cb(d);
    ipcRenderer.on("radar:changed", h);
    return () => ipcRenderer.removeListener("radar:changed", h);
  },

  updaterRestart: () => ipcRenderer.invoke("updater:restart"),
  updaterCheck: () => ipcRenderer.invoke("updater:check"),
  updaterGetState: () => ipcRenderer.invoke("updater:getState"),
  startUpdateDownload: () => ipcRenderer.invoke("updater:startDownload"),
  dismissUpdate: (version) => ipcRenderer.invoke("updater:dismiss", version),
  checkManualUpdate: () => ipcRenderer.invoke("updater:checkManual"),
  onUpdatePrompt: (cb) => {
    const h = (_e, data) => cb(data);
    ipcRenderer.on("updater:prompt", h);
    return () => ipcRenderer.removeListener("updater:prompt", h);
  },
  onUpdateProgress: (cb) => {
    const h = (_e, data) => cb(data);
    ipcRenderer.on("updater:progress", h);
    return () => ipcRenderer.removeListener("updater:progress", h);
  },
  onUpdateDownloaded: (cb) => {
    const h = (_e, data) => cb(data);
    ipcRenderer.on("updater:downloaded", h);
    return () => ipcRenderer.removeListener("updater:downloaded", h);
  },
  onUpdateError: (cb) => {
    const h = (_e, data) => cb(data);
    ipcRenderer.on("updater:error", h);
    return () => ipcRenderer.removeListener("updater:error", h);
  },
  onUpdateStatus: (cb) => {
    const h = (_e, data) => cb(data);
    ipcRenderer.on("updater:status", h);
    return () => ipcRenderer.removeListener("updater:status", h);
  },
  onUpdaterEvent: (cb) => {
    const h = (_e, s) => cb(s);
    ipcRenderer.on("updater:event", h);
    return () => ipcRenderer.removeListener("updater:event", h);
  },

  recordMapKey: () => ipcRenderer.invoke("map:recordKey"),
  recordPrimeKey: () => ipcRenderer.invoke("prime:recordKey"),
  recordStatsKey: () => ipcRenderer.invoke("stats:recordKey"),
  recordReloadKey: () => ipcRenderer.invoke("reload:recordKey"),
  recordResetLayoutKey: () => ipcRenderer.invoke("resetLayout:recordKey"),
  reloadApp: () => ipcRenderer.invoke("app:reload"),
  resetLayout: () => ipcRenderer.invoke("layout:reset"),

  onHotkeyMap: (cb) => {
    const h = () => cb();
    ipcRenderer.on("hotkey:map", h);
    return () => ipcRenderer.removeListener("hotkey:map", h);
  },
  onHotkeyPrime: (cb) => {
    const h = () => cb();
    ipcRenderer.on("hotkey:prime", h);
    return () => ipcRenderer.removeListener("hotkey:prime", h);
  },
  onHotkeyStats: (cb) => {
    const h = () => cb();
    ipcRenderer.on("hotkey:stats", h);
    return () => ipcRenderer.removeListener("hotkey:stats", h);
  },
});

if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", () => {
    let dashOn = true;
    let cursorOn = false;
    let isUpdateModalOpen = false;
    let isMouseOverInteractive = false;

    const updateIgnore = () => {
      const needsInteractivity = dashOn || cursorOn || isUpdateModalOpen;
      if (!needsInteractivity) {
        ipcRenderer.invoke("overlay:mouseIgnore", true);
        return;
      }
      ipcRenderer.invoke("overlay:mouseIgnore", !isMouseOverInteractive);
    };

    ipcRenderer.on("overlay:dash", (_e, on) => {
      dashOn = on;
      updateIgnore();
    });

    ipcRenderer.on("overlay:cursor", (_e, on) => {
      cursorOn = on;
      updateIgnore();
    });

    ipcRenderer.on("updater:prompt", () => {
      isUpdateModalOpen = true;
      updateIgnore();
    });

    window.addEventListener("updateModalClosed", () => {
      isUpdateModalOpen = false;
      updateIgnore();
    });

    window.addEventListener("mousemove", (e) => {
      let isInteractive = false;
      let el = e.target;
      while (el) {
        if (el.id === "updateModalContainer" || el.id === "updateToastContainer") {
          isInteractive = true;
          break;
        }
        if (el.classList && (
          el.classList.contains("interactive-region") ||
          el.classList.contains("envelopeFloat") ||
          el.classList.contains("statusPill") ||
          el.tagName === "BUTTON" ||
          el.tagName === "INPUT" ||
          el.tagName === "A" ||
          el.tagName === "TEXTAREA" ||
          el.tagName === "SELECT"
        )) {
          isInteractive = true;
          break;
        }
        el = el.parentElement;
      }
      
      if (isInteractive !== isMouseOverInteractive) {
        isMouseOverInteractive = isInteractive;
        updateIgnore();
      }
    });

    document.addEventListener("mouseleave", () => {
      isMouseOverInteractive = false;
      updateIgnore();
    });
  });
}
