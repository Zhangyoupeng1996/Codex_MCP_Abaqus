# Usage Guide

## Directory Model

The Abaqus plugin and MCP server communicate through `ABAQUS_MCP_HOME`.

The directory contains:

- `commands/`: MCP server writes command JSON files here.
- `results/`: Abaqus plugin writes command results here.
- `scripts/`: temporary Abaqus Python scripts.
- `screenshots/`: optional viewport captures.
- `status.json`: plugin heartbeat.
- `stop.flag`: stop signal file.

Both sides must use the same `ABAQUS_MCP_HOME`.

## noGUI Worker

Recommended for production and long-running simulations:

```powershell
set ABAQUS_MCP_HOME=D:\path\to\Codex_MCP_Abaqus
abaqus cae noGUI=D:\path\to\Codex_MCP_Abaqus\scripts\start_abaqus_mcp_loop.py
```

Then call MCP tools from Codex:

```text
mcp__abaqus.check_abaqus_connection
mcp__abaqus.execute_script
mcp__abaqus.get_model_info
mcp__abaqus.list_jobs
```

## Abaqus GUI Mode

GUI mode is useful when you want to inspect the model or ODB visually.

1. In Abaqus/CAE, run:

```text
File -> Run Script...
```

Choose:

```text
src\abaqus_mcp_plugin.py
```

2. Start polling:

```text
Plug-ins -> MCP -> Start MCP (Cooperative)
```

Avoid `Background, Experimental` on Abaqus 2022 if it does not pass the
self-test. Cooperative mode can make the GUI less responsive because it polls
from the GUI thread.

3. Stop polling if the GUI becomes slow:

```powershell
echo stop > D:\path\to\Codex_MCP_Abaqus\stop.flag
```

or from the Abaqus kernel console:

```python
mcp_stop()
```

## Running the Classic Example Without MCP

You can also run the cantilever example directly:

```powershell
abaqus cae noGUI=D:\path\to\Codex_MCP_Abaqus\examples\abaqus_cantilever_classic.py
```

The script creates:

- `classic_cantilever_beam.cae`
- `classic_cantilever_beam.inp`
- `classic_cantilever_beam.odb`
- `result_summary.json`

You can run the tensile example directly:

```powershell
abaqus cae noGUI=D:\path\to\Codex_MCP_Abaqus\examples\abaqus_tensile_bar_classic.py
```

The script creates:

- `classic_tensile_bar.cae`
- `classic_tensile_bar.inp`
- `classic_tensile_bar.odb`
- `result_summary.json`

To display the tensile ODB in a visible Abaqus/CAE viewport:

```powershell
abaqus cae startup=D:\path\to\Codex_MCP_Abaqus\examples\show_tensile_result_viewport.py
```

See `docs\TENSILE_MCP_WORKFLOW.md` for the full MCP query and viewport display
workflow.

## Troubleshooting

If MCP reports `plugin not found`, check:

- Abaqus plugin has been loaded.
- `status.json` exists under `ABAQUS_MCP_HOME`.
- MCP server and Abaqus plugin use the same `ABAQUS_MCP_HOME`.

If MCP reports stale heartbeat:

- The worker is stopped, blocked, or pointing to an old process.
- Restart the noGUI worker, or stop GUI Cooperative mode and start it again.

If Abaqus GUI becomes sluggish:

- Stop MCP polling with `stop.flag`.
- Prefer noGUI worker for automated simulations.
