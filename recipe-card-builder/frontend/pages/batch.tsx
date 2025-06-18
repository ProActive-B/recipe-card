import { useState } from 'react';
import Papa from 'papaparse';
import ProgressBar from '../components/ProgressBar';

interface Row {
  url: string;
  target_lang: string;
  job_id?: string;
  status?: string;
}

export default function Batch() {
  const [rows, setRows] = useState<Row[]>([]);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    Papa.parse<Row>(file, {
      header: true,
      complete: (res) => {
        setRows(res.data);
      },
    });
  };

  const startJobs = async () => {
    const updated = await Promise.all(
      rows.map(async (row) => {
        const res = await fetch('/api/job', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: row.url, target_lang: row.target_lang }),
        });
        const data = await res.json();
        return { ...row, job_id: data.job_id, status: 'pending' };
      })
    );
    setRows(updated);
  };

  const poll = async (row: Row) => {
    if (!row.job_id) return row;
    const res = await fetch(`/api/job/${row.job_id}`);
    const data = await res.json();
    return { ...row, status: data.status };
  };

  const refresh = async () => {
    const updated = await Promise.all(rows.map(poll));
    setRows(updated);
  };

  return (
    <div className="p-4 space-y-4">
      <input type="file" accept=".csv" onChange={handleFile} />
      <button className="bg-blue-500 text-white px-4 py-2" onClick={startJobs}>
        Start Jobs
      </button>
      <button className="ml-2 border px-2" onClick={refresh}>
        Refresh
      </button>
      <table className="table-auto w-full mt-4 border">
        <thead>
          <tr>
            <th className="border px-2">URL</th>
            <th className="border px-2">Target</th>
            <th className="border px-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} className="border">
              <td className="border px-2">{row.url}</td>
              <td className="border px-2">{row.target_lang}</td>
              <td className="border px-2">
                {row.status && <ProgressBar status={row.status} />}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
