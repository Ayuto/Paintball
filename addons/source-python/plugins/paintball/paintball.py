# Thanks to L'In20Cible for the paintball decals!

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import random

# Source.Python
from paths   import GAME_PATH
from events  import Event
from effects import temp_entities
from mathlib import Vector

from cvars import ConVar
from cvars.flags import ConVarFlags

from plugins.info           import PluginInfo
from engines.server         import engine_server
from filters.recipients     import RecipientFilter
from stringtables.downloads import Downloadables


# =============================================================================
# >> PLUGIN INFORMATION
# =============================================================================
info = PluginInfo()
info.author = 'Ayuto'
info.basename = 'paintball'
info.name = 'Paintball'
info.description = 'Adds paintball effects to the game.'
info.version = '1.1'
info.url = 'http://www.sourcepython.com/index.php'

ConVar('paintball_version', info.version, ConVarFlags.NOTIFY, info.description)


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

    temp_entities.world_decal(
        # Show the decal to all players
        RecipientFilter(),

        # Create it without a delay
        0,

        # Create the decal at the impact location
        Vector(*tuple(event.get_float(key) for key in 'xyz')),

        # Choose a random paintball material and precache it. It will return
        # an index.
        engine_server.precache_decal(random.choice(materials))
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
