from mono.tools.toolbox import ToolRegistry, ToolResult


from pathlib import Path

registry = ToolRegistry("files")

@registry.tool(
	"readFile",
	"Read a file and return its content.",
	{
		"path": (str, "Path to file. All OS paths supported. ~ supported for unix based.")
	}
)
def read_file(*, path: str) -> ToolResult:

	pathobj = Path(path).expanduser()

	if not pathobj.exists():
		return ToolResult(
			False,
			f"File not found: {path}."
		)
	
	if not pathobj.is_file():
		return ToolResult(
			False,
			f"Is not a file: {path}."
		)
	
	with open(pathobj.absolute()) as file:
		content = file.read()

	return ToolResult(
		True,
		f"File read: {path}.\n<file>\n{content}</file>\n"
	)


@registry.tool(
    "writeFile",
    "Write content to a file. Overwrites if file exists.",
    {
        "path": (str, "Path to file. All OS paths supported. ~ supported for unix based."),
        "content": (str, "The text content to write to the file.")
    }
)
def write_file(*, path: str, content: str) -> ToolResult:
    
    pathobj = Path(path).expanduser()
    
    try:
        pathobj.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return ToolResult(
            False,
            f"Failed to create directories for {path}: {str(e)}"
        )
    
    try:
        with open(pathobj.absolute(), 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        return ToolResult(
            False,
            f"Failed to write file {path}: {str(e)}"
        )

    return ToolResult(
        True,
        f"File written successfully: {path}."
    )


registry.submit()