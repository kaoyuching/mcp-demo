import requests
from bs4 import BeautifulSoup
import yfinance as yf
from mcp.server.fastmcp import FastMCP


# initialize MCP server
mcp = FastMCP("stock", dependencies=["yfinance"])


# unit functions
def get_tw_stock_symbols():
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


@mcp.tool()
def get_stock_symbol(name: str):
    """
    Search stock symbol by company name.
    """
    return symbol_mapping[name]
    

# prompt template
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
