import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel, HelperTopic } from 'components/molecules'
import Home1Img from './assets/home_1.png'
import Home2Img from './assets/home_2.png'
import Home3Img from './assets/home_3.png'

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
      <HelperTopic title="Requirements">
        <HelperItem title={'Freighter Wallet'}>
          Before you access the Stellar Asset Sandbox, make sure the{' '}
          <a href="https://www.freighter.app/" target={'_blank'}>
            Freighter wallet extension
          </a>{' '}
          installed. It is a non-custodial wallet extension that enables you to
          sign Stellar transactions via your browser.
          <br />
          <br />
          As a non-custodial solution, the Stellar Asset Sandbox fully
          integrates with Freighter so you can use your own Stellar accounts to
          create and manage assets in the Stellar network.
        </HelperItem>
        <HelperItem title={'Testnet'}>
          Once the Freighter extension is installed and running, click on its
          icon from the extension bar and make sure you have the option
          ‘TESTNET’ selected on the top right corner. As a tool for
          demonstration purposes, the Sandbox is locked to the Stellar Testnet
          and will not generate transactions for the Mainnet.
          <img src={Home1Img} />
        </HelperItem>
        <HelperItem title={'Issuing and Distribution accounts'}>
          As per{' '}
          <a
            href="https://developers.stellar.org/docs/issuing-assets/control-asset-access"
            target="_blank"
          >
            the best practice
          </a>{' '}
          adopted by the majority of the ecosystem, we recommend you have two
          accounts created and funded in the Stellar testnet to begin with.
          These two accounts will be used as the Issuing and Distribution
          accounts. To create a new account, open the Freighter extension and
          click on the top left account identicon.
          <img src={Home2Img} />
          From the list, select ‘Create a new Stellar address’ and input you
          password.Your newly create account will be added to the list. When in
          Testnet, if the account hasn’t been funded yet, a ‘Fund with
          Friendbot’ button will be displayed. By clicking on this button, the
          Friendbot will automatically initialize your new account and fill it
          with 10.000 XLM.
          <img src={Home3Img} width={240} />
          Make sure you have two accounts initialized and funded in Testnet to
          play the roles of ‘Issuing’ and ‘Distribution’ account, before
          accessing the Sandbox.
        </HelperItem>
      </HelperTopic>
      <HelperTopic title="Accessing">
        <HelperItem>
          Once you’ve met the requirements, to access the Stellar Asset Sandbox
          its only necessary to input the public key of the issuing account in
          the and it’ll automatically load the account information from the
          Stellar network and start the sandbox. Alternatively, clicking on the
          key icon will automatically load the public key of the selected
          account on Freighter.
        </HelperItem>
      </HelperTopic>
    </HelperPanel>
  )
}

export { HelperHome }
