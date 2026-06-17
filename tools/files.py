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


@registry.tool(
    "createFile",
    "Create an empty file. Note: Use 'writeFile' if you intend to write content to the file, as 'writeFile' handles creation automatically.",
    {
        "path": (str, "Path to the file to create.")
    }
)
def create_file(*, path: str) -> ToolResult:
    pathobj = Path(path).expanduser()
    
    if pathobj.exists():
        return ToolResult(False, f"File already exists: {path}")
    
    try:
        pathobj.parent.mkdir(parents=True, exist_ok=True)
        pathobj.touch()
        return ToolResult(True, f"File created successfully: {path}")
    except Exception as e:
        return ToolResult(False, f"Failed to create file {path}: {str(e)}")


@registry.tool(
    "deleteFile",
    "Delete a specific file.",
    {
        "path": (str, "Path to the file to delete.")
    }
)
def delete_file(*, path: str) -> ToolResult:
    pathobj = Path(path).expanduser()
    
    if not pathobj.exists():
        return ToolResult(False, f"File not found: {path}")
    if not pathobj.is_file():
        return ToolResult(False, f"Path is not a file: {path}")
        
    try:
        pathobj.unlink()
        return ToolResult(True, f"File deleted: {path}")
    except Exception as e:
        return ToolResult(False, f"Failed to delete file {path}: {str(e)}")


@registry.tool(
    "moveFile",
    "Move or copy a file to a new location.",
    {
        "source": (str, "Source path of the file."),
        "destination": (str, "Destination path."),
        "copy": (bool, "If True, copies the file instead of moving it.")
    }
)
def move_file(*, source: str, destination: str, copy: bool = False) -> ToolResult:
    import shutil
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()

    if not src.exists() or not src.is_file():
        return ToolResult(False, f"Source file not found: {source}")

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if copy:
            shutil.copy2(src, dst)
            return ToolResult(True, f"File copied from {source} to {destination}")
        else:
            shutil.move(src, dst)
            return ToolResult(True, f"File moved from {source} to {destination}")
    except Exception as e:
        return ToolResult(False, f"Failed to {'copy' if copy else 'move'} file: {str(e)}")


@registry.tool(
    "listDirectory",
    "List the contents of a directory, including hidden files if requested.",
    {
        "path": (str, "Path to the directory."),
        "hidden": (bool, "If True, include hidden files in the output.")
    }
)
def list_directory(*, path: str, hidden: bool = False) -> ToolResult:
    pathobj = Path(path).expanduser()
    
    if not pathobj.exists() or not pathobj.is_dir():
        return ToolResult(False, f"Directory not found: {path}")
        
    try:
        # If hidden is False, filter out files/folders starting with '.'
        items = [
            item.name for item in pathobj.iterdir() 
            if hidden or not item.name.startswith('.')
        ]
        return ToolResult(True, f"Contents of {path}:\n" + "\n".join(items))
    except Exception as e:
        return ToolResult(False, f"Failed to list directory: {str(e)}")


@registry.tool(
    "createDirectory",
    "Create a new directory.",
    {
        "path": (str, "Path to the directory to create.")
    }
)
def create_directory(*, path: str) -> ToolResult:
    pathobj = Path(path).expanduser()
    
    try:
        pathobj.mkdir(parents=True, exist_ok=True)
        return ToolResult(True, f"Directory created: {path}")
    except Exception as e:
        return ToolResult(False, f"Failed to create directory: {str(e)}")


@registry.tool(
    "moveDirectory",
    "Move or copy a directory and its contents to a new location.",
    {
        "source": (str, "Source directory path."),
        "destination": (str, "Destination directory path."),
        "copy": (bool, "If True, copies the directory instead of moving it.")
    }
)
def move_directory(*, source: str, destination: str, copy: bool = False) -> ToolResult:
    import shutil
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()

    if not src.exists() or not src.is_dir():
        return ToolResult(False, f"Source directory not found: {source}")

    try:
        if copy:
            shutil.copytree(src, dst)
            return ToolResult(True, f"Directory copied from {source} to {destination}")
        else:
            shutil.move(src, dst)
            return ToolResult(True, f"Directory moved from {source} to {destination}")
    except Exception as e:
        return ToolResult(False, f"Failed to {'copy' if copy else 'move'} directory: {str(e)}")


@registry.tool(
    "deleteDirectory",
    "Delete a directory and all its contents.",
    {
        "path": (str, "Path to the directory to delete.")
    }
)
def delete_directory(*, path: str) -> ToolResult:
    import shutil
    pathobj = Path(path).expanduser()
    
    if not pathobj.exists() or not pathobj.is_dir():
        return ToolResult(False, f"Directory not found: {path}")
        
    try:
        shutil.rmtree(pathobj)
        return ToolResult(True, f"Directory deleted: {path}")
    except Exception as e:
        return ToolResult(False, f"Failed to delete directory: {str(e)}")

registry.submit()