import { FunctionComponent, useCallback, useEffect, useState } from 'react'
import { Tag, Tooltip } from '@stellar/design-system'
import styles from './styles.module.scss'
import { getNetwork } from '@stellar/freighter-api'
import { useNavigate } from 'react-router-dom'

const HeaderStatus: FunctionComponent = () => {
  const [network, setNetwork] = useState('')
  const navigate = useNavigate()

  const redirectHome = useCallback(() => {
    navigate('/home')
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
    </div>
  )
}

export { HeaderStatus }
