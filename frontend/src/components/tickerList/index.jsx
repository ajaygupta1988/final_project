import React from "react";
import { CheckboxGroup, Checkbox, Stack, Text } from "@chakra-ui/react";

const TickerList = ({ tickerList = [], onChange, selectedTickers = [] }) => {
  return (
    <>
      <Stack spacing={1}>
        <Text>Available Tickers</Text>
        <Text fontSize="xs">
          Please select the ticker from the list to display in the chart
        </Text>
      </Stack>

      <Stack direction={["column"]} spacing={3}>
        {tickerList?.length > 0 &&
          tickerList?.map((item, index) => (
            <Checkbox
              key={index}
              value={item.symbol}
              onChange={onChange}
              isChecked={selectedTickers.includes(item.symbol)}
            >
              {item.symbol}
            </Checkbox>
          ))}
      </Stack>
    </>
  );
};

export default TickerList;
