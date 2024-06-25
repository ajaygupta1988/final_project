import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import TickerSelector from "./";

describe("TickerSelector", () => {
  it("should render the search input and label", () => {
    render(<TickerSelector />);
    expect(screen.getByLabelText("Search Ticker")).toBeInTheDocument();
  });

  it("should render the options when typing", () => {
    const options = [{ symbol: "AAPL" }, { symbol: "GOOG" }];
    render(<TickerSelector options={options} />);

    const input = screen.getByLabelText("Search Ticker");
    fireEvent.change(input, { target: { value: "A" } });

    expect(screen.getByText("AAPL")).toBeInTheDocument();
  });

  it("should call onChange when typing in the input", () => {
    const handleChange = vi.fn();
    render(<TickerSelector onChange={handleChange} />);

    const input = screen.getByLabelText("Search Ticker");
    fireEvent.change(input, { target: { value: "A" } });

    expect(handleChange).toHaveBeenCalled();
  });

  it("should call onSelect when an option is selected", () => {
    const options = [{ symbol: "AAPL" }, { symbol: "GOOG" }];
    const handleSelect = vi.fn();
    render(<TickerSelector options={options} onSelect={handleSelect} />);

    const input = screen.getByLabelText("Search Ticker");
    fireEvent.change(input, { target: { value: "A" } });

    const option = screen.getByText("AAPL");
    fireEvent.click(option);

    expect(handleSelect).toHaveBeenCalled();
  });
});
