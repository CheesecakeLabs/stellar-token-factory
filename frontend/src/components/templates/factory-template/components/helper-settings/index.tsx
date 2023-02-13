import { Dispatch, FunctionComponent, SetStateAction } from 'react'
import { HelperItem, HelperPanel, HelperTopic } from 'components/molecules'
import { HelperFactoryEnum } from 'components/templates'

export interface IHelperSettingsProps {
  setShowHelper: Dispatch<SetStateAction<HelperFactoryEnum | undefined>>
}

const HelperSettings: FunctionComponent<IHelperSettingsProps> = ({
  setShowHelper,
}) => {
  return (
    <HelperPanel
      onClick={(): void => {
        setShowHelper(undefined)
      }}
    >
      <HelperTopic title="Control Access">
        <HelperItem>
          The ‘Control Access’ area provides with a series of feature toggles
          that can be enable/disabled at any time for the loaded ‘Issuing’
          account. In the Sandbox, these toggles represent a combination of{' '}
          <a
            href="https://developers.stellar.org/docs/issuing-assets/control-asset-access#controlling-access-to-an-asset-with-flags"
            target="_blank"
          >
            control flags
          </a>{' '}
          managed in the Stellar network to create the intended control
          mechanism.
          <br />
          <br />
          <b>Freeze</b>: When active, this flag enables the ‘Freeze’ tab in the
          asset management area. In this tab, the Issuing account can freeze the
          current balance for a given account holding its asset. The frozen
          account ill then be unable to receive or send the asset in any way
          until the Issuing account unfreezes it.
          <br />
          <br />
          It is important to note that the Freeze functionality only affects
          assets Issued by the account with the active flag.
          <br />
          <br />
          <b>Clawback</b>: When active, this flag enables the ‘Clawback’ tab in
          the asset management area. In this tab, the Issuing account can
          clawback funds from a target account holding balance in its assets.
          The clawback amount is burned from the circulating supply as result.
          <br />
          <br />
          It is important to note the following characteristics of the Clawback
          functionality:
          <br />
          <ul>
            <li>
              It only affects assets Issued by the account with the active flag
            </li>
            <li>
              Upon being activated, it will only affect accounts which had their
              trustlines created after the flag activation. Existing accounts
              with trustlines created prior to activating the flag cannot have
              their funds clawbacked.
            </li>
            <li>
              To enable the Clawback flag, it is necessary to enable the Freeze
              flag as a requirement.
            </li>
          </ul>
        </HelperItem>
      </HelperTopic>
      <HelperTopic title={'Extra Accounts'}>
        <HelperItem>
          As the Sandbox loads its data based on the ‘Issuing’ account provided,
          it can be challenging working with multiple ‘Issuing’ accounts for
          different assets. The ‘Extra Accounts’ area was created as a way to
          allow additional accounts to be linked to the currently loaded Issuing
          account with no signing power.
          <br />
          <br />
          When accessing the Sandbox, it’ll load the assets issued by the given
          account plus all assets issued by accounts to which it was added as an
          extra account. Even though you’ll be able to see these other assets,
          the account will still be unable to sign for their transactions.
          <br />
          <br />
          This is intended as a way for sharing a view only permission when
          collaborating with friends and colleagues.
          <br />
          <br />
          To add an account as extra, simply enter its Public Key in the account
          field, press the ‘Add’ button and then ‘Save’.
        </HelperItem>
      </HelperTopic>
    </HelperPanel>
  )
}

export { HelperSettings }
