import type { ProductDetail } from "../../types/product";

interface VariantListPanelProps {
  product: ProductDetail | null;
  loading: boolean;
  error: string | null;
  selectedVariantId: number | null;
  onSelect: (variantId: number) => void;
}

function variantLabel(variant: ProductDetail["variants"][number]): string {
  if (variant.variant_name) return variant.variant_name;
  const parts: string[] = [];
  if (variant.ram_gb != null) parts.push(`${variant.ram_gb}GB RAM`);
  if (variant.storage_gb != null) parts.push(`${variant.storage_gb}GB`);
  if (variant.color) parts.push(variant.color);
  return parts.length > 0 ? parts.join(" / ") : `Variant #${variant.id}`;
}

export function VariantListPanel({ product, loading, error, selectedVariantId, onSelect }: VariantListPanelProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Variants</h2>

      {!product && !loading && <p className="text-sm text-ink-muted">Select a product to see its variants.</p>}
      {loading && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {product && !loading && product.variants.length === 0 && (
        <p className="text-sm text-ink-muted">This product has no variants yet.</p>
      )}

      {product && (
        <ul className="flex flex-col gap-1.5">
          {product.variants.map((variant) => {
            const isSelected = variant.id === selectedVariantId;
            return (
              <li key={variant.id}>
                <button
                  type="button"
                  onClick={() => onSelect(variant.id)}
                  className={`w-full rounded-md border px-3 py-2 text-left font-mono text-sm transition-colors ${
                    isSelected
                      ? "border-signal-amber/60 bg-signal-amber/10 text-ink"
                      : "border-base-hairline bg-base text-ink-muted hover:border-signal-amber/30"
                  }`}
                >
                  {variantLabel(variant)}
                  {variant.sku && <span className="ml-2 text-[11px] text-ink-muted">SKU {variant.sku}</span>}
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
