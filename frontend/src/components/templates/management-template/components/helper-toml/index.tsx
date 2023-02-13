import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel } from 'components/molecules'
import { TabsManagementEnum } from '../..'

export interface IHelperTomlProps {
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const HelperToml: FunctionComponent<IHelperTomlProps> = ({ setShowHelper }) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(undefined)
      }}
    >
      <HelperItem title="Generate Toml file">
      </HelperItem>
    </HelperPanel>
  )
}

export { HelperToml }
