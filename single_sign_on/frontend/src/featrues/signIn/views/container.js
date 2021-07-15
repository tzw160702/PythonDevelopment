import React, {useEffect} from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import axios from "axios";

import Input from '../../../components/CustomInput/Input'
import Button from '../../../components/CustomButton/Button'
import codeImg from '../../../assets/img/验证码.png'
import config from '../../../assets/config/config.json'
import {isPhoneNumber, isEmail} from '../../../util/validation'
import Snackbar from "../../../components/Snackbar/Snackbar";
import {AddAlert} from "@material-ui/icons";

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        minWidth: 310
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    button: {
        margin: theme.spacing(3, 0, 2),
    },
    img: {
        width: theme.spacing(19),
        height: theme.spacing(7),
        margin: theme.spacing(2, 0, 0, 3.5)
    },
}));

export default function SignIn(props) {
    const classes = useStyles();

    useEffect(() => {
        //页面渲染时获取验证码
        saveClientCode()
    }, [])

    const {onForgetPwdChange, number, setNumber, rememberMeValue, setRememberMeValue, notifyPageUrl, notifyBackendUrl} = props;

    const [numberHelperText, setNumberHelperText] = React.useState('');//手机号输入框提示文字
    const [numberError, setNumberError] = React.useState(false);//手机号输入框是否为error状态

    const [password, setPassword] = React.useState('');//密码
    const [passwordHelperText, setPasswordHelperText] = React.useState('');//密码输入框提示文字
    const [passwordError, setPasswordError] = React.useState(false);//密码输入框是否为error状态

    const [code, setCode] = React.useState('');//验证码
    const [codeHelperText, setCodeHelperText] = React.useState('');//验证码输入框提示文字
    const [codeError, setCodeError] = React.useState(false);//验证码输入框是否为error状态

    const [dialogOpen, setDialogOpen] = React.useState(false);//登录异常时是否显示错误提示框
    const [errMessage, setErrMessage] = React.useState("");//登录异常时候错误提示框显示的提示信息

    //记住我按钮点击
    const handleRememberMeClick = () => {
        setRememberMeValue(!rememberMeValue);
    };
    //手机号输入框值改变，验证手机号
    const handleNumberChange = (event) => {
        const number = event.target.value;//输入框值
        setNumber(number);
        const isPhone = isPhoneNumber(number);//是否为手机号
        const isE_mail = isEmail(number);//是否为邮箱
        if (isPhone) {//是手机号
            numberStatusChange(false, '');
        } else if (isE_mail) {//是邮箱
            numberStatusChange(false, '');
        } else {//不是邮箱也不是手机号
            numberStatusChange(true, '请输入正确的手机号或邮箱');
        }
    }
    //密码输入框值改变,保存数据并验证密码长度
    const handlePasswordChange = (event) => {
        const pwd = event.target.value;
        setPassword(pwd);
        if (pwd.length < 6 || pwd.length > 20 || pwd === '' || pwd == null) {//验证密码长度是否在6到20之间
            pwdStatusChange(true, '请输入6到20位的密码');
        } else {
            pwdStatusChange(false, '');
        }
    }
    //验证码输入框值改变，保存数据并验证验证码
    const handleCodeChange = (event) => {
        const code = event.target.value;
        setCode(code);
        if (code === '' || code === null) {//判断验证码为空
            codeStatusChange(true, '请输入验证码');
        } else {
            codeStatusChange(false, '');
        }
    }

    /* 设置提示框的显示、隐藏、过期时间*/
    const flagSnackbar = (messages) =>{
        if(!dialogOpen){
            setDialogOpen(true)
            setErrMessage(messages)
            setTimeout(function() {
                setDialogOpen(false);
                setErrMessage("")
            }, 4000);
        }
    }

    //登陆按钮点击
    const handleSignInButtonClick = () => {
        const infoStatus = infoValidation(number, password, code);
        if (infoStatus) {
            axios({
                url: config.ip + '/users/singin',
                method: 'POST',
                data: JSON.stringify({
                    "number": number,
                    "pwd": password,
                    "client_code": code,
                    "callback_url": notifyBackendUrl
                })
            })
                .then((result) => {

                    console.log(result)
                    // 登陆后跳转第三方页面
                    if (result.data.status===200){
                        // console.log('跳转')
                        window.location.href = notifyPageUrl + '/' + result.data.token;
                    }else{
                       flagSnackbar(result.data.message)
                    }
                })
                /*  拿到错误信息并提示用户 */
                .catch(() => {
                    flagSnackbar("网络异常")
                })
        }
    }
    //打开忘记密码页面
    const handleForgetPwdOpen = () => {
        onForgetPwdChange(true);
    }
    //获取验证码
    const saveClientCode = () => {
        axios({
            url: config.ip + "/code/client_code",
            method: "GET"
        })
            .then((result) => {
                console.log(result.data)
            })
    }
    //登陆信息验证
    const infoValidation = (number, pwd, code) => {
        if (isPhoneNumber(number) || isEmail(number)) {//number是手机号或邮箱
            if (pwd.length >= 6 && pwd.length <= 20 && pwd !== '' && pwd != null) {//密码不为空，长度在6到20位
                if (code !== '' && code !== null) {//验证码不为空
                    return true;
                } else {
                    codeStatusChange(true, '请输入验证码');
                    return false;
                }
            } else {
                pwdStatusChange(true, '请输入6到20位的密码');
                if (code === '' || code === null) {
                    codeStatusChange(true, '请输入验证码');
                }
                return false;
            }
        } else {
            numberStatusChange(true, '请输入正确的手机号或邮箱');
            if (pwd.length < 6 || pwd.length > 20 || pwd === '' || pwd == null) {
                pwdStatusChange(true, '请输入6到20位的密码');
            }
            if (code === '' || code === null) {
                codeStatusChange(true, '请输入验证码');
            }
            return false;
        }
    }
    //手机号码输入框状态及帮助文字设置 status:输入框状态 helperText：输入框下帮助文字
    const numberStatusChange = (status, helperText) => {
        setNumberError(status);
        setNumberHelperText(helperText);
    }
    //密码输入框状态及帮助文字设置
    const pwdStatusChange = (status, helperText) => {
        setPasswordError(status);
        setPasswordHelperText(helperText);
    }
    //验证码输入框状态及帮助文字设置
    const codeStatusChange = (status, helperText) => {
        setCodeError(status);
        setCodeHelperText(helperText);
    }
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline/>
            <Grid container className={classes.paper}>

                {/*  注册失败提示组件*/}
                <Grid item >
                    <Snackbar
                        place="tc"
                        color="info"
                        icon={AddAlert}
                        message={errMessage}
                        open={dialogOpen}
                        closeNotification={() => setDialogOpen(false)}
                        close
                    />
                </Grid>

                <Grid item>
                    <Typography component="h1" variant="h5">
                        密码登陆 / <Link href="/#/signInWithCode/local/local" variant="body2"> 验证码登陆 </Link>
                    </Typography>
                </Grid>
                <Grid item container className={classes.form}>
                    <Grid item xs={12}>
                        <Input
                            id={'number'}
                            label="手机号\邮箱"
                            name={'phone'}
                            variant="outlined"
                            fullWidth={true}
                            required={true}
                            value={number}
                            onChange={handleNumberChange}
                            helperText={numberHelperText}
                            error={numberError}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Input
                            id={'password'}
                            label="密码"
                            name={'password'}
                            variant="outlined"
                            fullWidth={true}
                            required={true}
                            type={'password'}
                            value={password}
                            onChange={handlePasswordChange}
                            helperText={passwordHelperText}
                            error={passwordError}
                        />
                    </Grid>
                    <Grid container item>
                        <Grid item xs={5} sm={6}>
                            <Input
                                id={'code'}
                                label="验证码"
                                name={'code'}
                                variant="outlined"
                                required={true}
                                value={code}
                                onChange={handleCodeChange}
                                helperText={codeHelperText}
                                error={codeError}
                                // onBlur={handleCodeBlur}
                            />
                        </Grid>
                        <Grid item>
                            <img alt={'验证码'} src={codeImg} onClick={saveClientCode} className={classes.img}/>
                        </Grid>
                    </Grid>
                    <Grid item>
                        <Checkbox checked={rememberMeValue} onClick={handleRememberMeClick} color="secondary"/>记住我
                    </Grid>
                    <Button
                        fullWidth={true}
                        variant="contained"
                        className={classes.button}
                        onClick={handleSignInButtonClick}
                    >
                        登陆
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="/#/" onClick={handleForgetPwdOpen} variant="body2">
                                忘记密码?
                            </Link>
                        </Grid>
                        <Grid item>
                            还没有账号？<Link href="/#/signUp/local/local" variant="body2">去注册</Link>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Container>
    );
}