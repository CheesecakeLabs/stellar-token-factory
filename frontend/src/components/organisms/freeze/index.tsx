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
  Column,
  ConfirmModal,
  CustomError,
  CustomLoader,
  FabHelper,
  FabHelperVariant,
  LastUpdated,
  Row,
  TokenMessage,
} from 'components/atoms'
import { getPublicKey } from '@stellar/freighter-api'
import { Key } from 'react-feather'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { defaultFreeze, freezeErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { UnauthorizedMessage } from 'components/atoms/unauthorized-message'
import { TabsManagementEnum } from 'components/templates'
import { CardInfo } from 'components/molecules'
import { IFreezeInfo } from 'services/factory/interfaces'
import { ListFrozenAccounts } from './list-frozen-accounts'

export interface IFreezeProps {
  distribution: string
  assetCode: string
  issuer: string
  authorized: boolean
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const Freeze: FunctionComponent<IFreezeProps> = props => {
  const [isLoadingFreeze, setIsLoadingFreeze] = useState(false)
  const [isLoadingUnfreeze, setIsLoadingUnfreeze] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(defaultFreeze)
  const [inputsErrors, setInputsErrors] = useState(freezeErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)
  const [isModalVisible, setModalVisible] = useState(false)
  const [isFreeze, setIsFreeze] = useState(false)
  const [isLoadingInfo, setLoadingInfo] = useState(false)
  const [infoData, setinfoData] = useState<IFreezeInfo>()

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

  const handleSubmit = async (isFreeze: boolean): Promise<void> => {
    setModalVisible(false)
    isFreeze ? setIsLoadingFreeze(true) : setIsLoadingUnfreeze(true)
    setError('')

    FactoryService.postFreeze(
      props.issuer,
      props.assetCode,
      inputs.target,
      inputs.memo_text,
      isFreeze
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
        isFreeze ? setIsLoadingFreeze(false) : setIsLoadingUnfreeze(false)
      })
  }

  const postEnvelopeXdr = async (xdr: string): Promise<void> => {
    await FactoryService.postEnvelope(xdr)
      .then(async response => {
        setResponseSubmit(response.data)
        setInputs(defaultFreeze)
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  const closeModal = (): void => {
    setModalVisible(false)
  }

  const confirmOperation = (isFreeze: boolean): void => {
    if (validateInputError(inputs, setInputsErrors, setError)) {
      return
    }
    setIsFreeze(isFreeze)
    setModalVisible(true)
  }

  const getData = useCallback(() => {
    setLoadingInfo(true)
    FactoryService.getFreezeInfo()
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
            onClick={(): void => props.setShowHelper(TabsManagementEnum.FREEZE)}
            variant={FabHelperVariant.fixedRight}
          />
        )}
        {props.authorized ? (
          <div>
            <Input
              name="target"
              id="input-target"
              label="Target Address"
              placeholder="Target Address"
              value={inputs.target || ''}
              onChange={handleChange}
              error={inputsErrors.target}
              autoComplete="off"
              rightElement={
                <IconButton
                  altText="Get Public Key"
                  icon={<Key key="target" />}
                  onClick={(): Promise<void> => getKey('target')}
                />
              }
            />
            <div className={styles.fieldInfo}>
              <Input
                name="memo_text"
                id="input-memo-text"
                label="Memo text"
                placeholder="Memo text"
                value={inputs.memo_text || ''}
                onChange={handleChange}
                error={inputsErrors.memo_text}
                autoComplete="off"
                maxLength={28}
              />
            </div>
            <div className={styles.contentSubmit}>
              <Button
                isLoading={isLoadingFreeze}
                onClick={(): void => confirmOperation(true)}
                key="freeze"
              >
                Freeze
              </Button>
              <Button
                isLoading={isLoadingUnfreeze}
                onClick={(): void => confirmOperation(false)}
                variant={Button.variant.tertiary}
                key="unfreeze"
              >
                Unfreeze
              </Button>
            </div>
            {error ? <CustomError message={error} /> : <div />}
            <ConfirmModal
              isModalVisible={isModalVisible}
              closeModal={closeModal}
              submit={(): Promise<void> => handleSubmit(isFreeze)}
              message={`You will ${
                isFreeze ? 'freeze' : 'unfreeze'
              } this target, are you sure?`}
            />
            <TokenMessage
              hash={responseSubmit.transaction_hash}
              link={responseSubmit.transaction_link}
            />
          </div>
        ) : (
          <UnauthorizedMessage message="You are not authorized to perform Freeze, please check permission in settings" />
        )}
      </Card>
      {isLoadingInfo ? (
        <CustomLoader />
      ) : (
        <div>
          <Row>
            <Column col={8}>
              <ListFrozenAccounts
                isLoading={isLoadingInfo}
                data={infoData?.frozen_accounts || []}
              />
            </Column>
            <Column col={4}>
              <CardInfo
                label={'Total frozen accounts'}
                value={infoData?.total_frozen_accounts}
              />
            </Column>
          </Row>
          <LastUpdated date={infoData?.last_updated} />
        </div>
      )}
    </>
  )
}

export { Freeze }
