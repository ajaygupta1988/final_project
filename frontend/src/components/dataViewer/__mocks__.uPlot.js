import {vi} from "vitest";

export const uPlot = vi.fn(() => ({
    root: document.createElement('div'),
    setData: vi.fn(),
    destroy: vi.fn(),
  }));
  
