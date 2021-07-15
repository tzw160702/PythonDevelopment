/**
 * @Description:
 * @author Chen
 * @date 2021-03-18 09:54
 */
import {decrypt} from './jsencryptUtil'
import config from "../assets/config/config.json";

export default function notify(notifyPage, notifyUrl) {
    let notifyPageUrl;//第三方页面回调地址
    let notifyBackendUrl;//第三方后台回调地址
    if (notifyPage === 'local') {
        notifyPageUrl = localStorage.getItem('notifyPageUrl');
    } else {
        notifyPageUrl = decrypt(notifyPage, config.privateKey);
        localStorage.setItem('notifyPageUrl', notifyPageUrl)
    }

    if (notifyUrl === 'local') {
        notifyBackendUrl = localStorage.getItem('notifyBackendUrl');
    } else {
        notifyBackendUrl = decrypt(notifyUrl, config.privateKey);
        localStorage.setItem('notifyBackendUrl', notifyBackendUrl)
    }
    return {notifyPageUrl,notifyBackendUrl}
}