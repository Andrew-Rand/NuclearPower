from reactor.events import RiseRods, LowerRods, ReactorAZ
from reactor.handlers import rise_rods, lower_rods, stop_reactor

MAPPER = {
    RiseRods: rise_rods,
    LowerRods: lower_rods,
    ReactorAZ: stop_reactor,
}