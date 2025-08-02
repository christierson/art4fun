import React from "react";

const Panel = ({ title, ...props }) => {
    return <div className="bg-slate-400 rounded-md shadow-lg p-5">{props.children}</div>
}

export default Panel