import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/header/page";

export const metadata: Metadata = {
  title: "The Hub",
  description: "Developed By 'The Team'",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
      </body>
    </html>
  );
}
