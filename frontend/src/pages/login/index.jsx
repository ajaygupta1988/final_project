import React, { useState } from "react";
import {
  Stack,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Text,
  Input,
  FormHelperText,
  Button,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { Logo } from "../../uiComponents";

const Login = () => {
  const {
    handleSubmit,
    register,
    reset,
    formState: { errors },
  } = useForm();
  const [input, setInput] = useState("");
  const handleInputChange = (e) => setInput(e.target.value);

  const isError = input === "";
  const onSubmit = (data) => {
    setInput(data.text_value);
  };

  const onClearClick = () => {
    reset();
    setInput(null);
  };

  return (
    <Stack w="100vw" h="100vh" justify={"center"} align={"center"} spacing={70}>
      <Text fontSize="xl">Front End Assignment Ajay Gupta</Text>
      {input && (
        <Stack direction={"row"} align="center">
          <Text>You have entered: {input} </Text>
          <Button onClick={onClearClick} variant="ghost">
            Clear
          </Button>
        </Stack>
      )}
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack w={500} spacing={12}>
          <FormControl isInvalid={errors.text_value} isRequired>
            <FormLabel htmlFor="text_value">
              Please Enter the text below you want to print.
            </FormLabel>
            <Input
              id="text_value"
              placeholder="Enter text to print"
              {...register("text_value", {
                required: "This is required",
              })}
            />
            <FormErrorMessage>
              {errors.text_value && errors.text_value.message}
            </FormErrorMessage>
          </FormControl>
          <Button
            type="submit"
            size="md"
            // loading={loading}
            colorScheme="primary"
          >
            Submit
          </Button>
        </Stack>
      </form>
    </Stack>
  );
};

export default Login;
