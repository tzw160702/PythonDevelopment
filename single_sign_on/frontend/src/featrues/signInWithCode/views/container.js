/**
 * @Description:
 * @author Chen
 * @date 2021-03-11 11:52
 */
import React, {useEffect} from "react";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";
import Input from "../../../components/CustomInput/Input";
import Checkbox from "@material-ui/core/Checkbox";
import Button from "../../../components/CustomButton/Button";
import Container from "@material-ui/core/Container";
import {makeStyles} from "@material-ui/core/styles";
import axios from "axios";
import config from "../../../assets/config/config.json";
import {isEmail, isPhoneNumber} from "../../../util/validation";
import {AddAlert} from "@material-ui/icons";
import Snackbar from "../../../components/Snackbar/Snackbar";

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
    codeButton: {
        margin: theme.spacing(2, 2, 2, 5),
        width: theme.spacing(15),
        height: theme.spacing(7)
    }
}));

export default function SignInWithCode(props) {
    const classes = useStyles();

    const {onForgetPwdChange, number, setNumber, rememberMeValue, setRememberMeValue, notifyPageUrl, notifyBackendUrl} = props;

    const [numberHelperText, setNumberHelperText] = React.useState('');//手机号输入框提示文字
    const [numberError, setNumberError] = React.useState(false);//手机号输入框是否为error状态
    const [code, setCode] = React.useState('');//验证码
    const [codeHelperText, setCodeHelperText] = React.useState('');//验证码输入框提示文字
    const [codeError, setCodeError] = React.useState(false);//验证码输入框是否为error状态

    const [saveCodeButtonText, setSaveCodeButtonText] = React.useState('发送验证码');//发送验证码按钮文字
    const [saveCodeButtonDisable, setSaveCodeButtonDisable] = React.useState(false);//发送验证码按钮是否禁用

    const [dialogOpen, setDialogOpen] = React.useState(false);//登录异常时候显示错误提示框
    const [errMessage, setErrMessage] = React.useState("");//登录异常时候错误提示框显示的提示信息

    //打开忘记密码页面
    const handleForgetPwdOpen = () => {
        onForgetPwdChange(true)
    }
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
    //验证码输入框值改变，验证验证码是否为空
    const handleCodeChange = (event) => {
        const code = event.target.value;
        setCode(code);
        if (code === '' || code === null) {//判断验证码为空
            codeStatusChange(true, '请输入验证码');
        } else {
            codeStatusChange(false, '');
        }
    }
    //获取验证码按钮点击事件
    const handleSaveCodeButtonClick = () => {
        console.log('进入方法')
        if (isPhoneNumber(number) || isEmail(number)) {
            // numberStatusChange(false,'')
            console.log('验证是手机号或邮箱')
            axios({
                url: config.ip + "/code/verify_code",
                method: "POST",
                params: {
                    number: number
                }
            })
            let time = parseInt(new Date().getTime() / 1000);//当前时间戳
            localStorage.setItem('signInTime', time);//将当前时间设置到本地缓存中
            saveCodeButtonRemainingTime(time, time);
        } else {
            console.log('不符')
            numberStatusChange(true, '请先填写正确的手机号或邮箱')
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

    //登陆按钮点击事件
    const handleSignInButtonClick = () => {
        console.log('点击事件')
        const infoStatus = infoValidation(number, code);
        console.log(infoStatus)
        if (infoStatus) {
            axios({
                url: config.ip + "/users/signin/verifycode",
                method: "POST",
                data: JSON.stringify({
                    number: number,
                    verify_code: code,
                    callback_url: notifyBackendUrl
                })
            })
                .then((result) => {
                    // 登陆后跳转第三方页面
                    if(result.data.status === 200){
                        window.location.href = notifyPageUrl + '/' + result.data.token;
                    }else {
                        flagSnackbar(result.data.message)
                    }

                })
                .catch(()=>{
                    flagSnackbar("网络异常")
                })
        }
    }
    //发送验证码时间验证
    const saveCodeButtonRemainingTime = (time, lastClickTime) => {
        setSaveCodeButtonDisable(true);
        let RemainingTime = 60 - (time - lastClickTime);//剩余时间
        setSaveCodeButtonText(RemainingTime + 's后重新发送')
        let signInClock = setInterval(() => {
            let lastClickTime = localStorage.getItem('signInTime');
            let time = parseInt(new Date().getTime() / 1000);//当前时间戳
            let RemainingTime = 60 - (time - lastClickTime);//剩余时间
            setSaveCodeButtonText(RemainingTime + 's后重新发送')
            if (RemainingTime <= 0) {
                clearInterval(signInClock);
                setSaveCodeButtonText('重新发送验证码');
                setSaveCodeButtonDisable(false);
            }
        }, 1000);
    }
    //登陆信息验证
    const infoValidation = (number, code) => {
        if (isPhoneNumber(number) || isEmail(number)) {//number是手机号或邮箱
            if (code !== '' || code !== null) {//验证码不为空
                return true;
            } else {
                codeStatusChange(true, '请输入验证码');
                return false;
            }
        } else {
            numberStatusChange(true, '请输入正确的手机号或邮箱');
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
    //验证码输入框状态及帮助文字设置
    const codeStatusChange = (status, helperText) => {
        setCodeError(status);
        setCodeHelperText(helperText);
    }
    useEffect(() => {
        let lastClickTime = localStorage.getItem('signInTime');//获取忘记密码页面发送验证码按钮上次点击时间戳
        let time = parseInt(new Date().getTime() / 1000);//当前时间戳
        if (time - lastClickTime >= 60) {
            setSaveCodeButtonDisable(false);
            setSaveCodeButtonText('发送验证码');
        } else {
            saveCodeButtonRemainingTime(time, lastClickTime);
        }
    }, [])
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline/>

            <Grid container className={classes.paper}>

                {/* 登录失败的弹出框 */}
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
                        验证码登陆 / <Link href="/#/signIn/local/local" variant="body2">
                        密码登陆
                    </Link>
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
                            error={numberError}/>
                    </Grid>
                    <Grid container item xs={12}>
                        <Grid item xs={5} sm={6}>
                            <Input
                                variant="outlined"
                                required name="code"
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
                                className={classes.codeButton}
                                onClick={handleSaveCodeButtonClick}
                                disable={saveCodeButtonDisable}
                            >
                                {saveCodeButtonText}
                            </Button>
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
                            <Link href="/#/signInWithCode" onClick={handleForgetPwdOpen} variant="body2">
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
    )
}