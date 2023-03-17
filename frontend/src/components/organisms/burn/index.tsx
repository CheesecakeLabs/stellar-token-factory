import {
  Dispatch,
  FunctionComponent,
  SetStateAction,
  useCallback,
  useEffect,
  useState,
} from 'react'
import { Button, Card, IconButton, Input } from '@stellar/design-system'
import {
  CustomError,
  ConfirmModal,
  TokenMessage,
  FabHelper,
  FabHelperVariant,
  Column,
  CustomLoader,
  LastUpdated,
  Row,
} from 'components/atoms'
import { getPublicKey } from '@stellar/freighter-api'
import { Key } from 'react-feather'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { getInitialBurn, burnErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { TabsManagementEnum } from 'components/templates'
import { CardInfo } from 'components/molecules'
import { IBurnInfo } from 'services/factory/interfaces'
import { ListBurnTransactions } from './list-burn-transactions'
import { ChartBurn } from './chart-burn'

export interface IBurnProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
  isDarkMode: boolean | undefined
}

const Burn: FunctionComponent<IBurnProps> = props => {
  const [isModalVisible, setModalVisible] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(getInitialBurn(props.distribution))
  const [inputsErrors, setInputsErrors] = useState(burnErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)
  const [isLoadingInfo, setLoadingInfo] = useState(false)
  const [infoData, setinfoData] = useState<IBurnInfo>()

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    cleanFields(event.target.name)
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const getKey = async (field: string): Promise<void> => {
    cleanFields(field)
    const publicKey = await getPublicKey()
    setInputs(values => ({ ...values, [field]: publicKey }))
  }

  const cleanFields = (field: string): void => {
    setError('')
    setResponseSubmit(defaultResponseSubmit)
    setInputsErrors(values => ({ ...values, [field]: '' }))
  }

  const handleSubmit = async (): Promise<void> => {
    setModalVisible(false)
    setIsLoading(true)
    setError('')

    FactoryService.postBurn(
      props.issuer,
      inputs.distributor,
      props.assetCode,
      inputs.amount
    )
      .then(async response => {
        const result = await FreighterService.requestSignatures(response.data)
        await postEnvelopeXdr(result)
      })
      .catch(e => {
        const responseError = e.response?.data
        handleSubmitErrors(
          responseError,
          e.response?.data?.code,
          error,
          setInputsErrors,
          setError
        )
      })
      .finally(() => {
        setIsLoading(false)
      })
  }

  const postEnvelopeXdr = async (xdr: string): Promise<void> => {
    await FactoryService.postEnvelope(xdr)
      .then(async response => {
        setResponseSubmit(response.data)
        setInputs(getInitialBurn(props.distribution))
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  const closeModal = (): void => {
    setModalVisible(false)
    setIsLoading(false)
  }

  const validateDistribution = (): void => {
    if (validateInputError(inputs, setInputsErrors, setError)) {
      setIsLoading(false)
      return
    }
    if (props.distribution == inputs.distributor) {
      handleSubmit()
      return
    }
    setModalVisible(true)
  }

  const getData = useCallback(() => {
    setLoadingInfo(true)
    FactoryService.getBurnInfo()
      .then(response => {
        setinfoData(response.data)
      })
      .catch(() => {
        setError('An error occurred while loading the informations')
      })
      .finally(() => {
        setLoadingInfo(false)
      })
  }, [])

  useEffect(() => {
    getData()
  }, [getData])

  return (
    <>
      <Card variant={Card.variant.highlight}>
        {false && (
          <FabHelper
            onClick={(): void => props.setShowHelper(TabsManagementEnum.BURN)}
            variant={FabHelperVariant.fixedRight}
          />
        )}
        <div className={styles.fieldAmount}>
          <Input
            name="amount"
            id="input-amount"
            label="Amount"
            placeholder="Asset amount you want to burn"
            type="number"
            value={inputs.amount || ''}
            onChange={handleChange}
            error={inputsErrors.amount}
            autoComplete="off"
            min={0}
          />
        </div>
        <Input
          name="distributor"
          id="input-recipient-address"
          label="From Distribution Address"
          placeholder="Address will lost the assets"
          value={inputs.distributor || ''}
          onChange={handleChange}
          error={inputsErrors.distributor}
          autoComplete="off"
          rightElement={
            <IconButton
              altText="Get Public Key"
              icon={<Key key="key-distributor" />}
              onClick={(): Promise<void> => getKey('distributor')}
            />
          }
        />
        <div className={styles.contentSubmit}>
          <Button isLoading={isLoading} onClick={validateDistribution}>
            Burn
          </Button>
        </div>
        {error ? <CustomError message={error} /> : <div />}
        <ConfirmModal
          isModalVisible={isModalVisible}
          closeModal={closeModal}
          submit={handleSubmit}
          message={
            'Make sure to use the Tresury Wallet for the burning process. Are you sure you want to change this address?'
          }
        />
        <TokenMessage
          hash={responseSubmit.transaction_hash}
          link={responseSubmit.transaction_link}
        />
      </Card>
      {isLoadingInfo ? (
        <CustomLoader />
      ) : (
        <div>
          <Row>
            <Column col={4}>
              <CardInfo
                label={'Total supply'}
                value={infoData?.total_supply}
                description={infoData?.symbol}
              />
              <CardInfo
                label={'Total in-circulation'}
                value={infoData?.total_in_circulation}
                description={infoData?.symbol}
              />
              <CardInfo
                label={'Total burn transactions'}
                value={infoData?.total_burn_transactions}
              />
              <CardInfo
                label={'Total reserves'}
                value={infoData?.total_reserves}
              />
            </Column>
            <Column col={8}>
              <ChartBurn
                label={'Burned amount'}
                isDarkMode={props.isDarkMode}
              />
              <ListBurnTransactions
                isLoading={isLoading}
                data={infoData?.last_transactions || []}
              />
            </Column>
          </Row>
          <LastUpdated date={infoData?.last_updated} />
        </div>
      )}
    </>
  )
}

export { Burn }
