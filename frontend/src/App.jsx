import { useEffect, useState } from 'react'
import FileSelect from './components/FileSelect'
import axios from 'axios'
import * as XLSX from "xlsx";
import Button from './components/Button';

function App() {
  const [inventory, setInventory] = useState()
  const [subtractions, setSubractions] = useState()
  const [downloadUrl, setDownloadUrl] = useState()
  const [tableData, setTableData] = useState()
  const upload = async (file) => {
    try {
      const res = await axios.post("/api/upload", file, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });

      console.log(res)
      // Preview
      const blob = new Blob([res.data]);
      const arrayBuffer = await blob.arrayBuffer();
      const workbook = XLSX.read(arrayBuffer, { type: "array" });

      // Example: Get first sheet data
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

      // Show preview in console or UI
      // console.table(json); // or render to table
      setTableData(json)

      // Optional: keep the blob for later download
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url); // store it for later download click
    } catch (err) {
      console.error("Upload failed", err);
      return
    }
  }

  const download = () => {
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "result.xlsx";
    a.click();
    URL.revokeObjectURL(downloadUrl);
  }

  useEffect(() => {
    if (!inventory || !subtractions) return
    const formData = new FormData();
    formData.append("inventory", inventory);
    formData.append("subtractions", subtractions)
    upload(formData)
  }, [inventory, subtractions])

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
    </div>
    {tableData ?
      <div className='flex flex-col gap-5 items-end'>
        <div className='overflow-y-auto h-128'>
          <table>
            {tableData.map((row, i) => {
              if (i === 0) {
                return <tr key={i} className='sticky top-0'>
                  {row.map((cell, j) => (
                    <th key={j} className='px-5 py-2'>{cell}</th>
                  ))}
                </tr>
              } else {
                return <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j} className='px-5 py-2'>{cell}</td>
                  ))}
                </tr>
              }
            })}
          </table>
        </div>
        <Button onClick={download}>Save file</Button>
      </div>
      : <></>}
  </div>
}

export default App
