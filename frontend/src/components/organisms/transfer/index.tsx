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
import { getInitialTransfer, transferErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { TabsManagementEnum } from 'components/templates'
import { CardInfo } from 'components/molecules'
import { ITransferInfo } from 'services/factory/interfaces'
import { ChartTransfer } from './chart-transfer'
import { ListTransferTransactions } from './list-transfer-transactions'

export interface ITransferProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const Transfer: FunctionComponent<ITransferProps> = props => {
  const [isModalVisible, setModalVisible] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(getInitialTransfer(props.distribution))
  const [inputsErrors, setInputsErrors] = useState(transferErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)
  const [isLoadingInfo, setLoadingInfo] = useState(false)
  const [infoData, setinfoData] = useState<ITransferInfo>()

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

    FactoryService.postTransfer(
      props.issuer,
      inputs.distributor,
      props.assetCode,
      inputs.amount,
      inputs.recipient
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
        setInputs(getInitialTransfer(props.distribution))
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
    FactoryService.getTransferInfo()
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
            onClick={(): void =>
              props.setShowHelper(TabsManagementEnum.TRANSFER)
            }
            variant={FabHelperVariant.fixedRight}
          />
        )}
        <div className={styles.fieldAmount}>
          <Input
            name="amount"
            id="input-amount"
            label="Amount"
            placeholder="Asset amount you want to transfer"
            type="number"
            value={inputs.amount || ''}
            onChange={handleChange}
            error={inputsErrors.amount}
            autoComplete="off"
            min={0}
          />
        </div>
        <div className={styles.fieldDistribution}>
          <Input
            name="distributor"
            id="input-recipient-address"
            label="Source (Distribution Address)"
            placeholder="Distribution Address"
            value={inputs.distributor || ''}
            onChange={handleChange}
            error={inputsErrors.distributor}
            autoComplete="off"
            rightElement={
              <IconButton
                altText="Get Public Key"
                icon={<Key key="distributor" />}
                onClick={(): Promise<void> => getKey('distributor')}
              />
            }
          />
        </div>
        <Input
          name="recipient"
          id="input-recipient-address"
          label="Recipient Address"
          placeholder="Address will receive the new assets"
          value={inputs.recipient || ''}
          onChange={handleChange}
          error={inputsErrors.target}
          autoComplete="off"
          rightElement={
            <IconButton
              altText="Get Public Key"
              icon={<Key key="recipient" />}
              onClick={(): Promise<void> => getKey('recipient')}
            />
          }
        />
        <div className={styles.contentSubmit}>
          <Button isLoading={isLoading} onClick={validateDistribution}>
            Transfer
          </Button>
        </div>
        {error ? <CustomError message={error} /> : <div />}
        <ConfirmModal
          isModalVisible={isModalVisible}
          closeModal={closeModal}
          submit={handleSubmit}
          message={
            'Make sure to use the Tresury Wallet to transfer the asset. Are you sure you want to change this address?'
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
          <ChartTransfer label={'Amount and volume of transfer transactions'} />
          <Row>
            <Column col={8}>
              <ListTransferTransactions
                isLoading={isLoading}
                data={infoData?.last_transactions || []}
              />
            </Column>
            <Column col={4}>
              <CardInfo
                label={'Total amount transfered'}
                value={infoData?.total_amount_transfered}
                description={'COIN'}
              />
              <CardInfo
                label={'Total transfer transactions'}
                value={infoData?.total_transfer_transactions}
                description={'COIN'}
              />
            </Column>
          </Row>
          <LastUpdated date={infoData?.last_updated} />
        </div>
      )}
    </>
  )
}

export { Transfer }
