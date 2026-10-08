import "./globals.css";

export const metadata = {
  title: "ShelfLife AI",
  description: "Upload a receipt, track your pantry, get reminders before food expires.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
