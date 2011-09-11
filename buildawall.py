
import sys
import logging

from pymclevel import mclevel

def wall_low_x(chunk, materials):
    chunk.Blocks[-16:-15,:,-119:120] = materials.WhiteWool.ID
    chunk.Blocks[-15:-14,:,-119:120] = materials.Bedrock.ID
    chunk.Blocks[-14:-13,:,-119:120] = materials.WhiteWool.ID

def wall_high_x(chunk, materials):
    chunk.Blocks[15:16,:,-119:120] = materials.WhiteWool.ID
    chunk.Blocks[14:15,:,-119:120] = materials.Bedrock.ID
    chunk.Blocks[13:14,:,-119:120] = materials.WhiteWool.ID

def wall_low_z(chunk, materials):
    chunk.Blocks[:,-16:-15,-119:120] = materials.WhiteWool.ID
    chunk.Blocks[:,-15:-14,-119:120] = materials.Bedrock.ID
    chunk.Blocks[:,-14:-13,-119:120] = materials.WhiteWool.ID

def wall_high_z(chunk, materials):
    chunk.Blocks[:,15:16,-119:120] = materials.WhiteWool.ID
    chunk.Blocks[:,14:15,-119:120] = materials.Bedrock.ID
    chunk.Blocks[:,13:14,-119:120] = materials.WhiteWool.ID

def main(args=sys.argv[1:]):
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        stream=sys.stdout)
    if not args:
        print """\
USAGE
  buildawall.py <level.dat>
"""
        return 1

    world = mclevel.fromFile(args[0])
    chunk_map = dict()
    print "Scanning chunks."
    for chunk_x, chunk_z in world.allChunks:
        chunk_map.setdefault(chunk_x, set()).add(chunk_z)

    print "Building walls."
    n_chunks = 0
    n_chunks_changed = 0
    for chunk_x, chunk_z in world.allChunks:
        chunk = None
        if not chunk_z in chunk_map.get(chunk_x - 1, set()):
            if not chunk: chunk = world.getChunk(chunk_x, chunk_z)
            wall_low_x(chunk, world.materials)
        if not chunk_z in chunk_map.get(chunk_x + 1, set()):
            if not chunk: chunk = world.getChunk(chunk_x, chunk_z)
            wall_high_x(chunk, world.materials)
        if not (chunk_z - 1) in chunk_map.get(chunk_x, set()):
            if not chunk: chunk = world.getChunk(chunk_x, chunk_z)
            wall_low_z(chunk, world.materials)
        if not (chunk_z + 1) in chunk_map.get(chunk_x, set()):
            if not chunk: chunk = world.getChunk(chunk_x, chunk_z)
            wall_high_z(chunk, world.materials)
        if chunk:
            import pdb; pdb.set_trace() # --miv DEBUG
            chunk.chunkChanged()
            n_chunks_changed += 1
        n_chunks += 1

    print "Changed %i of %i chunks." % (n_chunks_changed, n_chunks)
    print "Generating light."
    world.generateLights()
    print "Saving."
    world.saveInPlace()
    print "Saved."
    return 0


if __name__=='__main__':
    main()
