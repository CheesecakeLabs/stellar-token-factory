import { Typography, TypographyVariant } from 'components/atoms'

import styles from './styles.module.scss'

const Home = (): JSX.Element => {
  return (
    <main>
      <header className={styles.header}></header>
      <div className={styles.container}>
        <div className={styles.containerInfo}>
          <Typography
            variant={TypographyVariant.p}
            text={'Payees'}
            className={styles.headerText}
          />
        </div>
        <div className={styles.containerList}>
          <table>
            <thead>
              <tr>
                <th>Company name</th>
                <th>Phone</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>ACME Technologies Inc.</td>
                <td>805-555-0196</td>
                <td></td>
              </tr>
              <tr>
                <td>Ziemann-Mills</td>
                <td>701-555-0114</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  )
}

export default Home
