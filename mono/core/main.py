from dotenv import load_dotenv
load_dotenv()

from mono.core.orchestrator import Orchestrator
from mono.utils import MonoError, Color
import sys


def main():
	try:
		o = Orchestrator()
		o.run(sys.argv[1])
	except MonoError as e:
		print("Uncaught mono error.")
		Color.print(e.chain(), Color.red)
	except Exception as e:
		print("Unexpected mono error. This shouldn't have happened.")
		raise e
		
	