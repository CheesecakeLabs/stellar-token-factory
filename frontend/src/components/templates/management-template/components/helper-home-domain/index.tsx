import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel } from 'components/molecules'
import { TabsManagementEnum } from '../..'

export interface IHelperHomeDomainProps {
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const HelperHomeDomain: FunctionComponent<IHelperHomeDomainProps> = ({ setShowHelper }) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(undefined)
      }}
    >
      <HelperItem title="Home Domain">
      </HelperItem>
    </HelperPanel>
  )
}

export { HelperHomeDomain }
