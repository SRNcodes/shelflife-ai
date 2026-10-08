"use client";

import { useEffect, useState } from "react";

// Boilerplate - not core logic. The extracted item/receipt shape isn't
// pinned down yet (see backend/app/schemas.py, which you implement), so
// this stays loose for now. Tighten this type once your Pydantic schemas
// settle and you can generate/hand-write a matching TS type.
type ExtractedItem = Record<string, unknown>;
type ExtractedReceipt = { items?: ExtractedItem[]; [key: string]: unknown };
type PantryItem = {
  id: number;
  name: string;
  quantity: string;
  unit: string;
  price: string | null;
  expiration_date: string | null;
  status: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function Home() {
  const [receiptId, setReceiptId] = useState<number | null>(null);
  const [items, setItems] = useState<ExtractedItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [expiringSoon, setExpiringSoon] = useState<PantryItem[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/pantry/expiring-soon`)
      .then((res) => res.json())
      .then(setExpiringSoon)
      .catch(() => {
        /* backend not up yet - fine for Week 1 */
      });
  }, []);

  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    const form = e.currentTarget;
    const fileInput = form.elements.namedItem("file") as HTMLInputElement;
    const file = fileInput.files?.[0];
    if (!file) return;

    const body = new FormData();
    body.append("file", file);

    setUploading(true);
    try {
      const res = await fetch(`${API_BASE}/receipts`, { method: "POST", body });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail ?? "Upload failed");
      }
      setReceiptId(data.receipt_id);
      const extracted: ExtractedReceipt = data.extracted;
      setItems(extracted.items ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setUploading(false);
    }
  }

  function updateItemField(index: number, field: string, value: string) {
    setItems((prev) =>
      prev.map((item, i) => (i === index ? { ...item, [field]: value } : item))
    );
  }

  async function handleConfirm() {
    if (receiptId == null) return;
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/receipts/${receiptId}/confirm`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(items),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail ?? "Confirm failed");
      }
      setReceiptId(null);
      setItems([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  // Columns shown in the editable table. Adjust once schemas.py defines
  // the real ExtractedItem fields - this just reads whatever keys show up.
  const columns = items.length > 0 ? Object.keys(items[0]) : ["name", "quantity", "unit", "price"];

  return (
    <main>
      <h1>ShelfLife AI</h1>

      {expiringSoon.length > 0 && (
        <div className="banner">
          <strong>Expiring soon:</strong>{" "}
          {expiringSoon.map((i) => `${i.name} (${i.expiration_date})`).join(", ")}
        </div>
      )}

      <form onSubmit={handleUpload}>
        <input type="file" name="file" accept="image/*" required />
        <button type="submit" disabled={uploading}>
          {uploading ? "Extracting..." : "Upload receipt"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {items.length > 0 && (
        <>
          <h2>Extracted items (edit before confirming)</h2>
          <table>
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((item, i) => (
                <tr key={i}>
                  {columns.map((col) => (
                    <td key={col}>
                      <input
                        value={String(item[col] ?? "")}
                        onChange={(e) => updateItemField(i, col, e.target.value)}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={handleConfirm}>Confirm &amp; save to pantry</button>
        </>
      )}
    </main>
  );
}
