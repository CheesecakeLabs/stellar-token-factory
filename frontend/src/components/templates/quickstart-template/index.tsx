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
          projectTitle="Token Factory"
          projectLink=""
          contentRight={
            <div className={styles.logo}>
              <Logo width={24} height={24} fill="#0058FF" />
              <Cheesecake height={19} fill="var(--pal-text-primary)" />
            </div>
          }
        />
        <Layout.Inset>
          <Card variant={Card.variant.highlight}>
            <div className={styles.content}>
              <h3>Welcome to the Token Factory</h3>
              <p>
                The Token Factory is a sandbox supported by the Stellar
                Development Foundation and Cheesecake Labs for the public to
                experiment with token issuance on the Stellar testnet network.
              </p>
              <p>
                To use the sandbox, users will need to have a Freighter wallet,
                available{' '}
                <a href="https://www.freighter.app/" target="_blank">
                  here
                </a>
                . Users will need to create two accounts in Freighter–one for
                the issuer account and a second for the distribution account in
                the Token Factory. Please set Freighter to testnet (and not
                mainnet).
              </p>
              <p>
                We encourage you to play around with the Token Factory and learn
                more about Stellar’s asset issuer control functions and the ease
                with which tokens can be issued. For more information on
                Stellar, please see our developer{' '}
                <a href="https://developers.stellar.org/docs" target="_blank">
                  website
                </a>
                .
              </p>{' '}
              <p>
                To speak with technical staff or potential business
                opportunities, please reach out to{' '}
                <a href="mailto:partnerships@stellar.org">
                  partnerships@stellar.org
                </a>
                .
              </p>
              <br />
              <Button onClick={goToHome}>Access Token Factory</Button>
            </div>
          </Card>
        </Layout.Inset>
      </Layout.Content>
    </main>
  )
}

export { QuickstartTemplate }
