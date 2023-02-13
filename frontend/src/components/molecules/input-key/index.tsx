import { ChangeEventHandler, Dispatch, FunctionComponent, MouseEventHandler, SetStateAction } from 'react'
import { IconButton, Input } from '@stellar/design-system'
import { Info, Key } from 'react-feather'

import styles from './styles.module.scss'
import { FabHelper, FabHelperVariant } from 'components/atoms'

export interface IInputKeyProps {
  publicKey: string
  handleChange: ChangeEventHandler<HTMLInputElement>
  getKey: MouseEventHandler
  setShowHelper: Dispatch<SetStateAction<boolean>>
}

const InputKey: FunctionComponent<IInputKeyProps> = inputKeyProps => {
  return (
    <div>
      <div className={styles.header}>
        <p>Issuing account public key</p>
        <FabHelper
          variant={FabHelperVariant.fixedRight}
          onClick={(): void => {
            inputKeyProps.setShowHelper(true)
          }}
        />
      </div>
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
        Make sure the issuing account is selected on Freighter before clicking
        the key icon.
      </p>
    </div>
  )
}

export { InputKey }
