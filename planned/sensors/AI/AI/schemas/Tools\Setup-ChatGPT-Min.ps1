# One-shot ChatGPT CLI setup (minimal, low-bandwidth)
# - Creates C:\Tools\ChatGPT-CLI
# - Python venv + openai SDK
# - Persists OPENAI_API_KEY (User)
# - Adds ask.py + stream support
# - Adds Start Menu shortcut + run-gpt shim

$ErrorActionPreference = 'Stop'

# --- Paths & defaults ---
$ROOT = 'C:\Tools\ChatGPT-CLI'
$VENV = Join-Path $ROOT '.venv'
$PY   = Join-Path $VENV 'Scripts\python.exe'
$PIP  = Join-Path $VENV 'Scripts\pip.exe'
$MODEL_DEFAULT = 'gpt-5'

# --- Ensure root + venv ---
New-Item -Force -ItemType Directory $ROOT | Out-Null
if (-not (Test-Path $VENV)) { py -3 -m venv $VENV }

# --- Bootstrap packages ---
& $PIP install --upgrade pip wheel | Out-Null
& $PIP install openai | Out-Null

# --- Ask for API key if missing, then persist (User scope) ---
if (-not $env:OPENAI_API_KEY) {
  $key = Read-Host 'Enter your OPENAI_API_KEY (sk-...)'
  if (-not $key) { throw "OPENAI_API_KEY is required once. Re-run and provide it." }
  [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $key, 'User')
}
# Also set a default model (user-level) if absent
if (-not [Environment]::GetEnvironmentVariable('OPENAI_MODEL','User')) {
  [Environment]::SetEnvironmentVariable('OPENAI_MODEL', $MODEL_DEFAULT, 'User')
}

# --- ask.py (minimal CLI w/ token cap for rural links) ---
@'
from openai import OpenAI
import os, sys
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model  = os.environ.get("OPENAI_MODEL","gpt-5")
prompt = " ".join(sys.argv[1:]) or "Say hello in 5 words."
resp = client.responses.create(
    model=model,
    input=[{"role":"user","content":prompt}],
    max_output_tokens=300,   # keep responses compact on slow links
    temperature=0.2
)
print(resp.output_text)
'@ | Set-Content -Encoding UTF8 (Join-Path $ROOT 'ask.py')

# --- stream.py (token-by-token output for faster first byte) ---
@'
from openai import OpenAI
import os, sys
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model  = os.environ.get("OPENAI_MODEL","gpt-5")
prompt = " ".join(sys.argv[1:]) or "3 bullet tips for slow internet dev."
with client.responses.stream(model=model,
    input=[{"role":"user","content":prompt}],
    temperature=0.3,
    max_output_tokens=300) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
'@ | Set-Content -Encoding UTF8 (Join-Path $ROOT 'stream.py')

# --- run-gpt.ps1 wrapper (ask | stream) ---
@"
param([Parameter(ValueFromRemainingArguments=\$true)][string[]]\$Args)
if (\$Args.Count -eq 0) { Write-Host 'Usage: run-gpt ask <prompt>   OR   run-gpt stream <prompt>'; exit 1 }
\$mode = \$Args[0]; \$rest = \$Args[1..(\$Args.Count-1)]
switch (\$mode) {
  'ask'    { & '$PY' (Join-Path '$ROOT' 'ask.py')    @rest; break }
  'stream' { & '$PY' (Join-Path '$ROOT' 'stream.py') @rest; break }
  default  { Write-Host 'Usage: run-gpt ask <prompt>   OR   run-gpt stream <prompt>' }
}
"@ | Set-Content -Encoding UTF8 (Join-Path $ROOT 'run-gpt.ps1')

# --- Global shim so `run-gpt` works anywhere ---
$Bin = Join-Path $env:USERPROFILE '.local\bin'
New-Item -Force -ItemType Directory $Bin | Out-Null
"pwsh -ExecutionPolicy Bypass -File `"$ROOT\run-gpt.ps1`" `"$args`"" |
  Set-Content (Join-Path $Bin 'run-gpt.cmd')

# Ensure ~/.local/bin is on PATH for the user
$uPath = [Environment]::GetEnvironmentVariable('Path','User')
if ($uPath -notlike "*\.local\bin*") {
  [Environment]::SetEnvironmentVariable('Path', $uPath + ';' + $Bin, 'User')
}

# --- Start Menu shortcut (optional) ---
$WshShell  = New-Object -ComObject WScript.Shell
$Programs  = [Environment]::GetFolderPath('Programs')
$Shortcut  = $WshShell.CreateShortcut((Join-Path $Programs 'ChatGPT CLI.lnk'))
$Shortcut.TargetPath = 'pwsh.exe'
$Shortcut.Arguments  = "-ExecutionPolicy Bypass -File `"$ROOT\run-gpt.ps1`" ask"
$Shortcut.WorkingDirectory = $ROOT
$Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,280"
$Shortcut.Save()

Write-Host "`nInstalled ChatGPT CLI at $ROOT"
Write-Host "OPENAI_API_KEY saved (User). Default model: $MODEL_DEFAULT"
Write-Host "Open a NEW terminal, then try:"
Write-Host '  run-gpt ask   "One-line BrainSim build order"'
Write-Host '  run-gpt stream "3 bullet tips for offline-first Windows dev"'
