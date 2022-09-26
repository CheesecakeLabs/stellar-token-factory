import { FunctionComponent } from 'react'
import { CustomLoader } from 'components/atoms'
import {
  Mint,
  Burn,
  Transfer,
  HomeDomain,
  GenerateToml,
  Freeze,
  Clawback,
} from 'components/molecules'
import { Tabs, TabList, Tab, TabPanel } from 'react-tabs'
import styles from './styles.module.scss'

export interface ITabsManagementProps {
  treasury: string
  issuer: string
  assetCode: string
  isLoading: boolean,
  isFreeze: boolean,
  isClawback: boolean
}

const TabsManagement: FunctionComponent<ITabsManagementProps> = props => {
  return (
    <div>
      {props.isLoading ? (
        <CustomLoader />
      ) : (
        <div>
          <Tabs
            direction={'rtl'}
            selectedTabClassName={styles.selectedTabClassName}
          >
            <TabList>
              <Tab className={styles.tab}>Mint</Tab>
              <Tab className={styles.tab}>Burn</Tab>
              <Tab className={styles.tab}>Transfer</Tab>
              <Tab className={styles.tab}>Home Domain</Tab>
              <Tab className={styles.tab}>Generate TOML</Tab>
              <Tab className={props.isFreeze ? styles.tab : [styles.tab, styles.tabUnauthorized]}>Freeze</Tab>
              <Tab className={props.isClawback ? styles.tab : [styles.tab, styles.tabUnauthorized]}>Clawback</Tab>
            </TabList>
            <TabPanel>
              <Mint
                treasury={props.treasury}
                issuer={props.issuer}
                assetCode={props.assetCode}
              />
            </TabPanel>
            <TabPanel>
              <Burn
                treasury={props.treasury}
                issuer={props.issuer}
                assetCode={props.assetCode}
              />
            </TabPanel>
            <TabPanel>
              <Transfer
                treasury={props.treasury}
                issuer={props.issuer}
                assetCode={props.assetCode}
              />
            </TabPanel>
            <TabPanel>
              <HomeDomain issuer={props.issuer} />
            </TabPanel>
            <TabPanel>
              <GenerateToml issuer={props.issuer} />
            </TabPanel>
            <TabPanel>
              <Freeze
                treasury={props.treasury}
                issuer={props.issuer}
                assetCode={props.assetCode}
                authorized={props.isFreeze}
              />
            </TabPanel>
            <TabPanel>
              <Clawback
                treasury={props.treasury}
                issuer={props.issuer}
                assetCode={props.assetCode}
                authorized={props.isClawback}
              />
            </TabPanel>
          </Tabs>
        </div>
      )}
    </div>
  )
}

export { TabsManagement }
