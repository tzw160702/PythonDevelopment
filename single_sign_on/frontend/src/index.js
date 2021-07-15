/**
 * @Description:
 * @author Chen
 * @date 2021-03-08 09:27
 */
import React from 'react';
import ReactDOM from 'react-dom';
import {HashRouter, Route} from "react-router-dom";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import {ThemeProvider} from "@material-ui/styles";
import {createMuiTheme} from "@material-ui/core/styles";
import {purple} from "@material-ui/core/colors";
import Backdrop from "@material-ui/core/Backdrop";

import {makeStyles} from '@material-ui/core/styles';

import SignIn from './page/SignIn'
import SignUp from './page/SignUp'
import SignInWithCode from "./page/SignInWithCode";
import ForgetPwd from "./featrues/forgetPwd";
// import {decrypt, encrypt} from './util/jsencryptUtil'
// import config from './assets/config/config.json'
import saveNotify from "./util/saveNotify";

const useStyles = makeStyles((theme) => ({
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
    },
}));

const theme = createMuiTheme({
    palette: {
        primary: {
            // Purple and green play nicely together.
            main: purple[500],
        }
    },
});

function PageRouter() {
    const classes = useStyles();

    const [forgetPwdOpen, setForgetPwdOpen] = React.useState(false);//忘记密码背景板是否显示

    const [rememberMeValue, setRememberMeValue] = React.useState(false);//是否记住登陆(一直保持登陆状态)

    const [number, setNumber] = React.useState('');//手机号

    const handleForgetPwdChange = (val) => {
        setForgetPwdOpen(val)
    }

    return (
        <ThemeProvider theme={theme}>
            <Container maxWidth={"xl"}>
                <CssBaseline/>
                <HashRouter>
                    <Route
                        path={'/signIn/:notifyPage/:notifyUrl'}
                        render={(props) => {
                            const {notifyPage, notifyUrl} = saveUrl(props);
                            return <SignIn
                                onForgetPwdChange={handleForgetPwdChange}
                                number={number}
                                setNumber={setNumber}
                                rememberMeValue={rememberMeValue}
                                setRememberMeValue={setRememberMeValue}
                                notifyPage={notifyPage}
                                notifyUrl={notifyUrl}
                            />
                        }}
                        exact
                    />
                    <Route
                        path={'/signInWithCode/:notifyPage/:notifyUrl'}
                        render={(props) => {
                            const {notifyPage, notifyUrl} = saveUrl(props);
                            return <SignInWithCode
                                onForgetPwdChange={handleForgetPwdChange}
                                number={number}
                                setNumber={setNumber}
                                rememberMeValue={rememberMeValue}
                                setRememberMeValue={setRememberMeValue}
                                notifyPage={notifyPage}
                                notifyUrl={notifyUrl}
                            />
                        }}
                        exact
                    />
                    <Route
                        path={'/signUp/:notifyPage/:notifyUrl'}
                        render={(props) => {
                            const {notifyPage, notifyUrl} = saveUrl(props);
                            return <SignUp
                                notifyPage={notifyPage}
                                notifyUrl={notifyUrl}
                            />
                        }}
                        exact
                    />
                    <Route
                        path={'/test/:notifyPage/:notifyUrl'}
                        render={(props) => {
                            const {notifyPage, notifyUrl} = saveUrl(props);
                            return <Test notifyPage={notifyPage} notifyUrl={notifyUrl}/>
                        }} exact
                    />
                </HashRouter>
                <Backdrop open={forgetPwdOpen} className={classes.backdrop}>
                    <ForgetPwd handleForgetPwdChange={handleForgetPwdChange}/>
                </Backdrop>
            </Container>
        </ThemeProvider>

    )
}

//测试用
function Test(props) {
    // let jsEncryptData = encrypt('你好', config.publicKey);
    // console.log(jsEncryptData)
    // let decryptData = decrypt(jsEncryptData, config.privateKey);
    // console.log(decryptData)
    // let jsEncryptData1 = encrypt('回调', config.publicKey);
    // console.log(jsEncryptData1)
    // let decryptData1 = decrypt(jsEncryptData1, config.privateKey);
    // console.log(decryptData1)
    const {notifyPage, notifyUrl} = props;
    const {notifyPageUrl, notifyBackendUrl} = saveNotify(notifyPage, notifyUrl);
    console.log(notifyPageUrl)
    console.log(notifyBackendUrl)
    return (
        <div>123</div>
    );
}

//获取url
function saveUrl(props) {
    const notifyPage = props.match.params.notifyPage;//回调页面
    const notifyUrl = props.match.params.notifyUrl;//回调地址
    return {notifyPage, notifyUrl}
}

ReactDOM.render(
    <PageRouter/>,
    document.getElementById('root')
);
