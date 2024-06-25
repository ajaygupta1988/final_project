import { useCallback, useRef, useLayoutEffect, useState } from "react";
import uPlot from "uplot";
import UplotReact from "uplot-react";
import { Box, useColorModeValue, Flex } from "@chakra-ui/react";
import "uplot/dist/uPlot.min.css";
import moment from "moment";

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
import useResizeObserver from "@react-hook/resize-observer";
import noData from "./nodata.json";

const useSize = (target) => {
  const [size, setSize] = useState();

  useLayoutEffect(() => {
    if (target.current) {
      setSize(target.current.getBoundingClientRect());
    }
  }, [target]);

  // Where the magic happens
  useResizeObserver(target, (entry) => setSize(entry.contentRect));
  return size;
};

export const DataViwer = ({
  dataSet = noData,
  height = 650,
  width = 1600,
  loading = false,
}) => {
  const elementRef = useRef(null);
  const size = useSize(elementRef);
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
            value: (self, rawValue) => moment.unix(rawValue).format("ll"),
          };
        } else {
          result = {
            label: item,
            width: 2,
            stroke: chartColors[i],
            scale: "y",
            points: { show: false, fill: chartColors[i] },
            spanGaps: true,
          };
        }
        return result;
      });
    }
    return result;
  }, [dataSet]);

  const renderChart = useCallback(() => {
    let options = {};
    if (dataSet.columns.length > 0) {
      options = {
        width: size?.width || width,
        height: size?.height - 100 || height,
        axes: [
          {
            label: "Time Period",
            stroke: chartTextColor,
            labelFont: "12px Poppins, sans-serif",
          },
          {
            scale: "y",
            label: "Stock Price",
            labelFont: "Poppins, sans-serif",
            stroke: chartTextColor,
          },
        ],
        series: getSeries(),
        scales: {
          x: { time: true },
        },
      };
    } else {
      options = {
        width: size?.width || width,
        height: size?.height - 100 || height,
        axes: [
          {
            label: "Time Period",
            stroke: chartTextColor,
            labelFont: "12px Poppins, sans-serif",
          },
          {
            scale: "",
            label: "Stock Price",
            labelFont: "Poppins, sans-serif",
            stroke: chartTextColor,
          },
        ],
        scales: {
          x: {
            range(u, dataMin, dataMax) {
              if (dataMin == null) return [1717200000, 944006400];
              return [dataMin, dataMax];
            },
          },
          y: {
            range(u, dataMin, dataMax) {
              if (dataMin == null) return [0, 100];
              return uPlot.rangeNum(dataMin, dataMax, 1, true);
            },
          },
        },
        // plugins: [touchZoomPlugin],
      };
    }

    return <UplotReact options={options} data={data} />;
  }, [dataSet]);

  return (
    <Flex overflowX={"overlay"} ref={elementRef} h={"100%"} width={"100%"}>
      <Flex role="figure">{renderChart()}</Flex>
    </Flex>
  );
};

export default DataViwer;
