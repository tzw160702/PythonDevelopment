/**
 * @Description:
 * @author Chen
 * @date 2021-03-08 11:10
 */
import React from "react";

import TextField from "@material-ui/core/TextField";

export default function Input(props) {
    const {
        id,
        label,
        variant,
        onChange,
        helperText,
        color,
        fullWidth,
        margin,
        required,
        name,
        type,
        onBlur,
        value,
        error,
    } = props;
    return (
        <TextField id={id} label={label ? label : '标题'} margin={margin ? margin : 'normal'} type={type ? type : 'text'}
                   color={color} fullWidth={fullWidth} variant={variant} onChange={onChange}
                   helperText={helperText} required={required} autoComplete="email" name={name} onBlur={onBlur}
                   value={value} error={error}/>
    )
}