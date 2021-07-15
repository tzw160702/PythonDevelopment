/**
 * @Description:
 * @author Chen
 * @date 2020-11-23 13:40
 */

import JSEncrypt from 'encryptlong/bin/jsencrypt.min'
function encrypt(data, publicKey) {
    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(publicKey);//设置加密公钥
    data = encrypt.encryptLong(JSON.stringify(data));//加密data
    data = data.replace(/\//g, '_');//替换特殊字符
    return data;
}
function decrypt(data, privateKey) {
    let decrypt = new JSEncrypt();
    //设置解密私钥
    decrypt.setPrivateKey(privateKey);
    //替换特殊字符
    data = data.replace(/_/g, '/');//替换密文中的特殊字符
    data = decrypt.decryptLong(data);//解密
    if(data.indexOf('"')===0){
        data=data.substring(1,data.length)
    }
    if(data.indexOf('"')===data.length-1){
        data=data.substring(0,data.length-1)
    }
    return data;
}
export {encrypt,decrypt}