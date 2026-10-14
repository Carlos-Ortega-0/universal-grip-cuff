# Testing

## 1. Digital fit check (done)

`scripts/fit_check.py` loads each cuff and each adapter STL, moves the adapter into its seated position, and computes the boolean intersection volume.

Result on the released files:

| Cuff | Adapter Flat overlap (mm³) | Adapter Round overlap (mm³) |
|---|---|---|
| S | 0.0 | 0.0 |
| M | 0.0 | 0.0 |
| L | 0.0 | 0.0 |

Sanity check: moving the seated flat adapter 1 mm toward the socket wall in cuff M gives about 245 mm³ of overlap, so the test does catch collisions.

Run it:

```
pip install trimesh manifold3d
python scripts/fit_check.py
```

## 2. Print test (to do)

- [ ] Print cuff M and both adapters in PETG
- [ ] Shank slides into socket by hand, no sanding
- [ ] Pin holes line up, M3 bolt passes through
- [ ] Set screw holds a metal fork under normal use
- [ ] Pen in round adapter writes without wobble
- [ ] No sharp edges on skin-contact surfaces

## 3. User feedback (to do)

- [ ] Fit on S, M and L hands
- [ ] Review with an occupational therapist
