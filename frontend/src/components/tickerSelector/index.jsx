import {
  AutoComplete,
  AutoCompleteInput,
  AutoCompleteItem,
  AutoCompleteList,
} from "@choc-ui/chakra-autocomplete";
import { FormControl, FormLabel, Stack } from "@chakra-ui/react";

const TickerSelector = ({
  value,
  onChange,
  options = [],
  onSelect,
  isLoading,
}) => {
  return (
    <Stack>
      <FormControl>
        <FormLabel>Search Ticker</FormLabel>
        <AutoComplete
          openOnFocus
          border={0}
          closeOnSelect
          isLoading={isLoading}
          onSelectOption={onSelect}
        >
          <AutoCompleteInput
            size="md"
            variant="filled"
            value={null}
            maxLength={5}
            onChange={onChange}
          />
          <AutoCompleteList minHeight={"80vh"}>
            {options?.map((item, cid) => (
              <AutoCompleteItem
                key={`option-${cid}`}
                value={item.symbol}
                fontSize="xs"
                textTransform="capitalize"
              >
                {item.symbol}
              </AutoCompleteItem>
            ))}
          </AutoCompleteList>
        </AutoComplete>
      </FormControl>
    </Stack>
  );
};

export default TickerSelector;
