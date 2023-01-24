import React, { useState } from 'react'

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

  return (
    <>
      <ModalStellarPay
        isOpen={isOpenStellarPay}
        setOpenModal={setModalStellarPay}
        payee={props.payee}
      />
      <tr>
        <td
          className={styles.tdDetails}
          onClick={(): void => setExpanded(!isExpanded)}
        >
          {isExpanded ? (
            <ArrowUp width={12} height={12} className={styles.arrow} />
          ) : (
            <ArrowDown width={12} height={12} className={styles.arrow} />
          )}
        </td>
        <td>{props.payee.name}</td>
        <td>{props.payee.phone}</td>
        <td className={styles.alignEnd}>
          <Row>
            <Button
              variant={ButtonVariant.secondary}
              label={'Wire Transfer'}
              onClick={(): void => setModalStellarPay(true)}
            />
            <Button
              variant={ButtonVariant.primary}
              label={'Stellar Pay'}
              onClick={(): void => setModalStellarPay(true)}
            />
          </Row>
        </td>
      </tr>
      {isExpanded && (
        <tr className={styles.expandable}>
          <td className="uk-background-muted" colSpan={6}>
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
