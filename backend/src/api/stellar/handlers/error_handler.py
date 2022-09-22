import json

from stellar_sdk.exceptions import BaseHorizonError
from stellar_sdk.xdr import TransactionResult

tx_codes_map = {
    "tx_failed": "Err: One of the operations failed.",
    "tx_bad_auth": "Err: needs more signatures to complete this operation.",
    "tx_too_early": "Err: The ledger closeTime was before the minTime.",
    "tx_too_late": "Err: The ledger closeTime was after the maxTime.",
    "tx_missing_operation": "Err: No operation was specified.",
    "tx_bad_seq": "Err: sequence number does not match source account.",
    "tx_insufficient_balance": "Err: fee would bring account below reserve.",
    "tx_no_source_account": "Err: source account not found.",
    "tx_insufficient_fee": "Err: fee is too small.",
    "tx_bad_auth_extra": "Err: unused signatures attached to transaction.",
    "tx_internal_error": "Err: an unknown error occurred.",
    "tx_fee_bump_inner_failed": "Err: The fee bump inner transaction failed.",
}

op_codes_map = {
    "op_bad_auth": "Err: needs more signatures to complete this operation.",
    "op_no_source_account": "Err: The source account was not found.",
    "op_not_supported": "Err: The operation is not supported at this time.",
    "op_too_many_subentries": "Err: Max number of subentries (1000) already reached.",
    "op_exceeded_work_limit": "Err: Operation did too much work.",
    "OpMalformed": "Err: The operation is malformed because the source account cannot merge with itself. The destination must be a different account.",
    "op_no_account": "Err: The destination account does not exist.",
    "op_immutable_set": "Err: The source account has AUTH_IMMUTABLE flag set.",
    "op_has_sub_entries": "Err: The source account has trustlines and/or offers.",
    "op_seq_num_too_far": "Err: Source account sequence number is too high.",
    "op_dest_full": "Err: The destination account cannot receive the balance of the source account and still satisfy its lumen buying liabilities.",
    "op_not_supported_yet": "Err: The network hasn’t moved to this protocol change yet. This failure means the network doesn’t support this feature yet",
    "op_data_name_not_found": "Err: Trying to remove a Data Entry that isn’t there. This will happen if Name is set (and Value isn’t) but the Account doesn’t have a DataEntry with that Name.",
    "op_low_reserve": "Err: This account does not have enough XLM to satisfy the minimum XLM reserve increase caused by adding a subentry and still satisfy its XLM selling liabilities. For every new DataEntry added to an account, the minimum reserve of XLM that account must hold increases.",
    "op_data_invalid_name": "Err: Name not a valid string.",
    "op_bad_seq": "Err: The specified bump To sequence number is not a valid sequence number. It must be between 0 and INT64_MAX (9223372036854775807 or 0x7fffffffffffffff).",
}

MESSAGES = {
    "NO_OPERATION_DETAILS": "No operation details found",
}


class StellarErrorHandler:
    """
    Handles, decodes and organizes stellar api errors
    in order to provide a more readable error message

    input: stellar_error  - object required

    output: structured error message - json or string
    """

    def __init__(self, network_passphrase: str, stellar_error: object):
        """
        Initializes the class
        """
        self.network = network_passphrase

        self.stellar_error = stellar_error
        if isinstance(stellar_error, BaseHorizonError):
            self.stellar_error = {
                "title": stellar_error.title,
                "status": stellar_error.status,
                "detail": stellar_error.detail,
                "extras": stellar_error.extras,
                "type": stellar_error.type,
            }

        self.title = self.stellar_error.get("title")
        self.status = self.stellar_error.get("status")
        self.more_details = self.stellar_error.get("detail")
        self.envelope = None
        self.tx_codes = None
        self.message = None
        self.operations = []

        try:
            self.handle_extra_error()
        except Exception as e:
            raise e

    def handle_extra_error(self):
        """
        Handles extra errors
        """
        # List of some fields that come without form in the extra
        more_fields_to_check_in_extra = ["invalid_field", "reason"]

        if self.stellar_error.get("extras"):
            extras = self.stellar_error["extras"]
            tx_result = ""

            # Decode transaction envelope
            envelope_xdr = None
            if "envelope_xdr" in extras:
                try:
                    if extras["envelope_xdr"]:
                        self.envelope = extras["envelope_xdr"]
                except Exception as e:
                    print(e)

            # Get transaction error codes
            if "result_xdr" in extras:
                try:
                    tx_result = TransactionResult.from_xdr(extras["result_xdr"])
                except Exception as e:
                    tx_result = None
                    print(e)

            # Check if there are any info out of the shape of the envelope
            if set(more_fields_to_check_in_extra).issubset(extras):
                checks = {}
                for field in more_fields_to_check_in_extra:
                    if field in extras:
                        checks[field] = extras[field]
                self.operations.append(checks)

            # List the operations performed up to the time of the error in order
            if "result_codes" in extras:
                result_codes = extras["result_codes"]
                if "transaction" in result_codes:
                    self.tx_codes = result_codes["transaction"]
                    self.message = tx_codes_map[self.tx_codes]
                if "operations" in result_codes:
                    for index, operation in enumerate(result_codes["operations"]):
                        op_details = MESSAGES["NO_OPERATION_DETAILS"]
                        if operation in op_codes_map:
                            op_details = op_codes_map[operation]
                        elif tx_result is not None:
                            op_details = (
                                tx_result.result.results[index]
                                .tr.type.__str__()
                                .replace("OperationType.", "")
                            )
                        operation = {
                            "index": index,
                            "code": operation,
                            "detail": op_details,
                        }

                        # Add operation details context -  TO BE IMPLEMENTED [Things like wallet etc]
                        #
                        # if envelope_xdr is not None:
                        #     operation["context"] = envelope_xdr.transaction.operations[
                        #         index
                        #     ].__str__()

                        self.operations.append(operation)

    def has_any_info(self):
        """
        Checks if any info is available
        """
        return any(
            [
                self.get_title(),
                self.get_message(),
                self.get_operations(),
                self.get_more_details(),
            ]
        )

    def get_stellar_error(self):
        return self.stellar_error

    def get_message(self):
        return self.message

    def get_operations(self):
        return self.operations

    def get_status(self):
        return self.status

    def get_envelope(self):
        return self.envelope

    def get_tx_codes(self):
        return self.tx_codes

    def get_title(self):
        return self.title

    def get_more_details(self):
        return self.more_details

    def as_dict(self):
        """
        Returns a dict representation of the error
        """
        if self.has_any_info():
            return {
                "title": self.get_title(),
                "status": self.get_status(),
                "message": self.get_message(),
                "envelope": self.get_envelope(),
                "tx_codes": self.get_tx_codes(),
                "operations": self.get_operations(),
                "more_details": self.get_more_details(),
            }

        return {
            "title": "Can't handle this error",
            "ERROR": self.get_stellar_error(),
        }

    def as_json(self):
        """
        Returns a json representation of the error
        """
        return json.dumps(self.as_dict())

    def __str__(self):
        """
        Returns a string representation of the error
        """
        if self.has_any_info():
            infos = [
                f"Title: {self.get_title()}" if self.get_title() else "",
                f"Status: {self.get_status()}" if self.get_status() else "",
                f"Message: {self.get_message()}" if self.get_message() else "",
                f"Message: {self.get_envelope()}" if self.get_envelope() else "",
                "Operations:"
                + "\n".join(
                    "\t{index}: {code} - {detail}".format(**operation)
                    for operation in self.get_operations()
                )
                if self.get_tx_codes()
                else "",
                f"More details: {self.get_more_details()}"
                if self.get_more_details()
                else "",
            ]
            return "\n".join(filter(lambda x: x, infos))

        return {
            "title": "Can't handle this error",
            "ERROR": self.get_stellar_error(),
        }
