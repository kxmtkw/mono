from mono.core.orchestrator import Orchestrator
import sys

def main():
	o = Orchestrator()
	o.run(sys.argv[1])