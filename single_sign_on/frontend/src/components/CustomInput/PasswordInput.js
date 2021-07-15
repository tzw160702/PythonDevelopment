/**
 * @Description:
 * @author Chen
 * @date 2021-03-08 17:50
 */
import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import OutlinedInput from '@material-ui/core/FilledInput';
import InputAdornment from "@material-ui/core/InputAdornment";
import IconButton from "@material-ui/core/IconButton";
import Visibility from "@material-ui/icons/Visibility";
import VisibilityOff from "@material-ui/icons/VisibilityOff";
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    margin: {
        margin: theme.spacing(1),
    },
    withoutLabel: {
        marginTop: theme.spacing(3),
    },
    textField: {
        width: '25ch',
    },
}));

export default function Input(props) {
    const classes = useStyles();
    const {id, label, variant, onChange, helperText, color, fullWidth, margin, required, name, type, onClick, onMouseDown, showPassword} = props;
    return (
        <FormControl className={classes.margin} variant={'variant'}>
            <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
            <OutlinedInput
                id={'outlined-adornment-password'} label={label ? label : '标题'} margin={margin ? margin : 'normal'} type={type ? type : 'text'}
                color={color ? color : 'secondary'} fullWidth={fullWidth} variant={variant} onChange={onChange}
                helperText={helperText} required={required} autoComplete="email" name={name} endAdornment={
                <InputAdornment position="end">
                    <IconButton
                        aria-label="toggle password visibility"
                        onClick={onClick}
                        onMouseDown={onMouseDown}
                    >
                        {showPassword ? <Visibility/> : <VisibilityOff/>}
                    </IconButton>
                </InputAdornment>
            }
            />
        </FormControl>

    )
}