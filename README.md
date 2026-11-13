# OpenCode Codex Pet

An unofficial OpenCode TUI plugin that brings a small animated companion into the terminal. The home screen uses the running animation; the conversation sidebar uses the laptop-holding work animation.

<img width="914" height="481" alt="Screenshot 2026-11-11 153114" src="https://github.com/user-attachments/assets/5b1978d9-c319-481f-bd46-5923ed0920bf" /> 




## What it does

- Animates the pet on OpenCode's home screen.
- Shows the laptop-holding animation in the session sidebar.
- Uses colored terminal blocks with the terminal's current background.
- Keeps the sprite image and derived frame data local so they are not uploaded with the source.

## Requirements

- OpenCode CLI 1.19.x using the V1 TUI plugin API.
- Node.js/npm for the plugin runtime dependencies.
- Python 3.10+ and Pillow to build the local terminal frames.

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

