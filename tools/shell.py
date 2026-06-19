from mono.tools.toolbox import ToolRegistry, ToolResult

import os, subprocess


registry = ToolRegistry("shell")


@registry.tool(
	"shell",
	f"Run a shell command. OS: {os.name}",
	{
		"cmd": (str, "Command to run.")
	}
)
def shell_run(*, cmd: str) -> ToolResult:

	try:
		output = subprocess.run(
			cmd,
			shell=True,
			capture_output=True, 
			timeout=60,
			text=True
		)
	except Exception as e:
		return ToolResult(
			False,
			f"Failed to run shell command. Error: ({e.__class__.__name__}) {e}"
		)

	return ToolResult(True, f"RETURNCODE:{output.returncode}\nSTDOUT:\n{output.stdout}\nSTDERR:\n{output.stderr}")


registry.submit()