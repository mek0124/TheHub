'use client';

import Navbar from "@/components/navbar/page";

export default function Home() {
  return (
    <div className="flex flex-row items-start justify-start w-full min-h-screen">
      <Navbar props={{ loggedIn: false }} />

      <div className="flex flex-col items-center justify-start mt-5 ml-2 mr-2 w-full h-[785px] border-white border-2"></div>
    </div>
  );
}
