# universal_grip_cuff.py
# Fusion 360 script by Carlos Ortega (FSU Biomedical Engineering).
# Builds a universal grip cuff in sizes S/M/L plus two quick-swap tool adapters,
# then exports .f3d, .step and .stl to Downloads/universal-grip-cuff.
#
# Run: Utilities > Add-Ins > Scripts and Add-Ins > + > pick this file > Run.
# To change fit: edit SIZES or P below, then run again.

import adsk.core, adsk.fusion, traceback, os

# ---- Hand sizes (mm) ----
SIZES = {
    'S': {'palmWidth': 70, 'palmDepth': 26, 'thumbGap': 22},
    'M': {'palmWidth': 80, 'palmDepth': 30, 'thumbGap': 26},
    'L': {'palmWidth': 90, 'palmDepth': 34, 'thumbGap': 30},
}
BUILD = ['S', 'M', 'L']

# ---- Shared parameters (mm) ----
P = {
    'clearance': 2.0,     # room for skin, swelling or a thin foam liner
    'wall': 3.0,          # cuff wall thickness
    'cuffHeight': 35.0,   # band height along the fingers
    'socketSize': 12.0,   # square shank size on adapters
    'socketDepth': 26.0,  # socket depth in the cuff boss
    'fitTol': 0.4,        # socket clearance over shank
    'pinDia': 3.2,        # cross pin hole (M3 bolt or 3 mm pin)
    'headSize': 22.0,     # adapter head square size
    'headLen': 24.0,      # adapter head length
    'flatSlotW': 4.5,     # flat handle slot thickness (fork, spoon, toothbrush)
    'flatSlotH': 15.0,    # flat handle slot width
    'roundBore': 11.0,    # round bore (pen, pencil, marker)
    'setScrewDia': 2.5,   # pilot hole for an M3 self-tapping set screw
}

EXPORT = True
OUT_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'universal-grip-cuff')

FO = adsk.fusion.FeatureOperations
NEW = FO.NewBodyFeatureOperation
JOIN = FO.JoinFeatureOperation
CUT = FO.CutFeatureOperation
POS = adsk.fusion.ExtentDirections.PositiveExtentDirection
NEG = adsk.fusion.ExtentDirections.NegativeExtentDirection


def cm(mm):
    return mm / 10.0


def P3(x, y, z):
    return adsk.core.Point3D.create(cm(x), cm(y), cm(z))


def to_sketch(sk, xyz):
    p = sk.modelToSketchSpace(P3(*xyz))
    p.z = 0
    return p


def rect_on(sk, p1, p2):
    sk.sketchCurves.sketchLines.addTwoPointRectangle(to_sketch(sk, p1), to_sketch(sk, p2))


def circle_on(sk, c, dia):
    sk.sketchCurves.sketchCircles.addByCenterRadius(to_sketch(sk, c), cm(dia) / 2.0)


def offset_plane(comp, base, dist_mm):
    pi = comp.constructionPlanes.createInput()
    pi.setByOffset(base, adsk.core.ValueInput.createByReal(cm(dist_mm)))
    return comp.constructionPlanes.add(pi)


def extrude(comp, prof, dist_mm, op, direction=POS, bodies=None, through_all=False):
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(prof, op)
    if through_all:
        extent = adsk.fusion.ThroughAllExtentDefinition.create()
    else:
        extent = adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByReal(cm(dist_mm)))
    inp.setOneSideExtent(extent, direction)
    if bodies is not None:
        inp.participantBodies = bodies
    return ext.add(inp)


def build_cuff(root, size, palmWidth, palmDepth, thumbGap):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'Cuff_' + size

    h, w, c = P['cuffHeight'], P['wall'], P['clearance']
    a_in, b_in = palmWidth / 2.0 + c, palmDepth / 2.0 + c
    a_out, b_out = a_in + w, b_in + w
    s, sd = P['socketSize'], P['socketDepth']
    sb = s + P['fitTol']
    # Socket sits low enough that the adapter head clears the cuff wall.
    yc = -(b_out + P['headSize'] / 2.0 + 1.0)
    # Boss runs the full band height so the cuff prints on its edge with no supports.
    bossL, bossW = sd + 4.0, h
    bossT = P['headSize'] / 2.0 + 1.0 + sb / 2.0 + 3.0

    # 1. Solid outer ellipse (X = palm width, Y = palm depth, Z = along fingers)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'Outer'
    sk.sketchCurves.sketchEllipses.add(P3(0, 0, 0), P3(a_out, 0, 0), P3(0, b_out, 0))
    body = extrude(comp, sk.profiles.item(0), h, NEW).bodies.item(0)
    body.name = 'Cuff_' + size

    # 2. Socket boss on the palm side (-Y)
    zb = (h - bossW) / 2.0
    sk = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, zb))
    sk.name = 'Boss'
    rect_on(sk, (-bossL / 2.0, -(b_out + bossT), zb), (bossL / 2.0, 0, zb))
    extrude(comp, sk.profiles.item(0), bossW, JOIN, bodies=[body])

    # 3. Hollow for the hand
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'Inner'
    sk.sketchCurves.sketchEllipses.add(P3(0, 0, 0), P3(a_in, 0, 0), P3(0, b_in, 0))
    extrude(comp, sk.profiles.item(0), h, CUT, bodies=[body])

    # 4. Thumb gap on the radial side (+X)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'ThumbGap'
    rect_on(sk, (0, -thumbGap / 2.0, 0), (a_out + 5.0, thumbGap / 2.0, 0))
    extrude(comp, sk.profiles.item(0), h, CUT, bodies=[body])

    # 5. Square socket, opening toward the thumb side
    zc = h / 2.0
    sk = comp.sketches.add(offset_plane(comp, comp.yZConstructionPlane, bossL / 2.0))
    sk.name = 'Socket'
    rect_on(sk, (bossL / 2.0, yc - sb / 2.0, zc - sb / 2.0),
                (bossL / 2.0, yc + sb / 2.0, zc + sb / 2.0))
    extrude(comp, sk.profiles.item(0), sd, CUT, NEG, [body])

    # 6. Cross pin hole through boss (Z)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'PinHole'
    circle_on(sk, (bossL / 2.0 - sd / 2.0, yc, 0), P['pinDia'])
    extrude(comp, sk.profiles.item(0), 0, CUT, bodies=[body], through_all=True)
    return comp


def build_adapter(root, name, y0, kind):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = name

    s, sd = P['socketSize'], P['socketDepth']
    H, hl = P['headSize'], P['headLen']
    shankLen = sd - 0.5
    zc = H / 2.0

    # Shank
    sk = comp.sketches.add(comp.yZConstructionPlane)
    sk.name = 'Shank'
    rect_on(sk, (0, y0 - s / 2.0, zc - s / 2.0), (0, y0 + s / 2.0, zc + s / 2.0))
    body = extrude(comp, sk.profiles.item(0), shankLen, NEW).bodies.item(0)
    body.name = name

    # Head (also the stop against the boss face)
    sk = comp.sketches.add(offset_plane(comp, comp.yZConstructionPlane, shankLen))
    sk.name = 'Head'
    rect_on(sk, (shankLen, y0 - H / 2.0, 0), (shankLen, y0 + H / 2.0, H))
    extrude(comp, sk.profiles.item(0), hl, JOIN, bodies=[body])

    # Tool pocket from the head end
    xe = shankLen + hl
    sk = comp.sketches.add(offset_plane(comp, comp.yZConstructionPlane, xe))
    sk.name = 'Pocket'
    if kind == 'flat':
        rect_on(sk, (xe, y0 - P['flatSlotH'] / 2.0, zc - P['flatSlotW'] / 2.0),
                    (xe, y0 + P['flatSlotH'] / 2.0, zc + P['flatSlotW'] / 2.0))
    else:
        circle_on(sk, (xe, y0, zc), P['roundBore'])
    extrude(comp, sk.profiles.item(0), hl - 2.0, CUT, NEG, [body])

    # Set screw pilot through head (Z)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'SetScrew'
    circle_on(sk, (shankLen + hl / 2.0, y0, 0), P['setScrewDia'])
    extrude(comp, sk.profiles.item(0), 0, CUT, bodies=[body], through_all=True)

    # Cross pin hole in shank, matches cuff boss
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'PinHole'
    circle_on(sk, (shankLen - sd / 2.0, y0, 0), P['pinDia'])
    extrude(comp, sk.profiles.item(0), 0, CUT, bodies=[body], through_all=True)
    return comp


def export_size(design, size, comps):
    em = design.exportManager
    for comp in comps:
        body = comp.bRepBodies.item(0)
        opt = em.createSTLExportOptions(body, os.path.join(OUT_DIR, comp.name + '.stl'))
        opt.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(opt)
    root = design.rootComponent
    em.execute(em.createSTEPExportOptions(os.path.join(OUT_DIR, 'GripCuff_Size_' + size + '.step'), root))
    em.execute(em.createFusionArchiveExportOptions(os.path.join(OUT_DIR, 'GripCuff_Size_' + size + '.f3d'), root))


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        if EXPORT:
            os.makedirs(OUT_DIR, exist_ok=True)

        for i, size in enumerate(BUILD):
            app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
            design = adsk.fusion.Design.cast(app.activeProduct)
            design.designType = adsk.fusion.DesignTypes.ParametricDesignType
            root = design.rootComponent

            cuff = build_cuff(root, size, **SIZES[size])
            flat = build_adapter(root, 'Adapter_Flat', -70.0, 'flat')
            rnd = build_adapter(root, 'Adapter_Round', -100.0, 'round')

            if EXPORT:
                # Adapters are identical across sizes, so export their STLs once.
                export_size(design, size, [cuff] + ([flat, rnd] if i == 0 else []))

        msg = 'Built sizes: ' + ', '.join(BUILD)
        if EXPORT:
            msg += '\nFiles saved to:\n' + OUT_DIR
        ui.messageBox(msg)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
