/*global _ */

define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events',
    'mail_view/ui/recipients/recipients_input',
    'mail_view/ui/recipients/recipient',
    'mail_view/ui/recipients/recipients_iterator'
  ],
  function (defineComponent, templates, events, RecipientsInput, Recipient, RecipientsIterator) {
    'use strict';

    return defineComponent(recipients);

    function recipients() {
      this.defaultAttrs({
        navigationHandler: '.recipients-navigation-handler'
      });

      function getAddresses(recipients) {
        return _.flatten(_.map(recipients, function (e) { return e.attr.address;}));
      }

      function moveLeft() { this.attr.iterator.moveLeft(); }
      function moveRight() { this.attr.iterator.moveRight(); }
      function deleteCurrentRecipient() {
        this.attr.iterator.deleteCurrent();
        this.addressesUpdated();
      }

      var SPECIAL_KEYS_ACTIONS = {
        8: deleteCurrentRecipient,
        46: deleteCurrentRecipient,
        37: moveLeft,
        39: moveRight
      };

      this.addRecipient = function(recipient) {
        var newRecipient = Recipient.prototype.renderAndPrepend(this.$node, recipient);
        this.attr.recipients.push(newRecipient);
      };

      this.recipientEntered = function (event, recipient) {
        this.addRecipient(recipient);
        this.addressesUpdated();
      };

      this.deleteLastRecipient = function () {
        this.attr.recipients.pop().destroy();
        this.addressesUpdated();
      };

      this.enterNavigationMode = function () {
        this.attr.iterator = new RecipientsIterator({
          elements: this.attr.recipients,
          exitInput: this.attr.input.$node
        });

        this.attr.iterator.current().select();
        this.attr.input.$node.blur();
        this.select('navigationHandler').focus();
      };

      this.leaveNavigationMode = function () {
        if(this.attr.iterator) { this.attr.iterator.current().unselect(); }
        this.attr.iterator = null;
      };

      this.selectLastRecipient = function () {
        if (this.attr.recipients.length === 0) { return; }
        this.enterNavigationMode();
      };

      this.attachInput = function () {
        this.attr.input = RecipientsInput.prototype.attachAndReturn(this.$node.find('input[type=text]'), this.attr.name);
      };

      this.processSpecialKey = function (event) {
        if(SPECIAL_KEYS_ACTIONS.hasOwnProperty(event.which)) { SPECIAL_KEYS_ACTIONS[event.which].apply(this); }
      };

      this.initializeAddresses = function () {
        _.each(_.flatten(this.attr.addresses), function (address) {
          this.addRecipient({ address: address, name: this.attr.name });
        }.bind(this));
      };

      this.addressesUpdated = function() {
        this.trigger(document, events.ui.recipients.updated, {recipientsName: this.attr.name, newRecipients: getAddresses(this.attr.recipients)});
      };

      this.doCompleteRecipients = function () {
        var address = this.attr.input.$node.val();
        if (!_.isEmpty(address)) {
          var recipient = Recipient.prototype.renderAndPrepend(this.$node, { name: this.attr.name, address: address });
          this.attr.recipients.push(recipient);
          this.attr.input.$node.val('');
        }

        this.trigger(document, events.ui.recipients.updated, {
          recipientsName: this.attr.name,
          newRecipients: getAddresses(this.attr.recipients),
          skipSaveDraft: true
        });

      };

      this.after('initialize', function () {
        this.attr.recipients = [];
        this.attachInput();
        this.initializeAddresses();

        this.on(events.ui.recipients.deleteLast, this.deleteLastRecipient);
        this.on(events.ui.recipients.selectLast, this.selectLastRecipient);
        this.on(events.ui.recipients.entered, this.recipientEntered);

        this.on(document, events.ui.recipients.doCompleteInput, this.doCompleteRecipients);

        this.on(this.attr.input.$node, 'focus', this.leaveNavigationMode);
        this.on(this.select('navigationHandler'), 'keydown', this.processSpecialKey);

        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
      });
    }
  });