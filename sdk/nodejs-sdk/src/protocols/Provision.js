'use strict'
const utils = require('../utils')
const Protocol = require('./Protocol')
const indy = require('../utils/indy')

module.exports = class Provision extends Protocol {
  constructor (threadId = null) {
    const msgFamily = 'agent-provisioning'
    const msgFamilyVersion = '0.6'
    const msgQualifier = utils.constants.EVERNYM_MSG_QUALIFIER
    super(msgFamily, msgFamilyVersion, msgQualifier, threadId)

    this.msgNames = {
      CREATE_AGENT: 'CREATE_AGENT'
    }
  }

  async provisionSdkMsg (context) {
    const msg = this._getBaseMessage(this.msgNames.CREATE_AGENT);
    [context.sdkPairwiseDID, context.sdkPairwiseVerkey] = await indy.newDid(context)
    msg.fromDID = context.sdkPairwiseDID
    msg.fromDIDVerKey = context.sdkPairwiseVerkey
    return msg
  }

  async provisionSdkMsgPacked (context) {
    return this.getMessageBytes(context, await this.provisionSdkMsg(context))
  }

  async provisionSdk (context) {
    const packedMessage = await this.provisionSdkMsgPacked(context)
    const rawResponse = await utils.sendPackedMessage(context, packedMessage)
    const jweBytes = (new TextEncoder()).encode(rawResponse)
    const response = await utils.unpackMessage(context, jweBytes)
    context.verityPairwiseDID = response.message.withPairwiseDID
    context.verityPairwiseVerkey = response.message.withPairwiseDIDVerKey
    return context
  }
}
