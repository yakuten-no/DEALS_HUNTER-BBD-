/**
 * A visually unmissable marker for fixture/demo data (Product.is_demo /
 * RetailerListing.is_demo) -- the app must communicate the difference
 * between real observed data and demo data, not just leave it to a
 * tooltip or fine print (see project-memory/DECISIONS.md, D-005).
 */
export function DemoBadge() {
  return (
    <span className="inline-flex items-center rounded border border-signal-amber/40 bg-signal-amber/10 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide text-signal-amber">
      Demo
    </span>
  );
}
