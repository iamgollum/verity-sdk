import pytest

from test.test_utils import get_test_config, send_stub, cleanup
from src.protocols.CommittedAnswer import CommittedAnswer
from src.utils import unpack_forward_message, COMMUNITY_MSG_QUALIFIER
from src.utils.Context import Context

for_relationship = 'some_did'
question_text = 'Are you trying to login to acme.com?'
question_detail = 'IP Address: 56.24.11.126'
valid_responses = ['Yes', 'No, that\'s not me!']
signature_required = True


def test_init():
    committed_answer = CommittedAnswer(for_relationship, None, question_text, question_detail, valid_responses,
                                       signature_required)

    assert committed_answer.for_relationship == for_relationship
    assert committed_answer.question_text == question_text
    assert committed_answer.question_detail == question_detail
    assert committed_answer.valid_responses == valid_responses
    assert committed_answer.signature_required == signature_required


@pytest.mark.asyncio
async def test_ask():
    context = await Context.create(await get_test_config())
    committed_answer = CommittedAnswer(for_relationship, None, question_text, question_detail, valid_responses,
                                       signature_required)
    committed_answer.send = send_stub
    msg = await committed_answer.ask(context)
    msg = await unpack_forward_message(context, msg)

    assert msg['@type'] == '{};spec/{}/{}/{}'.format(
        COMMUNITY_MSG_QUALIFIER,
        CommittedAnswer.MSG_FAMILY,
        CommittedAnswer.MSG_FAMILY_VERSION,
        CommittedAnswer.ASK_QUESTION
    )
    assert msg['@id'] is not None
    assert msg['~thread'] is not None
    assert msg['~thread']['thid'] is not None
    assert msg['~for_relationship'] == for_relationship
    assert msg['text'] == question_text
    assert msg['detail'] == question_detail
    assert msg['valid_responses'] == valid_responses
    assert msg['signature_required'] == signature_required

    await cleanup(context)


@pytest.mark.asyncio
async def test_status():
    context = await Context.create(await get_test_config())
    committed_answer = CommittedAnswer(for_relationship, None, question_text, question_detail, valid_responses,
                                       signature_required)
    committed_answer.send = send_stub
    msg = await committed_answer.status(context)
    msg = await unpack_forward_message(context, msg)

    assert msg['@type'] == '{};spec/{}/{}/{}'.format(
        COMMUNITY_MSG_QUALIFIER,
        CommittedAnswer.MSG_FAMILY,
        CommittedAnswer.MSG_FAMILY_VERSION,
        CommittedAnswer.GET_STATUS
    )
    assert msg['@id'] is not None
    assert msg['~for_relationship'] == for_relationship
    assert msg['~thread'] is not None
    assert msg['~thread']['thid'] is not None

    await cleanup(context)
