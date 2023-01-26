import { FunctionComponent, useRef, useState } from 'react'
import {
  Button,
  Checkbox,
  Input,
  Select,
  Tooltip,
} from '@stellar/design-system'
import styles from './styles.module.scss'
import { ICurrency, inputsCurrencyDoc } from '../generate-toml/constants'
import { Info } from 'react-feather'

export interface IFormCurrencyDocProps {
  isModalVisible: boolean
  closeModal: () => void
  addValue: (
    currency: ICurrency,
    isEdit: boolean,
    oldCurrency: ICurrency
  ) => void
  initialValues: ICurrency
}

const FormCurrencyDoc: FunctionComponent<IFormCurrencyDocProps> = props => {
  const myRef = useRef(null)
  const [inputs, setInputs] = useState(props.initialValues)

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const handleAdd = (): void => {
    props.addValue(inputs, isEdit(), props.initialValues)
    setInputs(inputsCurrencyDoc)
    props.closeModal()
  }

  const isEdit = (): boolean => {
    return props.initialValues != inputsCurrencyDoc
  }

  const isInvalidForm = (): boolean => {
    if (inputs.image) {
      return !isValidHttpUrl(inputs.image)
    }
    if (inputs.attestation_of_reserve) {
      return !isValidHttpUrl(inputs.attestation_of_reserve)
    }
    return inputs == inputsCurrencyDoc
  }

  function isValidHttpUrl(inputUrl: string): boolean {
    let url
    try {
      url = new URL(inputUrl)
    } catch (_) {
      return false
    }
    return url.protocol === 'http:' || url.protocol === 'https:'
  }

  return (
    <>
      <div className={styles.darkBG} onClick={props.closeModal} />
      <div className={styles.centered}>
        <div className={styles.modal} ref={myRef}>
          <Input
            name="issuer"
            id="input-issuer"
            label={
              <label>
                <Tooltip content="Asset issuer Stellar public key">
                  Issuer <Info size={14} className={styles.iconTooltip} />
                </Tooltip>
              </label>
            }
            placeholder="Issuer"
            autoComplete="off"
            value={inputs.issuer}
            onChange={handleChange}
          />

          <div className={styles.contentForm}>
            <Input
              name="name"
              id="input-name"
              label={
                <label>
                  <Tooltip content="A short name for the asset">
                    Name <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              placeholder="Name"
              autoComplete="off"
              value={inputs.name}
              onChange={handleChange}
            />
            <div className={styles.spacer} />
            <Input
              name="code"
              id="input-code"
              label={
                <label>
                  <Tooltip content="Asset code">
                    Code <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              placeholder="Code"
              autoComplete="off"
              value={inputs.code}
              onChange={handleChange}
            />
            <div className={styles.spacer} />
            <Input
              name="anchor_asset"
              id="input-anchor-asset"
              label={
                <label>
                  <Tooltip content="If anchored asset, code / symbol for asset that asset is anchored to">
                    Anchor asset{' '}
                    <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              placeholder="Anchor Asset"
              autoComplete="off"
              value={inputs.anchor_asset}
              onChange={handleChange}
            />
          </div>
          <Input
            name="desc"
            id="input-desc"
            label={
              <label>
                <Tooltip content="Description of asset and what it represents">
                  Description <Info size={14} className={styles.iconTooltip} />
                </Tooltip>
              </label>
            }
            placeholder="Description"
            autoComplete="off"
            value={inputs.desc}
            onChange={handleChange}
          />
          <div className={styles.contentForm}>
            <Select
              name="status"
              id="status"
              label={
                <label>
                  <Tooltip content="Status of asset. One of live, dead, test, or private.">
                    Status <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              value={inputs.status}
              onChange={handleChange}
            >
              <option></option>
              <option value="live">Live</option>
              <option value={'dead'}>Dead</option>
              <option value={'test'}>Test</option>
              <option value={'private'}>Private</option>
            </Select>
            <div className={styles.spacer} />
            <Select
              name="anchor_asset_type"
              id="anchor_asset_type"
              label={
                <label>
                  <Tooltip content="Type of asset anchored. Can be fiat, crypto, nft, stock, bond, commodity, realestate, or other.">
                    Anchor Asset Type{' '}
                    <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              value={inputs.anchor_asset_type}
              onChange={handleChange}
            >
              <option></option>
              <option value={'fiat'}>Fiat</option>
              <option value={'crypto'}>Crypto</option>
              <option value={'nft'}>NFT</option>
              <option value={'stock'}>Stock</option>
              <option value={'bond'}>Bond</option>
              <option value={'commodity'}>Commodity</option>
              <option value={'realestate'}>Realestate</option>
              <option value={'other'}>Other</option>
            </Select>
            <div className={styles.checkbox}>
              <Checkbox
                name="is_asset_anchored"
                id="is_asset_anchored"
                label="Is Asset Anchored"
                onChange={handleChange}
                defaultChecked={inputs.is_asset_anchored}
                className={styles.checkbox}
              />
            </div>
          </div>
          <div className={styles.contentForm}>
            <Input
              name="attestation_of_reserve"
              id="input-attestation-of-reserve"
              label={
                <label>
                  <Tooltip content="URL to attestation or other proof, evidence, or verification of reserves, such as third-party audits.">
                    Attestation of reserve{' '}
                    <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              placeholder="URL"
              autoComplete="off"
              value={inputs.attestation_of_reserve}
              onChange={handleChange}
            />
            <div className={styles.spacer} />
            <Input
              name="image"
              id="input-code"
              label={
                <label>
                  <Tooltip content="URL to a PNG image on a transparent background representing asset.">
                    URL Image <Info size={14} className={styles.iconTooltip} />
                  </Tooltip>
                </label>
              }
              placeholder="URL"
              autoComplete="off"
              value={inputs.image}
              onChange={handleChange}
            />
          </div>
          <Input
            name="redemption_instructions"
            id="input-redemption-instructions"
            placeholder="Redemption Instructions"
            autoComplete="off"
            label={
              <label>
                <Tooltip content="If anchored asset, these are instructions to redeem the underlying asset from tokens.">
                  Redemption Instructions{' '}
                  <Info size={14} className={styles.iconTooltip} />
                </Tooltip>
              </label>
            }
            value={inputs.redemption_instructions}
            onChange={handleChange}
          />
          <div className={styles.button}>
            <Button
              variant={Button.variant.tertiary}
              onClick={props.closeModal}
            >
              Cancel
            </Button>
            <div className={styles.spacer} />
            <Button
              variant={Button.variant.primary}
              onClick={handleAdd}
              disabled={isInvalidForm()}
            >
              {isEdit() ? 'Update' : 'Save'}
            </Button>
          </div>
        </div>
      </div>
    </>
  )
}

export { FormCurrencyDoc }
