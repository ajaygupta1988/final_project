import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import TickerList from "./";

describe("TickerList", () => {
  it("should display the header text", () => {
    render(<TickerList />);
    expect(screen.getByText("Available Tickers")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Please select the ticker from the list to display in the chart"
      )
    ).toBeInTheDocument();
  });

  it("should render the ticker list", () => {
    const tickers = [
      { symbol: "AAPL" },
      { symbol: "GOOG" },
      { symbol: "MSFT" },
    ];
    render(<TickerList tickerList={tickers} />);
    tickers.forEach((ticker) => {
      expect(screen.getByText(ticker.symbol)).toBeInTheDocument();
    });
  });

  it("should call onChange when a ticker is checked", () => {
    const tickers = [{ symbol: "AAPL" }, { symbol: "GOOG" }];
    const handleChange = vi.fn();
    render(<TickerList tickerList={tickers} onChange={handleChange} />);

    tickers.forEach((ticker) => {
      const checkbox = screen.getByLabelText(ticker.symbol);
      fireEvent.click(checkbox);
      expect(handleChange).toHaveBeenCalled();
    });
  });

  it("should check checkboxes based on selectedTickers", () => {
    const tickers = [{ symbol: "AAPL" }, { symbol: "GOOG" }];
    const selectedTickers = ["AAPL"];
    render(
      <TickerList tickerList={tickers} selectedTickers={selectedTickers} />
    );

    tickers.forEach((ticker) => {
      const checkbox = screen.getByLabelText(ticker.symbol);
      if (selectedTickers.includes(ticker.symbol)) {
        expect(checkbox).toBeChecked();
      } else {
        expect(checkbox).not.toBeChecked();
      }
    });
  });
});
