import React, { useState } from 'react'

import { DollarOutlined } from '@ant-design/icons'

import {
  Button,
  ButtonVariant,
  Row,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { ArrowDown, ArrowUp } from 'components/icons'

import { ModalStellarPay } from '../modal-stellar-pay'
import styles from './styles.module.scss'

interface IItemPayeeProps {
  payee: Hooks.UsePayeesTypes.IPayee
}

export const ItemPayee: React.FC<IItemPayeeProps> = (
  props: IItemPayeeProps
) => {
  const [isExpanded, setExpanded] = useState(false)
  const [isOpenStellarPay, setModalStellarPay] = useState(false)

  const openModalStellar = (
    event: React.MouseEvent<HTMLButtonElement>
  ): void => {
    event.stopPropagation()
    setModalStellarPay(true)
  }

  return (
    <>
      <ModalStellarPay
        isOpen={isOpenStellarPay}
        setOpenModal={setModalStellarPay}
        payee={props.payee}
      />
      <tr onClick={(): void => setExpanded(!isExpanded)}>
        <td className={styles.tdDetails}>
          {isExpanded ? (
            <ArrowUp width={12} height={12} className={styles.arrow} />
          ) : (
            <ArrowDown width={12} height={12} className={styles.arrow} />
          )}
        </td>
        <td>{props.payee.name}</td>
        <td className={styles.tdPhone}>{props.payee.phone}</td>
        <td className={styles.alignEnd}>
          <Row>
            <Button
              variant={ButtonVariant.primary}
              label={'Create payment order'}
              icon={<DollarOutlined />}
              onClick={openModalStellar}
            />
          </Row>
        </td>
      </tr>
      {isExpanded && (
        <tr className={styles.expandable}>
          <td colSpan={6}>
            <div className={styles.containerDatails}>
              <Typography
                variant={TypographyVariant.label}
                text={'Address'}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={props.payee.address}
                className={styles.value}
              />
              <div className={styles.detailPhone}>
                <Typography
                  variant={TypographyVariant.label}
                  text={'Phone'}
                  className={styles.label}
                />
                <Typography
                  variant={TypographyVariant.p}
                  text={props.payee.phone}
                  className={styles.value}
                />
              </div>
              <Typography
                variant={TypographyVariant.label}
                text={'Bank account'}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={props.payee.bank_account}
                className={styles.value}
              />
              <Typography
                variant={TypographyVariant.label}
                text={'Stellar wallet'}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={props.payee.stellar_wallet}
                className={styles.value}
              />
            </div>
          </td>
        </tr>
      )}
    </>
  )
}
