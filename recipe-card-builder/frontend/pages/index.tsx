import { useState } from 'react';
import ProgressBar from '../components/ProgressBar';
import RecipeEditor from '../components/RecipeEditor';

export default function Home() {
  const [url, setUrl] = useState('');
  const [lang, setLang] = useState('en');
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState('pending');
  const [recipeId, setRecipeId] = useState<string | null>(null);

  const pollStatus = async (id: string) => {
    const res = await fetch(`/api/job/${id}`);
    const data = await res.json();
    setStatus(data.status);
    if (data.status === 'completed') {
      setRecipeId(data.recipe_id);
    }
  };

  const handleGenerate = async () => {
    const res = await fetch('/api/job', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, target_lang: lang }),
    });
    const data = await res.json();
    setJobId(data.job_id);
    setStatus('pending');
    const interval = setInterval(async () => {
      await pollStatus(data.job_id);
      if (status === 'completed' || status === 'failed') {
        clearInterval(interval);
      }
    }, 2000);
  };

  return (
    <div className="p-4 space-y-4">
      <div>
        <input
          className="border p-2 mr-2"
          placeholder="YouTube URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <select
          className="border p-2 mr-2"
          value={lang}
          onChange={(e) => setLang(e.target.value)}
        >
          <option value="en">English</option>
          <option value="de">German</option>
          <option value="es">Spanish</option>
        </select>
        <button className="bg-blue-500 text-white px-4 py-2" onClick={handleGenerate}>
          Generate
        </button>
      </div>
      {jobId && <ProgressBar status={status} />}
      {status === 'completed' && recipeId && (
        <div>
          <a href={`/static/cards/${recipeId}.pdf`} className="underline">
            Download PDF
          </a>
          <RecipeEditor recipeId={recipeId} />
        </div>
      )}
    </div>
  );
}
