import { useState, useEffect, useRef } from "react";
import { loader } from "../../uiComponents";
import { Box, Button, Stack , Text} from "@chakra-ui/react";



const Home = () => {
  const [data, setData] = useState(null);
  const [qloading, setLoading] = useState(false);
  const loading = loader(qloading);

  useEffect(() => {
    // axios.get("http://127.0.0.1:8000/places").then((res) => setData(res.data));
    // duckQuery("select * from whatever").then((res) => setData(res));
  }, []);

  console.log(qloading, "ajay");


  const onQuery = (value) => {
    if (value) {
      setLoading(true);
      // duckQuery(value).then((res) => {
      //   setData(res);
      //   setLoading(false);
      // });
    }
  };

  return (
    <Stack
      w="100vw"
      h="100vh"
      direction={"row"}
      overflow={"hidden"}
      spacing={0}
    >
      <Stack w="250px" h="100vh" bg="gray.400"></Stack>
      <Stack w={"calc(100vw - 250px)"} id="content">
      <Text>This is the place for charts</Text>
      </Stack>
    </Stack>
  );
};

export default Home;
