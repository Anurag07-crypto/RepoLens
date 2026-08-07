declare module 'react-syntax-highlighter' {
  import * as React from 'react'

  export interface SyntaxHighlighterProps {
    children: React.ReactNode
    language?: string
    style?: unknown
    PreTag?: React.ElementType
    [key: string]: any
  }

  export class Prism extends React.Component<SyntaxHighlighterProps> {}
}

declare module 'react-syntax-highlighter/dist/esm/styles/prism' {
  export const oneDark: Record<string, unknown>
}
