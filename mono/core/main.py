from mono.core.orchestrator import Orchestrator
from mono.utils import MonoError
import sys

def main():
	try:
		o = Orchestrator()
		o.run(sys.argv[1])
	except MonoError as e:
		print("Uncaught mono error.")
		print(str(e))
	except Exception as e:
		print("Unexpected mono error. This shouldn't have happened.")
		raise e
		
	