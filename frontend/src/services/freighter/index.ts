import { getNetwork, signTransaction } from '@stellar/freighter-api';
import { ITransactionResponse } from 'services/factory/interfaces';

const toSign = async (xdr: string, signWith: string): Promise<string> => {
  let signedTransaction = '';
  const network = await getNetwork();
  signedTransaction = await signTransaction(xdr, network == "TESTNET" ? "TESTNET" : "PUBLIC", signWith);
  return signedTransaction;
}

const requestSignatures = async (transaction: ITransactionResponse): Promise<string> => {
  const signatures = transaction.required_signatures;
  let envelopeXdr = transaction.envelope_xdr;
  for (const signature of signatures) {
    envelopeXdr = await FreighterService.toSign(envelopeXdr, signature);
  }
  return envelopeXdr;
}

const FreighterService = {
  toSign,
  requestSignatures
}

export { FreighterService }

