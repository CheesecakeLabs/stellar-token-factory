import { LoadingIcon } from 'components/icons'
import styles from './styles.module.scss'

export interface ILoadingProps {
  width?: number
  height?: number
}

const Loading = ({ 
    width, 
    height,
}: ILoadingProps): JSX.Element => {
  return (
    <div 
      className={styles.container}
    >
      <LoadingIcon 
        width={width || 32} 
        height={height || 32}
      />
    </div>
  )
}

export { Loading }
