import { useEffect, useState } from 'react'
import FileSelect from './components/FileSelect'
import axios from 'axios'
import * as XLSX from "xlsx";
import Button from './components/Button';
import { List, useList } from './components/List';
import FilterList from './FilterList';
import Checkbox from './components/Checkbox';

function App() {
  const [inventory, setInventory] = useState()
  const [subtractions, setSubractions] = useState()
  const [downloadUrl, setDownloadUrl] = useState()
  const [tableData, setTableData] = useState()
  const [filters, setFilters] = useState(new Set([]))
  const [onlyComplete, setOnlyComplete] = useState(true)
  const calculate = async () => {
    try {
      const res = await axios.post("/api/calculate", { onlyComplete: onlyComplete }, {
        responseType: "blob",
      });
      const blob = new Blob([res.data]);
      console.log(blob)
      const arrayBuffer = await blob.arrayBuffer();
      console.log(arrayBuffer)
      const workbook = XLSX.read(arrayBuffer, { type: "array" });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      setTableData(json)
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url); // store it for later download click
    } catch (err) {
      console.error("Upload failed", err);
      return
    }
  }

  useEffect(() => {
    calculate()
  }, [onlyComplete])

  const submitFilters = (filters) => {
    axios.post("/api/filters", { "filters": [...filters] }).then(response => {
      setFilters(new Set([...response.data]))
    }).then(calculate)
  }

  const download = () => {
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "result.xlsx";
    a.click();
    URL.revokeObjectURL(downloadUrl);
  }

  useEffect(() => {
    axios.get("/api/clear").then(() => {
      axios.get("/api/filters").then(response => {
        setFilters(new Set([...response.data]))
      })
    })
  }, [])

  useEffect(() => {
    if (!subtractions) return
    const upload = async () => {
      const formData = new FormData();
      formData.append("subtractions", subtractions);
      const res = await axios.post("/api/subtractions", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    }
    upload().then(() => {
      if (inventory) {
        calculate()
      }
    })
  }, [subtractions])


  useEffect(() => {
    if (!inventory) return
    const upload = async () => {
      const formData = new FormData();
      formData.append("inventory", inventory);
      const res = await axios.post("/api/inventory", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    }
    upload().then(() => {
      if (subtractions) {
        calculate()
      }
    })
  }, [inventory])

  return <div className='w-full h-full flex flex-col items-center gap-12'>
    <div className='flex flex-row gap-24'>
      <div className='flex flex-col gap-3'>
        <div className={"font-semibold"}>Lagerlista:</div>
        <FileSelect setFile={setInventory} />
      </div>
      <div className='flex flex-col gap-3'>
        <div className={"font-semibold"}>Artikelstatistik:</div>
        <FileSelect setFile={setSubractions} />
      </div>
      <FilterList filters={filters} submitFilters={submitFilters} onlyComplete={onlyComplete} setOnlyComplete={setOnlyComplete} />
    </div>
    {tableData ?
      <div className='flex flex-col gap-5 items-end'>
        <div className='overflow-y-auto h-128'>
          <table>
            <thead>
              <tr className='sticky top-0'>
                {tableData[0].map((cell, j) => (
                  <th key={j} className='px-5 py-2'>{cell}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, i) => {
                if (i === 0) return <tr key={i}></tr>
                return <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j} className='px-5 py-2'>{cell}</td>
                  ))}
                </tr>
              })}
            </tbody>
          </table>
        </div>
        <Button onClick={download}>Save result</Button>
      </div>
      : <></>}
  </div>
}

export default App
