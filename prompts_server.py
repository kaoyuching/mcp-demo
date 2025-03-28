from mcp.server.fastmcp import FastMCP


mcp = FastMCP("custom prompts")


@mcp.prompt()
def translate_to_chinese(texts: str) -> str:
    return f"Please translate this texts to Traditional Chinese:\n\n{texts}"


if __name__ == "__main__":
    mcp.run(transport='studio')
