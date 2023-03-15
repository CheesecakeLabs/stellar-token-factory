import { FunctionComponent, ReactNode } from 'react'

export interface IColumnProps {
  children: ReactNode
  col?: number
}

const Column: FunctionComponent<IColumnProps> = ({ children, col }) => {
  return <div style={{ width: `${100 / (12 / (col || 1))}%` }}>{children}</div>
}

export { Column }
