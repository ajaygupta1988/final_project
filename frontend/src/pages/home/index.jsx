import { useState, useEffect, useRef } from "react";
import { loader } from "../../uiComponents";
import { Box, IconButton, Stack, Text, useColorMode } from "@chakra-ui/react";
import TickerSelector from "../../components/tickerSelector";
import TickerList from "../../components/tickerList";
import DataViwer from "../../components/dataViewer";
import { serverCall } from "../../serverCall/serverCall";
import { SunIcon, MoonIcon } from "@chakra-ui/icons";

const defaultOptions = ["TSLA", "AAPL", "GOOG", "NVDA", "MSFT"];

const Home = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const [tickers, setTickers] = useState([]);
  const [tickerOptions, setTickerOptions] = useState([]);
  const [selectedTickers, setSelectedTickers] = useState(Array);
  const [data, setData] = useState({ columns: [], data: [] });
  const [dataInventory, setDataInventory] = useState({});
  const [qloading, setLoading] = useState(false);
  const loading = loader(qloading);
  const getDataEndpoint = "/get_symbol_data";
  const lookupEndpoint = "/symbol_lookup";
  const allTickersEndpoint = "/get_available_symbols";

  useEffect(() => {
    setLoading(true);
    serverCall(allTickersEndpoint).then((response) => setTickers(response));
    setLoading(false);
  }, []);

  const addDataToChart = (picker) => {
    if (dataInventory[picker]) {
      loadChartData(dataInventory[picker]);
    } else {
      serverCall(`${getDataEndpoint}/${picker}`).then((response) => {
        setLoading(true);
        setDataInventory({
          [picker]: {
            columns: response.columns,
            data: response.data,
            summary: response.summary,
          },
          ...dataInventory,
        });
        loadChartData(response);
        setLoading(false);
      });
    }
  };

  const loadChartData = (dataToload) => {
    let stale_data = data;

    if (stale_data.columns.length > 0) {
      if (stale_data.data[0].length < dataToload.data[0].length) {
        stale_data.data[0] = dataToload.data[0];
      }
      stale_data.columns.push(dataToload.columns[1]);
      stale_data.data.push(dataToload.data[1]);

      setData({ ...stale_data });
    } else {
      setData({ columns: dataToload.columns, data: dataToload.data });
    }
  };

  const deleteDataFromTheChart = (picker) => {
    if (picker) {
      let stale_data = data;
      //Find index of column and remove it
      const indexToDelete = stale_data.columns.indexOf(picker);
      // them remove the data of the same index
      if (indexToDelete > -1) {
        stale_data.columns = stale_data.columns.filter(
          (_, i) => i !== indexToDelete
        );
        stale_data.data = stale_data.data.filter((_, i) => i !== indexToDelete);
        setData({ ...stale_data });
      } else {
        // setData({ columns: response.columns, data: response.data });
      }
    }
  };

  const onSearchPicker = (term) => {
    const keywords = term.target.value;
    if (keywords.length > 3) {
      serverCall(`${lookupEndpoint}/${keywords}`).then((response) => {
        setTickerOptions(response);
      });
    }
  };

  const onSelect = ({ item }) => {
    const value = item.value;
    if (!tickers.find((d) => d.symbol === value)) {
      let tickerList = tickers;
      tickerList.push({ symbol: value });
      setTickers([...tickerList]);
    }
    console.log(
      !tickers.find((d) => d.symbol === "AAPL"),
      item,
      tickers,
      "AJAY 95"
    );
    onTickerChange(value);
  };

  const onTickerChange = (valueToInsert) => {
    let oldTickers = selectedTickers;
    const existingIndex = oldTickers.findIndex((e) => e === valueToInsert);
    if (existingIndex < 0) {
      oldTickers.push(valueToInsert);
      addDataToChart(valueToInsert);
    } else {
      oldTickers = oldTickers.filter((e) => e !== valueToInsert);
      deleteDataFromTheChart(valueToInsert);
    }
    setSelectedTickers([...oldTickers]);
  };

  return (
    <Stack
      w="100vw"
      h="100vh"
      direction={"row"}
      overflow={"hidden"}
      spacing={0}
    >
      <Stack
        w="250px"
        h="100vh"
        p="4"
        zIndex={100}
        _light={{ bg: "gray.50" }}
        _dark={{ bg: "gray.900" }}
        spacing={18}
      >
        <TickerSelector
          options={[{ symbol: "AAPL" }, { symbol: "GOOG" }] || tickerOptions}
          onChange={onSearchPicker}
          onSelect={onSelect}
        />
        <TickerList
          tickerList={tickers}
          onChange={(e) => onTickerChange(e.target.value)}
          selectedTickers={selectedTickers}
        />
      </Stack>
      <Stack
        w={"calc(100vw - 250px)"}
        id="content"
        p="8"
        alignItems={"center"}
        spacing={8}
      >
        <Stack direction="row" justify="space-between" w={"100%"}>
          <Text fontSize="2xl">Stock Chart</Text>
          <IconButton
            aria-label="Search database"
            icon={colorMode === "light" ? <MoonIcon /> : <SunIcon />}
            onClick={toggleColorMode}
          />
        </Stack>

        <DataViwer dataSet={data} />
      </Stack>
    </Stack>
  );
};

export default Home;
