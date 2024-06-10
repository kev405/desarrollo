import { ref } from 'vue'
import axios from 'axios'

export const useAxios = () => {
  const resultRequest = ref(null)

  const makeRequest = async (url, method, params) => {
    try {
      const request = await axios({
        method: method,
        url: url,
        data: params,
        responseType: 'json'
      })

      resultRequest.value = request.data
    } catch (error) {
      console.log(error);
    }
  }

  const empty = (str) => {
    return (
      typeof str === typeof undefined ||
      str == null ||
      str == '' ||
      str == 0 ||
      (Array.isArray(str) && str.length === 0) ||
      (typeof str === 'object' && Object.keys(str).length === 0)
    )
  }

  return {
    makeRequest,
    resultRequest,
    empty,
  }
}