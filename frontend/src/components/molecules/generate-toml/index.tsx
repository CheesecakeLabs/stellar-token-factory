import {
  Dispatch,
  FunctionComponent,
  SetStateAction,
  useCallback,
  useEffect,
  useState,
} from 'react'
import { Button, Card, InfoBlock } from '@stellar/design-system'
import {
  CustomError,
  CustomLoader,
  FabHelper,
  FabHelperVariant,
} from 'components/atoms'
import { FactoryService } from 'services/factory'

import styles from './styles.module.scss'
import { defaultGenerateToml, defaultOrgDoc, IToml } from './constants'
import { handleSubmitErrors } from './form-validation'
import {
  AccordionContact,
  AccordionCurrencyDoc,
  AccordionGeneralInfo,
  AccordionOrgDoc,
} from '..'
import fileDownload from 'js-file-download'
import { TabsManagementEnum } from 'components/templates'

export interface IGenerateTomlProps {
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const GenerateToml: FunctionComponent<IGenerateTomlProps> = props => {
  const [isLoadingSubmit, setIsLoadingSubmit] = useState(false)
  const [error, setError] = useState('')
  const [isSuccess, setIsSuccess] = useState(false)
  const [toml, setToml] = useState<IToml>(defaultGenerateToml)
  const [isLoadingToml, setIsLoadingToml] = useState(true)

  const cleanToml = useCallback(() => {
    const toml = defaultGenerateToml
    toml.general_info.accounts = []
    toml.currency_doc = []
    toml.org_doc = defaultOrgDoc
    toml.point_of_contact_doc = []
    return toml
  }, [])

  const loadToml = useCallback(
    async (publicKey: string) => {
      setIsLoadingToml(true)
      FactoryService.getToml(publicKey)
        .then(response => {
          setToml(response ? response.data : cleanToml())
        })
        .catch(() => {
          setToml(cleanToml())
        })
        .finally(() => {
          setIsLoadingToml(false)
        })
    },
    [cleanToml]
  )

  useEffect(() => {
    loadToml(props.issuer)
  }, [loadToml, props])

  const handleSubmit = async (): Promise<void> => {
    setIsLoadingSubmit(true)
    setError('')

    FactoryService.postToml(toml)
      .then(async response => {
        fileDownload(response.data, 'stellar.toml')
        setIsSuccess(true)

        setTimeout(
          function (): void {
            setIsSuccess(false)
          }.bind(this),
          5000
        )
      })
      .catch(e => {
        const responseError = e.response?.data
        handleSubmitErrors(responseError, e.response?.data?.code, setError)
      })
      .finally(() => {
        setIsLoadingSubmit(false)
      })
  }

  return (
    <div>
      {isLoadingToml ? (
        <CustomLoader />
      ) : (
        <Card variant={Card.variant.highlight}>
          <div className={styles.helper}>
            <FabHelper
              onClick={(): void => props.setShowHelper(TabsManagementEnum.TOML)}
              variant={FabHelperVariant.fixedRight}
            />
          </div>
          <AccordionGeneralInfo toml={toml} setToml={setToml} />
          <AccordionOrgDoc toml={toml} setToml={setToml} />
          <AccordionCurrencyDoc toml={toml} setToml={setToml} />
          <AccordionContact toml={toml} setToml={setToml} />

          <div className={styles.contentSubmit}>
            <Button isLoading={isLoadingSubmit} onClick={handleSubmit}>
              Generate TOML
            </Button>
          </div>
          {error && <CustomError message={error} />}
          <br />
          {isSuccess && (
            <InfoBlock variant={InfoBlock.variant.success}>
              <div>
                <p>
                  Operation completed successfully! Your TOML file will be
                  downloaded
                </p>
              </div>
            </InfoBlock>
          )}
        </Card>
      )}
    </div>
  )
}

export { GenerateToml }
