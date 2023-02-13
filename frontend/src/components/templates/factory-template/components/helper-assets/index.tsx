import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel, HelperTopic } from 'components/molecules'
import { HelperFactoryEnum } from 'components/templates'

export interface IHelperAssetsProps {
  setShowHelper: Dispatch<SetStateAction<HelperFactoryEnum | undefined>>
}

const HelperAssets: FunctionComponent<IHelperAssetsProps> = ({
  setShowHelper,
}) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(undefined)
      }}
    >
      <HelperTopic title="Asset List">
        <HelperItem>
          The asset list presents the on-chain information about the assets
          issued by the ‘Issuing’ account used to access the sandbox. By
          clicking on the ‘manage’ button you’ll be taken to the management area
          for that asset.
          <br />
          <br />
          When accessing with an extra account, the asset will be flagged with a
          ‘Read only’ badge and to indicate it was issued by a different account
          and cannot be managed by the account with which the sandbox was
          loaded. Extra accounts can be ser in the ‘Settings’ area.
        </HelperItem>
      </HelperTopic>
    </HelperPanel>
  )
}

export { HelperAssets }
