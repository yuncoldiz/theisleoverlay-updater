import sys
from pathlib import Path

js_path = Path("src_extracted/dist/assets/index-CealnApy.js")
code = js_path.read_text(encoding="utf-8")

old_code = 'C=B.useCallback(w=>{if(w.button!==0)return;w.preventDefault();const I=w.currentTarget,G=w.pointerId,D=w.screenX,E=w.screenY;window.isleOverlay.radarGetBounds().then(k=>{if(!k)return;try{I.setPointerCapture(G)}catch{}const H=N=>{window.isleOverlay.radarSetBounds({x:k.x+(N.screenX-D),y:k.y+(N.screenY-E),width:k.width,height:k.height})},V=()=>{try{I.releasePointerCapture(G)}catch{}I.removeEventListener("pointermove",H),I.removeEventListener("pointerup",V)};I.addEventListener("pointermove",H),I.addEventListener("pointerup",V)})},[]);return y.jsx("div",{ref:m,style:Ej,children:y.jsx("div",{onPointerDown:C,style:{cursor:"grab",pointerEvents:"auto"}'

new_code = 'C=B.useCallback(w=>{if(w.button!==0)return;w.preventDefault();const D=w.screenX,E=w.screenY,initX=window.screenX,initY=window.screenY,winW=window.outerWidth||320,winH=window.outerHeight||320;const H=N=>{window.isleOverlay.radarSetBounds({x:Math.round(initX+(N.screenX-D)),y:Math.round(initY+(N.screenY-E)),width:winW,height:winH})};const V=()=>{window.removeEventListener("pointermove",H);window.removeEventListener("pointerup",V);window.removeEventListener("mousemove",H);window.removeEventListener("mouseup",V)};window.addEventListener("pointermove",H);window.addEventListener("pointerup",V);window.addEventListener("mousemove",H);window.addEventListener("mouseup",V)},[]);return y.jsx("div",{ref:m,style:Ej,children:y.jsx("div",{className:"interactive-region",onPointerDown:C,onMouseDown:C,style:{cursor:"grab",pointerEvents:"auto",userSelect:"none"}'

if old_code in code:
    updated = code.replace(old_code, new_code)
    js_path.write_text(updated, encoding="utf-8")
    print("SUCCESS: Radar drag handler updated in index-CealnApy.js!")
else:
    print("ERROR: old_code not found in index-CealnApy.js")
    sys.exit(1)
