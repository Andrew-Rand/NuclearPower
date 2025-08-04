import pydantic

from core.events import BaseUnitEvet
from reactor.unit import Reactor


class RiseRods(BaseUnitEvet):
    '''lift the rods out of the reactor'''
    unit: Reactor


class LowerRods(BaseUnitEvet):
    '''Return rods back to the reactor'''
    unit: Reactor


class ReactorAZ(BaseUnitEvet):
    '''All rods down'''
    # TODO: add a litle reactivity first 2 seconds
    unit: Reactor