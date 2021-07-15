/**
 * @Description:
 * @author Chen
 * @date 2021-03-08 09:27
 */
import React from "react";
import Grid from "@material-ui/core/Grid";

import SignIn from '../featrues/signIn';
import saveNotify from '../util/saveNotify'

export default function SignInPage(props) {
    const {onForgetPwdChange, number, setNumber, rememberMeValue, setRememberMeValue, notifyPage, notifyUrl} = props;
    const {notifyPageUrl,notifyBackendUrl} = saveNotify(notifyPage,notifyUrl);
    return (
        <Grid container>
            <SignIn
                onForgetPwdChange={onForgetPwdChange}
                number={number}
                setNumber={setNumber}
                rememberMeValue={rememberMeValue}
                setRememberMeValue={setRememberMeValue}
                notifyPageUrl={notifyPageUrl}
                notifyBackendUrl={notifyBackendUrl}
            />
        </Grid>
    )
}