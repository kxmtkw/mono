from mono.tools.toolbox import ToolRegistry, ToolResult

from datetime import datetime


registry = ToolRegistry("time")


@registry.tool(
    "getDateTime",
    "Get the current date and time in a specified format.",
    {
        "fmt": (str, "The strftime format string (e.g., '%Y-%m-%d %I:%M:%S %P'). Defaults to ISO format if none is provided.")
    }
)
def get_date_time(*, fmt: str | None = None) -> ToolResult:

    try:
        now = datetime.now()
        if fmt:
            formatted_time = now.strftime(fmt)
        else:
            formatted_time = now.isoformat()
            
        return ToolResult(
            True,
            f"Current time: {formatted_time}"
        )
    except Exception as e:
        return ToolResult(
            False,
            f"Failed to format date/time: {str(e)}"
        )
    

registry.submit()