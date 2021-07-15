/**
 * @Description:
 * @author Chen
 * @date 2021-03-11 09:33
 */
import React from "react";
import Grid from "@material-ui/core/Grid";

import SignInWithCode from "../featrues/signInWithCode";
import saveNotify from "../util/saveNotify";

export default function SignInWithCodePage(props) {
    const {onForgetPwdChange, number, setNumber, rememberMeValue, setRememberMeValue,notifyPage,notifyUrl} = props;
    const {notifyPageUrl,notifyBackendUrl} = saveNotify(notifyPage,notifyUrl);
    return (
        <Grid container>
            <SignInWithCode
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