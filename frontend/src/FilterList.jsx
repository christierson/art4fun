import React, { useEffect, useState } from "react";
import { List, useList } from "./components/List";
import Button from "./components/Button";
import Checkbox from "./components/Checkbox";

const FilterList = ({ filters, submitFilters, onlyComplete, setOnlyComplete }) => {
    const listProps = useList({ collection: filters, update: submitFilters })

    const [text, setText] = useState("")

    const onChange = (e) => {
        setText(e.target.value)
    }

    const addNewFilter = () => {
        if (!text || text == "")
            return
        submitFilters(filters.union(new Set([text])))
        setText("")
    }

    return <div className="flex flex-col gap-5">
        <List {...listProps} />
        <div className="flex flex-row gap-2">
            <input type="text" className="bg-white rounded px-3 text-black" onChange={onChange} value={text} />
            <Button onClick={addNewFilter}>Add filter</Button>
        </div>
        <div className="flex flex-row gap-5 items-center">
            <Checkbox value={onlyComplete} setValue={setOnlyComplete} />
            Only complete rows
        </div>
    </div>
}


export default FilterList