import type { ComponentType } from "react";
import { BatteryCharging, Camera, Cpu, Gamepad2, HardDrive, Trash2, Wallet, Zap } from "lucide-react";
import type { WishlistEntry } from "../../types/wishlist";

interface WishlistItemProps {
  item: WishlistEntry;
  onDelete: (id: number) => void;
}

interface Chip {
  icon: ComponentType<{ className?: string }>;
  label: string;
}

function formatINR(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function buildChips(item: WishlistEntry): Chip[] {
  const chips: Chip[] = [];

  if (item.budget_target != null || item.budget_max != null) {
    const label =
      item.budget_target != null && item.budget_max != null
        ? `${formatINR(item.budget_target)}\u2013${formatINR(item.budget_max)}`
        : formatINR(item.budget_target ?? item.budget_max ?? 0);
    chips.push({ icon: Wallet, label });
  }
  if (item.minimum_storage_gb != null) chips.push({ icon: HardDrive, label: `${item.minimum_storage_gb}GB+` });
  if (item.preferred_ram_gb != null) chips.push({ icon: Cpu, label: `${item.preferred_ram_gb}GB RAM` });
  if (item.camera_priority) chips.push({ icon: Camera, label: "Camera" });
  if (item.gaming_priority) chips.push({ icon: Gamepad2, label: "Gaming" });
  if (item.battery_priority) chips.push({ icon: BatteryCharging, label: "Battery" });
  if (item.wireless_charging_preferred) chips.push({ icon: Zap, label: "Wireless charging" });

  return chips;
}

export function WishlistItem({ item, onDelete }: WishlistItemProps) {
  const chips = buildChips(item);
  const hasBadges = chips.length > 0 || (item.preferred_brands?.length ?? 0) > 0 || Boolean(item.preferred_os);

  return (
    <li className="group animate-insert-row rounded-md border border-base-hairline bg-base p-3">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-ink">{item.name}</p>
          <p className="line-clamp-2 mt-0.5 text-xs text-ink-muted">{item.raw_query}</p>
        </div>
        <button
          type="button"
          onClick={() => onDelete(item.id)}
          aria-label={`Remove ${item.name} from wishlist`}
          className="flex-shrink-0 rounded p-1 text-ink-muted opacity-0 transition-opacity hover:text-signal-negative focus-visible:opacity-100 group-hover:opacity-100"
        >
          <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
        </button>
      </div>

      {hasBadges && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {chips.map(({ icon: Icon, label }) => (
            <span
              key={label}
              className="inline-flex items-center gap-1 rounded border border-base-hairline px-1.5 py-0.5 font-mono text-[11px] text-ink-muted"
            >
              <Icon className="h-3 w-3" />
              {label}
            </span>
          ))}
          {item.preferred_brands?.map((brand) => (
            <span
              key={brand}
              className="inline-flex items-center rounded border border-base-hairline px-1.5 py-0.5 text-[11px] text-ink-muted"
            >
              {brand}
            </span>
          ))}
          {item.preferred_os && (
            <span className="inline-flex items-center rounded border border-base-hairline px-1.5 py-0.5 text-[11px] text-ink-muted">
              {item.preferred_os}
            </span>
          )}
        </div>
      )}
    </li>
  );
}
