import React from 'react'
import { useTranslation } from 'react-i18next'

import { Loading } from 'components/atoms'

import { ItemPayee } from '../item-payee'
import styles from './styles.module.scss'

interface IListPayeesProps {
  loading: boolean
  payees: Hooks.UsePayeesTypes.IPayee[] | undefined
}

export const ListPayees: React.FC<IListPayeesProps> = ({ loading, payees }) => {
  const { t } = useTranslation()

  return (
    <div className={styles.container}>
      <table>
        {loading ? (
          <Loading />
        ) : (
          <>
            <thead>
              <tr>
                <th></th>
                <th>{t('company_name')}</th>
                <th className={styles.thPhone}>{t('phone')}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {payees &&
                payees.map(item => {
                  return <ItemPayee payee={item} />
                })}
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
