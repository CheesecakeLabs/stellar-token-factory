import {
  Button,
  Card,
  Eyebrow,
  Input,
  Toggle,
  Tooltip,
} from '@stellar/design-system'
import {
  CustomError,
  CustomLoader,
  FabHelper,
  FabHelperVariant,
  TokenMessage,
} from 'components/atoms'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { HelperFactoryEnum } from 'components/templates'
import {
  Dispatch,
  FunctionComponent,
  SetStateAction,
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react'
import { Edit, Info, List, Trash } from 'react-feather'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'
import { defaultSettings, inputsAccounts, ISettings } from './constants'
import styles from './styles.module.scss'

export interface ISettingsProps {
  isModalVisible: boolean
  closeModal: () => void
  issuer: string
  isReadOnly: boolean
  loadTokens: () => void
  setShowHelper: Dispatch<SetStateAction<HelperFactoryEnum | undefined>>
}

const SettingsModal: FunctionComponent<ISettingsProps> = props => {
  const myRef = useRef(null)

  const [inputs, setInputs] = useState(inputsAccounts)
  const [settings, setSettings] = useState<ISettings>(defaultSettings)
  const [isLoadingSettings, setLoading] = useState(true)
  const [isLoadingSubmit, setLoadingSubmit] = useState(false)
  const [error, setError] = useState('')
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)

  const loadSettings = useCallback(async (publicKey: string) => {
    FactoryService.getSetOptions(publicKey)
      .then(response => {
        setSettings(response ? response.data : defaultSettings)
      })
      .catch(() => {
        setSettings(defaultSettings)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    loadSettings(props.issuer)
  }, [loadSettings, props])

  const handleSubmit = async (): Promise<void> => {
    setLoadingSubmit(true)
    setError('')
    settings.public_key = props.issuer

    FactoryService.postSetOptions(settings, props.isReadOnly)
      .then(async response => {
        const result = await FreighterService.requestSignatures(response.data)
        await postEnvelopeXdr(result)
      })
      .catch(e => {
        const responseError = e.response?.data
        setError(responseError ?? 'Unable to save changes')
      })
      .finally(() => {
        setLoadingSubmit(false)
      })
  }

  const postEnvelopeXdr = async (xdr: string): Promise<void> => {
    await FactoryService.postEnvelope(xdr)
      .then(async response => {
        setResponseSubmit(response.data)
        props.loadTokens()
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    cleanFields()
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const removeAccount = (account: number): void => {
    cleanFields()
    setInputs(values => ({ ...values, ['account']: inputs.account }))
    settings.signers.splice(account, 1)
    setSettings(settings)
  }

  const editAccount = (account: string): void => {
    setInputs(values => ({ ...values, ['account']: account }))
    settings.signers = [...settings.signers.filter(item => item !== account)]
    setSettings(settings)
  }

  const addValue = (): void => {
    settings.signers = [...settings.signers, inputs.account]
    setSettings(settings)
    setInputs(values => ({ ...values, ['account']: '' }))
  }

  const cleanFields = (): void => {
    setError('')
    setResponseSubmit(defaultResponseSubmit)
  }

  return (
    <>
      <div className={styles.darkBG} onClick={props.closeModal} />
      <div className={styles.centered}>
        <div className={styles.modal} ref={myRef}>
          {isLoadingSettings ? (
            <CustomLoader />
          ) : (
            <div>
              <FabHelper
                variant={FabHelperVariant.fixedRight}
                onClick={(): void =>
                  props.setShowHelper(HelperFactoryEnum.SETTINGS)
                }
              />
              <Eyebrow className={styles.titles}>
                <Tooltip content="You can enable Freeze and Clawback functionality. Clawback requires Freeze to be enabled as well.">
                  Control access
                  <Info size={14} className={styles.iconTooltip} />
                </Tooltip>
              </Eyebrow>
              <Card>
                <div className={styles.contentControllers}>
                  <Toggle
                    id="toggle-freeze"
                    labelOn="Freeze"
                    labelPosition={Toggle.labelPosition.left}
                    onChange={function (): void {
                      setSettings(values => ({
                        ...values,
                        ['freeze']: !values.freeze,
                      }))
                    }}
                    checked={settings.clawback ? true : settings.freeze}
                    disabled={settings.clawback}
                  />
                  <Toggle
                    id="toggle-clawback"
                    labelOn="Clawback"
                    labelPosition={Toggle.labelPosition.left}
                    onChange={function (): void {
                      setSettings(values => ({
                        ...values,
                        ['clawback']: !values.clawback,
                      }))
                    }}
                    checked={settings.clawback}
                  />
                </div>
              </Card>
              {!props.isReadOnly && (
                <div>
                  <Eyebrow className={styles.titles}>
                    <Tooltip content="Extra accounts with view permission">
                      Extra accounts
                      <Info size={14} className={styles.iconTooltip} />
                    </Tooltip>
                  </Eyebrow>
                  <Card>
                    {settings.signers.map((item, index) => (
                      <div className={styles.listData} key={index}>
                        {item}
                        <div className={styles.listAction}>
                          <Edit
                            size={16}
                            onClick={(): void => editAccount(item)}
                          />
                          <div className={styles.spacer} />
                          <Trash
                            size={16}
                            onClick={(): void => removeAccount(index)}
                          />
                        </div>
                      </div>
                    ))}
                    {settings.signers.length == 0 && (
                      <div className={styles.empty}>
                        <List size={24} />
                        <p>No extra accounts added</p>
                      </div>
                    )}
                    <div className={styles.inputForm}>
                      <div className={styles.fieldAccount}>
                        <Input
                          name="account"
                          id="input-account"
                          placeholder="Account"
                          autoComplete="off"
                          value={inputs.account || ''}
                          onChange={handleChange}
                        />
                      </div>
                      <Button
                        variant={Button.variant.secondary}
                        onClick={addValue}
                        disabled={!inputs.account}
                      >
                        Add
                      </Button>
                    </div>
                  </Card>
                </div>
              )}
              <div className={styles.button}>
                <Button
                  variant={Button.variant.tertiary}
                  onClick={props.closeModal}
                >
                  Close
                </Button>
                <div className={styles.spacer} />
                <Button
                  variant={Button.variant.primary}
                  onClick={handleSubmit}
                  isLoading={isLoadingSubmit}
                >
                  Save
                </Button>
              </div>
              {error && <CustomError message={error} />}
              <TokenMessage
                hash={responseSubmit.transaction_hash}
                link={responseSubmit.transaction_link}
              />
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export { SettingsModal }
