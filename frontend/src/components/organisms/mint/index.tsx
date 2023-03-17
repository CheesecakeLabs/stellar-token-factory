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
  LastUpdated,
  Row,
  CustomLoader,
} from 'components/atoms'
import { getPublicKey } from '@stellar/freighter-api'
import { Key } from 'react-feather'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { getInitialMint, mintErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { TabsManagementEnum } from 'components/templates'
import { CardInfo } from 'components/molecules'
import { IMintInfo } from 'services/factory/interfaces'
import { ListMintTransactions } from './list-mint-transactions'
import { ChartMint } from './chart-mint'

export interface IMintProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
  isDarkMode: boolean | undefined
}

const Mint: FunctionComponent<IMintProps> = props => {
  const [isModalVisible, setModalVisible] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(getInitialMint(props.distribution))
  const [inputsErrors, setInputsErrors] = useState(mintErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)
  const [isLoadingInfo, setLoadingInfo] = useState(false)
  const [infoData, setinfoData] = useState<IMintInfo>()

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

    FactoryService.postMint(
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
        setInputs(getInitialMint(props.distribution))
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
    FactoryService.getMintInfo()
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
    <div>
      <Card variant={Card.variant.highlight}>
        {false && (
          <FabHelper
            onClick={(): void => props.setShowHelper(TabsManagementEnum.MINT)}
            variant={FabHelperVariant.fixedRight}
          />
        )}
        <div className={styles.fieldAmount}>
          <Input
            name="amount"
            id="input-amount"
            label="Amount"
            placeholder="New asset amount you want to mint"
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
          label="To Distribution Address"
          placeholder="Address will receive the new assets"
          value={inputs.distributor || ''}
          onChange={handleChange}
          error={inputsErrors.distributor}
          autoComplete="off"
          rightElement={
            <IconButton
              altText="Get Public Key"
              icon={<Key key="key" />}
              onClick={(): Promise<void> => getKey('distributor')}
            />
          }
        />
        <div className={styles.contentSubmit}>
          <Button isLoading={isLoading} onClick={validateDistribution}>
            Mint
          </Button>
        </div>
        {error ? <CustomError message={error} /> : <div />}
        <ConfirmModal
          isModalVisible={isModalVisible}
          closeModal={closeModal}
          submit={handleSubmit}
          message={
            'Make sure to use the Tresury Wallet for the minting process. Are you sure you want to change this address?'
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
                label={'Total mint transactions'}
                value={infoData?.total_mint_transactions}
              />
              <CardInfo
                label={'Total reserves'}
                value={infoData?.total_reserves}
              />
            </Column>
            <Column col={8}>
              <ChartMint
                label={'Minted amount'}
                isDarkMode={props.isDarkMode}
              />
              <ListMintTransactions
                isLoading={isLoading}
                data={infoData?.last_transactions || []}
              />
            </Column>
          </Row>
          <LastUpdated date={infoData?.last_updated} />
        </div>
      )}
    </div>
  )
}

export { Mint }
