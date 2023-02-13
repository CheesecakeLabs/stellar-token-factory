import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel, HelperTopic } from 'components/molecules'
import { HelperFactoryEnum } from 'components/templates'
import FlowImg from '../helper-forging/assets/flow.png'

export interface IHelperForgingProps {
  setShowHelper: Dispatch<SetStateAction<HelperFactoryEnum | undefined>>
}

const HelperForging: FunctionComponent<IHelperForgingProps> = ({
  setShowHelper,
}) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(undefined)
      }}
    >
      <HelperTopic title="Forging">
        <HelperItem>
          The forging areas allows for a new asset to be created for the issuing
          account indicated. During this process a a first trustline is created
          for the distribution account, therefore it is necessary to sign and
          authorize the transaction for the distribution account using
          Freighter.
          <br />
          <br />
          As per{' '}
          <a
            href="https://developers.stellar.org/docs/issuing-assets/control-asset-access"
            target="_blank"
          >
            the best practice
          </a>{' '}
          adopted by the majority of the ecosystem, we recommend you use the
          design patter of having dedicated Issuing and Distribution accounts.
          If you’d like to use different accounts, just input manually the
          desired accounts.
          <img src={FlowImg} />
          <br />
          <b>Issuing account Field:</b> Requires the public key of the account
          that will be used as the issuing account for this asset. By default,
          the same account used to load the sandbox comes prefilled.
          <br />
          <br />
          Clicking on the key icon will load the public key of the account
          selected on Freighter.
          <br />
          <br />
          <b>Distribution account Field:</b> Requires the public key of the
          account that will be used as the distribution account for this asset.
          <br />
          <br />
          Clicking on the key icon will load the public key of the account
          selected on Freighter.
          <br />
          <br />
          <b>Name your Asset field:</b> The asset code for your new asset like
          BTC for Bitcoin or XLM for Lumens. It will be used as an
          identification code for your asset.
          <br />
          <br />
          <b>Add a Limit field:</b> Used to define a limit to how much balance
          of this asset the distribution account may hold. This field is
          optional, not filling it implies the maximum network limit.
        </HelperItem>
      </HelperTopic>
    </HelperPanel>
  )
}

export { HelperForging }
