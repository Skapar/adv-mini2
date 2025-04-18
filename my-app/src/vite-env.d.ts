/// <reference types="vite/client" />

declare module '*.css' {
  const classes: { [key: string]: string }
  export default classes
}

declare module '*.scss' {
  const scss: string
  export default scss
}

