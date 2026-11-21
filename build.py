"""Builds the GitHub Pages site (index.html) from ../the-last-violin-ios.html.

Run with: python3 build.py
The source file is written for Claude artifacts, which add the page skeleton themselves,
so this wraps it in a full page with iPhone home-screen settings (full screen app mode,
icon, dark status bar) and swaps the title-screen tip for an "Add to Home Screen" hint.
"""
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / 'the-last-violin-ios.html'

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="The Last Violin: a ten-level chase platformer. Gather notes, defeat each tower's guardian, and play the last violin to drive back The Hush.">
<meta name="theme-color" content="#07050c">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Last Violin">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="manifest" href="manifest.webmanifest">
<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}[hidden]{display:none!important}</style>
'''

# On the site (not inside a frame) the "Play full screen" button hides itself on iPhone,
# so point people to Add to Home Screen instead, which opens the game full screen.
TIP = '''<script>
(() => {
  const tip = document.getElementById('rotTip'); if (!tip) return;
  let framed = false; try { framed = window.self !== window.top; } catch (e) { framed = true; }
  if (framed) return;
  const app = navigator.standalone || matchMedia('(display-mode: standalone)').matches || matchMedia('(display-mode: fullscreen)').matches;
  tip.textContent = app
    ? 'Turn your phone sideways for the biggest view, or tap \\u27f3 at the top to turn the game sideways.'
    : 'Tip: tap Share, then Add to Home Screen, to play full screen like an app. Turn your phone sideways for the biggest view.';
})();
</script>
'''

s = SRC.read_text()
split = s.index('<div id="app">')  # everything before it is title, fonts and styles
html = HEAD + s[:split] + '</head>\n<body>\n' + s[split:] + '\n' + TIP + '</body>\n</html>\n'
(HERE / 'index.html').write_text(html)
print('index.html', len(html), 'bytes')
