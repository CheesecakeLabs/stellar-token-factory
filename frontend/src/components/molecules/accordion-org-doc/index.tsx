import { Dispatch, FunctionComponent, SetStateAction, useState } from 'react'
import { Input, Tooltip } from '@stellar/design-system'
import { ArrowDown, ArrowUp, Info } from 'react-feather';

import styles from './styles.module.scss'
import { IToml } from '../generate-toml/constants';

export interface IAccordionOrgDocProps {
  toml: IToml,
  setToml: Dispatch<SetStateAction<IToml>>
}

const AccordionOrgDoc: FunctionComponent<IAccordionOrgDocProps> = (props) => {

  const [isActive, setIsActive] = useState(true);

  const handleChange = (event: { target: { name: string; value: string; }; }): void => {
    const name = event.target.name;
    const value = event.target.value;
    props.toml.org_doc = { ...props.toml.org_doc, [name]: value }
    props.setToml(values => ({ ...values, ['org_doc']: props.toml.org_doc }));
  }

  return (
    <div>
      <div className={styles.accordion}>
        <div className={styles.accordionItem} onClick={(): void => setIsActive(!isActive)}>
          Organization Documentation
          {isActive ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
        </div>
      </div>
      {isActive &&
        <div className={styles.accordionContent}>
          <Input
            name="name"
            id='input-org-name'
            label='ORG Name'
            placeholder='ORG Name'
            value={props.toml.org_doc.name || ''}
            onChange={handleChange}
            autoComplete="off"
          />
          <Input
            name="url"
            id='input-org-url'
            label={<label>
              <Tooltip
                content='This URL must contain https'>
                ORG URL <Info size={14} className={styles.iconTooltip} />
              </Tooltip>
            </label>}
            placeholder='https://'
            value={props.toml.org_doc.url || ''}
            onChange={handleChange}
            autoComplete="off"
          />
          <Input
            name="logo"
            id='input-org-logo'
            label='ORG Logo'
            placeholder='http://'
            value={props.toml.org_doc.logo || ''}
            onChange={handleChange}
            autoComplete="off"
          />
          <Input
            name="description"
            id='input-org-description'
            label='ORG Description'
            placeholder='ORG Description'
            value={props.toml.org_doc.description || ''}
            onChange={handleChange}
            autoComplete="off"
          />
          <Input
            name="physical_address"
            id='input-org-physical-address'
            label='ORG Physical Address'
            placeholder='ORG Physical Address'
            value={props.toml.org_doc.physical_address || ''}
            onChange={handleChange}
            autoComplete="off"
          />
          <div className={styles.contentForm}>
            <Input
              name="twitter"
              id='input-org-twitter'
              label='ORG Twitter'
              placeholder='ORG Twitter'
              value={props.toml.org_doc.twitter || ''}
              onChange={handleChange}
              autoComplete="off"
            />
            <div className={styles.spacer} />
            <Input
              name="github"
              id='input-org-github'
              label='ORG Github'
              placeholder='Github'
              value={props.toml.org_doc.github || ''}
              onChange={handleChange}
              autoComplete="off"
            />
          </div>
          <div className={styles.contentForm}>
            <Input
              name="official_email"
              id='input-org-official-email'
              label='ORG Official Email'
              placeholder='ORG Official Email'
              value={props.toml.org_doc.official_email || ''}
              onChange={handleChange}
              autoComplete="off"
            />
            <div className={styles.spacer} />
            <Input
              name="support_email"
              id='input-org-support-email'
              label='ORG Support Email'
              placeholder='ORG Support Email'
              value={props.toml.org_doc.support_email || ''}
              onChange={handleChange}
              autoComplete="off"
            />
          </div>
        </div>
      }
    </div>
  )
}

export { AccordionOrgDoc }