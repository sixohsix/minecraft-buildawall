
import sys
import logging
from contextlib import contextmanager

from pymclevel import mclevel, ChunkNotPresent

"""
  -x
-z  +z
  +x

"""


class WallBuilder(object):
    def __init__(self, level, min_height=-119, max_height=119,
                 outer_mat_id=None, inner_mat_id=None):
        self.mih = min_height
        self.mah = max_height
        self.om = outer_mat_id or level.materials.WhiteWool.ID
        self.im = inner_mat_id or level.materials.Bedrock.ID
        self.level = level


    @contextmanager
    def chunk(self, chunk_address):
        chunk = self.level.getChunk(*chunk_address)
        yield chunk
        chunk.chunkChanged()


    @contextmanager
    def y_bound_blocks(self, chunk_address):
        with self.chunk(chunk_address) as chunk:
            yield chunk.Blocks[:,:,self.mih:self.mah+1]


    def build_walls(self):
        chunk_map = dict()
        print "Scanning chunks."
        for chunk_x, chunk_z in self.level.allChunks:
            chunk_map.setdefault(chunk_x, set()).add(chunk_z)

        print "Building walls."
        walls_px = set()
        walls_nx = set()
        walls_pz = set()
        walls_nz = set()

        null_set = set()

        for chunk_x, chunk_z in self.level.allChunks:
            chunk = (chunk_x, chunk_z)
            if not chunk_z in chunk_map.get(chunk_x - 1, null_set):
                walls_nx.add(chunk)
                self.wall_x(0, chunk)
            if not chunk_z in chunk_map.get(chunk_x + 1, null_set):
                walls_px.add(chunk)
                self.wall_x(1, chunk)
            if not (chunk_z - 1) in chunk_map.get(chunk_x, null_set):
                walls_nz.add(chunk)
                self.wall_z(0, chunk)
            if not (chunk_z + 1) in chunk_map.get(chunk_x, null_set):
                walls_pz.add(chunk)
                self.wall_z(1, chunk)

        for chunk_x, chunk_z in walls_nx:
            if (chunk_x, chunk_z - 1) not in walls_nx:
                self.corner(1, 2, (chunk_x, chunk_z - 1))
            if (chunk_x, chunk_z + 1) not in walls_nx:
                self.corner(0, 3, (chunk_x, chunk_z + 1))
        for chunk_x, chunk_z in walls_px:
            if (chunk_x, chunk_z - 1) not in walls_px:
                self.corner(3, 0, (chunk_x, chunk_z - 1))
            if (chunk_x, chunk_z + 1) not in walls_px:
                self.corner(2, 1, (chunk_x, chunk_z + 1))
        for chunk_x, chunk_z in walls_nz:
            if (chunk_x - 1, chunk_z) not in walls_nz:
                self.corner(2, 1, (chunk_x - 1, chunk_z))
            if (chunk_x + 1, chunk_z) not in walls_nz:
                self.corner(0, 3, (chunk_x + 1, chunk_z))
        for chunk_x, chunk_z in walls_pz:
            if (chunk_x - 1, chunk_z) not in walls_pz:
                self.corner(3, 0, (chunk_x - 1, chunk_z))
            if (chunk_x + 1, chunk_z) not in walls_pz:
                self.corner(1, 2, (chunk_x + 1, chunk_z))

        for chunk_a in walls_nx:
            if chunk_a in walls_nz:
                self.corner(0, 0, chunk_a)
            if chunk_a in walls_pz:
                self.corner(1, 1, chunk_a)
        for chunk_a in walls_px:
            if chunk_a in walls_nz:
                self.corner(2, 2, chunk_a)
            if chunk_a in walls_pz:
                self.corner(3, 3, chunk_a)


    def wall_x(self, side, chunk_a):
        with self.y_bound_blocks(chunk_a) as blocks:
            low_ix = 13 if side else -16
            blocks[low_ix,:,:] = self.om
            blocks[low_ix+1,:,:] = self.im
            blocks[low_ix+2,:,:] = self.om


    def wall_z(self, side, chunk_a):
        with self.y_bound_blocks(chunk_a) as blocks:
            low_ix = 13 if side else -16
            blocks[:,low_ix,:] = self.om
            blocks[:,low_ix+1,:] = self.im
            blocks[:,low_ix+2,:] = self.om


    def corner(self, corner, out_direction, chunk_a):
        try:
            with self.y_bound_blocks(chunk_a) as blocks:
                corner_blocks = self.bound_corner(corner, blocks)
                self.carve_corner(out_direction, corner_blocks)
        except ChunkNotPresent:
            pass


    def carve_corner(self, out_direction, blocks):
        """
        out_direction:
          0: ooo      1: ooo
             oii         iio
             oio         oio

          2: oio      3: oio
             oii         iio
             ooo         ooo
        """
        x_flip = bool(out_direction & 2) * 2
        z_flip = bool(out_direction & 1) * 2
        blocks[:,:,:]      = self.im
        blocks[x_flip,:,:] = self.om
        blocks[:,z_flip,:] = self.om
        blocks[2-x_flip,2-z_flip,:] = self.om


    def bound_corner(self, corner, blocks):
        """
        0 1
        2 3
        """
        # lol
        x = int((((bool(corner & 2) * 2) - 1) * 14.5) - 1.5)
        z = int((((bool(corner & 1) * 2) - 1) * 14.5) - 1.5)
        return blocks[x:x+3,z:z+3,:]


def main(args=sys.argv):
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        stream=sys.stdout)
    if not args[1:]:
        print """\
USAGE
  buildawall.py <level.dat>
"""
        return 1

    world = mclevel.fromFile(args[1])
    WallBuilder(world).build_walls()

    print "Generating light."
    world.generateLights()
    print "Saving."
    world.saveInPlace()
    print "Saved."
    return 0
