import { Button, Card, Layout } from '@stellar/design-system'
import { useNavigate } from 'react-router-dom'
import { ReactComponent as Logo } from '../../../assets/logo.svg'
import { ReactComponent as Cheesecake } from '../../../assets/cheesecake.svg'

import styles from './styles.module.scss'
import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { useCallback } from 'react'

const QuickstartTemplate = (): JSX.Element => {
  const navigate = useNavigate()

  const goToHome = useCallback(() => {
    navigate('/home')
  }, [navigate])

  return (
    <main className={styles.main}>
      <Layout.Content>
        <Layout.Header
          hasDarkModeToggle
          projectTitle="Stellar Asset Sandbox"
          projectLink=""
          contentRight={
            <a href="https://cheesecakelabs.com/" target="_blank">
              <div className={styles.logo}>
                <Logo width={24} height={24} fill="#0058FF" />
                <Cheesecake height={19} fill="var(--pal-text-primary)" />
              </div>
            </a>
          }
        />
        <Layout.Inset>
          <Card variant={Card.variant.highlight}>
            <div className={styles.content}>
              <h4>Welcome to the Stellar Asset Issuance Sandbox</h4>
              <p>
                The Stellar Asset Sandbox is a sandbox supported by the Stellar
                Development Foundation and Cheesecake Labs for businesses to
                experiment with token issuance on the Stellar testnet network.
              </p>
              <br />
              <br />
              <h4>Requirements</h4>
              <p>
                Before trying the Stellar Asset Sandbox complete the steps below
                then click get started.
              </p>
              <p>
                <table>
                  <tr>
                    <td>
                      <div className={styles.containerStep}>
                        <div className={styles.step}>1</div>
                      </div>
                      <div>Install the Freighter Wallet browser extension.</div>
                    </td>
                    <td>
                      <div className={styles.containerStep}>
                        <div className={styles.step}>2</div>
                      </div>
                      <div>Set Freighter to Testnet.</div>
                    </td>
                    <td>
                      <div className={styles.containerStep}>
                        <div className={styles.step}>3</div>
                      </div>
                      <div>
                        Create 3 Stellar Addresses in Freighter representing
                        your issuing, distribution and recipient accounts.
                      </div>
                    </td>
                  </tr>
                </table>
              </p>
              <div className={styles.getStarted}>
                <Button onClick={goToHome}>Get Started</Button>
              </div>
              <p>
                Questions? To learn more about Asset Issuance on Stellar visit
                stellar.org/asset-issuance or contact our partnerships team at
                <a href="mailto:partnerships@stellar.org">
                  {` partnerships@stellar.org`}
                </a>
                .
              </p>
            </div>
          </Card>
        </Layout.Inset>
      </Layout.Content>
    </main>
  )
}

export { QuickstartTemplate }
