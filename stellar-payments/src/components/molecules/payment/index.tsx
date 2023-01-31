import { Dispatch, SetStateAction, useState } from 'react'

import { InfoCircleFilled } from '@ant-design/icons'
import { Radio, RadioChangeEvent } from 'antd'
import { toCurrency, toEur, toUsd } from 'services/utils/utils'

import {
  Row,
  RowContent,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { TypePayment } from 'components/enums'
import { BlockchainIcon, FinanceIcon } from 'components/icons'

import styles from './styles.module.scss'

interface IEstimatedCost {
  amount: number
  payment: Hooks.UsePaymentTypes.IPayment | undefined
  formPayment: TypePayment | undefined
  setFormPayment: Dispatch<SetStateAction<TypePayment | undefined>>
}

export const Payment: React.FC<IEstimatedCost> = ({
  amount,
  payment,
  setFormPayment,
  formPayment,
}) => {
  const [isOpenStellarPay, setOpenStellarPay] = useState(false)
  const [isOpenWireTransfer, setOpenWireTransfer] = useState(false)

  const onChange = (e: RadioChangeEvent): void => {
    setFormPayment(e.target.value)
  }

  const setPayment = (type: TypePayment): void => {
    if (type == TypePayment.stellar) {
      setOpenStellarPay(true)
    }
    if (type == TypePayment.wire) {
      setOpenWireTransfer(true)
    }
    setFormPayment(type)
  }

  return (
    <div className={styles.container}>
      <Typography
        variant={TypographyVariant.label}
        text={`Form of payment`}
        className={styles.message}
      />
      <div className={styles.containerCosts}>
        <Row justifyContent={RowContent.spaceBetween}>
          <Typography
            variant={TypographyVariant.label}
            text={'Payment amount'}
            className={styles.label}
          />
          <Typography
            variant={TypographyVariant.p}
            text={toUsd(amount)}
            className={styles.value}
          />
        </Row>
      </div>

      <Radio.Group onChange={onChange} value={formPayment}>
        <div
          className={styles.containerFormPayment}
          onClick={(): void => setPayment(TypePayment.wire)}
        >
          <Radio value={TypePayment.wire} />
          <div className={styles.formPayment}>
            <div className={styles.containerTitle}>
              <FinanceIcon width={48} height={32} />
              <Typography
                variant={TypographyVariant.p}
                text={'Wire Transfer'}
                className={styles.title}
              />
            </div>
            {isOpenWireTransfer && (
              <>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Fees'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={`${toEur(20)}`}
                    className={styles.value}
                  />
                </Row>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'ETA'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={'2 - 5 days'}
                    className={styles.value}
                  />
                </Row>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Exchange'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={`${toCurrency(payment?.usd_price ?? 0)} USD/EUR`}
                    className={styles.value}
                  />
                </Row>
                <div className={styles.divider} />
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Final cost'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={toEur(
                      payment
                        ? payment?.final_cost + 20
                        : 0
                    )}
                    className={styles.value}
                  />
                </Row>
              </>
            )}
          </div>
        </div>

        <div
          className={styles.containerFormPayment}
          onClick={(): void => setPayment(TypePayment.stellar)}
        >
          <Radio value={TypePayment.stellar} />
          <div className={styles.formPayment}>
            <div className={styles.containerTitle}>
              <BlockchainIcon width={48} height={48} />
              <Typography
                variant={TypographyVariant.p}
                text={'Stellar pay'}
                className={styles.title}
              />
            </div>
            {isOpenStellarPay && payment && (
              <>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Fees'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={'< € 0.01'}
                    className={styles.value}
                  />
                </Row>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'ETA'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={'< 10s'}
                    className={styles.value}
                  />
                </Row>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Exchange'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={`${toCurrency(payment?.usd_price)} USD/EUR`}
                    className={styles.value}
                  />
                </Row>
                <div className={styles.divider} />
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Final cost'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={toEur(payment.final_cost)}
                    className={styles.value}
                  />
                </Row>
                {payment.required_signatures.length > 0 && (
                  <div className={styles.requestSignature}>
                    <InfoCircleFilled style={{ fontSize: '16px' }} />
                    <Typography
                      variant={TypographyVariant.label}
                      text={`0/2 approvals required`}
                      className={styles.signatures}
                    />
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </Radio.Group>
    </div>
  )
}
