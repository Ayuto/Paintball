# Thanks to L'In20Cible for the paintball decals!

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import random

# Source.Python
from paths   import GAME_PATH
from events  import Event
from mathlib import Vector

from cvars.public           import PublicConVar
from effects.base           import TempEntity
from plugins.info           import PluginInfo
from engines.server         import engine_server
from stringtables.downloads import Downloadables


# =============================================================================
# >> PLUGIN INFORMATION
# =============================================================================
info = PluginInfo()
info.author = 'Ayuto'
info.basename = 'paintball'
info.name = 'Paintball'
info.description = 'Adds paintball effects to the game.'
info.version = '1.2'
info.url = 'http://www.sourcepython.com/index.php'

PublicConVar('paintball_version', info.version, description=info.description)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# ../<game>/materials/paintball
PAINTBALL_MATERIALS = GAME_PATH / 'materials' / 'paintball'

# Create a downloadables container
dl = Downloadables()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('bullet_impact')
def bullet_impact(event):
    """Called whenever a bullet hits something."""
    entity = TempEntity('World Decal')

    # Create the decal at the impact location
    entity.origin = Vector(*tuple(event.get_float(key) for key in 'xyz'))

    # Choose a random paintball material and precache it. It will return an
    # index.
    entity.decal_index = engine_server.precache_decal(random.choice(materials))

    entity.create()


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def prepare_materials():
    """Adds all found paintball materials to the download table and returns
    the added material names as a tuple."""

    materials = set()

    # Loop through all paintball material files
    for f in PAINTBALL_MATERIALS.files():
        materials.add('paintball/%s.vmt'% f.namebase)

        # Add the file to the download table
        dl.add(str('materials/paintball/' + f.basename()))

    return tuple(materials)

materials = prepare_materials()

# Check if any material was found
if not materials:
    raise ValueError('No paintball materials were found.')
