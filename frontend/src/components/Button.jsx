import React from "react";

const Button = ({ onClick, disabled, tooltip, ...props }) => {
    return <button onClick={onClick} >{props.children}</button>
}

export default Button