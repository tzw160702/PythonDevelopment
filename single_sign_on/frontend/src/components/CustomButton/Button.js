/**
 * @Description:
 * @author Chen
 * @date 2021-03-08 10:40
 */
import React from "react";
import Button from "@material-ui/core/Button";

export default function RegularButton(props) {
    const {id, children, size, variant, color, onClick, fullWidth, className, disable} = props;
    return (
        <Button
            id={id}
            size={size ? size : 'medium'}
            variant={variant ? variant : 'outlined'}
            color={color ? color : 'primary'}
            onClick={onClick}
            fullWidth={fullWidth}
            className={className}
            disabled={disable}
        >
            {children ? children : 'Button'}
        </Button>
    )
}