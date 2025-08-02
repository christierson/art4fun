import axios from 'axios';

const Request = () => {
    const get = ({ url }) => {
        return axios.get(url)
    }
    const post = ({ url, data }) => {
        return axios.post(url, data)
    }

    return { get, post }
}

const request = Request()

export default request