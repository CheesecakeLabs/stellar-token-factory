import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel } from 'components/molecules'

export interface IHelperForgingProps {
  setShowHelper: Dispatch<SetStateAction<boolean>>
}

const HelperForging: FunctionComponent<IHelperForgingProps> = ({
  setShowHelper,
}) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(false)
      }}
    >
      <HelperItem title="Token Forging">
        Following up on the main screen, we have the Token Creation formulary.
        Basically, what it does is to create a trustline between the Issuer
        Address and the Treasury Address (Distributor) with the change_trust
        operation, and then, perform a payment of that asset from the issuer
        address to the distributor address. You can check the whole process of
        issuing Stellar assets in their documentation.
      </HelperItem>
    </HelperPanel>
  )
}

export { HelperForging }
