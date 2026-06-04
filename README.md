# Codex MCP Abaqus

Utilities and examples for driving Abaqus through a file-based MCP bridge from
Codex or other MCP clients.

This project collects the patched Abaqus MCP plugin, MCP stdio server, startup
scripts, and a classic finite element example verified on Abaqus 2022.

## What Is Included

- `src/abaqus_mcp_plugin.py`  
  Abaqus/CAE kernel-side plugin. It polls command JSON files, executes Abaqus
  Python code, submits jobs, and writes result JSON files.
- `src/mcp_server.py`  
  MCP server exposing tools such as `check_abaqus_connection`,
  `execute_script`, `get_model_info`, `list_jobs`, and `submit_job`.
- `scripts/start_abaqus_mcp_loop.py`  
  noGUI worker launcher script. Recommended for stable background simulation.
- `examples/abaqus_cantilever_classic.py`  
  Classic 3D cantilever beam static bending example.
- `docs/USAGE.md`  
  Setup and operating notes.

## Recommended Mode

Use **Abaqus noGUI** for simulation automation:

```powershell
abaqus cae noGUI=scripts\start_abaqus_mcp_loop.py
```

Running MCP inside the Abaqus GUI with Cooperative mode works, but it can make
the GUI sluggish because the GUI thread is used for command polling. For most
batch simulations, keep the Abaqus window closed and let noGUI produce `.cae`,
`.inp`, `.odb`, and summary files.

## Quick Start

1. Install the MCP server dependency:

```powershell
python -m pip install -r requirements.txt
```

2. Configure the MCP client to run:

```toml
[mcp_servers.abaqus]
command = 'python'
args = ['D:\path\to\Codex_MCP_Abaqus\src\mcp_server.py']
cwd = 'D:\path\to\Codex_MCP_Abaqus'

[mcp_servers.abaqus.env]
ABAQUS_MCP_HOME = 'D:\path\to\Codex_MCP_Abaqus'
```

3. Start Abaqus noGUI worker:

```powershell
set ABAQUS_MCP_HOME=D:\path\to\Codex_MCP_Abaqus
abaqus cae noGUI=D:\path\to\Codex_MCP_Abaqus\scripts\start_abaqus_mcp_loop.py
```

4. Check connection from the MCP client:

```text
mcp__abaqus.check_abaqus_connection
```

## Verified Example

The included cantilever example uses:

- Geometry: `100 mm x 10 mm x 10 mm`
- Material: linear elastic steel, `E = 210000 MPa`, `nu = 0.3`
- Element: `C3D8R`
- Boundary condition: fixed left end
- Load: vertical surface traction on the right end, equivalent total force
  `1000 N`

Typical result:

- Maximum displacement: about `2.037 mm`
- Maximum Mises stress: about `471 MPa`

## Notes

The plugin in this repository includes compatibility fixes for Abaqus 2022's
Python 2 kernel:

- Unicode-safe JSON and text writes
- Captured stdout/stderr for `execute_script`
- Stale heartbeat diagnostics in the MCP server

