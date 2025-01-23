'use client';

import Image from "next/image";

export default function Header() {
  return (
    <div className="flex flex-row items-center justify-center w-full flex-shrink-0 border-b-2 border-b-bdr p-2">
      <div className="flex flex-row items-center justify-start w-full">
        <Image 
          src="/images/app-icon.jpeg" 
          alt="The Hub Icon" 
          width="100" 
          height="100"
          className="rounded-full ml-5" />
      </div>

      <div className="flex flex-col items-center justify-end w-full">
        <h1 className="font-patrickHand font-bold italic text-end text-fg text-2xl tracking-widest w-full mr-5">
          The Hub
        </h1>

        <h3 className="font-indieFlower italic text-end text-fg text-lg tracking-widest w-full mr-5">
          Catch Phrase Here
        </h3>
      </div>
    </div>
  );
};
