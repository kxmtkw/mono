from mono.core.orchestrator import Orchestrator
from mono.interface.terminal import TerminalInterface


def main():
	iface = TerminalInterface()
	o = Orchestrator(iface)
	o.run("agents/mono.toml")