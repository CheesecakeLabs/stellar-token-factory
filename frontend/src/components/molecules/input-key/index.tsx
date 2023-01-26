import { ChangeEventHandler, FunctionComponent, MouseEventHandler } from 'react'
import { IconButton, Input } from '@stellar/design-system'
import { Info, Key } from 'react-feather'

import styles from './styles.module.scss'

export interface IInputKeyProps {
  publicKey: string
  handleChange: ChangeEventHandler<HTMLInputElement>
  getKey: MouseEventHandler
}

const InputKey: FunctionComponent<IInputKeyProps> = inputKeyProps => {
  return (
    <div>
      <Input
        id="input-public-key"
        placeholder="Click the key to connect your Freighter wallet"
        onChange={inputKeyProps.handleChange}
        value={inputKeyProps.publicKey}
        autoComplete="off"
        rightElement={
          <IconButton
            key="bt-public-key"
            altText="Get Public Key"
            icon={<Key key={'key'} />}
            onClick={inputKeyProps.getKey}
          />
        }
      />
      <p className={styles.warning}>
        <Info size={12} className={styles.icon} />
        Make sure to select the Issuer Wallet
      </p>
    </div>
  )
}

export { InputKey }
