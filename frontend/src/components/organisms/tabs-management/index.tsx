import { Dispatch, FunctionComponent, SetStateAction } from 'react'
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
import { TabsManagementEnum } from 'components/templates'

export interface ITabsManagementProps {
  distribution: string
  issuer: string
  assetCode: string
  isLoading: boolean
  isFreeze: boolean
  isClawback: boolean
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
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
              <Tab
                className={
                  props.isFreeze
                    ? styles.tab
                    : [styles.tab, styles.tabUnauthorized]
                }
              >
                Freeze
              </Tab>
              <Tab
                className={
                  props.isClawback
                    ? styles.tab
                    : [styles.tab, styles.tabUnauthorized]
                }
              >
                Clawback
              </Tab>
            </TabList>
            <TabPanel>
              <Mint
                distribution={props.distribution}
                issuer={props.issuer}
                assetCode={props.assetCode}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <Burn
                distribution={props.distribution}
                issuer={props.issuer}
                assetCode={props.assetCode}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <Transfer
                distribution={props.distribution}
                issuer={props.issuer}
                assetCode={props.assetCode}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <HomeDomain
                issuer={props.issuer}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <GenerateToml
                issuer={props.issuer}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <Freeze
                distribution={props.distribution}
                issuer={props.issuer}
                assetCode={props.assetCode}
                authorized={props.isFreeze}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
            <TabPanel>
              <Clawback
                distribution={props.distribution}
                issuer={props.issuer}
                assetCode={props.assetCode}
                authorized={props.isClawback}
                setShowHelper={props.setShowHelper}
              />
            </TabPanel>
          </Tabs>
        </div>
      )}
    </div>
  )
}

export { TabsManagement }
