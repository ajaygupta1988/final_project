import axios from 'axios';
import {createStandaloneToast} from '@chakra-ui/toast';
const {toast} = createStandaloneToast();
const baseURL = import.meta.env.VITE_API_URL

const axiosInstance = axios.create({
    baseURL: baseURL,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  });

export function serverCall(endpoint) {
    return axiosInstance({
      method: "get",
      url: endpoint,
    })
      .then(response => {
            // toast({
            //   position: 'top',
            //   title: 'Success',
            //   status: 'success',
            //   isClosable: true,
            // });
        return response.data;
      })
      .catch(error => {
        toast({
            position: 'top',
            variant: 'subtle',
            title: 'Session Expired',
            description: 'Oops! Somthing went wrong.',
            status: 'error',
            isClosable: true,
          });
      });
  }