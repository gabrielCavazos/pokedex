
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const notify = (weight_average, height_average, count) => {
    toast(`Favorite data: avg weight:${weight_average} avg height:${height_average} count:${count}`)
  };
  
const notifyError = (weight_average, height_average, count) => {
    toast(`Oops something went wrong, verify you internet conection and retry please`)
};

export {notify, notifyError}