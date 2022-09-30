import { FunctionComponent, useCallback, useEffect, useState } from 'react'
import { IconButton, Tag, Tooltip } from '@stellar/design-system'
import styles from './styles.module.scss'
import { getNetwork } from '@stellar/freighter-api'
import { useNavigate } from 'react-router-dom'
import { LogOut } from 'react-feather'
import { Authentication } from 'app/core/auth'

const HeaderStatus: FunctionComponent = () => {
  const [network, setNetwork] = useState('')
  const navigate = useNavigate()

  const redirectHome = useCallback(() => {
    navigate('/')
  }, [navigate])

  const listenNetwork = useCallback(() => {
    getNetwork().then(data => {
      if (network && data != network) {
        redirectHome()
      }
      setNetwork(data)
    })
  }, [network, redirectHome])

  useEffect(() => {
    listenNetwork()
    const timer = setInterval(() => {
      listenNetwork()
    }, 3000)
    return () => clearInterval(timer)
  }, [listenNetwork])

  const logout = (): void => {
    Authentication.logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className={styles.network}>
      <Tooltip content="You can change the network directly from Freighter">
        <Tag
          variant={
            network == 'PUBLIC' ? Tag.variant.success : Tag.variant.warning
          }
        >
          {network}
        </Tag>
      </Tooltip>
      <IconButton
        altText="Logout"
        icon={<LogOut key="logout" />}
        label="Logout"
        onClick={logout}
      />
    </div>
  )
}

export { HeaderStatus }
