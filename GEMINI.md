# Custom Rules and Workflow for TheIsleOverlay-BanhMiBietChoi

Welcome to the project custom guidelines. Follow these rules to ensure secure compilation, smooth development, and prevent critical errors that could affect distributed users.

## 1. Secure Packing Workflow
- **Rule**: Always use the secure packing script [pack_secure_app.py](file:///c:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/pack_secure_app.py) to package the application. Do NOT use the old `pack_app.py` unless explicitly instructed.
- **Why**: [pack_secure_app.py](file:///c:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/pack_secure_app.py) automatically runs `javascript-obfuscator` on key files (`main.cjs`, `preload.cjs`, `native-windows.cjs`, `index-*.js`) to scramble variable names and encrypt string arrays (URLs, API keys, tokens), preventing users from decompiling or stealing the source code.

## 2. Preventing Permission & File Lock Errors
- **Rule**: Before compiling/repacking the app, always check for and terminate any running background instances of `TheIsleVn-BanhMi.exe`.
- **Why**: If the application is running in the background, Windows locks the DLL files and native modules (such as `koffi.node` and `uiohook-napi`). Overwriting them during packing will trigger `PermissionError: [Errno 13] Permission denied`.

## 3. Safe Development and Auto-Update Mechanism
- **Rule**: 
  1. **Strict Local Isolation**: When developing new features, only run and test code locally on your development machine. 
  2. **Do Not Push Untested Updates**: Never upload updated package files (`Setup.exe` / `latest.yml`) to the official update host (e.g., GitHub Releases or Web Server) until you have fully verified the changes locally and through beta testers.
  3. **Auto-Updater Safety**: The `initAutoUpdate()` function in `main.cjs` is disabled by default. If you decide to re-enable it, always ensure that [app-update.yml](file:///c:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/resources/app-update.yml) points to the custom update server owned by you (e.g., your own GitHub repository/website), **never** to the original author's official update URL (`islepilot.eu`). Otherwise, users will receive official updates that will overwrite and erase all your custom channel overlays and logo modifications.
