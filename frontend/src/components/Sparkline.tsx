const WIDTH = 200;
const HEIGHT = 56;

export function Sparkline({ values }: { values: number[] }) {
  if (values.length < 2) {
    return <svg width={WIDTH} height={HEIGHT} aria-hidden="true" />;
  }

  const lo = Math.min(...values);
  const hi = Math.max(...values);
  const span = hi - lo || 1;

  const points = values.map((v, i) => {
    const x = (i / (values.length - 1)) * WIDTH;
    const y = HEIGHT - 4 - ((v - lo) / span) * (HEIGHT - 8);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });

  const lastY = points[points.length - 1].split(",")[1];
  const areaPoints = `0,${HEIGHT} ${points.join(" ")} ${WIDTH},${HEIGHT}`;

  return (
    <svg width={WIDTH} height={HEIGHT} aria-hidden="true">
      <polyline points={areaPoints} fill="var(--accent-soft)" stroke="none" />
      <polyline
        points={points.join(" ")}
        fill="none"
        stroke="var(--accent)"
        strokeWidth={1.6}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <circle cx={WIDTH} cy={lastY} r={3} fill="var(--accent)" />
    </svg>
  );
}
