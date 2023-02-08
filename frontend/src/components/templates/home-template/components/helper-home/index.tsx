import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperPanel } from 'components/molecules'

export interface IHelperPanelProps {
  setShowHelper: Dispatch<SetStateAction<boolean>>
}

const HelperHome: FunctionComponent<IHelperPanelProps> = ({
  setShowHelper,
}) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(false)
      }}
    >
      Helper
    </HelperPanel>
  )
}

export { HelperHome }
