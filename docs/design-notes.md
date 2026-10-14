# Design Notes

## Goal and user

Give people with weak or no grip a way to hold everyday tools. Target users can move the arm and wrist but can't close the hand with enough force.

## Constraints

- Prints on a desktop FDM printer, no supports needed
- Fits a range of adult hands with three sizes
- Uses only M3 hardware
- Adapters work in every cuff size
- Material cost near $1 per kit

## Coordinate system (script)

- X: across the palm (palm width). +X is the thumb side.
- Y: through the palm (palm depth). -Y is the palm side.
- Z: along the fingers (band height).

Note: Fusion shows Y as up by default, so the model appears rotated in the viewport.

## Parts

### Cuff (S / M / L)

| Feature | S | M | L |
|---|---|---|---|
| Inner ellipse (mm) | 74 x 30 | 84 x 34 | 94 x 38 |
| Outer ellipse (mm) | 80 x 36 | 90 x 40 | 100 x 44 |
| Thumb gap (mm) | 22 | 26 | 30 |
| Band height (mm) | 35 | 35 | 35 |

Inner ellipse = palm size + 2 mm clearance per side. Wall = 3 mm.

Socket boss on the palm side: 30 mm long (X), 35 mm tall (Z, full band height so the cuff prints on its edge with no supports), extends 21.2 mm below the outer wall. It holds a 12.4 mm square socket, 26 mm deep, open toward the thumb side. A 3.2 mm cross pin hole runs through the boss in Z.

The socket center sits 12 mm below the lowest point of the outer wall (half the adapter head plus 1 mm). This keeps the 22 mm adapter head clear of the cuff wall when seated. An earlier version placed the socket 6.7 mm below the wall, and the head collided with the band. Fixed before release. A later pass made the boss full height to remove a support-needing overhang.

### Adapters

| Feature | Flat | Round |
|---|---|---|
| Shank | 12 x 12 x 25.5 mm | 12 x 12 x 25.5 mm |
| Head | 22 x 22 x 24 mm | 22 x 22 x 24 mm |
| Tool pocket | 4.5 x 15 mm slot, 22 mm deep | 11 mm bore, 22 mm deep |
| Set screw pilot | 2.5 mm | 2.5 mm |
| Cross pin hole | 3.2 mm, 12.5 mm from shank tip | 3.2 mm, 12.5 mm from shank tip |

The head doubles as a depth stop. It seats against the boss face and lines the pin holes up.

## How parts connect

1. Hand enters the cuff fingers first. Thumb exits through the gap.
2. Adapter shank enters the socket from the thumb side.
3. M3 x 40 bolt passes through boss and shank.
4. Tool goes into the adapter pocket. M3 self-tapping screw clamps it.

## What makes it different

- Fabric cuffs take flat handles only. This takes flat and round tools, and new adapters can be printed for anything else.
- Rigid socket gives a fixed tool angle, so the tool doesn't flop.
- Fully parametric, so a clinic can size a cuff to one patient by editing numbers.

## BOM (one kit)

| Item | Qty | Notes |
|---|---|---|
| Printed cuff (S, M or L) | 1 | PETG, ~43 to 47 g at 100% infill |
| Adapter Flat | 1 | PETG, ~17 g |
| Adapter Round | 1 | PETG, ~17 g |
| M3 x 40 bolt + nut | 1 | Cross pin |
| M3 x 8 self-tapping screw | 1 | Set screw, one per adapter in use |
| Foam liner, 1 to 2 mm | optional | Comfort |

Mass figures are solid volume x 1.27 g/cm³ (PETG). Real prints with 30 to 40% infill will weigh less.

## Parameters (script)

| Name | Default | Meaning |
|---|---|---|
| clearance | 2.0 | Skin clearance per side |
| wall | 3.0 | Cuff wall |
| cuffHeight | 35.0 | Band height |
| socketSize | 12.0 | Adapter shank size |
| socketDepth | 26.0 | Socket depth |
| fitTol | 0.4 | Extra socket width over shank |
| pinDia | 3.2 | Cross pin hole |
| headSize | 22.0 | Adapter head size |
| headLen | 24.0 | Adapter head length |
| flatSlotW / flatSlotH | 4.5 / 15.0 | Flat slot |
| roundBore | 11.0 | Round bore |
| setScrewDia | 2.5 | Set screw pilot |
