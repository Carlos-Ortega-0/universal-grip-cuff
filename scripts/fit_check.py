"""Fit check: seat each adapter in each cuff and measure overlap volume.

Usage (from repo root):
    pip install trimesh manifold3d
    python scripts/fit_check.py
"""
import os
import trimesh

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Outer half-depth of each cuff (palmDepth/2 + clearance + wall), mm
B_OUT = {'S': 18.0, 'M': 20.0, 'L': 22.0}
# Y offset each adapter was modeled at in the Fusion script
Y0 = {'Flat': -70.0, 'Round': -100.0}
HEAD = 22.0           # adapter head size
SOCKET_DEPTH = 26.0
BOSS_FACE_X = 15.0    # bossL / 2
CUFF_HEIGHT = 35.0


def seated(kind, size):
    a = trimesh.load(os.path.join(ROOT, 'stl', 'adapters', f'Adapter_{kind}.stl'))
    yc = -(B_OUT[size] + HEAD / 2.0 + 1.0)      # socket centre in the cuff
    shank_len = SOCKET_DEPTH - 0.5
    a.apply_translation([BOSS_FACE_X - shank_len, yc - Y0[kind], CUFF_HEIGHT / 2.0 - HEAD / 2.0])
    return a


def main():
    print('size adapter overlap_mm3')
    for size in 'SML':
        cuff = trimesh.load(os.path.join(ROOT, 'stl', f'size-{size}', f'Cuff_{size}.stl'))
        for kind in Y0:
            inter = trimesh.boolean.intersection([cuff, seated(kind, size)])
            v = 0.0 if inter.is_empty else abs(inter.volume)
            print(f'{size}    {kind:<7} {v:.2f}')


if __name__ == '__main__':
    main()
