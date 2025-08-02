import React, { useEffect, useRef, useState } from "react";
import request from "../utils/api";
import Button from "./Button";
import axios from "axios";
const FileSelect = ({ setFile }) => {
    const fileSelect = useRef()
    const [fileName, setFileName] = useState("No file selected")

    const onChange = async (e) => {
        e.preventDefault();
        const file = e.target.files[0]
        setFileName(file.name)
        setFile(file)


    };

    const open = () => {
        fileSelect.current.click()
    }

    return (
        <div className="flex flex-col gap-3">
            {fileName}
            <input type="file" id="file" ref={fileSelect} onChange={onChange} className="hidden" />
            <Button onClick={open} >Select file</Button>
        </div>
    );
};
export default FileSelect