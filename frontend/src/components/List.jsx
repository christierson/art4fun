import React, { useEffect, useState } from "react";
import Button from "./Button";
export const useList = ({ collection, update }) => {
    const [items, setItems] = useState(new Set([]))

    useEffect(() => {
        setItems(new Set([...collection]))
    }, [collection])

    const removeItem = (item) => {
        const updated = items.difference(new Set([item]))
        setItems(updated)
        update(updated)

    }
    return { items, removeItem }
}

export const List = ({ items, removeItem }) => {
    return <div className="flex flex-col gap-2">
        {[...items].map(item => {
            return <div className="flex flex-row justify-between items-center" key={item}>{item} <Button onClick={() => removeItem(item)}>×</Button></div>
        })}
    </div>
}

