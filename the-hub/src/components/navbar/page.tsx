'use client';

import LoggedOut from "./loggedOut/page";
import LoggedIn from "./loggedIn/page";

export default function Navbar({
  props,
} : {
  props: { loggedIn: boolean },
}) {
  if (!props.loggedIn) {
    return <LoggedOut />
  } else {
    return <LoggedIn />
  };
};
