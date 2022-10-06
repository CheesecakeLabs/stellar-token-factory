import { HeaderStatus } from 'components/atoms'
import { FunctionComponent, useCallback } from 'react'
import { ArrowLeftCircle } from 'react-feather'
import { useNavigate } from 'react-router-dom'
import styles from './styles.module.scss'

export interface IManagementHeaderProps {
  asset_code: string
  asset_issuer: string
  asset_distributor: string
  isLoading: boolean
}

const ManagementHeader: FunctionComponent<IManagementHeaderProps> = props => {
  const navigate = useNavigate()

  const back = useCallback(() => {
    navigate(-1)
  }, [navigate])

  return (
    <>
      <div className={styles.header}>
        <div className={styles.content}>
          <p>
            Asset code: <b>{props.asset_code}</b>
          </p>
          <p>
            Issuer: <b>{props.asset_issuer}</b>
          </p>
          <p>
            Distribution:{' '}
            <b>{props.isLoading ? 'Loading...' : props.asset_distributor}</b>
          </p>
          <div className={styles.btBack} onClick={back}>
            <ArrowLeftCircle size={14} /> Back to list
          </div>
        </div>
        <HeaderStatus key={'status'} />
      </div>
    </>
  )
}

export { ManagementHeader }
