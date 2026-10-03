// jest-dom's Vitest entry point registers its matchers on Vitest's own
// `expect`. (The plain "@testing-library/jest-dom" entry expects a global
// `expect`, which only exists when Vitest's `globals` option is on -- this
// project keeps it off and imports from "vitest" explicitly instead.)
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Testing Library only auto-registers its per-test cleanup when a global
// `afterEach` exists. With globals off it never does, so unmount rendered
// trees explicitly; otherwise DOM from one test leaks into the next and
// queries start finding duplicate elements.
afterEach(() => {
  cleanup();
});
