# Thanks to L'In20Cible for the paintball decals!

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import random

# Source.Python
from engines.server import EngineServer
from mathlib import Vector
from cvars import FCVAR_NOTIFY

from paths     import GAME_PATH
from cvars     import ServerVar
from events    import Event
from downloads import Downloadables
from effects   import TempEntities

from filters.recipients import RecipientFilter
from plugins.info       import PluginInfo


# =============================================================================
# >> PLUGIN INFORMATION
# =============================================================================
info = PluginInfo()
info.author = 'Ayuto'
info.basename = 'paintball'
info.name = 'Paintball'
info.description = 'Adds paintball effects to the game.'
info.version = '1.0'
info.url = 'http://www.sourcepython.com/index.php'

ServerVar('paintball_version', info.version, FCVAR_NOTIFY, info.description)


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
@Event
def bullet_impact(event):
    '''
    Gets called whenever a bullet hits something.
    '''

    TempEntities.world_decal(
        # Show the decal to all players
        RecipientFilter(),

        # Create it without a delay
        0,

        # Create the decal at the impact location
        Vector(*tuple(event.get_float(key) for key in 'xyz')),

        # Choose a random paintball material and precache it. It will return
        # an index.
        EngineServer.precache_decal(random.choice(materials))
    )


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def prepare_materials():
    '''
    Adds all found paintball materials to the download table and returns the
    added material names as a tuple.
    '''

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
