import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import DataViwer from "./";

// Mock uPlot
vi.mock("uplot-react", () => ({
  __esModule: true,
  default: vi.fn(() => <div role="figure" />),
}));

describe("DataViewer", () => {
  const sampleDataSet = {
    columns: ["unix_month_time", "stock_price"],
    data: [
      [1622505600000, 1625097600000], // example timestamps
      [150, 160], // example stock prices
    ],
  };

  it("should render the DataViwer component", () => {
    render(<DataViwer dataSet={sampleDataSet} />);
    const chart = screen.getByRole("figure"); // assuming the chart is rendered with a <figure> role or similar
    expect(chart).toBeInTheDocument();
  });

  it("should apply the correct series options", () => {
    render(<DataViwer dataSet={sampleDataSet} />);
    // Add assertions to check if the series options are correctly applied
    // This part might require more detailed knowledge about how uPlot renders the chart
    // For instance, you could mock uPlot to inspect the options passed to it
  });
});
