# KABLab guide sources

Retrieved from the shared KABLab Google Drive folder on 2026-09-22:
https://drive.google.com/drive/folders/1pFNT8T6PBa1txT4gyd08siEE_fo5O8YJ

`sources.json` records source document URLs and modification dates. `pages.json`
maps each source to local JPEG pages rendered from its PDF export at 1500 px wide.
The website provides an accessible HTML reading path alongside these illustrated
source pages. Click any page to view it at full size. Original Google Docs remain
linked for the latest editable source. Local images are a dated snapshot.

## Coverage

- Instructions/Cub: full and shipped-kit gantry manuals, Vernier mount, calibration.
- Instructions/CubXL: Vernier mount, ASMI wellplate holder, Hamilton heater/cooler
  holder, calibration. The top-level Rev. 2 manual supplies gantry assembly.
- Instructions/CubXL+: calibration; the top-level PANDA Rev. 0 manual is retained
  as an explicitly legacy gantry/mount reference, not a new revision.
- Instructions/CubXL_2.0: separate 4040-PRO MAX assembly guide.
- Existing Cubware-derived pipette and capper guides are preserved.
- The PANDA parts spreadsheet is linked from the build page; it is a kit inventory,
  not a priced purchasing BOM.

## Source gaps and editorial choices

- Older top-level CubXL Rev. 1 and the recipient-specific Rev. 2 copy are not used
  in place of the current top-level Rev. 2 manual.
- `Cub - Enclosure Document` is a list of ideas/vendor links, not an assembly guide.
- `Opentrons Pipette Wiring Instructions_REV. 0` actually contains gantry assembly
  steps, so it is not presented as a pipette wiring guide.
- The separate `Opentrons Pipette Wiring Schematic` contains a `120V/2A` supply
  label alongside a `12V DC` connector. Its source-page export is retained in this
  inventory for review, but is not promoted into the working pipette instructions.
- To Do List and Picture Formatting are not build guides.
- Cub gantry manuals contain isolated 4040-PRO MAX references despite identifying
  the kit as 3018-PROVer V2. HTML uses the kit model stated by the manual; original
  page images preserve the source wording for comparison.
- CubXL_2.0 skips wiring because its documented kit ships prewired; this does not
  establish a complete sensor/deck build on that platform.
- The CubXL software section describes a prepared appliance; its specific setup
  SSID is an example, not a universal machine identifier.

No physical build, motion, electrical validation, or live deployment was performed.
