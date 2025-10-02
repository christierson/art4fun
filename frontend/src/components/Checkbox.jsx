import React from "react";

const Checkbox = ({ value, setValue }) => {
    const onChange = (e) => {
        setValue(e.target.checked)
    }
    return <div>
        <input type="checkbox" className="w-6 h-6 rounded-md" checked={value} onChange={onChange} />
    </div>
}

export default Checkbox