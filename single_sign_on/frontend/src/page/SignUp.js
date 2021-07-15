/**
 * @Description:
 * @author Chen
 * @date 2021-03-09 11:14
 */
import React from "react";
import Grid from "@material-ui/core/Grid";

import SignUp from "../featrues/signUp";
import saveNotify from "../util/saveNotify";

export default function SignUpPage(props) {
    const {notifyPage,notifyUrl} = props;
    const {notifyPageUrl,notifyBackendUrl} = saveNotify(notifyPage,notifyUrl);
    return(
        <Grid container>
            <SignUp
                notifyPageUrl={notifyPageUrl}
                notifyBackendUrl={notifyBackendUrl}
            />
        </Grid>
    )
}