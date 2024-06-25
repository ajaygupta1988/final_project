import {
  AutoComplete,
  AutoCompleteInput,
  AutoCompleteItem,
  AutoCompleteList,
} from "@choc-ui/chakra-autocomplete";
import { FormControl, FormLabel, Stack } from "@chakra-ui/react";

const TickerSelector = ({ value, onChange, options = [], onSelect }) => {
  return (
    <Stack>
      <FormControl>
        <FormLabel>Search Ticker</FormLabel>
        <AutoComplete border={0} onSelectOption={onSelect}>
          <AutoCompleteInput
            size="sm"
            variant="filled"
            value={null}
            onChange={onChange}
          />
          <AutoCompleteList>
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
