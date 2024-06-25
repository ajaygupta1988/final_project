import { useCallback, useRef } from "react";
import UplotReact from "uplot-react";
import { Flex, useColorModeValue, useDimensions } from "@chakra-ui/react";
import "uplot/dist/uPlot.min.css";

export const chartColors = [
  "gray",
  "#37a2eb",
  "#ff6384",
  "#4cc0c0",
  "#ffa600",
  "#805AD5",
  "#F6E05E",
  "#00B5D8",
  "#D53F8C",
  "#6ec12c",
  "#E53E3E",
  "#a05195",
  "#38A169",
  "#ff7c43",
  "#665191",
  "#319795",
  "#656c80",
  "#003f5c",
  "#2f4b7c",
  "#d45087",
  "#f95d6a",
  "#DD6B20",
];

export const DataViwer = ({
  dataSet = sample,
  height = 650,
  width = 1600,
  loading = false,
}) => {
  const elementRef = useRef();
  const dimensions = useDimensions(elementRef, true);
  const chartTextColor = useColorModeValue("#718096", "#fff");
  const { columns, data } = dataSet;

  const getSeries = useCallback(() => {
    let result = [];
    if (columns?.length > 0) {
      result = columns.map((item, i) => {
        let result = null;
        if (item === "unix_month_time") {
          result = {
            label: "datetime",
            value: (self, rawValue) => rawValue,
          };
        } else {
          result = {
            label: item.replaceAll("_", " "),
            width: 2,
            stroke: chartColors[i],
            scale: "impedance",
            points: { show: true, fill: chartColors[i] },
            spanGaps: true,
          };
        }
        return result;
      });
    }
    return result;
  }, [dataSet]);

  const renderChart = useCallback(() => {
    const options = {
      width: width,
      height: height,
      axes: [
        {
          label: "Time Period",
          stroke: chartTextColor,
          labelFont: "12px Poppins, sans-serif",
        },
        {
          scale: "impedance",
          label: "Stock Price",
          labelFont: "Poppins, sans-serif",
          stroke: chartTextColor,
          values: (self, ticks) => ticks.map((rawValue) => rawValue),
        },
      ],
      series: getSeries(),
      scales: {
        x: { time: true },
      },
      // plugins: [touchZoomPlugin],
    };
    return <UplotReact options={options} data={data} />;
  }, [dataSet]);

  return (
    <Flex overflowX={"overlay"} ref={elementRef}>
      {dimensions?.borderBox?.height}
      <Flex>{renderChart()}</Flex>
    </Flex>
  );
};

export default DataViwer;
