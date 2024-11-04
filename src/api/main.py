from typing import TypeAlias, Tuple
import logging
import hashlib
import flask
import hashlib
from io import BytesIO
from datetime import datetime, timedelta
import PIL
import base64
import numpy as np

from web3 import Web3, HTTPProvider

import src.api.errors as errs
from src.contracts.oracle import OracleContract, ContestContract
from src.api.comparison import get_claim_from_embedding
from src.extractor.comparison import get_distance_squared
from src.extractor.embedding import FeatureExtractor, FaceExtractionStatus, DiscretizedFeatureVector
from src.extractor.base64 import decode_base64
from src.config.env import EnvConfig
from src.issuer.connector import IssuerConnector
from src.model.claim import Claim
from src.model.contest import Contest
from src.model.participants import Participant

app = flask.Flask(__name__)
cfg = EnvConfig()

Response: TypeAlias = Tuple[dict, int] # Just a type alias for the response

def run_api() -> None:
    """
    Runs the API for serving feature extraction method
    """
    
    app.run(port=cfg.api_port, debug=True)

@app.route("/integrations/face-extractor-svc/extract", methods=["POST"])
def extract_features() -> None:
    def jsonify_error(err: errs.ErrorResponse) -> Response:
        json_err, status_code = err
        return flask.jsonify(json_err), status_code
    
    # Returning an error if got a wrong method
    if flask.request.method != "POST":
        return jsonify_error(errs.INVALID_METHOD)
    
    # Asserting that the request has the necessary data
    def validate_request() -> bool:
        if "data" not in flask.request.json:
            return False
        data = flask.request.json["data"]
        if "attributes" not in data:
            return False
        attributes = data["attributes"]
        return ("did" in attributes
            and "user_id" in attributes
            and "public_key" in attributes
            and "metadata" in attributes)

    if not validate_request():
        logging.error("Bad request!")
        return jsonify_error(errs.BAD_REQUEST)
    
    # Getting attributes
    attributes = flask.request.json["data"]["attributes"]
    did = attributes["did"]
    user_id = attributes["user_id"]
    public_key = attributes["public_key"]
    metadata = attributes["metadata"]
    image_base64 = attributes["image"]
    
    # Creating connector with the issuer service
    connector = IssuerConnector(cfg.issuer_base_url, cfg.issuer_id)
    logging.error('3')
    # Decoding the image and processing it
    try:
        img = decode_base64(image_base64)
        extractor = FeatureExtractor(img)
        emb, status = extractor.extract_features()
        
        # Returning the status if something bad happenned
        match status:
            case FaceExtractionStatus.NO_FACE_FOUND:
                return jsonify_error(errs.NO_FACE_FOUND)
            case FaceExtractionStatus.TOO_MANY_PEOPLE:
                return jsonify_error(errs.TOO_MANY_PEOPLE)
        
        # Verifying that the claim does not already exist or if it exists, it
        # has not been submitted to the issuer
        closest_claim = get_claim_from_embedding(emb)
        is_revoke = closest_claim is not None
        
        if is_revoke and closest_claim['is_submitted']:
            connector.revoke_claim(closest_claim['claim_id']) 
    except Exception as exception:
        logging.error(f"Failed to process the image: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)
    
    # Saving the claim to the database
    try:
        emb_string = str(emb)
        emb_hash = hashlib.sha256(emb_string.encode()).hexdigest()
        
        if not is_revoke:
            claim = Claim.create(user_id=user_id, 
                                vector=emb_string, 
                                metadata=metadata, 
                                pk=public_key, 
                                claim_id="",
                                is_submitted=False)
            claim.save()
    except Exception as exception:
        logging.error(f"Failed to save the claim: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)
    
    # Making request to the issuer
    try:
        claim_id = connector.create_credential({
            "user_id": user_id,
            "embedding": emb_hash,
            "public_key": public_key,
            "did": did,
            "metadata": metadata
        })
    except Exception as exception:
        logging.error(f"Failed to send data to the issuer: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)
    
    # Updating that the claim was submitted
    try:
        str_to_update = emb_string if not is_revoke else closest_claim['vector']
        q = Claim.update(is_submitted=True, claim_id=claim_id).where(Claim.vector == str_to_update)
        q.execute()
        logging.error('7')
        # TODO: make in a single update
        if is_revoke:
            q = Claim.update(user_id=user_id, 
                vector=emb_string, 
                metadata=metadata, 
                pk=public_key).where(Claim.vector == closest_claim['vector'])
            q.execute()
        
        response_user_id = None
        if is_revoke:
            response_user_id = closest_claim['user_id']
        return form_extract_response(emb_string, claim_id=claim_id, user_id=response_user_id)
    except Exception as exception:
        logging.error(f"Failed while finalizing the request: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)
    
@app.route("/integrations/face-extractor-svc/pk-from-image", methods=["POST"])
def get_public_key_from_image() -> None:
    def jsonify_error(err: errs.ErrorResponse) -> Response:
        json_err, status_code = err
        return flask.jsonify(json_err), status_code
    
    # Returning an error if got a wrong method
    if flask.request.method != "POST":
        return jsonify_error(errs.INVALID_METHOD)
    
    # Asserting that the request has the necessary data
    def validate_request() -> bool:
        if "data" not in flask.request.json:
            return False
        data = flask.request.json["data"]
        if "attributes" not in data:
            return False
        attributes = data["attributes"]
        return "image" in attributes

    if not validate_request():
        logging.error("Bad request!")
        return jsonify_error(errs.BAD_REQUEST)
    
    # Getting attributes
    attributes = flask.request.json["data"]["attributes"]
    image_base64 = attributes["image"]
    
    # Decoding the image and processing it
    try:
        img = decode_base64(image_base64)
        extractor = FeatureExtractor(img)
        emb, status = extractor.extract_features()
        # Returning the status if something bad happenned
        match status:
            case FaceExtractionStatus.NO_FACE_FOUND:
                return jsonify_error(errs.NO_FACE_FOUND)
            case FaceExtractionStatus.TOO_MANY_PEOPLE:
                return jsonify_error(errs.TOO_MANY_PEOPLE)
        
        # Verifying that the claim does exist
        closest_claim = get_claim_from_embedding(emb)
        claim_exists = closest_claim is not None
        
        if not claim_exists:
            return jsonify_error(errs.ACCOUNT_DOES_NOT_EXIST)
    except Exception as exception:
        logging.error(f"Failed to process the image: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)

    return form_pk_response(closest_claim['pk'], closest_claim['metadata'], closest_claim['user_id'])

@app.route("/integrations/face-extractor-svc/contest/register", methods = ["POST"])
def register() -> Response:
    def jsonify_error(err: errs.ErrorResponse) -> Response:
        json_err, status_code = err
        return flask.jsonify(json_err), status_code

    image_base64 = flask.request.json["imageBase64"]
    proof = flask.request.json["proof"]
    name = flask.request.json["name"]

    if None in [image_base64, proof, name]:
        logging.info(f"User provided request without required fields. got={flask.request.json}")
        return jsonify_error(errs.BAD_REQUEST)

    image_bytes = decode_base64(image_base64)
    image_bytes_raw = base64.b64decode(image_base64)

    hasher = hashlib.sha3_256()
    hasher.update(image_bytes)
    hexhash = hasher.hexdigest()
    hash = hasher.digest()
    logging.info(f"Got image with hash={hexhash}")

    # Decoding the image and processing it
    try:
        extractor = FeatureExtractor(image_bytes)
        emb, status = extractor.extract_discrete_features()
        # Returning the status if something bad happenned
        match status:
            case FaceExtractionStatus.NO_FACE_FOUND:
                return jsonify_error(errs.NO_FACE_FOUND)
            case FaceExtractionStatus.TOO_MANY_PEOPLE:
                return jsonify_error(errs.TOO_MANY_PEOPLE)
        
        logging.debug(f"Got feature vector: {emb}")
    except Exception as exception:
        logging.error(f"Failed to process the image: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)

    oracle = OracleContract(cfg.eth_provider, cfg.oracle_address, cfg.private_key)

    # check if hash was already published
    if not oracle.isoraclesubmitted(hash):
        txid = oracle.submit(hash, emb)
        oracle.w3.eth.wait_for_transaction_receipt(txid)
        logging.info(f"Sent sumbit {txid=} {hash=}")
        # for demo, as we have only one comittee member, we finalize round
        # immidiatly, but in future it can be only possible after some delay.
        txid = oracle.finalizeround(hash)
        oracle.w3.eth.wait_for_transaction_receipt(txid)
        logging.info(f"Sent finalizeRound {txid=} {hash=}")
    
    contest = ContestContract(cfg.eth_provider, cfg.contest_address, cfg.private_key)
    contest_id = contest.latest_contest_id()

    Contest.insert(id=contest_id).on_conflict(action="IGNORE").execute()
    Participant.insert(
        image_hash=hexhash, image_content=BytesIO(image_bytes_raw).getvalue(),
        name=name, reward_address="", proof=proof, feature_vector=emb,
        contest=contest_id,
    ).on_conflict(action="IGNORE").execute()

    if not contest.isparticipantregistered(contest_id, hash):
        txid = contest.register(contest_id, hash, proof, oracle.from_addr)
        logging.info(f"Sent register {txid=} {hash=} {contest_id=}")

    response = {
        "data": {
            "id": 1,
            "type": "image",
            "attributes": {
                "hash": hexhash,
                "feature_vector": emb,
            }
        }
    }

    return response, 200

@app.route("/integrations/face-extractor-svc/contest/winner", methods = ["GET"])
def choose_winner() -> Response:
    contest = ContestContract(cfg.eth_provider, cfg.contest_address, cfg.private_key)
    # oracle = OracleContract(cfg.eth_provider, cfg.contest_address, cfg.private_key)
    contest_id = contest.latest_contest_id()
    features, start, duration, winner = contest.contestinfo(contest_id)

    participants = Participant.select().where(Participant.contest == contest_id)

    part_resp = []
    for participant in participants:
        distance = get_distance_squared(features, participant.feature_vector)
        d_min = 5_000
        d_max = 15_000
        print(distance)
        if distance < d_min:
            coeficient_of_similiarity = 100.0
        elif distance > d_max:
            coeficient_of_similiarity = 0.0
        else:
            coeficient_of_similiarity = (1 - (distance - d_min)/(d_max - d_min)) * 100
            
        
        part_resp.append(dict(
            name=str(participant.name),
            image=str(base64.b64encode(participant.image_content))[2:-1],
            hash=str(participant.image_hash),
            percentage=coeficient_of_similiarity,
        ))
                
    response = dict(
        winningPool=100,
        participants=part_resp
    )

    print(contest_id)
    print(winner)
    if winner != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
        participants = [p for p in Participant.select().where(Participant.image_hash == winner and Participant.contest == contest_id)]
        participant = participants[0]
        response["winner"] = dict(name=participant.name, image_hash=winner.hex())

    return response, 200
        
def form_extract_response(embedding: DiscretizedFeatureVector, claim_id: int, user_id: str = None) -> Response:
    """
    Formats the response to be returned by the API.
    If the `user_id` is None, it means that revoke did not happen.
    """
    
    response = {
        "data": {
            "id" : 1,
            "type": "embedding",
            "attributes": {
                "embedding": embedding,
                "claim_id": claim_id,
            }
        }
    }
    if user_id is not None:
        # Adding user id to the response
        response["data"]["attributes"]["user_id"] = user_id

    return response, 200
    
 
def form_pk_response(public_key: str, metadata: str, user_id: str) -> Response:
    """
    Formats the response to be returned by the API.
    """
    
    return flask.jsonify({
        "data": {
            "id" : 1,
            "type": "pk",
            "attributes": {
                "public_key": public_key,
                "metadata": metadata,
                "user_id": user_id
            }
        }
    }), 200

