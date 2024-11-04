from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional
import logging

from web3 import Web3, HTTPProvider
from web3.middleware import SignAndSendRawMiddlewareBuilder
from web3.exceptions import ContractLogicError

class Contract:
    ABI = ""

    def __init__(self, url: str, address: str, private_key: str) -> None:
        """
        Construct new oracle contract provider from web3 provider and address.
        """
        
        w3 = Web3(HTTPProvider(url))

        act1 = w3.eth.account.from_key(private_key)

        w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(act1), layer=0)
        w3.eth.set_gas_price_strategy(lambda w3, transaction_params: Web3.to_wei(0, 'gwei'))
        
        self.contract = w3.eth.contract(address=address, abi=self.ABI)
        self.w3 = w3
        self.from_addr = act1.address
        self.tx_params = {
            "gas": 20_000_000,
            "from": self.from_addr,
            "gasPrice": 0,
        }

class OracleContract(Contract):
    ABI = """[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"newOwners","type":"address[]"}],"name":"OwnersAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"removedOwners","type":"address[]"}],"name":"OwnersRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"MIN_SUBMISSIONS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ROUND_TIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"VALIDATION_TIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"__FeatureVectorOracle_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"newOwners_","type":"address[]"}],"name":"addOwners","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash_","type":"bytes32"}],"name":"finalizeRound","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash_","type":"bytes32"}],"name":"getFeatureVector","outputs":[{"internalType":"uint8[128]","name":"","type":"uint8[128]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"}],"name":"isOracleSubmitted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash_","type":"bytes32"},{"internalType":"address","name":"oracle_","type":"address"}],"name":"isOracleSubmittedForRound","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"address_","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash_","type":"bytes32"},{"internalType":"address","name":"toSliceAddress_","type":"address"}],"name":"punish","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"oldOwners_","type":"address[]"}],"name":"removeOwners","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"roundData","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"roundOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"rounds","outputs":[{"internalType":"uint64","name":"startTime","type":"uint64"},{"internalType":"uint64","name":"roundTime","type":"uint64"},{"internalType":"uint64","name":"validationTime","type":"uint64"},{"internalType":"bool","name":"isFinalized","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash_","type":"bytes32"},{"internalType":"uint8[128]","name":"inference_","type":"uint8[128]"}],"name":"submit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]"""

    def submit(self, hash: bytes, feature_vector: list[int]) -> bytes:
        """
        Publish new member for the contest
        """
        
        return self.contract.functions.submit(hash, feature_vector).transact(self.tx_params)

    def finalizeround(self, hash: bytes) -> bytes:
        """
        Send round finalization transaction which stops finding the middle
        feature vector between comittee.
        """

        return self.contract.functions.finalizeRound(hash).transact(self.tx_params)

    def isoraclesubmitted(self, image_hash: bytes) -> bool:
        self.contract.functions.isOracleSubmitted(image_hash, str(self.from_addr)).call()

    def getfeaturevector(self, hash: bytes) -> Optional[list[int]]:
        try:
            return self.contract.functions.getFeatureVector(hash).call()
        except ContractLogicError as e:
            logging.info(f"Failed to get feature vector from contract: {e}")
            return None

class ContestContract(Contract):
    ABI = """[{"inputs":[{"internalType":"address","name":"contestVerifier_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"newOwners","type":"address[]"}],"name":"OwnersAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"removedOwners","type":"address[]"}],"name":"OwnersRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"CONTEST_VERIFIER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"featureOracle_","type":"address"}],"name":"__Contest_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"newOwners_","type":"address[]"}],"name":"addOwners","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8[128]","name":"features_","type":"uint8[128]"},{"internalType":"uint8[128]","name":"referenceVector_","type":"uint8[128]"}],"name":"calculateDistance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"}],"name":"chooseWinner","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"contestParticipants","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"contestParticipantsData","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"contestParticipantsRegistered","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"contests","outputs":[{"internalType":"uint64","name":"startTime","type":"uint64"},{"internalType":"uint64","name":"duration","type":"uint64"},{"internalType":"bytes32","name":"winner","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8[128]","name":"referenceVector_","type":"uint8[128]"},{"internalType":"uint64","name":"duration_","type":"uint64"}],"name":"createContest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"featureOracle","outputs":[{"internalType":"contract FeatureVectorOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"}],"name":"finalizeContest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"}],"name":"getContestInfo","outputs":[{"internalType":"uint8[128]","name":"","type":"uint8[128]"},{"internalType":"uint64","name":"","type":"uint64"},{"internalType":"uint64","name":"","type":"uint64"},{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"},{"internalType":"bytes32","name":"participant_","type":"bytes32"}],"name":"getContestParticipantData","outputs":[{"internalType":"uint8[128]","name":"","type":"uint8[128]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"}],"name":"getContestParticipants","outputs":[{"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"address_","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"},{"internalType":"bytes32","name":"participant_","type":"bytes32"}],"name":"isParticipantRegistered","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastContestId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"contestId_","type":"uint256"},{"internalType":"bytes32","name":"hash_","type":"bytes32"},{"internalType":"address","name":"rewardAddress_","type":"address"},{"components":[{"internalType":"uint256[2]","name":"a","type":"uint256[2]"},{"internalType":"uint256[2][2]","name":"b","type":"uint256[2][2]"},{"internalType":"uint256[2]","name":"c","type":"uint256[2]"}],"internalType":"struct VerifierHelper.ProofPoints","name":"zkPoints_","type":"tuple"},{"internalType":"uint256[]","name":"pubSignals_","type":"uint256[]"}],"name":"register","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"oldOwners_","type":"address[]"}],"name":"removeOwners","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]"""

    def register(self, contest_id: int, hash: bytes, proof: dict, reward_address: bytes) -> None:
        """
        Publish register to contest transcation on-chain.
        """

        a = list(map(int, proof["proof"]["pi_a"]))
        c = list(map(int, proof["proof"]["pi_c"]))
        b = proof["proof"]["pi_b"]

        b[0][0], b[0][1] = int(b[0][1]), int(b[0][0])
        b[1][0], b[1][1] = int(b[1][1]), int(b[1][0])

        signals = list(map(int, proof["pub_signals"]))

        return self.contract.functions.register(contest_id, hash, reward_address, (a[:2], b[:2], c[:2]), signals).transact(self.tx_params)

    def isparticipantregistered(self, contest_id: int, hash: bytes) -> bool:
        """
        Read the participant reward address by contest id and image hash.
        """
        
        return self.contract.functions.isParticipantRegistered(contest_id, hash).call()

    def contestinfo(self, contest_id: int) -> (bytes, datetime, timedelta):
        """
        Read 
        """

        features, start, duration, winner = self.contract.functions.getContestInfo(contest_id).call()
        return features, datetime.fromtimestamp(start), timedelta(seconds=duration), winner

    def latest_contest_id(self) -> int:
        """
        Read id of the latest contest.
        """

        return self.contract.functions.lastContestId().call() - 1

    def choosewinner(self, contest_id: int) -> bytes:
        """
        Send transaciton which chooses winner for contest.
        """

        return self.contract.functions.chooseWinner(contest_id).call(self.tx_params)


    def createcontest(self, feature_vector: list[int], duration: int) -> bytes:
        return self.contract.functions.createContest(feature_vector, duration).transact(self.tx_params)

    def finalizecontest(self, contest_id: int) -> bytes:
        return self.contract.functions.finalizeContest(contest_id).transact(self.tx_params)
