import { FunctionComponent, ReactNode } from 'react'

export interface IRowProps {
  children: ReactNode
  col?: number
}

const Row: FunctionComponent<IRowProps> = ({ children, col }) => {
  return (
    <div
      style={{
        width: `${100 / (12 / (col || 12))}%`,
        display: 'flex',
        flexDirection: 'row',
      }}
    >
      {children}
    </div>
  )
}

export { Row }
