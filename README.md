buildawall - a wall builder for Minecraft. It builds a wall around
your world.


Minecraft worlds are driven by a seed, and Minecraft creates the world
from the seed as you visit new parts. However, upgrades to Minecraft
can knock the world builder out of whack, and create jarring
discontinuities where the old world ends and the new world begins.

Buildawall puts a wall around your existing world, creating a
psychological and in-game division between old and new.

By default the wall is white wool with a core of indestructable
bedrock. It's not-quite maximum height or depth, so you can climb over
it or burrow under it, though that's still a challenge. By tweaking
the script you can change the wall material, and make it destructable
if you want.

Usage
-----

These instructions are for Mac OS X. Ensure you have a working Python 2.x release.

Clone and install pymclevel (it's not in PyPI, sadly).

    git clone git://github.com/mcedit/pymclevel.git
    cd pymclevel
    python setup.py install
    
Clone and install buildawall

     cd ..
     git clone git://github.com/sixohsix/minecraft-buildawall.git
     cd minecraft-buildawall
     python setup.py install

Make a backup of your world

    cp -pr ~/Library/Application\ Support/minecraft/saves/your_world_name ~/world_backup
    
Run buildawall

    buildawall ~/Library/Application\ Support/minecraft/saves/your_world_name/level.dat

Wait.

Play.
