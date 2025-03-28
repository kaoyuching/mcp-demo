import yfinance as yf
from mcp.server.fastmcp import FastMCP


# initialize MCP server
mcp = FastMCP("stock")


# tools
@mcp.tool()
def get_realtime_stock_price(ticker_symbol: str):
    """
    Get realtime stock price.

    Args:
        ticker_symbol: ticker symbol.
    """
    ticker = yf.Ticker(ticker_symbol)
    realtime_price = ticker.info['regularMarketPrice']
    return realtime_price


@mcp.tool()
def get_stock_previous_close(ticker_symbol: str):
    """
    Get the previous close price.

    Args:
        ticker_symbol: ticker symbol.
    """
    ticker = yf.Ticker(ticker_symbol)
    previous_close = ticker.info['regularMarketPreviousClose']
    return previous_close


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
