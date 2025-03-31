import requests
from bs4 import BeautifulSoup
import yfinance as yf
from mcp.server.fastmcp import FastMCP


# initialize MCP server
mcp = FastMCP("stock", dependencies=["yfinance"])


# unit functions
def get_tw_stock_symbols():
    """
    Stock name and symbol mapping.
    """
    urls = ["https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",  # listed
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=3",  # bond
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"  # otc
    ]

    symbol_mapping = {}
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for x in soup.find_all('tr')[2:]:
          symbol = x.find('td').text.split('\u3000')
          if len(symbol) == 2:
            symbol_mapping[symbol[1]] = symbol[0] + ".TW"
    return symbol_mapping

symbol_mapping = get_tw_stock_symbols()


# tools
@mcp.tool()
def get_realtime_stock_price(ticker_symbol: str):
    """
    Get realtime stock price.

    Args:
        ticker_symbol: ticker symbol.
    """
    ticker = yf.Ticker(ticker_symbol)
    tradeable = ticker.info.get("tradeable")
    ticker_info = ticker.info
    if ticker_info.get("regularMarketPrice", None):
        realtime_price = ticker_info["regularMarketPrice"]
    elif ticker_info.get("currentPrice", None):
        realtime_price = ticker_info["currentPrice"]
    elif ticker.fast_info.get("lastPrice", None):
        realtime_price = ticker.fast_info["lastPrice"]
    else:
        realtime_price = None
    return {"tradeable": tradeable, "realtime_price": realtime_price}


@mcp.tool()
def get_stock_previous_close(ticker_symbol: str):
    """
    Get the previous close price.

    Args:
        ticker_symbol: ticker symbol.
    """
    ticker = yf.Ticker(ticker_symbol)
    tradeable = ticker.info.get("tradeable")
    ticker_info = ticker.info
    if not tradeable:
        if ticker_info.get("regularMarketPrice", None):
            previous_close  = ticker_info["regularMarketPrice"]
        elif ticker_info.get("currentPrice", None):
            previous_close = ticker_info["currentPrice"]
        elif ticker.fast_info.get("lastPrice", None):
            previous_close = ticker.fast_info["lastPrice"]
    else:
        previous_close = ticker_info['regularMarketPreviousClose']
    return previous_close


@mcp.tool()
def get_stock_symbol(name: str):
    """
    Search stock symbol by company name.
    """
    return symbol_mapping[name]
    

# prompt template
@mcp.prompt()
def ask_realtime_stock_price(company: str):
    """
    Ask realtime stock price.

    Args:
        company: company name
    """
    return f"請問{company}現在的股價多少?"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
