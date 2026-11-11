# OpenCode Codex Pet

An unofficial OpenCode TUI plugin that brings a small animated companion into the terminal. The home screen uses the running animation; the conversation sidebar uses the laptop-holding work animation.

![Codex pet sprite atlas preview, linked from the OpenAI CDN](https://cdn.openai.com/c6d7b0d0-3abf-40b5-9d0c-ecd2b9364692/codex-spritesheet-v4.webp)

The preview is linked from OpenAI's CDN. The original artwork and the generated frame data are excluded from Git. To build a local copy, supply a sprite sheet you are authorized to use. See <code>NOTICE.md</code>.

## What it does

- Animates the pet on OpenCode's home screen.
- Shows the laptop-holding animation in the session sidebar.
- Uses colored terminal blocks with the terminal's current background.
- Keeps the sprite image and derived frame data local so they are not uploaded with the source.

## Requirements

- OpenCode CLI 1.19.x using the V1 TUI plugin API.
- Node.js/npm for the plugin runtime dependencies.
- Python 3.10+ and Pillow to build the local terminal frames.
- A compatible 1536x1872 sprite sheet that you are authorized to use.

OpenCode V2 uses a different plugin API and needs a port of <code>src/tui.tsx</code>.

## Install

1. Clone this repository into the global OpenCode plugin folder, for example <code>%USERPROFILE%\\.config\\opencode\\plugins\\opencode-codex-pet</code>.
2. Put your authorized sprite sheet at <code>assets/codex-spritesheet-v4.webp</code>. On a machine where the current plugin is already installed, you can copy its local sprite sheet with:

   ~~~powershell
   $plugin = Join-Path $env:USERPROFILE '.config\\opencode\\plugins\\opencode-codex-pet'
   Copy-Item (Join-Path $env:USERPROFILE '.config\\opencode\\plugins\\codex-pet\\codex-spritesheet-v4.webp') (Join-Path $plugin 'assets\\codex-spritesheet-v4.webp')
   ~~~

3. Generate the local frames:

   ~~~powershell
   cd "$env:USERPROFILE\\.config\\opencode\\plugins\\opencode-codex-pet"
   py -m pip install -r requirements.txt
   py scripts/build_frames.py
   ~~~

4. Install the TUI peer dependencies into OpenCode's global config if they are not already present:

   ~~~powershell
   npm install --prefix "$env:USERPROFILE\\.config\\opencode" --save-exact '@opencode-ai/plugin@1.18.30' '@opentui/core@0.4.5' '@opentui/solid@0.4.5' 'solid-js@1.9.12'
   ~~~

5. Add this entry to <code>%USERPROFILE%\\.config\\opencode\\tui.json</code>, preserving any other settings:

   ~~~json
   {
     "$schema": "https://opencode.ai/tui.json",
     "plugin": ["./plugins/opencode-codex-pet/src/tui.tsx"]
   }
   ~~~

6. Restart OpenCode.

## Build the local frames

The frame generator reads the local sprite sheet, uses the idle/running/work rows, and writes <code>src/frames.js</code>. Both that generated file and the sprite sheet are ignored by Git.

~~~powershell
py -m pip install -r requirements.txt
py scripts/build_frames.py
~~~

## Project files

- <code>src/tui.tsx</code> — OpenCode TUI slots and animation component.
- <code>scripts/build_frames.py</code> — converts an authorized sprite sheet into terminal frames.
- <code>assets/</code> — local sprite input; ignored by Git.
- <code>src/frames.js</code> — generated local animation data; ignored by Git.

See <code>NOTICE.md</code> for the artwork and branding note. This repository does not include a license for reuse; add one if you want to grant permission for others to reuse the plugin code.
