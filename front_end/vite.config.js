/** @type {import('vite').UserConfig} */
export default {
  build: {
    lib: {
      entry: './index.html',
      formats: ['es', 'cjs'],
    },
  },
};
