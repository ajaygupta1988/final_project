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

export function serverCall(endpoint, showSucces, succesMessage,status ) {
    return axiosInstance({
      method: "get",
      url: endpoint,
    })
      .then(response => {
        if (response?.data?.source === 'external') {
          toast({
            position: 'top',
            title: 'Success',
            status: 'warning',
            description:'This data came from external api. But we have send a message queue to collector to get this data in our database for next query.', 
            isClosable: true,
          });
        } else if (response?.data?.source === 'internal') {
          toast({
            position: 'top',
            title: 'Success',
            status: 'success',
            description:'This data is now coming from Mongo DB', 
            isClosable: true,
          });
        }
       
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