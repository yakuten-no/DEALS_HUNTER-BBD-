import { useState, type FormEvent, type ReactNode } from "react";
import { ChevronDown, ChevronUp, Search } from "lucide-react";
import type { WishlistCreateInput } from "../../types/wishlist";

interface HuntInputProps {
  onSubmit: (data: WishlistCreateInput) => Promise<unknown>;
}

interface ConstraintsState {
  budget_target: string;
  budget_max: string;
  minimum_storage_gb: string;
  preferred_ram_gb: string;
  camera_priority: boolean;
  gaming_priority: boolean;
  battery_priority: boolean;
  wireless_charging_preferred: boolean;
  preferred_brands: string;
  preferred_os: string;
}

const EMPTY_CONSTRAINTS: ConstraintsState = {
  budget_target: "",
  budget_max: "",
  minimum_storage_gb: "",
  preferred_ram_gb: "",
  camera_priority: false,
  gaming_priority: false,
  battery_priority: false,
  wireless_charging_preferred: false,
  preferred_brands: "",
  preferred_os: "",
};

function toInt(value: string): number | undefined {
  if (value.trim() === "") return undefined;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? Math.round(parsed) : undefined;
}

const inputClass =
  "w-full rounded-md border border-base-hairline bg-base px-3 py-2 font-mono text-sm text-ink placeholder:text-ink-muted/50 focus:border-signal-amber/60 focus:outline-none";

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-xs text-ink-muted">{label}</span>
      {children}
    </label>
  );
}

function PriorityCheckbox({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
  label: string;
}) {
  return (
    <label className="flex cursor-pointer items-center gap-2 text-sm text-ink">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="h-4 w-4 rounded border-base-hairline bg-base text-signal-amber focus:ring-signal-amber"
      />
      {label}
    </label>
  );
}

/**
 * The dashboard's hero element: a large natural-language input that saves
 * the query exactly as typed. V0.1 has no AI yet, so nothing here is
 * "interpreted" -- the optional constraints panel lets a user set exact,
 * deterministic filters directly instead, for anyone who wants precision
 * before AI parsing exists (see project-memory/ARCHITECTURE.md).
 */
export function HuntInput({ onSubmit }: HuntInputProps) {
  const [query, setQuery] = useState("");
  const [showConstraints, setShowConstraints] = useState(false);
  const [constraints, setConstraints] = useState<ConstraintsState>(EMPTY_CONSTRAINTS);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!query.trim() || submitting) return;

    setSubmitting(true);
    setError(null);
    try {
      const brands = constraints.preferred_brands
        .split(",")
        .map((brand) => brand.trim())
        .filter(Boolean);

      await onSubmit({
        raw_query: query.trim(),
        budget_target: toInt(constraints.budget_target),
        budget_max: toInt(constraints.budget_max),
        minimum_storage_gb: toInt(constraints.minimum_storage_gb),
        preferred_ram_gb: toInt(constraints.preferred_ram_gb),
        // `false || undefined` -> undefined, which JSON.stringify omits
        // entirely, so an unchecked box means "not specified" on the
        // backend rather than an explicit "false".
        camera_priority: constraints.camera_priority || undefined,
        gaming_priority: constraints.gaming_priority || undefined,
        battery_priority: constraints.battery_priority || undefined,
        wireless_charging_preferred: constraints.wireless_charging_preferred || undefined,
        preferred_brands: brands.length > 0 ? brands : undefined,
        preferred_os: constraints.preferred_os.trim() || undefined,
      });

      setQuery("");
      setConstraints(EMPTY_CONSTRAINTS);
      setShowConstraints(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't save that -- try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="mx-auto max-w-7xl px-6 pb-8 pt-10">
      <h1 className="mb-1.5 text-2xl font-semibold tracking-tight text-ink">
        Describe the phone you want. We'll start tracking it.
      </h1>
      <p className="mb-5 max-w-2xl text-sm text-ink-muted">
        Saved exactly as you write it. Turning this into structured filters automatically is a planned AI feature,
        not active in this version -- use "Set exact constraints" below for precise rules right away.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="flex items-start gap-3 rounded-lg border border-base-hairline bg-base-panel p-3 transition-colors focus-within:border-signal-amber/60">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Phone around ₹60,000, great camera, strong gaming, 256GB, good battery..."
            rows={2}
            className="min-h-[3rem] flex-1 resize-none bg-transparent text-base text-ink placeholder:text-ink-muted/60 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!query.trim() || submitting}
            aria-label="Add to wishlist"
            className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-md bg-signal-amber text-base transition-opacity hover:opacity-90 disabled:opacity-30"
          >
            <Search className="h-4 w-4" strokeWidth={2} aria-hidden="true" />
          </button>
        </div>

        {error && <p className="mt-2 text-sm text-signal-negative">{error}</p>}

        <button
          type="button"
          onClick={() => setShowConstraints((visible) => !visible)}
          className="mt-3 flex items-center gap-1 text-sm text-ink-muted transition-colors hover:text-ink"
        >
          {showConstraints ? (
            <ChevronUp className="h-3.5 w-3.5" aria-hidden="true" />
          ) : (
            <ChevronDown className="h-3.5 w-3.5" aria-hidden="true" />
          )}
          Set exact constraints (optional)
        </button>

        {showConstraints && (
          <div className="mt-3 grid grid-cols-1 gap-4 rounded-lg border border-base-hairline bg-base-panel p-4 sm:grid-cols-2 lg:grid-cols-4">
            <Field label="Target budget (₹)">
              <input
                type="number"
                min={0}
                value={constraints.budget_target}
                onChange={(e) => setConstraints((c) => ({ ...c, budget_target: e.target.value }))}
                placeholder="60000"
                className={inputClass}
              />
            </Field>
            <Field label="Max budget (₹)">
              <input
                type="number"
                min={0}
                value={constraints.budget_max}
                onChange={(e) => setConstraints((c) => ({ ...c, budget_max: e.target.value }))}
                placeholder="70000"
                className={inputClass}
              />
            </Field>
            <Field label="Min storage (GB)">
              <input
                type="number"
                min={0}
                value={constraints.minimum_storage_gb}
                onChange={(e) => setConstraints((c) => ({ ...c, minimum_storage_gb: e.target.value }))}
                placeholder="256"
                className={inputClass}
              />
            </Field>
            <Field label="Preferred RAM (GB)">
              <input
                type="number"
                min={0}
                value={constraints.preferred_ram_gb}
                onChange={(e) => setConstraints((c) => ({ ...c, preferred_ram_gb: e.target.value }))}
                placeholder="12"
                className={inputClass}
              />
            </Field>
            <Field label="Preferred brands">
              <input
                type="text"
                value={constraints.preferred_brands}
                onChange={(e) => setConstraints((c) => ({ ...c, preferred_brands: e.target.value }))}
                placeholder="Nothing, Samsung"
                className={inputClass}
              />
            </Field>
            <Field label="Preferred software">
              <input
                type="text"
                value={constraints.preferred_os}
                onChange={(e) => setConstraints((c) => ({ ...c, preferred_os: e.target.value }))}
                placeholder="Nothing OS"
                className={inputClass}
              />
            </Field>
            <div className="flex flex-col justify-center gap-2 sm:col-span-2 lg:col-span-2">
              <PriorityCheckbox
                checked={constraints.camera_priority}
                onChange={(v) => setConstraints((c) => ({ ...c, camera_priority: v }))}
                label="Camera matters"
              />
              <PriorityCheckbox
                checked={constraints.gaming_priority}
                onChange={(v) => setConstraints((c) => ({ ...c, gaming_priority: v }))}
                label="Gaming performance matters"
              />
              <PriorityCheckbox
                checked={constraints.battery_priority}
                onChange={(v) => setConstraints((c) => ({ ...c, battery_priority: v }))}
                label="Battery life matters"
              />
              <PriorityCheckbox
                checked={constraints.wireless_charging_preferred}
                onChange={(v) => setConstraints((c) => ({ ...c, wireless_charging_preferred: v }))}
                label="Wireless charging wanted"
              />
            </div>
          </div>
        )}
      </form>
    </section>
  );
}
