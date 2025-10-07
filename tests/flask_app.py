import datetime
import dataclasses
from dataclasses_json import DataClassJsonMixin
from itertools import count
from typing import Any, Dict, List
from flask import Flask, g, request, jsonify


@dataclasses.dataclass
class Mailbox(DataClassJsonMixin):
    id: int
    address: str
    last_activity: str


@dataclasses.dataclass
class Email(DataClassJsonMixin):
    id: int
    mailbox_id: int
    fromaddr: str
    message: str
    timestamp: str
    sent_via_ssl: bool
    read: bool


def app_initializations() -> None:
    g.mailboxes = {}
    g.emails = {}
    g.mailboxes_count = count(1)


def create_app() -> Flask:
    app = Flask("MailboxerSimulation")

    def _get_success_response() -> Dict[str, str]:
        return {"result": "ok"}

    def _get_paginated_response(objects: List[Any]) -> Dict[str, Any]:
        page = request.args.get("page", default=1, type=int)
        page_size = request.args.get("page_size", default=1000, type=int)
        result_objects = objects[(page - 1) * page_size : page_size * page]
        return {
            "metadata": {"total_num_objects": len(objects)},
            "result": result_objects,
        }

    def now() -> str:
        return datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    @app.route("/v2/mailboxes", methods=["GET"])
    def query_mailboxes():
        sorted_mailboxes = sorted(
            g.mailboxes.values(), key=lambda mailbox: mailbox.address
        )
        return _get_paginated_response(sorted_mailboxes)

    @app.route("/v2/mailboxes", methods=["POST"])
    def create_mailbox():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Not JSON body"}), 400
        address = data.get("address")
        if not isinstance(address, str):
            return jsonify({"error": "Invalid address {address!r}"}), 400

        g.mailboxes[address] = Mailbox(
            id=next(g.mailboxes_count), address=address, last_activity=now()
        )
        return _get_success_response()

    @app.route("/v2/mailboxes/<address>", methods=["DELETE"])
    def delete_mailbox(address: str):
        g.mailboxes.pop(address, None)
        return _get_success_response()

    @app.route("/v2/mailboxes/<address>/emails", methods=["GET"])
    def query_mailbox_emails(address: str):
        emails = g.emails.get(address, [])
        return _get_paginated_response(emails)

    @app.route("/v2/vacuum", methods=["POST"])
    def vacuum():
        return _get_success_response()

    return app
