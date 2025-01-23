'use client';

import Link from "next/link";

import { usePathname } from "next/navigation";


const NavLink = ({
  href,
  children
}: {
  href: string,
  children: React.ReactNode
}) => {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      className={`
        border-t-2 border-t-bdr border-b-2 border-b-bdr 
        font-indieFlower italic text-fg text-center 
        w-[90%] p-2 outline-none hover:outline-none focus:outline-none
        hover:bg-hvr hover:text-2xl hover:scale-105 transition-all delay-105
        ${isActive ? 'font-bold' : ''}
        ${isActive ? 'bg-gray-700' : ''}
        ${isActive ? 'text-2xl' : 'text-xl'}
      `}
    >
      {children}
    </Link>
  );
};

export default function LoggedOut() {
  return (
    <div className="flex flex-col items-center justify-start gap-5 w-[20%] h-[900px]">
      <NavLink href="/">Home</NavLink>
      <NavLink href="/auth/signup">Sign Up</NavLink>
      <NavLink href="/x">Login</NavLink>
      <NavLink href="/w">About</NavLink>
      <NavLink href="/2">Support</NavLink>
    </div>
  );
};
