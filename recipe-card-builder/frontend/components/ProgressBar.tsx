interface Props {
  status: string;
}

export default function ProgressBar({ status }: Props) {
  const color =
    status === 'completed'
      ? 'bg-green-500'
      : status === 'failed'
      ? 'bg-red-500'
      : status === 'in_progress'
      ? 'bg-yellow-500'
      : 'bg-gray-300';
  return <div className={`w-full h-2 ${color}`}></div>;
}
