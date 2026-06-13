from mono.core.orchestrator import Orchestrator
from mono.interface.terminal import TerminalInterface

iface = TerminalInterface()
o = Orchestrator(iface)
o.run("/home/haseeb/code/mono/mono.toml")