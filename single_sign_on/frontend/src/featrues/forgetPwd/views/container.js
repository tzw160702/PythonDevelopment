/**
 * @Description:
 * @author Chen
 * @date 2021-03-11 16:22
 */
import React, {useEffect} from "react";
import Grid from "@material-ui/core/Grid";
import {Paper} from "@material-ui/core";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from '@material-ui/icons/Close';

import Input from "../../../components/CustomInput/Input";
import Button from "../../../components/CustomButton/Button";
import axios from "axios";
import config from "../../../assets/config/config.json";
import {isEmail, isPhoneNumber} from "../../../util/validation";

const useStyles = makeStyles((theme) => ({
    paper: {
        // marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        minWidth: 330,
        padding: theme.spacing(2)
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
    button: {
        margin: theme.spacing(2, 2, 2, 5),
        width: theme.spacing(15),
        height: theme.spacing(7)
    },
    grid: {
        minWidth: 310
    }
}));

export default function ForgetPwd(props) {
    const classes = useStyles();

    const [number, setNumber] = React.useState('');//手机号
    const [numberHelperText, setNumberHelperText] = React.useState('');//手机号输入框提示文字
    const [numberError, setNumberError] = React.useState(false);//手机号输入框是否为error状态

    const [password, setPassword] = React.useState('');//密码
    const [passwordHelperText, setPasswordHelperText] = React.useState('');//密码输入框提示文字
    const [passwordError, setPasswordError] = React.useState(false);//密码输入框是否为error状态

    const [code, setCode] = React.useState('');//验证码
    const [codeHelperText, setCodeHelperText] = React.useState('');//验证码输入框提示文字
    const [codeError, setCodeError] = React.useState(false);//验证码输入框是否为error状态

    const [passwordRetry, setPasswordRetry] = React.useState('');//密码确认
    const [passwordRetryHelperText, setPasswordRetryHelperText] = React.useState('');//密码确认输入框帮助文字
    const [passwordRetryError, setPasswordRetryError] = React.useState(false);//密码确认输入框错误状态

    const [saveCodeButtonText, setSaveCodeButtonText] = React.useState('发送验证码');//发送验证码按钮文字
    const [saveCodeButtonDisable, setSaveCodeButtonDisable] = React.useState(false);//发送验证码按钮是否禁用
    //忘记密码页面关闭
    const handleForgetPwdClose = () => {
        props.handleForgetPwdChange(false);
        numberStatusChange(false, '');
        pwdStatusChange(false, '');
        pwdRetryStatusChange(false, '');
        codeStatusChange(false, '');
    }
    //手机号输入框值改变
    const handleNumberChange = (event) => {
        const number = event.target.value;//输入框值
        setNumber(number)
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
    //密码输入框值改变 验证密码长度
    const handlePasswordChange = (event) => {
        const pwd = event.target.value;
        setPassword(pwd)
        if (pwd.length < 6 || pwd.length > 20 || pwd === '' || pwd == null) {//验证密码长度是否在6到20之间
            pwdStatusChange(true, '请输入6到20位的密码');
        } else {
            pwdStatusChange(false, '');
        }

    }
    //密码确认框输入值改变,验证两次输入密码是否一样
    const handlePasswordRetryChange = (event) => {
        const pwd = event.target.value
        setPasswordRetry(pwd);
        if (pwd !== password) {
            pwdRetryStatusChange(true, '两次密码输入不一致');
        } else {
            pwdRetryStatusChange(false, '');
        }
    }
    //验证码输入框值改变 验证验证码是否为空
    const handleCodeChange = (event) => {
        const code = event.target.value;
        setCode(code)
        if (code === '' || code === null) {//判断验证码为空
            codeStatusChange(true, '请输入验证码');
        } else {
            codeStatusChange(false, '');
        }
    }
    //获取验证码按钮点击事件
    const handleSaveCodeButtonClick = () => {
        if (isPhoneNumber(number) || isEmail(number)) {
            axios({
                url: config.ip + "/code/verify_code",
                method: "POST",
                params: {
                    number: number
                }
            })

            //密码发送成功后禁用发送验证码按钮
            // 还不完善,需要添加,没有做出判断是否是已经发送成功
            let time = parseInt(new Date().getTime() / 1000);//当前时间戳
            localStorage.setItem('forgetPwdTime', time);//将当前时间设置到本地缓存中

            saveCodeButtonRemainingTime(time, time);
        } else {
            numberStatusChange(true, '请先填写正确的手机号或邮箱')
        }


    }
    useEffect(() => {
        let lastClickTime = localStorage.getItem('forgetPwdTime');//获取忘记密码页面发送验证码按钮上次点击时间戳
        let time = parseInt(new Date().getTime() / 1000);//当前时间戳
        if (time - lastClickTime >= 60) {
            setSaveCodeButtonDisable(false);
            setSaveCodeButtonText('发送验证码');
        } else {
            saveCodeButtonRemainingTime(time, lastClickTime);
        }
    }, [])
    //重置密码按钮点击事件
    const handleResetPwdButtonClick = () => {
        const infoStatus = infoValidation(number, password, passwordRetry, code);
        if (infoStatus) {
            axios({
                url: config.ip + "/users/verify_code_password",
                method: "PATCH",
                data: JSON.stringify({
                    number: number,
                    pwd: password,
                    verify_code: code
                })
            })
        }
    }
    //发送验证码时间验证
    const saveCodeButtonRemainingTime = (time, lastClickTime) => {
        setSaveCodeButtonDisable(true);
        let RemainingTime = 60 - (time - lastClickTime);//剩余时间
        setSaveCodeButtonText(RemainingTime + 's后重新发送')
        let forgetPwdClock = setInterval(() => {
            let lastClickTime = localStorage.getItem('forgetPwdTime');
            let time = parseInt(new Date().getTime() / 1000);//当前时间戳
            let RemainingTime = 60 - (time - lastClickTime);//剩余时间
            setSaveCodeButtonText(RemainingTime + 's后重新发送')
            if (RemainingTime <= 0) {
                clearInterval(forgetPwdClock);
                setSaveCodeButtonText('重新发送验证码');
                setSaveCodeButtonDisable(false);
            }
        }, 1000);
    }

    //信息验证
    const infoValidation = (number, pwd, pwdRetry, code) => {
        if (isPhoneNumber(number) || isEmail(number)) {//number是手机号或邮箱
            if (pwd.length >= 6 && pwd.length <= 20 && pwd !== '' && pwd != null) {//密码不为空，长度在6到20位
                if (passwordRetry === password) {
                    if (code !== '' || code !== null) {//验证码不为空
                        return true;
                    } else {
                        codeStatusChange(true, '请输入验证码');
                        return false;
                    }
                } else {
                    pwdRetryStatusChange(true, '两次密码输入不一致');
                    if (code === '' || code === null) {
                        codeStatusChange(true, '请输入验证码');
                    }
                    return false;
                }
            } else {
                pwdStatusChange(true, '请输入6到20位的密码');
                pwdRetryStatusChange(true, '两次密码输入不一致');
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
            if (passwordRetry !== password) {
                pwdRetryStatusChange(true, '两次密码输入不一致');
            }
            console.log(code)
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
    //密码确认输入框状态及帮助文字设置
    const pwdRetryStatusChange = (status, helperText) => {
        setPasswordRetryError(status);
        setPasswordRetryHelperText(helperText);
    }
    //验证码输入框状态及帮助文字设置
    const codeStatusChange = (status, helperText) => {
        setCodeError(status);
        setCodeHelperText(helperText);
    }
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline/>
            <Paper className={classes.paper}>
                <Grid container className={classes.grid}>
                    <Grid container justify="space-between">
                        <Grid item>
                            <Typography component="h1" variant="h4">
                                忘记密码？
                            </Typography>
                            <Typography variant="body2">
                                您可以使用验证码来重置密码
                            </Typography>
                        </Grid>
                        <Grid>
                            <IconButton onClick={handleForgetPwdClose}>
                                <CloseIcon/>
                            </IconButton>
                        </Grid>
                    </Grid>
                    <Grid container className={classes.form}>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Input
                                    id="phone"
                                    name="phone"
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="手机号\邮箱"
                                    value={number}
                                    onChange={handleNumberChange}
                                    helperText={numberHelperText}
                                    error={numberError}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <Input
                                    id="password"
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="新密码"
                                    type="password"
                                    name="password"
                                    value={password}
                                    onChange={handlePasswordChange}
                                    helperText={passwordHelperText}
                                    error={passwordError}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <Input
                                    id="passwordRetry"
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="密码确认"
                                    type="password"
                                    name="passwordRetry"
                                    value={passwordRetry}
                                    onChange={handlePasswordRetryChange}
                                    helperText={passwordRetryHelperText}
                                    error={passwordRetryError}
                                />
                            </Grid>
                            <Grid container item xs={12}>
                                <Grid item xs={5} sm={6}>
                                    <Input
                                        variant="outlined"
                                        required
                                        name="code"
                                        label="验证码"
                                        id="code"
                                        value={code}
                                        onChange={handleCodeChange}
                                        helperText={codeHelperText}
                                        error={codeError}
                                    />
                                </Grid>
                                <Grid item>
                                    <Button
                                        className={classes.button}
                                        onClick={handleSaveCodeButtonClick}
                                        disable={saveCodeButtonDisable}
                                    >
                                        {saveCodeButtonText}
                                    </Button>
                                </Grid>
                            </Grid>
                        </Grid>
                        <Button
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                            onClick={handleResetPwdButtonClick}
                        >
                            重置密码
                        </Button>
                    </Grid>
                </Grid>
            </Paper>
        </Container>
    )
}