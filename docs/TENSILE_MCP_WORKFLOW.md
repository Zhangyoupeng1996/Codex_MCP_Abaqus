# Classic Tensile MCP Workflow

This workflow records a simple end-to-end Abaqus MCP run:

1. Generate a classic 3D tensile bar model.
2. Submit the Abaqus/Standard job.
3. Read the ODB and write a numeric result summary.
4. Use Abaqus MCP to open/query the result database.
5. Show the ODB in a visible Abaqus/CAE viewport.

The example uses N-mm-MPa units.

## Model

- Geometry: `100 mm x 10 mm x 10 mm` rectangular bar
- Material: linear elastic steel, `E = 210000 MPa`, `nu = 0.3`
- Element: `C3D8R`
- Step: static tension
- Boundary condition: left end encastre
- Loading: right end prescribed displacement `U1 = 1 mm`
- Nominal engineering strain: `0.01`

## Run The Tensile Simulation

From the repository root:

```powershell
abaqus cae noGUI=examples\abaqus_tensile_bar_classic.py
```

By default, results are written to:

```text
examples\output\classic_tensile\
```

To choose a different output folder:

```powershell
$env:ABAQUS_TENSILE_WORK_DIR='D:\work\classic_tensile'
abaqus cae noGUI=examples\abaqus_tensile_bar_classic.py
```

The script creates:

- `classic_tensile_bar.cae`
- `classic_tensile_bar.inp`
- `classic_tensile_bar.odb`
- `result_summary.json`

Expected result scale:

- Engineering strain: about `0.01`
- Nominal stress: about `2100 MPa`
- Apparent modulus: about `210000 MPa`
- Average `S11`: about `2100 MPa`

## Start The Abaqus MCP Worker

Use the same repository folder for both the MCP server and Abaqus worker:

```powershell
$env:ABAQUS_MCP_HOME='D:\path\to\Codex_MCP_Abaqus'
abaqus cae noGUI=scripts\start_abaqus_mcp_loop.py
```

Then query the worker from Codex or another MCP client:

```text
mcp__abaqus.check_abaqus_connection
mcp__abaqus.ping
mcp__abaqus.get_odb_info(
  odb_path='D:\path\to\Codex_MCP_Abaqus\examples\output\classic_tensile\classic_tensile_bar.odb'
)
```

To set a noGUI Abaqus viewport to the tensile `S11` result through MCP, use
`mcp__abaqus.execute_script` with Abaqus Python similar to:

```python
from abaqus import session
from abaqusConstants import *
import visualization

odb_path = r'D:\path\to\classic_tensile_bar.odb'
odb = session.openOdb(name=odb_path, path=odb_path, readOnly=True)
vp = session.viewports['Viewport: 1']
vp.setValues(displayedObject=odb)
vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
vp.odbDisplay.setPrimaryVariable(
    variableLabel='S',
    outputPosition=INTEGRATION_POINT,
    refinement=(COMPONENT, 'S11'),
)
vp.view.setValues(session.views['Iso'])
vp.view.fitView()
```

In a noGUI worker, `get_viewport_image` may be unavailable depending on the
display environment. In that case, export from the Abaqus session:

```python
session.pngOptions.setValues(imageSize=(1400, 900))
session.printToFile(
    fileName=r'D:\path\to\tensile_s11_view',
    format=PNG,
    canvasObjects=(vp,),
)
```

## Show The Result In A Visible Abaqus Viewport

For direct visual inspection in Abaqus/CAE:

```powershell
abaqus cae startup=examples\show_tensile_result_viewport.py
```

If the result files are not in `examples\output\classic_tensile`, set the
paths explicitly:

```powershell
$env:ABAQUS_TENSILE_CAE='D:\work\classic_tensile\classic_tensile_bar.cae'
$env:ABAQUS_TENSILE_ODB='D:\work\classic_tensile\classic_tensile_bar.odb'
abaqus cae startup=examples\show_tensile_result_viewport.py
```

If another Abaqus worker is holding the `.cae` file open, the viewport script
continues with the `.odb` file and still displays the result contours.
