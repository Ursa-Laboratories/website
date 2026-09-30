#!/usr/bin/env python3
"""Render the Cub + ASMI build process (overview + one page per part) into docs/.

Usage: python3 scripts/build-cub-guide.py
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
FIG = "../assets/docs/cub-build"
GENMITSU_MANUAL = "https://www.manualslib.com/manual/3567589/Genmitsu-3018-Prover-V2.html"
CUBOS_REPO = "https://github.com/Ursa-Laboratories/CubOS"
UGS = "https://winder.github.io/ugs_website/download/"


def fig(*names, caption=""):
    imgs = "".join(
        f'<a href="{FIG}/{n}.jpg" target="_blank" rel="noopener"><img src="{FIG}/{n}.jpg" alt="{escape(caption)}" loading="lazy" /></a>'
        for n in names
    )
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="wiki-fig wiki-fig--{min(len(names), 3)}">{imgs}{cap}</figure>'


def note(text, kind="note"):
    label = {"note": "Note", "warn": "Caution", "tip": "Tip", "cub": "Cub change"}[kind]
    return f'<aside class="wiki-callout wiki-callout--{kind}"><strong>{label}</strong><p>{text}</p></aside>'


def code(text):
    return f"<pre><code>{escape(text)}</code></pre>"


PARTS = [
    {
        "slug": "cub-asmi-1-gantry",
        "letter": "A",
        "title": "Assemble the gantry",
        "time": "2 hours",
        "summary": "Build the Genmitsu 3018-PROVer V2 kit exactly as Genmitsu describes, except for the spindle, acrylic baffle and cable ties noted below.",
        "need": [
            "Genmitsu 3018-PROVer V2 kit (includes the Allen wrenches, Phillips wrench, screws, T-nuts, limit switches and wire pack)",
            "The Genmitsu 3018-PROVer V2 user manual that came in the box (<a href=\"%s\" target=\"_blank\" rel=\"noopener\">online copy</a>)" % GENMITSU_MANUAL,
        ],
        "intro": "The Genmitsu manual numbers its <em>Mechanical Installation</em> steps 1–12. Each step below matches the step with the same number, so you can keep the booklet open next to this page. The photos show what the finished step should look like on a Cub.",
        "steps": [
            ("Secure the XY-axis lead screw holder", "genmitsu 1",
             "<p>Turn the XY base assembly upside down and cut the shipping cable ties. Slide the aluminum platform until its holes line up with the lead screw holder, then fix the holder with the two M6 × 10 mm socket screws and the 5 mm Allen wrench.</p>"
             + fig("fig-00", caption="Lead screw holder fixed under the platform.")),
            ("Install the rubber feet", "genmitsu 2",
             "<p>Screw the four rubber feet into the corners of the base with the 3 mm Allen wrench.</p>" + fig("fig-01", caption="One of the four feet installed.")),
            ("Install the Y-axis limit switches", "genmitsu 3",
             "<p>Mount one limit switch on the front module and one on the rear module, two M3 × 8 mm round-head screws each.</p>"
             + note("Genmitsu says to use the 3 mm Allen wrench here. Use the included Phillips wrench instead.", "cub")
             + fig("fig-02", "fig-03", caption="Front and rear Y limit switches.")),
            ("Wire the Y-axis limit switches", "genmitsu 4",
             "<p>Take the 410 mm and 430 mm Y-limit cables from the wire pack. Plug the 6-wire connector into the rear switch and the longer 3-wire connector into the front switch. Leave the short free end loose for now; it plugs into the control board in step 11. Tie the cable at the tie points and press it into the profile slot with the 270 mm profile seal.</p>"
             + fig("fig-04", "fig-05", "fig-06", caption="Y-limit cable, then routed into the profile slot.")),
            ("Install the X-axis limit switches", "genmitsu 5",
             "<p>On the motor-side X plate, mount a switch using the two M3 × 7 mm PCB standoffs and M3 × 14 mm screws. On the opposite plate, mount the second switch directly with two M3 × 8 mm screws (no standoffs on that side).</p>"
             + fig("fig-07", "fig-08", caption="Motor-side and opposite-side X limit switches.")),
            ("Install the E-stop switch", "genmitsu 6",
             "<p>Unscrew the black plastic nut and square gasket from the E-stop. Push the wire through the hole in the X plate from the outside, then refit the square gasket and black nut from the inside and tighten.</p>"
             + note("Put the iron square gasket and black nut back in the same orientation they came in.", "cub")
             + fig("fig-09", caption="E-stop fitted through the X plate.")),
            ("Wire the X-axis limit switches", "genmitsu 7",
             "<p>Take the 415 mm and 170 mm X-limit cables. Plug the 6-wire connector into the switch on the motor-side plate and the 3-wire connector into the switch on the other plate. Press the cable into the profile slot with the 340 mm profile seal.</p>"
             + note("Genmitsu calls for cable ties at this step. Skip them; they aren't needed yet.", "cub")
             + fig("fig-10", "fig-11", "fig-12", caption="X-limit cable and both switches connected.")),
            ("Install the control board", "genmitsu 8",
             "<p>Thread four M3 T-nuts one turn onto four M3 × 8 mm screws through the control board's mounting points. Turn the T-nuts flat, slide them into the profile channel, and tighten all four screws with the Phillips wrench.</p>"
             + note("Check every T-nut has rotated and seated in the channel after tightening. A loose board will shift when the gantry moves.", "cub")
             + fig("fig-13", caption="Control board mounted on the XZ frame.")),
            ("Install the XZ-axis assembly", "genmitsu 9",
             "<p>Stand the XZ assembly on the XY base and fix it with the eight M5 × 22 mm round-head screws (four each side) using the 3 mm Allen wrench.</p>"
             + fig("fig-14", "fig-15", caption="Both sides of the XZ assembly bolted to the base.")),
            ("Skip: spindle", "genmitsu 10",
             "<p>The Cub doesn't use the spindle. Leave the spindle, collet and 13/17 mm wrenches in the box.</p>"),
            ("Wire the control board", "genmitsu 11",
             "<p>Follow Genmitsu's control board diagram: X, Y and Z motor cables to their motor ports; X, Y and Z limit cables to their limit ports; E-stop to the E-stop port. Tidy the wires with the cable wrap and ties.</p>"
             + note("Skip the spindle wiring (the red/black M+ M− pair). Nothing is plugged into the spindle port.", "cub")
             + fig("fig-16", caption="Finished Cub gantry, wired without a spindle.")),
            ("Skip: acrylic baffle", "genmitsu 12",
             "<p>The acrylic side baffles aren't used on the Cub. Stop here in the Genmitsu booklet; its software chapters (Candle, probing) don't apply.</p>"),
        ],
        "done": [
            "All four motors, three limit switches and the E-stop are plugged into the control board.",
            "Nothing is connected to the spindle port.",
            "Each axis turns smoothly by hand (with power off) over its full travel.",
        ],
    },
    {
        "slug": "cub-asmi-2-sensor-mount",
        "letter": "B",
        "title": "Mount the ASMI force sensor",
        "time": "45 minutes",
        "summary": "Clamp the Vernier force sensor in its printed mount and fit it to the gantry's Z axis. This is the ASMI's indenting head.",
        "need": [
            "Vernier Go Direct Force and Acceleration Sensor and its cable (<a href=\"https://www.vernier.com/product/go-direct-force-and-acceleration-sensor/\" target=\"_blank\" rel=\"noopener\">Vernier</a>)",
            "A 3 mm or 5 mm ball indenter",
            "Printed parts: Cub Vernier Go Direct mount base and cover, and the Cub 3018 mount (STEP files in <a href=\"https://github.com/Ursa-Laboratories/Cubware/tree/main/cub/instrument_mounts\" target=\"_blank\" rel=\"noopener\">Cubware</a>, preview in the <a href=\"../build.html#build-cad\">CAD viewer</a>)",
            "2× M5 × 15 mm button-head screws and 2× M5 hex nuts",
            "3 mm Allen wrench (from the Genmitsu kit)",
        ],
        "intro": "The mount has three printed parts: a base that holds the sensor, a cover that closes over it, and the Cub 3018 mount that slides into the gantry's round Z-axis clamp (where the spindle would go).",
        "steps": [
            ("Print the parts", "",
             "<p>Print the base, cover and Cub 3018 mount in PLA. Default settings work; the only change is to turn supports on for the overhangs (tree supports, Tree Slim style, 30° threshold). Our reference prints used a Bambu Lab X1-Carbon with Bambu PLA Basic.</p>"
             + fig("sensor-000", "sensor-002", caption="Assembled mount, and the support settings used.")),
            ("Seat the sensor in the base", "",
             "<p>Set the Vernier sensor into the rectangular opening in the base, oriented as shown.</p>"
             + fig("sensor-005", caption="Sensor seated in the base.")),
            ("Fit the cover", "",
             "<p>Place the cover over the sensor and base.</p>" + fig("sensor-006", caption="Cover in place.")),
            ("Clamp the sensor", "",
             "<p>Push the two M5 × 15 mm screws through the two holes above the sensor. Drop the two M5 nuts into the hex pockets on the back, then tighten the screws with the 3 mm Allen wrench until the mount is snug and clamps the sensor.</p>"
             + fig("sensor-003", "sensor-004", "sensor-007", caption="M5 × 15 mm screw, M5 nut, and both screws tightened.")),
            ("Fit the indenter", "",
             "<p>Screw the 3 mm or 5 mm ball indenter into the sensor's threaded tip, whichever your test calls for. Finger-tight is enough.</p>"),
            ("Attach the Cub 3018 mount", "",
             "<p>Line up the dovetail on the back of the base with the dovetail slot on the Cub 3018 mount and slide them together.</p>"
             + fig("sensor-008", "sensor-009", caption="Dovetail engaged, from the back and the side.")),
            ("Install on the gantry", "",
             "<p>Slide the Cub 3018 mount into the round clamp on the Z axis, pushing it in as far as it will go. Tighten the clamp screw with the 3 mm Allen wrench, then plug the sensor cable into the side of the sensor.</p>"
             + note("Route the sensor cable so it has slack when the head moves to every corner and to the top of Z. A taut cable can pull the reading off.", "tip")
             + fig("sensor-010", caption="Sensor mount installed in the Z-axis clamp.")),
        ],
        "done": [
            "The sensor doesn't shift in the mount when you press on the indenter.",
            "The mount is pushed fully into the Z clamp and the clamp screw is tight.",
            "The sensor cable is plugged in and has slack across the whole travel.",
        ],
    },
    {
        "slug": "cub-asmi-3-bring-up",
        "letter": "C",
        "title": "Bring up the gantry",
        "time": "30 minutes",
        "summary": "Set the controller's firmware so the machine homes to the back-right-top corner and every axis moves the right way. CubOS relies on this and never flips axes in software.",
        "need": [
            "The assembled gantry, its 24 V power supply and the USB A-to-B cable",
            "A computer with <a href=\"%s\" target=\"_blank\" rel=\"noopener\">Universal Gcode Sender (UGS)</a> installed" % UGS,
            "A clear deck (remove plates and anything the indenter could hit)",
        ],
        "intro": "You'll talk to the controller directly with UGS in this part, not with CubOS. The controller runs GRBL; you change it by typing short <code>$</code> commands into the UGS console. Write down every setting before you change it so you can put it back.",
        "steps": [
            ("Connect with UGS", "",
             "<ol><li>Plug in the gantry's power and USB, and switch it on.</li>"
             "<li>Open UGS. Pick the port (on a Mac it looks like <code>/dev/tty.usbserial-…</code>, on Windows <code>COM3</code> or similar; unplug the USB to see which one disappears). Set the baud rate to <strong>115200</strong> and click <strong>Connect</strong>.</li></ol>"
             + note("If every reply says <code>Estop is activated</code>, twist the red E-stop button to release it.", "tip")),
            ("Record the current settings", "",
             "<p>Type <code>$$</code> and press Enter. Copy the full list into a text file and keep it. The settings this part changes are:</p>"
             "<div class=\"doc-table-wrap\"><table><thead><tr><th>Setting</th><th>What it does</th></tr></thead><tbody>"
             "<tr><td>$3</td><td>Reverses the direction of individual axes</td></tr>"
             "<tr><td>$10</td><td>What the status line reports; 0 = work position (WPos)</td></tr>"
             "<tr><td>$20</td><td>Soft limits (refuse moves outside the travel)</td></tr>"
             "<tr><td>$21</td><td>Hard limits (stop when a limit switch is hit)</td></tr>"
             "<tr><td>$22</td><td>Homing enabled</td></tr>"
             "<tr><td>$23</td><td>Which way each axis looks for its limit switch when homing</td></tr>"
             "<tr><td>$27</td><td>How far the head backs off a switch after homing (mm)</td></tr>"
             "</tbody></table></div>"),
            ("Turn on hard limits and homing", "",
             code("$21=1\n$22=1\n$10=0") +
             "<p>Then type <code>?</code>. The status line should include <code>WPos:</code>. If it shows <code>MPos:</code>, <code>$10=0</code> didn't take; send it again.</p>"),
            ("Check each axis moves the right way", "",
             "<p>Stand at the front of the machine. Using the UGS jog buttons with a small step (1–5 mm), jog one axis at a time and watch which way the head moves:</p>"
             "<ul><li><strong>+X</strong> moves the head to the <strong>right</strong>.</li>"
             "<li><strong>+Y</strong> moves the head (or the bed's work point) <strong>away from you</strong>, toward the back.</li>"
             "<li><strong>+Z</strong> moves the head <strong>up</strong>.</li></ul>"
             "<p>If an axis goes the wrong way, reverse it with <code>$3</code>. Add up the numbers for every axis that needs reversing: X = 1, Y = 2, Z = 4. For example, reversing only Y is <code>$3=2</code>; reversing X and Y is <code>$3=3</code>. Re-test after each change.</p>"
             + note("Keep a hand near the E-stop while jogging. If the head runs toward the frame, press it.", "warn")),
            ("Home to the back-right-top corner", "",
             "<p>Type <code>$H</code>. The machine should lift Z first, then move X and Y until it touches the switches at the <strong>back-right</strong> corner with the head at the top.</p>"
             "<p>If an axis heads the wrong way (away from its switch, or into the frame), press the E-stop, then flip that axis in <code>$23</code> using the same numbers (X = 1, Y = 2, Z = 4). Release the E-stop, send <code>$X</code> to unlock, and run <code>$H</code> again. Repeat until homing finishes cleanly every time.</p>"
             + note("If the head stops on a switch and won't move, send <code>$X</code> and jog it a few millimetres away from the switch.", "tip")),
            ("Set the pull-off and turn on soft limits", "",
             "<p>Once homing works, set a small pull-off so the switches release after homing, then enable soft limits:</p>"
             + code("$27=2\n$20=1") +
             "<p>Run <code>$H</code> once more to confirm. Save the final <code>$$</code> output next to the original. CubOS checks these values every time it connects and warns you if they change.</p>"),
            ("Close UGS", "",
             "<p>Click <strong>Disconnect</strong> and quit UGS. Only one program can use the USB port at a time, and CubOS needs it next.</p>"),
        ],
        "done": [
            "<code>?</code> reports <code>WPos:</code>.",
            "<code>$H</code> reliably finishes at the back-right-top corner.",
            "+X moves right, +Y moves toward the back, +Z moves up.",
            "Soft limits (<code>$20=1</code>) and hard limits (<code>$21=1</code>) are on.",
        ],
    },
    {
        "slug": "cub-asmi-4-install-cubos",
        "letter": "D",
        "title": "Install CubOS",
        "time": "15 minutes",
        "summary": "Install CubOS, the software that runs the gantry and the force sensor, and open its Operator window.",
        "need": [
            "A Mac or a Windows PC with the gantry's USB cable plugged in",
            "Mac only: an internet connection and about 1 GB of disk space",
        ],
        "intro": "Choose the path for your computer. Both end with the CubOS Operator open, showing the <strong>Workflow</strong>, <strong>Visualize</strong>, <strong>State</strong> and <strong>Results</strong> tabs.",
        "steps": [
            ("Windows: run the installer", "",
             "<ol><li>Go to the <a href=\"%s/releases/latest\" target=\"_blank\" rel=\"noopener\">latest CubOS release</a> and download <code>CubOS-Setup-….exe</code> under <strong>Assets</strong>.</li>"
             "<li>Run it. It doesn't need administrator rights, Python or Git.</li>"
             "<li>Open <strong>CubOS</strong> from the Start menu or desktop shortcut. The Operator opens in its own window.</li></ol>"
             "<p>Your configuration files live in <code>%%LOCALAPPDATA%%\\UrsaLabs\\CubOS\\configs</code>.</p>" % CUBOS_REPO),
            ("Mac: install the tools", "",
             "<p>If you don't have <a href=\"https://brew.sh\" target=\"_blank\" rel=\"noopener\">Homebrew</a>, install it first. Then, in Terminal:</p>"
             + code("brew install python@3.11 git node")),
            ("Mac: download and install CubOS", "",
             code(f"git clone {CUBOS_REPO}.git\ncd CubOS\npython3.11 -m venv .venv\nsource .venv/bin/activate\npython -m pip install --upgrade pip\npython -m pip install -e \"packages/core[dev,asmi-vernier]\"\npython -m pip install -e services/api")
             + "<p><code>asmi-vernier</code> adds the driver for the Vernier force sensor.</p>"),
            ("Mac: build the Operator screen", "",
             "<p>This only needs doing once (and again after updating CubOS):</p>"
             + code("cd apps/operator-web && npm ci && npm run build && cd ../..")),
            ("Mac: start CubOS", "",
             code("source .venv/bin/activate\npython -m cubos_api")
             + "<p>Open <a href=\"http://127.0.0.1:8742\">http://127.0.0.1:8742</a> in your browser. Leave the Terminal window open while you use CubOS.</p>"
             + note("<code>No module named cubos_api</code> means the <code>source .venv/bin/activate</code> line was skipped. A page saying compiled web assets weren't found means the build step above didn't run.", "tip")),
        ],
        "done": [
            "The CubOS Operator is open with the Workflow, Visualize, State and Results tabs.",
            "UGS is closed, so CubOS can use the USB port.",
        ],
    },
    {
        "slug": "cub-asmi-5-calibrate",
        "letter": "E",
        "title": "Calibrate the gantry",
        "time": "15 minutes",
        "summary": "Teach CubOS where the deck is and how far each axis can travel, using a printed calibration block and the indenter tip.",
        "need": [
            "Printed Cub calibration block and Cub calibration base (<a href=\"cub-calibration.html\">print and mounting guide</a>)",
            "Calipers to measure the block height",
            "The CubOS Operator from part D",
        ],
        "intro": "Calibration sets the deck's zero point, the indenter's height, and the machine's real travel, and saves them to your gantry file. Redo it after a crash or any mechanical change.",
        "steps": [
            ("Place the calibration block", "",
             "<p>Seat the calibration base's two pegs in two holes near a corner of the baseplate, then set the block on the base so its four diamond-shaped feet drop into the matching holes. Measure the block's height with calipers.</p>"
             + note("The wizard tells you which corner it expects (front-left on a default setup). Put the block there.", "tip")),
            ("Load the Cub gantry file and connect", "",
             "<ol><li>In the <strong>Workflow</strong> tab, open <strong>Gantry</strong> and choose your Cub ASMI gantry file.</li>"
             "<li>Click <strong>Connect</strong> in the Gantry Control panel. The status dot turns green when the USB link is up. CubOS never moves on its own when it connects.</li></ol>"
             + note("If CubOS reports a GRBL settings mismatch, the controller doesn't match what part C set. Go back and check <code>$3</code>, <code>$20</code>, <code>$22</code> and <code>$23</code>.", "warn")),
            ("Run the calibration wizard", "",
             "<p>Click <strong>Calibrate</strong>. For a single-instrument Cub the wizard has five steps:</p>"
             "<ol><li><strong>Prepare</strong> — optionally enter a new output file name to keep the original file untouched.</li>"
             "<li><strong>Home</strong> — click <strong>Home gantry</strong>.</li>"
             "<li><strong>Reference height</strong> — enter the block height you measured.</li>"
             "<li><strong>Set origin</strong> — jog the indenter over the block and down until the ball just touches the block's top surface. Switch to 0.1 mm steps for the last few millimetres.</li>"
             "<li><strong>Save</strong> — clear the deck. The gantry re-homes, measures its travel and writes the gantry file.</li></ol>"
             + note("Jog down slowly near the block. The force sensor is the instrument you're protecting.", "warn")),
            ("Check the result", "",
             "<p>Jog a few millimetres in each direction from the Operator. +X should move right, +Y toward the back, +Z up, and the position readout should match what you see.</p>"),
        ],
        "done": [
            "The wizard's Save step finished without errors.",
            "Jogging from the Operator moves the right way on every axis.",
        ],
    },
    {
        "slug": "cub-asmi-6-labware",
        "letter": "F",
        "title": "Calibrate labware",
        "time": "5 minutes per plate",
        "summary": "Record exactly where your 96-well plate sits so the indenter lands in the centre of every well.",
        "need": [
            "A 96-well plate, seated firmly in its holder on the deck",
            "A calibrated gantry (part E)",
        ],
        "intro": "You'll touch the indenter to two wells, A1 and A2. CubOS works out every other well from those two points and the plate's well spacing.",
        "steps": [
            ("Open the labware calibration dialog", "",
             "<p>In the <strong>Workflow</strong> tab, open <strong>Deck</strong>, pick your deck file and click <strong>Calibrate labware</strong>.</p>"),
            ("Select the plate", "",
             "<p>Choose <strong>Well plate</strong>, then pick an existing plate or click <strong>Add new</strong> and start from the 96-well SBS template. Give it a name, set the reference instrument to the ASMI indenter, leave <strong>Calibrate with a tip attached</strong> unticked, and click <strong>Continue</strong>.</p>"
             + note("For a plate that isn't in the templates, create it with <strong>New Labware</strong> first and enter its rows, columns and well spacing.", "tip")),
            ("Record A1 and A2", "",
             "<ol><li>Jog the indenter over well <strong>A1</strong>, centre it, and lower it until it's just at the top of the well. Click <strong>Record</strong>.</li>"
             "<li>Jog one well along the row to <strong>A2</strong> and click <strong>Record</strong>. CubOS snaps A2 to exactly one well spacing (9 mm on a 96-well plate) in the direction you moved.</li></ol>"),
            ("Review and save", "",
             "<p>Check the positions on the review screen and click <strong>Save labware calibration</strong>. It's written to your deck file straight away.</p>"),
            ("Check a well", "",
             "<p>Use <strong>Move To</strong> on A1 and a far well such as H12. The indenter should sit over the centre of each one. If it doesn't, the plate has probably moved in its holder; reseat it and redo this part.</p>"),
        ],
        "done": [
            "Move To A1 and H12 both land in the centre of the well.",
            "Your Cub is ready to run an ASMI indentation protocol.",
        ],
    },
]


BOM = [
    # (item, qty, cost shown, cost counted in total, where, used in part)
    ("Genmitsu 3018-PROVer V2 CNC router kit", "1", "$269", 269, "SainSmart / Amazon", "A"),
    ("Vernier Go Direct Force and Acceleration Sensor (GDX-FOR), includes USB cable", "1", "$124", 124,
     '<a href="https://www.vernier.com/product/go-direct-force-and-acceleration-sensor/" target="_blank" rel="noopener">Vernier</a>', "B"),
    ("Ball indenter, 3 mm or 5 mm", "1", "Ask us", 0, "Ursa Labs", "B"),
    ("PLA filament: sensor mount base and cover, Cub 3018 mount, calibration block and base", "~100 g", "$5", 5,
     'Any PLA; files in <a href="https://github.com/Ursa-Laboratories/Cubware" target="_blank" rel="noopener">Cubware</a>', "B, E"),
    ("M5 × 15 mm stainless button-head screws", "2", "~$10 for both packs", 10, "Hardware store or McMaster-Carr", "B"),
    ("M5 hex nuts", "2", "", 0, "Hardware store or McMaster-Carr", "B"),
    ("96-well plate (SBS format)", "1", "Consumable", 0, "Any lab supplier", "F"),
]
PI = ("Raspberry Pi 5 with power supply, SD card and case", "~$150", 150, "Raspberry Pi reseller",
      "Runs CubOS on the machine itself, so no lab computer is tied up")


def bom_table():
    total = sum(row[3] for row in BOM)
    rows = "".join(f"<tr><td>{i}</td><td>{q}</td><td>{c}</td><td>{w}</td><td>{p}</td></tr>" for i, q, c, _, w, p in BOM)
    pi_item, pi_cost, pi_value, pi_where, pi_why = PI
    return (
        '<h2 id="bom">Bill of materials</h2>'
        f'<p>One Cub + ASMI comes to about <strong>${total:,}</strong>, plus the ball indenter and plates. Prices are USD list prices as of September 2026.</p>'
        '<div class="doc-table-wrap wiki-bom"><table><thead><tr><th>Item</th><th>Qty</th><th>Cost</th><th>Where</th><th>Part</th></tr></thead><tbody>'
        f'{rows}<tr class="wiki-bom-total"><td>Total</td><td></td><td><strong>${total:,}</strong></td><td></td><td></td></tr></tbody></table></div>'
        '<h3>Optional</h3><div class="doc-table-wrap wiki-bom"><table><thead><tr><th>Item</th><th>Cost</th><th>Where</th><th>Why</th></tr></thead><tbody>'
        f'<tr><td>{pi_item}</td><td>{pi_cost}</td><td>{pi_where}</td><td>{pi_why}</td></tr></tbody></table></div>'
        f'<p>Without the Pi, CubOS runs on your own Mac or Windows computer (part D). With the Pi, the total is about <strong>${total + pi_value:,}</strong>.</p>'
    )


HEADER = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{description}" />
    <title>{title} | Ursa Laboratories</title>
    <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg" />
    <link rel="stylesheet" href="../styles.css" />
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CFM3B0DT2P"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-CFM3B0DT2P');
    </script>
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="../index.html" aria-label="Ursa Laboratories — home">
        <img class="brand-mark" src="../assets/favicon.svg" alt="" aria-hidden="true" />
        <span>Ursa Labs</span>
      </a>
      <nav class="site-nav" aria-label="Primary">
        <a href="../index.html#instruments">Instruments</a>
        <a href="../index.html#compare">Hardware</a>
        <a href="../index.html#software">Software</a>
        <a href="../build.html" aria-current="page">Build It</a>
        <a href="https://github.com/Hydra-Laboratories/CubOS" target="_blank" rel="noopener">GitHub</a>
      </nav>
      <a class="btn btn-primary btn-nav" href="../index.html#airtable">Get in touch</a>
    </header>
    <main id="top">
      <article class="section build doc wiki" aria-labelledby="doc-title">
        <nav class="doc-breadcrumb" aria-label="Breadcrumb"><a href="../build.html">Build It</a><span aria-hidden="true">/</span><a href="../build.html#build-process">Build process</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
"""

FOOTER = """      </article>
    </main>
    <footer class="site-footer">
      <p>Ursa Laboratories — self-driving laboratories for autonomous materials discovery.</p>
      <nav class="site-footer-links" aria-label="Footer">
        <a href="https://github.com/Hydra-Laboratories/CubOS" target="_blank" rel="noopener">GitHub</a>
        <a href="../build.html">Build It</a>
        <a href="../index.html#airtable">Contact</a>
      </nav>
      <p class="site-footer-copyright">&copy; 2026 Ursa Labs. All rights reserved.</p>
    </footer>
  </body>
</html>
"""


def sidebar(current):
    cur = ' aria-current="page"'
    items = [f'<li><a href="cub-asmi-build.html"{cur if current is None else ""}>Overview</a></li>']
    for p in PARTS:
        here = current is p
        sub = ""
        if here:
            sub = "<ol>" + "".join(f'<li><a href="#step-{i}">{escape(s[0])}</a></li>' for i, s in enumerate(p["steps"], 1)) + '<li><a href="#done">Check your work</a></li></ol>'
        items.append(
            f'<li class="{"is-current" if here else ""}"><a href="{p["slug"]}.html"{cur if here else ""}>'
            f'<span class="wiki-nav-letter">{p["letter"]}</span>{escape(p["title"])}<span class="wiki-nav-time">{p["time"]}</span></a>{sub}</li>'
        )
    return f'<aside class="doc-toc wiki-nav" aria-label="Build process"><p class="cad-group-label">Cub + ASMI build</p><ol>{"".join(items)}</ol></aside>'


def pager(idx):
    prev = ("cub-asmi-build.html", "Overview") if idx == 0 else (PARTS[idx - 1]["slug"] + ".html", f'Part {PARTS[idx - 1]["letter"]} · {PARTS[idx - 1]["title"]}')
    nxt = (PARTS[idx + 1]["slug"] + ".html", f'Part {PARTS[idx + 1]["letter"]} · {PARTS[idx + 1]["title"]}') if idx + 1 < len(PARTS) else ("../build.html#guide-library", "Browse all guides")
    return (f'<nav class="wiki-pager" aria-label="Part navigation"><a href="{prev[0]}"><span>&larr; Previous</span>{escape(prev[1])}</a>'
            f'<a class="wiki-pager-next" href="{nxt[0]}"><span>Next &rarr;</span>{escape(nxt[1])}</a></nav>')


def render_part(idx, p):
    steps = []
    for i, (title, ref, body) in enumerate(p["steps"], 1):
        tag = f'<span class="wiki-step-ref">Genmitsu step {ref.split()[1]}</span>' if ref else ""
        steps.append(f'<section class="wiki-step" id="step-{i}"><h3><span class="wiki-step-num">{i}</span>{escape(title)}{tag}</h3>{body}</section>')
    need = "".join(f"<li>{n}</li>" for n in p["need"])
    done = "".join(f"<li>{d}</li>" for d in p["done"])
    body = (
        f'<div class="section-heading narrow"><p class="eyebrow">Part {p["letter"]} of {len(PARTS)} · Cub + ASMI</p>'
        f'<h1 id="doc-title">{escape(p["title"])}</h1><p>{p["summary"]}</p>'
        f'<p class="wiki-meta"><span>&#9201; {p["time"]}</span><span>Genmitsu 3018-PROVer V2</span></p></div>'
        f'<div class="doc-layout">{sidebar(p)}<div class="doc-body">'
        f'<div class="wiki-need"><h2>What you need</h2><ul>{need}</ul></div>'
        f'<p>{p["intro"]}</p><h2>Steps</h2>{"".join(steps)}'
        f'<div class="wiki-done" id="done"><h2>Check your work</h2><ul>{done}</ul></div>'
        f'{pager(idx)}</div></div>'
    )
    head = HEADER.format(title=f'Part {p["letter"]}: {p["title"]} · Cub + ASMI build', description=p["summary"].replace('"', "&quot;"), crumb=f'Part {p["letter"]}')
    (OUT / f'{p["slug"]}.html').write_text(head + body + FOOTER)


def render_overview():
    cards = "".join(
        f'<li><a href="{p["slug"]}.html"><span class="wiki-nav-letter">{p["letter"]}</span><strong>{escape(p["title"])}</strong>'
        f'<span class="wiki-card-time">{p["time"]}</span><span class="wiki-card-sum">{p["summary"]}</span></a></li>'
        for p in PARTS
    )
    body = (
        '<div class="section-heading narrow"><p class="eyebrow">Build process · Cub + ASMI</p>'
        '<h1 id="doc-title">Build a Cub with the ASMI indenter</h1>'
        '<p>Turn a Genmitsu 3018-PROVer V2 into an automated indentation tester that measures the mechanical properties of samples in a 96-well plate. Work through the six parts in order; each ends with a short check so you know it worked before moving on.</p>'
        '<p class="wiki-meta"><span>&#9201; About 4 hours total</span><span>No soldering</span><span>Mac or Windows</span></p></div>'
        f'<div class="doc-layout">{sidebar(None)}<div class="doc-body">'
        f'<h2>The six parts</h2><ol class="wiki-cards">{cards}</ol>'
        + bom_table()
        + '<h2>What else you need</h2>'
        '<h3>Tools</h3><ul><li>A Mac or Windows computer</li><li>The Allen wrenches and Phillips wrench included with the Genmitsu kit</li><li>Calipers</li><li>A 3D printer, if you\'re printing the mounts yourself</li></ul>'
        '<h3>Software</h3><ul><li><a href="%s" target="_blank" rel="noopener">Universal Gcode Sender</a> (part C only)</li><li><a href="%s" target="_blank" rel="noopener">CubOS</a> (part D)</li></ul>' % (UGS, CUBOS_REPO)
        + note("Never leave the gantry running unattended during bring-up or calibration, and keep the E-stop within reach whenever it's powered.", "warn")
        + pager_overview() + "</div></div>"
    )
    head = HEADER.format(title="Cub + ASMI build process", description="Step-by-step build of a Cub (Genmitsu 3018-PROVer V2) with the ASMI indenter: assembly, bring-up, CubOS install and calibration.", crumb="Cub + ASMI")
    (OUT / "cub-asmi-build.html").write_text(head + body + FOOTER)


def pager_overview():
    p = PARTS[0]
    return f'<nav class="wiki-pager" aria-label="Part navigation"><span></span><a class="wiki-pager-next" href="{p["slug"]}.html"><span>Start &rarr;</span>Part {p["letter"]} · {escape(p["title"])}</a></nav>'


if __name__ == "__main__":
    render_overview()
    for i, part in enumerate(PARTS):
        render_part(i, part)
    print(f"wrote {len(PARTS) + 1} pages to {OUT}")
